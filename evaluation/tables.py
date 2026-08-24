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


def two_dimension_table_latex(
    breakdown: dict[tuple, dict],
    col1_name: str,
    col2_name: str,
    col1_order: list[str],
    col2_order: list[str],
    caption: str,
    label: str,
) -> str:
    """
    Builds a LaTeX table from any two-dimension breakdown (e.g. model x severity).
    """
    lines = []
    lines.append(r"\begin{table}[h]")
    lines.append(r"\centering")
    lines.append(r"\begin{tabular}{llccc}")
    lines.append(r"\toprule")
    lines.append(f"{col1_name} & {col2_name} & Precision & Recall & F1 \\\\")
    lines.append(r"\midrule")

    for c1 in col1_order:
        for c2 in col2_order:
            key = (c1, c2)
            if key not in breakdown:
                continue
            m = breakdown[key]
            lines.append(
                f"{c1} & {c2.capitalize()} & {m['precision']:.2f} & {m['recall']:.2f} & {m['f1']:.2f} \\\\"
            )
        lines.append(r"\midrule")

    lines.pop()
    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    lines.append(f"\\caption{{{caption}}}")
    lines.append(f"\\label{{{label}}}")
    lines.append(r"\end{table}")

    return "\n".join(lines)


def cost_summary_table_latex(
    cost_by_model: dict[str, float], total_results: int
) -> str:
    """
    Builds a LaTeX table summarizing total cost per model and the total
    number of results processed.
    """
    lines = []
    lines.append(r"\begin{table}[h]")
    lines.append(r"\centering")
    lines.append(r"\begin{tabular}{lr}")
    lines.append(r"\toprule")
    lines.append(r"Model & Total cost (\$) \\")
    lines.append(r"\midrule")

    for model, cost in cost_by_model.items():
        lines.append(f"{model} & {cost:.2f} \\\\")

    total_cost = sum(cost_by_model.values())
    lines.append(r"\midrule")
    lines.append(f"Total & {total_cost:.2f} \\\\")
    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    lines.append(
        f"\\caption{{Total cost by model, and total items processed: {total_results}.}}"
    )
    lines.append(r"\label{tab:cost-summary}")
    lines.append(r"\end{table}")

    return "\n".join(lines)
