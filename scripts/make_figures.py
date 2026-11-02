"""Regenerate every figure in results/figures/ from the CSVs in results/.  Run from the repo root:
    .venv/bin/python scripts/make_figures.py
Aggregation everywhere: average over seeds within a case, then median (bars/markers) and IQR (whiskers) over cases."""
import textwrap
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Patch

RES = Path(__file__).resolve().parents[1] / "results"
OUT = RES / "figures"
NAMES = {"independent": "Independent (LIME-style)", "neighbors": "Training neighbors", "dep_aware": "Dependency-aware",
         "abl_no_dependency": "Ablation: no dependencies", "abl_no_locality": "Ablation: no locality"}
ORDER = list(NAMES)
# dataviz reference palette, categorical slots 1-5 in fixed order (validated: adjacent CVD dE >= 9.1, normal-vision >= 19.6)
COLOR = dict(zip(ORDER, ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]))
MARK = dict(zip(ORDER, "osD^v"))  # second channel for the scatter/line forms, where five hues alone are not CVD-safe
SURF, INK, INK2, MUTED = "#fcfcfb", "#0b0b0b", "#52514e", "#898781"
BLUE_LIGHT, BLUE_DARK = "#6da7ec", "#184f95"  # one-hue ordinal pair for n = 200 / 500 where no sampler is shown
TITLE = {("synthetic_dep", "lr"): "Synthetic, dependent features, linear model",
         ("synthetic_dep", "rf"): "Synthetic, dependent features, random forest",
         ("adult", "rf"): "Adult, random forest", ("synthetic_indep", "rf"): "Synthetic, independent features, random forest"}
FID = "Fidelity (held-out weighted R²)"
plt.rcParams.update({"figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF, "font.size": 12,
                     "axes.edgecolor": "#c3c2b7", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "axes.grid.axis": "y", "axes.axisbelow": True, "grid.color": "#e1e0d9",
                     "grid.linewidth": 0.8, "text.color": INK, "axes.labelcolor": INK2, "axes.titlesize": 13,
                     "xtick.color": INK2, "ytick.color": INK2, "xtick.labelsize": 10, "ytick.labelsize": 10,
                     "legend.frameon": False, "axes.titlelocation": "left"})


def per_case(d, keys, cols="fidelity"):
    """Seed mean within each case, grouped by keys (aggregate the result over cases)."""
    return d.groupby(keys + ["case"], dropna=False)[cols].mean().groupby(level=keys, dropna=False)


def agg(d, keys, col="fidelity"):
    g = per_case(d, keys, col)
    return pd.DataFrame({"med": g.median(), "q1": g.quantile(.25), "q3": g.quantile(.75)}).reset_index()


def save(fig, name):
    fig.savefig(OUT / name, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("wrote", OUT / name)


def shade(j, k):  # lighter = earlier level (n = 200 before 500); a lone level is full strength
    return 1 - 0.6 * (k - 1 - j) / max(k - 1, 1)


def bars(ax, a, inner=None, levels=(None,), ylo=None, labels=False):
    """x = sampler at its fixed slot; one bar per inner level present; IQR whiskers; bars below ylo are cut at ylo and
    labeled with their true median."""
    ss = [s for s in ORDER if s in set(a.sampler)]
    for s in ss:
        rs = [(j, r) for j, lv in enumerate(levels) for _, r in a[(a.sampler == s) & ((a[inner] == lv) if inner else True)].iterrows()]
        w = 0.7 / max(len(levels), 2)
        for k, (j, r) in enumerate(rs):
            x = ORDER.index(s) + (k - (len(rs) - 1) / 2) * w
            ax.bar(x, r.med if ylo is None else max(r.med, ylo), w - 0.04, color=COLOR[s], alpha=shade(j, len(levels)))
            ax.vlines(x, r.q1, r.q3, color=INK2, lw=1.2)
            if ylo is not None and r.med < ylo:
                ax.text(x, ylo + 0.03, f"{r.med:.2f}".replace("-", "\u2212"), rotation=90, ha="center", va="bottom",
                        fontsize=9, bbox=dict(fc=SURF, ec="none", pad=1))
            elif labels:
                ax.text(x, max(r.q3, r.med), f"{r.med:.2f}", ha="center", va="bottom", fontsize=10)
    ax.set_xticks([ORDER.index(s) for s in ss], [textwrap.fill(NAMES[s], 12) for s in ss])
    ax.set_xlim(-0.6, len(ORDER) - 0.4)
    ax.grid(axis="x", visible=False)


def shade_legend(fig, labels):
    fig.legend([Patch(color=INK2, alpha=shade(j, len(labels))) for j in range(len(labels))], labels,
               loc="upper right", ncol=len(labels), fontsize=11)


def fid_bars(ax, d, inner, levels, title):
    """Median-fidelity bars for one dataset panel; Adult is cut at -1 (its Independent medians sit near -2 to -3)."""
    a, ylo = agg(d, ["sampler", inner]), -1 if (d.dataset == "adult").all() else None
    bars(ax, a, inner, levels, ylo)
    ax.axhline(0, color=INK2, lw=1, ls="--")
    ax.set_ylim(ylo if ylo else min(0, a.q1.min()) - 0.05, 1)
    ax.set_title(title + ("\n(cut at −1, labels give the true median)" if ylo else ""), fontsize=12)
    ax.set_ylabel(FID)


def fig_fidelity(p):
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    for ax, (ds, m) in zip(axes.flat, TITLE):
        fid_bars(ax, p[(p.dataset == ds) & (p.model == m)], "n", (200, 500), TITLE[ds, m])
    shade_legend(fig, ["n = 200 queries", "n = 500 queries"])
    fig.suptitle("Fidelity by sampler: median over cases, whiskers span the IQR", x=0.01, ha="left", fontsize=14)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    save(fig, "fig_fidelity_by_sampler.png")


def fig_validity(p):
    d = p[(p.dataset == "adult") & (p.model == "rf") & (p.n == 500)]
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.8))
    for ax, col, lab in [(axes[0], "mean_nn_dist", "Mean distance to the nearest\ntraining record"),
                         (axes[1], "frac_seen_combo", "Share of samples whose category\ncombination occurs in training")]:
        bars(ax, agg(d, ["sampler"], col), labels=True)
        ax.set_ylabel(lab)
    axes[1].set_ylim(0, 1.1)
    fig.suptitle("How realistic are the samples? Adult, random forest, n = 500 (median over cases, IQR whiskers)",
                 x=0.01, ha="left", fontsize=14)
    fig.tight_layout()
    save(fig, "fig_validity.png")


def fig_fit_vs_heldout(p):
    d = p[(p.dataset == "adult") & (p.model == "rf")]
    fig, ax = plt.subplots(figsize=(7.5, 7.5))
    ax.plot([-3, 1], [-3, 1], color=MUTED, lw=1)
    for s in ORDER:
        r = d[d.sampler == s]
        ax.scatter(r.fit_r2, r.fidelity, s=40, marker=MARK[s], color=COLOR[s], edgecolor=SURF, lw=0.8, alpha=0.85,
                   label=NAMES[s])
    out = ((d[["fit_r2", "fidelity"]] < -3) | (d[["fit_r2", "fidelity"]] > 1)).any(axis=1)
    ax.text(-2.9, -2.9, f"{out.sum()} of {len(d)} explanations fall outside the axes\n"
            f"({out[d.sampler == 'independent'].sum()} of them Independent)", fontsize=10, color=INK2, va="bottom")
    ax.set(xlim=(-3, 1), ylim=(-3, 1), aspect="equal", xlabel="In-sample fit (weighted R² on the fit samples)",
           ylabel=FID)
    ax.grid(axis="x")
    ax.legend(loc="upper left", fontsize=10, title="Line: held-out = in-sample", title_fontsize=10)
    ax.set_title("Adult, random forest: in-sample fit looks fine, held-out fidelity does not", fontsize=12)
    save(fig, "fig_fit_vs_heldout.png")


def fig_first_start():
    d = pd.read_csv(RES / "first_start.csv")
    settings = [("synthetic_indep", 0.0, "Linear f,\nindependent features"), ("synthetic_dep", 0.0, "Linear f,\ncorrelated pair"),
                ("synthetic_dep", 0.5, "Linear f + noise\n(σ = 0.5)")]
    fig, ax = plt.subplots(figsize=(9, 5.5))
    for i, (ds, noise, _) in enumerate(settings):
        for j, (n, c) in enumerate([(200, BLUE_LIGHT), (500, BLUE_DARK)]):
            e = d[(d.dataset == ds) & (d.noise == noise) & (d.n == n)]
            mx, md, x = e.max_abs_err.max(), e.groupby(["sampler", "case"]).max_abs_err.mean().median(), i + (j - .5) * .3
            ax.vlines(x, md, mx, color=c, lw=2)
            ax.plot(x, md, "o", ms=9, mfc=SURF, mec=c, mew=2, label=f"Median, n = {n}" if i == 0 else None)
            ax.plot(x, mx, "o", ms=10, color=c, mec=SURF, mew=1.5, label=f"Max, n = {n}" if i == 0 else None)
            ax.annotate(f"{mx:.1e}", (x, mx), xytext=(0, 9), textcoords="offset points", ha="center", fontsize=9)
    ax.set_yscale("log")
    ax.set_ylim(1e-11, 3)
    ax.set_xticks(range(3), [s[2] for s in settings])
    ax.grid(axis="x", visible=False)
    ax.set_ylabel("Max |coefficient error| (log scale)")
    ax.legend(loc="upper left", ncol=2, fontsize=10)
    ax.set_title("First start: recovering a known linear predictor (max and median over cases, seeds, samplers)",
                 fontsize=12)
    save(fig, "fig_first_start.png")


def panels(d):
    return [(ds, m) for ds, m in TITLE if ((d.dataset == ds) & (d.model == m)).any()]


def fig_scale_sweep(d):
    d = d[d.width_rule == "default"]
    ps = panels(d)
    fig, axes = plt.subplots(1, len(ps), figsize=(7 * len(ps), 5.5), squeeze=False)
    for ax, (ds, m) in zip(axes[0], ps):
        q = d[(d.dataset == ds) & (d.model == m)]
        q = q[q.n == q.n.max()]  # ponytail: one budget per panel; facet by n if the sweep ever runs several
        t = per_case(q, ["sampler", "scale"], ["fidelity", "mean_dist_to_query"]).median().reset_index()
        for s in [s for s in ORDER if s in set(t.sampler)]:
            r = t[t.sampler == s].sort_values("scale")
            ax.plot(r.mean_dist_to_query, r.fidelity, color=COLOR[s], marker=MARK[s], lw=2, ms=8, mec=SURF,
                    label=NAMES[s])
            for _, k in r.dropna(subset=["scale"]).iterrows():
                ax.annotate(f"{k.scale:g}", (k.mean_dist_to_query, k.fidelity), xytext=(6, 4),
                            textcoords="offset points", fontsize=9, color=INK2)
        ax.grid(axis="x")
        ax.set(xlabel="Mean distance from samples to the query", ylabel=f"Median {FID[0].lower()}{FID[1:]}",
               title=f"{TITLE[ds, m]}, n = {q.n.max()}")
    axes[0][0].legend(fontsize=10, title="Labels: noise scale", title_fontsize=10)
    fig.suptitle("Fidelity vs neighborhood size at matched noise scales (default kernel width)", x=0.01, ha="left",
                 fontsize=14)
    fig.tight_layout()
    save(fig, "fig_scale_sweep.png")


def fig_width_sweep(d):
    rules = [r for r in ("default", "median", "half_median") if r in set(d.width_rule)]
    # keep (sampler, scale) settings run under more than one width rule: the width sweep proper
    d = d[d.groupby(["dataset", "model", "sampler", "scale"], dropna=False).width_rule.transform("nunique") > 1]
    ps = panels(d)
    fig, axes = plt.subplots(1, len(ps), figsize=(7 * len(ps), 5.5), squeeze=False)
    for ax, (ds, m) in zip(axes[0], ps):
        q = d[(d.dataset == ds) & (d.model == m)]
        fid_bars(ax, q[q.n == q.n.max()], "width_rule", rules, f"{TITLE[ds, m]}, n = {q.n.max()}")
    shade_legend(fig, ["Kernel width: " + r.replace("_", " ") for r in rules])
    fig.suptitle("Fidelity by kernel-width rule (median over cases, IQR whiskers)", x=0.01, ha="left", fontsize=14)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    save(fig, "fig_width_sweep.png")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    p = pd.read_csv(RES / "pilot.csv")
    fig_fidelity(p)
    fig_validity(p)
    fig_fit_vs_heldout(p)
    fig_first_start()
    print("skipped fig_stability_by_sampler.png: rank stability needs coefficient vectors, which no CSV stores")
    w4 = RES / "w4_scale_match.csv"
    if w4.exists():
        w = pd.read_csv(w4)
        fig_scale_sweep(w)
        fig_width_sweep(w)
    else:
        print(f"skipped fig_scale_sweep.png and fig_width_sweep.png: {w4.relative_to(RES.parent)} not found yet")
