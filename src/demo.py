"""Small demonstration: explain one Adult test record with the dependency-aware and the independent (LIME-style)
neighborhood using the saved RF checkpoint; prints both explanations and writes results/demo_explanation.json."""
import json
from pathlib import Path

import joblib
import numpy as np

from data import fit_models, load_dataset
from explain import Explainer, default_eval_neighborhood, sample_dependency_aware, sample_independent

ds = load_dataset("adult")
ck = Path("checkpoints/adult_rf.joblib")
m = joblib.load(ck) if ck.exists() else fit_models(ds)["rf"]
pre = m[:-1]
x = ds.X_test.iloc[[ds.explain_idx[0]]]
E = Explainer(lambda X: m.predict_proba(X)[:, 1], pre.transform, ds.X_train, ds.numeric, ds.categorical,
              pre.get_feature_names_out())
ev = default_eval_neighborhood(pre.transform(x)[0], pre.transform(ds.X_dev), ds.X_dev, k=200)
record = x.iloc[0].to_dict()
print(f"checkpoint: {ck if ck.exists() else 'refit (no checkpoint)'}; test row {ds.explain_idx[0]}:")
print("  " + ", ".join(f"{k}={v}" for k, v in record.items()))
out = {"test_row": int(ds.explain_idx[0]), "record": record}
for name, sampler in [("dep_aware", sample_dependency_aware), ("independent", sample_independent)]:
    r = E.explain(x, sampler, 500, 0, ev)
    coef = dict(zip(r["feature_names"], np.asarray(r["coef"]).tolist()))
    print(f"\n[{name}, n=500, seed 0] model {r['prediction']:.4f}  surrogate {r['surrogate_prediction']:.4f}  "
          f"fidelity {r['fidelity']:.3f}  fit_r2 {r['fit_r2']:.3f}  runtime {r['runtime_s'] * 1e3:.1f} ms")
    print(f"  validity {r['validity']}")
    for f, c in sorted(coef.items(), key=lambda kv: -abs(kv[1]))[:8]:
        print(f"  {f:<44}{c:+.4f}")
    out[name] = {"coef": coef, **{k: v for k, v in r.items() if np.isscalar(v) or isinstance(v, dict)}}
json.dump(out, open("results/demo_explanation.json", "w"), indent=1, default=float)
print("\nwrote results/demo_explanation.json")
