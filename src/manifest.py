import json
from datetime import datetime
from pathlib import Path

import numpy as np
from sklearn.model_selection import train_test_split

from data import load_adult, sha256


def build_manifest(seed=0):
    # no model is fit here: the split manifest exists before any training
    rng = np.random.default_rng(seed)
    m = {"created": datetime.now().isoformat(timespec="seconds"), "seed": seed}
    n = 10000
    for name, dep in [("synthetic_dep", True), ("synthetic_indep", False)]:
        perm = rng.permutation(n)
        tr, dv, te = (sorted(map(int, p)) for p in np.split(perm, [int(0.7 * n), int(0.85 * n)]))  # 70/15/15
        m[name] = {"n": n, "gen_seed": 0, "dependent": dep, "train_idx": tr, "dev_idx": dv, "test_idx": te,
                   "explain_idx": sorted(map(int, rng.choice(len(te), 100, replace=False)))}  # positions in test_idx
    _, y, X_test, _ = load_adult()
    tr, dv = train_test_split(np.arange(len(y)), test_size=0.2, stratify=y, random_state=seed)
    m["adult"] = {"source": "UCI Adult published adult.data / adult.test",
                  "sha256": {f: sha256(Path("data/adult") / f) for f in ["adult.data", "adult.test"]},
                  "train_idx": sorted(map(int, tr)), "dev_idx": sorted(map(int, dv)),
                  "test": f"published adult.test ({len(X_test)} rows)",
                  "explain_idx": sorted(map(int, rng.choice(len(X_test), 100, replace=False)))}
    return m


if __name__ == "__main__":
    m = build_manifest()
    assert len(m["adult"]["train_idx"]) == 26048 and len(m["adult"]["dev_idx"]) == 6513
    assert len(m["synthetic_dep"]["test_idx"]) == 1500 and len(m["synthetic_dep"]["explain_idx"]) == 100
    json.dump(m, open("manifests/splits.json", "w"), indent=1)
