"""
functional_relevance.py: mutations that substitute the image with an unrelated one. Testing whether the mnodel detects irrelevant images
"""

import random
from pathlib import Path

from domain.item import Item
from PIL import Image
from mutations.base import MutatedItem, MutationType, Severity


class FunctionalRelevanceMutation:
    def __init__(self, candidates: list[Item]):
        self.candidates = candidates

    def name(self) -> str:
        return "funct_relevance_substitution"

    def apply(self, item: Item, severity: Severity, seed: int) -> MutatedItem:
        # TODO: apply severity, so that the more severe substitutions are taken from different subjects
        original_path = Path(item.image)
        new_filename = (
            f"{original_path.stem}_funct_relevance_substitute{original_path.suffix}"
        )

        rng = random.Random(seed)
        possible_substitutes = [
            candidate for candidate in self.candidates if candidate.id != item.id
        ]
        substitute = rng.choice(possible_substitutes)
        substitute_path = Path(substitute.image)
        substitute_image = Image.open(substitute_path)
        new_path = original_path.parent / new_filename
        substitute_image.save(new_path)

        return MutatedItem(
            original=item,
            mutation_type=MutationType.FUNCTIONAL_RELEVANCE,
            severity=severity,
            mutated_image=str(new_path),
        )
