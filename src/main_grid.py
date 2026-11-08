"""Main grid, protocol v1 (configs/protocol_v1.md): 6 conditions x 2 budgets x 5 seeds x 100 cases per (dataset, model).
Resumable per pair. Writes {OUT}/grid_<d>_<m>.csv, coefs_<d>_<m>.npy (condition, budget, case, seed, p), features_<d>.json,
then grid.csv (all pairs). --quick: first 3 cases, seeds 0..1, OUT = results/main_quick. Run from the repo root."""
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

from data import fit_models, load_dataset
from explain import Explainer, default_eval_neighborhood, sample_dependency_aware, sample_independent, sample_neighbors

QUICK = "--quick" in sys.argv
CONDITIONS = ["independent", "independent_matched", "neighbors", "dep_aware", "abl_no_dependency", "abl_no_locality"]
BUDGETS, SEEDS, N_CASES, K_EVAL = (200, 500), range(2 if QUICK else 5), 3 if QUICK else 100, 200
MATCHED_SCALE = {"synthetic_dep": 0.75, "synthetic_indep": 0.75, "adult": 0.25}
DATASETS, MODELS = ["synthetic_dep", "synthetic_indep", "adult"], ["lr", "rf"]
OUT = Path("results/main_quick" if QUICK else "results/main")
COLS = ["dataset", "model", "condition", "n", "case", "seed", "fidelity", "fit_r2", "mean_nn_dist", "frac_seen_combo",
        "mean_dist_to_query", "mean_weight", "width", "runtime_s", "wall_s", "prediction", "surrogate_prediction"]
PER_CASE = len(CONDITIONS) * len(BUDGETS) * len(SEEDS)


def condition(name, dataset):
    """-> (sampler, explain kwargs); locality goes to explain, everything else through to the sampler"""
    return {"independent": (sample_independent, {}),
            "independent_matched": (sample_independent, {"scale": MATCHED_SCALE[dataset]}),
            "neighbors": (sample_neighbors, {}),
            "dep_aware": (sample_dependency_aware, {}),
            "abl_no_dependency": (sample_dependency_aware, {"dependencies": False}),
            "abl_no_locality": (sample_dependency_aware, {"locality": False})}[name]


def run_pair(d, mname, tick):
    ds = load_dataset(d)
    m = fit_models(ds)[mname]  # fits lr and rf, keeps one
    pre = m[:-1]
    names = pre.get_feature_names_out().tolist()
    (OUT / f"features_{d}.json").write_text(json.dumps(names))
    E = Explainer(lambda X: m.predict_proba(X)[:, 1], pre.transform, ds.X_train, ds.numeric, ds.categorical, names)
    Z_dev, cases = pre.transform(ds.X_dev), ds.explain_idx[:N_CASES]
    C, rows = np.full((len(CONDITIONS), len(BUDGETS), len(cases), len(SEEDS), len(names)), np.nan), []
    for k, case in enumerate(cases):
        x = ds.X_test.iloc[[case]]
        z_x = pre.transform(x)[0]
        ev = default_eval_neighborhood(z_x, Z_dev, ds.X_dev, k=K_EVAL)
        width = float(np.median(np.linalg.norm(pre.transform(ev) - z_x, axis=1)))  # one width per case
        for ci, cond in enumerate(CONDITIONS):
            fn, kw = condition(cond, d)
            for bi, n in enumerate(BUDGETS):
                for si, seed in enumerate(SEEDS):
                    t0 = time.perf_counter()
                    r = E.explain(x, fn, n, seed, ev, width=width, **kw)
                    wall = time.perf_counter() - t0
                    C[ci, bi, k, si] = r["coef"]
                    rows.append(dict(dataset=d, model=mname, condition=cond, n=n, case=int(case), seed=seed,
                                     fidelity=r["fidelity"], fit_r2=r["fit_r2"], **r["validity"],
                                     mean_dist_to_query=r["mean_dist_to_query"], mean_weight=r["mean_weight"], width=width,
                                     runtime_s=r["runtime_s"], wall_s=wall, prediction=r["prediction"],
                                     surrogate_prediction=r["surrogate_prediction"]))
        tick(f"{d}/{mname} case {k + 1}/{len(cases)} (test row {case})")
    pd.DataFrame(rows, columns=COLS).to_csv(OUT / f"grid_{d}_{mname}.csv", index=False)
    tmp = OUT / f"coefs_{d}_{mname}.tmp.npy"  # coefs written last + atomic rename = the pair's "done" marker
    np.save(tmp, C)
    tmp.replace(OUT / f"coefs_{d}_{mname}.npy")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    T0 = time.perf_counter()
    exists = lambda d, m: (OUT / f"grid_{d}_{m}.csv").exists() and (OUT / f"coefs_{d}_{m}.npy").exists()
    todo = [(d, m) for d in DATASETS for m in MODELS if not exists(d, m)]
    total, done = len(todo) * N_CASES * PER_CASE, [0]

    def tick(msg):
        done[0] += PER_CASE
        el = time.perf_counter() - T0
        print(f"[{el / 60:6.1f} min] {msg}: {done[0]}/{total} explanations, ETA {el / done[0] * (total - done[0]) / 60:.1f} min",
              flush=True)

    for d in DATASETS:
        for mname in MODELS:
            if (d, mname) in todo:
                run_pair(d, mname, tick)
            else:
                print(f"skip {d}/{mname}: grid_{d}_{mname}.csv and coefs_{d}_{mname}.npy exist", flush=True)
    g = pd.concat([pd.read_csv(f) for f in sorted(OUT.glob("grid_*_*.csv"))], ignore_index=True)
    g.to_csv(OUT / "grid.csv", index=False)
    print(f"grid.csv: {len(g)} rows; total {(time.perf_counter() - T0) / 60:.1f} min\nmean wall_s per (dataset, model):")
    print(g.groupby(["dataset", "model"]).wall_s.mean().round(4).to_string())
