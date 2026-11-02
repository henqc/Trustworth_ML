# Week-4 scale match and kernel width (RF, n=500, 3 seeds)

fidelity = mean ± sd (and median) over cases of the per-case seed mean; rank_stability = mean over cases of the mean pairwise Spearman of |coef| over seeds; mean_weight = mean kernel weight over the 500 fit samples. Fidelity uses the SAME width on the 200 eval points, so different width rules score different weightings of them. rank_stability counts one-hot coefs that are exactly 0 in every seed (absent categories) as agreeing ranks, which inflates it on Adult for samplers that copy categorical blocks.

## synthetic_dep (30 cases)

Table 1: scale sweep (default width 0.75*sqrt(p) = 2.37)

| sampler | scale | fidelity | fidelity_med | rank_stability | mean_dist_to_query | mean_nn_dist |
|---|---|---|---|---|---|---|
| independent | 0.25 | 0.140 ± 0.702 | 0.263 | 0.940 | 0.770 | 1.379 |
| independent | 0.5 | 0.573 ± 0.388 | 0.685 | 0.953 | 1.540 | 1.511 |
| independent | 0.75 | 0.663 ± 0.205 | 0.718 | 0.958 | 2.310 | 1.736 |
| independent | 1.0 | 0.653 ± 0.116 | 0.680 | 0.958 | 3.080 | 2.049 |
| dep_aware | 0.25 | 0.777 ± 0.053 | 0.795 | 0.954 | 2.291 | 0.479 |
| dep_aware | 0.5 | 0.798 ± 0.046 | 0.803 | 0.953 | 2.433 | 0.936 |
| dep_aware | 0.75 | 0.799 ± 0.040 | 0.798 | 0.961 | 2.655 | 1.251 |
| dep_aware | 1.0 | 0.784 ± 0.039 | 0.788 | 0.956 | 2.938 | 1.449 |
| neighbors | nan | 0.671 ± 0.074 | 0.694 | 0.937 | 2.298 | 0.000 |

Table 2: width sweep (mean width over cases: median 2.86, half_median 1.43; independent at its matched scale 0.75)

| sampler | scale | width_rule | fidelity | fidelity_med | rank_stability | mean_weight |
|---|---|---|---|---|---|---|
| dep_aware | 0.5 | default | 0.798 ± 0.046 | 0.803 | 0.953 | 0.363 |
| dep_aware | 0.5 | median | 0.801 ± 0.043 | 0.811 | 0.955 | 0.489 |
| dep_aware | 0.5 | half_median | 0.782 ± 0.057 | 0.791 | 0.949 | 0.076 |
| independent | 0.75 | default | 0.663 ± 0.205 | 0.718 | 0.958 | 0.403 |
| independent | 0.75 | median | 0.662 ± 0.200 | 0.714 | 0.961 | 0.520 |
| independent | 0.75 | half_median | 0.667 ± 0.207 | 0.724 | 0.946 | 0.117 |

## adult (15 cases)

Table 1: scale sweep (default width 0.75*sqrt(p) = 7.69)

| sampler | scale | fidelity | fidelity_med | rank_stability | mean_dist_to_query | mean_nn_dist |
|---|---|---|---|---|---|---|
| independent | 0.25 | -0.392 ± 1.964 | 0.295 | 0.437 | 3.082 | 1.965 |
| independent | 0.5 | -0.587 ± 1.998 | 0.186 | 0.185 | 3.259 | 2.107 |
| independent | 0.75 | -2.235 ± 5.076 | -0.908 | 0.109 | 3.529 | 2.310 |
| independent | 1.0 | -5.685 ± 12.672 | -2.148 | 0.118 | 3.871 | 2.556 |
| dep_aware | 0.25 | 0.512 ± 0.252 | 0.617 | 0.779 | 2.234 | 0.197 |
| dep_aware | 0.5 | 0.524 ± 0.255 | 0.611 | 0.761 | 2.266 | 0.354 |
| dep_aware | 0.75 | 0.526 ± 0.256 | 0.585 | 0.734 | 2.318 | 0.480 |
| dep_aware | 1.0 | 0.521 ± 0.254 | 0.570 | 0.716 | 2.385 | 0.591 |
| neighbors | nan | 0.466 ± 0.272 | 0.568 | 0.806 | 2.231 | 0.000 |

Table 2: width sweep (mean width over cases: median 2.65, half_median 1.32; independent at its matched scale 0.25)

| sampler | scale | width_rule | fidelity | fidelity_med | rank_stability | mean_weight |
|---|---|---|---|---|---|---|
| dep_aware | 0.5 | default | 0.524 ± 0.255 | 0.611 | 0.761 | 0.913 |
| dep_aware | 0.5 | median | 0.530 ± 0.253 | 0.617 | 0.760 | 0.484 |
| dep_aware | 0.5 | half_median | 0.550 ± 0.240 | 0.619 | 0.767 | 0.069 |
| independent | 0.25 | default | -0.392 ± 1.964 | 0.295 | 0.437 | 0.850 |
| independent | 0.25 | median | -0.336 ± 1.797 | 0.281 | 0.443 | 0.262 |
| independent | 0.25 | half_median | -0.472 ± 1.796 | 0.373 | 0.488 | 0.012 |

- (1) synthetic_dep: yes; scale does not explain the pilot gap. Matched pair dep_aware(0.5, dist 2.43) vs independent(0.75, dist 2.31): fidelity 0.798 vs 0.663 (median 0.803 vs 0.718), paired per-case gain +0.135 ± 0.167, dep_aware higher in 30/30 cases, rank stability 0.953 vs 0.958. Shrinking independent's noise hurts (scale 0.25: 0.140).
- (2) Adult: not matchable with this knob: scale shrinks only numeric noise while the 8 categoricals are still drawn from marginals, so independent stays >= 3.08 from the query vs dep_aware <= 2.39. Closest pair dep_aware(0.5, dist 2.27) vs independent(0.25, dist 3.08): fidelity 0.524 vs -0.392 (median 0.611 vs 0.295), paired per-case gain +0.916 ± 1.866, dep_aware higher in 14/15 cases, rank stability 0.761 vs 0.437. Independent improves as its scale shrinks, so part of this gap is distance; a true match needs a categorical keep-probability knob.
- (3) Use `median`: it fixes Adult's near-uniform default kernel (dep_aware mean weight 0.913 -> 0.484), stays close to the default width on synthetic_dep, and dep_aware fidelity and rank stability are no worse than default on either dataset. half_median over-concentrates (Adult mean weight 0.069 dep_aware, 0.012 independent), costs dep_aware fidelity and stability on synthetic_dep, and makes fidelity a much more local target. The dep_aware - independent gap barely moves across default/median/half_median (synthetic_dep +0.135/+0.139/+0.115, Adult +0.916/+0.866/+1.022), so the sampler verdict does not depend on the width.
