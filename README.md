# Trustworth_ML

## How to run (from the repo root)
1. `python3 -m venv .venv && source .venv/bin/activate`
2. `pip install -r requirements.txt`
3. Download `adult.data`, `adult.test`, `adult.names` from https://archive.ics.uci.edu/ml/machine-learning-databases/adult/ into `data/adult/`
4. `python src/manifest.py` (only once, before any training; it overwrites `manifests/splits.json`, so skip it if the manifest exists)
5. `python src/data.py` (data/split/model self-check)
6. `python src/explain.py` (sampler/surrogate self-check)
7. `python src/first_start.py` (recover the known linear predictor, then the pilot: writes `results/first_start.csv`, `results/pilot.csv`, `results/pilot_summary.md`)

## Small demonstration
`python src/demo.py` (about 3 s) explains one Adult test record (the first fixed explanation case) for the saved random forest, once with the dependency-aware neighborhood and once with the independent LIME-style one (n=500, seed 0). For each it prints the record's raw values, the model and surrogate predictions, the top-8 surrogate coefficients, fidelity on the 200-record eval neighborhood, fit R^2, the validity diagnostic (distance to the nearest training row, fraction of samples with a categorical combination seen in training) and the runtime. Both explanations go to `results/demo_explanation.json`.

## Saved system state
`python src/save_state.py` (about 10 s) fits the six pipelines (3 datasets x {lr, rf}, seed 0), saves each to `checkpoints/{dataset}_{model}.joblib`, reloads it and asserts the dev-set predictions match, and writes `checkpoints/state.json`: git commit, Python and package versions, hardware, precision, manifest and Adult file hashes, and per checkpoint the classifier parameters, dev accuracy, fit time, file size and feature count. The six files total 21 MB and are not tracked in git (`checkpoints/*.joblib` is ignored; `state.json` is tracked). Regenerating them takes seconds and gives the same models (identical RF trees; predictions equal up to ~1e-16, since the threaded RF averages trees in varying order) from the same manifest, data and `requirements.lock`. Load one with `joblib.load("checkpoints/adult_rf.joblib")`. `requirements.lock` (written by the same script) is the exact environment; `requirements.txt` is the loose spec.

## Compute summary
See `results/compute.md`: hardware, measured fit and per-explanation timings, peak memory (under 0.5 GB), disk, and the revised Week 4 estimate. The headline: about 60 min sequential on an M1 Pro laptop for the full 30,000-explanation grid plus the scale and kernel-width sweeps (2 h at most with the optional SHAP baseline, 4 h with 2x headroom). No GPU is used.

## Reuse statement
No external explanation code is used or adapted; the samplers, the weighted ridge surrogate and the metrics are written here. LIME (Ribeiro, Singh and Guestrin, KDD 2016) and SHAP (Lundberg and Lee, NeurIPS 2017) are read as references only; SHAP may be added as a library baseline in Week 4. Libraries:
- numpy (BSD-3): arrays and the closed-form surrogate fit
- pandas (BSD-3): tabular data and result tables
- scikit-learn (BSD-3): preprocessing, the lr and rf models, nearest neighbors
- scipy (BSD-3): Spearman rank stability and the chi-square behind Cramer's V
- matplotlib (PSF-based Matplotlib license): figures
- joblib (BSD-3): checkpoint files

Data: UCI Adult (Becker and Kohavi, 1996, https://doi.org/10.24432/C5XW20), licensed CC BY 4.0. Download it as in step 3 of "How to run"; `manifests/splits.json` records the sha256 of the files used.
