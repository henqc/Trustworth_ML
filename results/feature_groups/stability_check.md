# Is the feature-level stability of the independent sampler a cardinality artifact?

The teammate's sum-of-|coef| feature importance makes the independent sampler look more stable than dep_aware at the original-feature level, reversing the coefficient-level result. We test whether that ranking is fixed by cardinality times estimation noise (a noise null with no signal shared across seeds) and recompute stability with cardinality-robust importances.

Cells: observed / noise-null mean pairwise Spearman across 5 seeds, mean over 100 cases. Null: each coefficient drawn independently per seed from N(0, s_j^2), s_j its across-seed sd, 20 repetitions. Undefined seed pairs (a constant importance vector) are excluded and counted in `n_undefined` (total over all query_level rows: 0).

## Adult RF, n = 500

| condition | coefficient_level | sum_abs | mean_abs | l2_norm | query_level |
| --- | --- | --- | --- | --- | --- |
| independent | 0.164 / 0.425 | 0.956 / 0.890 | 0.769 / 0.797 | 0.839 / 0.825 | 0.642 / 0.322 |
| independent_matched | 0.453 / 0.384 | 0.948 / 0.872 | 0.801 / 0.491 | 0.832 / 0.561 | 0.767 / 0.275 |
| neighbors | 0.803 / 0.494 | 0.933 / 0.878 | 0.920 / 0.768 | 0.917 / 0.764 | 0.888 / 0.618 |
| dep_aware | 0.747 / 0.470 | 0.923 / 0.888 | 0.920 / 0.757 | 0.911 / 0.770 | 0.868 / 0.602 |
| abl_no_dependency | 0.291 / 0.423 | 0.952 / 0.897 | 0.797 / 0.703 | 0.816 / 0.751 | 0.766 / 0.337 |
| abl_no_locality | 0.741 / 0.453 | 0.922 / 0.885 | 0.918 / 0.750 | 0.909 / 0.764 | 0.863 / 0.590 |

## Adult LR, n = 500

| condition | coefficient_level | sum_abs | mean_abs | l2_norm | query_level |
| --- | --- | --- | --- | --- | --- |
| independent | 0.183 / 0.440 | 0.961 / 0.891 | 0.790 / 0.802 | 0.832 / 0.827 | 0.665 / 0.354 |
| independent_matched | 0.350 / 0.424 | 0.970 / 0.871 | 0.825 / 0.550 | 0.875 / 0.632 | 0.734 / 0.223 |
| neighbors | 0.876 / 0.553 | 0.958 / 0.888 | 0.959 / 0.793 | 0.956 / 0.802 | 0.938 / 0.656 |
| dep_aware | 0.861 / 0.515 | 0.960 / 0.896 | 0.961 / 0.782 | 0.955 / 0.796 | 0.934 / 0.637 |
| abl_no_dependency | 0.362 / 0.456 | 0.974 / 0.894 | 0.855 / 0.727 | 0.888 / 0.773 | 0.809 / 0.320 |
| abl_no_locality | 0.858 / 0.500 | 0.958 / 0.894 | 0.959 / 0.773 | 0.953 / 0.789 | 0.930 / 0.625 |

## Cardinality dependence of sum_abs

Spearman(cardinality, mean sum_abs importance) over the 14 features:

- RF n=200: independent 0.93, independent_matched 0.87, neighbors 0.70, dep_aware 0.65, abl_no_dependency 0.81, abl_no_locality 0.65
- RF n=500: independent 0.90, independent_matched 0.88, neighbors 0.72, dep_aware 0.65, abl_no_dependency 0.80, abl_no_locality 0.65
- LR n=200: independent 0.92, independent_matched 0.84, neighbors 0.51, dep_aware 0.53, abl_no_dependency 0.85, abl_no_locality 0.53
- LR n=500: independent 0.89, independent_matched 0.82, neighbors 0.55, dep_aware 0.54, abl_no_dependency 0.86, abl_no_locality 0.54

Adult RF n = 500, sum_abs importance and mean rank (1 = largest), mean over cases and seeds:

| feature | cardinality | independent importance | independent rank | dep_aware importance | dep_aware rank |
| --- | --- | --- | --- | --- | --- |
| native-country | 41 | 1.848 | 1.0 | 0.114 | 7.805 |
| education | 16 | 0.656 | 2.338 | 0.155 | 4.889 |
| occupation | 14 | 0.519 | 2.682 | 0.421 | 1.983 |
| workclass | 8 | 0.186 | 6.166 | 0.138 | 5.838 |
| marital-status | 7 | 0.27 | 4.686 | 0.141 | 6.724 |
| relationship | 6 | 0.257 | 4.82 | 0.147 | 5.82 |
| race | 5 | 0.156 | 6.964 | 0.051 | 8.496 |
| sex | 2 | 0.03 | 10.868 | 0.022 | 10.579 |
| age | 1 | 0.032 | 10.41 | 0.048 | 7.752 |
| capital-gain | 1 | 0.143 | 7.346 | 0.149 | 5.32 |
| capital-loss | 1 | 0.008 | 13.214 | 0.006 | 12.0 |
| education-num | 1 | 0.033 | 10.532 | 0.042 | 9.02 |
| fnlwgt | 1 | 0.009 | 12.98 | 0.011 | 10.416 |
| hours-per-week | 1 | 0.028 | 10.994 | 0.043 | 8.358 |

## Signal-to-noise (RF n = 500)

Median over cases of var_features(seed-mean importance) / mean_features(var_seeds(importance)); observed / null.

| condition | sum_abs | mean_abs | l2_norm | query_level |
| --- | --- | --- | --- | --- |
| independent | 13.3 / 37.5 | 16.0 / 5.8 | 12.6 / 6.7 | 7.1 / 0.7 |
| dep_aware | 18.4 / 4.9 | 8.6 / 1.7 | 9.9 / 1.8 | 7.9 / 1.2 |
| neighbors | 25.6 / 4.7 | 14.0 / 1.6 | 14.0 / 1.7 | 11.3 / 1.2 |

## Sensitivity: |coef| < 1e-08 set to 0 (numerical zeros), n = 500

RF:

| condition | coefficient_level_snap | sum_abs_snap | mean_abs_snap | l2_norm_snap | query_level_snap |
| --- | --- | --- | --- | --- | --- |
| independent | 0.164 / 0.425 | 0.956 / 0.890 | 0.769 / 0.797 | 0.839 / 0.825 | 0.642 / 0.322 |
| independent_matched | 0.453 / 0.384 | 0.948 / 0.872 | 0.801 / 0.491 | 0.832 / 0.561 | 0.767 / 0.275 |
| neighbors | 0.783 / 0.392 | 0.941 / 0.887 | 0.926 / 0.771 | 0.923 / 0.770 | 0.895 / 0.626 |
| dep_aware | 0.734 / 0.416 | 0.925 / 0.891 | 0.923 / 0.759 | 0.914 / 0.773 | 0.871 / 0.605 |
| abl_no_dependency | 0.291 / 0.423 | 0.952 / 0.897 | 0.797 / 0.703 | 0.816 / 0.751 | 0.766 / 0.337 |
| abl_no_locality | 0.730 / 0.409 | 0.924 / 0.887 | 0.920 / 0.751 | 0.911 / 0.766 | 0.865 / 0.591 |

LR:

| condition | coefficient_level_snap | sum_abs_snap | mean_abs_snap | l2_norm_snap | query_level_snap |
| --- | --- | --- | --- | --- | --- |
| independent | 0.183 / 0.440 | 0.961 / 0.891 | 0.790 / 0.802 | 0.832 / 0.827 | 0.665 / 0.354 |
| independent_matched | 0.350 / 0.424 | 0.970 / 0.871 | 0.825 / 0.550 | 0.875 / 0.632 | 0.734 / 0.223 |
| neighbors | 0.869 / 0.469 | 0.967 / 0.897 | 0.965 / 0.797 | 0.962 / 0.809 | 0.947 / 0.665 |
| dep_aware | 0.857 / 0.470 | 0.962 / 0.900 | 0.964 / 0.784 | 0.958 / 0.799 | 0.936 / 0.640 |
| abl_no_dependency | 0.362 / 0.456 | 0.974 / 0.894 | 0.855 / 0.727 | 0.888 / 0.773 | 0.809 / 0.320 |
| abl_no_locality | 0.854 / 0.461 | 0.961 / 0.896 | 0.961 / 0.774 | 0.955 / 0.791 | 0.933 / 0.626 |

## Verdict

- **Mostly an artifact.** sum_abs at n=500: RF independent 0.956 (null 0.890) vs dep_aware 0.923 (null 0.888); LR independent 0.961 (null 0.891) vs dep_aware 0.960 (null 0.896). Noise with no signal shared across seeds gets 0.867-0.905 in all 24 model x condition x n rows. It ranks cardinality: Spearman(cardinality, importance) RF n=500 is 0.90 for independent vs 0.65 for dep_aware, and native-country (41 levels) has mean rank 1.00 under independent (7.80 under dep_aware).
- **Not entirely.** Above the null, sum_abs excess is independent 0.066 vs dep_aware 0.036 (RF n=500), 0.023 vs -0.043 (RF n=200), 0.070 vs 0.064 (LR n=500). So independent keeps a small residual edge under this metric (mainly RF). The null does not account for it, but it sits in the ~0.11 of headroom above the floor.
- **What survives: dep_aware is more stable than independent under every cardinality-robust definition** (n=500, dep_aware vs independent). RF: mean_abs 0.920 vs 0.769, l2_norm 0.911 vs 0.839, query_level 0.868 vs 0.642. LR: 0.961 vs 0.790, 0.955 vs 0.832, 0.934 vs 0.665. This holds at both budgets for both models. Under mean_abs and l2_norm independent sits at its null (excess RF -0.028, 0.014; LR -0.012, 0.005), while dep_aware is 0.141-0.179 above its null. neighbors matches dep_aware within 0.019.
- **Query level** (the coefficient of the record's own category): both samplers beat their null (RF excess independent 0.321, dep_aware 0.266). But dep_aware's null is already 0.602 vs 0.322: features that do not vary in a local neighborhood get ~0 in every seed, and the null keeps that. Part of the query-level gap is that cheap agreement.
- **Report**: do not cite sum-|coef| feature-level stability as evidence that independent is more stable. It is dominated by a cardinality floor (null 0.87-0.91). Report a cardinality-normalised (mean_abs) or query-level feature stability with its null next to coefficient-level rank stability. The coefficient-level direction holds at the feature level, with a smaller gap (RF n=500 dep_aware - independent: coefficient 0.583, mean_abs 0.151, l2_norm 0.072, query_level 0.226).
- **Uncertain**: (a) the Gaussian null is not a strict floor. For independent, coefficient-level stability is 0.164 (null 0.425). This fits 30% of its coefficients being exactly 0 in some seeds but not others (rare levels drawn or not), zero inflation that a Gaussian null does not reproduce. So 'excess' is a rough scale. (b) The size of the robust gap depends on the definition (0.072-0.269). (c) One-hot levels are identified only up to a shift within a feature (no level is dropped; the tie is broken by ridge alpha), and per-level and per-SD numeric magnitudes are not on one scale. (d) Numerical zeros (|coef| < 1e-08, 1.8% of neighbors coefficients) move any stability by at most 0.031 (sensitivity table). (e) The variance-ratio SNR does not order the samplers the way Spearman does (RF n=500 mean_abs: independent 16.0 vs dep_aware 8.6; nulls 5.8 vs 1.7). It is driven by how far apart the few largest features are, while Spearman weighs all 14 ranks. (f) Only 5 seeds per case.
