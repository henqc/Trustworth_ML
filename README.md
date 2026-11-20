# Trustworth_ML

## How to run (from the repo root)
1. `python3 -m venv .venv && source .venv/bin/activate`
2. `pip install -r requirements.txt`
3. Download the three Adult files into `data/adult/`. The folder URL itself returns "Not Found" because UCI serves no directory listing, so fetch the files by name:
   ```bash
   mkdir -p data/adult && for f in adult.data adult.test adult.names; do curl -fL -o "data/adult/$f" "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/$f"; done
   ```
   Dataset page: https://archive.ics.uci.edu/dataset/2/adult. `load_dataset("adult")` compares the files' SHA-256 with `manifests/splits.json` and refuses files that do not match.
4. `python src/manifest.py` (only once, before any training; it overwrites `manifests/splits.json`, so skip it if the manifest exists)
5. `python src/data.py` (data/split/model self-check)
6. `python src/explain.py` (sampler/surrogate self-check)
7. `python src/first_start.py` (recover the known linear predictor, then the pilot: writes `results/first_start.csv`, `results/pilot.csv`, `results/pilot_summary.md`)

## Small demonstration
`python src/demo.py` (about 3 s) explains one Adult test record (the first fixed explanation case) for the saved random forest, once with the dependency-aware neighborhood and once with the independent LIME-style one (n=500, seed 0). For each it prints the record's raw values, the model and surrogate predictions, the top-8 surrogate coefficients, fidelity on the 200-record eval neighborhood, fit R^2, the validity diagnostic (distance to the nearest training row, fraction of samples with a categorical combination seen in training) and the runtime. Both explanations go to `results/demo_explanation.json`.

## Saved system state
`python src/save_state.py` (about 10 s) fits the six pipelines (3 datasets x {lr, rf}, seed 0), saves each to `checkpoints/{dataset}_{model}.joblib`, reloads it and asserts the dev-set predictions match, and writes `checkpoints/state.json`: git commit, Python and package versions, hardware, precision, manifest and Adult file hashes, and per checkpoint the classifier parameters, dev accuracy, fit time, file size and feature count. The six files total 21 MB and are not tracked in git (`checkpoints/*.joblib` is ignored; `state.json` is tracked). Regenerating them takes seconds and gives the same models (identical RF trees; predictions equal up to ~1e-16, since the threaded RF averages trees in varying order) from the same manifest, data and `requirements.lock`. Load one with `joblib.load("checkpoints/adult_rf.joblib")`. `requirements.lock` (written by the same script) is the exact environment; `requirements.txt` is the loose spec.

## Compute summary
See `results/compute.md` for hardware, per-explanation timings, peak memory and the week-3 estimate. Measured since then on the same M1 Pro laptop, CPU only: the 36,000-explanation main grid took 56.7 min sequential with 384 MB peak memory (`results/week4_evidence.md`), and the 20,000-explanation leaf-size sweep took 48.7 min (`results/week5_evidence.md`).

## Reuse statement
No external explanation code is used or adapted; the samplers, the weighted ridge surrogate and the metrics are written here. LIME (Ribeiro, Singh and Guestrin, KDD 2016) and SHAP (Lundberg and Lee, NeurIPS 2017) are read as references only; SHAP may be added as a library baseline in Week 4. Libraries:
- numpy (BSD-3): arrays and the closed-form surrogate fit
- pandas (BSD-3): tabular data and result tables
- scikit-learn (BSD-3): preprocessing, the lr and rf models, nearest neighbors
- scipy (BSD-3): Spearman rank stability and the chi-square behind Cramer's V
- matplotlib (PSF-based Matplotlib license): figures
- joblib (BSD-3): checkpoint files

Data: UCI Adult (Becker and Kohavi, 1996, https://doi.org/10.24432/C5XW20), licensed CC BY 4.0. Download it as in step 3 of "How to run"; `manifests/splits.json` records the sha256 of the files used.

## Main experiment (protocol v1)
The protocol is frozen in `configs/protocol_v1.md`. Results and their reading: `results/week4_evidence.md`.
- `python src/main_grid.py` (57 min, resumable per dataset and model; `--quick` gives a 1-minute smoke run in `results/main_quick/`): every explanation and coefficient vector → `results/main/`
- `python src/analyze_grid.py` (seconds): summary by condition, paired bootstrap comparisons, held-out-case subset, lowest-fidelity cases → `results/main/`
- `python scripts/make_figures.py` (about 20 s): every figure in `results/figures/`, including the two used in the final talk (`fig_talk_fidelity.png`, `fig_talk_leaf.png`)

## Final talk
`slides/Trustworth_ML_Final_Presentation_v2.pptx`. Every number on the slides comes from a committed result file: the main grid in `results/main/`; error (RMSE), the control, ablation stability and the leaf sweep in `results/week5/`; the failure case in `results/failure_analysis/`; feature-level stability in `results/feature_groups/stability_check.csv`; the correctness check in `results/first_start.csv`. Both charts are generated by `scripts/make_figures.py` (`fig_talk_fidelity.png`, `fig_talk_leaf.png`).

## Week 5 analyses
All read the frozen main grid in `results/main/`; none reruns it. Consolidated findings: `results/week5_evidence.md`.
- `python src/week5_analysis.py` (15 s): weighted RMSE for every grid explanation, the independent-feature control, and rank stability of the isolating ablation → `results/week5/`
- `python src/feature_stability_check.py` (7 s): feature-level stability under four importance definitions with a noise null → `results/feature_groups/`
- `python src/min_samples_leaf_experiment.py [dataset]` (35 min on Adult, 14 min with `synthetic_dep`): forest leaf-size sweep, dependency-aware vs training neighbors → `results/min_samples_leaf[_dataset]/`
- `python src/isolating_ablation.py`: isolating dependency ablation on Adult RF → `results/isolating_ablation/`
- `python src/analyze_failures_fixed.py`: Adult evaluation-neighborhood variance and weighted MSE → `results/failure_analysis/`
