"""
test_clarity.py: tests for ClarityMutation.
"""

import pytest
from PIL import Image
from pathlib import Path

from mutations.visual_clarity import ClarityMutation
from mutations.base import Severity, MutationType
from domain.item import Item


def make_item(image_path: str, **overrides):
    defaults = dict(
        id="q1",
        question="Q",
        choices=("a", "b"),
        answer=0,
        hint="",
        image=image_path,
        task="t",
        grade="g",
        subject="s",
        topic="t",
        category="c",
        skill="sk",
        lecture="",
        solution="",
        split="train",
    )

    defaults.update(overrides)
    return Item(**defaults)


def make_test_image(path: Path) -> None:
    """Creates a small solid-color test image at the given path."""
    img = Image.new("RGB", (50, 50), color="red")
    img.save(path)


def test_clarity_produces_valid_mutated_item(tmp_path):
    image_path = tmp_path / "original.png"
    make_test_image(image_path)

    item = make_item(str(image_path))
    mutation = ClarityMutation()
    result = mutation.apply(item, Severity.OBVIOUS, seed=42)

    assert result.mutation_type == MutationType.VISUAL_CLARITY
    assert result.severity == Severity.OBVIOUS
    assert Path(result.mutated_image).exists()


def test_clarity_severity_produces_different_files(tmp_path):
    image_path = tmp_path / "original.png"
    make_test_image(image_path)

    item = make_item(str(image_path))
    mutation = ClarityMutation()

    subtle_result = mutation.apply(item, Severity.SUBTLE, seed=42)
    obvious_result = mutation.apply(item, Severity.OBVIOUS, seed=42)

    assert subtle_result.mutated_image != obvious_result.mutated_image
