#!/usr/bin/env python3
"""Adaptive search loop for Phase 4 (round -> Opus eval -> optional deviation round).

This module owns the loop's *logic* so the orchestrator stays a thin driver:
  - the sub-agent `signals` contract (parse_signals)
  - the deviation budget + depth tracking (Budget)
  - the deviations.md audit artifact (Deviation, write_deviations)
  - the cross-agent contradiction scan + the Opus deviation decision
  - the round loop itself (run_search_loop)

Everything is provider-agnostic (LLMProvider) and runs on DryRunProvider for tests.
Real web search is out of scope here — sources stay placeholders.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field

log = logging.getLogger(__name__)

TRIGGERS = ("empty_result", "citation_lead", "unexpected_finding", "contradiction")
CHEAP_TRIGGERS = ("empty_result", "citation_lead")
EXPENSIVE_TRIGGERS = ("unexpected_finding", "contradiction")


def parse_signals(agent_blob: dict) -> tuple[set[str], dict[str, str]]:
    """Extract the set of fired trigger names + their details from one sub-agent's JSON.

    Fail-safe: any malformed/partial signals block yields an empty set (no flag) and a
    logged warning — a cheap model's bad output must never block the run.
    """
    fired: set[str] = set()
    details: dict[str, str] = {}
    block = agent_blob.get("signals")
    if not isinstance(block, dict):
        if block is not None:
            log.warning("signals block is not a dict (%r) — treating as no-flag", type(block))
        return fired, details
    for name in TRIGGERS:
        entry = block.get(name)
        if not isinstance(entry, dict):
            continue
        if entry.get("fired") is True:
            fired.add(name)
            d = entry.get("detail")
            if isinstance(d, str):
                details[name] = d
    unknown = set(block) - set(TRIGGERS)
    if unknown:
        log.warning("signals block has unknown triggers %s — ignored", sorted(unknown))
    return fired, details


# depth -> (cheap_budget, expensive_budget, depth_limit)
BUDGET_BY_DEPTH = {
    "shallow": (2, 0, 1),
    "medium":  (4, 1, 1),
    "deep":    (8, 3, 2),
}


def class_of(trigger: str) -> str:
    """Map a trigger name to its deviation class."""
    if trigger in CHEAP_TRIGGERS:
        return "cheap"
    if trigger in EXPENSIVE_TRIGGERS:
        return "expensive"
    raise ValueError(f"unknown trigger {trigger!r}")


@dataclass
class Budget:
    """Per-run deviation budget. Orchestrator-owned; debit is atomic, never negative."""
    cheap: int
    expensive: int
    depth_limit: int

    @classmethod
    def for_depth(cls, depth: str) -> "Budget":
        try:
            c, e, d = BUDGET_BY_DEPTH[depth]
        except KeyError:
            raise ValueError(f"unknown depth {depth!r} (expected shallow|medium|deep)")
        return cls(cheap=c, expensive=e, depth_limit=d)

    def can_spend(self, klass: str) -> bool:
        return getattr(self, klass) > 0

    def spend(self, klass: str) -> None:
        if not self.can_spend(klass):
            raise ValueError(f"{klass} budget exhausted — caller must check can_spend first")
        setattr(self, klass, getattr(self, klass) - 1)

    def depth_ok(self, current_depth: int) -> bool:
        """True if a round at current_depth may spawn a (deeper) deviation round."""
        return current_depth < self.depth_limit
