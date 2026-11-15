"""Adult feature-group stability analysis using the saved Week 4 coefficient tensors.

Run from the repository root:
    python src/analyze_feature_groups.py

This does NOT rerun the 36,000-explanation grid and does NOT require the Adult raw data.
It aggregates absolute encoded coefficients to original Adult features, then to the
connected dependency groups identified in slides/proposal.md:
  * education + education-num
  * marital-status + relationship + sex
All other original features remain singleton groups.

The absolute-coefficient sum is used as group importance to avoid cancellation between
positive and negative one-hot coefficients. Stability is mean pairwise Spearman correlation
of group-importance rankings across the five sampling seeds, per case.
"""
from __future__ import annotations

import json
import sys
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

CONDITIONS = [
    "independent", "independent_matched", "neighbors", "dep_aware",
    "abl_no_dependency", "abl_no_locality",
]
BUDGETS = [200, 500]
# Connected components of the dependencies reported in the proposal:
# education <-> education-num; relationship <-> sex; marital-status <-> relationship.
DEPENDENCY_GROUPS = {
    "education+education-num": {"education", "education-num"},
    "marital-status+relationship+sex": {"marital-status", "relationship", "sex"},
}


def original_feature(encoded_name: str, raw_features: list[str]) -> str:
    """Map sklearn ColumnTransformer feature names back to their raw input feature."""
    if encoded_name.startswith("num__"):
        candidate = encoded_name[len("num__"):]
        if candidate in raw_features:
            return candidate
    elif encoded_name.startswith("cat__"):
        tail = encoded_name[len("cat__"):]
        # Longest-prefix matching avoids ambiguity if feature names overlap.
        matches = [f for f in raw_features if tail.startswith(f + "_")]
        if matches:
            return max(matches, key=len)
    raise ValueError(f"Cannot map encoded feature {encoded_name!r} to a raw feature")


def pairwise_spearman(vectors: np.ndarray) -> float:
    """Mean pairwise Spearman over rows (seeds); returns NaN for degenerate vectors."""
    vals = []
    for i, j in combinations(range(len(vectors)), 2):
        a, b = vectors[i], vectors[j]
        if np.std(a) == 0 or np.std(b) == 0:
            vals.append(np.nan)
        else:
            vals.append(float(spearmanr(a, b).statistic))
    return float(np.nanmean(vals)) if np.isfinite(vals).any() else np.nan


def main(input_dir: Path) -> None:
    adult_features = json.loads((input_dir / "features_adult.json").read_text())
    raw_features = [
        "age", "workclass", "fnlwgt", "education", "education-num", "marital-status",
        "occupation", "relationship", "race", "sex", "capital-gain", "capital-loss",
        "hours-per-week", "native-country",
    ]
    encoded_to_raw = [original_feature(name, raw_features) for name in adult_features]

    # One set of encoded-column indices per original raw feature.
    raw_to_idx = {
        f: np.array([i for i, raw in enumerate(encoded_to_raw) if raw == f], dtype=int)
        for f in raw_features
    }
    # Original-feature representation: sum |coef| across one-hot columns belonging to
    # each original feature. This gives 14 comparable input-feature importances.
    raw_groups = {f: {f} for f in raw_features}
    # Dependency-group representation: merge connected features; keep other features separate.
    merged_groups = {f: {f} for f in raw_features}
    for group_name, members in DEPENDENCY_GROUPS.items():
        for member in members:
            merged_groups.pop(member, None)
        merged_groups[group_name] = members

    def aggregate(C: np.ndarray, groups: dict[str, set[str]]) -> np.ndarray:
        # C shape: seeds x encoded_features. Return seeds x groups.
        out = np.zeros((C.shape[0], len(groups)), dtype=float)
        for gi, members in enumerate(groups.values()):
            idx = np.concatenate([raw_to_idx[m] for m in sorted(members)])
            out[:, gi] = np.abs(C[:, idx]).sum(axis=1)
        return out

    rows = []
    for model in ("lr", "rf"):
        path = input_dir / f"coefs_adult_{model}.npy"
        if not path.exists():
            raise FileNotFoundError(f"Missing saved coefficient tensor: {path}")
        C = np.load(path)
        expected = (len(CONDITIONS), len(BUDGETS), 100, 5, len(adult_features))
        if C.shape != expected:
            raise ValueError(f"{path} has shape {C.shape}; expected {expected}")

        for ci, condition in enumerate(CONDITIONS):
            for bi, budget in enumerate(BUDGETS):
                for case_idx in range(C.shape[2]):
                    seed_coefs = C[ci, bi, case_idx]  # seeds x encoded features
                    raw_importance = aggregate(seed_coefs, raw_groups)
                    merged_importance = aggregate(seed_coefs, merged_groups)
                    rows.append({
                        "model": model,
                        "condition": condition,
                        "n": budget,
                        "case_position": case_idx + 1,
                        "feature_level_stability": pairwise_spearman(raw_importance),
                        "dependency_group_stability": pairwise_spearman(merged_importance),
                        "difference_group_minus_feature": (
                            pairwise_spearman(merged_importance) - pairwise_spearman(raw_importance)
                        ),
                    })

    per_case = pd.DataFrame(rows)
    per_case.to_csv(input_dir / "feature_group_stability_per_case.csv", index=False)
    summary = (per_case.groupby(["model", "condition", "n"], sort=False)
               .agg(n_cases=("case_position", "nunique"),
                    feature_level_mean=("feature_level_stability", "mean"),
                    feature_level_sd=("feature_level_stability", "std"),
                    dependency_group_mean=("dependency_group_stability", "mean"),
                    dependency_group_sd=("dependency_group_stability", "std"),
                    mean_difference=("difference_group_minus_feature", "mean"),
                    difference_sd=("difference_group_minus_feature", "std"))
               .reset_index())
    summary.to_csv(input_dir / "feature_group_stability_summary.csv", index=False)

    report = [
        "# Adult feature-group stability",
        "",
        "Group importance is the sum of absolute standardized surrogate coefficients across all encoded columns belonging to an original feature. Dependency groups merge connected components reported in the proposal: education + education-num; marital-status + relationship + sex. All other original features remain singleton groups.",
        "Stability is mean pairwise Spearman correlation of group-importance rankings across the five sampling seeds, computed per explanation case and then averaged across 100 cases.",
        "",
        summary.to_markdown(index=False, floatfmt=".3f"),
        "",
        "Interpretation note: a higher dependency-group stability than feature-level stability suggests that some apparent instability is redistributed within correlated feature groups. This is a descriptive stability analysis, not evidence that the groups are causal.",
    ]
    (input_dir / "feature_group_stability.md").write_text("\n".join(report) + "\n")
    print(summary.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    print("\nWrote feature_group_stability_per_case.csv, feature_group_stability_summary.csv, and feature_group_stability.md")


if __name__ == "__main__":
    directory = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("results/main")
    main(directory)
