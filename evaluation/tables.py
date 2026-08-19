"""
tables.py: generates LaTeX tables from computed metrics, for direct
inclusion in the paper.
"""

from pathlib import Path


def detection_rate_table_latex(detection_rates: dict[str, dict]) -> str:
    """
    Builds a LaTeX table (using the booktabs style) showing precision,
    recall, and F1 for each severity level.
    """
    severity_order = ["subtle", "moderate", "obvious"]
    available = [s for s in severity_order if s in detection_rates]

    lines = []
    lines.append(r"\begin{table}[h]")
    lines.append(r"\centering")
    lines.append(r"\begin{tabular}{lccc}")
    lines.append(r"\toprule")
    lines.append(r"Severity & Precision & Recall & F1 \\")
    lines.append(r"\midrule")

    for severity in available:
        metrics = detection_rates[severity]
        lines.append(
            f"{severity.capitalize()} & "
            f"{metrics['precision']:.2f} & "
            f"{metrics['recall']:.2f} & "
            f"{metrics['f1']:.2f} \\\\"
        )

    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    lines.append(r"\caption{Detection performance by damage severity.}")
    lines.append(r"\label{tab:detection-by-severity}")
    lines.append(r"\end{table}")

    return "\n".join(lines)


def save_table(latex_string: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(latex_string)


def strategy_severity_table_latex(breakdown: dict[tuple, dict]) -> str:
    """
    Builds a LaTeX table from a (strategy, severity)-keyed breakdown,
    as produced by detection_rate_by(results, group_by=["strategy", "severity"]).
    """
    severity_order = ["subtle", "moderate", "obvious"]
    strategy_order = ["split", "combined"]

    lines = []
    lines.append(r"\begin{table}[h]")
    lines.append(r"\centering")
    lines.append(r"\begin{tabular}{llccc}")
    lines.append(r"\toprule")
    lines.append(r"Strategy & Severity & Precision & Recall & F1 \\")
    lines.append(r"\midrule")

    for strategy in strategy_order:
        for severity in severity_order:
            key = (strategy, severity)
            if key not in breakdown:
                continue
            metrics = breakdown[key]
            lines.append(
                f"{strategy.capitalize()} & {severity.capitalize()} & "
                f"{metrics['precision']:.2f} & "
                f"{metrics['recall']:.2f} & "
                f"{metrics['f1']:.2f} \\\\"
            )
        lines.append(r"\midrule")

    lines.pop()  # remove the trailing \midrule after the last group
    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    lines.append(
        r"\caption{Detection performance by prompting strategy and damage severity.}"
    )
    lines.append(r"\label{tab:strategy-severity}")
    lines.append(r"\end{table}")

    return "\n".join(lines)
