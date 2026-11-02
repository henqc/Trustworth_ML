"""Saved system state: fit every (dataset, model) pipeline, joblib it to checkpoints/, check the restored checkpoint
reproduces dev predictions, and record environment + hardware + per-checkpoint metadata in checkpoints/state.json."""
import hashlib
import json
import os
import platform
import resource
import subprocess
import sys
import time
from datetime import datetime
from importlib.metadata import version
from pathlib import Path

import joblib
import numpy as np

from data import fit_models, load_dataset

sh = lambda *cmd: subprocess.run(cmd, capture_output=True, text=True, check=True).stdout.strip()
out = Path("checkpoints")
out.mkdir(exist_ok=True)
manifest = json.load(open("manifests/splits.json"))
ckpts = []
for name in ["synthetic_dep", "synthetic_indep", "adult"]:
    ds, t = load_dataset(name), time.perf_counter()
    models = fit_models(ds)
    fit_s = time.perf_counter() - t  # both models of this dataset together
    for model, m in models.items():
        path = out / f"{name}_{model}.joblib"
        joblib.dump(m, path, compress=3)
        # restored-checkpoint check: the reloaded pipeline reproduces the original's dev predictions
        assert np.allclose(joblib.load(path).predict_proba(ds.X_dev), m.predict_proba(ds.X_dev)), path
        ckpts.append({"dataset": name, "model": model, "file": str(path), "clf_params": m[-1].get_params(),
                      "dev_acc": m.score(ds.X_dev, ds.y_dev), "fit_s_both_models": fit_s, "size_bytes": path.stat().st_size,
                      "n_z_features": len(m[:-1].get_feature_names_out())})

state = {
    "created": datetime.now().isoformat(timespec="seconds"), "git_commit": sh("git", "rev-parse", "HEAD"),
    "git_dirty": sh("git", "status", "--porcelain") != "",  # true when the tree had uncommitted changes
    "python": sys.version.split()[0],
    "packages": {p: version(p) for p in ["numpy", "pandas", "scikit-learn", "scipy", "joblib"]},
    "platform": {"platform": platform.platform(), "machine": platform.machine(), "cpu": sh("sysctl", "-n", "machdep.cpu.brand_string"),
                 "cpu_count": os.cpu_count(), "ram_gb": int(sh("sysctl", "-n", "hw.memsize")) / 2**30},
    "precision": "float64 on CPU",
    "manifest_sha256": hashlib.sha256(Path("manifests/splits.json").read_bytes()).hexdigest(),
    "adult_sha256": manifest["adult"]["sha256"],
    "checkpoints": ckpts,
    "peak_rss_mb": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**20,  # bytes on macOS (KiB on Linux)
}
json.dump(state, open(out / "state.json", "w"), indent=1, default=str)
Path("requirements.lock").write_text(sh(sys.executable, "-m", "pip", "freeze") + "\n")
for c in ckpts:
    print(f"{c['file']:<38}{c['size_bytes'] / 2**10:8.0f} KB  dev acc {c['dev_acc']:.4f}  fit(both) {c['fit_s_both_models']:.2f}s  Z dim {c['n_z_features']}")
print(f"total {sum(c['size_bytes'] for c in ckpts) / 2**20:.2f} MB; peak RSS {state['peak_rss_mb']:.0f} MB; restored checkpoints OK")
