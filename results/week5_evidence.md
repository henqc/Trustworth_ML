# Week 5 evidence — ablations, repetitions, uncertainty, failure analysis

Date: 2026-11-15. Suggested Week-5 target: ablations, repetitions, uncertainty estimates and failure analysis (course table); analyze independent-feature controls and failures (project brief). All main-grid numbers come from the frozen week-4 grid (`results/main/`, protocol `configs/protocol_v1.md`, 100 cases × budgets 200/500 × 5 seeds); nothing in that grid was rerun. New this week: Nadia's isolating ablation, Adult failure diagnostics and feature-group stability; the whole-grid absolute-error analysis, the control analysis, the feature-stability artifact check and the min_samples_leaf sweep (her script, run here on Adult and, with an added dataset argument, on correlated synthetic). Conventions unchanged: per-case mean over seeds first, then statistics over the 100 cases; paired percentile-bootstrap 95% CIs (2,000 resamples).

## 1. Ablations

**1a. Isolating dependency ablation** (`results/isolating_ablation/`, `src/isolating_ablation.py`; Adult, random forest). Same anchors, same local per-feature noise variance, same scale, width, budgets and seeds as the dependency-aware sampler; only the categorical block (each categorical redrawn from its marginal) and the noise correlations are removed. This answers protocol amendment 2, where the week-4 ablation also changed the noise scale.

| budget | fidelity, dependency-aware − isolating ablation | wins | rank stability, same difference | wins |
|---|---|---|---|---|
| 200 | +2.11 [0.82, 4.04] | 90/100 | +0.130 [0.100, 0.162] (0.54 vs 0.41) | 78/100 |
| 500 | +1.77 [0.74, 3.28] | 86/100 | +0.323 [0.298, 0.347] (0.75 vs 0.43) | 100/100 |

Median fidelity 0.57 vs 0.45 at n = 500; samples with a categorical combination seen in training 100 % vs 24 %. Caveats: it keeps each anchor's numeric values together, so it is a categorical-block ablation (Adult's numeric correlations are weak, at most 0.14); it was run in a different software environment, so it is compared only within its own run (its dependency-aware rows agree with the main grid in aggregate, 0.538 vs 0.537 mean, but not row by row).

**1b. Main-grid ablations** (week 4, `results/main/paired.csv`). No dependency constraints (dependency + scale): fidelity gap to dependency-aware +0.016 to +0.026 on correlated synthetic at n = 500, about 0 on the independent control, +5.2 (RF) and +34 (LR) on Adult with +0.46 / +0.50 rank stability. No locality weighting: fidelity |gap| ≤ 0.005 everywhere, and in three of the four synthetic dataset/model cells the unweighted surrogate has slightly lower absolute error (RMSE difference 0.0006 to 0.0010, CIs exclude 0). Locality weighting therefore contributes nothing measurable under this protocol; the neighborhood itself does the localizing.

## 2. Independent-feature control (does the sampler add bias when there is nothing to preserve?)

`results/week5/analysis.md`, Part B. Fidelity differences at n = 500 (LR / RF):

| comparison | correlated synthetic | independent-feature control |
|---|---|---|
| dependency-aware − independent | +0.120 / +0.164 | +0.111 / +0.145 |
| dependency-aware − training neighbors | +0.004 / +0.128 | +0.013 / +0.080 |
| dependency-aware − no-dependency ablation | +0.026 / +0.016 | −0.004 / −0.002 |

- No bias: on the control the dependency-aware sampler beats independent sampling in every cell (lowest CI bound +0.088, 94–100 of 100 wins), with lower RMSE (0.030 to 0.040) and slightly higher stability. No cell is significantly worse.
- The dependency-specific part exists only where there is a dependency: present in 4 of 4 cells on correlated synthetic (10–23 % of the gain over independent), absent on the control.
- So 77–90 % of the synthetic gain comes from anchoring samples on real local training records rather than from preserving the correlation (ratio of mean differences; the ablation also changes noise scale).

## 3. Failure analysis

**3a. Absolute error for the whole grid** (`src/week5_analysis.py`, `results/week5/`). Weighted R² explodes when the black box is nearly constant on the evaluation neighborhood, so every explanation's weighted RMSE was recovered as sqrt((1 − R²) × weighted prediction variance), with the 600 evaluation neighborhoods rebuilt and verified against the grid (kernel width equal to 4e-16 for every case). This generalizes Nadia's Adult diagnostic (`results/failure_analysis/`), which it reproduces (LR variance equal to 6 significant figures).

Mean weighted RMSE, n = 500 (fidelity median in parentheses):

| condition | Adult, RF | correlated synthetic, RF |
|---|---|---|
| independent (LIME-style) | 0.144 (−0.31) | 0.138 (0.64) |
| independent, scale-adjusted | 0.105 (0.29) | 0.134 (0.69) |
| training neighbors | 0.083 (0.50) | 0.131 (0.68) |
| dependency-aware | **0.078** (0.57) | **0.103** (0.80) |
| ablation: no dependency constraints | 0.102 (0.39) | 0.107 (0.78) |

Paired RMSE differences at n = 500, baseline − dependency-aware (positive = dependency-aware has lower error), with wins out of 100:

| dataset, model | vs independent | vs scale-adjusted | vs training neighbors |
|---|---|---|---|
| synthetic-dep, LR | +0.043 [0.040, 0.046], 100 | +0.029 [0.024, 0.035], 98 | +0.002 [0.001, 0.002], 82 |
| synthetic-dep, RF | +0.036 [0.034, 0.037], 100 | +0.031 [0.028, 0.034], 100 | +0.028 [0.027, 0.030], 100 |
| synthetic-indep, LR | +0.030 [0.025, 0.035], 94 | +0.034 [0.026, 0.042], 78 | +0.005 [0.004, 0.006], 95 |
| synthetic-indep, RF | +0.040 [0.036, 0.043], 100 | +0.039 [0.033, 0.045], 98 | +0.024 [0.022, 0.027], 98 |
| Adult, LR | +0.049 [0.045, 0.053], 98 | +0.022 [0.017, 0.027], 82 | −0.0005 [−0.0010, −0.0001], 39 |
| Adult, RF | +0.066 [0.060, 0.072], 98 | +0.027 [0.021, 0.034], 92 | +0.006 [0.004, 0.007], 87 |

On absolute error the Adult gap between independent and dependency-aware sampling is about 2× (0.144 vs 0.078), not the −16 mean R² the week-4 table suggested; the ordering of conditions is unchanged. One comparison sharpens: on Adult LR, training neighbors have significantly, though negligibly, lower error than dependency-aware (0.0005), where fidelity was inconclusive.

**3b. How much of the negative-R² tail is a small-denominator effect?** Adult, n = 500: per-case fidelity correlates with log prediction variance at ρ = +0.97 for the independent sampler and +0.64 for dependency-aware. Negative-fidelity cases: independent 41 (LR) and 58 (RF) of 100, of which only 10 sit in the bottom variance decile; dependency-aware 3 and 4. Restricting to cases above the 10th variance percentile (a sensitivity analysis, not an exclusion rule) moves the RF medians from −0.31 to −0.08 (independent) and from 0.57 to 0.60 (dependency-aware). The tiny denominator inflates the size of the worst values, but most independent-sampler failures are genuine: the surrogate is worse than predicting the neighborhood mean.

**3c. The dependency-aware sampler's own failures** (Nadia's per-seed diagnostics). Two kinds. Saturated predictions: test row 4076 (P ≈ 0.002, variance at the 3rd percentile) has R² of −13.7 with an RMSE of only 0.017. Genuine misses: row 8091 (both models) and row 3584 (LR) sit at the 29th–37th variance percentile with R² ≈ −0.1 and RMSE 0.08–0.12, i.e. the local linear surrogate is no better than a constant there. Synthetic failures are mild: the lowest per-case fidelity is between 0.41 and 0.76 across the four synthetic dataset/model pairs, the worst of them at saturated predictions.

## 4. Stability at the feature level (the brief's extension) and an artifact check

Nadia's analysis (`src/feature_group_analysis_patch/`) sums |coefficients| over the one-hot columns of each original feature and ranks the 14 features. Under that definition the independent sampler looks as stable as or more stable than dependency-aware (Adult RF, n = 500: 0.956 vs 0.923), reversing the coefficient-level result (0.16 vs 0.75). The check in `src/feature_stability_check.py` (`results/feature_groups/stability_check.md`) reproduces her numbers to 1e-6 and shows the metric is dominated by a cardinality floor: coefficients replaced by noise with no signal shared across seeds still score 0.87–0.91, because a feature with 41 levels gets a large sum regardless of signal (native-country has mean rank 1.0 under independent sampling).

Stability observed / noise null, Adult, n = 500:

| definition | independent, RF | dependency-aware, RF | training neighbors, RF | independent, LR | dependency-aware, LR |
|---|---|---|---|---|---|
| coefficient level (protocol metric) | 0.16 / 0.43 | 0.75 / 0.47 | 0.80 / 0.49 | 0.18 / 0.44 | 0.86 / 0.52 |
| feature level, sum of \|coef\| | 0.96 / 0.89 | 0.92 / 0.89 | 0.93 / 0.88 | 0.96 / 0.89 | 0.96 / 0.90 |
| feature level, mean \|coef\| | 0.77 / 0.80 | 0.92 / 0.76 | 0.92 / 0.77 | 0.79 / 0.80 | 0.96 / 0.78 |
| feature level, normalized L2 | 0.84 / 0.83 | 0.91 / 0.77 | 0.92 / 0.76 | 0.83 / 0.83 | 0.96 / 0.80 |
| query level (the record's own category) | 0.64 / 0.32 | 0.87 / 0.60 | 0.89 / 0.62 | 0.67 / 0.35 | 0.93 / 0.64 |

Under every cardinality-robust definition the dependency-aware sampler is more stable than independent sampling for both models and both budgets, with a smaller gap than at coefficient level (RF: 0.58 at coefficient level, 0.07–0.23 at feature level), and the independent sampler sits at its noise null under the normalized definitions. Training neighbors match dependency-aware within 0.02. The sum-of-|coef| numbers should not be cited as evidence that independent sampling is stable. Remaining uncertainty: the Gaussian null is a rough scale rather than a strict floor, the size of the gap depends on the definition, and there are only 5 seeds per case. Known sensitivity of the protocol metric: treating |coef| < 1e-8 as zero lowers Adult RF stability slightly (training neighbors 0.803 → 0.783, dependency-aware 0.747 → 0.734).

## 5. Does the forest's memorization explain the training-neighbor baseline? (`src/min_samples_leaf_experiment.py`)

Week 4 left a puzzle: training neighbors, which are real records, lost to the dependency-aware sampler under the random forest but tied under logistic regression. Hypothesis: a forest with tiny leaves partly memorizes its training rows, so a surrogate fit on real training rows learns a memorized surface that does not transfer to held-out neighbors. Test: refit the forest with `min_samples_leaf` in {1, 2, 5, 10, 20} (2 is the protocol setting), everything else as in protocol v1 (100 cases, budgets 200/500, 5 seeds, same evaluation neighborhoods and width rule); 10,000 explanations per dataset. Outputs: `results/min_samples_leaf/` (Adult) and `results/min_samples_leaf_synthetic_dep/`.

Mean fidelity at n = 500, and the paired difference dependency-aware − training neighbors with 95% CI and wins out of 100:

| min_samples_leaf | Adult: neighbors | Adult: dep-aware | Adult: difference | synthetic: neighbors | synthetic: dep-aware | synthetic: difference |
|---|---|---|---|---|---|---|
| 1 | −0.075 | 0.232 | +0.307 [0.249, 0.369], 95 | 0.608 | 0.792 | +0.184 [0.170, 0.199], 100 |
| 2 (protocol) | 0.483 | 0.537 | +0.054 [0.043, 0.065], 87 | 0.669 | 0.797 | +0.128 [0.117, 0.139], 100 |
| 5 | 0.602 | 0.621 | +0.019 [0.009, 0.028], 76 | 0.748 | 0.812 | +0.065 [0.059, 0.071], 99 |
| 10 | 0.639 | 0.651 | +0.012 [0.002, 0.021], 69 | 0.784 | 0.824 | +0.040 [0.035, 0.044], 98 |
| 20 | 0.675 | 0.684 | +0.010 [0.001, 0.018], 66 | 0.803 | 0.829 | +0.026 [0.023, 0.030], 96 |

- The hypothesis holds. The gap shrinks monotonically as leaves grow, on both datasets and both budgets (n = 200: Adult +0.377 → +0.018, synthetic +0.233 → +0.028). Going from the protocol forest to leaf size 20 removes about 80 % of the gap (Adult 0.054 → 0.010, synthetic 0.128 → 0.026), driven by training neighbors improving much more than the dependency-aware sampler.
- It does not vanish: at leaf size 20 the dependency-aware sampler is still ahead with CIs excluding zero, so memorization explains most of the difference, not all of it.
- Smoothing costs no accuracy: dev accuracy stays within 0.853–0.862 on Adult and 0.751–0.755 on synthetic across the sweep. The leaf-size-2 rows reproduce the main grid (Adult 0.537 and 0.483; synthetic 0.797 and 0.669).
- Stability: on Adult, training neighbors remain more stable than the dependency-aware sampler at every leaf size (0.80 vs 0.75 at the protocol setting, 0.86 vs 0.81 at leaf size 20); on synthetic the dependency-aware sampler is more stable and that gap also closes (training neighbors 0.938 vs dependency-aware 0.964 at leaf size 2; 0.964 vs 0.965 at leaf size 20).
- Consequence for the research question: against the strongest baseline, the value of perturbing real records depends on how rough the black box is at its training points. For a smooth model (logistic regression, or a forest with large leaves) plain training neighbors are nearly as faithful and at least as stable; for a memorizing model, perturbation is what makes the explanation transfer.

## 6. Repetitions and uncertainty

Every result uses 5 sampling seeds per case and 100 fixed cases; models are fixed (seed 0). Uncertainty is reported as paired percentile-bootstrap 95% CIs over cases with win counts, for fidelity, rank stability and RMSE; the week-4 confirmatory subset (cases never used for tuning) is unchanged. The isolating ablation and the leaf sweep follow the same budgets, seeds, cases, evaluation neighborhoods and kernel-width rule.

## 7. Compute

Same laptop as before (Apple M1 Pro, 8 cores, 16 GB, CPU only). Leaf sweep: 20,000 explanations in 48.7 min wall clock (Adult 35.1 min, synthetic 13.6 min; run while two analysis jobs shared the CPU; peak memory not instrumented, the comparable main-grid run peaked at 384 MB). Whole-grid error, control and ablation-stability analysis (`src/week5_analysis.py`): 15 s, including 6 model fits and 600 neighborhood rebuilds. Feature-stability check: 7 s. Nadia's isolating ablation: 2,000 explanations at about 0.1 s each in her environment. New artifacts: about 14 MB (`results/min_samples_leaf*`, `results/week5/`, `results/feature_groups/`).

## 8. Progress vs target, blockers, changes

Target met: ablations (two from the grid plus the isolating ablation), repetitions, paired uncertainty, the control analysis and failure analysis are all in hand. No blockers. To declare: (a) fidelity is now reported together with weighted RMSE, because R² alone overstates failures where the model is nearly constant; (b) the sum-of-|coef| feature stability is superseded by cardinality-robust definitions with a noise null; (c) the isolating ablation ran in a second software environment and is compared within its own run only; (d) locality weighting has no measurable benefit under this protocol. Housekeeping still open: Nadia's feature-group outputs live under `src/`, and her branch `week4-protocol-v1-eval` (categorical keep-probability and anchor-width knobs, defaults unchanged) is unmerged with no committed results.

## 9. Week-6 plan

1. Final report (6–8 pages) and 10-minute talk built on: held-out fidelity with RMSE, coefficient- and feature-level stability with nulls, the control, the two ablations, and the failure taxonomy.
2. Reproducibility package: one command per experiment already exists; add a top-level run-all script, record Nadia's environment next to `checkpoints/state.json`, move the feature-group outputs under `results/`, and list omitted experiments (SHAP baseline, synthetic isolating ablation).
3. Limitations section: one real dataset, two model classes, fidelity defined on a k-nearest dev neighborhood, kernel width tuned on a subset of the cases, 5 seeds per case.
