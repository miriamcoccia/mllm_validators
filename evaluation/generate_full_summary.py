"""
generate_full_summary.py: computes and saves the complete analysis across
both Phase 1 and Phase 2 — detection rates, cost, significance, and
model comparison.
"""

import json
from pathlib import Path

from evaluation.load import load_results
from evaluation.curves import detection_rate_by, total_cost_by_strategy
from evaluation.tables import (
    strategy_severity_table_latex,
    two_dimension_table_latex,
    save_table,
    cost_summary_table_latex,
)
from evaluation.figures import plot_detection_by_severity
from evaluation.significance import mcnemar_test, bootstrap_recall_ci

results = load_results(Path("runs/results"))
print(f"Total results (before filtering): {len(results)}")

REAL_MODELS = {"gpt5.6-luna", "gpt5.6-terra"}
results = [r for r in results if r.model in REAL_MODELS]
print(f"Total results (after filtering test contamination): {len(results)}")

by_strategy_severity = detection_rate_by(results, group_by=["strategy", "severity"])
by_strategy_property = detection_rate_by(
    results, group_by=["strategy", "mutation_type"]
)
by_model_severity = detection_rate_by(results, group_by=["model", "severity"])
by_model_property = detection_rate_by(results, group_by=["model", "mutation_type"])

cost_by_strategy = total_cost_by_strategy(results)
cost_by_model = {}
for r in results:
    cost_by_model[r.model] = cost_by_model.get(r.model, 0.0) + r.cost

split_results = [r for r in results if r.strategy == "split"]
combined_results = [r for r in results if r.strategy == "combined"]
mcnemar_result = mcnemar_test(split_results, combined_results)
split_ci = bootstrap_recall_ci(split_results, n_bootstrap=1000)
combined_ci = bootstrap_recall_ci(combined_results, n_bootstrap=1000)

summary = {
    "total_results": len(results),
    "detection_by_strategy_severity": {
        str(k): v for k, v in by_strategy_severity.items()
    },
    "detection_by_strategy_property": {
        str(k): v for k, v in by_strategy_property.items()
    },
    "detection_by_model_severity": {str(k): v for k, v in by_model_severity.items()},
    "detection_by_model_property": {str(k): v for k, v in by_model_property.items()},
    "cost_by_strategy": cost_by_strategy,
    "cost_by_model": cost_by_model,
    "mcnemar_test": mcnemar_result,
    "bootstrap_recall_ci": {"split": split_ci, "combined": combined_ci},
}

output_dir = Path("runs/full_summary")
output_dir.mkdir(parents=True, exist_ok=True)
with open(output_dir / "summary.json", "w") as f:
    json.dump(summary, f, indent=2)

# --- tables ---
save_table(
    strategy_severity_table_latex(by_strategy_severity),
    output_dir / "strategy_severity.tex",
)
save_table(
    two_dimension_table_latex(
        by_model_severity,
        "Model",
        "Severity",
        ["gpt5.6-luna", "gpt5.6-terra"],
        ["subtle", "moderate", "obvious"],
        "Detection performance by model and damage severity.",
        "tab:model-severity",
    ),
    output_dir / "model_severity.tex",
)
save_table(
    cost_summary_table_latex(cost_by_model, len(results)),
    output_dir / "cost_summary.tex",
)
save_table(
    two_dimension_table_latex(
        by_model_property,
        "Model",
        "Property",
        ["gpt5.6-luna", "gpt5.6-terra"],
        [
            "technical_quality",
            "visual_clarity",
            "standard_presentation",
            "functional_relevance",
            "text_image_coherence",
        ],
        "Detection performance by model and evaluated property.",
        "tab:model-property",
    ),
    output_dir / "model_property.tex",
)

# --- figure: overall detection by severity, combined strategy only ---
combined_by_severity = {
    sev: metrics
    for (strat, sev), metrics in by_strategy_severity.items()
    if strat == "combined"
}
plot_detection_by_severity(
    combined_by_severity, output_dir / "detection_by_severity.png"
)

print(f"Saved everything to {output_dir}/")
