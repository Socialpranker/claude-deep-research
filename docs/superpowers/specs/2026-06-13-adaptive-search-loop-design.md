# Adaptive Search (Phase 4 as an orchestrated loop) + Deviation Log — Design

**Date:** 2026-06-13
**Status:** Approved (brainstorm) → ready for implementation plan
**Scope owner:** `references/workflow.md`, `phases.yaml`, `references/source_dispatch.md` (read-only), `runner/orchestrator.py` (engine, when wired)

> **Architecture note (supersedes an earlier draft):** an earlier version of this spec
> introduced adaptivity as a *separate, conditional Phase 4.5*. That was rejected in
> favor of **Approach 2 — Phase 4 itself becomes an orchestrated loop** (round →
> orchestrator evaluation → optional next round). There is no Phase 4.5. The trade-off
> (every run pays for an Opus evaluation between rounds, even when no adaptation is
> needed) was accepted deliberately for conceptual simplicity: "Phase 4 is a loop,
> full stop."

## Goal

Give the deep-research workflow **bounded runtime adaptivity** in its search stage.
Today search is a single planned salvo: the LLM designs the channel strategy in
Phase 3 / 4.0, sub-agents execute it in Phase 4.1, and they **cannot react** to what
they find — an unexpected lead, an empty channel, a contradiction between sources, or a
citation pointing at an unreachable primary source all go unaddressed until the much
later adversarial/refresh phases (or never).

This design turns **Phase 4 (Search) into an orchestrator-driven loop**. Sub-agents
stay "dumb executors" that follow the plan (cheap). After each search round, control
returns to the orchestrator (Opus), which looks at the aggregated output across *all*
agents and decides: done / deviate / which deviation. A deviation is a re-run of the
search machinery that departs from the approved plan; deviations are bounded by a
**budget** and a **depth (nesting) limit**. The system's core property —
**transparency** — is preserved: every deviation (taken or declined) is recorded in a
structured `deviations.md`, which the adversarial pass (Phase 6) is obligated to audit.

**Finish line of this design:** Phase 4's loop is specified end-to-end — the round
structure, the orchestrator evaluation step, the trigger contract, budget economics,
the depth limit, the `deviations.md` artifact, and how Phases 5/6/7 change around it —
at the methodology level (`workflow.md` / `phases.yaml`), with a clear note of what the
`runner/` engine must implement when it reaches search.

**Explicitly NOT in this design:**
- The `runner/` does not yet do real web search (source URLs are placeholders — see
  the multi-llm-runner spec). This design describes the *methodology* and the engine
  contract; wiring it into live retrieval is downstream work.
- The `source_dispatch.md` matrix is **not modified**. Deviations reuse the existing
  channels — adaptivity changes *when/whether* a channel is queried, not *what
  channels exist*.

## Background: where the code is today

- **Phase 3 (Plan, Opus/medium)** decomposes the question into subquestions
  (`plan.md` section 11) and, at Phase 4.0 (Source Dispatch, Sonnet/medium), runs each
  subquestion through the deterministic matrix in `references/source_dispatch.md` to
  fix primary/secondary/fallback channels into `plan.md` section 12 **before** search.
- **Phase 4.1** launches N parallel `Explore`-type sub-agents (medium: 2–3, deep: 4–5)
  that **follow the fixed dispatch** — they do not choose channels. Each returns JSON
  (sources, quotes, scoring). This gives reproducibility and a user-approvable plan.
- **Phase 4.2/4.3** dedup by URL, apply paywall fallback (`channels.md`), and write
  `sources/SNN_<slug>.md` + `sources.csv`.
- **Phase 5** scores every source (credibility/recency/bias). **Phase 6** runs an
  adversarial pass (4 questions, Opus/high). **Phase 7** generates refresh targets.
- **`runner/`** is a model-agnostic engine scaffold: `orchestrator.py` drives the
  phases through an `LLMProvider` interface (`complete()` + `fanout()`); real web
  search is a TODO (URLs are placeholders). `DryRunProvider` gives deterministic,
  network-free runs — the natural test substrate for orchestration logic.

The current search philosophy is **LLM-as-planner, not LLM-as-router-in-the-loop**.
This design keeps the *plan* authoritative as the starting point and adds a bounded,
auditable feedback loop on top — the orchestrator may depart from the plan, but only
within budget, only with recorded justification.

## Decisions (from brainstorm)

| Decision | Choice |
|---|---|
| Core tension | Adaptivity vs. predictability — resolved as a **bounded feedback loop with a deviation budget**, not free-form runtime routing |
| Where adaptivity lives | **Phase 4 becomes an orchestrator-driven loop** (Approach 2). No separate Phase 4.5. Round → Opus evaluation → optional next round. |
| Who decides to deviate | The **orchestrator (Opus)** with the full cross-agent picture — **not** the cheap sub-agents. Judgment is expensive-model work; execution stays cheap. |
| Cost trade-off (accepted) | Every run pays for an Opus evaluation between rounds, even when nothing changes. Accepted for conceptual simplicity over per-run thrift. |
| Trigger set | Four triggers: `empty_result`, `citation_lead` (self-correction), `unexpected_finding`, `contradiction` (scope-expansion) |
| Detection model | **Two-tier**: sub-agents signal generously on **all four** flags (high recall); Opus filters strictly **and** independently re-checks cross-agent contradictions the sub-agents structurally cannot see (high precision) |
| Deviation classes | **cheap** (self-correction: doesn't change scope) vs **expensive** (scope-expansion: departs from the approved plan) — different budgets |
| Budget by depth | shallow `2 cheap / 0 expensive`, medium `4 / 1`, deep `8 / 3` (starting calibration) |
| Depth (nesting) limit | shallow/medium = 1, deep = 2 — a deviation may spawn a sub-round, but nesting is capped independently of budget (rabbit-hole guard) |
| Exhausted budget/depth | Remaining candidates are **not executed but still recorded** in `deviations.md` as `not_pursued` + reason — never a silent skip |
| Deviation log | Structured `deviations.md` (one record per considered trigger), owned solely by the orchestrator |
| Consumer | **Phase 6 (adversarial) must read it** — a 5th adversarial question audits *both* sides: `pursued` (did the agent stray?) and `not_pursued` (is it a coverage hole?) |
| Loop termination | The loop ends when: no justified trigger remains, OR both budgets are exhausted, OR the depth limit is reached. The first round always runs (it *is* the plan); evaluation happens *after* each round. |

## Architecture

### Flow

```
Phase 4 (Search) — now an orchestrator-driven LOOP
   │
   ├─ Round 1 (= the approved plan, Phase 4.0 dispatch) — ALWAYS runs
   │     └─ N sub-agents follow the fixed dispatch
   │     └─ each sub-agent emits a `signals` block in its JSON (all 4 flags)
   │
   ├─ Orchestrator evaluation (Opus) — runs AFTER every round:
   │     1. aggregate all sub-agent JSON for the round
   │     2. cheap cross-agent contradiction scan (Haiku/Sonnet) over the pool
   │        — catches contradictions a single sub-agent cannot see
   │     3. Opus reviews flags + scan + aggregated output
   │     4. are there JUSTIFIED triggers AND (budget remains) AND (depth < limit)?
   │           ├─ no  → exit loop → Phase 5
   │           └─ yes → for each justified trigger:
   │                      • classify cheap | expensive
   │                      • debit the matching budget counter
   │                      • write a `deviations.md` record
   │                    launch the next round (sub-round of sub-agents), depth++
   │     (every considered-but-skipped trigger → `not_pursued` record)
   │
   └─ (loop repeats: each new round is re-evaluated the same way)
   ↓
Phase 5 (Scoring) — scores ALL sources (planned + deviation-sourced) identically
   ↓
Phase 6 (Adversarial) — NEW obligation: read deviations.md (5th question)
   ↓
Phase 7 (Refresh) — reads not_pursued/carry_forward as refresh-target candidates
```

**Key difference from a single-salvo Phase 4:** the orchestrator evaluation step runs
on *every* run (that's the accepted cost). On a "calm" run it finds no justified
trigger in round 1 and exits immediately to Phase 5 — one extra Opus evaluation, no
extra rounds. On a run with real triggers it spends deviations until a termination
condition hits.

### Component 1 — Trigger contract (sub-agent → orchestrator)

Each sub-agent (every round) adds a `signals` block to its existing JSON. It **reports
observations; it does not decide to deviate.**

```json
{
  "subquestion_id": "Q3",
  "round": 1,
  "sources": [ ... ],
  "signals": {
    "empty_result":       { "fired": true,  "detail": "0 relevant hits on channel `academic`; all 4 results off-topic" },
    "unexpected_finding": { "fired": true,  "detail": "sources point to EU AI Act as the cause of the market collapse — not in the plan" },
    "contradiction":      { "fired": false, "detail": null },
    "citation_lead":      { "fired": true,  "detail": "S07 cites a primary Gartner 2024 report; no direct link present" }
  }
}
```

| Trigger | Nature | Meaning | Reliable detector |
|---|---|---|---|
| `empty_result` | self-correction (cheap) | a planned channel returned nothing relevant | the sub-agent (sees its own output) |
| `citation_lead` | self-correction (cheap) | a source references an unreachable primary source | the sub-agent |
| `unexpected_finding` | scope-expansion (expensive) | an important angle outside the plan surfaced | sub-agent *signals a candidate*; **Opus confirms** |
| `contradiction` | scope-expansion (expensive) | sources conflict | **often only Opus** (a sub-agent sees only its half) → backed by the cross-agent scan in the evaluation step |

**Principle:** sub-agents signal generously (recall), Opus filters strictly
(precision). Cheap model = recall, expensive model = judgment. A sub-agent's
`unexpected_finding`/`contradiction` flag is a *candidate*, never an automatic spend.

The cross-agent contradiction scan in the evaluation step is what catches conflicts no
single sub-agent can see (each sees only its own subquestion's half). It runs every
round, so a contradiction surfaced in round 2 is caught just like one in round 1.

### Component 2 — Budget, classes, depth limit (orchestrator-owned)

| Class | Triggers | Limit rationale |
|---|---|---|
| **cheap** (self-correction) | `empty_result`, `citation_lead` | finishes already-planned work; doesn't change scope → generous |
| **expensive** (scope-expansion) | `unexpected_finding`, `contradiction` | departs from the approved plan → hard ceiling |

| Depth | cheap | expensive | depth (nesting) limit |
|---|---|---|---|
| shallow | 2 | 0 | 1 |
| medium | 4 | 1 | 1 |
| deep | 8 | 3 | 2 |

- **shallow expensive = 0** — the only hard cut, and it's *by class*: a shallow run with
  `empty_result` still self-corrects; a shallow `unexpected_finding` is recorded
  `not_pursued: budget_exhausted` and not run.
- **expensive grows slowly** (0→1→3) — the costliest, scope-changing class.
- **cheap grows generously** (2→4→8) — self-correction is cheap and usually useful.
- **Depth limit** is independent of budget: a deviation may spawn a sub-round, but at
  the depth limit that sub-round cannot spawn its own. deep=2 lets a citation chain go
  two levels (S07 → Gartner report → primary source inside it), then stop. Because
  Phase 4 is now a loop, "depth" = how many deviation-spawned rounds deep the current
  round is (round 1 = depth 0; a deviation from round 1 produces a depth-1 round; etc.).
- **Numbers are starting calibration**, expected to be tuned against real runs.
- **Debit is atomic, orchestrator-only**, performed *before* launching the next round.
  One counter per run; no distributed state.

### Component 3 — `deviations.md` (the audit artifact)

Lives beside `plan.md` / `sources/` in the run directory. One record per **considered**
trigger (both `pursued` and `not_pursued`).

```markdown
# Deviations — <research topic>

## D1
- subquestion: Q3
- round: 1 → 2
- trigger: empty_result
- class: cheap
- status: pursued
- decision_by: orchestrator (opus)
- rationale: channel `academic` returned 0 relevant; reformulated query + added fallback `preprint-servers`
- action: launched round 2 sub-round on `preprint-servers`, query "..."
- depth: 1
- budget_after: { cheap: 3, expensive: 1 }
- outcome: +2 sources (S11, S12), both relevant
- new_source_ids: [S11, S12]

## D2
- subquestion: Q5
- round: 1
- trigger: unexpected_finding
- class: expensive
- status: not_pursued
- decision_by: orchestrator (opus)
- rationale: EU AI Act angle is relevant but the expensive budget is exhausted (deep=3 spent on D-…)
- action: none
- depth: —
- budget_after: { cheap: 5, expensive: 0 }
- outcome: —
- carry_forward: recommended as a Phase 7 refresh-target
```

| Field | Purpose |
|---|---|
| `round` | which round raised it → which round (if any) it spawned |
| `trigger` + `class` | which of the 4 triggers; cheap/expensive |
| `status` | `pursued` / `not_pursued` — **the honesty field** |
| `decision_by` | always the orchestrator (Opus) — records that judgment ran on the expensive model |
| `rationale` | **why** Opus decided as it did — the thing Phase 6 will challenge |
| `action` | concrete sub-round launched (channel + query), or `none` |
| `depth` | nesting level of this deviation |
| `budget_after` | spend traceability |
| `outcome` + `new_source_ids` | what the deviation actually yielded; links to `sources/` |
| `carry_forward` | for `not_pursued`: where it goes (usually a Phase 7 refresh-target) |

**Data flow:** the orchestrator (Opus) **writes** every decision during the Phase 4
loop. Phase 5 does **not** touch the log — it scores `new_source_ids` like any other
source (deviation-sourced material is indistinguishable in quality; only its provenance
differs, and that provenance is in `deviations.md`). Phase 6 **reads** it (mandatory
input). Phase 7 **reads** `not_pursued`/`carry_forward` for refresh candidates.

### Component 4 — Phase 6 obligation (the consumer)

A **5th adversarial question** is added to the existing four:

> Review `deviations.md`. For each `pursued` deviation: was it justified, and did it
> pull the research away from the approved plan? For each `not_pursued`: is the skipped
> angle critical to the final answer — is this a hole in coverage?

This audits **both** failure modes: over-adaptation (the agent chased a tangent) and
under-coverage (a real gap was left unexplored because of budget/depth).

## Changes to existing files

| File | Change |
|---|---|
| `phases.yaml` | Phase 4 entry annotated as a **loop** (model: sonnet for the search rounds, with an Opus evaluation step between rounds — captured in the workflow prose; `phases.yaml` keeps the main-thread model). No new phase id. |
| `references/workflow.md` | Phase 4 rewritten as a round loop: Round 1 = the plan; an orchestrator evaluation step after each round (cross-agent contradiction scan + Opus deviation decision); the `signals` block added to the Phase 4.1 sub-agent JSON; budget/depth/`deviations.md` mechanics; Phase 6 gains the 5th adversarial question; Phase 7 reads `carry_forward` |
| `scripts/stamp_docs.py` consumers (README/SKILL/workflow counts) | Re-stamped from `phases.yaml` so phase counts/lists stay in sync (existing `--check` gate). Phase count is **unchanged** (no new phase added). |
| `runner/orchestrator.py` | (engine, when wired) Phase 4 becomes a loop: round dispatch via existing `fanout()`, the evaluation step (`complete()` for the Opus decision + a cheap `complete()`/`fanout()` for the contradiction scan), budget/depth counters, `deviations.md` writer |

**Note on `phases.yaml`:** no new phase id is introduced (this is the main structural
difference from the rejected 4.5 draft). Phase 4 stays a single phase whose *internal*
behavior is now a loop. The per-round search work stays Sonnet/medium (as today); the
between-rounds evaluation is Opus and is described in `workflow.md` prose rather than as
a separate `phases.yaml` row, to avoid implying a new top-level phase. `stamp_docs.py`
phase counts therefore do not change.

## Testing strategy

Built on the existing contour: `tests/`, `pytest.ini`, `stamp_docs.py --check`, CI per PR.

1. **Doc consistency (existing gate).** `phases.yaml` Phase 4 annotation → `stamp_docs.py
   --check` green; phase counts/lists in README/SKILL/workflow.md still match (count
   unchanged — no new phase). Catches "changed the methodology, forgot the docs."
2. **Loop logic (unit, on `DryRunProvider`).** Tests the *orchestration of decisions*,
   not search quality:
   - round 1 always runs; evaluation runs after every round;
   - cheap/expensive debited correctly, never below zero (independent counters);
   - `expensive=0` on shallow → scope deviation not run, `not_pursued: budget_exhausted` written;
   - depth limit: a deviation-spawned round at the limit does not spawn another;
   - no justified trigger after round 1 → loop exits immediately to Phase 5 (one evaluation, one round);
   - **honesty test:** exhausted budget/depth still writes a `not_pursued` record (never a silent skip);
   - **termination test:** the loop cannot run forever — every path hits no-trigger / budget-out / depth-out.
3. **Signal contract (unit).** sub-agent JSON `signals` parses; Opus filter (mocked on
   DryRun) can mark a sub-agent's `unexpected_finding` as unjustified; cross-agent
   contradiction scan raises a deviation when sub-agents were silent.
4. **End-to-end (integration, opt-in behind `-m live`).** Mirrors the existing live
   smoke test: one small real run with a deliberate trigger (a query whose planned
   channel is knowingly empty) → assert the loop ran a second round, `deviations.md`
   created, source added.

### Edge cases (must be covered)

| Edge case | Expected behavior |
|---|---|
| All sub-agents flag, but the deep budget is exhausted in round 1 evaluation | the rest → `not_pursued`; loop exits; Phase 5 proceeds |
| A deviation round itself returns nothing | record `outcome: 0 sources`; budget **still** debited (an attempt costs money); the round is still re-evaluated but yields no new justified trigger → loop ends |
| Sub-agent sends malformed/partial `signals` | treated as "no flag" (fail-safe: never block the run on a cheap model); log a warning |
| Contradiction visible only to Opus (sub-agents silent) | the cross-agent scan in the evaluation step raises it; the loop continues even with zero sub-agent flags |
| Calm run (no triggers at all) | round 1 runs, one evaluation finds nothing justified, loop exits to Phase 5 — the accepted minimal overhead |

## Open questions / future work

- **Budget calibration.** The 2/0/1 · 4/1/1 · 8/3/2 table is a first guess; tune against
  real runs (track in `deviations.md` how often budgets are hit vs. wasted).
- **Evaluation overhead.** Approach 2 pays for an Opus evaluation on every run. If that
  proves too costly on calm runs in practice, the closest fallback is to gate the
  *first* evaluation behind a flag (the rejected hybrid). Noted, not chosen.
- **Runner integration.** This spec is methodology-first; the `runner/` engine
  implements the loop only once real web search lands (see multi-llm-runner spec).
