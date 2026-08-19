"""
pricing.py: cost calculation from token usage, using Decimal for precision.
"""

from decimal import Decimal
from config import ModelPricing


def calculate_cost(
    pricing: ModelPricing, input_tokens: int, output_tokens: int
) -> Decimal:
    """
    Computes the cost of one API call, given per-million-token pricing
    and actual token counts.
    """
    input_cost = (pricing.input_per_million * input_tokens) / 1_000_000
    output_cost = (pricing.output_per_million * output_tokens) / 1_000_000

    return input_cost + output_cost


def total_cost_by_strategy(results: list) -> dict[str, float]:
    """
    Sums total cost, grouped by strategy.
    """
    totals = {}
    for result in results:
        totals[result.strategy] = totals.get(result.strategy, 0.0) + result.cost
    return totals
