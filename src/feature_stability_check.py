"""Is the teammate's Adult feature-level stability (sum |coef| per original feature, src/feature_group_analysis_patch)
a cardinality x noise artifact? Reproduces it, compares it with a no-shared-signal noise null and with cardinality-robust
importances. Writes results/feature_groups/{stability_check.csv, cardinality.csv, stability_check.md}.
Run from the repo root: .venv/bin/python src/feature_stability_check.py"""
import json
import time
import warnings
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import rankdata, spearmanr

from data import build_preprocessor, load_dataset

CONDITIONS = ["independent", "independent_matched", "neighbors", "dep_aware", "abl_no_dependency", "abl_no_locality"]
BUDGETS, N_NULL, TOL, OUT = (200, 500), 20, 1e-8, Path("results/feature_groups")
DEFS = ["coefficient_level", "sum_abs", "mean_abs", "l2_norm", "query_level"]
warnings.simplefilter("ignore", RuntimeWarning)  # undefined Spearman pairs become NaN and are counted in n_undefined


def stab(V):
    """V (..., seeds, k) -> (mean pairwise Spearman over seed pairs, undefined pairs excluded; number of undefined pairs).
    Spearman = Pearson of average ranks, as scipy; a constant vector (all ties) makes its pairs NaN."""
    R = rankdata(V, axis=-1)
    R -= R.mean(-1, keepdims=True)
    R /= np.linalg.norm(R, axis=-1, keepdims=True)
    i, j = np.triu_indices(V.shape[-2], 1)
    P = (R[..., i, :] * R[..., j, :]).sum(-1)
    return np.nanmean(P, -1), np.isnan(P).sum(-1)


def importances(V, M, card, act):
    """V (..., cases, seeds, 105) coefficients -> {definition: (..., cases, seeds, 14)} original-feature importances."""
    A = np.abs(V)
    return {"sum_abs": A @ M, "mean_abs": A @ M / card, "l2_norm": np.sqrt(V ** 2 @ M / card),
            "query_level": (A * act[:, None]) @ M}


def check(model, M, card, act, tol):
    """-> importances and {definition: (stability, n_undefined)}, each (1 + N_NULL, condition, budget, case); [0] observed."""
    C = np.load(f"results/main/coefs_adult_{model}.npy")  # (condition, budget, case, seed, 105)
    C = np.where(np.abs(C) < tol, 0.0, C)
    null = np.random.default_rng(0).standard_normal((N_NULL, *C.shape)) * C.std(axis=3, keepdims=True)
    V = np.concatenate([C[None], null])  # null: independent N(0, s_j^2) per seed, no signal shared across seeds
    I = importances(V, M, card, act)
    res = {d: stab(x) for d, x in I.items()}
    cl, cu = np.full(V.shape[:4], np.nan), np.zeros(V.shape[:4], int)
    for ci, bi, k in np.ndindex(C.shape[:3]):  # explain.rank_stability: |coef|, minus coefs that are zero in every seed
        keep = np.any(C[ci, bi, k] != 0, axis=0)  # (the null is zero exactly there too: s_j = 0)
        cl[:, ci, bi, k], cu[:, ci, bi, k] = stab(np.abs(V[:, ci, bi, k][..., keep]))
    res["coefficient_level"] = (cl, cu)
    return I, res


def snr(I):
    """(..., seeds, 14) -> between-feature variance of the seed-mean importance / mean within-feature across-seed variance."""
    return I.mean(-2).var(-1, ddof=1) / I.var(-2, ddof=1).mean(-1)


def md(t):  # DataFrame -> markdown (tabulate is not installed)
    return "\n".join("| " + " | ".join(map(str, r)) + " |" for r in [t.columns, ["---"] * t.shape[1], *t.values])


t0 = time.perf_counter()
ds = load_dataset("adult")
pre = build_preprocessor(ds.numeric, ds.categorical).fit(ds.X_train)
names = json.load(open("results/main/features_adult.json"))
raw = ds.numeric + ds.categorical
feat = [max((f for f in raw if t == f or t.startswith(f + "_")), key=len) for t in (n.split("__", 1)[1] for n in names)]
M = (np.array(feat)[:, None] == np.array(raw)).astype(float)  # (105, 14) column -> original feature
card = M.sum(0)
Z_x = pre.transform(ds.X_test.iloc[ds.explain_idx])
act = (np.char.startswith(names, "num__") | (Z_x > 0.5)).astype(float)  # numerics + the query's active one-hot level

rows, crows, srows = [], [], []
for tol, model in product((0.0, TOL), ("lr", "rf")):
    I, res = check(model, M, card, act, tol)
    for (ci, cond), (bi, n) in product(enumerate(CONDITIONS), enumerate(BUDGETS)):
        for d in DEFS:
            s, u = res[d][0][:, ci, bi], res[d][1][0, ci, bi]
            obs, null = np.nanmean(s[0]), np.nanmean(s[1:])
            rows.append(dict(model=model, condition=cond, n=n, definition=d + ("_snap" if tol else ""), stability_mean=obs,
                             stability_sd=np.nanstd(s[0], ddof=1), null_stability_mean=null, excess=obs - null,
                             n_undefined=int(u.sum())))
        if tol:
            continue
        S = I["sum_abs"][0, ci, bi]  # (case, seed, 14)
        mi, mr = S.mean((0, 1)), rankdata(-S, axis=-1).mean((0, 1))  # rank 1 = most important
        crows += [dict(model=model, condition=cond, n=n, feature=f, cardinality=int(card[fi]), mean_importance=mi[fi],
                       mean_rank=mr[fi]) for fi, f in enumerate(raw)]
        if model == "rf" and n == 500:
            srows += [dict(condition=cond, definition=d, snr_median=np.median(r[0]), null_snr_median=np.median(r[1:]))
                      for d in DEFS[1:] for r in [snr(I[d][:, ci, bi])]]
df, cdf, sdf = pd.DataFrame(rows), pd.DataFrame(crows), pd.DataFrame(srows)

# Step 0 + column order: the one check. Teammate's feature-level numbers and the project's coefficient-level rank_stability.
mate = pd.read_csv("src/feature_group_analysis_patch/feature_group_stability_summary.csv")
main = pd.read_csv("results/main/summary.csv").query("dataset == 'adult'")
g = df.set_index(["model", "condition", "n", "definition"])
assert pre.get_feature_names_out().tolist() == names
assert all(abs(g.loc[(r.model, r.condition, r.n, "sum_abs"), "stability_mean"] - r.feature_level_mean) < 1e-6 for r in mate.itertuples())
assert all(abs(g.loc[(r.model, r.condition, r.n, "coefficient_level"), "stability_mean"] - r.rank_stability) < 1e-6 for r in main.itertuples())

OUT.mkdir(parents=True, exist_ok=True)
df.to_csv(OUT / "stability_check.csv", index=False)
cdf.to_csv(OUT / "cardinality.csv", index=False)
v = lambda m, c, d, col="stability_mean", n=500: g.loc[(m, c, n, d), col]
cell = lambda m, c, d: f"{v(m, c, d):.3f} / {v(m, c, d, 'null_stability_mean'):.3f}"
tab = lambda m, defs: md(pd.DataFrame({"condition": CONDITIONS, **{d: [cell(m, c, d) for c in CONDITIONS] for d in defs}}))
rho = {k: spearmanr(x.cardinality, x.mean_importance).statistic for k, x in cdf.groupby(["model", "n", "condition"])}
lst = cdf.query("model == 'rf' and n == 500").pivot(index=["feature", "cardinality"], columns="condition")
lst = lst.reset_index().sort_values("cardinality", ascending=False)
lst = pd.DataFrame({"feature": lst.feature, "cardinality": lst.cardinality,
                    **{f"{c} {k}": lst[(col, c)].round(3) for c in ("independent", "dep_aware")
                       for k, col in (("importance", "mean_importance"), ("rank", "mean_rank"))}})
sn = sdf.set_index(["condition", "definition"])
und = df.query("definition == 'query_level'").n_undefined.sum()
f = lambda m, c, d, col="stability_mean", n=500: f"{v(m, c, d, col, n):.3f}"
ON = lambda m, c, d, n=500: f"{f(m, c, d, n=n)} (null {f(m, c, d, 'null_stability_mean', n)})"
EX = lambda m, c, d, n=500: f(m, c, d, "excess", n)
ROB = ["mean_abs", "l2_norm", "query_level"]
gap = {(m, n, d): v(m, "dep_aware", d, n=n) - v(m, "independent", d, n=n) for m, n, d in product(("rf", "lr"), BUDGETS, DEFS)}
nsum = df.query("definition == 'sum_abs'").null_stability_mean
nr = cdf.set_index(["model", "n", "condition", "feature"]).mean_rank
Crf = np.load("results/main/coefs_adult_rf.npy")
Z0 = Crf[0, 1] == 0  # independent, n=500: coefficients exactly 0 in some seeds but not all (rare level drawn or not)
tiny = np.mean((Crf[2, 1] != 0) & (np.abs(Crf[2, 1]) < TOL))  # neighbors, n=500: numerical zeros
snapped = df.definition.str.endswith("_snap")
shift = np.abs(df[snapped].stability_mean.to_numpy() - df[~snapped].stability_mean.to_numpy()).max()
nb = max(abs(v(m, "neighbors", d) - v(m, "dep_aware", d)) for m in ("rf", "lr") for d in ROB)
rg = [gap[(m, 500, d)] for m in ("rf", "lr") for d in ROB]
de = [v(m, "dep_aware", d, "excess") for m in ("rf", "lr") for d in ("mean_abs", "l2_norm")]
VERDICT = [
    f"- **Mostly an artifact.** sum_abs at n=500: RF independent {ON('rf', 'independent', 'sum_abs')} vs dep_aware "
    f"{ON('rf', 'dep_aware', 'sum_abs')}; LR independent {ON('lr', 'independent', 'sum_abs')} vs dep_aware "
    f"{ON('lr', 'dep_aware', 'sum_abs')}. Noise with no signal shared across seeds gets {nsum.min():.3f}-{nsum.max():.3f} "
    f"in all 24 model x condition x n rows. It ranks cardinality: Spearman(cardinality, importance) RF n=500 is "
    f"{rho[('rf', 500, 'independent')]:.2f} for independent vs {rho[('rf', 500, 'dep_aware')]:.2f} for dep_aware, and "
    f"native-country (41 levels) has mean rank {nr[('rf', 500, 'independent', 'native-country')]:.2f} under independent "
    f"({nr[('rf', 500, 'dep_aware', 'native-country')]:.2f} under dep_aware).",
    f"- **Not entirely.** Above the null, sum_abs excess is independent {EX('rf', 'independent', 'sum_abs')} vs dep_aware "
    f"{EX('rf', 'dep_aware', 'sum_abs')} (RF n=500), {EX('rf', 'independent', 'sum_abs', 200)} vs "
    f"{EX('rf', 'dep_aware', 'sum_abs', 200)} (RF n=200), {EX('lr', 'independent', 'sum_abs')} vs "
    f"{EX('lr', 'dep_aware', 'sum_abs')} (LR n=500). So independent keeps a small residual edge under this metric "
    f"(mainly RF). The null does not account for it, but it sits in the ~{1 - nsum.mean():.2f} of headroom above the floor.",
    f"- **What survives: dep_aware is more stable than independent under every cardinality-robust definition** "
    f"(n=500, dep_aware vs independent). RF: mean_abs {f('rf', 'dep_aware', 'mean_abs')} vs {f('rf', 'independent', 'mean_abs')}, "
    f"l2_norm {f('rf', 'dep_aware', 'l2_norm')} vs {f('rf', 'independent', 'l2_norm')}, query_level "
    f"{f('rf', 'dep_aware', 'query_level')} vs {f('rf', 'independent', 'query_level')}. LR: {f('lr', 'dep_aware', 'mean_abs')} vs "
    f"{f('lr', 'independent', 'mean_abs')}, {f('lr', 'dep_aware', 'l2_norm')} vs {f('lr', 'independent', 'l2_norm')}, "
    f"{f('lr', 'dep_aware', 'query_level')} vs {f('lr', 'independent', 'query_level')}. This "
    f"{'holds' if all(gap[(m, n, d)] > 0 for m, n, d in product(('rf', 'lr'), BUDGETS, ROB)) else 'does NOT hold'} "
    f"at both budgets for both models. Under mean_abs and "
    f"l2_norm independent sits at its null (excess RF {EX('rf', 'independent', 'mean_abs')}, "
    f"{EX('rf', 'independent', 'l2_norm')}; LR {EX('lr', 'independent', 'mean_abs')}, {EX('lr', 'independent', 'l2_norm')}), "
    f"while dep_aware is {min(de):.3f}-{max(de):.3f} above its null. neighbors "
    f"matches dep_aware within {nb:.3f}.",
    f"- **Query level** (the coefficient of the record's own category): both samplers beat their null (RF excess "
    f"independent {EX('rf', 'independent', 'query_level')}, dep_aware {EX('rf', 'dep_aware', 'query_level')}). But dep_aware's "
    f"null is already {f('rf', 'dep_aware', 'query_level', 'null_stability_mean')} vs "
    f"{f('rf', 'independent', 'query_level', 'null_stability_mean')}: features that do not vary in a local neighborhood get "
    f"~0 in every seed, and the null keeps that. Part of the query-level gap is that cheap agreement.",
    f"- **Report**: do not cite sum-|coef| feature-level stability as evidence that independent is more stable. It is "
    f"dominated by a cardinality floor (null {nsum.min():.2f}-{nsum.max():.2f}). Report a cardinality-normalised (mean_abs) or "
    f"query-level feature stability with its null next to coefficient-level rank stability. The coefficient-level direction "
    f"holds at the feature level, with a smaller gap (RF n=500 dep_aware - independent: coefficient "
    f"{gap[('rf', 500, 'coefficient_level')]:.3f}, mean_abs {gap[('rf', 500, 'mean_abs')]:.3f}, l2_norm "
    f"{gap[('rf', 500, 'l2_norm')]:.3f}, query_level {gap[('rf', 500, 'query_level')]:.3f}).",
    f"- **Uncertain**: (a) the Gaussian null is not a strict floor. For independent, coefficient-level stability is "
    f"{ON('rf', 'independent', 'coefficient_level')}. This fits {np.mean(Z0.any(1) & ~Z0.all(1)):.0%} of its coefficients "
    f"being exactly 0 in some seeds but not others (rare levels drawn or not), zero inflation that a Gaussian null does not "
    f"reproduce. So 'excess' is a rough scale. (b) The size of the robust gap depends on the "
    f"definition ({min(rg):.3f}-{max(rg):.3f}). (c) One-hot levels are identified only up to a shift within a feature "
    f"(no level is dropped; the tie is broken by ridge alpha), and per-level and per-SD numeric magnitudes are not on one "
    f"scale. (d) Numerical zeros (|coef| < {TOL:g}, {tiny:.1%} of neighbors coefficients) move any stability by at most "
    f"{shift:.3f} (sensitivity table). (e) The variance-ratio SNR does not order the samplers the way Spearman does (RF n=500 mean_abs: "
    f"independent {sn.loc[('independent', 'mean_abs'), 'snr_median']:.1f} vs dep_aware "
    f"{sn.loc[('dep_aware', 'mean_abs'), 'snr_median']:.1f}; nulls {sn.loc[('independent', 'mean_abs'), 'null_snr_median']:.1f} "
    f"vs {sn.loc[('dep_aware', 'mean_abs'), 'null_snr_median']:.1f}). It is driven by how far apart the few largest features "
    f"are, while Spearman weighs all 14 ranks. (f) Only 5 seeds per case."]
text = [
    "# Is the feature-level stability of the independent sampler a cardinality artifact?", "",
    "The teammate's sum-of-|coef| feature importance makes the independent sampler look more stable than dep_aware at the "
    "original-feature level, reversing the coefficient-level result. We test whether that ranking is fixed by cardinality "
    "times estimation noise (a noise null with no signal shared across seeds) and recompute stability with "
    "cardinality-robust importances.", "",
    "Cells: observed / noise-null mean pairwise Spearman across 5 seeds, mean over 100 cases. Null: each coefficient drawn "
    f"independently per seed from N(0, s_j^2), s_j its across-seed sd, {N_NULL} repetitions. Undefined seed pairs "
    f"(a constant importance vector) are excluded and counted in `n_undefined` (total over all query_level rows: {und}).", "",
    "## Adult RF, n = 500", "", tab("rf", DEFS), "", "## Adult LR, n = 500", "", tab("lr", DEFS), "",
    "## Cardinality dependence of sum_abs", "",
    "Spearman(cardinality, mean sum_abs importance) over the 14 features:", "",
    *[f"- {m.upper()} n={n}: " + ", ".join(f"{c} {rho[(m, n, c)]:.2f}" for c in CONDITIONS) for m, n in product(("rf", "lr"), BUDGETS)],
    "", "Adult RF n = 500, sum_abs importance and mean rank (1 = largest), mean over cases and seeds:", "", md(lst), "",
    "## Signal-to-noise (RF n = 500)", "",
    "Median over cases of var_features(seed-mean importance) / mean_features(var_seeds(importance)); observed / null.", "",
    md(pd.DataFrame({"condition": ["independent", "dep_aware", "neighbors"],
                     **{d: [f"{sn.loc[(c, d), 'snr_median']:.1f} / {sn.loc[(c, d), 'null_snr_median']:.1f}"
                            for c in ("independent", "dep_aware", "neighbors")] for d in DEFS[1:]}})), "",
    f"## Sensitivity: |coef| < {TOL:g} set to 0 (numerical zeros), n = 500", "",
    "RF:", "", tab("rf", [d + "_snap" for d in DEFS]), "", "LR:", "", tab("lr", [d + "_snap" for d in DEFS]), "",
    "## Verdict", "", *VERDICT]
(OUT / "stability_check.md").write_text("\n".join(text) + "\n")
print(df.query("n == 500").round(3).to_string(index=False), f"\nruntime {time.perf_counter() - t0:.1f}s")
