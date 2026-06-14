# Real Retrieval `search()` — Phase 5 Stage 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `search()` method to the provider protocol that returns sub-agent output in the shape the adaptive loop already consumes, implement it as a deterministic fixture in `DryRunProvider`, and wire `orchestrator.search()` to use it — replacing the hardcoded empty-signals placeholder.

**Architecture:** `search(subquery) -> {subquestion_id, sources, signals}` joins `complete()`/`fanout()` on the `LLMProvider` Protocol. `DryRunProvider` returns a stable fixture (real source fields, `example.com` URLs, all signals `fired:false`). `ClaudeProvider`/`OpenAICompatProvider` raise `NotImplementedError` (the real `web_search` call is Stage 2). The orchestrator's `run_round` closure calls `provider.search()` per sub-agent instead of `fanout()`-and-discard, and writes sources from the returned blobs. The loop engine (`run_search_loop`/`parse_signals`) is untouched — it is already provider-agnostic.

**Tech Stack:** Python 3.14, `pytest` (NOT vitest). Spec: `docs/superpowers/specs/2026-06-14-real-retrieval-search-design.md`. Run all commands from `/Users/ivanteresenko/Downloads/claude-deep-research`. Baseline before starting: `pytest -q` → 82 passed / 4 skipped; `python3 scripts/stamp_docs.py --check` → exit 0. No bare `python` — use `python3`.

---

## Pre-flight (run once before Task 1)

- [ ] **Confirm baseline green**

Run: `pytest -q && python3 scripts/stamp_docs.py --check; echo "exit: $?"`
Expected: `82 passed, 4 skipped`, then `exit: 0`. If not green, STOP — investigate before writing code.

---

## Task 1: Add `search()` to the `LLMProvider` Protocol

**Files:**
- Modify: `runner/providers.py:35-45` (the `LLMProvider` Protocol body)

This task only declares the contract on the Protocol. No test on its own (a Protocol method has no behaviour) — it is verified by Task 2's DryRun test and Task 4's NotImplementedError tests. Do this task and Task 2 as one commit.

- [ ] **Step 1: Add the method signature to the Protocol**

In `runner/providers.py`, inside `class LLMProvider(Protocol)` (after the `fanout` stub at `:43-45`), add:

```python
    def search(self, subquery: str, *, subquestion_id: str = "Q0", model_tier: str = "cheap") -> dict:
        """One sub-agent search round. Returns an agent-output blob:
            {"subquestion_id": str,
             "sources": [{"id": str, "url": str, "title": str, "claim": str}, ...],
             "signals": {trigger: {"fired": bool, "detail": str | None}}}
        where trigger in ("empty_result", "citation_lead", "unexpected_finding", "contradiction").
        The shape matches what runner.adaptive.parse_signals consumes."""
        ...
```

- [ ] **Step 2: Verify nothing imports-broke**

Run: `python3 -c "from runner.providers import LLMProvider; print('ok')"`
Expected: `ok`

(Commit happens at the end of Task 2.)

---

## Task 2: Implement `DryRunProvider.search()` (deterministic fixture)

**Files:**
- Modify: `runner/providers.py:48-63` (the `DryRunProvider` class)
- Test: `tests/test_providers_search.py` (create)

- [ ] **Step 1: Write the failing test**

Create `tests/test_providers_search.py`:

```python
from runner.providers import DryRunProvider, SEARCH_TRIGGERS


def test_dryrun_search_returns_expected_shape():
    p = DryRunProvider()
    blob = p.search("market size of widgets", subquestion_id="Q3")
    assert blob["subquestion_id"] == "Q3"
    # sources: non-empty, each with required fields
    assert blob["sources"], "expected at least one fixture source"
    for s in blob["sources"]:
        assert set(("id", "url", "title", "claim")) <= set(s)
    # signals: all four triggers present, none fired
    assert set(blob["signals"]) == set(SEARCH_TRIGGERS)
    for trig, entry in blob["signals"].items():
        assert entry == {"fired": False, "detail": None}


def test_dryrun_search_is_deterministic():
    p = DryRunProvider()
    a = p.search("same query", subquestion_id="Q1")
    b = p.search("same query", subquestion_id="Q1")
    assert a == b


def test_dryrun_search_varies_by_subquery():
    p = DryRunProvider()
    a = p.search("query alpha", subquestion_id="Q1")
    b = p.search("query beta", subquestion_id="Q1")
    # different subqueries -> different source ids/urls (hash-derived)
    assert a["sources"] != b["sources"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_providers_search.py -v`
Expected: FAIL — `ImportError: cannot import name 'SEARCH_TRIGGERS'` (and `search` missing).

- [ ] **Step 3: Add `SEARCH_TRIGGERS` constant and implement `DryRunProvider.search()`**

In `runner/providers.py`, add the constant near the top (after `TIERS` at `:20`):

```python
SEARCH_TRIGGERS = ("empty_result", "citation_lead", "unexpected_finding", "contradiction")
```

Then in `class DryRunProvider`, after its `fanout` method (`:60-63`), add:

```python
    def search(self, subquery: str, *, subquestion_id: str = "Q0", model_tier: str = "cheap") -> dict:
        assert model_tier in TIERS, f"unknown tier {model_tier}"
        h = hashlib.sha1(subquery.encode()).hexdigest()[:8]
        sources = [
            {"id": f"s{h[:4]}{i}", "url": f"https://example.com/source-{h}-{i}",
             "title": f"Fixture source {i} for {subquery[:40]}",
             "claim": f"(dryrun claim {i})"}
            for i in range(1, 3)
        ]
        signals = {t: {"fired": False, "detail": None} for t in SEARCH_TRIGGERS}
        return {"subquestion_id": subquestion_id, "sources": sources, "signals": signals}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_providers_search.py -v`
Expected: PASS (3 tests).

- [ ] **Step 5: Confirm the signals shape matches `parse_signals`**

Run: `python3 -c "from runner.providers import DryRunProvider; from runner.adaptive import parse_signals; print(parse_signals(DryRunProvider().search('x')))"`
Expected: `(set(), {})` — DryRun fires nothing, so `parse_signals` returns empty fired-set and empty details. This proves the contract lines up.

- [ ] **Step 6: Commit (Tasks 1 + 2)**

```bash
git add runner/providers.py tests/test_providers_search.py
git commit -m "feat(retrieval): search() в протоколе LLMProvider + DryRun fixture

search(subquery)->{subquestion_id,sources,signals} в форме, которую ждёт
parse_signals. DryRun возвращает детерминированный fixture (реальные поля,
example.com URL, все signals fired:false) — CI зелёный, цикл выходит за раунд 1."
```

---

## Task 3: `ClaudeProvider.search()` and `OpenAICompatProvider.search()` raise `NotImplementedError`

**Files:**
- Modify: `runner/providers.py:66-99` (`ClaudeProvider`), `runner/providers.py:102-138` (`OpenAICompatProvider`)
- Test: `tests/test_providers_search.py` (append)

Stage-1 guard: the live `web_search` path doesn't exist yet, so calling it must fail loudly, not silently return a placeholder.

- [ ] **Step 1: Write the failing test**

Append to `tests/test_providers_search.py`:

```python
import pytest
from runner.providers import ClaudeProvider, OpenAICompatProvider


def test_claude_search_not_implemented_yet():
    # construct without touching the network: pass a dummy client
    p = ClaudeProvider(client=object())
    with pytest.raises(NotImplementedError):
        p.search("x")


def test_openai_search_not_implemented_yet():
    p = OpenAICompatProvider(client=object())
    with pytest.raises(NotImplementedError):
        p.search("x")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_providers_search.py -k not_implemented -v`
Expected: FAIL — `AttributeError: 'ClaudeProvider' object has no attribute 'search'`.

- [ ] **Step 3: Add the stubs**

In `runner/providers.py`, in `class ClaudeProvider`, after its `fanout` method (`:95-99`), add:

```python
    def search(self, subquery: str, *, subquestion_id: str = "Q0", model_tier: str = "cheap") -> dict:
        raise NotImplementedError(
            "ClaudeProvider.search (real web_search) lands in Phase 5 stage 2")
```

In `class OpenAICompatProvider`, after its `fanout` method (`:134-138`), add:

```python
    def search(self, subquery: str, *, subquestion_id: str = "Q0", model_tier: str = "cheap") -> dict:
        raise NotImplementedError(
            "web_search is Anthropic-specific; OpenAICompatProvider has no search backend")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_providers_search.py -k not_implemented -v`
Expected: PASS (2 tests).

- [ ] **Step 5: Commit**

```bash
git add runner/providers.py tests/test_providers_search.py
git commit -m "feat(retrieval): Claude/OpenAI search() -> NotImplementedError (Stage 1 guard)

Живой web_search — Stage 2. Пока обе ветки падают громко, чтобы плейсхолдер
нельзя было принять за рабочий путь."
```

---

## Task 4: Wire `orchestrator.search()` to use `provider.search()`

**Files:**
- Modify: `runner/orchestrator.py:112-143` (the `search` method — `run_round` closure and source-writing block)
- Test: `tests/test_orchestrator_search.py` (create)

- [ ] **Step 1: Read the current method to anchor the edit**

Run: `sed -n '112,143p' runner/orchestrator.py`
Expected: you see the `run_round` closure that calls `self.p.fanout(...)` and discards it (`:122`), returns `[{"subquestion_id": f"Q{i}", "sources": [], "signals": {}} ...]` (`:123-124`), and the source loop writing `https://example.com/source-{i}` (`:130-143`). Confirm line numbers before editing (they may have shifted by earlier tasks — but earlier tasks only touched `providers.py`, so `:112-143` should hold).

- [ ] **Step 2: Write the failing integration test**

Create `tests/test_orchestrator_search.py`. The verified facts (from `runner/orchestrator.py`): `Orchestrator(provider)` takes a provider; `RunState` is a `@dataclass` constructed directly as `RunState(question=..., depth=..., root=...)`; `s.dir` is a property `root / slug`; the pipeline runs `reframe(s)` → `choose_genre(s)` → `plan(s)` (which creates `s.dir`) **before** `search(s)`, and all three are required for `s` to be valid for `search`.

```python
from runner.orchestrator import Orchestrator, RunState
from runner.providers import DryRunProvider


def _ready_state(tmp_path, depth="medium"):
    """Build a RunState advanced to the point search() expects: reframe -> genre -> plan."""
    orch = Orchestrator(DryRunProvider())
    s = RunState(question="test question about widgets", depth=depth, root=tmp_path)
    orch.reframe(s)        # sets s.slug, s.hypotheses
    orch.choose_genre(s)   # sets s.genre
    orch.plan(s)           # creates s.dir, writes plan.md
    return orch, s


def test_search_populates_real_sources_not_placeholder(tmp_path):
    orch, s = _ready_state(tmp_path)
    orch.search(s)
    # sources came from provider.search() blobs, not a hardcoded loop
    assert s.sources, "expected sources written"
    # deviations.md was produced by the loop
    assert (s.dir / "deviations.md").exists()
    # DryRun fires no signals -> loop exits after round 1 (nothing pursued)
    assert all(d.status != "pursued" for d in s.deviations) or s.deviations == []


def test_search_handles_zero_fanout_depth(tmp_path):
    # shallow depth has DEPTH_FANOUT["shallow"]=0; max(1,k) must still yield one search round.
    orch, s = _ready_state(tmp_path, depth="shallow")
    orch.search(s)  # must not crash
    assert (s.dir / "sources.csv").exists()
    assert (s.dir / "deviations.md").exists()
```

If the import of `RunState` fails, confirm its name in `runner/orchestrator.py` (it is a top-level `@dataclass` near line 60). Do NOT invent fields — `RunState(question, depth, root)` is the full required signature; the rest default.

- [ ] **Step 3: Run test to verify it fails (for the right reason)**

Run: `pytest tests/test_orchestrator_search.py -v`
Expected: FAIL. If it fails on `_make_state` (wrong constructor), fix the helper first until it fails instead on the assertion `assert s.sources` or on `example.com`-placeholder behaviour — that is the real red.

- [ ] **Step 4: Rewrite the `run_round` closure and source-writing block**

In `runner/orchestrator.py`, replace the body of `search` (`:116-143`) so the closure calls `provider.search()` and sources come from the blobs. Target shape:

```python
    def search(self, s: RunState) -> None:
        n = DEPTH_SOURCES[s.depth]
        k = DEPTH_FANOUT[s.depth]
        collected: list[dict] = []

        def run_round(round_index, _round_depth, directives):
            blobs = [
                self.p.search(f"[r{round_index}] subtopic {i} for: {s.question}",
                              subquestion_id=f"Q{i}", model_tier="cheap")
                for i in range(max(1, k))
            ]
            collected.extend(blobs)
            return blobs

        deviations, _rounds = run_search_loop(self.p, s.depth, run_round)
        s.deviations = deviations
        write_deviations(s.dir, s.slug, deviations)

        # sources from collected blobs (dedup by url), capped at n
        srcdir = s.dir / "sources"
        srcdir.mkdir(exist_ok=True)
        seen: set[str] = set()
        flat = [src for blob in collected for src in blob.get("sources", [])]
        for i, src in enumerate(flat, start=1):
            if i > n or src["url"] in seen:
                continue
            seen.add(src["url"])
            sid = src.get("id", f"s{i:02d}")
            url = src["url"]
            stype = "Primary" if i % 2 else "Academic"
            s.sources.append({"id": sid, "url": url, "type": stype})
            fm = (f"---\nid: {sid}\nurl: {url}\ntitle: {src.get('title', 'Source')}\n"
                  f"access: OPEN\ntype: {stype}\n---\n{src.get('claim', '')}\n")
            (srcdir / f"{i:02d}_{sid}.md").write_text(fm, encoding="utf-8")

        rows = ["id,title,url,type,used"]
        rows += [f"{x['id']},Source {x['id']},{x['url']},{x['type']},Y" for x in s.sources]
        (s.dir / "sources.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")
```

IMPORTANT: keep whatever imports/helpers (`run_search_loop`, `write_deviations`, `DEPTH_SOURCES`, `DEPTH_FANOUT`, `RunState`) the method already used — they are unchanged. Only the closure and source-writing logic change.

- [ ] **Step 5: Run the integration test to verify it passes**

Run: `pytest tests/test_orchestrator_search.py -v`
Expected: PASS.

- [ ] **Step 6: Run the structure validator on a real scaffold run**

Produce a deep DryRun and validate it. Verified CLI (from `orchestrator.py` argparse): positional `question`, `--depth {shallow,medium,deep}`, `--provider dryrun`, `--out <dir>`.

Run:
```bash
python3 runner/orchestrator.py "structure check question" --depth deep --provider dryrun --out /tmp/p5run
python3 eval/validate_structure.py /tmp/p5run --strict; echo "exit: $?"
```
(If `validate_structure.py`'s arg form differs, check its `--help` — the point is: validate the produced run dir under `--strict`.)
Expected: validator `exit: 0` — no missing files or dead-URL structural failures introduced by sourcing from blobs.

- [ ] **Step 7: Commit**

```bash
git add runner/orchestrator.py tests/test_orchestrator_search.py
git commit -m "feat(retrieval): orchestrator.search() гоняет provider.search() вместо плейсхолдера

run_round теперь зовёт provider.search() per sub-agent; источники пишутся из
blob'ов (dedup по url), а не хардкодом example.com. Движок цикла не тронут."
```

---

## Task 5: Full regression + doc-gate

**Files:** none (verification only)

- [ ] **Step 1: Full test suite**

Run: `pytest -q`
Expected: previous baseline (82) **plus the 7 new tests** (3 in Task 2 + 2 in Task 3 + 2 in Task 4), 4 skipped unchanged → `89 passed, 4 skipped`. If any previously-passing test now fails, STOP and fix — the engine/tests must not regress. (If you added/split a test, adjust the count; the invariant is 82 prior + new, 4 skipped.)

- [ ] **Step 2: Doc-gate**

Run: `python3 scripts/stamp_docs.py --check; echo "exit: $?"`
Expected: `exit: 0`. (This task touched no `references/*.md` or `phases.yaml`, so the gate must stay green.)

- [ ] **Step 3: Mark the spec's Stage 1 done**

In `docs/superpowers/specs/2026-06-14-real-retrieval-search-design.md`, the Status line stays as-is, but add a one-line note under `## Goal` that Stage 1 is implemented (date it). Keep it factual.

- [ ] **Step 4: Final commit**

```bash
git add docs/superpowers/specs/2026-06-14-real-retrieval-search-design.md
git commit -m "docs(spec): пометить Phase 5 Stage 1 реализованным"
```

---

## Done criteria (Stage 1)

- `search()` is on the `LLMProvider` Protocol; `DryRunProvider` implements it as a deterministic fixture; `ClaudeProvider`/`OpenAICompatProvider` raise `NotImplementedError`.
- `orchestrator.search()` routes Phase-4 search through `provider.search()`; sources come from the returned blobs.
- `pytest -q` green (89 passed / 4 skipped target); `stamp_docs.py --check` exit 0; a scaffold run validates `--strict`.
- The loop in DryRun behaves exactly as before (exits after round 1, no triggers).

## NOT in this plan (Stage 2 — next plan)

- Real `ClaudeProvider.search()`: the two-call `web_search` flow (`web_search_20260209` without `format` → sources; then `output_config.format` with `SIGNALS_SCHEMA` → `{sources, signals}`). Needs live `ANTHROPIC_API_KEY` + an opt-in `-m live` smoke.
- `MAX_TOKENS` bump, `pause_turn` handling, `max_uses` tuning.
- `backfill outcome/new_source_ids` (`adaptive.py:262`), channels-from-`references/` in `plan.md`.
