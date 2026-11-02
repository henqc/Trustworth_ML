# Pilot summary

fidelity = mean ± std over cases of the per-case mean over seeds; fidelity_med = median over cases of the per-case mean; rank_stability = mean over cases of the mean pairwise Spearman of |coef| across seeds.

## synthetic_dep / lr

| sampler | n | fidelity | fidelity_med | rank_stability | mean_nn_dist | frac_seen_combo | mean_dist_to_query | runtime_ms |
|---|---|---|---|---|---|---|---|---|
| independent | 200 | 0.787 ± 0.128 | 0.839 | 0.953 | 2.044 | 1.000 | 3.079 | 3.0 |
| independent | 500 | 0.791 ± 0.131 | 0.840 | 0.968 | 2.048 | 1.000 | 3.078 | 3.0 |
| neighbors | 200 | 0.905 ± 0.049 | 0.923 | 0.974 | 0.000 | 1.000 | 2.299 | 2.6 |
| neighbors | 500 | 0.908 ± 0.047 | 0.925 | 0.981 | 0.000 | 1.000 | 2.296 | 2.8 |
| dep_aware | 200 | 0.907 ± 0.047 | 0.924 | 0.970 | 0.938 | 1.000 | 2.449 | 3.5 |
| dep_aware | 500 | 0.911 ± 0.046 | 0.928 | 0.974 | 0.934 | 1.000 | 2.437 | 3.5 |
| abl_no_dependency | 200 | 0.881 ± 0.054 | 0.900 | 0.966 | 1.442 | 1.000 | 2.694 | 3.4 |
| abl_no_dependency | 500 | 0.887 ± 0.050 | 0.907 | 0.969 | 1.443 | 1.000 | 2.699 | 3.7 |
| abl_no_locality | 200 | 0.908 ± 0.043 | 0.924 | 0.970 | 0.938 | 1.000 | 2.449 | 3.5 |
| abl_no_locality | 500 | 0.912 ± 0.041 | 0.927 | 0.977 | 0.934 | 1.000 | 2.437 | 3.6 |

## synthetic_dep / rf

| sampler | n | fidelity | fidelity_med | rank_stability | mean_nn_dist | frac_seen_combo | mean_dist_to_query | runtime_ms |
|---|---|---|---|---|---|---|---|---|
| independent | 200 | 0.649 ± 0.097 | 0.670 | 0.926 | 2.044 | 1.000 | 3.079 | 29.5 |
| independent | 500 | 0.653 ± 0.109 | 0.676 | 0.957 | 2.048 | 1.000 | 3.078 | 29.7 |
| neighbors | 200 | 0.630 ± 0.079 | 0.655 | 0.880 | 0.000 | 1.000 | 2.299 | 29.3 |
| neighbors | 500 | 0.665 ± 0.077 | 0.681 | 0.937 | 0.000 | 1.000 | 2.296 | 29.6 |
| dep_aware | 200 | 0.792 ± 0.043 | 0.799 | 0.939 | 0.938 | 1.000 | 2.449 | 30.4 |
| dep_aware | 500 | 0.798 ± 0.046 | 0.804 | 0.959 | 0.934 | 1.000 | 2.437 | 32.4 |
| abl_no_dependency | 200 | 0.777 ± 0.046 | 0.787 | 0.937 | 1.442 | 1.000 | 2.694 | 30.0 |
| abl_no_dependency | 500 | 0.784 ± 0.043 | 0.789 | 0.963 | 1.443 | 1.000 | 2.699 | 36.7 |
| abl_no_locality | 200 | 0.796 ± 0.039 | 0.800 | 0.941 | 0.938 | 1.000 | 2.449 | 30.9 |
| abl_no_locality | 500 | 0.802 ± 0.040 | 0.808 | 0.960 | 0.934 | 1.000 | 2.437 | 31.5 |

## adult / rf

| sampler | n | fidelity | fidelity_med | rank_stability | mean_nn_dist | frac_seen_combo | mean_dist_to_query | runtime_ms |
|---|---|---|---|---|---|---|---|---|
| independent | 200 | -6.890 ± 14.089 | -2.853 | 0.052 | 2.555 | 0.255 | 3.869 | 36.2 |
| independent | 500 | -5.685 ± 12.672 | -2.148 | 0.118 | 2.556 | 0.235 | 3.871 | 39.0 |
| neighbors | 200 | 0.391 ± 0.281 | 0.493 | 0.563 | 0.000 | 1.000 | 2.232 | 39.5 |
| neighbors | 500 | 0.466 ± 0.272 | 0.568 | 0.805 | 0.000 | 1.000 | 2.231 | 41.5 |
| dep_aware | 200 | 0.490 ± 0.260 | 0.550 | 0.564 | 0.355 | 1.000 | 2.271 | 45.8 |
| dep_aware | 500 | 0.524 ± 0.255 | 0.611 | 0.761 | 0.354 | 1.000 | 2.266 | 49.0 |
| abl_no_dependency | 200 | -1.998 ± 5.715 | 0.213 | 0.182 | 1.967 | 0.267 | 3.428 | 40.9 |
| abl_no_dependency | 500 | -1.045 ± 3.589 | 0.154 | 0.234 | 1.997 | 0.233 | 3.440 | 43.9 |
| abl_no_locality | 200 | 0.490 ± 0.260 | 0.550 | 0.566 | 0.355 | 1.000 | 2.271 | 45.8 |
| abl_no_locality | 500 | 0.524 ± 0.255 | 0.611 | 0.758 | 0.354 | 1.000 | 2.266 | 50.9 |

## synthetic_indep / rf

| sampler | n | fidelity | fidelity_med | rank_stability | mean_nn_dist | frac_seen_combo | mean_dist_to_query | runtime_ms |
|---|---|---|---|---|---|---|---|---|
| independent | 500 | 0.695 ± 0.134 | 0.733 | 0.945 | 2.160 | 1.000 | 3.078 | 30.4 |
| dep_aware | 500 | 0.831 ± 0.064 | 0.858 | 0.955 | 0.975 | 1.000 | 2.618 | 33.8 |

estimated full-grid minutes: 55.6 (30,000 explanations, sequential; adult lr uses adult rf timing as an upper bound, synthetic_indep uses synthetic_dep timings)
