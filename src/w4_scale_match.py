"""Week-4 decisions (RF): scale-matched independent baseline + kernel width. Block A: scale sweep, default width. Block B:
median / half_median widths for dep_aware(0.5) and the independent scale closest to it in mean distance to the query (default-
width rows come from Block A, not re-run). Writes results/w4_scale_match.{csv,md}. Run from the repo root."""
import time
from pathlib import Path

import numpy as np
import pandas as pd

from data import fit_models, load_dataset
from explain import (Explainer, default_eval_neighborhood, rank_stability, sample_dependency_aware,
                     sample_independent, sample_neighbors)

N, SEEDS, SCALES, OUT = 500, range(3), (0.25, 0.5, 0.75, 1.0), Path("results")
FN = {"independent": sample_independent, "neighbors": sample_neighbors, "dep_aware": sample_dependency_aware}
KEYS = ["dataset", "sampler", "scale", "width_rule"]
BLOCK_A = [(s, c, "default") for s in ("independent", "dep_aware") for c in SCALES] + [("neighbors", np.nan, "default")]


def run(ds, E, pre, Z_dev, cases, configs, rows):
    for case in cases:
        x = ds.X_test.iloc[[case]]
        z_x = pre.transform(x)[0]
        ev = default_eval_neighborhood(z_x, Z_dev, ds.X_dev, k=200)
        med = float(np.median(np.linalg.norm(pre.transform(ev) - z_x, axis=1)))
        widths = {"default": 0.75 * np.sqrt(E.p), "median": med, "half_median": med / 2}  # default == explain's None
        for s, scale, wr in configs:
            kw = {} if np.isnan(scale) else {"scale": scale}
            for seed in SEEDS:
                r = E.explain(x, FN[s], N, seed, ev, width=widths[wr], **kw)
                rows.append(dict(dataset=ds.name, model="rf", sampler=s, scale=scale, width_rule=wr, n=N, case=case,
                                 seed=seed, fidelity=r["fidelity"], fit_r2=r["fit_r2"],
                                 mean_dist_to_query=r["mean_dist_to_query"], **r["validity"], runtime_s=r["runtime_s"],
                                 coef=r["coef"], mean_weight=r["mean_weight"], width=widths[wr]))


def summarize(df):
    g = dict(dropna=False, sort=False)  # dropna=False: neighbors has scale NaN
    pc = df.groupby(KEYS + ["case"], **g).agg(
        fidelity=("fidelity", "mean"), rs=("coef", lambda c: rank_stability(list(c))), dist=("mean_dist_to_query", "mean"),
        nn=("mean_nn_dist", "mean"), mw=("mean_weight", "mean"))
    s = pc.groupby(KEYS, **g).agg(fid=("fidelity", "mean"), sd=("fidelity", "std"), med=("fidelity", "median"),
                                  rs=("rs", "mean"), dist=("dist", "mean"), nn=("nn", "mean"), mw=("mw", "mean"))
    return pc.sort_index(), s.reset_index()


def paired(pc, d, wr, scale):
    """per-case fidelity gain dep_aware(0.5) - independent(scale) at width rule wr -> (mean, sd, wins, cases)"""
    diff = pc.loc[(d, "dep_aware", 0.5, wr)].fidelity - pc.loc[(d, "independent", scale, wr)].fidelity
    return diff.mean(), diff.std(), int((diff > 0).sum()), len(diff)


if __name__ == "__main__":
    T0, rows, match = time.perf_counter(), [], {}
    for name, n_cases in [("synthetic_dep", 30), ("adult", 15)]:
        ds = load_dataset(name)
        m = fit_models(ds)["rf"]
        pre = m[:-1]
        E = Explainer(lambda X: m.predict_proba(X)[:, 1], pre.transform, ds.X_train, ds.numeric, ds.categorical,
                      pre.get_feature_names_out())
        Z_dev, cases = pre.transform(ds.X_dev), ds.explain_idx[:n_cases]
        t = time.perf_counter()
        run(ds, E, pre, Z_dev, cases, BLOCK_A, rows)
        print(f"== {name} Block A (scale sweep): {len(cases)} cases in {time.perf_counter() - t:.1f}s", flush=True)
        a = pd.DataFrame(rows).query("dataset == @name").groupby(["sampler", "scale"]).mean_dist_to_query.mean()
        match[name] = float((a["independent"] - a[("dep_aware", 0.5)]).abs().idxmin())
        print(f"   mean dist: dep_aware(0.5) {a['dep_aware', 0.5]:.3f}, independent {a['independent'].round(3).to_dict()}", flush=True)
        t = time.perf_counter()
        run(ds, E, pre, Z_dev, cases, [(s, c, wr) for s, c in [("dep_aware", 0.5), ("independent", match[name])]
                                       for wr in ("median", "half_median")], rows)
        print(f"== {name} Block B (width sweep): {len(cases)} cases in {time.perf_counter() - t:.1f}s", flush=True)

    df = pd.DataFrame(rows)
    df.drop(columns=["coef", "mean_weight", "width"]).to_csv(OUT / "w4_scale_match.csv", index=False)
    pc, s = summarize(df)
    v = lambda d, smp, sc, wr="default": s.set_index(KEYS).sort_index().loc[(d, smp, sc, wr)]
    WR, wd = ("default", "median", "half_median"), df.groupby(["dataset", "width_rule"]).width.mean()
    fmt = lambda r: f"{r.fid:.3f} ± {r.sd:.3f} | {r.med:.3f} | {r.rs:.3f}"
    lines = ["# Week-4 scale match and kernel width (RF, n=500, 3 seeds)", "",
             "fidelity = mean ± sd (and median) over cases of the per-case seed mean; rank_stability = mean over cases of the "
             "mean pairwise Spearman of |coef| over seeds; mean_weight = mean kernel weight over the 500 fit samples. Fidelity "
             "uses the SAME width on the 200 eval points, so different width rules score different weightings of them. "
             "rank_stability counts one-hot coefs that are exactly 0 in every seed (absent categories) as agreeing ranks, "
             "which inflates it on Adult for samplers that copy categorical blocks."]
    for d in match:
        lines += ["", f"## {d} ({df[df.dataset == d].case.nunique()} cases)", "",
                  f"Table 1: scale sweep (default width 0.75*sqrt(p) = {wd[d, 'default']:.2f})", "",
                  "| sampler | scale | fidelity | fidelity_med | rank_stability | mean_dist_to_query | mean_nn_dist |",
                  "|---|---|---|---|---|---|---|"]
        lines += [f"| {r.sampler} | {r.scale} | {fmt(r)} | {r.dist:.3f} | {r.nn:.3f} |"
                  for r in s[(s.dataset == d) & (s.width_rule == "default")].itertuples()]
        lines += ["", f"Table 2: width sweep (mean width over cases: median {wd[d, 'median']:.2f}, half_median "
                  f"{wd[d, 'half_median']:.2f}; independent at its matched scale {match[d]})", "",
                  "| sampler | scale | width_rule | fidelity | fidelity_med | rank_stability | mean_weight |",
                  "|---|---|---|---|---|---|---|"]
        lines += [f"| {smp} | {sc} | {wr} | {fmt(v(d, smp, sc, wr))} | {v(d, smp, sc, wr).mw:.3f} |"
                  for smp, sc in [("dep_aware", 0.5), ("independent", match[d])] for wr in WR]
    # ponytail: verdict words were written after reading this deterministic run; every number is live
    pair, ind = {}, lambda d, sc: v(d, "independent", sc)
    for d in match:
        a, i, (mu, sdv, k, nc) = v(d, "dep_aware", 0.5), ind(d, match[d]), paired(pc, d, "default", match[d])
        pair[d] = (f"dep_aware(0.5, dist {a.dist:.2f}) vs independent({match[d]}, dist {i.dist:.2f}): fidelity {a.fid:.3f} vs "
                   f"{i.fid:.3f} (median {a.med:.3f} vs {i.med:.3f}), paired per-case gain {mu:+.3f} ± {sdv:.3f}, dep_aware "
                   f"higher in {k}/{nc} cases, rank stability {a.rs:.3f} vs {i.rs:.3f}")
    mw = lambda wr, smp="dep_aware": v("adult", smp, 0.5 if smp == "dep_aware" else match["adult"], wr).mw
    gap = lambda d: "/".join(f"{paired(pc, d, wr, match[d])[0]:+.3f}" for wr in WR)
    lines += ["", f"- (1) synthetic_dep: yes; scale does not explain the pilot gap. Matched pair {pair['synthetic_dep']}. "
              f"Shrinking independent's noise hurts (scale 0.25: {ind('synthetic_dep', 0.25).fid:.3f}).",
              "- (2) Adult: not matchable with this knob: scale shrinks only numeric noise while the 8 categoricals are still "
              f"drawn from marginals, so independent stays >= {ind('adult', 0.25).dist:.2f} from the query vs dep_aware <= "
              f"{v('adult', 'dep_aware', 1.0).dist:.2f}. Closest pair {pair['adult']}. Independent improves as its scale "
              "shrinks, so part of this gap is distance; a true match needs a categorical keep-probability knob.",
              f"- (3) Use `median`: it fixes Adult's near-uniform default kernel (dep_aware mean weight {mw('default'):.3f} -> "
              f"{mw('median'):.3f}), stays close to the default width on synthetic_dep, and dep_aware fidelity and rank stability "
              f"are no worse than default on either dataset. half_median over-concentrates (Adult mean weight "
              f"{mw('half_median'):.3f} dep_aware, {mw('half_median', 'independent'):.3f} independent), costs dep_aware fidelity "
              "and stability on synthetic_dep, and makes fidelity a much more local target. The dep_aware - independent gap barely moves "
              f"across default/median/half_median (synthetic_dep {gap('synthetic_dep')}, Adult {gap('adult')}), so the "
              "sampler verdict does not depend on the width."]
    (OUT / "w4_scale_match.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"total runtime {time.perf_counter() - T0:.1f}s")
