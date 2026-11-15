"""Isolating dependency ablation for Adult/RF.

Run from repository root:
    python src/isolating_ablation.py

Compares the frozen dep_aware sampler with an isolating ablation that:
- uses the same k-nearest anchor pool and anchor-selection probabilities;
- retains the anchor numeric values;
- estimates the same local within-stratum covariance, but uses only its diagonal;
- samples each categorical column independently from its training marginal;
- preserves deterministic numeric/categorical mappings (e.g., education-num | education);
- uses the same scale, locality weighting, evaluation neighborhood, width, budgets and seeds.

Outputs are written separately to results/isolating_ablation/.
"""
from __future__ import annotations
import sys, time
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from data import fit_models, load_dataset
from explain import (
    Explainer, default_eval_neighborhood, kernel_weights,
    sample_dependency_aware,
)

OUT = ROOT / "results" / "isolating_ablation"
BUDGETS = (200, 500)
SEEDS = (0, 1, 2, 3, 4)
K = 200
SCALE = 0.5


def combo_keys(X, categorical):
    if not categorical:
        return np.full(len(X), "")
    return np.array(["|".join(r) for r in X[categorical].to_numpy().astype(str)])


def marginal(X_train, col, n, rng):
    return X_train[col].iloc[rng.integers(len(X_train), size=n)].reset_index(drop=True)


def sample_isolating_ablation(x, X_train, Z_train, z_x, numeric, categorical,
                              n, rng, k=K, scale=SCALE, locked=(), **kwargs):
    """Break categorical block + numeric correlations while retaining local diagonal variance."""
    from sklearn.neighbors import NearestNeighbors

    k_eff = min(k, len(Z_train))
    dist, idx = NearestNeighbors(n_neighbors=k_eff).fit(Z_train).kneighbors(
        np.asarray(z_x).reshape(1, -1)
    )
    idx, dist = idx[0], dist[0]
    p = kernel_weights(dist, 0.75 * np.sqrt(Z_train.shape[1]))
    p = p / p.sum()

    # Same anchor-selection mechanism as the original dependency-aware sampler.
    anchor_pos = rng.choice(len(idx), n, p=p)
    anchor_idx = idx[anchor_pos]
    S = X_train.iloc[anchor_idx].reset_index(drop=True).copy()

    # Destroy the categorical block: independently resample each categorical feature.
    for col in categorical:
        S[col] = marginal(X_train, col, n, rng)

    num_all = X_train[numeric].to_numpy(float)
    anchor_num = num_all[anchor_idx]
    local_num = num_all[idx]
    local_keys = combo_keys(X_train.iloc[idx], categorical)
    anchor_keys = local_keys[anchor_pos]

    # Estimate local covariance within the selected anchor's categorical stratum,
    # with the same <5-row fallback as the original sampler. Keep only its diagonal.
    diag_var = np.empty((n, len(numeric)), dtype=float)
    for key in np.unique(anchor_keys):
        stratum = local_num[local_keys == key]
        if len(stratum) < 5:
            stratum = local_num
        var = np.var(stratum, axis=0, ddof=1) if len(stratum) > 1 else np.var(local_num, axis=0, ddof=1)
        rows = anchor_keys == key
        diag_var[rows] = np.maximum(var, 0.0)

    eps = rng.normal(size=(n, len(numeric))) * scale * np.sqrt(diag_var)
    S[numeric] = np.clip(anchor_num + eps, num_all.min(axis=0), num_all.max(axis=0))

    # For numeric columns deterministically determined by a categorical column,
    # restore the mapping after independently drawing categoricals.
    for num_col in locked:
        determining_cat = None
        for cat_col in categorical:
            nunique = X_train.groupby(cat_col, dropna=False)[num_col].nunique(dropna=False)
            if len(nunique) and nunique.max() == 1:
                determining_cat = cat_col
                break
        if determining_cat is not None:
            mapping = (X_train.drop_duplicates(determining_cat)
                       .set_index(determining_cat)[num_col].to_dict())
            S[num_col] = S[determining_cat].map(mapping).fillna(
                X_train[num_col].median()
            ).to_numpy()
    return S


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    ds = load_dataset("adult")
    models = fit_models(ds)
    model = models["rf"]
    pre = model[:-1]
    names = pre.get_feature_names_out().tolist()
    E = Explainer(lambda X: model.predict_proba(X)[:, 1], pre.transform,
                  ds.X_train, ds.numeric, ds.categorical, names)
    Z_dev = np.asarray(pre.transform(ds.X_dev), float)
    rows = []
    coef_rows = []
    t0 = time.perf_counter()

    for case_i, case in enumerate(ds.explain_idx[:100]):
        x = ds.X_test.iloc[[int(case)]]
        z_x = np.asarray(pre.transform(x), float)[0]
        eval_X = default_eval_neighborhood(z_x, Z_dev, ds.X_dev, k=200)
        z_eval = np.asarray(pre.transform(eval_X), float)
        width = float(np.median(np.linalg.norm(z_eval - z_x, axis=1)))

        for budget in BUDGETS:
            for seed in SEEDS:
                for condition, sampler in (
                    ("dep_aware", sample_dependency_aware),
                    ("isolating_no_dependency", sample_isolating_ablation),
                ):
                    result = E.explain(
                        x, sampler, budget, seed, eval_X,
                        width=width, k=K, scale=SCALE
                    )
                    rows.append({
                        "dataset": "adult", "model": "rf", "condition": condition,
                        "n": budget, "case": int(case), "seed": seed,
                        "fidelity": result["fidelity"], "fit_r2": result["fit_r2"],
                        "mean_nn_dist": result["validity"]["mean_nn_dist"],
                        "frac_seen_combo": result["validity"]["frac_seen_combo"],
                        "mean_dist_to_query": result["mean_dist_to_query"],
                        "mean_weight": result["mean_weight"], "width": width,
                        "runtime_s": result["runtime_s"],
                        "prediction": result["prediction"],
                        "surrogate_prediction": result["surrogate_prediction"],
                    })
                    coef_rows.append((budget, int(case), seed, condition, result["coef"]))
        if (case_i + 1) % 10 == 0:
            elapsed = time.perf_counter() - t0
            print(f"{case_i+1}/100 cases; elapsed {elapsed/60:.1f} min", flush=True)

    df = pd.DataFrame(rows)
    df.to_csv(OUT / "grid.csv", index=False)
    # Save coefficients in a tidy array with explicit index manifest.
    coef_df = pd.DataFrame([
        {"n": n, "case": c, "seed": s, "condition": cond, "coef": repr(np.asarray(coef).tolist())}
        for n, c, s, cond, coef in coef_rows
    ])
    coef_df.to_csv(OUT / "coefficients.csv", index=False)

    summary = (df.groupby(["condition", "n"])
               .agg(fidelity_mean=("fidelity", "mean"),
                    fidelity_median=("fidelity", "median"),
                    fidelity_sd=("fidelity", "std"),
                    seen_combo=("frac_seen_combo", "mean"),
                    nn_distance=("mean_nn_dist", "mean"),
                    runtime_s=("runtime_s", "mean"))
               .reset_index())
    summary.to_csv(OUT / "summary.csv", index=False)

    # Paired comparison: average over seeds per case, then bootstrap over cases.
    pivot = (df.groupby(["condition", "n", "case"]).fidelity.mean()
             .unstack("condition"))
    paired_rows = []
    rng = np.random.default_rng(0)
    for budget in BUDGETS:
        delta = (pivot.loc[budget, "dep_aware"] -
                 pivot.loc[budget, "isolating_no_dependency"]).dropna().to_numpy()
        boots = np.array([
            rng.choice(delta, size=len(delta), replace=True).mean()
            for _ in range(2000)
        ])
        paired_rows.append({
            "n": budget, "comparison": "dep_aware_minus_isolating_no_dependency",
            "mean_delta": float(delta.mean()),
            "ci95_low": float(np.quantile(boots, .025)),
            "ci95_high": float(np.quantile(boots, .975)),
            "dep_aware_wins": int((delta > 0).sum()),
            "n_cases": int(len(delta)),
        })
    pd.DataFrame(paired_rows).to_csv(OUT / "paired.csv", index=False)
    print("\nSummary:\n", summary.to_string(index=False))
    print("\nPaired comparison:\n", pd.DataFrame(paired_rows).to_string(index=False))
    print(f"\nSaved results to {OUT}; elapsed {(time.perf_counter()-t0)/60:.1f} min")


if __name__ == "__main__":
    main()
