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
from pathlib import Path

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


@dataclass
class Deviation:
    """One considered trigger (pursued or not_pursued) for the deviations.md log."""
    subquestion: str
    round_from: int
    round_to: int | None        # the round this deviation spawned, or None if not pursued
    trigger: str
    klass: str                  # "cheap" | "expensive"
    status: str                 # "pursued" | "not_pursued"
    rationale: str
    action: str | None
    depth: int | None
    budget_after: dict[str, int]
    outcome: str | None
    new_source_ids: list[str] = field(default_factory=list)
    carry_forward: str | None = None

    def render(self) -> str:
        round_str = f"{self.round_from}" if self.round_to is None else f"{self.round_from} → {self.round_to}"
        ids = "[" + ", ".join(self.new_source_ids) + "]"
        ba = "{ cheap: %d, expensive: %d }" % (self.budget_after.get("cheap", 0),
                                               self.budget_after.get("expensive", 0))
        lines = [
            f"- subquestion: {self.subquestion}",
            f"- round: {round_str}",
            f"- trigger: {self.trigger}",
            f"- class: {self.klass}",
            f"- status: {self.status}",
            "- decision_by: orchestrator (opus)",
            f"- rationale: {self.rationale}",
            f"- action: {self.action if self.action else 'none'}",
            f"- depth: {self.depth if self.depth is not None else '—'}",
            f"- budget_after: {ba}",
            f"- outcome: {self.outcome if self.outcome else '—'}",
            f"- new_source_ids: {ids}",
        ]
        if self.carry_forward:
            lines.append(f"- carry_forward: {self.carry_forward}")
        return "\n".join(lines)


def write_deviations(run_dir: Path, topic: str, deviations: list[Deviation]) -> Path:
    """Render all deviation records to <run_dir>/deviations.md. Always writes a header,
    even for an empty list (an empty file is itself an honest signal: nothing deviated)."""
    out = [f"# Deviations — {topic}", ""]
    for i, d in enumerate(deviations, start=1):
        out.append(f"## D{i}")
        out.append(d.render())
        out.append("")
    path = run_dir / "deviations.md"
    path.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")
    return path


def cross_agent_contradiction_scan(provider, agent_outputs: list[dict]) -> list[dict]:
    """Cheap scan over the whole round's pool for cross-agent contradictions.

    Returns a list of synthetic contradiction findings (each a dict with
    trigger="contradiction" + detail). Catches conflicts no single sub-agent can see.
    Convention for the provider's reply: a line starting with "CONTRADICTION:" reports
    one; the literal "NONE" (or no such line) means none found.
    """
    if len(agent_outputs) < 2:
        return []  # nothing to compare; don't spend a call
    summary = "\n".join(
        f"{a.get('subquestion_id', '?')}: " +
        "; ".join(str(s.get("claim", s.get("url", ""))) for s in a.get("sources", []))
        for a in agent_outputs
    )
    prompt = (
        "Below are claims from independent search agents, one line per subquestion.\n"
        "Report any DIRECT contradictions between subquestions. For each, output a line:\n"
        "  CONTRADICTION: <Qa> vs <Qb> — <what conflicts>\n"
        "If there are none, output exactly: NONE\n\n" + summary
    )
    reply = provider.complete(prompt, model_tier="cheap")
    findings = []
    for line in reply.splitlines():
        line = line.strip()
        if line.upper().startswith("CONTRADICTION:"):
            findings.append({"trigger": "contradiction", "detail": line.split(":", 1)[1].strip()})
    return findings
