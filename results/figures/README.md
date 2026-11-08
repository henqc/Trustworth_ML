# Figures

Regenerate all of them with `.venv/bin/python scripts/make_figures.py` from the repo root. Aggregation everywhere: average over seeds within a case, then median (bars, markers) and IQR (whiskers) over cases.

- `fig_fidelity_by_sampler.png`: median held-out fidelity per sampler and query budget (n = 200 lighter, n = 500 solid) in four panels (synthetic dependent LR and RF, Adult RF, synthetic independent RF); Adult cut at −1 with the true medians labeled. From `results/pilot.csv`.
- `fig_validity.png`: Adult RF, n = 500: mean distance from samples to the nearest training record, and share of samples whose category combination occurs in training, per sampler. From `results/pilot.csv`.
- `fig_fit_vs_heldout.png`: Adult RF, every explanation: in-sample fit R² against held-out fidelity, colored and shaped by sampler, y = x line, axes [−3, 1] with the count of points outside. From `results/pilot.csv`.
- `fig_first_start.png`: max and median coefficient error (log scale) when recovering a known linear predictor, three settings × n = 200 / 500. From `results/first_start.csv`.
- `fig_scale_sweep.png` (only once `results/w4_scale_match.csv` exists): median fidelity against mean sample-to-query distance across noise scales, default kernel width, one line per sampler. From `results/w4_scale_match.csv`.
- `fig_width_sweep.png` (only once `results/w4_scale_match.csv` exists): median fidelity per sampler under each kernel-width rule. From `results/w4_scale_match.csv`.

Main grid (protocol v1; each figure is skipped with a printed note until `src/analyze_grid.py` has written its CSV). Rows = synthetic dependent, synthetic independent, Adult; columns = linear model, random forest; six conditions, the distance-matched Independent baseline in Independent's blue, two steps darker.

- `fig_main_fidelity.png`: median held-out fidelity per condition and budget (n = 200 lighter, n = 500 solid), IQR whiskers; Adult cut at −1 with the true medians labeled. From `results/main/summary.csv`.
- `fig_main_stability.png`: rank stability (mean pairwise Spearman of |coef| across the 5 seeds) per condition and budget, mean over cases with ± 1 sd whiskers, y in [0, 1]. From `results/main/summary.csv`.
- `fig_main_paired.png`: forest plot of the per-case paired fidelity difference, dependency-aware minus each baseline and ablation (mean, 95% bootstrap CI; n = 200 lighter above n = 500), x cut at ±1.5 with arrows and the true mean labeled; right margin: cases where dependency-aware is higher at n = 500. From `results/main/paired.csv`.
- `fig_main_paired_stability.png`: the same forest plot for rank stability, x in [−1, 1]. From `results/main/paired.csv`.
- `fig_main_validity.png`: synthetic dependent RF and Adult RF, n = 500: mean distance to the nearest training record and share of samples whose category combination occurs in training, per condition (means over cases and seeds). From `results/main/summary.csv`.

The pilot figures above do not plot rank stability: the pilot stored no coefficient vectors. `fig_main_stability.png` and `fig_main_paired_stability.png` cover it for the main grid.
