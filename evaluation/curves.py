"""
curves.py: computes detection rate by severity — the main result showing
whether models catch more obvious damage more reliably.
"""

from evaluation.load import LoadedResult
from evaluation.metrics import compute_confusion_counts, compute_metrics
from domain.properties import QualityProperty


def detection_rate_by_severity(results: list[LoadedResult]) -> dict[str, dict]:
    """
    Groups results by severity, computes aggregate precision/recall/F1 for each.
    """
    grouped = {}
    for result in results:
        severity = result.severity
        if severity not in grouped:
            grouped[severity] = {"tp": 0, "fp": 0, "fn": 0, "tn": 0}

        damaged_property = QualityProperty(result.mutation_type)

        counts = compute_confusion_counts(result.verdicts, damaged_property)
        grouped[severity]["tp"] += counts["tp"]
        grouped[severity]["fp"] += counts["fp"]
        grouped[severity]["fn"] += counts["fn"]
        grouped[severity]["tn"] += counts["tn"]

    final_result = {}
    for severity, counts in grouped.items():
        final_result[severity] = compute_metrics(counts)

    return final_result


def detection_rate_by(
    results: list[LoadedResult], group_by: list[str]
) -> dict[tuple, dict]:
    """
    Groups results by any combination of fields (e.g. ["strategy", "severity"]),
    computes aggregate precision/recall/F1 for each group.
    """
    grouped = {}

    for result in results:
        key = tuple(getattr(result, field) for field in group_by)

        if key not in grouped:
            grouped[key] = {"tp": 0, "fp": 0, "fn": 0, "tn": 0}

        damaged_property = QualityProperty(result.mutation_type)
        counts = compute_confusion_counts(result.verdicts, damaged_property)

        for k in grouped[key]:
            grouped[key][k] += counts[k]

    return {key: compute_metrics(counts) for key, counts in grouped.items()}


def total_cost_by_strategy(results: list) -> dict[str, float]:
    """
    Sums total cost, grouped by strategy.
    """
    totals = {}
    for result in results:
        totals[result.strategy] = totals.get(result.strategy, 0.0) + result.cost
    return totals
