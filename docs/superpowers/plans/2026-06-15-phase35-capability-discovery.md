# Phase 3.5 — Capability Discovery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Добавить Phase 3.5 (`Orchestrator.discover_capabilities`) — детерминированный аудит 18 env-ключей + LLM-маппинг подтем→источники, дописываемый блоком в `plan.md`, за гейтом `depth != "shallow"`.

**Architecture:** Чистый модуль `runner/capabilities.py` (`audit_env`, `render_capabilities`) без сети — паттерн `runner/scoring.py`. Метод `Orchestrator.discover_capabilities(s)` зовёт `audit_env(os.environ)`, затем `self.p.complete(prompt, model_tier="mid")` для маппинга, и дописывает (append) блок в `plan.md`. Вызывается в `run()` между `plan()` и `search()` за гейтом по depth.

**Tech Stack:** Python 3, pytest, ruff. Оркестратор — `runner/orchestrator.py`. Провайдеры — `runner/providers.py` (`complete(prompt, *, model_tier)`).

**Spec:** [docs/superpowers/specs/2026-06-15-phase35-capability-discovery-design.md](../specs/2026-06-15-phase35-capability-discovery-design.md)

---

## File Structure

- **`runner/capabilities.py`** (create) — чистая логика без сети: `KNOWN_KEYS` (18 имён), `audit_env(env) -> list[dict]`, `render_capabilities(audit, mapping_text) -> str`. Мирроринг `runner/scoring.py`.
- **`runner/orchestrator.py`** (modify) — `RunState` получает поле `capabilities`; новый метод `discover_capabilities(s)`; `run()` зовёт его за гейтом; добавить `import os`.
- **`tests/test_capabilities.py`** (create) — юнит-тесты `audit_env` / `render_capabilities`.
- **`tests/test_orchestrator_capabilities.py`** (create) — интеграция `discover_capabilities` + гейт по depth в `run()`.

---

### Task 1: `runner/capabilities.py` — `audit_env`

**Files:**
- Create: `runner/capabilities.py`
- Test: `tests/test_capabilities.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_capabilities.py
from runner.capabilities import KNOWN_KEYS, audit_env

def test_audit_env_marks_present_key():
    audit = audit_env({"FRED_API_KEY": "abc"})
    fred = next(a for a in audit if a["key"] == "FRED_API_KEY")
    assert fred["present"] is True

def test_audit_env_marks_absent_keys():
    audit = audit_env({"FRED_API_KEY": "abc"})
    github = next(a for a in audit if a["key"] == "GITHUB_TOKEN")
    assert github["present"] is False

def test_audit_env_empty_env_all_absent():
    audit = audit_env({})
    assert all(a["present"] is False for a in audit)

def test_audit_env_covers_all_known_keys():
    audit = audit_env({})
    assert {a["key"] for a in audit} == set(KNOWN_KEYS)
    assert len(KNOWN_KEYS) == 18

def test_audit_env_empty_string_is_absent():
    # an exported-but-empty var is not a usable key
    audit = audit_env({"FRED_API_KEY": ""})
    fred = next(a for a in audit if a["key"] == "FRED_API_KEY")
    assert fred["present"] is False
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_capabilities.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'runner.capabilities'`

- [ ] **Step 3: Write minimal implementation**

```python
# runner/capabilities.py
"""Phase 3.5 — pure capability-discovery logic (no network).

Mirrors runner.scoring: deterministic helpers live here; the LLM-facing mapping
call lives in the orchestrator method discover_capabilities(). audit_env takes the
environment explicitly so it is testable by injection (never reads os.environ here).
"""
from __future__ import annotations

# 18 known API-key env vars from references/capability_discovery.md.
KNOWN_KEYS: tuple[str, ...] = (
    "FRED_API_KEY", "GITHUB_TOKEN", "BRAVE_API_KEY", "TAVILY_API_KEY",
    "EXA_API_KEY", "SERPAPI_KEY", "NEWSAPI_KEY", "ALPHA_VANTAGE_KEY",
    "CRUNCHBASE_API_KEY", "OPENWEATHER_KEY", "ETHERSCAN_KEY", "STACKEXCHANGE_KEY",
    "CENSUS_API_KEY", "COMPANIES_HOUSE_API_KEY", "NCBI_API_KEY",
    "SEMANTIC_SCHOLAR_API_KEY", "DUNE_API_KEY", "NASA_API_KEY",
)


def audit_env(env: dict) -> list[dict]:
    """For each known key, whether it is present (non-empty) in `env`.
    Pure: takes env explicitly, never raises."""
    return [{"key": k, "present": bool(env.get(k))} for k in KNOWN_KEYS]
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_capabilities.py -q`
Expected: PASS (5 passed)

- [ ] **Step 5: Commit**

```bash
git add runner/capabilities.py tests/test_capabilities.py
git commit -m "feat(capabilities): чистый audit_env + KNOWN_KEYS (Phase 3.5)"
```

---

### Task 2: `runner/capabilities.py` — `render_capabilities`

**Files:**
- Modify: `runner/capabilities.py` (добавить `render_capabilities`)
- Test: `tests/test_capabilities.py` (добавить тесты)

- [ ] **Step 1: Write the failing test**

```python
# append to tests/test_capabilities.py
from runner.capabilities import render_capabilities

def test_render_capabilities_has_header_and_keys():
    audit = [{"key": "FRED_API_KEY", "present": True},
             {"key": "BRAVE_API_KEY", "present": False}]
    md = render_capabilities(audit, "Use FRED for macro context.")
    assert "## Capabilities check (Phase 3.5)" in md
    assert "✅ FRED_API_KEY" in md
    assert "❌ BRAVE_API_KEY" in md
    assert "Use FRED for macro context." in md

def test_render_capabilities_starts_with_blank_line_for_append():
    # block is appended to an existing plan.md, so it must start with a newline
    md = render_capabilities([{"key": "FRED_API_KEY", "present": True}], "m")
    assert md.startswith("\n")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_capabilities.py -k render_capabilities -q`
Expected: FAIL — `ImportError: cannot import name 'render_capabilities'`

- [ ] **Step 3: Write minimal implementation**

```python
# append to runner/capabilities.py
def render_capabilities(audit: list[dict], mapping_text: str) -> str:
    """Markdown block appended to plan.md. Leads with a blank line so it separates
    cleanly from the existing plan body."""
    lines = ["", "## Capabilities check (Phase 3.5)", "", "**API keys:**"]
    for a in audit:
        if a["present"]:
            lines.append(f"- ✅ {a['key']} — authenticated")
        else:
            lines.append(f"- ❌ {a['key']} — not set (fallback to standard web search)")
    lines += ["", "**Subtopic → source mapping:**", "", mapping_text, ""]
    return "\n".join(lines)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_capabilities.py -q`
Expected: PASS (7 passed)

- [ ] **Step 5: Commit**

```bash
git add runner/capabilities.py tests/test_capabilities.py
git commit -m "feat(capabilities): render_capabilities — markdown-блок для plan.md (Phase 3.5)"
```

---

### Task 3: `RunState.capabilities` + `Orchestrator.discover_capabilities()`

**Files:**
- Modify: `runner/orchestrator.py` (add `import os`; `RunState` field; new method; import from `runner.capabilities`)
- Test: `tests/test_orchestrator_capabilities.py`

**Context:** `plan()` writes `plan.md` via `write_text` (overwrite). `discover_capabilities` must APPEND to it (read existing + write back, or open in append mode). `RunState` currently ends with fields `round_source_ids` and `triangulation` plus a `dir` @property. Imports in `orchestrator.py` use a `try/except ImportError` pattern for `from runner...` modules (so the file runs both as a package and as a script) — follow it for the new import.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_orchestrator_capabilities.py
from runner.orchestrator import Orchestrator, RunState
from runner.providers import DryRunProvider
from runner.capabilities import KNOWN_KEYS

def test_discover_capabilities_writes_block_and_state(tmp_path):
    o = Orchestrator(DryRunProvider())
    s = RunState(question="impact of remote work", depth="medium", root=tmp_path)
    o.reframe(s)
    o.choose_genre(s)
    o.plan(s)
    o.discover_capabilities(s)

    plan = (s.dir / "plan.md").read_text(encoding="utf-8")
    assert "## Capabilities check (Phase 3.5)" in plan
    # the original plan body is preserved (append, not overwrite)
    assert "## Hypotheses" in plan
    assert len(s.capabilities) == len(KNOWN_KEYS)

def test_discover_capabilities_audits_real_env(tmp_path, monkeypatch):
    monkeypatch.setenv("FRED_API_KEY", "xyz")
    o = Orchestrator(DryRunProvider())
    s = RunState(question="q", depth="medium", root=tmp_path)
    o.reframe(s)
    o.choose_genre(s)
    o.plan(s)
    o.discover_capabilities(s)
    fred = next(a for a in s.capabilities if a["key"] == "FRED_API_KEY")
    assert fred["present"] is True
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_orchestrator_capabilities.py::test_discover_capabilities_writes_block_and_state -q`
Expected: FAIL — `AttributeError: 'Orchestrator' object has no attribute 'discover_capabilities'`

- [ ] **Step 3: Write minimal implementation**

(a) Add `import os` to the stdlib imports block in `runner/orchestrator.py` (near `import argparse` / `import re`):

```python
import os
```

(b) Add the capabilities import following the existing `try/except ImportError` pattern used for other `runner.*` imports:

```python
try:
    from runner.capabilities import audit_env, render_capabilities
except ImportError:  # run as a script
    from capabilities import audit_env, render_capabilities
```

(c) In `RunState`, after the `triangulation` field, add:

```python
    capabilities: list = field(default_factory=list)  # Phase 3.5: env-key audit
```

(d) Add the method to `Orchestrator`, placed AFTER `plan()` and BEFORE `search()`:

```python
    # --- Phase 3.5: capability discovery -----------------------------------
    def discover_capabilities(self, s: RunState) -> None:
        s.capabilities = audit_env(dict(os.environ))
        available = [a["key"] for a in s.capabilities if a["present"]]
        prompt = (
            "Map the research subtopics to information sources, given the available "
            "API keys. For any source whose key is missing, note the fallback.\n\n"
            f"Question: {s.question}\n"
            f"Hypotheses:\n" + "\n".join(f"- {h}" for h in s.hypotheses) + "\n\n"
            f"Available API keys: {', '.join(available) or '(none)'}\n"
        )
        mapping = self.p.complete(prompt, model_tier="mid")
        block = render_capabilities(s.capabilities, mapping)
        plan_path = s.dir / "plan.md"
        existing = plan_path.read_text(encoding="utf-8")
        plan_path.write_text(existing + block, encoding="utf-8")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_orchestrator_capabilities.py -q`
Expected: PASS (2 passed)

- [ ] **Step 5: Commit**

```bash
git add runner/orchestrator.py tests/test_orchestrator_capabilities.py
git commit -m "feat(orchestrator): Phase 3.5 discover_capabilities() — аудит + маппинг в plan.md"
```

---

### Task 4: подключить `discover_capabilities()` в `run()` за гейтом по depth

**Files:**
- Modify: `runner/orchestrator.py` (`run()`)
- Test: `tests/test_orchestrator_capabilities.py`

**Context:** Phase 3.5 is mandatory for medium+deep, skipped for shallow. The gate is `if s.depth != "shallow"`. Current `run()`:

```python
    def run(self, question: str, depth: str, root: Path) -> Path:
        s = RunState(question=question, depth=depth, root=root)
        self.reframe(s)
        self.choose_genre(s)
        self.plan(s)
        self.search(s)
        self.score(s)
        self.synthesize(s)
        return s.dir
```

- [ ] **Step 1: Write the failing test**

```python
# append to tests/test_orchestrator_capabilities.py
def test_run_includes_capabilities_for_medium(tmp_path):
    o = Orchestrator(DryRunProvider())
    out = o.run("does remote work help", "medium", tmp_path)
    plan = (out / "plan.md").read_text(encoding="utf-8")
    assert "## Capabilities check (Phase 3.5)" in plan

def test_run_skips_capabilities_for_shallow(tmp_path):
    o = Orchestrator(DryRunProvider())
    out = o.run("does remote work help", "shallow", tmp_path)
    plan = (out / "plan.md").read_text(encoding="utf-8")
    assert "## Capabilities check (Phase 3.5)" not in plan
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_orchestrator_capabilities.py::test_run_includes_capabilities_for_medium -q`
Expected: FAIL — no "Capabilities check" block (run() doesn't call discover_capabilities yet)

- [ ] **Step 3: Write minimal implementation**

In `run()`, insert the gated call between `self.plan(s)` and `self.search(s)`:

```python
        self.plan(s)
        if s.depth != "shallow":
            self.discover_capabilities(s)
        self.search(s)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_orchestrator_capabilities.py -q`
Expected: PASS (4 passed)

Also confirm no regression across the suite:

Run: `python3 -m pytest tests/ -m "not live" -q`
Expected: PASS (all green)

- [ ] **Step 5: Commit**

```bash
git add runner/orchestrator.py tests/test_orchestrator_capabilities.py
git commit -m "feat(orchestrator): run() зовёт Phase 3.5 за гейтом depth != shallow"
```

---

### Task 5: финальная верификация

**Files:** none (verification only)

- [ ] **Step 1: Run full test suite**

Run: `python3 -m pytest tests/ -m "not live" -q`
Expected: PASS (all green, live deselected)

- [ ] **Step 2: Run ruff (CI gate)**

Run: `ruff check runner/ tests/`
Expected: no violations

- [ ] **Step 3: Re-read the spec line by line**

Open `docs/superpowers/specs/2026-06-15-phase35-capability-discovery-design.md` and confirm each requirement maps to a shipped change. Note any gap explicitly.

- [ ] **Step 4: (optional) end-to-end smoke on DryRun**

```bash
python3 -c "
import tempfile, pathlib
from runner.orchestrator import Orchestrator, RunState
from runner.providers import DryRunProvider
d = pathlib.Path(tempfile.mkdtemp())
out = Orchestrator(DryRunProvider()).run('impact of remote work on productivity', 'medium', d)
print((out / 'plan.md').read_text())
"
```
Expected: plan.md ends with the Capabilities check block (18 keys + mapping paragraph).

---

## Self-Review notes

- **Spec coverage:** audit 18 env keys (T1, `KNOWN_KEYS`==18) ✓; LLM mapping via complete/mid (T3 prompt) ✓; append to plan.md not overwrite (T3 read+write, T3 test asserts `## Hypotheses` preserved) ✓; `s.capabilities` state (T3) ✓; gate `depth != shallow` (T4, both medium-includes and shallow-skips tests) ✓; render block format with ✅/❌ (T2) ✓.
- **Narrow boundary:** no WebFetch awesome-lists, no interactive Y/n — neither appears in any task. ✓
- **Type consistency:** `audit_env` returns `list[dict]` with keys `key`/`present`; `render_capabilities` and `discover_capabilities` read exactly those keys; `KNOWN_KEYS` referenced consistently in T1/T3 tests.
- **Pattern fidelity:** `try/except ImportError` import (T3) matches existing orchestrator imports; `import os` added because it's currently absent.
