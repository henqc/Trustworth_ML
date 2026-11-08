# Main grid summary

Fidelity: per case, the mean over its finite seeds; then mean +- sd, median and [q1, q3] over cases (validity and runtime columns: per-case seed mean, then mean over cases). Rank stability: per case, the mean pairwise Spearman of |coef| across seeds; then mean +- sd over cases with a finite value.

## By condition

### synthetic_dep / lr

| condition | n | fidelity mean ± sd | median [q1, q3] | rank stability | mean_nn_dist | frac_seen_combo | mean_dist_to_query | runtime ms |
|---|---|---|---|---|---|---|---|---|
| independent | 200 | 0.825 ± 0.002 | 0.825 [0.824, 0.826] | 0.964 ± 0.000 | 2.170 | 1.000 | 3.093 | 3.0 |
| independent | 500 | 0.847 ± 0.018 | 0.855 [0.841, 0.857] | 0.980 ± 0.025 | 2.159 | 1.000 | 3.077 | 2.7 |
| independent_matched | 200 | 0.878 ± 0.008 | 0.876 [0.873, 0.881] | 0.972 ± 0.007 | 1.846 | 1.000 | 2.320 | 2.6 |
| independent_matched | 500 | 0.895 ± 0.019 | 0.896 [0.886, 0.905] | 0.980 ± 0.007 | 1.836 | 1.000 | 2.308 | 2.7 |
| neighbors | 200 | 0.897 ± 0.028 | 0.884 [0.881, 0.907] | 0.968 ± 0.019 | 0.000 | 1.000 | 2.448 | 2.6 |
| neighbors | 500 | 0.900 ± 0.032 | 0.884 [0.881, 0.910] | 0.980 ± 0.014 | 0.000 | 1.000 | 2.444 | 2.4 |
| dep_aware | 200 | 0.903 ± 0.031 | 0.893 [0.885, 0.915] | 0.960 ± 0.007 | 0.968 | 1.000 | 2.587 | 4.4 |
| dep_aware | 500 | 0.907 ± 0.032 | 0.895 [0.889, 0.919] | 0.980 ± 0.014 | 0.962 | 1.000 | 2.574 | 3.3 |
| abl_no_dependency | 200 | 0.894 ± 0.027 | 0.887 [0.879, 0.905] | 0.968 ± 0.019 | 1.482 | 1.000 | 2.786 | 3.0 |
| abl_no_dependency | 500 | 0.896 ± 0.028 | 0.890 [0.880, 0.908] | 0.992 ± 0.007 | 1.480 | 1.000 | 2.801 | 3.3 |
| abl_no_locality | 200 | 0.903 ± 0.032 | 0.893 [0.885, 0.916] | 0.956 ± 0.007 | 0.968 | 1.000 | 2.587 | 3.2 |
| abl_no_locality | 500 | 0.908 ± 0.032 | 0.895 [0.889, 0.920] | 0.980 ± 0.014 | 0.962 | 1.000 | 2.574 | 3.2 |

### synthetic_dep / rf

| condition | n | fidelity mean ± sd | median [q1, q3] | rank stability | mean_nn_dist | frac_seen_combo | mean_dist_to_query | runtime ms |
|---|---|---|---|---|---|---|---|---|
| independent | 200 | 0.670 ± 0.021 | 0.667 [0.659, 0.679] | 0.943 ± 0.049 | 2.170 | 1.000 | 3.093 | 28.8 |
| independent | 500 | 0.684 ± 0.015 | 0.680 [0.676, 0.691] | 0.935 ± 0.025 | 2.159 | 1.000 | 3.077 | 29.6 |
| independent_matched | 200 | 0.698 ± 0.060 | 0.711 [0.672, 0.731] | 0.968 ± 0.014 | 1.846 | 1.000 | 2.320 | 29.5 |
| independent_matched | 500 | 0.717 ± 0.041 | 0.709 [0.695, 0.735] | 0.943 ± 0.014 | 1.836 | 1.000 | 2.308 | 28.7 |
| neighbors | 200 | 0.587 ± 0.089 | 0.582 [0.541, 0.630] | 0.943 ± 0.007 | 0.000 | 1.000 | 2.448 | 29.5 |
| neighbors | 500 | 0.619 ± 0.096 | 0.602 [0.567, 0.662] | 0.931 ± 0.046 | 0.000 | 1.000 | 2.444 | 28.4 |
| dep_aware | 200 | 0.795 ± 0.033 | 0.783 [0.776, 0.808] | 0.956 ± 0.043 | 0.968 | 1.000 | 2.587 | 29.8 |
| dep_aware | 500 | 0.803 ± 0.032 | 0.788 [0.784, 0.813] | 0.947 ± 0.043 | 0.962 | 1.000 | 2.574 | 30.0 |
| abl_no_dependency | 200 | 0.790 ± 0.029 | 0.790 [0.776, 0.805] | 0.939 ± 0.084 | 1.482 | 1.000 | 2.786 | 29.9 |
| abl_no_dependency | 500 | 0.796 ± 0.028 | 0.787 [0.780, 0.807] | 0.964 ± 0.012 | 1.480 | 1.000 | 2.801 | 30.2 |
| abl_no_locality | 200 | 0.797 ± 0.033 | 0.783 [0.778, 0.808] | 0.947 ± 0.035 | 0.968 | 1.000 | 2.587 | 29.8 |
| abl_no_locality | 500 | 0.805 ± 0.033 | 0.790 [0.787, 0.816] | 0.972 ± 0.025 | 0.962 | 1.000 | 2.574 | 32.5 |

### synthetic_indep / lr

| condition | n | fidelity mean ± sd | median [q1, q3] | rank stability | mean_nn_dist | frac_seen_combo | mean_dist_to_query | runtime ms |
|---|---|---|---|---|---|---|---|---|
| independent | 200 | 0.881 ± 0.006 | 0.880 [0.878, 0.884] | 0.972 ± 0.019 | 1.915 | 1.000 | 3.093 | 2.8 |
| independent | 500 | 0.900 ± 0.002 | 0.901 [0.899, 0.901] | 1.000 ± 0.000 | 1.910 | 1.000 | 3.077 | 2.9 |
| independent_matched | 200 | 0.911 ± 0.012 | 0.917 [0.907, 0.918] | 0.960 ± 0.019 | 1.612 | 1.000 | 2.320 | 2.9 |
| independent_matched | 500 | 0.920 ± 0.020 | 0.931 [0.914, 0.931] | 0.992 ± 0.007 | 1.616 | 1.000 | 2.308 | 2.9 |
| neighbors | 200 | 0.908 ± 0.024 | 0.922 [0.901, 0.922] | 0.980 ± 0.014 | 0.000 | 1.000 | 2.187 | 2.8 |
| neighbors | 500 | 0.911 ± 0.023 | 0.923 [0.904, 0.925] | 0.980 ± 0.014 | 0.000 | 1.000 | 2.185 | 2.7 |
| dep_aware | 200 | 0.913 ± 0.026 | 0.927 [0.905, 0.928] | 0.964 ± 0.032 | 0.931 | 1.000 | 2.336 | 3.5 |
| dep_aware | 500 | 0.918 ± 0.027 | 0.933 [0.910, 0.934] | 0.980 ± 0.025 | 0.929 | 1.000 | 2.326 | 3.7 |
| abl_no_dependency | 200 | 0.917 ± 0.018 | 0.925 [0.911, 0.927] | 0.960 ± 0.014 | 1.401 | 1.000 | 2.596 | 3.2 |
| abl_no_dependency | 500 | 0.923 ± 0.018 | 0.931 [0.917, 0.933] | 0.980 ± 0.019 | 1.398 | 1.000 | 2.602 | 3.5 |
| abl_no_locality | 200 | 0.913 ± 0.023 | 0.926 [0.906, 0.926] | 0.972 ± 0.019 | 0.931 | 1.000 | 2.336 | 3.8 |
| abl_no_locality | 500 | 0.919 ± 0.023 | 0.932 [0.912, 0.932] | 0.976 ± 0.032 | 0.929 | 1.000 | 2.326 | 3.4 |

### synthetic_indep / rf

| condition | n | fidelity mean ± sd | median [q1, q3] | rank stability | mean_nn_dist | frac_seen_combo | mean_dist_to_query | runtime ms |
|---|---|---|---|---|---|---|---|---|
| independent | 200 | 0.786 ± 0.007 | 0.788 [0.783, 0.790] | 0.972 ± 0.039 | 1.915 | 1.000 | 3.093 | 29.6 |
| independent | 500 | 0.801 ± 0.011 | 0.803 [0.796, 0.806] | 0.968 ± 0.031 | 1.910 | 1.000 | 3.077 | 29.3 |
| independent_matched | 200 | 0.836 ± 0.012 | 0.842 [0.832, 0.843] | 0.919 ± 0.046 | 1.612 | 1.000 | 2.320 | 29.5 |
| independent_matched | 500 | 0.854 ± 0.014 | 0.859 [0.849, 0.862] | 0.947 ± 0.035 | 1.616 | 1.000 | 2.308 | 29.1 |
| neighbors | 200 | 0.818 ± 0.054 | 0.842 [0.799, 0.849] | 0.952 ± 0.064 | 0.000 | 1.000 | 2.187 | 29.0 |
| neighbors | 500 | 0.826 ± 0.041 | 0.834 [0.808, 0.848] | 0.935 ± 0.050 | 0.000 | 1.000 | 2.185 | 29.5 |
| dep_aware | 200 | 0.879 ± 0.006 | 0.878 [0.876, 0.882] | 0.972 ± 0.028 | 0.931 | 1.000 | 2.336 | 29.7 |
| dep_aware | 500 | 0.884 ± 0.002 | 0.884 [0.883, 0.885] | 0.992 ± 0.007 | 0.929 | 1.000 | 2.326 | 29.8 |
| abl_no_dependency | 200 | 0.875 ± 0.004 | 0.875 [0.873, 0.876] | 0.976 ± 0.021 | 1.401 | 1.000 | 2.596 | 30.1 |
| abl_no_dependency | 500 | 0.883 ± 0.005 | 0.883 [0.880, 0.885] | 0.960 ± 0.031 | 1.398 | 1.000 | 2.602 | 30.3 |
| abl_no_locality | 200 | 0.879 ± 0.006 | 0.877 [0.876, 0.881] | 0.964 ± 0.021 | 0.931 | 1.000 | 2.336 | 30.4 |
| abl_no_locality | 500 | 0.884 ± 0.002 | 0.884 [0.883, 0.885] | 0.984 ± 0.028 | 0.929 | 1.000 | 2.326 | 29.9 |

### adult / lr

| condition | n | fidelity mean ± sd | median [q1, q3] | rank stability | mean_nn_dist | frac_seen_combo | mean_dist_to_query | runtime ms |
|---|---|---|---|---|---|---|---|---|
| independent | 200 | 0.474 ± 0.307 | 0.448 [0.314, 0.620] | -0.005 ± 0.067 | 2.587 | 0.240 | 3.728 | 7.9 |
| independent | 500 | 0.515 ± 0.405 | 0.655 [0.357, 0.743] | 0.162 ± 0.102 | 2.574 | 0.249 | 3.717 | 9.9 |
| independent_matched | 200 | 0.577 ± 0.351 | 0.576 [0.401, 0.752] | 0.152 ± 0.151 | 2.032 | 0.240 | 2.922 | 7.2 |
| independent_matched | 500 | 0.664 ± 0.301 | 0.687 [0.520, 0.820] | 0.374 ± 0.167 | 2.022 | 0.249 | 2.891 | 8.0 |
| neighbors | 200 | 0.888 ± 0.045 | 0.878 [0.864, 0.907] | 0.891 ± 0.124 | 0.000 | 1.000 | 2.120 | 12.7 |
| neighbors | 500 | 0.899 ± 0.034 | 0.881 [0.880, 0.909] | 0.912 ± 0.132 | 0.000 | 1.000 | 2.118 | 12.0 |
| dep_aware | 200 | 0.884 ± 0.042 | 0.871 [0.861, 0.901] | 0.605 ± 0.165 | 0.382 | 1.000 | 2.179 | 14.7 |
| dep_aware | 500 | 0.907 ± 0.030 | 0.901 [0.890, 0.920] | 0.975 ± 0.004 | 0.384 | 1.000 | 2.171 | 16.7 |
| abl_no_dependency | 200 | 0.838 ± 0.103 | 0.855 [0.791, 0.894] | 0.120 ± 0.059 | 2.067 | 0.258 | 3.293 | 11.8 |
| abl_no_dependency | 500 | 0.835 ± 0.112 | 0.825 [0.776, 0.888] | 0.411 ± 0.124 | 2.082 | 0.230 | 3.336 | 12.9 |
| abl_no_locality | 200 | 0.884 ± 0.042 | 0.872 [0.860, 0.901] | 0.598 ± 0.170 | 0.382 | 1.000 | 2.179 | 14.7 |
| abl_no_locality | 500 | 0.906 ± 0.030 | 0.901 [0.890, 0.920] | 0.971 ± 0.004 | 0.384 | 1.000 | 2.171 | 17.3 |

### adult / rf

| condition | n | fidelity mean ± sd | median [q1, q3] | rank stability | mean_nn_dist | frac_seen_combo | mean_dist_to_query | runtime ms |
|---|---|---|---|---|---|---|---|---|
| independent | 200 | -0.718 ± 1.618 | -0.062 [-1.311, 0.203] | 0.021 ± 0.150 | 2.587 | 0.240 | 3.728 | 34.9 |
| independent | 500 | -0.505 ± 1.420 | 0.103 [-1.012, 0.306] | 0.011 ± 0.046 | 2.574 | 0.249 | 3.717 | 34.3 |
| independent_matched | 200 | 0.320 ± 0.315 | 0.228 [0.145, 0.449] | 0.188 ± 0.163 | 2.032 | 0.240 | 2.922 | 34.3 |
| independent_matched | 500 | 0.345 ± 0.331 | 0.241 [0.160, 0.479] | 0.406 ± 0.107 | 2.022 | 0.249 | 2.891 | 34.8 |
| neighbors | 200 | 0.410 ± 0.252 | 0.533 [0.326, 0.555] | 0.713 ± 0.294 | 0.000 | 1.000 | 2.120 | 37.6 |
| neighbors | 500 | 0.470 ± 0.226 | 0.567 [0.390, 0.600] | 0.794 ± 0.140 | 0.000 | 1.000 | 2.118 | 37.5 |
| dep_aware | 200 | 0.504 ± 0.138 | 0.552 [0.451, 0.582] | 0.577 ± 0.185 | 0.382 | 1.000 | 2.179 | 48.1 |
| dep_aware | 500 | 0.557 ± 0.113 | 0.600 [0.515, 0.621] | 0.736 ± 0.127 | 0.384 | 1.000 | 2.171 | 58.8 |
| abl_no_dependency | 200 | 0.348 ± 0.126 | 0.390 [0.299, 0.419] | 0.018 ± 0.079 | 2.067 | 0.258 | 3.293 | 42.9 |
| abl_no_dependency | 500 | 0.349 ± 0.188 | 0.443 [0.288, 0.457] | 0.243 ± 0.124 | 2.082 | 0.230 | 3.336 | 46.7 |
| abl_no_locality | 200 | 0.504 ± 0.137 | 0.551 [0.450, 0.581] | 0.560 ± 0.164 | 0.382 | 1.000 | 2.179 | 45.3 |
| abl_no_locality | 500 | 0.558 ± 0.104 | 0.599 [0.519, 0.618] | 0.748 ± 0.135 | 0.384 | 1.000 | 2.171 | 46.3 |

## Paired comparisons (dep_aware minus baseline, per case; percentile bootstrap 95% CI, 2,000 resamples)

### synthetic_dep / lr

| comparison | n | metric | diff mean | 95% CI | wins/n |
|---|---|---|---|---|---|
| dep_aware-independent | 200 | fidelity | +0.078 | [+0.051, +0.113] | 3/3 |
| dep_aware-independent | 200 | rank_stability | -0.004 | [-0.012, +0.000] | 0/3 |
| dep_aware-independent_matched | 200 | fidelity | +0.025 | [+0.007, +0.051] | 3/3 |
| dep_aware-independent_matched | 200 | rank_stability | -0.012 | [-0.012, -0.012] | 0/3 |
| dep_aware-neighbors | 200 | fidelity | +0.006 | [-0.000, +0.009] | 2/3 |
| dep_aware-neighbors | 200 | rank_stability | -0.008 | [-0.024, +0.012] | 1/3 |
| dep_aware-abl_no_dependency | 200 | fidelity | +0.009 | [+0.006, +0.015] | 3/3 |
| dep_aware-abl_no_dependency | 200 | rank_stability | -0.008 | [-0.024, +0.012] | 1/3 |
| dep_aware-abl_no_locality | 200 | fidelity | -0.000 | [-0.001, +0.001] | 1/3 |
| dep_aware-abl_no_locality | 200 | rank_stability | +0.004 | [+0.000, +0.012] | 1/3 |
| dep_aware-independent | 500 | fidelity | +0.061 | [+0.040, +0.085] | 3/3 |
| dep_aware-independent | 500 | rank_stability | +0.000 | [-0.036, +0.036] | 1/3 |
| dep_aware-independent_matched | 500 | fidelity | +0.012 | [-0.001, +0.030] | 2/3 |
| dep_aware-independent_matched | 500 | rank_stability | -0.000 | [-0.024, +0.012] | 2/3 |
| dep_aware-neighbors | 500 | fidelity | +0.008 | [+0.004, +0.011] | 3/3 |
| dep_aware-neighbors | 500 | rank_stability | +0.000 | [-0.024, +0.024] | 1/3 |
| dep_aware-abl_no_dependency | 500 | fidelity | +0.012 | [+0.005, +0.018] | 3/3 |
| dep_aware-abl_no_dependency | 500 | rank_stability | -0.012 | [-0.024, +0.000] | 0/3 |
| dep_aware-abl_no_locality | 500 | fidelity | -0.000 | [-0.000, -0.000] | 0/3 |
| dep_aware-abl_no_locality | 500 | rank_stability | +0.000 | [+0.000, +0.000] | 0/3 |

### synthetic_dep / rf

| comparison | n | metric | diff mean | 95% CI | wins/n |
|---|---|---|---|---|---|
| dep_aware-independent | 200 | fidelity | +0.125 | [+0.103, +0.141] | 3/3 |
| dep_aware-independent | 200 | rank_stability | +0.012 | [-0.085, +0.085] | 2/3 |
| dep_aware-independent_matched | 200 | fidelity | +0.097 | [+0.072, +0.136] | 3/3 |
| dep_aware-independent_matched | 200 | rank_stability | -0.012 | [-0.061, +0.048] | 1/3 |
| dep_aware-neighbors | 200 | fidelity | +0.209 | [+0.155, +0.269] | 3/3 |
| dep_aware-neighbors | 200 | rank_stability | +0.012 | [-0.024, +0.061] | 1/3 |
| dep_aware-abl_no_dependency | 200 | fidelity | +0.005 | [-0.021, +0.022] | 2/3 |
| dep_aware-abl_no_dependency | 200 | rank_stability | +0.016 | [-0.073, +0.109] | 2/3 |
| dep_aware-abl_no_locality | 200 | fidelity | -0.002 | [-0.005, +0.001] | 1/3 |
| dep_aware-abl_no_locality | 200 | rank_stability | +0.008 | [-0.012, +0.024] | 2/3 |
| dep_aware-independent | 500 | fidelity | +0.118 | [+0.108, +0.138] | 3/3 |
| dep_aware-independent | 500 | rank_stability | +0.012 | [-0.012, +0.061] | 1/3 |
| dep_aware-independent_matched | 500 | fidelity | +0.085 | [+0.072, +0.106] | 3/3 |
| dep_aware-independent_matched | 500 | rank_stability | +0.004 | [-0.048, +0.036] | 2/3 |
| dep_aware-neighbors | 500 | fidelity | +0.183 | [+0.116, +0.254] | 3/3 |
| dep_aware-neighbors | 500 | rank_stability | +0.016 | [-0.048, +0.073] | 2/3 |
| dep_aware-abl_no_dependency | 500 | fidelity | +0.007 | [+0.000, +0.012] | 3/3 |
| dep_aware-abl_no_dependency | 500 | rank_stability | -0.016 | [-0.048, +0.012] | 1/3 |
| dep_aware-abl_no_locality | 500 | fidelity | -0.003 | [-0.004, -0.002] | 0/3 |
| dep_aware-abl_no_locality | 500 | rank_stability | -0.024 | [-0.061, +0.000] | 0/3 |

### synthetic_indep / lr

| comparison | n | metric | diff mean | 95% CI | wins/n |
|---|---|---|---|---|---|
| dep_aware-independent | 200 | fidelity | +0.032 | [-0.005, +0.052] | 2/3 |
| dep_aware-independent | 200 | rank_stability | -0.008 | [-0.048, +0.024] | 1/3 |
| dep_aware-independent_matched | 200 | fidelity | +0.002 | [-0.013, +0.011] | 2/3 |
| dep_aware-independent_matched | 200 | rank_stability | +0.004 | [-0.036, +0.036] | 2/3 |
| dep_aware-neighbors | 200 | fidelity | +0.005 | [+0.003, +0.007] | 3/3 |
| dep_aware-neighbors | 200 | rank_stability | -0.016 | [-0.036, +0.012] | 1/3 |
| dep_aware-abl_no_dependency | 200 | fidelity | -0.004 | [-0.013, +0.003] | 1/3 |
| dep_aware-abl_no_dependency | 200 | rank_stability | +0.004 | [-0.024, +0.048] | 1/3 |
| dep_aware-abl_no_locality | 200 | fidelity | +0.000 | [-0.003, +0.002] | 2/3 |
| dep_aware-abl_no_locality | 200 | rank_stability | -0.008 | [-0.036, +0.012] | 1/3 |
| dep_aware-independent | 500 | fidelity | +0.018 | [-0.010, +0.032] | 2/3 |
| dep_aware-independent | 500 | rank_stability | -0.020 | [-0.048, +0.000] | 0/3 |
| dep_aware-independent_matched | 500 | fidelity | -0.002 | [-0.010, +0.003] | 2/3 |
| dep_aware-independent_matched | 500 | rank_stability | -0.012 | [-0.036, +0.012] | 1/3 |
| dep_aware-neighbors | 500 | fidelity | +0.007 | [+0.003, +0.011] | 3/3 |
| dep_aware-neighbors | 500 | rank_stability | +0.000 | [-0.036, +0.036] | 1/3 |
| dep_aware-abl_no_dependency | 500 | fidelity | -0.005 | [-0.015, +0.002] | 1/3 |
| dep_aware-abl_no_dependency | 500 | rank_stability | +0.000 | [-0.012, +0.012] | 1/3 |
| dep_aware-abl_no_locality | 500 | fidelity | -0.001 | [-0.005, +0.001] | 2/3 |
| dep_aware-abl_no_locality | 500 | rank_stability | +0.004 | [+0.000, +0.012] | 1/3 |

### synthetic_indep / rf

| comparison | n | metric | diff mean | 95% CI | wins/n |
|---|---|---|---|---|---|
| dep_aware-independent | 200 | fidelity | +0.093 | [+0.085, +0.097] | 3/3 |
| dep_aware-independent | 200 | rank_stability | +0.000 | [-0.012, +0.012] | 1/3 |
| dep_aware-independent_matched | 200 | fidelity | +0.043 | [+0.034, +0.052] | 3/3 |
| dep_aware-independent_matched | 200 | rank_stability | +0.053 | [+0.036, +0.073] | 3/3 |
| dep_aware-neighbors | 200 | fidelity | +0.061 | [+0.029, +0.117] | 3/3 |
| dep_aware-neighbors | 200 | rank_stability | +0.020 | [-0.036, +0.109] | 1/3 |
| dep_aware-abl_no_dependency | 200 | fidelity | +0.005 | [-0.005, +0.015] | 2/3 |
| dep_aware-abl_no_dependency | 200 | rank_stability | -0.004 | [-0.048, +0.036] | 1/3 |
| dep_aware-abl_no_locality | 200 | fidelity | +0.000 | [-0.001, +0.001] | 2/3 |
| dep_aware-abl_no_locality | 200 | rank_stability | +0.008 | [+0.000, +0.012] | 2/3 |
| dep_aware-independent | 500 | fidelity | +0.084 | [+0.075, +0.093] | 3/3 |
| dep_aware-independent | 500 | rank_stability | +0.024 | [-0.012, +0.061] | 2/3 |
| dep_aware-independent_matched | 500 | fidelity | +0.030 | [+0.019, +0.043] | 3/3 |
| dep_aware-independent_matched | 500 | rank_stability | +0.044 | [+0.000, +0.073] | 2/3 |
| dep_aware-neighbors | 500 | fidelity | +0.058 | [+0.022, +0.100] | 3/3 |
| dep_aware-neighbors | 500 | rank_stability | +0.057 | [+0.012, +0.109] | 3/3 |
| dep_aware-abl_no_dependency | 500 | fidelity | +0.001 | [-0.002, +0.007] | 1/3 |
| dep_aware-abl_no_dependency | 500 | rank_stability | +0.032 | [+0.000, +0.061] | 2/3 |
| dep_aware-abl_no_locality | 500 | fidelity | -0.000 | [-0.001, +0.001] | 1/3 |
| dep_aware-abl_no_locality | 500 | rank_stability | +0.008 | [-0.012, +0.036] | 1/3 |

### adult / lr

| comparison | n | metric | diff mean | 95% CI | wins/n |
|---|---|---|---|---|---|
| dep_aware-independent | 200 | fidelity | +0.411 | [+0.079, +0.671] | 3/3 |
| dep_aware-independent | 200 | rank_stability | +0.610 | [+0.463, +0.712] | 3/3 |
| dep_aware-independent_matched | 200 | fidelity | +0.308 | [-0.056, +0.704] | 2/3 |
| dep_aware-independent_matched | 200 | rank_stability | +0.453 | [+0.338, +0.561] | 3/3 |
| dep_aware-neighbors | 200 | fidelity | -0.004 | [-0.007, +0.002] | 1/3 |
| dep_aware-neighbors | 200 | rank_stability | -0.286 | [-0.353, -0.205] | 0/3 |
| dep_aware-abl_no_dependency | 200 | fidelity | +0.046 | [-0.061, +0.123] | 2/3 |
| dep_aware-abl_no_dependency | 200 | rank_stability | +0.485 | [+0.320, +0.605] | 3/3 |
| dep_aware-abl_no_locality | 200 | fidelity | +0.001 | [-0.000, +0.002] | 2/3 |
| dep_aware-abl_no_locality | 200 | rank_stability | +0.007 | [+0.001, +0.010] | 3/3 |
| dep_aware-independent | 500 | fidelity | +0.392 | [+0.048, +0.843] | 3/3 |
| dep_aware-independent | 500 | rank_stability | +0.812 | [+0.704, +0.900] | 3/3 |
| dep_aware-independent_matched | 500 | fidelity | +0.242 | [-0.073, +0.586] | 2/3 |
| dep_aware-independent_matched | 500 | rank_stability | +0.601 | [+0.412, +0.716] | 3/3 |
| dep_aware-neighbors | 500 | fidelity | +0.008 | [+0.001, +0.020] | 3/3 |
| dep_aware-neighbors | 500 | rank_stability | +0.063 | [-0.019, +0.218] | 1/3 |
| dep_aware-abl_no_dependency | 500 | fidelity | +0.072 | [-0.071, +0.174] | 2/3 |
| dep_aware-abl_no_dependency | 500 | rank_stability | +0.563 | [+0.425, +0.652] | 3/3 |
| dep_aware-abl_no_locality | 500 | fidelity | +0.000 | [-0.000, +0.001] | 2/3 |
| dep_aware-abl_no_locality | 500 | rank_stability | +0.004 | [+0.001, +0.008] | 3/3 |

### adult / rf

| comparison | n | metric | diff mean | 95% CI | wins/n |
|---|---|---|---|---|---|
| dep_aware-independent | 200 | fidelity | +1.222 | [+0.084, +2.910] | 3/3 |
| dep_aware-independent | 200 | rank_stability | +0.556 | [+0.181, +0.791] | 3/3 |
| dep_aware-independent_matched | 200 | fidelity | +0.184 | [-0.118, +0.551] | 2/3 |
| dep_aware-independent_matched | 200 | rank_stability | +0.389 | [+0.008, +0.691] | 3/3 |
| dep_aware-neighbors | 200 | fidelity | +0.094 | [+0.019, +0.229] | 3/3 |
| dep_aware-neighbors | 200 | rank_stability | -0.136 | [-0.248, +0.001] | 1/3 |
| dep_aware-abl_no_dependency | 200 | fidelity | +0.156 | [+0.142, +0.164] | 3/3 |
| dep_aware-abl_no_dependency | 200 | rank_stability | +0.559 | [+0.440, +0.713] | 3/3 |
| dep_aware-abl_no_locality | 200 | fidelity | +0.000 | [-0.000, +0.001] | 1/3 |
| dep_aware-abl_no_locality | 200 | rank_stability | +0.017 | [-0.004, +0.042] | 2/3 |
| dep_aware-independent | 500 | fidelity | +1.062 | [+0.134, +2.557] | 3/3 |
| dep_aware-independent | 500 | rank_stability | +0.725 | [+0.604, +0.878] | 3/3 |
| dep_aware-independent_matched | 500 | fidelity | +0.212 | [-0.073, +0.522] | 2/3 |
| dep_aware-independent_matched | 500 | rank_stability | +0.330 | [+0.238, +0.456] | 3/3 |
| dep_aware-neighbors | 500 | fidelity | +0.087 | [-0.032, +0.217] | 2/3 |
| dep_aware-neighbors | 500 | rank_stability | -0.058 | [-0.125, -0.018] | 0/3 |
| dep_aware-abl_no_dependency | 500 | fidelity | +0.209 | [+0.129, +0.297] | 3/3 |
| dep_aware-abl_no_dependency | 500 | rank_stability | +0.492 | [+0.369, +0.681] | 3/3 |
| dep_aware-abl_no_locality | 500 | fidelity | -0.001 | [-0.010, +0.006] | 2/3 |
| dep_aware-abl_no_locality | 500 | rank_stability | -0.012 | [-0.020, -0.005] | 0/3 |

**Control (synthetic_indep, dep_aware - independent fidelity):** lr n=200: +0.032 [-0.005, +0.052]; lr n=500: +0.018 [-0.010, +0.032]; rf n=200: +0.093 [+0.085, +0.097]; rf n=500: +0.084 [+0.075, +0.093]

## Confirmatory subset: cases NOT used in the pilot or the kernel-width sweep (synthetic: cases 31-100, Adult: 16-100)

| dataset | model | comparison | n | metric | diff mean | 95% CI | wins/n |
|---|---|---|---|---|---|---|---|

Cases dropped from paired comparisons (non-finite on either side): none

## Five lowest-fidelity cases per budget (per-case seed means)

| dataset | model | condition | n | case | fidelity | fit_r2 | prediction | mean_nn_dist | frac_seen_combo | mean_dist_to_query |
|---|---|---|---|---|---|---|---|---|---|---|
| synthetic_dep | lr | independent | 200 | 38 | 0.823 | 0.884 | 0.675 | 1.998 | 1.000 | 3.093 |
| synthetic_dep | lr | independent | 200 | 6 | 0.825 | 0.874 | 0.725 | 2.208 | 1.000 | 3.093 |
| synthetic_dep | lr | independent | 200 | 64 | 0.827 | 0.854 | 0.303 | 2.304 | 1.000 | 3.093 |
| synthetic_dep | lr | independent | 500 | 64 | 0.826 | 0.865 | 0.303 | 2.299 | 1.000 | 3.077 |
| synthetic_dep | lr | independent | 500 | 38 | 0.855 | 0.884 | 0.675 | 1.994 | 1.000 | 3.077 |
| synthetic_dep | lr | independent | 500 | 6 | 0.859 | 0.874 | 0.725 | 2.184 | 1.000 | 3.077 |
| synthetic_dep | lr | dep_aware | 200 | 64 | 0.878 | 0.924 | 0.303 | 0.978 | 1.000 | 2.740 |
| synthetic_dep | lr | dep_aware | 200 | 38 | 0.893 | 0.923 | 0.675 | 0.944 | 1.000 | 2.384 |
| synthetic_dep | lr | dep_aware | 200 | 6 | 0.938 | 0.955 | 0.725 | 0.981 | 1.000 | 2.636 |
| synthetic_dep | lr | dep_aware | 500 | 64 | 0.883 | 0.923 | 0.303 | 0.977 | 1.000 | 2.719 |
| synthetic_dep | lr | dep_aware | 500 | 38 | 0.895 | 0.913 | 0.675 | 0.937 | 1.000 | 2.383 |
| synthetic_dep | lr | dep_aware | 500 | 6 | 0.944 | 0.956 | 0.725 | 0.972 | 1.000 | 2.618 |
| synthetic_dep | rf | independent | 200 | 38 | 0.650 | 0.773 | 0.851 | 1.998 | 1.000 | 3.093 |
| synthetic_dep | rf | independent | 200 | 64 | 0.667 | 0.821 | 0.301 | 2.304 | 1.000 | 3.093 |
| synthetic_dep | rf | independent | 200 | 6 | 0.692 | 0.810 | 0.653 | 2.208 | 1.000 | 3.093 |
| synthetic_dep | rf | independent | 500 | 38 | 0.671 | 0.785 | 0.851 | 1.994 | 1.000 | 3.077 |
| synthetic_dep | rf | independent | 500 | 64 | 0.680 | 0.824 | 0.301 | 2.299 | 1.000 | 3.077 |
| synthetic_dep | rf | independent | 500 | 6 | 0.701 | 0.814 | 0.653 | 2.184 | 1.000 | 3.077 |
| synthetic_dep | rf | dep_aware | 200 | 64 | 0.769 | 0.831 | 0.301 | 0.978 | 1.000 | 2.740 |
| synthetic_dep | rf | dep_aware | 200 | 38 | 0.783 | 0.796 | 0.851 | 0.944 | 1.000 | 2.384 |
| synthetic_dep | rf | dep_aware | 200 | 6 | 0.833 | 0.855 | 0.653 | 0.981 | 1.000 | 2.636 |
| synthetic_dep | rf | dep_aware | 500 | 38 | 0.781 | 0.745 | 0.851 | 0.937 | 1.000 | 2.383 |
| synthetic_dep | rf | dep_aware | 500 | 64 | 0.788 | 0.824 | 0.301 | 0.977 | 1.000 | 2.719 |
| synthetic_dep | rf | dep_aware | 500 | 6 | 0.839 | 0.850 | 0.653 | 0.972 | 1.000 | 2.618 |
| synthetic_indep | lr | independent | 200 | 20 | 0.875 | 0.886 | 0.693 | 1.826 | 1.000 | 3.093 |
| synthetic_indep | lr | independent | 200 | 24 | 0.880 | 0.890 | 0.651 | 1.805 | 1.000 | 3.093 |
| synthetic_indep | lr | independent | 200 | 33 | 0.888 | 0.877 | 0.403 | 2.115 | 1.000 | 3.093 |
| synthetic_indep | lr | independent | 500 | 33 | 0.897 | 0.883 | 0.403 | 2.115 | 1.000 | 3.077 |
| synthetic_indep | lr | independent | 500 | 24 | 0.901 | 0.889 | 0.651 | 1.790 | 1.000 | 3.077 |
| synthetic_indep | lr | independent | 500 | 20 | 0.902 | 0.885 | 0.693 | 1.826 | 1.000 | 3.077 |
| synthetic_indep | lr | dep_aware | 200 | 33 | 0.883 | 0.936 | 0.403 | 0.963 | 1.000 | 2.509 |
| synthetic_indep | lr | dep_aware | 200 | 20 | 0.927 | 0.920 | 0.693 | 0.904 | 1.000 | 2.242 |
| synthetic_indep | lr | dep_aware | 200 | 24 | 0.928 | 0.933 | 0.651 | 0.927 | 1.000 | 2.257 |
| synthetic_indep | lr | dep_aware | 500 | 33 | 0.887 | 0.930 | 0.403 | 0.963 | 1.000 | 2.524 |
| synthetic_indep | lr | dep_aware | 500 | 24 | 0.933 | 0.933 | 0.651 | 0.926 | 1.000 | 2.244 |
| synthetic_indep | lr | dep_aware | 500 | 20 | 0.934 | 0.924 | 0.693 | 0.900 | 1.000 | 2.209 |
| synthetic_indep | rf | independent | 200 | 33 | 0.778 | 0.853 | 0.499 | 2.115 | 1.000 | 3.093 |
| synthetic_indep | rf | independent | 200 | 20 | 0.788 | 0.845 | 0.688 | 1.826 | 1.000 | 3.093 |
| synthetic_indep | rf | independent | 200 | 24 | 0.792 | 0.870 | 0.608 | 1.805 | 1.000 | 3.093 |
| synthetic_indep | rf | independent | 500 | 33 | 0.789 | 0.849 | 0.499 | 2.115 | 1.000 | 3.077 |
| synthetic_indep | rf | independent | 500 | 20 | 0.803 | 0.854 | 0.688 | 1.826 | 1.000 | 3.077 |
| synthetic_indep | rf | independent | 500 | 24 | 0.810 | 0.858 | 0.608 | 1.790 | 1.000 | 3.077 |
| synthetic_indep | rf | dep_aware | 200 | 33 | 0.874 | 0.878 | 0.499 | 0.963 | 1.000 | 2.509 |
| synthetic_indep | rf | dep_aware | 200 | 24 | 0.878 | 0.888 | 0.608 | 0.927 | 1.000 | 2.257 |
| synthetic_indep | rf | dep_aware | 200 | 20 | 0.886 | 0.866 | 0.688 | 0.904 | 1.000 | 2.242 |
| synthetic_indep | rf | dep_aware | 500 | 33 | 0.882 | 0.876 | 0.499 | 0.963 | 1.000 | 2.524 |
| synthetic_indep | rf | dep_aware | 500 | 24 | 0.884 | 0.880 | 0.608 | 0.926 | 1.000 | 2.244 |
| synthetic_indep | rf | dep_aware | 500 | 20 | 0.886 | 0.886 | 0.688 | 0.900 | 1.000 | 2.209 |
| adult | lr | independent | 200 | 128 | 0.180 | 0.815 | 0.331 | 2.523 | 0.240 | 3.984 |
| adult | lr | independent | 200 | 664 | 0.448 | 0.762 | 0.200 | 2.580 | 0.240 | 3.605 |
| adult | lr | independent | 200 | 807 | 0.792 | 0.931 | 0.820 | 2.660 | 0.240 | 3.595 |
| adult | lr | independent | 500 | 128 | 0.058 | 0.803 | 0.331 | 2.483 | 0.249 | 3.981 |
| adult | lr | independent | 500 | 664 | 0.655 | 0.738 | 0.200 | 2.571 | 0.249 | 3.599 |
| adult | lr | independent | 500 | 807 | 0.831 | 0.908 | 0.820 | 2.669 | 0.249 | 3.572 |
| adult | lr | dep_aware | 200 | 128 | 0.851 | 0.989 | 0.331 | 0.314 | 1.000 | 2.317 |
| adult | lr | dep_aware | 200 | 807 | 0.871 | 0.987 | 0.820 | 0.462 | 1.000 | 2.129 |
| adult | lr | dep_aware | 200 | 664 | 0.931 | 0.989 | 0.200 | 0.369 | 1.000 | 2.091 |
| adult | lr | dep_aware | 500 | 807 | 0.880 | 0.985 | 0.820 | 0.461 | 1.000 | 2.125 |
| adult | lr | dep_aware | 500 | 128 | 0.901 | 0.988 | 0.331 | 0.307 | 1.000 | 2.307 |
| adult | lr | dep_aware | 500 | 664 | 0.939 | 0.986 | 0.200 | 0.385 | 1.000 | 2.081 |
| adult | rf | independent | 200 | 128 | -2.561 | 0.695 | 0.162 | 2.523 | 0.240 | 3.984 |
| adult | rf | independent | 200 | 664 | -0.062 | 0.671 | 0.052 | 2.580 | 0.240 | 3.605 |
| adult | rf | independent | 200 | 807 | 0.468 | 0.749 | 0.942 | 2.660 | 0.240 | 3.595 |
| adult | rf | independent | 500 | 128 | -2.127 | 0.648 | 0.162 | 2.483 | 0.249 | 3.981 |
| adult | rf | independent | 500 | 664 | 0.103 | 0.601 | 0.052 | 2.571 | 0.249 | 3.599 |
| adult | rf | independent | 500 | 807 | 0.509 | 0.704 | 0.942 | 2.669 | 0.249 | 3.572 |
| adult | rf | dep_aware | 200 | 128 | 0.349 | 0.750 | 0.162 | 0.314 | 1.000 | 2.317 |
| adult | rf | dep_aware | 200 | 807 | 0.552 | 0.748 | 0.942 | 0.462 | 1.000 | 2.129 |
| adult | rf | dep_aware | 200 | 664 | 0.612 | 0.769 | 0.052 | 0.369 | 1.000 | 2.091 |
| adult | rf | dep_aware | 500 | 128 | 0.429 | 0.689 | 0.162 | 0.307 | 1.000 | 2.307 |
| adult | rf | dep_aware | 500 | 664 | 0.600 | 0.747 | 0.052 | 0.385 | 1.000 | 2.081 |
| adult | rf | dep_aware | 500 | 807 | 0.643 | 0.645 | 0.942 | 0.461 | 1.000 | 2.125 |

Total explanations: 432; non-finite fidelity values: 0; non-finite per-case rank stability values: 0; total wall time: 0.7 min.
