# Adult feature-group stability

Group importance is the sum of absolute standardized surrogate coefficients across all encoded columns belonging to an original feature. Dependency groups merge connected components reported in the proposal: education + education-num; marital-status + relationship + sex. All other original features remain singleton groups.
Stability is mean pairwise Spearman correlation of group-importance rankings across the five sampling seeds, computed per explanation case and then averaged across 100 cases.

| model   | condition           |   n |   n_cases |   feature_level_mean |   feature_level_sd |   dependency_group_mean |   dependency_group_sd |   mean_difference |   difference_sd |
|:--------|:--------------------|----:|----------:|---------------------:|-------------------:|------------------------:|----------------------:|------------------:|----------------:|
| lr      | independent         | 200 |       100 |                0.940 |              0.017 |                   0.932 |                 0.018 |            -0.008 |           0.012 |
| lr      | independent         | 500 |       100 |                0.961 |              0.013 |                   0.955 |                 0.012 |            -0.007 |           0.015 |
| lr      | independent_matched | 200 |       100 |                0.941 |              0.014 |                   0.928 |                 0.023 |            -0.013 |           0.016 |
| lr      | independent_matched | 500 |       100 |                0.970 |              0.015 |                   0.964 |                 0.022 |            -0.006 |           0.009 |
| lr      | neighbors           | 200 |       100 |                0.894 |              0.068 |                   0.916 |                 0.056 |             0.022 |           0.042 |
| lr      | neighbors           | 500 |       100 |                0.958 |              0.037 |                   0.970 |                 0.025 |             0.011 |           0.027 |
| lr      | dep_aware           | 200 |       100 |                0.900 |              0.068 |                   0.917 |                 0.059 |             0.017 |           0.045 |
| lr      | dep_aware           | 500 |       100 |                0.960 |              0.032 |                   0.967 |                 0.031 |             0.007 |           0.018 |
| lr      | abl_no_dependency   | 200 |       100 |                0.934 |              0.016 |                   0.939 |                 0.020 |             0.005 |           0.012 |
| lr      | abl_no_dependency   | 500 |       100 |                0.974 |              0.011 |                   0.974 |                 0.013 |            -0.000 |           0.008 |
| lr      | abl_no_locality     | 200 |       100 |                0.900 |              0.069 |                   0.917 |                 0.059 |             0.016 |           0.045 |
| lr      | abl_no_locality     | 500 |       100 |                0.958 |              0.035 |                   0.966 |                 0.032 |             0.007 |           0.019 |
| rf      | independent         | 200 |       100 |                0.922 |              0.018 |                   0.933 |                 0.014 |             0.011 |           0.016 |
| rf      | independent         | 500 |       100 |                0.956 |              0.016 |                   0.957 |                 0.011 |             0.001 |           0.015 |
| rf      | independent_matched | 200 |       100 |                0.905 |              0.025 |                   0.918 |                 0.023 |             0.013 |           0.020 |
| rf      | independent_matched | 500 |       100 |                0.948 |              0.019 |                   0.936 |                 0.022 |            -0.011 |           0.021 |
| rf      | neighbors           | 200 |       100 |                0.852 |              0.080 |                   0.872 |                 0.072 |             0.019 |           0.049 |
| rf      | neighbors           | 500 |       100 |                0.933 |              0.050 |                   0.942 |                 0.039 |             0.009 |           0.027 |
| rf      | dep_aware           | 200 |       100 |                0.846 |              0.094 |                   0.861 |                 0.081 |             0.014 |           0.046 |
| rf      | dep_aware           | 500 |       100 |                0.923 |              0.052 |                   0.929 |                 0.054 |             0.006 |           0.029 |
| rf      | abl_no_dependency   | 200 |       100 |                0.929 |              0.025 |                   0.932 |                 0.019 |             0.003 |           0.017 |
| rf      | abl_no_dependency   | 500 |       100 |                0.952 |              0.022 |                   0.965 |                 0.013 |             0.014 |           0.016 |
| rf      | abl_no_locality     | 200 |       100 |                0.848 |              0.089 |                   0.861 |                 0.080 |             0.013 |           0.046 |
| rf      | abl_no_locality     | 500 |       100 |                0.922 |              0.053 |                   0.927 |                 0.056 |             0.005 |           0.029 |

Interpretation note: a higher dependency-group stability than feature-level stability suggests that some apparent instability is redistributed within correlated feature groups. This is a descriptive stability analysis, not evidence that the groups are causal.
