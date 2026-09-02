"""
planner.py: figures out what work remains to be done, given everything
that should be tested and what's already been completed (via the cache).
"""

from dataclasses import dataclass
from itertools import product

from domain.item import Item
from domain.properties import QualityProperty
from mutations.base import MutationType, Severity
from execution.unit import build_fingerprint
from execution.cache import Cache
from prompting.builder import build_prompt, hash_prompt


@dataclass(frozen=True)
class PlannedUnit:
    item: Item
    mutation_type: MutationType
    severity: Severity
    model: str
    strategy: str


def plan_work(
    items: list[Item],
    mutation_types: list[MutationType],
    severities: list[Severity],
    models: list[str],
    strategies: list[str],
    cache: Cache,
    seed: int,
) -> list[PlannedUnit]:
    remaining = []

    for item, mutation_type, model, strategy in product(
        items, mutation_types, models, strategies
    ):
        if mutation_type in (
            MutationType.FAIR_REPRESENTATION,
            MutationType.FAIR_REPRESENTATION_CONTROL,
        ):
            severities_to_use = [Severity.SUBTLE]
        else:
            severities_to_use = severities

        for severity in severities_to_use:
            if strategy == "split":
                # NOTE: relies on MutationType and QualityProperty sharing string values.
                properties = [QualityProperty(mutation_type.value)]
            else:
                properties = list(QualityProperty)

            prompt_text = build_prompt(item, properties)
            prompt_hash = hash_prompt(prompt_text)

            fingerprint = build_fingerprint(
                item.id,
                model,
                mutation_type.value,
                severity.value,
                seed,
                strategy,
                prompt_hash,
            )

            if cache.is_done(fingerprint):
                continue

            remaining.append(
                PlannedUnit(
                    item=item,
                    mutation_type=mutation_type,
                    severity=severity,
                    model=model,
                    strategy=strategy,
                )
            )

    return remaining
