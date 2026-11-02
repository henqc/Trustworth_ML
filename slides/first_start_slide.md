# First start: recover a known linear predictor

**Goal.** Check that our hand-written weighted local regression recovers the coefficients of a predictor we know exactly, before trusting it on black-box models.

**Setup**
- Known predictor: f(x) = w · x on the 10 synthetic features, w = (2, −1.5, 1, 0.5, 0, 0, 0.8, −0.8, 0, 0.3)
- 20 fixed test cases × 5 seeds, query budgets n = 200 and n = 500
- Per explanation: sample a neighborhood → query f → kernel weights → closed-form weighted ridge → compare coefficients to w
- Noisy variant adds N(0, 0.5²) to f, because an exact linear target is recovered by any full-rank solver

**Results** — max |coefficient error| over cases, seeds and samplers (`results/first_start.csv`)

| Setting | n = 200 | n = 500 |
|---|---|---|
| Linear f, independent features | 8.5e-10 | 2.7e-10 |
| Linear f, correlated pair | 3.0e-9 | 1.0e-9 |
| Linear f + noise (σ = 0.5) | 0.22 | 0.14 |

Exact targets recovered to ~1e-9 (the residual is the ridge penalty α = 1e-8, not float error); the noisy error falls as 1/√n. The implementation is correct; this says nothing yet about which sampler is better.
