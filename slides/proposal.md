# P02 proposal talk — slide-by-slide content (5 minutes, 6 slides)

One bullet = one line on the slide. Speaker notes in *italics*.

---

## Slide 1 — Title, research question, motivation

**Realistic Neighborhoods for Local Explanations**
*Dependency-aware sampling for LIME-style surrogates*

- **RQ:** Does a dependency-aware perturbation neighborhood improve local-surrogate **fidelity** and **stability** over independent perturbation, at equal query budgets (200 / 500)?
- LIME-style perturbation draws every feature independently → records the data never contains: *Husband + Female*, *education ≠ education-num*, x2 drifting away from x1 when corr = 0.8
- Surrogate is fit where the model never saw data → poor fit on real neighbors, coefficient ranks flip across seeds
- Fix the **neighborhood**, not the surrogate

---

## Slide 2 — System and original component

- Pipeline: data → black box (logistic regression, random forest) → **explanation service** → coefficients, prediction, fidelity, neighborhood-validity diagnostic
- Hand-written (no LIME/SHAP code): weighted ridge (closed form), independent sampler, training-neighbor sampler, dependency-aware sampler
- **Original component: dependency-aware sampler**
  1. Anchor on one of the k = 200 nearest training records (kernel-weighted draw)
  2. Copy its categorical values as a block
  3. Perturb numerics with N(0, s²·Σ_stratum); Σ from neighbors sharing that categorical tuple; clip to training range
- Preserves: realized categorical combos · categorical→numeric compatibility (deterministic partners such as *education-num* copied with the block; strata < 5 rows fall back to the k-neighbor covariance) · local numeric correlation. Not preserved: non-Gaussian / higher-order structure
- Option: validity-aware weights (down-weight samples far from any training record)

---

## Slide 3 — Readings, data, splits

- Readings: Ribeiro et al. 2016 (LIME) · Lundberg & Lee 2017 (SHAP) · LIME / SHAP repos as library baselines
- Synthetic: 10,000 × 10, corr(x1, x2) = 0.8, known logit w = (2, −1.5, 1, 0.5, 0, 0, 0.8, −0.8, 0, 0.3); independent-feature twin as control
- UCI Adult: published train / test = 32,561 / 16,281 rows, 14 features
- **Split manifest written before any training** (`manifests/splits.json`: indices, seeds, file hashes). Synthetic 70/15/15; Adult 80/20 train/dev stratified + published test; 100 fixed explanation cases per dataset
- Encoders and imputers fit on train only
- Dependencies found (train): Adult *education↔education-num* V = 1.00, *relationship↔sex* 0.65, *marital-status↔relationship* 0.49 · synthetic r(x1, x2) = 0.80
- Dev accuracy LR / RF: synthetic 0.785 / 0.753 (label-rule ceiling ≈ 0.78) · Adult 0.845 / 0.862

---

## Slide 4 — First start and pilot findings

- **First start:** weighted ridge recovers the analytic linear predictor's coefficients, max |error| = **3.0 × 10⁻⁹** (20 cases × 5 seeds × 3 samplers × 2 budgets); because an exactly linear target also passes with wrong weighting, it is cross-checked against scikit-learn's weighted Ridge on a noisy target with nonzero intercept (agreement 10⁻⁸)
- **Pilot, random forest on correlated synthetic** (30 cases × 5 seeds; fidelity = weighted R² on 200 held-out dev neighbors, never on the fit samples):

| sampler | fidelity n=200 | fidelity n=500 | rank stability (5 seeds) | dist. to nearest train record | ms / explanation |
|---|---|---|---|---|---|
| independent (LIME-style) | 0.65 | 0.65 | 0.96 | 2.04 | 30 |
| training neighbors | 0.63 | 0.67 | 0.94 | 0.00 | 30 |
| **dependency-aware** | **0.79** | **0.80** | 0.96 | 0.94 | 32 |
| ablation: no dependency constraints | 0.78 | 0.78 | 0.96 | 1.44 | 36 |

- **Pilot, random forest on Adult** (15 cases × 3 seeds; medians over cases of per-case seed means, because independent-sampler means are dominated by outliers: −5.7 ± 12.7):

| sampler | median fidelity n=200 | median fidelity n=500 | rank stability | raw categorical combos seen in train | dist. to nearest train record |
|---|---|---|---|---|---|
| independent (LIME-style) | −2.85 | −2.15 | 0.33 | 24 % | 2.56 |
| training neighbors | 0.49 | 0.57 | 0.97 | 100 % | 0.00 |
| **dependency-aware** | **0.55** | **0.61** | 0.95 | 100 % | 0.35 |
| ablation: no dependency constraints | 0.21 | 0.15 | 0.41 | 23 % | 2.00 |

- **Takeaway:** the phenomenon is measurable, and it is a *held-out* phenomenon: on Adult the independent sampler's in-sample R² is 0.68 but its fidelity on real neighbors is −2.0, with rank stability 0.33. Dependency constraints are what fix it there (ablation median 0.15 vs 0.61). On synthetic data the dependency-aware gain over independent (0.80 vs 0.65) **survives the independence ablation and the independent-feature control** (0.83 vs 0.70), so it is not a dependency effect; working hypothesis: neighborhood scale (perturbation 0.5·σ vs 1.0·σ, mean distance to query 2.4 vs 3.1), to be tested at matched radius in W4

*Notes: "seen combos" measures empirical support, not impossibility: 19 % of real Adult test records have a raw categorical tuple unseen in training. Removing locality weighting changed nothing: our kernel exp(−d²/w²) with w = 0.75√p ≈ 7.7 on the 105-dim one-hot space gave a measured mean weight of 0.91 in the pilot neighborhoods (stock LIME uses √exp(−d²/w²) over raw columns; ours is a LIME-style choice, not stock LIME). Kernel width needs a data-driven choice in W4.*

---

## Slide 5 — Baselines, metrics, compute, six-week scope

- Baselines: independent (LIME-style) · training-neighbor · library SHAP (optional). Ablations: no dependency constraints · no locality weighting. Control: independent-feature synthetic
- Fidelity = kernel-weighted R² on a **predefined** neighborhood (200 nearest dev records, identical for every sampler and seed)
- Stability = mean pairwise Spearman of |coef| over 5 seeds · Validity = distance to nearest training record + fraction of seen categorical combos · Runtime
- Compute: 30,000 explanations (100 cases × 2 budgets × 5 seeds × 5 configs × 2 models × 3 datasets) ≈ **1 h** sequential on an M1 Pro laptop (two pilot runs extrapolate to 58 and 71 min; measured 14 / 95 / 237 ms per explanation for synthetic LR / synthetic RF / Adult RF incl. fidelity + validity); each 3,750-explanation pilot took 5 to 6 min; < 1 GB disk
- W1 dependencies + splits ✓ · W2 weighted surrogate + independent sampler ✓ · W3 sampler + service (prototype ✓, harden) · W4 fidelity/stability grid · W5 independent-feature control + failure analysis · W6 reproducible explanations + report
- Fallback: 50 cases, both datasets and controls kept

---

## Slide 6 — Division of work, outcomes, assumptions

- Student A: samplers, explanation service, ablations · Student B: data/splits, models, evaluation harness, stability + runtime analysis · weekly cross-review of each other's code; report written jointly
- **Expected:** dependency-aware ↑ fidelity and ↑ rank stability on Adult and correlated synthetic at equal budget; parity with independent on the independent-feature control
- **Plausible failure:** gains vanish for logistic regression (near-linear black box); neighbor-anchored samples under-span the space → ill-conditioned surrogate; a scale-matched independent baseline closes the gap on Adult too, making the answer to the RQ "no" (the pilot already shows this on synthetic data)
- **Unresolved assumptions:** perturbation scale (independent uses 1.0 std, ours 0.5·Σ) must be matched before the comparison is fair · kernel width 0.75√p is near-uniform on one-hot data · k = 200 neighbors · "fidelity" depends on how the evaluation neighborhood is defined · the seen-combination diagnostic is empirical support, not impossibility · Gaussian stratum covariance · per-level one-hot coefficients vs feature groups · SHAP comparability (explains a different quantity)
