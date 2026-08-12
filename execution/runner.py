"""
runner.py: orchestrates the full pipeline — plans work, applies mutations,
submits batches, polls for completion, fetches and records results.
"""

import json
import time
from pathlib import Path

from domain.item import Item
from domain.properties import QualityProperty
from mutations.base import Mutation, MutationType, Severity
from mutations.registry import get_mutation
from providers.base import BatchProvider, PromptRequest, BatchStatus
from execution.planner import plan_work, PlannedUnit
from execution.cache import Cache
from execution.ledger import Ledger
from execution.unit import build_fingerprint
from execution.batch import chunk_requests
from prompting.builder import build_prompt, hash_prompt
from prompting.schema import VerdictResponse
from tracking.base import Tracker
from tracking.pricing import calculate_cost
from tracking.summary import summarize_verdicts
from config import ModelPricing
from execution.manifest import Manifest, get_git_commit, check_manifest


def build_mutations_by_type(items: list[Item]) -> dict[MutationType, Mutation]:
    """
    Constructs one instance of each available mutation, upfront.
    Substitution-based mutations need the full item pool as candidates.
    NOTE: fair_representation is intentionally absent — shelved, see project notes.
    """
    return {
        MutationType.TECHNICAL_QUALITY: get_mutation("blur"),
        MutationType.STANDARD_PRESENTATION: get_mutation("rotate"),
        MutationType.VISUAL_CLARITY: get_mutation("clarity_shapes"),
        MutationType.FUNCTIONAL_RELEVANCE: get_mutation(
            "funct_relevance_substitution", candidates=items
        ),
        MutationType.TEXT_IMAGE_COHERENCE: get_mutation(
            "coherence_substitution", candidates=items
        ),
    }


def build_request_for_unit(
    unit: PlannedUnit,
    seed: int,
    mutations_by_type: dict[MutationType, Mutation],
) -> tuple[PromptRequest, str]:
    """
    Applies the correct mutation to get a damaged image, builds the actual
    PromptRequest to send, plus its fingerprint (used for cache/tracking).
    """
    mutation = mutations_by_type[unit.mutation_type]
    mutated_item = mutation.apply(unit.item, unit.severity, seed)

    if unit.strategy == "split":
        properties = [QualityProperty(unit.mutation_type.value)]
    else:
        properties = list(QualityProperty)

    prompt_text = build_prompt(unit.item, properties)
    prompt_hash = hash_prompt(prompt_text)

    fingerprint = build_fingerprint(
        unit.item.id,
        unit.model,
        unit.mutation_type.value,
        unit.severity.value,
        seed,
        unit.strategy,
        prompt_hash,
    )

    request = PromptRequest(
        custom_id=fingerprint,
        prompt=prompt_text,
        image_path=mutated_item.mutated_image,
    )

    return request, fingerprint


def run_pipeline(
    items: list[Item],
    mutation_types: list[MutationType],
    severities: list[Severity],
    models: list[str],
    strategies: list[str],
    provider: BatchProvider,
    cache: Cache,
    ledger: Ledger,
    tracker: Tracker,
    pricing: dict[str, ModelPricing],
    seed: int,
    manifest_path: Path,
    max_per_batch: int = 50_000,
    poll_interval_seconds: int = 15,
) -> None:
    """
    Runs the full pipeline: plans remaining work, applies mutations,
    submits it in batches, waits for completion, records results.
    """

    manifest = Manifest(git_commit=get_git_commit(), models=models, seed=seed)
    check_manifest(manifest, manifest_path)
    planned_units = plan_work(
        items, mutation_types, severities, models, strategies, cache, seed
    )

    if not planned_units:
        print("Nothing to do — all work already completed.")
        return

    mutations_by_type = build_mutations_by_type(items)

    requests = []
    fingerprint_by_custom_id = {}
    unit_by_custom_id = {}

    for unit in planned_units:
        request, fingerprint = build_request_for_unit(unit, seed, mutations_by_type)
        requests.append(request)
        fingerprint_by_custom_id[request.custom_id] = fingerprint
        unit_by_custom_id[request.custom_id] = unit

    chunks = chunk_requests(requests, max_per_batch)

    for chunk in chunks:
        batch_id = provider.submit_batch(chunk)
        ledger.add_batch(batch_id)
        print(f"Submitted batch {batch_id} with {len(chunk)} requests.")

        while True:
            status = provider.check_batch_status(batch_id)
            if status == BatchStatus.COMPLETED:
                break
            if status == BatchStatus.FAILED:
                raise RuntimeError(f"Batch {batch_id} failed.")
            time.sleep(poll_interval_seconds)

        raw_responses = provider.fetch_batch(batch_id)

        for raw_response, request in zip(raw_responses, chunk):
            custom_id = request.custom_id
            unit = unit_by_custom_id[custom_id]
            fingerprint = fingerprint_by_custom_id[custom_id]

            try:
                verdicts_data = json.loads(raw_response.content)
                verdict_response = VerdictResponse(verdicts=verdicts_data)
            except Exception as e:
                print(f"Failed to parse response for {custom_id}: {e}")
                continue

            model_pricing = pricing[unit.model]
            cost = calculate_cost(
                model_pricing, raw_response.input_tokens, raw_response.output_tokens
            )
            summary = summarize_verdicts(verdict_response.verdicts)

            tracker.log_run_start(
                {
                    "model": unit.model,
                    "strategy": unit.strategy,
                    "mutation_type": unit.mutation_type.value,
                    "severity": unit.severity.value,
                    "item_id": unit.item.id,
                }
            )
            tracker.log_metrics(
                {
                    "cost": float(cost),
                    "input_tokens": raw_response.input_tokens,
                    "output_tokens": raw_response.output_tokens,
                    **summary,
                }
            )
            tracker.log_run_end()

            cache.mark_done(fingerprint)

        ledger.remove_batch(batch_id)
        print(f"Batch {batch_id} fully processed and removed from ledger.")
