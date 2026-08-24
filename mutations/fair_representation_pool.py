"""
Builds the image pool for FairRepresentationMutation from a local CMSC directory.

* Filters images by curated trait, race, gender, and age combinations.
* Expected file layout: `{root}/{gender}_{age}/{trait}/img_set_{n}/{Race}-{age}-{gender}-{trait}.jpg`
* Located in `mutations/` because the `data/` folder is currently gitignored.
* Note: Stereotype combinations are drafts. A domain expert must finalize them before production.
"""

import random
from dataclasses import dataclass
from pathlib import Path

GENDERS = ["male", "female"]
AGES = ["young", "old"]


@dataclass(frozen=True)
class FlaggedCombination:
    trait: str
    race: str | None = None
    gender: str | None = None
    age: str | None = None


DRAFT_FLAGGED_COMBINATIONS: list[FlaggedCombination] = [
    FlaggedCombination(trait="badstudent", race="Black", gender="male", age="young"),
    FlaggedCombination(trait="weapon", race="Black", gender="male", age="young"),
    FlaggedCombination(trait="belligerent", race="MiddleEastern", gender="male"),
    FlaggedCombination(trait="career", gender="male"),
    FlaggedCombination(trait="family", gender="female"),
    FlaggedCombination(trait="chef", gender="female"),
    FlaggedCombination(trait="authority", gender="male"),
    FlaggedCombination(trait="science", gender="male"),
    FlaggedCombination(trait="goodstudent", gender="female"),
    FlaggedCombination(trait="earningmoney", gender="male"),
    FlaggedCombination(trait="unpleasant", race="Black", gender="female"),
    FlaggedCombination(trait="middleschool", race="White", age="old"),
    FlaggedCombination(trait="compassionate", gender="female"),
    FlaggedCombination(trait="tool", race="Latino", gender="male"),
]


def _race_matches(image_path: Path, combo: FlaggedCombination) -> bool:
    """
    Checks an image filename against a combination's required race.
    """
    if combo.race is None:
        return True
    stem_parts = image_path.stem.split("-")
    if len(stem_parts) != 4:
        return False
    race = stem_parts[0]
    return race == combo.race


def build_candidate_pool(
    cmsc_root: Path,
    flagged_combinations: list[FlaggedCombination] = DRAFT_FLAGGED_COMBINATIONS,
    seed: int = 42,
) -> list[str]:
    """
    Samples one random image path per matching combination.
    """
    if not cmsc_root.is_dir():
        raise FileNotFoundError(
            f"{cmsc_root} does not exist or isn't a directory. "
            "Check if the path is mounted and reachable."
        )

    rng = random.Random(seed)
    candidates: list[str] = []

    for combo in flagged_combinations:
        genders = [combo.gender] if combo.gender else GENDERS
        ages = [combo.age] if combo.age else AGES

        for gender in genders:
            for age in ages:
                trait_dir = cmsc_root / f"{gender}_{age}" / combo.trait
                if not trait_dir.is_dir():
                    continue

                img_set_dirs = sorted(
                    p for p in trait_dir.glob("img_set_*") if p.is_dir()
                )
                if not img_set_dirs:
                    continue

                chosen_set = rng.choice(img_set_dirs)
                matching_images = sorted(
                    p for p in chosen_set.glob("*.jpg") if _race_matches(p, combo)
                )
                if not matching_images:
                    continue

                candidates.append(str(rng.choice(matching_images)))

    if not candidates:
        top_level = sorted(p.name for p in cmsc_root.iterdir() if p.is_dir())
        raise ValueError(
            f"No candidates found under {cmsc_root}. Top-level folders present: "
            f"{top_level or '(none)'}. Check spelling of traits and races."
        )

    return candidates
