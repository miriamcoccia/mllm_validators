"""
base.py: defines the Mutation protocol, Severity levels, and the shared vocabulary for all damage types.
"""

from enum import StrEnum
from domain.item import Item
from dataclasses import dataclass
from typing import Protocol


class Severity(StrEnum):
    SUBTLE = "subtle"
    MODERATE = "moderate"
    OBVIOUS = "obvious"


class MutationType(StrEnum):
    TECHNICAL_QUALITY = "technical_quality"
    STANDARD_PRESENTATION = "standard_presentation"
    VISUAL_CLARITY = "visual_clarity"
    FUNCTIONAL_RELEVANCE = "functional_relevance"
    FAIR_REPRESENTATION = "fair_representation"
    TEXT_IMAGE_COHERENCE = "text_image_coherence"


@dataclass(frozen=True)
class MutatedItem:
    original: Item
    mutation_type: MutationType
    severity: Severity
    mutated_image: str


class Mutation(Protocol):
    def apply(self, item: Item, severity: Severity) -> MutatedItem: ...

    def name(self) -> str: ...
