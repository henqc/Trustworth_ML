import hashlib
import json
import time
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


@dataclass
class Dataset:
    name: str
    X_train: pd.DataFrame; y_train: np.ndarray
    X_dev: pd.DataFrame;   y_dev: np.ndarray
    X_test: pd.DataFrame;  y_test: np.ndarray
    numeric: list[str]; categorical: list[str]
    explain_idx: np.ndarray            # 100 positional indices into X_test: the fixed explanation cases
    linear_w: np.ndarray | None = None # analytic linear predictor weights over `numeric` columns (synthetic only)
    linear_b: float | None = None


W_TRUE = np.array([2.0, -1.5, 1.0, 0.5, 0.0, 0.0, 0.8, -0.8, 0.0, 0.3]); B_TRUE = 0.0

ADULT_COLS = ["age", "workclass", "fnlwgt", "education", "education-num", "marital-status", "occupation",
              "relationship", "race", "sex", "capital-gain", "capital-loss", "hours-per-week", "native-country", "income"]
ADULT_NUMERIC = ["age", "fnlwgt", "education-num", "capital-gain", "capital-loss", "hours-per-week"]
ADULT_CATEGORICAL = [c for c in ADULT_COLS[:-1] if c not in ADULT_NUMERIC]


def make_synthetic(n=10000, dependent=True, seed=0):
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((n, len(W_TRUE)))
    if dependent:
        X[:, 1] = 0.8 * X[:, 0] + 0.6 * X[:, 1]  # corr(x1, x2) = 0.8, var(x2) = 1
    y = (rng.random(n) < 1 / (1 + np.exp(-(X @ W_TRUE + B_TRUE)))).astype(int)
    return pd.DataFrame(X, columns=[f"x{i + 1}" for i in range(X.shape[1])]), y, W_TRUE, B_TRUE


def linear_predictor(w, b):
    return lambda X: np.asarray(X, dtype=float) @ w + b  # linear logit, not sigmoid


def load_adult(data_dir="data/adult"):
    def read(f, skip):
        df = pd.read_csv(Path(data_dir) / f, header=None, names=ADULT_COLS, skiprows=skip,
                         skipinitialspace=True, na_values="?")
        y = df.pop("income").str.strip().str.startswith(">50K").to_numpy(dtype=int)
        df[ADULT_NUMERIC] = df[ADULT_NUMERIC].astype("float64")
        return df, y
    return *read("adult.data", 0), *read("adult.test", 1)  # adult.test line 1 is "|1x3 Cross validator"


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def build_preprocessor(numeric, categorical):
    return ColumnTransformer([
        ("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), numeric),
        ("cat", make_pipeline(SimpleImputer(strategy="most_frequent"),
                              OneHotEncoder(handle_unknown="ignore", sparse_output=False)), categorical),
    ], sparse_threshold=0)


def load_dataset(name, manifest_path="manifests/splits.json"):
    m = json.load(open(manifest_path))[name]
    idx = lambda k: np.array(m[k], dtype=int)
    if name == "adult":
        for f, h in m["sha256"].items():  # same manifest + same files -> identical splits
            assert sha256(Path("data/adult") / f) == h, f"{f} does not match manifest hash"
        X, y, X_test, y_test = load_adult()
        num, cat, w, b = ADULT_NUMERIC, ADULT_CATEGORICAL, None, None
    else:
        X, y, w, b = make_synthetic(m["n"], m["dependent"], m["gen_seed"])
        t = idx("test_idx")
        X_test, y_test = X.iloc[t].reset_index(drop=True), y[t]
        num, cat = list(X.columns), []
    tr, dv = idx("train_idx"), idx("dev_idx")
    return Dataset(name, X.iloc[tr].reset_index(drop=True), y[tr], X.iloc[dv].reset_index(drop=True), y[dv],
                   X_test, y_test, num, cat, idx("explain_idx"), w, b)


def fit_models(ds, seed=0):
    pre = lambda: build_preprocessor(ds.numeric, ds.categorical)
    models = {"lr": Pipeline([("pre", pre()), ("clf", LogisticRegression(max_iter=2000))]),
              "rf": Pipeline([("pre", pre()), ("clf", RandomForestClassifier(
                  n_estimators=200, min_samples_leaf=2, n_jobs=-1, random_state=seed))])}
    for k, mdl in models.items():
        t = time.perf_counter()
        mdl.fit(ds.X_train, ds.y_train)  # fit on train only (preprocessor included)
        print(f"{ds.name} {k}: dev acc {mdl.score(ds.X_dev, ds.y_dev):.4f}  fit {time.perf_counter() - t:.1f}s")
    return models


def dependency_report(X, numeric, categorical):
    r = X[numeric].corr().abs()
    num = [("pearson_abs", a, b, r.loc[a, b]) for a, b in combinations(numeric, 2)]
    # ponytail: discrete numerics (<=20 levels, e.g. education-num) join the Cramer's V pool so
    # education~education-num shows up; add a mixed-type measure if more numeric/categorical pairs matter
    pool = categorical + [c for c in numeric if X[c].nunique() <= 20]

    def cramers_v(a, b):
        ct = pd.crosstab(X[a], X[b])
        return np.sqrt(chi2_contingency(ct, correction=False)[0] / (ct.to_numpy().sum() * (min(ct.shape) - 1)))
    cat = [("cramers_v", a, b, cramers_v(a, b)) for a, b in combinations(pool, 2)]
    top = lambda rows: sorted(rows, key=lambda t: -t[3])[:5]
    return pd.DataFrame(top(num) + top(cat), columns=["kind", "feature_a", "feature_b", "strength"])


if __name__ == "__main__":
    # (a) synthetic dependence
    Xd, yd, w, b = make_synthetic(dependent=True)
    Xi, _, _, _ = make_synthetic(dependent=False)
    assert 0.75 <= Xd.x1.corr(Xd.x2) <= 0.85 and abs(Xi.x1.corr(Xi.x2)) < 0.05
    assert set(np.unique(yd)) == {0, 1} and yd.dtype.kind == "i"
    # (b) analytic linear predictor
    assert np.allclose(linear_predictor(w, b)(Xd), Xd.to_numpy() @ w + b)
    # (c) published Adult files
    Xa, ya, Xat, yat = load_adult()
    assert Xa.shape == (32561, 14) and Xat.shape == (16281, 14)
    assert abs(ya.mean() - 0.24) < 0.01 and abs(yat.mean() - 0.24) < 0.01, (ya.mean(), yat.mean())
    print(f"adult y mean train {ya.mean():.4f} test {yat.mean():.4f}; missing cells train {Xa.isna().sum().sum()}")
    # (d) manifest splits, (e) preprocessor fit on train only
    for name, sizes, n_feat in [("synthetic_dep", (7000, 1500, 1500), (10, 10)),
                                ("synthetic_indep", (7000, 1500, 1500), (10, 10)),
                                ("adult", (26048, 6513, 16281), (100, 120))]:
        ds = load_dataset(name)
        assert (len(ds.X_train), len(ds.X_dev), len(ds.X_test)) == sizes == (len(ds.y_train), len(ds.y_dev), len(ds.y_test))
        assert len(ds.explain_idx) == len(set(ds.explain_idx)) == 100 and ds.explain_idx.max() < len(ds.X_test)
        m = json.load(open("manifests/splits.json"))[name]
        assert not set(m["train_idx"]) & set(m["dev_idx"])
        assert ds.X_train.equals(load_dataset(name).X_train)  # deterministic
        pre = build_preprocessor(ds.numeric, ds.categorical).fit(ds.X_train)
        Z = pre.transform(ds.X_test)
        assert isinstance(Z, np.ndarray) and Z.dtype == np.float64 and not np.isnan(Z).any()
        assert n_feat[0] <= len(pre.get_feature_names_out()) == Z.shape[1] <= n_feat[1]
        print(f"{name}: train/dev/test {sizes}, Z dim {Z.shape[1]}, y_train mean {ds.y_train.mean():.3f}")
    # models + dependency tables
    fit_models(load_dataset("synthetic_dep"))
    fit_models(load_dataset("adult"))
    for name in ["adult", "synthetic_dep"]:
        ds = load_dataset(name)
        print(f"\ndependency_report({name} train)\n" + dependency_report(ds.X_train, ds.numeric, ds.categorical).round(3).to_string())
    print("\ndata.py self-check OK")
