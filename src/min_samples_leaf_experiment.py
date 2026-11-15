"""Random Forest min_samples_leaf sensitivity experiment.

Run from the repository root:
    python src/min_samples_leaf_experiment.py

This is a separate experiment. It does not modify results/main. Default dataset: Adult
(results/min_samples_leaf/). Optional argument: another dataset name, e.g.
    python src/min_samples_leaf_experiment.py synthetic_dep   -> results/min_samples_leaf_synthetic_dep/
"""
import json
import sys
import time
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

from data import build_preprocessor, load_dataset
from explain import (
    Explainer,
    default_eval_neighborhood,
    sample_dependency_aware,
    sample_neighbors,
    rank_stability,
)

LEAF_VALUES = [1, 2, 5, 10, 20]
BUDGETS = [200, 500]
SEEDS = list(range(5))
N_CASES = 100
K_EVAL = 200
N_BOOT = 2000
BOOT_SEED = 0
DATASET = sys.argv[1] if len(sys.argv) > 1 else "adult"
OUT = Path("results/min_samples_leaf" + ("" if DATASET == "adult" else f"_{DATASET}"))
OUT.mkdir(parents=True, exist_ok=True)

GRID_COLUMNS = [
    "dataset", "model", "min_samples_leaf", "condition", "n", "case", "seed",
    "fidelity", "fit_r2", "mean_nn_dist", "frac_seen_combo",
    "mean_dist_to_query", "mean_weight", "width", "runtime_s", "wall_s",
    "prediction", "surrogate_prediction",
]


def fit_rf(ds, min_samples_leaf):
    """Match the project RF settings, changing only min_samples_leaf."""
    pre = build_preprocessor(ds.numeric, ds.categorical)
    clf = RandomForestClassifier(
        n_estimators=200,
        min_samples_leaf=min_samples_leaf,
        n_jobs=-1,
        random_state=0,
    )
    model = Pipeline([("pre", pre), ("clf", clf)])
    t0 = time.perf_counter()
    model.fit(ds.X_train, ds.y_train)
    elapsed = time.perf_counter() - t0
    print(
        f"{DATASET} RF min_samples_leaf={min_samples_leaf}: "
        f"dev acc {model.score(ds.X_dev, ds.y_dev):.4f}; fit {elapsed:.1f}s",
        flush=True,
    )
    return model, elapsed


def bootstrap_ci(values, n_boot=N_BOOT, seed=BOOT_SEED):
    values = np.asarray(values, dtype=float)
    rng = np.random.default_rng(seed)
    means = np.empty(n_boot, dtype=float)
    for b in range(n_boot):
        means[b] = rng.choice(values, size=len(values), replace=True).mean()
    return float(np.quantile(means, 0.025)), float(np.quantile(means, 0.975))


def main():
    total_start = time.perf_counter()
    ds = load_dataset(DATASET)
    if len(ds.explain_idx) < N_CASES:
        raise ValueError(f"Expected at least {N_CASES} explanation cases")

    all_rows = []
    all_coefs = {}
    case_total = len(LEAF_VALUES) * N_CASES

    for li, leaf in enumerate(LEAF_VALUES):
        model, fit_seconds = fit_rf(ds, leaf)
        pre = model.named_steps["pre"]
        names = pre.get_feature_names_out().tolist()
        Z_dev = pre.transform(ds.X_dev)
        explainer = Explainer(
            lambda X, model=model: model.predict_proba(X)[:, 1],
            pre.transform,
            ds.X_train,
            ds.numeric,
            ds.categorical,
            names,
        )

        # Shape: condition, budget, case, seed, transformed feature.
        coef_tensor = np.full(
            (2, len(BUDGETS), N_CASES, len(SEEDS), len(names)),
            np.nan,
            dtype=float,
        )
        conditions = [
            ("dep_aware", sample_dependency_aware),
            ("neighbors", sample_neighbors),
        ]

        for case_pos, case in enumerate(ds.explain_idx[:N_CASES]):
            x = ds.X_test.iloc[[int(case)]]
            z_x = pre.transform(x)[0]
            eval_X = default_eval_neighborhood(
                z_x, Z_dev, ds.X_dev, k=K_EVAL
            )
            width = float(
                np.median(
                    np.linalg.norm(pre.transform(eval_X) - z_x, axis=1)
                )
            )

            for ci, (condition, sampler) in enumerate(conditions):
                for bi, budget in enumerate(BUDGETS):
                    for si, seed in enumerate(SEEDS):
                        t0 = time.perf_counter()
                        result = explainer.explain(
                            x, sampler, budget, seed, eval_X, width=width
                        )
                        wall = time.perf_counter() - t0
                        coef_tensor[ci, bi, case_pos, si] = result["coef"]
                        validity = result["validity"]
                        all_rows.append({
                            "dataset": DATASET,
                            "model": "rf",
                            "min_samples_leaf": leaf,
                            "condition": condition,
                            "n": budget,
                            "case": int(case),
                            "seed": seed,
                            "fidelity": result["fidelity"],
                            "fit_r2": result["fit_r2"],
                            **validity,
                            "mean_dist_to_query": result["mean_dist_to_query"],
                            "mean_weight": result["mean_weight"],
                            "width": width,
                            "runtime_s": result["runtime_s"],
                            "wall_s": wall,
                            "prediction": result["prediction"],
                            "surrogate_prediction": result["surrogate_prediction"],
                        })

            if (case_pos + 1) % 10 == 0:
                print(
                    f"leaf={leaf}: completed {case_pos + 1}/{N_CASES} cases",
                    flush=True,
                )

        if not np.isfinite(coef_tensor).all():
            raise RuntimeError(
                f"Non-finite coefficients for min_samples_leaf={leaf}"
            )
        all_coefs[leaf] = coef_tensor
        np.save(OUT / f"coefs_leaf_{leaf}.npy", coef_tensor)

    grid = pd.DataFrame(all_rows, columns=GRID_COLUMNS)
    expected = len(LEAF_VALUES) * 2 * len(BUDGETS) * N_CASES * len(SEEDS)
    if len(grid) != expected:
        raise RuntimeError(f"Expected {expected} rows, got {len(grid)}")
    key_cols = ["min_samples_leaf", "condition", "n", "case", "seed"]
    if grid.duplicated(key_cols).any():
        raise RuntimeError("Duplicate experiment rows found")
    if not np.isfinite(grid["fidelity"]).all():
        raise RuntimeError("Non-finite fidelity values found")
    grid.to_csv(OUT / "grid.csv", index=False)

    # Primary summaries use each case's mean across the five sampling seeds.
    case_means = (
        grid.groupby(
            ["min_samples_leaf", "condition", "n", "case"], as_index=False
        )["fidelity"].mean()
    )
    summary_rows = []
    for (leaf, condition, budget), group in case_means.groupby(
        ["min_samples_leaf", "condition", "n"]
    ):
        vals = group["fidelity"].to_numpy()
        summary_rows.append({
            "min_samples_leaf": leaf,
            "condition": condition,
            "n": budget,
            "n_cases": len(vals),
            "fidelity_mean": float(np.mean(vals)),
            "fidelity_median": float(np.median(vals)),
            "fidelity_sd": float(np.std(vals, ddof=1)),
        })

    # Rank stability: per case, across the five seeds, following protocol v1.
    stability_rows = []
    for leaf in LEAF_VALUES:
        C = all_coefs[leaf]
        for ci, condition in enumerate(["dep_aware", "neighbors"]):
            for bi, budget in enumerate(BUDGETS):
                for case_pos, case in enumerate(ds.explain_idx[:N_CASES]):
                    stab = rank_stability(C[ci, bi, case_pos])
                    stability_rows.append({
                        "min_samples_leaf": leaf,
                        "condition": condition,
                        "n": budget,
                        "case": int(case),
                        "rank_stability": stab,
                    })
    stability = pd.DataFrame(stability_rows)
    stability_summary = (
        stability.groupby(
            ["min_samples_leaf", "condition", "n"], as_index=False
        )["rank_stability"].mean()
        .rename(columns={"rank_stability": "rank_stability_mean"})
    )
    summary = pd.DataFrame(summary_rows).merge(
        stability_summary,
        on=["min_samples_leaf", "condition", "n"],
        how="left",
    )
    summary.to_csv(OUT / "summary.csv", index=False)

    # Paired comparison: average over seeds within each case, then bootstrap cases.
    paired_rows = []
    for leaf in LEAF_VALUES:
        for budget in BUDGETS:
            p = case_means[
                (case_means["min_samples_leaf"] == leaf)
                & (case_means["n"] == budget)
            ].pivot(index="case", columns="condition", values="fidelity")
            delta = (p["dep_aware"] - p["neighbors"]).to_numpy()
            lo, hi = bootstrap_ci(delta, seed=BOOT_SEED + leaf + budget)
            paired_rows.append({
                "min_samples_leaf": leaf,
                "n": budget,
                "comparison": "dep_aware_minus_neighbors",
                "mean_delta": float(delta.mean()),
                "ci95_low": lo,
                "ci95_high": hi,
                "dep_aware_wins": int(np.sum(delta > 0)),
                "n_cases": len(delta),
            })
    paired = pd.DataFrame(paired_rows)
    paired.to_csv(OUT / "paired.csv", index=False)

    elapsed = time.perf_counter() - total_start
    print("\nSummary:")
    print(summary.sort_values(["n", "min_samples_leaf", "condition"]).to_string(index=False))
    print("\nPaired comparison:")
    print(paired.to_string(index=False))
    print(f"\nSaved results to {OUT.resolve()}; elapsed {elapsed / 60:.1f} min")


if __name__ == "__main__":
    main()
