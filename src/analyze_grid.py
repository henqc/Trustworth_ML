"""Main-grid analysis (configs/protocol_v1.md, "Analysis"). Reads {dir}/grid.csv, coefs_*.npy, features_*.json and
writes summary.csv, summary.md, paired.csv, failures.csv into the same dir. Run from the repo root:
    .venv/bin/python src/analyze_grid.py [input_dir]      (default results/main)"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from explain import rank_stability

CONDITIONS = ["independent", "independent_matched", "neighbors", "dep_aware", "abl_no_dependency", "abl_no_locality"]
BUDGETS = (200, 500)
BASES = [c for c in CONDITIONS if c != "dep_aware"]  # comparisons dep_aware-<base>, in this order
KEYS = ["dataset", "model", "condition", "n"]
SIDE = ["fit_r2", "prediction", "mean_nn_dist", "frac_seen_combo", "mean_dist_to_query", "mean_weight", "runtime_s", "wall_s"]
FAIL = ["dataset", "model", "condition", "n", "case", "fidelity", "fit_r2", "prediction", "mean_nn_dist", "frac_seen_combo",
        "mean_dist_to_query"]
fin = np.isfinite
USED = {"synthetic_dep": 30, "synthetic_indep": 30, "adult": 15}  # leading explain_idx positions used by the pilot / width sweep


def complete(df, d):
    """Every (dataset, model) pair must hold each (condition, n, case, seed) exactly once, cases in manifest explain_idx order,
    seeds 0..S-1; the full grid (dir name 'main') must have 100 cases and 5 seeds."""
    man = json.load(open("manifests/splits.json"))
    for (ds, mo), g in df.groupby(["dataset", "model"], sort=False):
        cases, seeds = list(dict.fromkeys(g.case)), sorted(g.seed.unique())
        assert cases == [int(c) for c in man[ds]["explain_idx"][:len(cases)]], f"{ds}/{mo}: case order != manifest"
        assert seeds == list(range(len(seeds))), f"{ds}/{mo}: seeds {seeds}"
        assert len(g) == 6 * 2 * len(cases) * len(seeds) and not g.duplicated(["condition", "n", "case", "seed"]).any(), f"{ds}/{mo} incomplete"
        if d.name == "main":
            assert (len(cases), len(seeds)) == (100, 5), f"{ds}/{mo}: {len(cases)} cases, {len(seeds)} seeds"
        assert not np.isnan(np.load(d / f"coefs_{ds}_{mo}.npy")).any(), f"{ds}/{mo}: NaN in coefs"


def per_case(df, d):
    """One row per (dataset, model, condition, n, case): seed means (fidelity over its finite seeds only; a NaN in a side
    column propagates instead of being skipped), raw non-finite fidelity count, and rank stability over the seeds."""
    g = df.assign(bad=~fin(df.fidelity)).groupby(KEYS + ["case"], sort=False)
    pc = g[SIDE].mean(skipna=False).join(g.bad.sum().rename("n_nonfinite"))
    pc["fidelity"] = df[fin(df.fidelity)].groupby(KEYS + ["case"], sort=False).fidelity.mean()  # all seeds bad -> NaN
    pc = pc.reset_index()
    for (ds, mo), g in pc.groupby(["dataset", "model"], sort=False):
        C = np.load(d / f"coefs_{ds}_{mo}.npy")
        raw = df[(df.dataset == ds) & (df.model == mo)]
        cases = {c: i for i, c in enumerate(raw.case.unique())}  # first-appearance order = runner's case axis
        assert C.shape == (6, 2, len(cases), raw.seed.nunique(), len(json.load(open(d / f"features_{ds}.json")))), C.shape
        pc.loc[g.index, "rank_stability"] = [rank_stability(list(C[CONDITIONS.index(r.condition), BUDGETS.index(r.n),
                                                                    cases[r.case]])) for r in g.itertuples()]
    return pc


def summarize(pc):
    rows = []
    for k, g in pc.groupby(KEYS, sort=False):
        f, s = g.fidelity[fin(g.fidelity)], g.rank_stability[fin(g.rank_stability)]
        rows.append(dict(zip(KEYS, k), n_cases=len(f), fidelity_mean=f.mean(), fidelity_sd=f.std(), fidelity_med=f.median(),
                         fidelity_q1=f.quantile(.25), fidelity_q3=f.quantile(.75), rank_stability=s.mean(),
                         rank_stability_sd=s.std(), **{c: g[c].mean(skipna=False) for c in SIDE[2:6]},
                         runtime_ms=1000 * g.runtime_s.mean(skipna=False), wall_ms=1000 * g.wall_s.mean(skipna=False),
                         n_nonfinite=int(g.n_nonfinite.sum()), rs_nonfinite=len(g) - len(s)))
    return pd.DataFrame(rows)


def paired(pc):
    w, rows = pc.set_index(["dataset", "model", "n", "case", "condition"])[["fidelity", "rank_stability"]].unstack("condition"), []
    for ds, mo, n in pc[["dataset", "model", "n"]].drop_duplicates().itertuples(index=False):  # grid order, not unstack's
        g = w.loc[(ds, mo, n)]
        for b in BASES:
            for m in ["fidelity", "rank_stability"]:
                x, y = g[(m, "dep_aware")].to_numpy(), g[(m, b)].to_numpy()
                ok = fin(x) & fin(y)
                dd = x[ok] - y[ok]
                boot = dd[np.random.default_rng(0).integers(0, len(dd), (2000, len(dd)))].mean(1) if len(dd) else [np.nan]
                lo, hi = np.percentile(boot, [2.5, 97.5])
                rows.append(dict(dataset=ds, model=mo, n=n, comparison=f"dep_aware-{b}", metric=m, diff_mean=dd.mean() if len(dd)
                                 else np.nan, diff_median=np.median(dd) if len(dd) else np.nan, ci_lo=lo, ci_hi=hi,
                                 wins=int((dd > 0).sum()), n_cases=len(dd), dropped=int((~ok).sum())))
    return pd.DataFrame(rows)


def report(df, s, p, fail, ph):
    L = ["# Main grid summary", "", "Fidelity: per case, the mean over its finite seeds; then mean +- sd, median and "
         "[q1, q3] over cases (validity and runtime columns: per-case seed mean, then mean over cases). Rank stability: per "
         "case, the mean pairwise Spearman of |coef| across seeds; then mean +- sd over cases with a finite value.", "",
         "## By condition"]
    for (ds, mo), g in s.groupby(["dataset", "model"], sort=False):
        L += ["", f"### {ds} / {mo}", "", "| condition | n | fidelity mean ± sd | median [q1, q3] | rank stability | "
              "mean_nn_dist | frac_seen_combo | mean_dist_to_query | runtime ms |", "|---|---|---|---|---|---|---|---|---|"]
        L += [f"| {r.condition} | {r.n} | {r.fidelity_mean:.3f} ± {r.fidelity_sd:.3f} | {r.fidelity_med:.3f} [{r.fidelity_q1:.3f}, "
              f"{r.fidelity_q3:.3f}] | {r.rank_stability:.3f} ± {r.rank_stability_sd:.3f} | {r.mean_nn_dist:.3f} | "
              f"{r.frac_seen_combo:.3f} | {r.mean_dist_to_query:.3f} | {r.runtime_ms:.1f} |" for r in g.itertuples()]
    L += ["", "## Paired comparisons (dep_aware minus baseline, per case; percentile bootstrap 95% CI, 2,000 resamples)"]
    for (ds, mo), g in p.groupby(["dataset", "model"], sort=False):
        L += ["", f"### {ds} / {mo}", "", "| comparison | n | metric | diff mean | 95% CI | wins/n |", "|---|---|---|---|---|---|"]
        L += [f"| {r.comparison} | {r.n} | {r.metric} | {r.diff_mean:+.3f} | [{r.ci_lo:+.3f}, {r.ci_hi:+.3f}] | {r.wins}/{r.n_cases} |"
              for r in g.itertuples()]
    c = p[(p.dataset == "synthetic_indep") & (p.comparison == "dep_aware-independent") & (p.metric == "fidelity")]
    L += ["", "**Control (synthetic_indep, dep_aware - independent fidelity):** " + "; ".join(
        f"{r.model} n={r.n}: {r.diff_mean:+.3f} [{r.ci_lo:+.3f}, {r.ci_hi:+.3f}]" for r in c.itertuples())]
    L += ["", "## Confirmatory subset: cases NOT used in the pilot or the kernel-width sweep (synthetic: cases 31-100, Adult: 16-100)",
          "", "| dataset | model | comparison | n | metric | diff mean | 95% CI | wins/n |", "|---|---|---|---|---|---|---|---|"]
    L += [f"| {r.dataset} | {r.model} | {r.comparison} | {r.n} | {r.metric} | {r.diff_mean:+.3f} | [{r.ci_lo:+.3f}, {r.ci_hi:+.3f}] | "
          f"{r.wins}/{r.n_cases} |" for r in ph[ph.metric == "fidelity"].itertuples()]
    dr = p[p.dropped > 0]
    L += ["", "Cases dropped from paired comparisons (non-finite on either side): " + ("; ".join(
        f"{r.dataset}/{r.model} n={r.n} {r.comparison} {r.metric}: {r.dropped}" for r in dr.itertuples()) or "none")]
    L += ["", "## Five lowest-fidelity cases per budget (per-case seed means)", "", "| " + " | ".join(FAIL) + " |",
          "|" + "---|" * len(FAIL)]
    L += ["| " + " | ".join(f"{v:.3f}" if isinstance(v, float) else str(v) for v in r) + " |" for r in fail.itertuples(index=False)]
    L += ["", f"Total explanations: {len(df)}; non-finite fidelity values: {int(s.n_nonfinite.sum())}; non-finite per-case "
          f"rank stability values: {int(s.rs_nonfinite.sum())}; total wall time: {df.wall_s.sum() / 60:.1f} min."]
    return "\n".join(L) + "\n"


def check(s, p):
    assert (p.wins <= p.n_cases).all()
    q = p[p.n_cases > 0]
    assert ((q.ci_lo <= q.diff_mean + 1e-12) & (q.diff_mean <= q.ci_hi + 1e-12)).all()
    m, f = s.set_index(KEYS).fidelity_mean, p[(p.metric == "fidelity") & (p.dropped == 0)]
    for r in f.itertuples():  # nothing dropped -> paired mean == difference of the two summary means
        a, b = r.comparison.split("-")
        assert np.isclose(r.diff_mean, m[r.dataset, r.model, a, r.n] - m[r.dataset, r.model, b, r.n]), r
    print(f"self-check passed ({len(f)} fidelity rows matched against summary.csv)")


if __name__ == "__main__":
    d = Path(sys.argv[1] if len(sys.argv) > 1 else "results/main")
    order = {"synthetic_dep": 0, "synthetic_indep": 1, "adult": 2}  # protocol order for every table (grid.csv is alphabetical)
    df = pd.read_csv(d / "grid.csv").sort_values("dataset", key=lambda c: c.map(order), kind="stable", ignore_index=True)
    complete(df, d)
    pc = per_case(df, d)
    s, p = summarize(pc), paired(pc)
    check(s, p)  # before anything is written
    pos = pc.groupby(["dataset", "model", "condition", "n"], sort=False).cumcount()  # case position = manifest position (checked above)
    held = pc[pos >= pc.dataset.map(USED)]  # cases never used in the pilot or the width sweep
    ph = paired(held) if len(held) else p.iloc[0:0]
    sub = pc[pc.condition.isin(["dep_aware", "independent"])]
    fail = pd.concat(g.nsmallest(5, "fidelity") for _, g in sub.groupby(["dataset", "model", "condition", "n"], sort=False))[FAIL]
    s.to_csv(d / "summary.csv", index=False)
    p.to_csv(d / "paired.csv", index=False)
    ph.to_csv(d / "paired_heldout_cases.csv", index=False)
    fail.to_csv(d / "failures.csv", index=False)
    (d / "summary.md").write_text(txt := report(df, s, p, fail, ph))
    print(txt)
