"""Week-5 analysis (results/week4_evidence.md, section 5). A: absolute error (kernel-weighted RMSE) for the whole main grid,
B: the independent-feature control, C: rank stability of the teammate's isolating ablation (Adult RF, her own run),
D: forest dev accuracy and the lead over training neighbors across the leaf-size sweep.
Analysis only: reads results/main and results/isolating_ablation, refits the six models to rebuild the evaluation
neighborhoods, writes results/week5/{analysis.md, eval_variance.csv, paired_rmse.csv, isolating_stability.csv, leaf_sweep.csv}.
Run from the repo root: .venv/bin/python src/week5_analysis.py"""
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

from analyze_grid import BASES, BUDGETS, KEYS
from data import build_preprocessor, fit_models, load_dataset
from explain import default_eval_neighborhood, kernel_weights, rank_stability
from main_grid import DATASETS, K_EVAL, MODELS, N_CASES

OUT, MAIN, ISO, T0 = Path("results/week5"), Path("results/main"), Path("results/isolating_ablation"), time.perf_counter()
SYN = ["synthetic_dep", "synthetic_indep"]


def boot(d):
    """Paired summary of per-case differences, analyze_grid.paired conventions: mean, percentile-bootstrap 95% CI over cases
    (2,000 resamples, fresh default_rng(0)), wins = cases with d > 0."""
    d = np.asarray(d, float)
    lo, hi = np.percentile(d[np.random.default_rng(0).integers(0, len(d), (2000, len(d)))].mean(1), [2.5, 97.5])
    assert lo - 1e-12 <= d.mean() <= hi + 1e-12, (lo, d.mean(), hi)
    return dict(diff_mean=d.mean(), ci_lo=lo, ci_hi=hi, wins=int((d > 0).sum()), n_cases=len(d))


def eval_variance():
    """Per (dataset, model, case): evaluation neighborhood and median width rebuilt exactly as main_grid.run_pair, and the
    kernel-weighted variance of the black-box predictions on it (the weighted-R^2 denominator divided by sum(w))."""
    rows = []
    for d in DATASETS:
        ds = load_dataset(d)
        for mname, m in fit_models(ds).items():  # seed 0, the grid's models
            pre = m[:-1]
            Z_dev = pre.transform(ds.X_dev)
            for case in ds.explain_idx[:N_CASES]:
                z_x = pre.transform(ds.X_test.iloc[[case]])[0]
                ev = default_eval_neighborhood(z_x, Z_dev, ds.X_dev, k=K_EVAL)
                dist = np.linalg.norm(pre.transform(ev) - z_x, axis=1)
                width = float(np.median(dist))
                f, w = m.predict_proba(ev)[:, 1], kernel_weights(dist, width)
                rows.append(dict(dataset=d, model=mname, case=int(case), width=width,
                                 var_w=np.sum(w * (f - np.average(f, weights=w)) ** 2) / w.sum()))
    return pd.DataFrame(rows)[["dataset", "model", "case", "var_w", "width"]]


def table(head, rows):
    return ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)] + ["| " + " | ".join(map(str, r)) + " |" for r in rows]


ci = lambda r, f=".3f": f"{r.diff_mean:+{f}} [{r.ci_lo:+{f}}, {r.ci_hi:+{f}}]"

if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    ev = eval_variance()
    ev.to_csv(OUT / "eval_variance.csv", index=False)
    order = {d: i for i, d in enumerate(DATASETS)}  # protocol order (grid.csv is alphabetical)
    g = pd.read_csv(MAIN / "grid.csv").sort_values("dataset", key=lambda c: c.map(order), kind="stable", ignore_index=True)
    g = g.merge(ev, on=["dataset", "model", "case"], suffixes=("", "_rebuilt"), validate="many_to_one")
    dw = (g.width - g.width_rebuilt).abs().max()
    assert len(ev) == 600 and len(g) == 36000 and np.isfinite(g.fidelity).all() and dw < 1e-9, dw  # same neighborhoods
    g["rmse"] = np.sqrt((1 - g.fidelity) * g.var_w)  # weighted MSE = (1 - weighted R^2) * var_w
    pc = g.groupby(KEYS + ["case"], sort=False)[["fidelity", "rmse", "var_w"]].mean().reset_index()  # per-case seed means

    # A1 levels; A2 paired RMSE; A3 tail vs var_w; A4 teammate check
    S = pd.read_csv(MAIN / "summary.csv")
    a1 = (pc.groupby(KEYS, sort=False).agg(fid_med=("fidelity", "median"), rmse_mean=("rmse", "mean"), rmse_med=("rmse", "median"))
          .reset_index().merge(S[KEYS + ["fidelity_med", "rank_stability"]], on=KEYS, validate="one_to_one"))
    assert np.allclose(a1.fid_med, a1.fidelity_med)  # same per-case seed means as analyze_grid
    W = pc.set_index(["dataset", "model", "n", "case", "condition"]).rmse.unstack("condition")
    pr = pd.DataFrame([dict(dataset=d, model=m, n=n, comparison=f"{b}-dep_aware",
                            **boot(W.loc[(d, m, n), b] - W.loc[(d, m, n), "dep_aware"]))
                       for d in DATASETS for m in MODELS for n in BUDGETS for b in BASES])
    pr.to_csv(OUT / "paired_rmse.csv", index=False)
    p10 = ev.groupby(["dataset", "model"]).var_w.quantile(0.1).rename("p10")
    a3 = []
    for (d, m, c), x in pc[pc.n == 500].join(p10, on=["dataset", "model"]).groupby(["dataset", "model", "condition"], sort=False):
        neg, hi = x.fidelity < 0, x.var_w > x.p10
        a3.append([d, m, c, f"{spearmanr(x.fidelity, np.log10(x.var_w)).statistic:+.2f}", neg.sum(), (neg & ~hi).sum(),
                   f"{x.fidelity.median():.3f}", f"{x.fidelity[hi].median():.3f}", hi.sum()])
    qp = g[g.dataset == "adult"].groupby(["model", "case"]).prediction.first()  # black box at the query, as the grid saw it
    t = pd.read_csv("results/failure_analysis/evaluation_variance.csv").merge(ev, on=["dataset", "model", "case"], validate="one_to_one")
    a4 = [f"- {m} ({len(x)} cases): mean var_w {x.var_w.mean():.6g} here vs {x.eval_weighted_variance.mean():.6g} teammate; median "
          f"{x.var_w.median():.6g} vs {x.eval_weighted_variance.median():.6g}; max relative difference "
          f"{((x.var_w - x.eval_weighted_variance).abs() / x.eval_weighted_variance).max():.2e}; max |width difference| "
          f"{(x.width - x.kernel_width).abs().max():.2e}; max |query prediction difference| vs grid.csv `prediction` "
          f"{(x.set_index('case').query_prediction - qp[m]).abs().max():.2e}." for m, x in t.groupby("model")]

    # B: control table and bullets, from paired.csv / summary.csv plus this script's RMSE
    P = pd.read_csv(MAIN / "paired.csv")
    Pi, A = P.set_index(["dataset", "model", "n", "comparison", "metric"]), a1.set_index(KEYS)
    rows_b = []
    for m in MODELS:
        for n in BUDGETS:
            for b in ["independent", "neighbors", "abl_no_dependency"]:
                fs = [(Pi.loc[(d, m, n, f"dep_aware-{b}", "fidelity")], Pi.loc[(d, m, n, f"dep_aware-{b}", "rank_stability")]) for d in SYN]
                rows_b.append([m, n, f"dep_aware - {b}"] + [v for f, s in fs for v in (f"{ci(f)} {f.wins:.0f}/{f.n_cases:.0f}", ci(s))])
            lv = [A.loc[(d, m, "dep_aware", n)] for d in SYN]
            rows_b.append([m, n, "dep_aware level: fidelity median / RMSE mean; stability"] +
                          [v for r in lv for v in (f"{r.fidelity_med:.3f} / {r.rmse_mean:.4f}", f"{r.rank_stability:.3f}")])
    sel = lambda d, b, k: P[(P.dataset == d) & (P.comparison == f"dep_aware-{b}") & (P.metric == k)].set_index(["model", "n"])
    f_, s_ = sel("synthetic_indep", "independent", "fidelity"), sel("synthetic_indep", "independent", "rank_stability")
    r_ = pr[(pr.dataset == "synthetic_indep") & (pr.comparison == "independent-dep_aware")].set_index(["model", "n"])
    worse = [f"{lab} {m} n={n}" for lab, q in [("fidelity", f_), ("stability", s_), ("RMSE", r_)] for (m, n), x in q.iterrows() if x.ci_hi < 0]
    bul = [f"(i) Bias on the control (synthetic_indep, dep_aware vs independent, 4 model x budget cells): fidelity difference "
           f"{f_.diff_mean.min():+.3f} to {f_.diff_mean.max():+.3f} (lowest CI bound {f_.ci_lo.min():+.3f}; dep_aware higher in "
           f"{f_.wins.min()}-{f_.wins.max()} of 100 cases), rank stability {s_.diff_mean.min():+.3f} to {s_.diff_mean.max():+.3f} (lowest "
           f"CI bound {s_.ci_lo.min():+.3f}), RMSE reduction {r_.diff_mean.min():+.4f} to {r_.diff_mean.max():+.4f} (lowest CI bound "
           f"{r_.ci_lo.min():+.4f}). Cells where dep_aware is significantly worse (CI entirely below 0): {', '.join(worse) or 'none'}."]
    share = {}
    for d in SYN:
        tot, a = sel(d, "independent", "fidelity"), sel(d, "abl_no_dependency", "fidelity")
        share[d] = 1 - a.diff_mean / tot.diff_mean
        bul.append(f"(ii) {d}: dep_aware - abl_no_dependency fidelity " + "; ".join(
            f"{m} n={n}: {ci(x, '.4f')} = {100 * x.diff_mean / tot.loc[(m, n)].diff_mean:.0f}% of the {tot.loc[(m, n)].diff_mean:+.3f} "
            f"gain over independent" for (m, n), x in a.iterrows()) +
            f". CI entirely above 0 in {(a.ci_lo > 0).sum()}/4 cells, entirely below 0 in {(a.ci_hi < 0).sum()}/4.")
    bul.append("(iii) Share of the fidelity gain over independent that survives removing the dependency structure, i.e. attributable "
               "to anchoring on real local records: mean(abl_no_dependency - independent) / mean(dep_aware - independent) = "
               + "; ".join(f"{d} {share[d].min():.0%} to {share[d].max():.0%}" for d in SYN) + " across the 4 cells. Caveat (protocol "
               "amendment 2): abl_no_dependency also replaces the local stratum covariance with global-std noise, so its gap mixes "
               "dependency removal with a noise-scale change; this is a ratio of mean differences, not a clean attribution.")

    # C: isolating ablation (teammate's run only; never mixed with main-grid rows)
    gi, co = pd.read_csv(ISO / "grid.csv"), pd.read_csv(ISO / "coefficients.csv")
    assert len(co) == 2000 and set(co.seed) == set(range(5)) and not co.duplicated(["n", "case", "seed", "condition"]).any()
    co["coef"] = co.coef.map(json.loads)
    st = co.groupby(["condition", "n", "case"]).coef.apply(lambda c: rank_stability(list(c))).unstack("condition")
    fi = gi.groupby(["condition", "n", "case"]).fidelity.mean().unstack("condition")
    assert st.shape == fi.shape == (200, 2) and st.notna().all().all() and fi.notna().all().all()
    cs = pd.DataFrame([dict(n=n, metric=k, comparison="dep_aware-isolating_no_dependency", dep_aware_mean=q.loc[n].dep_aware.mean(),
                            dep_aware_sd=q.loc[n].dep_aware.std(), iso_mean=q.loc[n].isolating_no_dependency.mean(),
                            iso_sd=q.loc[n].isolating_no_dependency.std(), dep_aware_med=q.loc[n].dep_aware.median(),
                            iso_med=q.loc[n].isolating_no_dependency.median(),
                            **boot(q.loc[n].dep_aware - q.loc[n].isolating_no_dependency))
                       for n in BUDGETS for k, q in [("rank_stability", st), ("fidelity", fi)]])
    cs.to_csv(OUT / "isolating_stability.csv", index=False)
    hp = pd.read_csv(ISO / "paired.csv").set_index("n")
    c_chk = [f"- n={r.n}: recomputed {ci(r, '.4f')}, {r.wins}/{r.n_cases}; teammate's paired.csv {hp.mean_delta[r.n]:+.4f} "
             f"[{hp.ci95_low[r.n]:+.4f}, {hp.ci95_high[r.n]:+.4f}], {hp.dep_aware_wins[r.n]}/{hp.n_cases[r.n]}; mean and wins "
             f"{'match' if np.isclose(r.diff_mean, hp.mean_delta[r.n], rtol=0, atol=1e-9) and r.wins == hp.dep_aware_wins[r.n] else 'DIFFER'}"
             f" (|mean difference| {abs(r.diff_mean - hp.mean_delta[r.n]):.1e}); max |CI bound difference| "
             f"{max(abs(r.ci_lo - hp.ci95_low[r.n]), abs(r.ci_hi - hp.ci95_high[r.n])):.1e}."
             for r in cs[cs.metric == "fidelity"].itertuples()]

    L = ["# Week 5 analysis", "", "Generated by `src/week5_analysis.py` from `results/main/{grid,summary,paired}.csv` and "
         "`results/isolating_ablation/{grid,coefficients,paired}.csv`. Conventions of `src/analyze_grid.py`: per-case mean over "
         "the 5 seeds first, then statistics over the 100 cases; paired percentile bootstrap, 2,000 resamples, `default_rng(0)`.", "",
         "## A. Absolute error on the evaluation neighborhood", "",
         "var_w = sum(w (f - fbar_w)^2) / sum(w) on each case's 200-record dev neighborhood with w = exp(-d^2 / width^2) (the "
         "weighted-R^2 denominator per unit weight); weighted MSE = (1 - fidelity) * var_w, RMSE = sqrt(MSE) per explanation, then "
         f"seed mean per case. Neighborhood check: the rebuilt median width equals grid.csv's `width` for all {len(ev)} cases "
         f"(all {len(g)} rows), max |difference| {dw:.1e} (assert < 1e-9). Per-case var_w: `eval_variance.csv`.", "",
         "### A1. Fidelity median vs RMSE (mean and median over cases of the per-case seed-mean RMSE)"]
    for (d, m), x in a1.groupby(["dataset", "model"], sort=False):
        L += ["", f"#### {d} / {m}", ""] + table(["condition", "n", "fidelity median (summary.csv)", "RMSE mean", "RMSE median"],
                                                [[r.condition, r.n, f"{r.fidelity_med:.3f}", f"{r.rmse_mean:.4f}", f"{r.rmse_med:.4f}"]
                                                 for r in x.itertuples()])
    L += ["", "### A2. Paired per-case RMSE differences, baseline - dep_aware (positive = dep_aware has lower error): mean [95% CI] "
          "wins/n (`paired_rmse.csv`)", ""]
    L += table(["dataset", "model", "n"] + BASES, [[d, m, n] + [f"{ci(r, '.4f')} {r.wins}/{r.n_cases}" for r in x.itertuples()]
                                                   for (d, m, n), x in pr.groupby(["dataset", "model", "n"], sort=False)])
    L += ["", "### A3. Negative-fidelity tail vs evaluation-neighborhood variance (n = 500)", "",
          "Sensitivity analysis, not an exclusion rule: the main results keep every case. p10 = 10th percentile of var_w over the 100 "
          "cases of each dataset/model; bottom decile = var_w <= p10.", ""]
    L += table(["dataset", "model", "condition", "Spearman(fidelity, log10 var_w)", "cases fidelity < 0", "of those in bottom var_w decile",
                "fidelity median, all cases", "fidelity median, var_w > p10", "cases var_w > p10"], a3)
    L += ["", "### A4. Sanity check vs the teammate's Adult `results/failure_analysis/evaluation_variance.csv` (reported, not asserted; "
          "her forest was fit in another environment)", ""] + a4
    L += ["", "## B. Independent-feature control (synthetic_indep) next to synthetic_dep", "",
          "Fidelity cells: dep_aware - baseline mean [95% CI] wins/n; stability cells: mean [95% CI] (`results/main/paired.csv`). "
          "Level rows: dep_aware's fidelity median (summary.csv) / mean per-case RMSE (A1); rank stability (summary.csv).", ""]
    L += table(["model", "n", "row", "synthetic_dep fidelity", "synthetic_dep stability", "synthetic_indep fidelity",
                "synthetic_indep stability"], rows_b)
    L += [""] + [f"- {b}" for b in bul]
    L += ["", "## C. Isolating ablation, Adult RF (teammate's run; conditions compared only within it)", "",
          "Rank stability per case over the 5 seeds from `coefficients.csv` (`explain.rank_stability`); fidelity = per-case seed mean "
          "from her `grid.csv`. Paired differences dep_aware - isolating_no_dependency (`isolating_stability.csv`).", ""]
    L += table(["n", "metric", "dep_aware mean ± sd", "isolating_no_dependency mean ± sd", "difference [95% CI]", "wins/n"],
               [[r.n, r.metric, f"{r.dep_aware_mean:.3f} ± {r.dep_aware_sd:.3f}", f"{r.iso_mean:.3f} ± {r.iso_sd:.3f}", ci(r),
                 f"{r.wins}/{r.n_cases}"] for r in cs.itertuples()])
    L += ["", "Fidelity paired difference recomputed with the project's conventions vs her `paired.csv` (her script draws both "
          "budgets from one `default_rng(0)` stream, so n = 200 reuses the project's resamples and n = 500 does not):", ""] + c_chk
    run_med = gi[gi.n == 500].groupby("condition").fidelity.median()
    L += ["", "Fidelity medians over cases (per-case seed means, the protocol's convention): " + "; ".join(
        f"n={r.n}: {r.dep_aware_med:.3f} vs {r.iso_med:.3f}" for r in cs[cs.metric == "fidelity"].itertuples()) +
        f". Her `summary.csv` takes the median over the 500 runs instead ({run_med.dep_aware:.3f} vs "
        f"{run_med.isolating_no_dependency:.3f} at n = 500); slides and evidence files use the per-case numbers."]

    # D: leaf-size sweep (src/min_samples_leaf_experiment.py): dev accuracy of each refit forest next to the saved lead
    rows_d = []
    for d, folder in [("adult", "min_samples_leaf"), ("synthetic_dep", "min_samples_leaf_synthetic_dep")]:
        ds, lead = load_dataset(d), pd.read_csv(Path("results") / folder / "paired.csv")
        lead = lead[lead.n == 500].set_index("min_samples_leaf")
        for leaf in lead.index:
            rf = Pipeline([("pre", build_preprocessor(ds.numeric, ds.categorical)), ("clf", RandomForestClassifier(
                n_estimators=200, min_samples_leaf=int(leaf), n_jobs=-1, random_state=0))]).fit(ds.X_train, ds.y_train)
            rows_d.append(dict(dataset=d, min_samples_leaf=int(leaf), dev_accuracy=rf.score(ds.X_dev, ds.y_dev), lead_n500=lead.mean_delta[leaf],
                               ci_lo=lead.ci95_low[leaf], ci_hi=lead.ci95_high[leaf], wins=int(lead.dep_aware_wins[leaf])))
    dd = pd.DataFrame(rows_d)
    dd.to_csv(OUT / "leaf_sweep.csv", index=False)
    L += ["", "## D. Leaf-size sweep: forest dev accuracy and the lead over training neighbors (n = 500)", "",
          "Forests refit here with the sweep's settings (200 trees, seed 0). Lead = mean paired fidelity difference dep_aware - "
          "neighbors with its 95% CI, from `results/min_samples_leaf*/paired.csv` (`leaf_sweep.csv`).", ""]
    L += table(["dataset", "min_samples_leaf", "dev accuracy", "lead [95% CI]", "wins/100"],
               [[r.dataset, r.min_samples_leaf, f"{r.dev_accuracy:.4f}", f"{r.lead_n500:+.3f} [{r.ci_lo:+.3f}, {r.ci_hi:+.3f}]", r.wins]
                for r in dd.itertuples()])
    for d, x in dd.groupby("dataset", sort=False):
        a, b = x.set_index("min_samples_leaf").lead_n500[[2, 20]]
        L += ["", f"- {d}: the lead falls from {a:+.3f} at leaf size 2 (protocol) to {b:+.3f} at 20, a {100 * (1 - b / a):.0f}% reduction; "
              f"dev accuracy stays between {x.dev_accuracy.min():.3f} and {x.dev_accuracy.max():.3f}."]
    (OUT / "analysis.md").write_text(txt := "\n".join(L) + "\n")
    print(txt + f"\nwidth check passed: {len(ev)} cases, max |diff| {dw:.1e}; runtime {time.perf_counter() - T0:.1f} s")
