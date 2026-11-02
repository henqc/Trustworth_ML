# Measured compute summary

Sources: `checkpoints/state.json` (written by `src/save_state.py`), `results/pilot.csv` (3,750 timed explanations), `du -sh`.

## Hardware and software
| item | value |
|---|---|
| machine | Apple M1 Pro (arm64), 8 cores, 16 GB RAM, no GPU used |
| OS | macOS 26.6.2 |
| Python / packages | 3.14.0; numpy 2.5.4, pandas 3.0.6, scikit-learn 1.9.1, scipy 1.18.1, joblib 1.6.0 (exact list: `requirements.lock`) |
| precision | float64 on CPU |
| batch size | one explanation at a time; each queries the model on its n = 200 or 500 samples in one call |
| parallelism | sequential explanations; only the RF uses all cores (`n_jobs=-1`) in fit and predict |

## Measured timings
Model fit (seconds, as printed by `fit_models`; all six together under 2 s):

| dataset | lr | rf |
|---|---|---|
| synthetic_dep | 0.01 | 0.42 |
| synthetic_indep | 0.01 | 0.41 |
| adult | 0.25 | 0.70 |

Per explanation, means over the pilot (ms). `runtime` = sampling + model queries + surrogate fit; `wall` = runtime + fidelity on the 200-record eval neighborhood + the validity diagnostic.

| dataset / model | explanations | runtime ms | wall ms | wall ms at n=500 |
|---|---|---|---|---|
| synthetic_dep / lr | 1,500 | 3.3 | 13.6 | 16.2 |
| synthetic_dep / rf | 1,500 | 31.0 | 89.7 | 94.1 |
| synthetic_indep / rf | 300 | 32.1 | 101.5 | 101.5 |
| adult / rf | 450 | 43.3 | 230.1 | 236.0 |

Timings are from the 2026-11-01 re-run of the pilot on an otherwise idle machine; an earlier run with other jobs in parallel was 20-30% slower (full grid 70.7 min), so treat the estimates below as idle-machine numbers.

Peak memory (max RSS): 424 MB for `save_state.py` (three datasets, six fits, dump + reload); 402 MB for `demo.py`.

Disk: data/ 5.7 MB, results/ 1.1 MB (incl. figures), checkpoints/ 22 MB on disk (six pipelines, 20.7 MB, + state.json); environment .venv/ 350 MB (not an artifact).

## Revised estimate (measured time per run x planned runs + evaluation overhead)
Week 4 full grid = 100 cases x 2 budgets x 5 seeds x 5 sampler configs = 5,000 explanations per (dataset, model), 30,000 total; minutes = wall mean x 5,000. synthetic_indep uses synthetic_dep timings (its measured rf wall is within 6%); adult lr uses adult rf timing (upper bound). Sweeps use the n=500 wall means, both models, 3 seeds.

| block | explanations | minutes |
|---|---|---|
| grid synthetic_dep lr / rf | 5,000 / 5,000 | 1.1 / 7.5 |
| grid synthetic_indep lr / rf | 5,000 / 5,000 | 1.1 / 7.5 |
| grid adult lr / rf | 5,000 / 5,000 | 19.2 / 19.2 |
| **full grid subtotal** | **30,000** | **55.6** |
| scale sweep as run (RF only): synthetic_dep 30 cases + adult 15 cases, 9 sampler-scale configs, 3 seeds, n=500 | 1,215 | 2.9 |
| kernel-width sweep as run (RF only): same cases, 4 configs, 3 seeds, n=500 | 540 | 1.3 |
| evaluation overhead: model fits, one eval neighborhood per case, aggregation, figures | - | < 1 |
| **total, no SHAP** | **31,755** | **60** (1.0 h) |
| optional SHAP (rough): TreeSHAP on RF, 3 x 100 cases at ~1-2 s | 300 | 5-10 |
| optional SHAP (rough): KernelSHAP on LR, 3 x 100 cases at ~5-10 s | 300 | 25-50 |
| **total with SHAP** | | **90-120** (1.5-2.0 h) |
| **with 2x headroom** | | **120 no SHAP; 180-240 with SHAP** (at most 4 h) |

Check on the per-run numbers: the pilot's 3,750 explanations took 5.0 min wall clock (script total 303 s; sum of wall_s = 4.8 min), and the scale + width sweep (1,755 explanations) took 4.8 min (286 s), both consistent with the table.
SHAP figures are guesses, not measurements; `shap` is not installed and would be the only new dependency.
Everything fits a laptop (compute tier C0): at most 0.5 GB RAM, under 30 MB of artifacts, no GPU used.
