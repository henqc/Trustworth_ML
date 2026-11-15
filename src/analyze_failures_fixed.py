"""Diagnose low-fidelity Adult explanations using the ORIGINAL saved main-grid metrics.

Run from the repository root:
    python src/analyze_failures.py

This version intentionally does NOT rerun explanation sampling. It reconstructs only
the fixed evaluation neighborhoods, computes the black-box weighted target variance,
then derives weighted MSE from the original saved fidelity:

    weighted_R2 = 1 - weighted_MSE / weighted_target_variance
    weighted_MSE = (1 - saved_weighted_R2) * weighted_target_variance

This avoids changing seeds, sampling behavior, package-dependent RNG details, or
surrogate fits when diagnosing the already-completed experiment.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from data import fit_models, load_dataset  # noqa: E402
from explain import default_eval_neighborhood, kernel_weights  # noqa: E402

K_EVAL = 200
CONDITIONS = ("independent", "dep_aware")


def weighted_target_stats(y: np.ndarray, weights: np.ndarray) -> dict:
    y = np.asarray(y, dtype=float).reshape(-1)
    weights = np.asarray(weights, dtype=float).reshape(-1)
    if len(y) != len(weights) or not np.isfinite(y).all():
        raise ValueError("Invalid evaluation predictions or weights")
    if not np.isfinite(weights).all() or weights.sum() <= 0:
        raise ValueError("Invalid evaluation weights")
    w = weights / weights.sum()
    mean = float(np.sum(w * y))
    var = float(np.sum(w * (y - mean) ** 2))
    return {
        "eval_weighted_mean": mean,
        "eval_weighted_variance": var,
        "eval_weighted_sd": float(np.sqrt(var)),
        "eval_weighted_min": float(np.min(y)),
        "eval_weighted_max": float(np.max(y)),
        "eval_weighted_range": float(np.max(y) - np.min(y)),
        "eval_effective_n": float(1.0 / np.sum(w ** 2)),
    }


def diagnose_model(model_name, ds, model, grid, failures):
    pre = model[:-1]
    Z_dev = np.asarray(pre.transform(ds.X_dev), dtype=float)
    cases = [int(c) for c in ds.explain_idx[:100]]
    gm = grid[(grid.dataset == "adult") & (grid.model == model_name)].copy()
    if gm.empty:
        raise ValueError(f"No Adult/{model_name} rows in grid.csv")
    if set(gm.case.astype(int).unique()) != set(cases):
        raise ValueError(f"Adult/{model_name}: grid cases do not match the frozen 100 cases")

    eval_rows = []
    for case in cases:
        x = ds.X_test.iloc[[case]]
        z_x = np.asarray(pre.transform(x), dtype=float)[0]
        eval_X = default_eval_neighborhood(z_x, Z_dev, ds.X_dev, k=K_EVAL)
        z_eval = np.asarray(pre.transform(eval_X), dtype=float)
        width = float(np.median(np.linalg.norm(z_eval - z_x, axis=1)))
        if not np.isfinite(width) or width <= 0:
            raise ValueError(f"Invalid kernel width for case {case}: {width}")
        f_eval = np.asarray(model.predict_proba(eval_X)[:, 1], dtype=float)
        dist = np.linalg.norm(z_eval - z_x, axis=1)
        weights = kernel_weights(dist, width)
        stats = weighted_target_stats(f_eval, weights)
        eval_rows.append({
            "dataset": "adult", "model": model_name, "case": case,
            "query_prediction": float(model.predict_proba(x)[:, 1][0]),
            "eval_n": len(eval_X), "kernel_width": width, **stats,
        })

    ev = pd.DataFrame(eval_rows)
    ev["variance_percentile"] = (
        ev.eval_weighted_variance.rank(pct=True, method="average") * 100
    )
    ev["bottom_decile_variance"] = ev.variance_percentile <= 10.0

    # Keep the original experiment's fidelity values. The identity above gives
    # MSE exactly, without trying to regenerate the stochastic surrogate fit.
    focus = gm[gm.condition.isin(CONDITIONS)].copy()
    focus = focus.merge(
        ev, on=["dataset", "model", "case"], how="left", validate="many_to_one"
    )
    if focus.eval_weighted_variance.isna().any():
        raise ValueError("Could not match some saved grid rows to evaluation diagnostics")
    focus["weighted_mse"] = (
        (1.0 - focus.fidelity) * focus.eval_weighted_variance
    )
    # Guard against tiny negative values from floating-point R² slightly > 1.
    focus["weighted_mse"] = focus.weighted_mse.clip(lower=0.0)
    focus["weighted_rmse"] = np.sqrt(focus.weighted_mse)
    focus["fidelity_source"] = "original results/main/grid.csv"

    fail = failures[
        (failures.dataset == "adult") & (failures.model == model_name)
        & failures.condition.isin(CONDITIONS)
    ][["condition", "n", "case", "fidelity"]].rename(
        columns={"fidelity": "listed_failure_fidelity"}
    )
    focus = focus.merge(
        fail, on=["condition", "n", "case"], how="left", validate="many_to_one"
    )
    focus["is_listed_failure"] = focus.listed_failure_fidelity.notna()
    return ev, focus


def build_report(ev, diag):
    lines = [
        "# Adult failure analysis", "",
        "This diagnostic preserves the original main-grid fidelity values. It reconstructs "
        "the fixed 200-record dev evaluation neighborhoods and computes the weighted variance "
        "of black-box predictions in each neighborhood.", "",
        "Weighted MSE is derived algebraically from the saved weighted R² and the reconstructed "
        "weighted target variance: MSE = (1 - R²) × variance. No explanation sampler is rerun.", "",
        "## Evaluation-neighborhood prediction variance", "",
        "| model | mean weighted variance | median | 10th percentile | 90th percentile |",
        "|---|---:|---:|---:|---:|",
    ]
    for model, g in ev.groupby("model", sort=True):
        v = g.eval_weighted_variance
        lines.append(
            f"| {model} | {v.mean():.6g} | {v.median():.6g} | "
            f"{v.quantile(.1):.6g} | {v.quantile(.9):.6g} |"
        )
    lines += [
        "", "## Listed low-fidelity cases", "",
        "These are the low-fidelity cases already identified in failures.csv. No cases are "
        "removed from the main results.", "",
        "| model | condition | budget | case | saved R² | weighted variance | variance percentile | weighted MSE | weighted RMSE |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    low = diag[diag.is_listed_failure].sort_values(
        ["model", "condition", "n", "listed_failure_fidelity"]
    )
    for r in low.itertuples():
        lines.append(
            f"| {r.model} | {r.condition} | {r.n} | {r.case} | {r.fidelity:.4f} | "
            f"{r.eval_weighted_variance:.6g} | {r.variance_percentile:.1f} | "
            f"{r.weighted_mse:.6g} | {r.weighted_rmse:.6g} |"
        )
    lines += [
        "", "## Mean metrics by model, condition, and budget", "",
        "| model | condition | budget | mean saved R² | mean weighted MSE | mean weighted RMSE | mean target variance |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    summary = diag.groupby(["model", "condition", "n"], as_index=False).agg(
        r2=("fidelity", "mean"), mse=("weighted_mse", "mean"),
        rmse=("weighted_rmse", "mean"), variance=("eval_weighted_variance", "mean")
    )
    for r in summary.itertuples():
        lines.append(
            f"| {r.model} | {r.condition} | {r.n} | {r.r2:.4f} | "
            f"{r.mse:.6g} | {r.rmse:.6g} | {r.variance:.6g} |"
        )
    lines += [
        "", "## Interpretation", "",
        "- Weighted R² can become very negative when the black-box target variance in the "
        "evaluation neighborhood is very small.",
        "- Weighted MSE/RMSE show absolute surrogate error on the same neighborhood; read them "
        "alongside target variance rather than replacing R².",
        "- This is a diagnostic only. The original main-grid results are unchanged, and no "
        "low-variance cases are excluded.",
        "- The variance percentile is descriptive; the bottom decile is not an exclusion rule.",
        "",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, default=ROOT / "results" / "main")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "results" / "failure_analysis")
    args = parser.parse_args()
    grid_path, failures_path = args.input_dir / "grid.csv", args.input_dir / "failures.csv"
    if not grid_path.exists() or not failures_path.exists():
        raise FileNotFoundError(f"Expected {grid_path} and {failures_path}; run analyze_grid.py first")

    try:
        ds = load_dataset("adult")
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            "Adult raw data is missing. Place the same adult.data and adult.test files "
            "used for the original experiment in data/adult/."
        ) from exc

    grid, failures = pd.read_csv(grid_path), pd.read_csv(failures_path)
    required = {"dataset", "model", "condition", "n", "case", "seed", "fidelity"}
    missing = required - set(grid.columns)
    if missing:
        raise ValueError(f"grid.csv missing columns: {sorted(missing)}")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    models = fit_models(ds)
    eval_parts, diag_parts = [], []
    for model_name in ("lr", "rf"):
        print(f"Measuring Adult/{model_name} evaluation variance ...", flush=True)
        ev, diag = diagnose_model(model_name, ds, models[model_name], grid, failures)
        eval_parts.append(ev)
        diag_parts.append(diag)
        print(f"  done: {len(ev)} cases; used saved grid fidelity (no explainer reruns)", flush=True)

    ev, diag = pd.concat(eval_parts, ignore_index=True), pd.concat(diag_parts, ignore_index=True)
    ev.to_csv(args.output_dir / "evaluation_variance.csv", index=False)
    diag.to_csv(args.output_dir / "failure_diagnostics_by_seed.csv", index=False)
    # One row per case/condition/budget, averaging only the seed-level MSE values.
    agg = diag.groupby(["dataset", "model", "condition", "n", "case"], as_index=False).agg(
        fidelity_mean=("fidelity", "mean"), fidelity_sd=("fidelity", "std"),
        weighted_mse_mean=("weighted_mse", "mean"), weighted_mse_sd=("weighted_mse", "std"),
        weighted_rmse_mean=("weighted_rmse", "mean"), weighted_rmse_sd=("weighted_rmse", "std"),
        eval_weighted_variance=("eval_weighted_variance", "first"),
        variance_percentile=("variance_percentile", "first"),
        is_listed_failure=("is_listed_failure", "max"),
    )
    agg.to_csv(args.output_dir / "failure_diagnostics.csv", index=False)
    report = build_report(ev, diag)
    (args.output_dir / "failure_analysis.md").write_text(report, encoding="utf-8")
    print("\n" + report)
    print(f"\nOutputs written to: {args.output_dir}")


if __name__ == "__main__":
    main()
