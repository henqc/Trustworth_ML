"""First start (recover a known linear predictor) + pilot of the perturbation neighborhoods.
Writes results/first_start.csv, results/pilot.csv, results/pilot_summary.md. Run from the repo root."""
import time
from pathlib import Path

import numpy as np
import pandas as pd

from data import fit_models, linear_predictor, load_dataset
from explain import (Explainer, default_eval_neighborhood, rank_stability, sample_dependency_aware,
                     sample_independent, sample_neighbors)

N_CASES, BUDGETS, SEEDS, OUT = 30, (200, 500), range(5), Path("results")
SAMPLERS = {"independent": (sample_independent, {}), "neighbors": (sample_neighbors, {}),
            "dep_aware": (sample_dependency_aware, {}),
            "abl_no_dependency": (sample_dependency_aware, {"dependencies": False}),
            "abl_no_locality": (sample_dependency_aware, {"locality": False})}
KEYS = ["dataset", "model", "sampler", "n"]
METRICS = ["fidelity", "fit_r2", "mean_nn_dist", "frac_seen_combo", "mean_dist_to_query", "runtime_s", "wall_s"]


def first_start():
    rows = []
    three = ["independent", "neighbors", "dep_aware"]
    for name, samplers, noise in [("synthetic_dep", three, 0.0), ("synthetic_indep", ["independent"], 0.0),
                                  ("synthetic_dep", three, 0.5)]:  # noise sd 0.5 on a logit of scale ~3
        ds = load_dataset(name)
        T = lambda X: X[ds.numeric].to_numpy(float)
        f, nrng = linear_predictor(ds.linear_w, ds.linear_b), np.random.default_rng(123)
        E = Explainer(lambda X: f(X) + noise * nrng.normal(size=len(X)), T, ds.X_train, ds.numeric, ds.categorical, ds.numeric)
        for case in ds.explain_idx[:20]:
            x = ds.X_test.iloc[[case]]
            ev = default_eval_neighborhood(T(x)[0], T(ds.X_dev), ds.X_dev, k=200)
            for s in samplers:
                for n in BUDGETS:
                    for seed in SEEDS:
                        r = E.explain(x, SAMPLERS[s][0], n, seed, ev, alpha=1e-8)
                        rows.append(dict(dataset=name, noise=noise, sampler=s, n=n, case=case, seed=seed,
                                         max_abs_err=np.abs(r["coef"] - ds.linear_w).max(), fidelity=r["fidelity"]))
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "first_start.csv", index=False)
    print(df.groupby(["dataset", "noise", "sampler", "n"], sort=False)
          .agg(max_abs_err=("max_abs_err", "max"), mean_fidelity=("fidelity", "mean")).to_string())
    assert (df[df.noise == 0].max_abs_err < 1e-4).all(), df.max_abs_err.max()  # exact target must be recovered exactly


def pilot(ds, models, model_names, n_cases, samplers, budgets, seeds, rows):
    for mname in model_names:
        m, t = models[mname], time.perf_counter()
        pre = m[:-1]
        E = Explainer(lambda X: m.predict_proba(X)[:, 1], pre.transform, ds.X_train, ds.numeric, ds.categorical,
                      pre.get_feature_names_out())
        Z_dev = pre.transform(ds.X_dev)
        for case in ds.explain_idx[:n_cases]:
            x = ds.X_test.iloc[[case]]
            ev = default_eval_neighborhood(pre.transform(x)[0], Z_dev, ds.X_dev, k=200)  # once per case, all samplers/seeds
            for s in samplers:
                fn, kw = SAMPLERS[s]
                for n in budgets:
                    for seed in seeds:
                        t0 = time.perf_counter()
                        r = E.explain(x, fn, n, seed, ev, **kw)
                        rows.append(dict(dataset=ds.name, model=mname, sampler=s, n=n, case=case, seed=seed,
                                         fidelity=r["fidelity"], fit_r2=r["fit_r2"], **r["validity"],
                                         mean_dist_to_query=r["mean_dist_to_query"], runtime_s=r["runtime_s"],
                                         wall_s=time.perf_counter() - t0, coef=r["coef"]))
        print(f"  {ds.name} {mname}: {n_cases} cases done in {time.perf_counter() - t:.1f}s", flush=True)


def summarize(df):
    per_case = df.groupby(KEYS + ["case"], sort=False).agg(
        **{c: (c, "mean") for c in METRICS}, rank_stability=("coef", lambda c: rank_stability(list(c))))
    print("non-finite metrics:", {"fidelity (per run)": int((~np.isfinite(df.fidelity)).sum()),
                                  "rank_stability (per case)": int((~np.isfinite(per_case.rank_stability)).sum())})
    s = per_case.groupby(KEYS, sort=False).agg(**{c: (c, "mean") for c in METRICS + ["rank_stability"]},
                                               fidelity_std=("fidelity", "std"), fidelity_med=("fidelity", "median")).reset_index()
    lines = ["# Pilot summary", "", "fidelity = mean ± std over cases of the per-case mean over seeds; "
             "fidelity_med = median over cases of the per-case mean; "
             "rank_stability = mean over cases of the mean pairwise Spearman of |coef| across seeds."]
    for (d, mo), g in s.groupby(["dataset", "model"], sort=False):
        lines += ["", f"## {d} / {mo}", "", "| sampler | n | fidelity | fidelity_med | rank_stability | mean_nn_dist | frac_seen_combo "
                  "| mean_dist_to_query | runtime_ms |", "|---|---|---|---|---|---|---|---|---|"]
        lines += [f"| {r.sampler} | {r.n} | {r.fidelity:.3f} ± {r.fidelity_std:.3f} | {r.fidelity_med:.3f} | {r.rank_stability:.3f} | "
                  f"{r.mean_nn_dist:.3f} | {r.frac_seen_combo:.3f} | {r.mean_dist_to_query:.3f} | {1000 * r.runtime_s:.1f} |"
                  for r in g.itertuples()]
    wall = df.groupby(["dataset", "model"]).wall_s.mean()
    print("mean per-explanation wall_s (incl. fidelity + validity):\n" + wall.round(4).to_string())
    # synthetic_indep reuses synthetic_dep timings; adult lr was never explained -> adult rf timing as an upper bound
    src = lambda d, mo: ("synthetic_dep" if d == "synthetic_indep" else d, "rf" if d == "adult" else mo)
    full = 100 * 2 * 5 * 5  # explanations per (dataset, model) in the 30,000-explanation full grid
    mins = sum(wall[src(d, mo)] for d in ["synthetic_dep", "synthetic_indep", "adult"] for mo in ["lr", "rf"]) * full / 60
    lines += ["", f"estimated full-grid minutes: {mins:.1f} (30,000 explanations, sequential; adult lr uses adult rf "
              "timing as an upper bound, synthetic_indep uses synthetic_dep timings)"]
    (OUT / "pilot_summary.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    T0 = time.perf_counter()
    OUT.mkdir(exist_ok=True)
    print("== Block 1: first start (recover the known linear predictor)", flush=True)
    first_start()
    rows = []
    print("== Block 2: pilot synthetic_dep (lr, rf)", flush=True)
    ds = load_dataset("synthetic_dep")
    pilot(ds, fit_models(ds), ["lr", "rf"], N_CASES, list(SAMPLERS), BUDGETS, SEEDS, rows)
    print("== Block 3: pilot adult (rf) + synthetic_indep control (rf)", flush=True)
    ds = load_dataset("adult")
    pilot(ds, fit_models(ds), ["rf"], 15, list(SAMPLERS), BUDGETS, range(3), rows)
    ds = load_dataset("synthetic_indep")
    pilot(ds, fit_models(ds), ["rf"], N_CASES, ["independent", "dep_aware"], [500], SEEDS, rows)
    print("== Block 4: summaries", flush=True)
    df = pd.DataFrame(rows)
    df.drop(columns="coef").to_csv(OUT / "pilot.csv", index=False)
    summarize(df)
    print(f"total runtime {time.perf_counter() - T0:.1f}s")
    print("first_start.py OK")
