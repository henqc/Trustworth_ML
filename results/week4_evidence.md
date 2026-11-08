# Week 4 evidence — main experiments under the predefined protocol

Date: 2026-11-08. Protocol: `configs/protocol_v1.md`, committed (2fd8b61) before the grid ran; four dated amendments were added after an adversarial code review and before results were read. Grid: 100 fixed test cases × budgets {200, 500} × 5 sampling seeds × 6 conditions × {logistic regression, random forest} × {synthetic-dependent, synthetic-independent control, Adult} = 36,000 explanations, all completed, no non-finite metric values. Every number below regenerates from `results/main/grid.csv` via `src/analyze_grid.py` and `scripts/make_figures.py`.

Definitions. Fidelity = kernel-weighted R² of the surrogate against the black box on a fixed neighborhood of the 200 nearest dev records (identical for every condition and seed; never the fit samples). Rank stability = mean pairwise Spearman of |coef| across the 5 seeds per case, over coefficients that are nonzero in at least one seed. Aggregation: per-case mean over seeds, then statistics over the 100 cases. Paired differences are per case with percentile-bootstrap 95% CIs (2,000 resamples). Kernel width = median evaluation-neighborhood distance (week-3 decision).

## 1. The brief's core comparison: independent vs training-neighbor vs dependency-aware (n = 500)

Fidelity (median over cases) / rank stability:

| dataset, model | independent (LIME-style) | independent, scale-adjusted | training neighbors | dependency-aware |
|---|---|---|---|---|
| synthetic-dep, LR | 0.84 / 0.97 | 0.89 / 0.97 | 0.92 / 0.98 | **0.92** / 0.98 |
| synthetic-dep, RF | 0.64 / 0.96 | 0.69 / 0.95 | 0.68 / 0.94 | **0.80** / 0.96 |
| synthetic-indep, LR | 0.83 / 0.96 | 0.85 / 0.96 | 0.87 / 0.97 | **0.88** / 0.97 |
| synthetic-indep, RF | 0.73 / 0.94 | 0.74 / 0.94 | 0.77 / 0.92 | **0.85** / 0.96 |
| Adult, LR | 0.27 / 0.18 | 0.68 / 0.35 | **0.86** / **0.88** | 0.86 / 0.86 |
| Adult, RF | −0.31 / 0.16 | 0.29 / 0.45 | 0.50 / **0.80** | **0.57** / 0.75 |

Adult means are dominated by outliers (independent, RF: mean −16.3 ± 78.6), hence medians in the table; the CSVs carry mean, sd and quartiles.

Paired per-case differences, dependency-aware minus baseline, fidelity, n = 500 (mean [95% CI], wins out of 100):

| dataset, model | vs independent | vs scale-adjusted independent | vs training neighbors |
|---|---|---|---|
| synthetic-dep, LR | +0.120 [0.106, 0.134], 100 | +0.095 [0.070, 0.121], 98 | +0.004 [0.003, 0.005], 82 |
| synthetic-dep, RF | +0.164 [0.153, 0.176], 100 | +0.153 [0.130, 0.179], 100 | +0.128 [0.118, 0.138], 100 |
| synthetic-indep, LR | +0.111 [0.088, 0.136], 94 | +0.155 [0.116, 0.199], 78 | +0.013 [0.010, 0.015], 95 |
| synthetic-indep, RF | +0.145 [0.129, 0.163], 100 | +0.175 [0.140, 0.211], 98 | +0.080 [0.071, 0.091], 98 |
| Adult, LR | +14.3 [3.3, 30.7], 99 | +4.6 [1.0, 9.5], 82 | −0.035 [−0.106, 0.002], 39 |
| Adult, RF | +16.8 [5.2, 34.2], 98 | +1.6 [0.6, 3.1], 92 | +0.054 [0.042, 0.065], 87 |

Rank stability, same comparison, Adult (synthetic differences are within ±0.04; the largest is +0.040 vs neighbors on synthetic-indep RF): vs independent +0.68 (LR) and +0.58 (RF), 100/100 wins both; vs scale-adjusted +0.51 and +0.29, 100/100; vs training neighbors −0.015 [−0.028, −0.000] (LR) and −0.056 [−0.073, −0.039] (RF), i.e. training neighbors are the most stable condition on Adult.

Budget 200 gives the same ordering with slightly larger gaps vs independent (e.g. Adult RF +23.1) and lower stability for the realistic conditions (Adult RF dependency-aware 0.53 at n = 200 vs 0.75 at n = 500; the independent sampler's Adult stability is flat, 0.20 vs 0.18 LR and 0.18 vs 0.16 RF).

Confirmatory subset (cases never touched by the pilot or the kernel-width sweep: synthetic 31–100, Adult 16–100): every primary fidelity comparison at n = 500 keeps its sign and CI (a few small stability CIs shift, e.g. synthetic-indep LR vs neighbors moves from [−0.005, 0.001] to [−0.007, −0.001]), e.g. synthetic-dep RF vs independent +0.170 [0.157, 0.182] 70/70; Adult RF vs independent +18.7 [5.0, 39.6] 83/85, vs scale-adjusted +1.73 [0.61, 3.52] 78/85, vs neighbors +0.053 [0.042, 0.065] 75/85. `results/main/paired_heldout_cases.csv`.

Validity and runtime (Adult RF, n = 500): fraction of samples whose raw categorical combination occurs in training: independent 24 %, scale-adjusted 24 %, training neighbors 100 %, dependency-aware 100 %. Mean distance to the nearest training record: 2.57, 1.97, 0.00, 0.33. Runtime per explanation (sampling + model queries + fit): 37 / 37 / 39 / 48 ms; including fidelity and validity evaluation 222–233 ms. Synthetic: about 3 ms (LR) and 30 ms (RF) per explanation for every condition.

**Reading.** Against the LIME-style baseline the dependency-aware neighborhood wins on fidelity in 94–100 of 100 cases on every dataset and model, and on Adult it lifts rank stability from about 0.2 to 0.75–0.86. The gain survives the scale-adjusted baseline. Against training neighbors, the strongest baseline, the picture is mixed: dependency-aware is better on fidelity under the random forest (+0.13 synthetic, +0.05 Adult, 87–100 wins), gains little under logistic regression on synthetic (+0.004, +0.013) and is inconclusive on Adult LR (−0.035 [−0.106, 0.002]), while training neighbors are more stable on Adult.

## 2. Collected for week 5 (not analysed here)

- Ablation, no dependency constraints (also changes noise scale, see protocol amendment 2): gap to dependency-aware in fidelity is +0.016 [0.013, 0.019] on synthetic-dep RF, −0.002 on synthetic-indep RF, and +5.2 [1.5, 11.0] with +0.46 stability on Adult RF (+34 / +0.50 on Adult LR).
- Ablation, no locality weighting: fidelity |gap| ≤ 0.005 and stability |gap| ≤ 0.006 everywhere, although the median-width kernel does give non-uniform weights (dependency-aware mean weight 0.48–0.50).
- Independent-feature control: dependency-aware beats independent by +0.145 [0.129, 0.163] (RF) and +0.111 (LR) with no dependencies to preserve, and the no-dependency ablation matches it there. Mechanism to analyse in week 5: on synthetic data the gain comes from anchoring samples on real local training records rather than from dependency preservation; on Adult, dependency preservation appears to matter, but this stays a hypothesis until the isolating ablation runs, because the current ablation also changes the noise scale.
- Representative failures (`results/main/failures.csv`): the five lowest-fidelity dependency-aware cases on Adult all have black-box predictions within 0.05 of 0 (e.g. test row 4076: LR fidelity −6.1 with in-sample fit 0.99), consistent with a near-constant black box over the evaluation neighborhood making the weighted-R² denominator tiny (to be verified in week 5 by measuring that variance directly). Independent-sampler failures are the heavy negative tail behind the −16 means.

## 3. Compute (measured)

36,000 explanations in 56.7 min wall clock on the M1 Pro (8 cores, 16 GB), peak RSS 384 MB; analysis and figures take well under a minute each when run interactively (not instrumented); `results/main/` is 28.7 MB (36,000 rows and six coefficient tensors). The week-3 pilot-based estimate was 55.6 min and the 3-case smoke run projected 56 min. Compute tier C0, no GPU.

## 4. Progress vs target, blockers, changes

Target met: main experiments ran once under the frozen protocol with repetitions, paired uncertainty and results by condition. No blockers. Declared changes: (a) the kernel-width rule and matched scales were tuned on cases inside the 100-case sets, so the untouched-case subset is reported alongside; (b) the no-dependency ablation also changes noise scale and is labelled a dependency-plus-scale ablation, with an isolating version scheduled; (c) failures listed per budget; (d) completeness checks added to the analysis. Known limitation: random-forest predictions are reproducible only to ~1e-16 across runs.

## 5. Week-5 plan

1. Isolating ablation: keep the local diagonal variance, remove only correlations and the categorical block; rerun on RF only.
2. Failure analysis: saturated-prediction cases (tiny eval-neighborhood variance); report fidelity also as weighted MSE or restrict to cases with sufficient eval variance, and say which.
3. Dependency-aware vs training neighbors: fidelity vs stability trade-off; test the forest-memorization hypothesis by varying `min_samples_leaf`.
4. Feature-group stability for Adult (sum one-hot coefficients within the dependency groups found in week 1), the brief's extension.
5. Optional: TreeSHAP stability column.

Figures: `fig_main_fidelity.png`, `fig_main_stability.png`, `fig_main_paired.png`, `fig_main_paired_stability.png`, `fig_main_validity.png` in `results/figures/`.
