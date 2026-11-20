# Feature-group stability (sum of |coef|): superseded for stability claims

`feature_group_stability.md` and its two CSVs rank the 14 original Adult features by the **sum** of absolute surrogate
coefficients over each feature's one-hot columns. That score is dominated by how many levels a feature has: coefficients
replaced by noise with no signal shared across seeds still score 0.87 to 0.91 (`results/feature_groups/stability_check.md`).

Use `results/feature_groups/stability_check.csv` instead. With a cardinality-robust definition (mean |coef| per feature) the
Adult random-forest numbers at n = 500 are 0.77 for independent sampling and 0.92 for dependency-aware sampling, which is
what the final talk and `results/week5_evidence.md` report. The files here are kept as the record of the first analysis.
