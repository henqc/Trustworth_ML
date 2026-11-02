# Figures

Regenerate all of them with `.venv/bin/python scripts/make_figures.py` from the repo root. Aggregation everywhere: average over seeds within a case, then median (bars, markers) and IQR (whiskers) over cases.

- `fig_fidelity_by_sampler.png`: median held-out fidelity per sampler and query budget (n = 200 lighter, n = 500 solid) in four panels (synthetic dependent LR and RF, Adult RF, synthetic independent RF); Adult cut at −1 with the true medians labeled. From `results/pilot.csv`.
- `fig_validity.png`: Adult RF, n = 500: mean distance from samples to the nearest training record, and share of samples whose category combination occurs in training, per sampler. From `results/pilot.csv`.
- `fig_fit_vs_heldout.png`: Adult RF, every explanation: in-sample fit R² against held-out fidelity, colored and shaped by sampler, y = x line, axes [−3, 1] with the count of points outside. From `results/pilot.csv`.
- `fig_first_start.png`: max and median coefficient error (log scale) when recovering a known linear predictor, three settings × n = 200 / 500. From `results/first_start.csv`.
- `fig_scale_sweep.png` (only once `results/w4_scale_match.csv` exists): median fidelity against mean sample-to-query distance across noise scales, default kernel width, one line per sampler. From `results/w4_scale_match.csv`.
- `fig_width_sweep.png` (only once `results/w4_scale_match.csv` exists): median fidelity per sampler under each kernel-width rule. From `results/w4_scale_match.csv`.

Not plotted: rank stability, because the coefficient vectors it needs are not stored in any CSV.
