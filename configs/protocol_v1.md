# Evaluation protocol v1 (frozen 2026-11-08, before the main grid ran)

Research question: does a dependency-aware perturbation neighborhood improve local-surrogate fidelity and stability compared with independent feature perturbation, at equal query budgets?

## Fixed inputs
- Splits and cases: `manifests/splits.json` (seed 0). Explanation cases = the 100 `explain_idx` rows of each dataset's test split, in manifest order. Dev is used only for the evaluation neighborhoods and for reported accuracy. Test labels are never used.
- Datasets: `synthetic_dep` (correlated pair), `synthetic_indep` (independent-feature control), `adult` (published train/test; 80/20 train/dev of the published train file).
- Models: `fit_models(ds, seed=0)` from `src/data.py`: logistic regression and a 200-tree random forest, preprocessing fit on train only. Identical fitted models for every condition.
- Budgets n: 200 and 500 samples per explanation. Seeds: 0, 1, 2, 3, 4 (sampling seeds; models are fixed).

## Conditions (same model, same cases, same budget, same evaluation neighborhood)
| condition | sampler | notes |
|---|---|---|
| `independent` | `sample_independent`, scale 1.0 | LIME-style baseline: each numeric perturbed at one training std, categoricals from training marginals |
| `independent_matched` | `sample_independent`, scale 0.75 on synthetic, 0.25 on Adult | distance-matched baseline from the week-3 sweep (Adult is the closest achievable, not a true match) |
| `neighbors` | `sample_neighbors`, k = 200 | training-neighbor baseline: real records only |
| `dep_aware` | `sample_dependency_aware`, k = 200, scale 0.5 | the original component |
| `abl_no_dependency` | `sample_dependency_aware(dependencies=False)` | ablation: independent anchor per numeric coordinate, marginal categoricals, diagonal noise |
| `abl_no_locality` | `sample_dependency_aware`, `locality=False` | ablation: uniform surrogate weights |

Not run this week: SHAP (optional in the brief), a categorical keep-probability variant of the independent sampler (not in the brief's comparison set).

## Surrogate and weighting
- Surrogate: hand-written weighted ridge (`weighted_ridge`, alpha = 1e-3, intercept unpenalized) on the Z representation (standardized numerics + one-hot categoricals) with target = black-box P(y = 1).
- Kernel: exp(-d^2 / width^2) on Z-space Euclidean distance. Width = the median distance from the case's evaluation neighborhood to the query (computed once per case; same width for fitting, fidelity and fit R^2). Rationale: week-3 sweep (`results/w4_scale_match.md`); LIME's 0.75*sqrt(p) is near-uniform on Adult's 105-dim Z space.
- Known limitation kept as is: the anchor-selection kernel inside `sample_dependency_aware` still uses 0.75*sqrt(p).

## Metrics (per explanation unless stated)
- Fidelity: kernel-weighted R^2 of the surrogate against the black box on the predefined evaluation neighborhood = the 200 nearest dev records to the query in Z space, computed once per case and shared by every condition and seed. Never on the fit samples. `fit_r2` on the fit samples is recorded for reference only.
- Rank stability (per case): mean pairwise Spearman correlation of |coef| across the 5 seeds, over coefficients that are nonzero in at least one seed.
- Validity: mean Z distance from each sample to its nearest training record; fraction of samples whose raw categorical tuple occurs in training (empirical support, not impossibility). Mean distance from samples to the query.
- Runtime: `runtime_s` (sampling + black-box queries + surrogate fit) and `wall_s` (including fidelity and validity).

## Analysis
- Primary unit = case. Per (dataset, model, n, condition): mean +- sd and median over cases of the per-case seed mean of fidelity; mean over cases of per-case rank stability; means of validity and runtime.
- Paired comparisons: per-case differences dep_aware - baseline for baseline in {independent, independent_matched, neighbors}, fidelity and rank stability, with percentile bootstrap 95% CIs over the 100 cases (2,000 resamples, seed 0) and the number of cases where dep_aware is higher. Ablation gaps dep_aware - abl_* reported the same way. Control: dep_aware - independent on synthetic_indep.
- Report by condition and dataset/model/budget, not only aggregates. Representative failures: the five lowest-fidelity cases per dataset/model for dep_aware and independent.
- Non-finite metrics are counted and reported, not silently dropped.

## Compute plan
6 conditions x 2 budgets x 5 seeds x 100 cases x 2 models x 3 datasets = 36,000 explanations; week-3 timings predict about 70 minutes sequential on the M1 Pro laptop (C0). Outputs: `results/main/grid.csv` (every explanation), `results/main/coefs_{dataset}_{model}.npy` (every coefficient vector), `results/main/summary.csv|md`, `results/main/paired.csv`, figures in `results/figures/`.

## Amendments (2026-11-08, after an adversarial code review, before results were read)
1. Disclosure: the kernel-width rule and the matched scales were chosen on the first 30 synthetic and 15 Adult explanation cases (pilot and week-3 sweep), which are part of the 100-case sets. The analysis therefore also reports every paired comparison on the untouched cases only (`paired_heldout_cases.csv`, synthetic cases 31-100, Adult 16-100) as the confirmatory subset.
2. The `abl_no_dependency` condition removes dependency structure AND changes the noise scale (global training std instead of the local stratum covariance), so its gap to `dep_aware` is a dependency-plus-scale effect. It is reported as such; an isolating ablation that keeps the local diagonal variance and removes only the correlations and the categorical block is scheduled for week 5.
3. Failure cases are listed per budget (n = 200 and n = 500), not only at n = 500.
4. The analysis verifies grid completeness (every condition x budget x case x seed exactly once, cases in manifest order, no NaN coefficients) before computing anything, and keeps the exclusion counts in the CSVs.
