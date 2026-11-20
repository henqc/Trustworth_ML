# Isolating dependency ablation (Adult, random forest)

Produced by `src/isolating_ablation.py` in a second software environment, so its rows are compared only with each other,
never with `results/main/`.

`summary.csv` reports the fidelity median over all 500 runs of a condition (0.583 vs 0.450 at n = 500). The protocol's
convention is the mean over seeds within a case first, then statistics over the 100 cases. Those numbers, the rank
stability computed from `coefficients.csv`, and the paired differences are in `results/week5/isolating_stability.csv`
and section C of `results/week5/analysis.md` (fidelity median 0.569 vs 0.446, rank stability 0.748 vs 0.426, full method
better in 86 of 100 cases). The final talk and `results/week5_evidence.md` use the per-case numbers.
