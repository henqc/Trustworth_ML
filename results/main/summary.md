# Main grid summary

Fidelity: per case, the mean over its finite seeds; then mean +- sd, median and [q1, q3] over cases (validity and runtime columns: per-case seed mean, then mean over cases). Rank stability: per case, the mean pairwise Spearman of |coef| across seeds; then mean +- sd over cases with a finite value.

## By condition

### synthetic_dep / lr

| condition | n | fidelity mean ± sd | median [q1, q3] | rank stability | mean_nn_dist | frac_seen_combo | mean_dist_to_query | runtime ms |
|---|---|---|---|---|---|---|---|---|
| independent | 200 | 0.790 ± 0.105 | 0.838 [0.788, 0.853] | 0.953 ± 0.027 | 2.124 | 1.000 | 3.079 | 3.1 |
| independent | 500 | 0.796 ± 0.100 | 0.840 [0.786, 0.859] | 0.966 ± 0.010 | 2.127 | 1.000 | 3.078 | 3.1 |
| independent_matched | 200 | 0.813 ± 0.169 | 0.882 [0.817, 0.907] | 0.952 ± 0.029 | 1.813 | 1.000 | 2.309 | 3.2 |
| independent_matched | 500 | 0.821 ± 0.165 | 0.888 [0.829, 0.913] | 0.966 ± 0.008 | 1.815 | 1.000 | 2.309 | 3.2 |
| neighbors | 200 | 0.909 ± 0.042 | 0.918 [0.889, 0.940] | 0.973 ± 0.011 | 0.000 | 1.000 | 2.400 | 2.9 |
| neighbors | 500 | 0.912 ± 0.041 | 0.921 [0.891, 0.942] | 0.981 ± 0.009 | 0.000 | 1.000 | 2.396 | 2.8 |
| dep_aware | 200 | 0.912 ± 0.039 | 0.920 [0.893, 0.942] | 0.970 ± 0.009 | 0.950 | 1.000 | 2.541 | 3.5 |
| dep_aware | 500 | 0.916 ± 0.038 | 0.924 [0.899, 0.946] | 0.975 ± 0.008 | 0.947 | 1.000 | 2.531 | 3.5 |
| abl_no_dependency | 200 | 0.884 ± 0.040 | 0.895 [0.868, 0.913] | 0.966 ± 0.010 | 1.462 | 1.000 | 2.774 | 3.6 |
| abl_no_dependency | 500 | 0.890 ± 0.038 | 0.900 [0.873, 0.917] | 0.970 ± 0.006 | 1.461 | 1.000 | 2.777 | 3.8 |
| abl_no_locality | 200 | 0.913 ± 0.038 | 0.921 [0.893, 0.941] | 0.970 ± 0.008 | 0.950 | 1.000 | 2.541 | 3.5 |
| abl_no_locality | 500 | 0.916 ± 0.037 | 0.923 [0.900, 0.945] | 0.976 ± 0.008 | 0.947 | 1.000 | 2.531 | 3.8 |

### synthetic_dep / rf

| condition | n | fidelity mean ± sd | median [q1, q3] | rank stability | mean_nn_dist | frac_seen_combo | mean_dist_to_query | runtime ms |
|---|---|---|---|---|---|---|---|---|
| independent | 200 | 0.626 ± 0.081 | 0.639 [0.589, 0.682] | 0.928 ± 0.030 | 2.124 | 1.000 | 3.079 | 29.6 |
| independent | 500 | 0.633 ± 0.082 | 0.640 [0.598, 0.692] | 0.958 ± 0.017 | 2.127 | 1.000 | 3.078 | 29.9 |
| independent_matched | 200 | 0.637 ± 0.156 | 0.680 [0.592, 0.739] | 0.927 ± 0.032 | 1.813 | 1.000 | 2.309 | 30.0 |
| independent_matched | 500 | 0.644 ± 0.156 | 0.687 [0.596, 0.737] | 0.955 ± 0.024 | 1.815 | 1.000 | 2.309 | 30.2 |
| neighbors | 200 | 0.633 ± 0.080 | 0.647 [0.606, 0.687] | 0.889 ± 0.040 | 0.000 | 1.000 | 2.400 | 29.6 |
| neighbors | 500 | 0.669 ± 0.078 | 0.679 [0.637, 0.722] | 0.938 ± 0.026 | 0.000 | 1.000 | 2.396 | 29.6 |
| dep_aware | 200 | 0.791 ± 0.044 | 0.796 [0.767, 0.822] | 0.941 ± 0.027 | 0.950 | 1.000 | 2.541 | 30.2 |
| dep_aware | 500 | 0.797 ± 0.044 | 0.801 [0.776, 0.828] | 0.964 ± 0.018 | 0.947 | 1.000 | 2.531 | 30.4 |
| abl_no_dependency | 200 | 0.774 ± 0.038 | 0.777 [0.752, 0.796] | 0.942 ± 0.022 | 1.462 | 1.000 | 2.774 | 30.4 |
| abl_no_dependency | 500 | 0.780 ± 0.037 | 0.784 [0.759, 0.803] | 0.963 ± 0.018 | 1.461 | 1.000 | 2.777 | 30.7 |
| abl_no_locality | 200 | 0.794 ± 0.042 | 0.798 [0.769, 0.823] | 0.940 ± 0.024 | 0.950 | 1.000 | 2.541 | 30.2 |
| abl_no_locality | 500 | 0.800 ± 0.041 | 0.803 [0.780, 0.828] | 0.964 ± 0.017 | 0.947 | 1.000 | 2.531 | 31.0 |

### synthetic_indep / lr

| condition | n | fidelity mean ± sd | median [q1, q3] | rank stability | mean_nn_dist | frac_seen_combo | mean_dist_to_query | runtime ms |
|---|---|---|---|---|---|---|---|---|
| independent | 200 | 0.730 ± 0.215 | 0.824 [0.620, 0.885] | 0.939 ± 0.044 | 2.158 | 1.000 | 3.079 | 3.0 |
| independent | 500 | 0.738 ± 0.213 | 0.832 [0.650, 0.891] | 0.959 ± 0.025 | 2.160 | 1.000 | 3.078 | 3.1 |
| independent_matched | 200 | 0.685 ± 0.302 | 0.835 [0.546, 0.898] | 0.930 ± 0.056 | 1.864 | 1.000 | 2.309 | 3.0 |
| independent_matched | 500 | 0.694 ± 0.303 | 0.849 [0.565, 0.906] | 0.957 ± 0.026 | 1.865 | 1.000 | 2.309 | 3.1 |
| neighbors | 200 | 0.832 ± 0.104 | 0.863 [0.798, 0.897] | 0.956 ± 0.030 | 0.000 | 1.000 | 2.502 | 3.1 |
| neighbors | 500 | 0.836 ± 0.105 | 0.869 [0.803, 0.901] | 0.971 ± 0.022 | 0.000 | 1.000 | 2.498 | 2.8 |
| dep_aware | 200 | 0.845 ± 0.100 | 0.879 [0.801, 0.907] | 0.957 ± 0.021 | 0.981 | 1.000 | 2.642 | 3.6 |
| dep_aware | 500 | 0.849 ± 0.097 | 0.883 [0.807, 0.910] | 0.969 ± 0.016 | 0.978 | 1.000 | 2.633 | 3.6 |
| abl_no_dependency | 200 | 0.847 ± 0.092 | 0.886 [0.809, 0.907] | 0.957 ± 0.024 | 1.472 | 1.000 | 2.855 | 3.6 |
| abl_no_dependency | 500 | 0.853 ± 0.088 | 0.893 [0.808, 0.909] | 0.969 ± 0.008 | 1.473 | 1.000 | 2.858 | 3.9 |
| abl_no_locality | 200 | 0.848 ± 0.094 | 0.883 [0.806, 0.907] | 0.956 ± 0.021 | 0.981 | 1.000 | 2.642 | 4.3 |
| abl_no_locality | 500 | 0.853 ± 0.091 | 0.885 [0.813, 0.911] | 0.968 ± 0.018 | 0.978 | 1.000 | 2.633 | 4.0 |

### synthetic_indep / rf

| condition | n | fidelity mean ± sd | median [q1, q3] | rank stability | mean_nn_dist | frac_seen_combo | mean_dist_to_query | runtime ms |
|---|---|---|---|---|---|---|---|---|
| independent | 200 | 0.668 ± 0.144 | 0.711 [0.603, 0.768] | 0.905 ± 0.047 | 2.158 | 1.000 | 3.079 | 30.1 |
| independent | 500 | 0.674 ± 0.145 | 0.727 [0.611, 0.780] | 0.942 ± 0.039 | 2.160 | 1.000 | 3.078 | 29.5 |
| independent_matched | 200 | 0.638 ± 0.247 | 0.728 [0.528, 0.818] | 0.900 ± 0.065 | 1.864 | 1.000 | 2.309 | 29.4 |
| independent_matched | 500 | 0.645 ± 0.251 | 0.743 [0.517, 0.825] | 0.940 ± 0.039 | 1.865 | 1.000 | 2.309 | 29.8 |
| neighbors | 200 | 0.716 ± 0.114 | 0.754 [0.694, 0.779] | 0.848 ± 0.083 | 0.000 | 1.000 | 2.502 | 29.2 |
| neighbors | 500 | 0.739 ± 0.114 | 0.775 [0.715, 0.805] | 0.915 ± 0.052 | 0.000 | 1.000 | 2.498 | 30.2 |
| dep_aware | 200 | 0.814 ± 0.087 | 0.847 [0.779, 0.865] | 0.930 ± 0.032 | 0.981 | 1.000 | 2.642 | 31.0 |
| dep_aware | 500 | 0.820 ± 0.086 | 0.853 [0.782, 0.873] | 0.956 ± 0.026 | 0.978 | 1.000 | 2.633 | 30.8 |
| abl_no_dependency | 200 | 0.815 ± 0.078 | 0.844 [0.782, 0.867] | 0.936 ± 0.030 | 1.472 | 1.000 | 2.855 | 30.0 |
| abl_no_dependency | 500 | 0.821 ± 0.074 | 0.848 [0.784, 0.868] | 0.960 ± 0.020 | 1.473 | 1.000 | 2.858 | 30.1 |
| abl_no_locality | 200 | 0.817 ± 0.082 | 0.848 [0.784, 0.867] | 0.929 ± 0.036 | 0.981 | 1.000 | 2.642 | 30.1 |
| abl_no_locality | 500 | 0.824 ± 0.079 | 0.855 [0.788, 0.874] | 0.956 ± 0.026 | 0.978 | 1.000 | 2.633 | 30.3 |

### adult / lr

| condition | n | fidelity mean ± sd | median [q1, q3] | rank stability | mean_nn_dist | frac_seen_combo | mean_dist_to_query | runtime ms |
|---|---|---|---|---|---|---|---|---|
| independent | 200 | -24.432 ± 125.829 | -0.026 [-1.850, 0.495] | 0.201 ± 0.050 | 2.578 | 0.242 | 3.814 | 9.3 |
| independent | 500 | -13.583 ± 70.627 | 0.268 [-0.936, 0.644] | 0.183 ± 0.046 | 2.570 | 0.238 | 3.807 | 9.5 |
| independent_matched | 200 | -4.282 ± 23.398 | 0.546 [-0.031, 0.764] | 0.313 ± 0.060 | 1.964 | 0.242 | 3.006 | 9.5 |
| independent_matched | 500 | -3.891 ± 23.088 | 0.677 [0.252, 0.812] | 0.350 ± 0.095 | 1.965 | 0.238 | 3.001 | 9.6 |
| neighbors | 200 | 0.658 ± 0.588 | 0.814 [0.558, 0.896] | 0.672 ± 0.138 | 0.000 | 1.000 | 2.130 | 12.9 |
| neighbors | 500 | 0.706 ± 0.428 | 0.859 [0.608, 0.911] | 0.876 ± 0.092 | 0.000 | 1.000 | 2.126 | 13.6 |
| dep_aware | 200 | 0.680 ± 0.437 | 0.826 [0.569, 0.896] | 0.669 ± 0.138 | 0.327 | 1.000 | 2.172 | 17.4 |
| dep_aware | 500 | 0.670 ± 0.729 | 0.856 [0.612, 0.910] | 0.861 ± 0.090 | 0.328 | 1.000 | 2.165 | 20.7 |
| abl_no_dependency | 200 | -50.081 ± 268.913 | 0.683 [-1.625, 0.845] | 0.366 ± 0.075 | 1.967 | 0.261 | 3.357 | 13.4 |
| abl_no_dependency | 500 | -33.708 ± 185.820 | 0.741 [-0.874, 0.884] | 0.362 ± 0.080 | 1.981 | 0.244 | 3.367 | 14.7 |
| abl_no_locality | 200 | 0.680 ± 0.438 | 0.828 [0.570, 0.893] | 0.665 ± 0.138 | 0.327 | 1.000 | 2.172 | 17.4 |
| abl_no_locality | 500 | 0.671 ± 0.730 | 0.857 [0.606, 0.909] | 0.858 ± 0.091 | 0.328 | 1.000 | 2.165 | 20.8 |

### adult / rf

| condition | n | fidelity mean ± sd | median [q1, q3] | rank stability | mean_nn_dist | frac_seen_combo | mean_dist_to_query | runtime ms |
|---|---|---|---|---|---|---|---|---|
| independent | 200 | -22.596 ± 117.454 | -0.452 [-3.547, 0.194] | 0.177 ± 0.026 | 2.578 | 0.242 | 3.814 | 35.2 |
| independent | 500 | -16.276 ± 78.570 | -0.305 [-3.115, 0.315] | 0.164 ± 0.033 | 2.570 | 0.238 | 3.807 | 37.1 |
| independent_matched | 200 | -1.497 ± 8.219 | 0.275 [-0.233, 0.502] | 0.381 ± 0.049 | 1.964 | 0.242 | 3.006 | 35.5 |
| independent_matched | 500 | -1.074 ± 6.841 | 0.290 [-0.027, 0.517] | 0.453 ± 0.059 | 1.965 | 0.238 | 3.001 | 37.3 |
| neighbors | 200 | 0.440 ± 0.254 | 0.447 [0.258, 0.644] | 0.566 ± 0.146 | 0.000 | 1.000 | 2.130 | 39.2 |
| neighbors | 500 | 0.483 ± 0.251 | 0.504 [0.341, 0.706] | 0.803 ± 0.103 | 0.000 | 1.000 | 2.126 | 39.2 |
| dep_aware | 200 | 0.498 ± 0.250 | 0.526 [0.360, 0.695] | 0.532 ± 0.164 | 0.327 | 1.000 | 2.172 | 45.0 |
| dep_aware | 500 | 0.537 ± 0.249 | 0.571 [0.397, 0.727] | 0.747 ± 0.114 | 0.328 | 1.000 | 2.165 | 48.2 |
| abl_no_dependency | 200 | -9.407 ± 53.595 | 0.287 [-0.800, 0.487] | 0.276 ± 0.049 | 1.967 | 0.261 | 3.357 | 40.0 |
| abl_no_dependency | 500 | -4.683 ± 26.327 | 0.393 [-0.433, 0.576] | 0.291 ± 0.035 | 1.981 | 0.244 | 3.367 | 42.4 |
| abl_no_locality | 200 | 0.497 ± 0.254 | 0.529 [0.357, 0.694] | 0.527 ± 0.160 | 0.327 | 1.000 | 2.172 | 44.3 |
| abl_no_locality | 500 | 0.537 ± 0.250 | 0.574 [0.400, 0.728] | 0.741 ± 0.114 | 0.328 | 1.000 | 2.165 | 48.0 |

## Paired comparisons (dep_aware minus baseline, per case; percentile bootstrap 95% CI, 2,000 resamples)

### synthetic_dep / lr

| comparison | n | metric | diff mean | 95% CI | wins/n |
|---|---|---|---|---|---|
| dep_aware-independent | 200 | fidelity | +0.123 | [+0.109, +0.137] | 100/100 |
| dep_aware-independent | 200 | rank_stability | +0.016 | [+0.011, +0.021] | 86/100 |
| dep_aware-independent_matched | 200 | fidelity | +0.099 | [+0.074, +0.126] | 99/100 |
| dep_aware-independent_matched | 200 | rank_stability | +0.018 | [+0.012, +0.023] | 79/100 |
| dep_aware-neighbors | 200 | fidelity | +0.004 | [+0.002, +0.005] | 74/100 |
| dep_aware-neighbors | 200 | rank_stability | -0.004 | [-0.006, -0.002] | 36/100 |
| dep_aware-abl_no_dependency | 200 | fidelity | +0.029 | [+0.026, +0.031] | 96/100 |
| dep_aware-abl_no_dependency | 200 | rank_stability | +0.004 | [+0.001, +0.006] | 59/100 |
| dep_aware-abl_no_locality | 200 | fidelity | -0.000 | [-0.001, +0.000] | 54/100 |
| dep_aware-abl_no_locality | 200 | rank_stability | -0.000 | [-0.001, +0.001] | 38/100 |
| dep_aware-independent | 500 | fidelity | +0.120 | [+0.106, +0.134] | 100/100 |
| dep_aware-independent | 500 | rank_stability | +0.009 | [+0.007, +0.012] | 77/100 |
| dep_aware-independent_matched | 500 | fidelity | +0.095 | [+0.070, +0.121] | 98/100 |
| dep_aware-independent_matched | 500 | rank_stability | +0.010 | [+0.007, +0.012] | 81/100 |
| dep_aware-neighbors | 500 | fidelity | +0.004 | [+0.003, +0.005] | 82/100 |
| dep_aware-neighbors | 500 | rank_stability | -0.005 | [-0.007, -0.003] | 22/100 |
| dep_aware-abl_no_dependency | 500 | fidelity | +0.026 | [+0.023, +0.028] | 98/100 |
| dep_aware-abl_no_dependency | 500 | rank_stability | +0.005 | [+0.004, +0.007] | 66/100 |
| dep_aware-abl_no_locality | 500 | fidelity | -0.001 | [-0.001, -0.000] | 46/100 |
| dep_aware-abl_no_locality | 500 | rank_stability | -0.000 | [-0.001, +0.000] | 31/100 |

### synthetic_dep / rf

| comparison | n | metric | diff mean | 95% CI | wins/n |
|---|---|---|---|---|---|
| dep_aware-independent | 200 | fidelity | +0.165 | [+0.154, +0.176] | 100/100 |
| dep_aware-independent | 200 | rank_stability | +0.013 | [+0.007, +0.019] | 62/100 |
| dep_aware-independent_matched | 200 | fidelity | +0.153 | [+0.130, +0.179] | 100/100 |
| dep_aware-independent_matched | 200 | rank_stability | +0.014 | [+0.008, +0.021] | 69/100 |
| dep_aware-neighbors | 200 | fidelity | +0.157 | [+0.147, +0.169] | 100/100 |
| dep_aware-neighbors | 200 | rank_stability | +0.052 | [+0.042, +0.062] | 87/100 |
| dep_aware-abl_no_dependency | 200 | fidelity | +0.017 | [+0.013, +0.019] | 91/100 |
| dep_aware-abl_no_dependency | 200 | rank_stability | -0.000 | [-0.005, +0.004] | 50/100 |
| dep_aware-abl_no_locality | 200 | fidelity | -0.003 | [-0.003, -0.002] | 25/100 |
| dep_aware-abl_no_locality | 200 | rank_stability | +0.001 | [-0.001, +0.003] | 52/100 |
| dep_aware-independent | 500 | fidelity | +0.164 | [+0.153, +0.176] | 100/100 |
| dep_aware-independent | 500 | rank_stability | +0.006 | [+0.001, +0.011] | 59/100 |
| dep_aware-independent_matched | 500 | fidelity | +0.153 | [+0.130, +0.179] | 100/100 |
| dep_aware-independent_matched | 500 | rank_stability | +0.009 | [+0.004, +0.015] | 62/100 |
| dep_aware-neighbors | 500 | fidelity | +0.128 | [+0.118, +0.138] | 100/100 |
| dep_aware-neighbors | 500 | rank_stability | +0.026 | [+0.020, +0.031] | 82/100 |
| dep_aware-abl_no_dependency | 500 | fidelity | +0.016 | [+0.013, +0.019] | 89/100 |
| dep_aware-abl_no_dependency | 500 | rank_stability | +0.001 | [-0.003, +0.005] | 50/100 |
| dep_aware-abl_no_locality | 500 | fidelity | -0.003 | [-0.004, -0.002] | 16/100 |
| dep_aware-abl_no_locality | 500 | rank_stability | -0.000 | [-0.002, +0.001] | 47/100 |

### synthetic_indep / lr

| comparison | n | metric | diff mean | 95% CI | wins/n |
|---|---|---|---|---|---|
| dep_aware-independent | 200 | fidelity | +0.115 | [+0.092, +0.139] | 96/100 |
| dep_aware-independent | 200 | rank_stability | +0.018 | [+0.012, +0.025] | 67/100 |
| dep_aware-independent_matched | 200 | fidelity | +0.159 | [+0.120, +0.201] | 89/100 |
| dep_aware-independent_matched | 200 | rank_stability | +0.027 | [+0.019, +0.036] | 72/100 |
| dep_aware-neighbors | 200 | fidelity | +0.013 | [+0.010, +0.016] | 89/100 |
| dep_aware-neighbors | 200 | rank_stability | +0.002 | [-0.003, +0.006] | 43/100 |
| dep_aware-abl_no_dependency | 200 | fidelity | -0.002 | [-0.006, +0.001] | 47/100 |
| dep_aware-abl_no_dependency | 200 | rank_stability | +0.000 | [-0.004, +0.004] | 45/100 |
| dep_aware-abl_no_locality | 200 | fidelity | -0.003 | [-0.004, -0.002] | 25/100 |
| dep_aware-abl_no_locality | 200 | rank_stability | +0.001 | [-0.001, +0.003] | 53/100 |
| dep_aware-independent | 500 | fidelity | +0.111 | [+0.088, +0.136] | 94/100 |
| dep_aware-independent | 500 | rank_stability | +0.010 | [+0.006, +0.015] | 71/100 |
| dep_aware-independent_matched | 500 | fidelity | +0.155 | [+0.116, +0.199] | 78/100 |
| dep_aware-independent_matched | 500 | rank_stability | +0.011 | [+0.007, +0.017] | 78/100 |
| dep_aware-neighbors | 500 | fidelity | +0.013 | [+0.010, +0.015] | 95/100 |
| dep_aware-neighbors | 500 | rank_stability | -0.002 | [-0.005, +0.001] | 36/100 |
| dep_aware-abl_no_dependency | 500 | fidelity | -0.004 | [-0.007, -0.001] | 35/100 |
| dep_aware-abl_no_dependency | 500 | rank_stability | -0.001 | [-0.004, +0.002] | 56/100 |
| dep_aware-abl_no_locality | 500 | fidelity | -0.004 | [-0.005, -0.003] | 16/100 |
| dep_aware-abl_no_locality | 500 | rank_stability | +0.001 | [-0.001, +0.002] | 37/100 |

### synthetic_indep / rf

| comparison | n | metric | diff mean | 95% CI | wins/n |
|---|---|---|---|---|---|
| dep_aware-independent | 200 | fidelity | +0.146 | [+0.131, +0.163] | 100/100 |
| dep_aware-independent | 200 | rank_stability | +0.024 | [+0.016, +0.032] | 75/100 |
| dep_aware-independent_matched | 200 | fidelity | +0.175 | [+0.141, +0.211] | 99/100 |
| dep_aware-independent_matched | 200 | rank_stability | +0.030 | [+0.018, +0.041] | 70/100 |
| dep_aware-neighbors | 200 | fidelity | +0.097 | [+0.088, +0.107] | 100/100 |
| dep_aware-neighbors | 200 | rank_stability | +0.082 | [+0.068, +0.097] | 92/100 |
| dep_aware-abl_no_dependency | 200 | fidelity | -0.001 | [-0.005, +0.002] | 48/100 |
| dep_aware-abl_no_dependency | 200 | rank_stability | -0.006 | [-0.012, +0.000] | 43/100 |
| dep_aware-abl_no_locality | 200 | fidelity | -0.004 | [-0.005, -0.002] | 18/100 |
| dep_aware-abl_no_locality | 200 | rank_stability | +0.001 | [-0.002, +0.003] | 49/100 |
| dep_aware-independent | 500 | fidelity | +0.145 | [+0.129, +0.163] | 100/100 |
| dep_aware-independent | 500 | rank_stability | +0.014 | [+0.007, +0.021] | 68/100 |
| dep_aware-independent_matched | 500 | fidelity | +0.175 | [+0.140, +0.211] | 98/100 |
| dep_aware-independent_matched | 500 | rank_stability | +0.016 | [+0.008, +0.024] | 65/100 |
| dep_aware-neighbors | 500 | fidelity | +0.080 | [+0.071, +0.091] | 98/100 |
| dep_aware-neighbors | 500 | rank_stability | +0.040 | [+0.032, +0.049] | 82/100 |
| dep_aware-abl_no_dependency | 500 | fidelity | -0.002 | [-0.005, +0.002] | 53/100 |
| dep_aware-abl_no_dependency | 500 | rank_stability | -0.005 | [-0.009, -0.000] | 40/100 |
| dep_aware-abl_no_locality | 500 | fidelity | -0.004 | [-0.006, -0.003] | 14/100 |
| dep_aware-abl_no_locality | 500 | rank_stability | -0.000 | [-0.002, +0.001] | 37/100 |

### adult / lr

| comparison | n | metric | diff mean | 95% CI | wins/n |
|---|---|---|---|---|---|
| dep_aware-independent | 200 | fidelity | +25.113 | [+5.385, +53.577] | 99/100 |
| dep_aware-independent | 200 | rank_stability | +0.468 | [+0.443, +0.494] | 100/100 |
| dep_aware-independent_matched | 200 | fidelity | +4.962 | [+1.271, +10.043] | 87/100 |
| dep_aware-independent_matched | 200 | rank_stability | +0.356 | [+0.329, +0.383] | 100/100 |
| dep_aware-neighbors | 200 | fidelity | +0.022 | [-0.002, +0.060] | 46/100 |
| dep_aware-neighbors | 200 | rank_stability | -0.003 | [-0.020, +0.013] | 48/100 |
| dep_aware-abl_no_dependency | 200 | fidelity | +50.762 | [+10.132, +111.387] | 81/100 |
| dep_aware-abl_no_dependency | 200 | rank_stability | +0.303 | [+0.277, +0.330] | 100/100 |
| dep_aware-abl_no_locality | 200 | fidelity | +0.000 | [-0.000, +0.001] | 52/100 |
| dep_aware-abl_no_locality | 200 | rank_stability | +0.004 | [+0.003, +0.006] | 64/100 |
| dep_aware-independent | 500 | fidelity | +14.253 | [+3.336, +30.731] | 99/100 |
| dep_aware-independent | 500 | rank_stability | +0.679 | [+0.662, +0.696] | 100/100 |
| dep_aware-independent_matched | 500 | fidelity | +4.562 | [+0.994, +9.485] | 82/100 |
| dep_aware-independent_matched | 500 | rank_stability | +0.511 | [+0.489, +0.532] | 100/100 |
| dep_aware-neighbors | 500 | fidelity | -0.035 | [-0.106, +0.002] | 39/100 |
| dep_aware-neighbors | 500 | rank_stability | -0.015 | [-0.028, -0.000] | 39/100 |
| dep_aware-abl_no_dependency | 500 | fidelity | +34.379 | [+6.520, +77.102] | 76/100 |
| dep_aware-abl_no_dependency | 500 | rank_stability | +0.499 | [+0.480, +0.518] | 100/100 |
| dep_aware-abl_no_locality | 500 | fidelity | -0.000 | [-0.001, +0.001] | 49/100 |
| dep_aware-abl_no_locality | 500 | rank_stability | +0.004 | [+0.002, +0.005] | 75/100 |

### adult / rf

| comparison | n | metric | diff mean | 95% CI | wins/n |
|---|---|---|---|---|---|
| dep_aware-independent | 200 | fidelity | +23.095 | [+5.859, +49.119] | 98/100 |
| dep_aware-independent | 200 | rank_stability | +0.354 | [+0.325, +0.386] | 99/100 |
| dep_aware-independent_matched | 200 | fidelity | +1.996 | [+0.741, +3.806] | 89/100 |
| dep_aware-independent_matched | 200 | rank_stability | +0.151 | [+0.121, +0.183] | 80/100 |
| dep_aware-neighbors | 200 | fidelity | +0.059 | [+0.045, +0.072] | 82/100 |
| dep_aware-neighbors | 200 | rank_stability | -0.035 | [-0.057, -0.013] | 34/100 |
| dep_aware-abl_no_dependency | 200 | fidelity | +9.905 | [+2.461, +21.446] | 93/100 |
| dep_aware-abl_no_dependency | 200 | rank_stability | +0.256 | [+0.227, +0.287] | 96/100 |
| dep_aware-abl_no_locality | 200 | fidelity | +0.001 | [-0.001, +0.005] | 50/100 |
| dep_aware-abl_no_locality | 200 | rank_stability | +0.005 | [+0.001, +0.008] | 58/100 |
| dep_aware-independent | 500 | fidelity | +16.813 | [+5.191, +34.175] | 98/100 |
| dep_aware-independent | 500 | rank_stability | +0.583 | [+0.561, +0.603] | 100/100 |
| dep_aware-independent_matched | 500 | fidelity | +1.611 | [+0.645, +3.092] | 92/100 |
| dep_aware-independent_matched | 500 | rank_stability | +0.294 | [+0.274, +0.313] | 100/100 |
| dep_aware-neighbors | 500 | fidelity | +0.054 | [+0.042, +0.065] | 87/100 |
| dep_aware-neighbors | 500 | rank_stability | -0.056 | [-0.073, -0.039] | 22/100 |
| dep_aware-abl_no_dependency | 500 | fidelity | +5.220 | [+1.455, +10.960] | 87/100 |
| dep_aware-abl_no_dependency | 500 | rank_stability | +0.456 | [+0.433, +0.478] | 100/100 |
| dep_aware-abl_no_locality | 500 | fidelity | +0.000 | [-0.001, +0.002] | 46/100 |
| dep_aware-abl_no_locality | 500 | rank_stability | +0.006 | [+0.003, +0.009] | 64/100 |

**Control (synthetic_indep, dep_aware - independent fidelity):** lr n=200: +0.115 [+0.092, +0.139]; lr n=500: +0.111 [+0.088, +0.136]; rf n=200: +0.146 [+0.131, +0.163]; rf n=500: +0.145 [+0.129, +0.163]

## Confirmatory subset: cases NOT used in the pilot or the kernel-width sweep (synthetic: cases 31-100, Adult: 16-100)

| dataset | model | comparison | n | metric | diff mean | 95% CI | wins/n |
|---|---|---|---|---|---|---|---|
| synthetic_dep | lr | dep_aware-independent | 200 | fidelity | +0.122 | [+0.106, +0.139] | 70/70 |
| synthetic_dep | lr | dep_aware-independent_matched | 200 | fidelity | +0.097 | [+0.068, +0.128] | 69/70 |
| synthetic_dep | lr | dep_aware-neighbors | 200 | fidelity | +0.004 | [+0.002, +0.005] | 51/70 |
| synthetic_dep | lr | dep_aware-abl_no_dependency | 200 | fidelity | +0.029 | [+0.026, +0.032] | 66/70 |
| synthetic_dep | lr | dep_aware-abl_no_locality | 200 | fidelity | -0.000 | [-0.001, +0.000] | 37/70 |
| synthetic_dep | lr | dep_aware-independent | 500 | fidelity | +0.117 | [+0.103, +0.132] | 70/70 |
| synthetic_dep | lr | dep_aware-independent_matched | 500 | fidelity | +0.091 | [+0.064, +0.120] | 68/70 |
| synthetic_dep | lr | dep_aware-neighbors | 500 | fidelity | +0.004 | [+0.003, +0.005] | 57/70 |
| synthetic_dep | lr | dep_aware-abl_no_dependency | 500 | fidelity | +0.026 | [+0.023, +0.028] | 68/70 |
| synthetic_dep | lr | dep_aware-abl_no_locality | 500 | fidelity | -0.001 | [-0.001, -0.000] | 32/70 |
| synthetic_dep | rf | dep_aware-independent | 200 | fidelity | +0.172 | [+0.160, +0.184] | 70/70 |
| synthetic_dep | rf | dep_aware-independent_matched | 200 | fidelity | +0.161 | [+0.136, +0.186] | 70/70 |
| synthetic_dep | rf | dep_aware-neighbors | 200 | fidelity | +0.155 | [+0.141, +0.170] | 70/70 |
| synthetic_dep | rf | dep_aware-abl_no_dependency | 200 | fidelity | +0.017 | [+0.013, +0.021] | 65/70 |
| synthetic_dep | rf | dep_aware-abl_no_locality | 200 | fidelity | -0.003 | [-0.004, -0.002] | 17/70 |
| synthetic_dep | rf | dep_aware-independent | 500 | fidelity | +0.170 | [+0.157, +0.182] | 70/70 |
| synthetic_dep | rf | dep_aware-independent_matched | 500 | fidelity | +0.159 | [+0.135, +0.183] | 70/70 |
| synthetic_dep | rf | dep_aware-neighbors | 500 | fidelity | +0.125 | [+0.112, +0.139] | 70/70 |
| synthetic_dep | rf | dep_aware-abl_no_dependency | 500 | fidelity | +0.017 | [+0.012, +0.021] | 64/70 |
| synthetic_dep | rf | dep_aware-abl_no_locality | 500 | fidelity | -0.003 | [-0.004, -0.002] | 6/70 |
| synthetic_indep | lr | dep_aware-independent | 200 | fidelity | +0.121 | [+0.092, +0.150] | 68/70 |
| synthetic_indep | lr | dep_aware-independent_matched | 200 | fidelity | +0.166 | [+0.117, +0.215] | 62/70 |
| synthetic_indep | lr | dep_aware-neighbors | 200 | fidelity | +0.012 | [+0.009, +0.016] | 61/70 |
| synthetic_indep | lr | dep_aware-abl_no_dependency | 200 | fidelity | -0.003 | [-0.007, +0.001] | 34/70 |
| synthetic_indep | lr | dep_aware-abl_no_locality | 200 | fidelity | -0.004 | [-0.005, -0.002] | 15/70 |
| synthetic_indep | lr | dep_aware-independent | 500 | fidelity | +0.115 | [+0.087, +0.144] | 66/70 |
| synthetic_indep | lr | dep_aware-independent_matched | 500 | fidelity | +0.161 | [+0.113, +0.211] | 59/70 |
| synthetic_indep | lr | dep_aware-neighbors | 500 | fidelity | +0.012 | [+0.010, +0.016] | 66/70 |
| synthetic_indep | lr | dep_aware-abl_no_dependency | 500 | fidelity | -0.004 | [-0.009, -0.000] | 25/70 |
| synthetic_indep | lr | dep_aware-abl_no_locality | 500 | fidelity | -0.004 | [-0.006, -0.003] | 9/70 |
| synthetic_indep | rf | dep_aware-independent | 200 | fidelity | +0.149 | [+0.129, +0.170] | 70/70 |
| synthetic_indep | rf | dep_aware-independent_matched | 200 | fidelity | +0.184 | [+0.142, +0.228] | 69/70 |
| synthetic_indep | rf | dep_aware-neighbors | 200 | fidelity | +0.097 | [+0.087, +0.108] | 70/70 |
| synthetic_indep | rf | dep_aware-abl_no_dependency | 200 | fidelity | -0.003 | [-0.007, +0.002] | 31/70 |
| synthetic_indep | rf | dep_aware-abl_no_locality | 200 | fidelity | -0.004 | [-0.006, -0.003] | 10/70 |
| synthetic_indep | rf | dep_aware-independent | 500 | fidelity | +0.148 | [+0.128, +0.169] | 70/70 |
| synthetic_indep | rf | dep_aware-independent_matched | 500 | fidelity | +0.183 | [+0.140, +0.228] | 69/70 |
| synthetic_indep | rf | dep_aware-neighbors | 500 | fidelity | +0.080 | [+0.070, +0.092] | 68/70 |
| synthetic_indep | rf | dep_aware-abl_no_dependency | 500 | fidelity | -0.002 | [-0.007, +0.002] | 35/70 |
| synthetic_indep | rf | dep_aware-abl_no_locality | 500 | fidelity | -0.005 | [-0.007, -0.003] | 10/70 |
| adult | lr | dep_aware-independent | 200 | fidelity | +28.934 | [+5.458, +62.192] | 84/85 |
| adult | lr | dep_aware-independent_matched | 200 | fidelity | +5.509 | [+1.216, +11.223] | 74/85 |
| adult | lr | dep_aware-neighbors | 200 | fidelity | +0.025 | [-0.002, +0.069] | 38/85 |
| adult | lr | dep_aware-abl_no_dependency | 200 | fidelity | +58.749 | [+10.492, +127.834] | 68/85 |
| adult | lr | dep_aware-abl_no_locality | 200 | fidelity | +0.000 | [-0.000, +0.001] | 46/85 |
| adult | lr | dep_aware-independent | 500 | fidelity | +16.353 | [+3.451, +35.483] | 84/85 |
| adult | lr | dep_aware-independent_matched | 500 | fidelity | +5.082 | [+0.961, +10.681] | 70/85 |
| adult | lr | dep_aware-neighbors | 500 | fidelity | -0.042 | [-0.124, +0.003] | 29/85 |
| adult | lr | dep_aware-abl_no_dependency | 500 | fidelity | +39.727 | [+6.783, +87.122] | 63/85 |
| adult | lr | dep_aware-abl_no_locality | 500 | fidelity | -0.000 | [-0.001, +0.001] | 40/85 |
| adult | rf | dep_aware-independent | 200 | fidelity | +26.002 | [+5.801, +57.128] | 83/85 |
| adult | rf | dep_aware-independent_matched | 200 | fidelity | +2.175 | [+0.685, +4.295] | 76/85 |
| adult | rf | dep_aware-neighbors | 200 | fidelity | +0.056 | [+0.041, +0.070] | 69/85 |
| adult | rf | dep_aware-abl_no_dependency | 200 | fidelity | +11.206 | [+2.389, +25.399] | 78/85 |
| adult | rf | dep_aware-abl_no_locality | 200 | fidelity | +0.001 | [-0.002, +0.006] | 39/85 |
| adult | rf | dep_aware-independent | 500 | fidelity | +18.739 | [+5.007, +39.583] | 83/85 |
| adult | rf | dep_aware-independent_matched | 500 | fidelity | +1.728 | [+0.611, +3.520] | 78/85 |
| adult | rf | dep_aware-neighbors | 500 | fidelity | +0.053 | [+0.042, +0.065] | 75/85 |
| adult | rf | dep_aware-abl_no_dependency | 500 | fidelity | +5.835 | [+1.384, +12.863] | 72/85 |
| adult | rf | dep_aware-abl_no_locality | 500 | fidelity | +0.000 | [-0.002, +0.002] | 36/85 |

Cases dropped from paired comparisons (non-finite on either side): none

## Five lowest-fidelity cases per budget (per-case seed means)

| dataset | model | condition | n | case | fidelity | fit_r2 | prediction | mean_nn_dist | frac_seen_combo | mean_dist_to_query |
|---|---|---|---|---|---|---|---|---|---|---|
| synthetic_dep | lr | independent | 200 | 336 | 0.344 | 0.482 | 0.995 | 2.462 | 1.000 | 3.079 |
| synthetic_dep | lr | independent | 200 | 1020 | 0.391 | 0.490 | 0.007 | 2.142 | 1.000 | 3.079 |
| synthetic_dep | lr | independent | 200 | 173 | 0.521 | 0.594 | 0.018 | 2.289 | 1.000 | 3.079 |
| synthetic_dep | lr | independent | 200 | 1284 | 0.535 | 0.608 | 0.020 | 2.304 | 1.000 | 3.079 |
| synthetic_dep | lr | independent | 200 | 435 | 0.563 | 0.628 | 0.025 | 2.046 | 1.000 | 3.079 |
| synthetic_dep | lr | independent | 500 | 336 | 0.308 | 0.452 | 0.995 | 2.462 | 1.000 | 3.078 |
| synthetic_dep | lr | independent | 500 | 1020 | 0.459 | 0.507 | 0.007 | 2.136 | 1.000 | 3.078 |
| synthetic_dep | lr | independent | 500 | 522 | 0.559 | 0.614 | 0.981 | 2.285 | 1.000 | 3.078 |
| synthetic_dep | lr | independent | 500 | 173 | 0.587 | 0.616 | 0.018 | 2.287 | 1.000 | 3.078 |
| synthetic_dep | lr | independent | 500 | 1284 | 0.589 | 0.631 | 0.020 | 2.270 | 1.000 | 3.078 |
| synthetic_dep | lr | dep_aware | 200 | 1020 | 0.754 | 0.780 | 0.007 | 0.950 | 1.000 | 2.535 |
| synthetic_dep | lr | dep_aware | 200 | 336 | 0.758 | 0.778 | 0.995 | 1.030 | 1.000 | 3.018 |
| synthetic_dep | lr | dep_aware | 200 | 380 | 0.828 | 0.860 | 0.965 | 1.019 | 1.000 | 2.889 |
| synthetic_dep | lr | dep_aware | 200 | 1199 | 0.834 | 0.927 | 0.039 | 1.013 | 1.000 | 3.009 |
| synthetic_dep | lr | dep_aware | 200 | 1284 | 0.841 | 0.846 | 0.020 | 0.949 | 1.000 | 2.682 |
| synthetic_dep | lr | dep_aware | 500 | 1020 | 0.760 | 0.781 | 0.007 | 0.948 | 1.000 | 2.533 |
| synthetic_dep | lr | dep_aware | 500 | 336 | 0.770 | 0.773 | 0.995 | 1.022 | 1.000 | 3.022 |
| synthetic_dep | lr | dep_aware | 500 | 380 | 0.830 | 0.840 | 0.965 | 1.017 | 1.000 | 2.890 |
| synthetic_dep | lr | dep_aware | 500 | 1284 | 0.840 | 0.836 | 0.020 | 0.954 | 1.000 | 2.669 |
| synthetic_dep | lr | dep_aware | 500 | 1199 | 0.845 | 0.922 | 0.039 | 1.011 | 1.000 | 2.992 |
| synthetic_dep | rf | independent | 200 | 336 | 0.268 | 0.571 | 0.946 | 2.462 | 1.000 | 3.079 |
| synthetic_dep | rf | independent | 200 | 568 | 0.430 | 0.600 | 0.249 | 2.837 | 1.000 | 3.079 |
| synthetic_dep | rf | independent | 200 | 856 | 0.449 | 0.650 | 0.157 | 2.675 | 1.000 | 3.079 |
| synthetic_dep | rf | independent | 200 | 539 | 0.454 | 0.664 | 0.127 | 2.235 | 1.000 | 3.079 |
| synthetic_dep | rf | independent | 200 | 1035 | 0.470 | 0.756 | 0.746 | 2.859 | 1.000 | 3.079 |
| synthetic_dep | rf | independent | 500 | 336 | 0.217 | 0.566 | 0.946 | 2.462 | 1.000 | 3.078 |
| synthetic_dep | rf | independent | 500 | 568 | 0.443 | 0.605 | 0.249 | 2.838 | 1.000 | 3.078 |
| synthetic_dep | rf | independent | 500 | 856 | 0.457 | 0.636 | 0.157 | 2.699 | 1.000 | 3.078 |
| synthetic_dep | rf | independent | 500 | 1035 | 0.460 | 0.756 | 0.746 | 2.860 | 1.000 | 3.078 |
| synthetic_dep | rf | independent | 500 | 114 | 0.481 | 0.691 | 0.833 | 2.354 | 1.000 | 3.078 |
| synthetic_dep | rf | dep_aware | 200 | 1020 | 0.568 | 0.643 | 0.044 | 0.950 | 1.000 | 2.535 |
| synthetic_dep | rf | dep_aware | 200 | 336 | 0.671 | 0.739 | 0.946 | 1.030 | 1.000 | 3.018 |
| synthetic_dep | rf | dep_aware | 200 | 539 | 0.711 | 0.745 | 0.127 | 0.987 | 1.000 | 2.637 |
| synthetic_dep | rf | dep_aware | 200 | 1310 | 0.711 | 0.770 | 0.254 | 0.940 | 1.000 | 2.513 |
| synthetic_dep | rf | dep_aware | 200 | 380 | 0.724 | 0.789 | 0.768 | 1.019 | 1.000 | 2.889 |
| synthetic_dep | rf | dep_aware | 500 | 1020 | 0.576 | 0.650 | 0.044 | 0.948 | 1.000 | 2.533 |
| synthetic_dep | rf | dep_aware | 500 | 336 | 0.650 | 0.709 | 0.946 | 1.022 | 1.000 | 3.022 |
| synthetic_dep | rf | dep_aware | 500 | 1310 | 0.708 | 0.742 | 0.254 | 0.935 | 1.000 | 2.508 |
| synthetic_dep | rf | dep_aware | 500 | 435 | 0.723 | 0.758 | 0.092 | 0.927 | 1.000 | 2.384 |
| synthetic_dep | rf | dep_aware | 500 | 1402 | 0.724 | 0.771 | 0.066 | 0.866 | 1.000 | 2.189 |
| synthetic_indep | lr | independent | 200 | 1349 | -0.166 | 0.213 | 0.000 | 2.458 | 1.000 | 3.079 |
| synthetic_indep | lr | independent | 200 | 484 | 0.003 | 0.285 | 0.001 | 2.177 | 1.000 | 3.079 |
| synthetic_indep | lr | independent | 200 | 1069 | 0.094 | 0.270 | 1.000 | 2.121 | 1.000 | 3.079 |
| synthetic_indep | lr | independent | 200 | 864 | 0.269 | 0.430 | 0.004 | 2.313 | 1.000 | 3.079 |
| synthetic_indep | lr | independent | 200 | 73 | 0.291 | 0.422 | 0.997 | 2.509 | 1.000 | 3.079 |
| synthetic_indep | lr | independent | 500 | 1349 | -0.122 | 0.167 | 0.000 | 2.434 | 1.000 | 3.078 |
| synthetic_indep | lr | independent | 500 | 484 | 0.055 | 0.265 | 0.001 | 2.158 | 1.000 | 3.078 |
| synthetic_indep | lr | independent | 500 | 1069 | 0.064 | 0.231 | 1.000 | 2.144 | 1.000 | 3.078 |
| synthetic_indep | lr | independent | 500 | 73 | 0.243 | 0.390 | 0.997 | 2.504 | 1.000 | 3.078 |
| synthetic_indep | lr | independent | 500 | 1372 | 0.296 | 0.399 | 0.997 | 2.398 | 1.000 | 3.078 |
| synthetic_indep | lr | dep_aware | 200 | 1349 | 0.392 | 0.487 | 0.000 | 1.045 | 1.000 | 2.983 |
| synthetic_indep | lr | dep_aware | 200 | 484 | 0.453 | 0.540 | 0.001 | 1.016 | 1.000 | 2.689 |
| synthetic_indep | lr | dep_aware | 200 | 1069 | 0.460 | 0.503 | 1.000 | 0.994 | 1.000 | 2.630 |
| synthetic_indep | lr | dep_aware | 200 | 1126 | 0.628 | 0.628 | 0.004 | 0.964 | 1.000 | 2.427 |
| synthetic_indep | lr | dep_aware | 200 | 73 | 0.653 | 0.641 | 0.997 | 1.079 | 1.000 | 3.131 |
| synthetic_indep | lr | dep_aware | 500 | 1349 | 0.424 | 0.488 | 0.000 | 1.039 | 1.000 | 2.981 |
| synthetic_indep | lr | dep_aware | 500 | 1069 | 0.462 | 0.503 | 1.000 | 0.991 | 1.000 | 2.610 |
| synthetic_indep | lr | dep_aware | 500 | 484 | 0.464 | 0.510 | 0.001 | 1.013 | 1.000 | 2.682 |
| synthetic_indep | lr | dep_aware | 500 | 1126 | 0.619 | 0.610 | 0.004 | 0.961 | 1.000 | 2.419 |
| synthetic_indep | lr | dep_aware | 500 | 73 | 0.657 | 0.638 | 0.997 | 1.074 | 1.000 | 3.120 |
| synthetic_indep | rf | independent | 200 | 628 | 0.193 | 0.505 | 0.851 | 2.724 | 1.000 | 3.079 |
| synthetic_indep | rf | independent | 200 | 1349 | 0.229 | 0.499 | 0.019 | 2.458 | 1.000 | 3.079 |
| synthetic_indep | rf | independent | 200 | 484 | 0.247 | 0.479 | 0.025 | 2.177 | 1.000 | 3.079 |
| synthetic_indep | rf | independent | 200 | 1069 | 0.256 | 0.393 | 0.988 | 2.121 | 1.000 | 3.079 |
| synthetic_indep | rf | independent | 200 | 49 | 0.305 | 0.646 | 0.818 | 3.566 | 1.000 | 3.079 |
| synthetic_indep | rf | independent | 500 | 628 | 0.194 | 0.494 | 0.851 | 2.725 | 1.000 | 3.078 |
| synthetic_indep | rf | independent | 500 | 1069 | 0.224 | 0.372 | 0.988 | 2.144 | 1.000 | 3.078 |
| synthetic_indep | rf | independent | 500 | 1349 | 0.234 | 0.484 | 0.019 | 2.434 | 1.000 | 3.078 |
| synthetic_indep | rf | independent | 500 | 484 | 0.277 | 0.472 | 0.025 | 2.158 | 1.000 | 3.078 |
| synthetic_indep | rf | independent | 500 | 49 | 0.311 | 0.627 | 0.818 | 3.574 | 1.000 | 3.078 |
| synthetic_indep | rf | dep_aware | 200 | 1069 | 0.399 | 0.505 | 0.988 | 0.994 | 1.000 | 2.630 |
| synthetic_indep | rf | dep_aware | 200 | 1349 | 0.486 | 0.558 | 0.019 | 1.045 | 1.000 | 2.983 |
| synthetic_indep | rf | dep_aware | 200 | 484 | 0.489 | 0.569 | 0.025 | 1.016 | 1.000 | 2.689 |
| synthetic_indep | rf | dep_aware | 200 | 1126 | 0.612 | 0.643 | 0.024 | 0.964 | 1.000 | 2.427 |
| synthetic_indep | rf | dep_aware | 200 | 1466 | 0.678 | 0.671 | 0.062 | 0.977 | 1.000 | 2.517 |
| synthetic_indep | rf | dep_aware | 500 | 1069 | 0.410 | 0.487 | 0.988 | 0.991 | 1.000 | 2.610 |
| synthetic_indep | rf | dep_aware | 500 | 1349 | 0.507 | 0.574 | 0.019 | 1.039 | 1.000 | 2.981 |
| synthetic_indep | rf | dep_aware | 500 | 484 | 0.515 | 0.567 | 0.025 | 1.013 | 1.000 | 2.682 |
| synthetic_indep | rf | dep_aware | 500 | 1126 | 0.607 | 0.620 | 0.024 | 0.961 | 1.000 | 2.419 |
| synthetic_indep | rf | dep_aware | 500 | 1466 | 0.686 | 0.685 | 0.062 | 0.971 | 1.000 | 2.512 |
| adult | lr | independent | 200 | 6077 | -1057.989 | 0.654 | 0.001 | 2.716 | 0.242 | 4.021 |
| adult | lr | independent | 200 | 2646 | -526.480 | 0.586 | 0.001 | 2.990 | 0.242 | 3.754 |
| adult | lr | independent | 200 | 4076 | -406.503 | 0.743 | 0.002 | 2.670 | 0.242 | 3.979 |
| adult | lr | independent | 200 | 6932 | -249.566 | 0.683 | 0.003 | 2.781 | 0.242 | 3.724 |
| adult | lr | independent | 200 | 4106 | -26.923 | 0.712 | 0.002 | 2.547 | 0.242 | 3.752 |
| adult | lr | independent | 500 | 6077 | -599.496 | 0.583 | 0.001 | 2.701 | 0.238 | 4.036 |
| adult | lr | independent | 500 | 2646 | -304.259 | 0.485 | 0.001 | 2.977 | 0.238 | 3.744 |
| adult | lr | independent | 500 | 4076 | -175.242 | 0.696 | 0.002 | 2.652 | 0.238 | 3.989 |
| adult | lr | independent | 500 | 6932 | -167.455 | 0.613 | 0.003 | 2.760 | 0.238 | 3.734 |
| adult | lr | independent | 500 | 5286 | -19.490 | 0.734 | 0.005 | 2.452 | 0.238 | 3.736 |
| adult | lr | dep_aware | 200 | 4076 | -2.850 | 0.933 | 0.002 | 0.336 | 1.000 | 2.298 |
| adult | lr | dep_aware | 200 | 8091 | -0.119 | 0.970 | 0.049 | 0.272 | 1.000 | 1.481 |
| adult | lr | dep_aware | 200 | 3584 | -0.059 | 0.953 | 0.033 | 0.254 | 1.000 | 1.550 |
| adult | lr | dep_aware | 200 | 4106 | 0.045 | 0.966 | 0.002 | 0.236 | 1.000 | 1.535 |
| adult | lr | dep_aware | 200 | 9752 | 0.084 | 0.967 | 0.004 | 0.217 | 1.000 | 1.393 |
| adult | lr | dep_aware | 500 | 4076 | -6.101 | 0.993 | 0.002 | 0.340 | 1.000 | 2.294 |
| adult | lr | dep_aware | 500 | 8091 | -0.105 | 0.962 | 0.049 | 0.278 | 1.000 | 1.476 |
| adult | lr | dep_aware | 500 | 3584 | -0.048 | 0.943 | 0.033 | 0.257 | 1.000 | 1.530 |
| adult | lr | dep_aware | 500 | 4106 | 0.041 | 0.957 | 0.002 | 0.235 | 1.000 | 1.532 |
| adult | lr | dep_aware | 500 | 9752 | 0.085 | 0.960 | 0.004 | 0.221 | 1.000 | 1.378 |
| adult | rf | independent | 200 | 2646 | -1079.046 | 0.724 | 0.000 | 2.990 | 0.242 | 3.754 |
| adult | rf | independent | 200 | 4076 | -344.802 | 0.740 | 0.004 | 2.670 | 0.242 | 3.979 |
| adult | rf | independent | 200 | 6932 | -320.911 | 0.718 | 0.000 | 2.781 | 0.242 | 3.724 |
| adult | rf | independent | 200 | 6077 | -140.034 | 0.720 | 0.002 | 2.716 | 0.242 | 4.021 |
| adult | rf | independent | 200 | 15962 | -49.311 | 0.749 | 0.000 | 2.486 | 0.242 | 3.660 |
| adult | rf | independent | 500 | 2646 | -714.023 | 0.642 | 0.000 | 2.977 | 0.238 | 3.744 |
| adult | rf | independent | 500 | 6932 | -232.029 | 0.637 | 0.000 | 2.760 | 0.238 | 3.734 |
| adult | rf | independent | 500 | 4076 | -230.435 | 0.655 | 0.004 | 2.652 | 0.238 | 3.989 |
| adult | rf | independent | 500 | 6077 | -111.571 | 0.643 | 0.002 | 2.701 | 0.238 | 4.036 |
| adult | rf | independent | 500 | 877 | -40.688 | 0.654 | 0.001 | 2.459 | 0.238 | 3.933 |
| adult | rf | dep_aware | 200 | 8091 | -0.157 | 0.710 | 0.016 | 0.272 | 1.000 | 1.481 |
| adult | rf | dep_aware | 200 | 6053 | -0.139 | 0.704 | 0.007 | 0.268 | 1.000 | 1.548 |
| adult | rf | dep_aware | 200 | 877 | -0.006 | 0.595 | 0.001 | 0.215 | 1.000 | 2.156 |
| adult | rf | dep_aware | 200 | 4106 | -0.003 | 0.449 | 0.000 | 0.236 | 1.000 | 1.535 |
| adult | rf | dep_aware | 200 | 2026 | 0.009 | 0.720 | 0.010 | 0.323 | 1.000 | 1.792 |
| adult | rf | dep_aware | 500 | 4076 | -0.115 | 0.893 | 0.004 | 0.340 | 1.000 | 2.294 |
| adult | rf | dep_aware | 500 | 8091 | -0.100 | 0.697 | 0.016 | 0.278 | 1.000 | 1.476 |
| adult | rf | dep_aware | 500 | 6053 | -0.065 | 0.463 | 0.007 | 0.273 | 1.000 | 1.546 |
| adult | rf | dep_aware | 500 | 4106 | -0.018 | 0.530 | 0.000 | 0.235 | 1.000 | 1.532 |
| adult | rf | dep_aware | 500 | 877 | 0.011 | 0.560 | 0.001 | 0.216 | 1.000 | 2.148 |

Total explanations: 36000; non-finite fidelity values: 0; non-finite per-case rank stability values: 0; total wall time: 56.6 min.
