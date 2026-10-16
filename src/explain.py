"""Local surrogate explanations with three perturbation neighborhoods: independent (LIME-style), training neighbors,
and dependency-aware. Samplers work in RAW feature space (DataFrame); the surrogate is fit in Z space = transform(X)."""
import time
from itertools import combinations

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.neighbors import NearestNeighbors


def kernel_weights(dist, width):
    return np.exp(-(dist**2) / width**2)


def weighted_ridge(Z, t, w, alpha=1e-3):
    """Weighted least squares, L2 penalty on the slope only (intercept unpenalized), closed form. Returns (intercept, coef)."""
    A = np.column_stack([np.ones(len(Z)), Z])
    P = alpha * np.eye(A.shape[1])
    P[0, 0] = 0.0
    beta = np.linalg.solve(A.T @ (w[:, None] * A) + P, A.T @ (w * t))
    return float(beta[0]), beta[1:]


def _wr2(f, g, w):
    f = np.asarray(f, float)
    return float(1 - np.sum(w * (f - g) ** 2) / np.sum(w * (f - np.average(f, weights=w)) ** 2))


def _knn(Z, z_x, k):
    d = np.linalg.norm(Z - z_x, axis=1)
    idx = np.argsort(d)[:k]
    return idx, d[idx]


def _combo_keys(X, categorical):
    """One string per row for its categorical tuple; numpy astype(str) maps NaN -> 'nan' so NaN is a level."""
    if not categorical:
        return np.full(len(X), "")
    return np.array(["|".join(r) for r in X[categorical].to_numpy().astype(str)])


def _marginal(X_train, c, n, rng):
    # value of a uniformly random training row == a draw from value_counts(dropna=False) frequencies; keeps dtype and NaN
    return X_train[c].iloc[rng.integers(len(X_train), size=n)].reset_index(drop=True)


def sample_independent(x, X_train, Z_train, z_x, numeric, categorical, n, rng, **kw):
    """LIME-style baseline. Numeric: x_j + N(0, std_train_j); categorical: training marginal (NaN is a level); every feature
    independently. Preserves NO dependencies: breaks numeric correlations and creates unseen categorical combinations."""
    S = x.iloc[np.zeros(n, int)].reset_index(drop=True)
    S[numeric] = x[numeric].to_numpy(float) + rng.normal(size=(n, len(numeric))) * X_train[numeric].std().to_numpy()
    for c in categorical:
        S[c] = _marginal(X_train, c, n, rng)
    return S


def sample_neighbors(x, X_train, Z_train, z_x, numeric, categorical, n, rng, k=200, **kw):
    """Training-neighbor baseline: n real records drawn uniformly with replacement from the k nearest training rows (Z space).
    Preserves ALL dependencies trivially (real records), but no fresh variation: <= k distinct points, duplicates waste budget."""
    return X_train.iloc[rng.choice(_knn(Z_train, z_x, k)[0], n)].reset_index(drop=True)


def sample_dependency_aware(x, X_train, Z_train, z_x, numeric, categorical, n, rng, k=200, scale=0.5, dependencies=True,
                            locked=(), **kw):
    """Dependency-aware neighborhood (original component). Anchor = one of the k nearest training rows (prob. ~ kernel of its
    Z distance); copy its categoricals as a block; add N(0, scale^2 * Sigma_stratum) to its numerics, where the stratum is the
    neighbors sharing its categorical tuple (all k if < 5 rows or no categoricals); clip numerics to the training range.
    `locked` numerics (a deterministic function of a categorical, e.g. Adult education-num given education) are copied with
    the block and never perturbed.
    Preserves: (a) only realized categorical combinations, (b) categorical->numeric compatibility (scale and correlation given
    the stratum; exact for locked partners, approximate when a stratum < 5 rows falls back to all k neighbors),
    (c) local numeric-numeric correlation. Not preserved: higher-order / non-Gaussian numeric structure.
    dependencies=False (ablation): categoricals redrawn from marginals, EVERY numeric coordinate takes its own independently
    drawn anchor (kills numeric-numeric and categorical-numeric structure), noise N(0, scale^2 * diag(global var)); clipped."""
    idx, d = _knn(Z_train, z_x, k)
    p = kernel_weights(d, 0.75 * np.sqrt(Z_train.shape[1]))
    p /= p.sum()
    a = rng.choice(len(idx), n, p=p)  # anchor = position in the neighbor list
    S = X_train.iloc[idx[a]].reset_index(drop=True)
    num, m = X_train[numeric].to_numpy(float), len(numeric)
    base = num[idx[a]]
    if dependencies:
        keys, nb, eps = _combo_keys(X_train.iloc[idx], categorical), num[idx], np.empty((n, m))
        for key in np.unique(keys[a]):
            s = keys == key
            cov = np.cov(nb[s] if s.sum() >= 5 else nb, rowvar=False).reshape(m, m) + 1e-6 * np.eye(m)
            rows = keys[a] == key
            eps[rows] = rng.multivariate_normal(np.zeros(m), scale**2 * cov, size=rows.sum())
        eps[:, [numeric.index(c) for c in locked]] = 0.0  # deterministic partners travel with the categorical block
    else:
        for c in categorical:
            S[c] = _marginal(X_train, c, n, rng)
        base = num[idx[rng.choice(len(idx), (n, m), p=p)], np.arange(m)]  # independent anchor per coordinate
        eps = rng.normal(size=(n, m)) * scale * num.std(0, ddof=1)
    S[numeric] = np.clip(base + eps, num.min(0), num.max(0))
    return S


def validity(Z_samples, nn, X_samples, X_train, categorical):
    """mean Z-space distance from each sample to its nearest training row (nn = fitted NearestNeighbors on Z_train);
    fraction of samples whose categorical tuple occurs in X_train."""
    # ponytail: rebuilds the training combo keys every call; cache them in Explainer if this shows up in profiles
    seen = np.isin(_combo_keys(X_samples, categorical), _combo_keys(X_train, categorical))
    return {"mean_nn_dist": float(nn.kneighbors(Z_samples, 1)[0].mean()), "frac_seen_combo": float(seen.mean())}


class Explainer:
    def __init__(self, predict_fn, transform, X_train, numeric, categorical, feature_names):
        self.predict_fn, self.transform, self.X_train = predict_fn, transform, X_train
        self.numeric, self.categorical = list(numeric), list(categorical)
        self.Z_train = np.asarray(transform(X_train), float)
        self.nn = NearestNeighbors(n_neighbors=1).fit(self.Z_train)
        self.p = self.Z_train.shape[1]
        self.feature_names = list(feature_names)
        # numerics that are a deterministic function of some categorical (Adult: education-num given education)
        # ponytail: an id-like categorical with one row per level would lock everything; none in these datasets
        self.locked = [c for c in self.numeric
                       if any(X_train.groupby(g, dropna=False)[c].nunique(dropna=False).max() == 1 for g in self.categorical)]

    def explain(self, x, sampler, n, seed, eval_X, locality=True, validity_weight=False, alpha=1e-3, **sampler_kw):
        """Fit a weighted ridge surrogate on sampler's neighborhood of the 1-row x; fidelity = weighted R^2 on the caller's eval_X."""
        Zf = lambda X: np.asarray(self.transform(X), float)
        width = 0.75 * np.sqrt(self.p)
        z_x = Zf(x)[0]
        t0 = time.perf_counter()
        S = sampler(x, self.X_train, self.Z_train, z_x, self.numeric, self.categorical, n, np.random.default_rng(seed),
                    locked=self.locked, **sampler_kw)
        Z_s, f_s = Zf(S), np.asarray(self.predict_fn(S), float)
        d = np.linalg.norm(Z_s - z_x, axis=1)
        w = kernel_weights(d, width) if locality else np.ones(n)
        if validity_weight:  # validity-aware weighting: down-weight samples far from any training row
            w = w * kernel_weights(self.nn.kneighbors(Z_s, 1)[0][:, 0], width)
        b0, coef = weighted_ridge(Z_s, f_s, w, alpha)
        runtime = time.perf_counter() - t0
        Z_e = Zf(eval_X)
        return {
            "coef": coef, "intercept": b0, "feature_names": self.feature_names,
            "prediction": float(np.asarray(self.predict_fn(x))[0]), "surrogate_prediction": float(b0 + z_x @ coef),
            "fidelity": _wr2(self.predict_fn(eval_X), b0 + Z_e @ coef, kernel_weights(np.linalg.norm(Z_e - z_x, axis=1), width)),
            "fit_r2": _wr2(f_s, b0 + Z_s @ coef, kernel_weights(d, width)),
            "validity": validity(Z_s, self.nn, S, self.X_train, self.categorical),
            "mean_dist_to_query": float(d.mean()), "n": n, "runtime_s": runtime,
        }


def rank_stability(coefs):
    """Mean pairwise Spearman correlation of |coef| across seeds. 1.0 = identical ranking."""
    return float(np.mean([spearmanr(np.abs(a), np.abs(b)).statistic for a, b in combinations(coefs, 2)]))


def default_eval_neighborhood(z_x, Z_pool, X_pool, k=200):
    """Predefined fidelity neighborhood: the k nearest held-out pool rows to z_x (Z space). Reuse it for every sampler/seed."""
    return X_pool.iloc[_knn(np.asarray(Z_pool, float), np.ravel(z_x), k)[0]].reset_index(drop=True)


if __name__ == "__main__":
    def toy(n, seed):
        r = np.random.default_rng(seed)
        a = r.normal(size=n)
        b = 0.8 * a + 0.6 * r.normal(size=n)
        g = pd.Series(r.choice(["u", "v", "w"], n, p=[0.5, 0.3, 0.2]))
        c = r.normal(size=n) + 2.0 * (g == "w").to_numpy()
        return pd.DataFrame({"a": a, "b": b, "c": c, "g": g.where(r.random(n) > 0.05)})

    X, Xdev = toy(3000, 0), toy(1000, 1)
    num, cat, true = ["a", "b", "c"], ["g"], np.array([2.0, -1.5, 0.5])
    f = lambda D: D[num].to_numpy(float) @ true
    T = lambda D: D[num].to_numpy(float)

    # 1. weighted ridge recovers a known linear function
    rr = np.random.default_rng(2)
    i = rr.choice(len(X), 500, replace=False)
    b0, coef = weighted_ridge(T(X.iloc[i]), f(X.iloc[i]), rr.uniform(0.1, 1, 500), alpha=1e-8)
    assert np.allclose(coef, true, atol=1e-6) and abs(b0) < 1e-6, coef
    from sklearn.linear_model import Ridge  # noisy, nonzero intercept, alpha=1: must equal sklearn's weighted ridge
    tn, wn = f(X.iloc[i]) + 3.0 + rr.normal(scale=0.5, size=500), rr.uniform(0.1, 1, 500)
    b0, coef = weighted_ridge(T(X.iloc[i]), tn, wn, alpha=1.0)
    sk = Ridge(alpha=1.0).fit(T(X.iloc[i]), tn, sample_weight=wn)
    assert np.allclose(coef, sk.coef_, atol=1e-8) and abs(b0 - sk.intercept_) < 1e-8, (coef, sk.coef_)

    E = Explainer(f, T, X, num, cat, feature_names=num)
    x = Xdev.iloc[[0]]
    z_x = T(x)[0]
    ev = default_eval_neighborhood(z_x, T(Xdev), Xdev)
    samplers = {"independent": (sample_independent, {}), "neighbors": (sample_neighbors, {}),
                "dep_aware": (sample_dependency_aware, {}), "dep_aware_nodep": (sample_dependency_aware, {"dependencies": False})}
    S, R = {}, {}
    for name, (fn, kw) in samplers.items():
        S[name] = s = fn(x, X, E.Z_train, z_x, num, cat, 500, np.random.default_rng(0), **kw)
        R[name] = r = E.explain(x, fn, 500, 0, ev, **kw)
        # 2. shape / dtype contract, coefficient recovery
        assert len(s) == 500 and list(s.columns) == list(X.columns) and (s.dtypes == X.dtypes).all(), s.dtypes
        assert all(s[c].dtype == np.float64 for c in num) and s["g"].map(lambda v: isinstance(v, str) or pd.isna(v)).all()
        if name == "neighbors":
            assert r["fidelity"] > 0.9, r["fidelity"]
        else:
            assert np.allclose(r["coef"], true, atol=1e-3), (name, r["coef"])
    r = E.explain(x, sample_dependency_aware, 500, 0, ev, locality=False, validity_weight=True)
    assert np.allclose(r["coef"], true, atol=1e-3), r["coef"]

    # 3. validity
    assert R["dep_aware"]["validity"]["frac_seen_combo"] == 1.0 and R["neighbors"]["validity"]["frac_seen_combo"] == 1.0
    assert R["dep_aware"]["validity"]["mean_nn_dist"] < R["independent"]["validity"]["mean_nn_dist"]

    # 4. correlated pair: dep-aware matches the LOCAL corr of the k=200 training neighbors (~0.3 here; the global 0.8 is not
    #    visible inside a 200-of-3000 ball), the ablation and independent sampler do not
    corr = {k: np.corrcoef(v["a"], v["b"])[0, 1] for k, v in S.items()}
    nb = X.iloc[_knn(E.Z_train, z_x, 200)[0]]
    corr["local_truth"] = np.corrcoef(nb["a"], nb["b"])[0, 1]
    print("corr(a,b):", {k: round(float(v), 3) for k, v in corr.items()})
    assert abs(corr["dep_aware"] - corr["local_truth"]) < 0.1 and corr["dep_aware"] > corr["dep_aware_nodep"] + 0.1, corr
    assert abs(corr["independent"]) < 0.2 and abs(corr["dep_aware_nodep"]) < 0.2, corr

    # 4b. locked deterministic partner: e = 2*[g=="w"] is copied with g, never perturbed
    X2, x2 = X.assign(e=(X.g == "w").astype(float) * 2), x.assign(e=(x.g == "w").astype(float) * 2)
    E2 = Explainer(f, lambda D: D[num + ["e"]].to_numpy(float), X2, num + ["e"], cat, num + ["e"])
    assert E2.locked == ["e"], E2.locked
    s2 = sample_dependency_aware(x2, X2, E2.Z_train, np.r_[z_x, 0.0], num + ["e"], cat, 500, np.random.default_rng(0), locked=E2.locked)
    assert (s2.e == (s2.g == "w") * 2.0).all()

    # 5. stability metric and fidelity sanity on a perfectly linear f
    assert rank_stability([true, true]) == 1.0
    assert abs(R["dep_aware"]["fidelity"] - R["dep_aware"]["fit_r2"]) < 1e-9 and R["dep_aware"]["fidelity"] > 1 - 1e-9

    # 6. summary table
    print(f"{'sampler':<16}{'n':>5}{'fidelity':>10}{'nn_dist':>9}{'seen':>6}{'runtime_s':>11}")
    for nn_ in (200, 500):
        for name, (fn, kw) in samplers.items():
            r = E.explain(x, fn, nn_, 0, ev, **kw)
            v = r["validity"]
            print(f"{name:<16}{nn_:>5}{r['fidelity']:>10.6f}{v['mean_nn_dist']:>9.4f}{v['frac_seen_combo']:>6.2f}{r['runtime_s']:>11.5f}")
    print("all checks passed")
