# Real Retrieval Stage 2 — live `ClaudeProvider.search()` Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the `NotImplementedError` in `ClaudeProvider.search()` with a live two-call `web_search` flow that returns a blob in the exact shape `runner.adaptive.parse_signals` consumes.

**Architecture:** Two sequential `messages.create` calls per search. Call 1 runs the `web_search_20260209` server tool (no structured output) and collects answer text + raw sources. Call 2 takes that text+sources as **plain user text** (never the raw tool-result blocks — citations + `output_config.format` = 400) and returns strict JSON `{sources, signals}` via `SIGNALS_SCHEMA`. The search model is hard-resolved to `mid` (`claude-sonnet-4-6`) because the `cheap` tier (`claude-haiku-4-5`) is not in the docs' `web_search_20260209` support list. All tests mock a fake `anthropic` client; the live path is an opt-in `-m live` smoke.

**Tech Stack:** Python 3.14, `anthropic` SDK, pytest (`-m live` marker registered in `pytest.ini`).

**Spec:** [docs/superpowers/specs/2026-06-14-real-retrieval-search-stage2-design.md](../specs/2026-06-14-real-retrieval-search-stage2-design.md)

---

## File Structure

- **`runner/providers.py`** (modify) — add module-level `SIGNALS_SCHEMA`; add a private helper `_search_model()` on `ClaudeProvider`; add private helpers to (a) collect sources+text from a call-1 response and (b) parse the call-2 JSON; replace `ClaudeProvider.search()` body (`:123-125`). `OpenAICompatProvider.search()` untouched.
- **`tests/test_providers_search.py`** (modify) — replace `test_claude_search_not_implemented_yet` (`:48-52`) with mock-based tests of the two-call flow. Add a tiny fake-client helper at the top of the file. Everything else stays untouched and green.
- **`tests/test_providers_live.py`** (modify) — add one opt-in `@pytest.mark.live` smoke for `search()`.

The fake client lives in the test file (not a shared fixture) — it's small and only this file needs it.

---

## Conventions used in every task

- Run tests from repo root `/Users/ivanteresenko/Downloads/claude-deep-research`.
- `ruff` is not installed in this environment (`python3 -m ruff` → "No module named ruff"); the project's lint gate runs elsewhere. Do **not** add a ruff step. The verification gate here is `pytest` + `scripts/stamp_docs.py --check`.
- `python3 -m pytest <args>` (the `pytest` entrypoint may not be on PATH; the module form is known-good — Stage 1 used it).
- Commit messages in Russian, conventional-commits prefix, per project convention. `git add` by explicit path, never `-A`.

---

### Task 1: `SIGNALS_SCHEMA` module constant

**Files:**
- Modify: `runner/providers.py` (add after the `SEARCH_TRIGGERS` / `MAX_TOKENS` block, around `:23`)
- Test: `tests/test_providers_search.py`

- [ ] **Step 1: Write the failing test**

Add to `tests/test_providers_search.py` (extend the existing import from `runner.providers` to include `SIGNALS_SCHEMA`):

```python
from runner.providers import (
    ClaudeProvider,
    DryRunProvider,
    OpenAICompatProvider,
    SEARCH_TRIGGERS,
    SIGNALS_SCHEMA,
)


def test_signals_schema_is_structured_output_safe():
    # Every object in the schema must forbid extra props and use no unsupported
    # keywords (minLength/maxLength/minimum/maximum/minItems) — structured outputs
    # reject those. Walk the schema and assert.
    UNSUPPORTED = {"minLength", "maxLength", "minimum", "maximum", "minItems", "maxItems"}

    def walk(node):
        if not isinstance(node, dict):
            return
        if node.get("type") == "object":
            assert node.get("additionalProperties") is False, f"missing additionalProperties:false in {node}"
        assert UNSUPPORTED.isdisjoint(node), f"unsupported keyword in {node}"
        for v in node.get("properties", {}).values():
            walk(v)
        if "items" in node:
            walk(node["items"])

    walk(SIGNALS_SCHEMA)
    # signals object lists exactly the 4 triggers, all required
    sig = SIGNALS_SCHEMA["properties"]["signals"]
    assert set(sig["properties"]) == set(SEARCH_TRIGGERS)
    assert set(sig["required"]) == set(SEARCH_TRIGGERS)
    # each trigger entry allows null detail
    entry = sig["properties"][SEARCH_TRIGGERS[0]]
    assert entry["properties"]["detail"]["type"] == ["string", "null"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_providers_search.py::test_signals_schema_is_structured_output_safe -v`
Expected: FAIL with `ImportError: cannot import name 'SIGNALS_SCHEMA'`.

- [ ] **Step 3: Write minimal implementation**

In `runner/providers.py`, after the `MAX_TOKENS = 4096` line (`:23`), add:

```python
# --- Stage 2: structured-output schema for the web_search signals call ---
# Constraints (Anthropic structured outputs): every object needs
# additionalProperties:false; no min/max length, no minItems, no recursion.
_SIGNAL_SCHEMA = {
    "type": "object",
    "properties": {
        "fired": {"type": "boolean"},
        "detail": {"type": ["string", "null"]},
    },
    "required": ["fired", "detail"],
    "additionalProperties": False,
}
_SOURCE_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "url": {"type": "string"},
        "title": {"type": "string"},
        "claim": {"type": "string"},
    },
    "required": ["id", "url", "title", "claim"],
    "additionalProperties": False,
}
SIGNALS_SCHEMA = {
    "type": "object",
    "properties": {
        "sources": {"type": "array", "items": _SOURCE_SCHEMA},
        "signals": {
            "type": "object",
            "properties": {t: _SIGNAL_SCHEMA for t in SEARCH_TRIGGERS},
            "required": list(SEARCH_TRIGGERS),
            "additionalProperties": False,
        },
    },
    "required": ["sources", "signals"],
    "additionalProperties": False,
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_providers_search.py::test_signals_schema_is_structured_output_safe -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add runner/providers.py tests/test_providers_search.py
git commit -m "feat(retrieval): SIGNALS_SCHEMA для structured-output вызова Stage 2

$(printf 'Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>')"
```

---

### Task 2: `_search_model()` — hard-resolve search to `mid`

**Files:**
- Modify: `runner/providers.py` (`ClaudeProvider`, add method after `_model_for` at `:105`)
- Test: `tests/test_providers_search.py`

- [ ] **Step 1: Write the failing test**

Add to `tests/test_providers_search.py`:

```python
def test_claude_search_model_is_mid_not_cheap():
    # Haiku (cheap) is not in the web_search_20260209 support list; search() must
    # resolve to mid (sonnet) regardless of the tier the orchestrator passes.
    p = ClaudeProvider(client=object())
    assert p._search_model("cheap") == "claude-sonnet-4-6"
    assert p._search_model("strong") == "claude-sonnet-4-6"


def test_claude_search_model_override_wins():
    p = ClaudeProvider(client=object(), model_override="claude-opus-4-8")
    assert p._search_model("cheap") == "claude-opus-4-8"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_providers_search.py::test_claude_search_model_is_mid_not_cheap -v`
Expected: FAIL with `AttributeError: 'ClaudeProvider' object has no attribute '_search_model'`.

- [ ] **Step 3: Write minimal implementation**

In `runner/providers.py`, in `ClaudeProvider`, after `_model_for` (ends `:105`), add:

```python
    def _search_model(self, tier: str) -> str:
        # web_search_20260209 is documented for opus/sonnet/fable, NOT haiku.
        # The orchestrator passes tier="cheap" (= haiku) for search; override to
        # mid (sonnet) which supports the tool. model_override still wins.
        return self.model_override or self.TIER_MODEL["mid"]
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_providers_search.py -k search_model -v`
Expected: 2 PASS.

- [ ] **Step 5: Commit**

```bash
git add runner/providers.py tests/test_providers_search.py
git commit -m "feat(retrieval): search() прибит к mid-модели (sonnet), не cheap

$(printf 'Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>')"
```

---

### Task 3: `_collect_call1(resp)` — extract answer text + raw sources from a call-1 response

**Files:**
- Modify: `runner/providers.py` (module-level private helper, near the bottom or above `ClaudeProvider`)
- Test: `tests/test_providers_search.py`

This helper turns a call-1 `messages.create` response into `(answer_text, raw_sources)`. `raw_sources` is a list of `{"url","title"}` dicts pulled from `web_search_tool_result` blocks; `answer_text` is the concatenation of `text` blocks (same pattern as `complete()`).

- [ ] **Step 1: Write the failing test**

First add a fake-block/response helper at the TOP of `tests/test_providers_search.py` (after imports), then the test:

```python
import types


def _block(**kw):
    # a content block as a simple attribute bag (mimics the SDK's block objects)
    return types.SimpleNamespace(**kw)


def _resp(content, stop_reason="end_turn"):
    return types.SimpleNamespace(content=content, stop_reason=stop_reason)


def test_collect_call1_pulls_text_and_sources():
    from runner.providers import _collect_call1
    resp = _resp([
        _block(type="text", text="Widgets market is ~$5B. "),
        _block(type="web_search_tool_result", content=[
            _block(type="web_search_result", url="https://acme.example/report", title="Acme Report"),
            _block(type="web_search_result", url="https://data.example/widgets", title="Widget Data"),
        ]),
        _block(type="text", text="Growth is 4%/yr."),
    ])
    text, sources = _collect_call1(resp)
    assert text == "Widgets market is ~$5B. Growth is 4%/yr."
    assert sources == [
        {"url": "https://acme.example/report", "title": "Acme Report"},
        {"url": "https://data.example/widgets", "title": "Widget Data"},
    ]


def test_collect_call1_handles_no_search():
    # model answered without searching -> empty sources, still returns text
    from runner.providers import _collect_call1
    resp = _resp([_block(type="text", text="No search needed.")])
    text, sources = _collect_call1(resp)
    assert text == "No search needed."
    assert sources == []
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_providers_search.py -k collect_call1 -v`
Expected: FAIL with `ImportError: cannot import name '_collect_call1'`.

- [ ] **Step 3: Write minimal implementation**

In `runner/providers.py`, add a module-level helper (above `class ClaudeProvider`):

```python
def _collect_call1(resp) -> tuple[str, list[dict]]:
    """From a web_search call-1 response, return (answer_text, raw_sources).

    raw_sources are {url, title} dicts harvested from web_search_tool_result
    blocks. Defensive: tolerate blocks missing url/title (skip), and a
    tool-result block whose .content is not a list.
    """
    texts: list[str] = []
    sources: list[dict] = []
    for block in getattr(resp, "content", []) or []:
        btype = getattr(block, "type", None)
        if btype == "text":
            texts.append(getattr(block, "text", ""))
        elif btype == "web_search_tool_result":
            for item in getattr(block, "content", []) or []:
                url = getattr(item, "url", None)
                if not url:
                    continue
                sources.append({"url": url, "title": getattr(item, "title", "") or ""})
    return "".join(texts), sources
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_providers_search.py -k collect_call1 -v`
Expected: 2 PASS.

- [ ] **Step 5: Commit**

```bash
git add runner/providers.py tests/test_providers_search.py
git commit -m "feat(retrieval): _collect_call1 — текст+источники из web_search ответа

$(printf 'Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>')"
```

---

### Task 4: `_parse_call2(resp, subquestion_id)` — parse structured JSON into a contract blob, fail-safe

**Files:**
- Modify: `runner/providers.py` (module-level private helper)
- Test: `tests/test_providers_search.py`

Turns a call-2 response (whose first text block is `SIGNALS_SCHEMA`-shaped JSON) into the final blob. On any parse failure / refusal, returns a well-formed blob with empty sources and all-`fired:false` signals (mirrors `parse_signals`' fail-safe — a bad cheap-model turn must never block the run).

- [ ] **Step 1: Write the failing test**

```python
import json


def test_parse_call2_happy_path():
    from runner.providers import _parse_call2
    payload = {
        "sources": [{"id": "s1", "url": "https://x.example", "title": "X", "claim": "c"}],
        "signals": {
            "empty_result": {"fired": False, "detail": None},
            "citation_lead": {"fired": True, "detail": "found a lead"},
            "unexpected_finding": {"fired": False, "detail": None},
            "contradiction": {"fired": False, "detail": None},
        },
    }
    resp = _resp([_block(type="text", text=json.dumps(payload))])
    blob = _parse_call2(resp, "Q2")
    assert blob["subquestion_id"] == "Q2"
    assert blob["sources"] == payload["sources"]
    assert blob["signals"]["citation_lead"] == {"fired": True, "detail": "found a lead"}


def test_parse_call2_failsafe_on_garbage():
    from runner.providers import _parse_call2
    from runner.providers import SEARCH_TRIGGERS
    resp = _resp([_block(type="text", text="I cannot help with that.")], stop_reason="refusal")
    blob = _parse_call2(resp, "Q0")
    assert blob["subquestion_id"] == "Q0"
    assert blob["sources"] == []
    # all triggers present, none fired
    assert set(blob["signals"]) == set(SEARCH_TRIGGERS)
    assert all(v == {"fired": False, "detail": None} for v in blob["signals"].values())
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_providers_search.py -k parse_call2 -v`
Expected: FAIL with `ImportError: cannot import name '_parse_call2'`.

- [ ] **Step 3: Write minimal implementation**

In `runner/providers.py`, add (above `class ClaudeProvider`, near `_collect_call1`):

```python
def _empty_signals() -> dict:
    return {t: {"fired": False, "detail": None} for t in SEARCH_TRIGGERS}


def _parse_call2(resp, subquestion_id: str) -> dict:
    """Parse the structured-output call-2 response into a contract blob.

    Fail-safe: malformed JSON, a refusal, or a missing signals block yields a
    valid blob with empty sources and all-fired:false signals — never raises,
    so one bad cheap-model turn can't break the loop (mirrors parse_signals).
    subquestion_id is always the caller's value, never the model's.
    """
    text = "".join(
        getattr(b, "text", "") for b in (getattr(resp, "content", []) or [])
        if getattr(b, "type", None) == "text"
    )
    try:
        data = json.loads(text)
        assert isinstance(data, dict)
    except (ValueError, AssertionError):
        return {"subquestion_id": subquestion_id, "sources": [], "signals": _empty_signals()}

    sources = data.get("sources")
    if not isinstance(sources, list):
        sources = []
    signals = data.get("signals")
    if not isinstance(signals, dict):
        signals = _empty_signals()
    return {"subquestion_id": subquestion_id, "sources": sources, "signals": signals}
```

Also add `import json` to the top of `runner/providers.py` if not already present (check `:13-18`; Stage 1 imports are `concurrent.futures`, `hashlib`, `os`, `typing` — `json` is **not** there, so add it).

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_providers_search.py -k parse_call2 -v`
Expected: 2 PASS.

- [ ] **Step 5: Commit**

```bash
git add runner/providers.py tests/test_providers_search.py
git commit -m "feat(retrieval): _parse_call2 — JSON→blob с fail-safe на refusal/мусор

$(printf 'Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>')"
```

---

### Task 5: wire the two calls in `ClaudeProvider.search()`

**Files:**
- Modify: `runner/providers.py:123-125` (replace the `NotImplementedError` body)
- Test: `tests/test_providers_search.py` — replace `test_claude_search_not_implemented_yet`

- [ ] **Step 1: Write the failing test**

In `tests/test_providers_search.py`, **delete** `test_claude_search_not_implemented_yet` (`:48-52`) and add a scripted fake client + the flow tests:

```python
class _FakeClient:
    """Records each messages.create call and returns scripted responses in order."""
    def __init__(self, responses):
        self._responses = list(responses)
        self.calls = []
        self.messages = self  # so client.messages.create works

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return self._responses.pop(0)


def _call1_resp():
    return _resp([
        _block(type="text", text="Answer text. "),
        _block(type="web_search_tool_result", content=[
            _block(type="web_search_result", url="https://r.example", title="R"),
        ]),
    ])


def _call2_resp():
    payload = {
        "sources": [{"id": "s1", "url": "https://r.example", "title": "R", "claim": "c"}],
        "signals": {
            "empty_result": {"fired": False, "detail": None},
            "citation_lead": {"fired": True, "detail": "lead"},
            "unexpected_finding": {"fired": False, "detail": None},
            "contradiction": {"fired": False, "detail": None},
        },
    }
    return _resp([_block(type="text", text=json.dumps(payload))])


def test_claude_search_makes_two_calls_with_right_shapes():
    client = _FakeClient([_call1_resp(), _call2_resp()])
    p = ClaudeProvider(client=client)
    blob = p.search("widget market size", subquestion_id="Q4", model_tier="cheap")

    # exactly two create calls
    assert len(client.calls) == 2
    call1, call2 = client.calls

    # call 1: web_search tool, NO output_config; model is sonnet (mid)
    assert call1["model"] == "claude-sonnet-4-6"
    assert call1["tools"][0]["type"] == "web_search_20260209"
    assert "output_config" not in call1

    # call 2: structured output, NO tools
    assert call2["model"] == "claude-sonnet-4-6"
    assert call2["output_config"]["format"]["schema"] == SIGNALS_SCHEMA
    assert "tools" not in call2

    # blob shape + caller-owned subquestion_id
    assert blob["subquestion_id"] == "Q4"
    assert blob["sources"][0]["url"] == "https://r.example"
    assert set(blob["signals"]) == set(SEARCH_TRIGGERS)
    assert blob["signals"]["citation_lead"]["fired"] is True


def test_claude_search_call2_user_text_is_plain_not_tool_blocks():
    # The whole point of two calls: call 2 must NOT carry call-1's
    # web_search_tool_result blocks (citations + format = 400). Its messages
    # must be plain user text only.
    client = _FakeClient([_call1_resp(), _call2_resp()])
    p = ClaudeProvider(client=client)
    p.search("q", subquestion_id="Q0")
    call2 = client.calls[1]
    for msg in call2["messages"]:
        content = msg["content"]
        if isinstance(content, list):
            for block in content:
                assert block.get("type") != "web_search_tool_result"


def test_claude_search_blob_feeds_parse_signals():
    # Prove the returned blob actually mates with the loop's signal reader.
    from runner.adaptive import parse_signals
    client = _FakeClient([_call1_resp(), _call2_resp()])
    blob = ClaudeProvider(client=client).search("q", subquestion_id="Q1")
    fired, details = parse_signals(blob)
    assert "citation_lead" in fired
    assert details["citation_lead"] == "lead"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_providers_search.py -k claude_search -v`
Expected: FAIL — `NotImplementedError` raised by the current stub (tests call `search()` which still raises).

- [ ] **Step 3: Write minimal implementation**

Replace `ClaudeProvider.search()` body (`runner/providers.py:123-125`) with:

```python
    def search(self, subquery: str, *, subquestion_id: str = "Q0", model_tier: str = "cheap") -> dict:
        model = self._search_model(model_tier)

        # --- call 1: web_search, no structured output ---
        messages = [{"role": "user", "content": _SEARCH_PROMPT.format(subquery=subquery)}]
        resp = self.client.messages.create(
            model=model,
            max_tokens=MAX_TOKENS,
            tools=[{"type": "web_search_20260209", "name": "web_search"}],
            messages=messages,
        )
        # server-side tool loop may pause after N iterations; resume until terminal
        guard = 0
        while getattr(resp, "stop_reason", None) == "pause_turn" and guard < 5:
            guard += 1
            messages = [
                {"role": "user", "content": _SEARCH_PROMPT.format(subquery=subquery)},
                {"role": "assistant", "content": resp.content},
            ]
            resp = self.client.messages.create(
                model=model,
                max_tokens=MAX_TOKENS,
                tools=[{"type": "web_search_20260209", "name": "web_search"}],
                messages=messages,
            )
        answer_text, raw_sources = _collect_call1(resp)

        # --- call 2: structured output, NO web_search (citations + format = 400) ---
        # call-1 sources/text passed as PLAIN user text, never the tool-result blocks.
        rendered_sources = "\n".join(
            f"- {s['title']}: {s['url']}" for s in raw_sources
        ) or "(no sources found)"
        call2_prompt = _SIGNALS_PROMPT.format(
            subquery=subquery, answer=answer_text, sources=rendered_sources
        )
        resp2 = self.client.messages.create(
            model=model,
            max_tokens=MAX_TOKENS,
            output_config={"format": {"type": "json_schema", "schema": SIGNALS_SCHEMA}},
            messages=[{"role": "user", "content": call2_prompt}],
        )
        return _parse_call2(resp2, subquestion_id)
```

And add the two prompt constants near `SIGNALS_SCHEMA` (module level):

```python
_SEARCH_PROMPT = (
    "Search the web to answer this sub-question for a research report. "
    "Cite concrete sources.\n\nSub-question: {subquery}"
)
_SIGNALS_PROMPT = (
    "You just researched a sub-question. Return JSON matching the schema: a list "
    "of `sources` (id, url, title, claim) and a `signals` object. For each signal, "
    "set fired=true with a short detail only if it genuinely applies:\n"
    "- empty_result: the search found nothing useful\n"
    "- citation_lead: a source points to another worth chasing\n"
    "- unexpected_finding: a result contradicts the premise or surprises\n"
    "- contradiction: two sources disagree\n\n"
    "Sub-question: {subquery}\n\nYour findings:\n{answer}\n\nSources:\n{sources}"
)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_providers_search.py -v`
Expected: ALL pass (new flow tests + the untouched DryRun/taxonomy/openai tests). No `NotImplementedError` test remains for Claude.

- [ ] **Step 5: Commit**

```bash
git add runner/providers.py tests/test_providers_search.py
git commit -m "feat(retrieval): живой ClaudeProvider.search() — two-call web_search→signals

$(printf 'Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>')"
```

---

### Task 6: opt-in live smoke for `search()`

**Files:**
- Modify: `tests/test_providers_live.py` (add one test, follow the existing skipif pattern)

- [ ] **Step 1: Write the test** (no separate failing step — it's `-m live`, skipped by default)

Append to `tests/test_providers_live.py`:

```python
@pytest.mark.skipif(not os.environ.get("ANTHROPIC_API_KEY"), reason="no ANTHROPIC_API_KEY")
def test_claude_live_search():
    from runner.providers import SEARCH_TRIGGERS
    blob = ClaudeProvider().search(
        "What is the current stable version of Python?", subquestion_id="Q0"
    )
    assert blob["subquestion_id"] == "Q0"
    assert set(blob["signals"]) == set(SEARCH_TRIGGERS)
    assert isinstance(blob["sources"], list)
    # at least one real (non-example.com) source on a successful search
    assert any("example.com" not in s.get("url", "") for s in blob["sources"]) or blob["sources"] == []
```

- [ ] **Step 2: Confirm it's skipped in the normal run**

Run: `python3 -m pytest tests/test_providers_live.py -v`
Expected: all deselected/skipped (marker `live` not selected) — `1 skipped` or `deselected` for the new test, no network hit.

- [ ] **Step 3: Commit**

```bash
git add tests/test_providers_live.py
git commit -m "test(retrieval): opt-in live smoke для search() (-m live)

$(printf 'Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>')"
```

---

### Task 7: full regression + doc gate + memory update

**Files:** none (verification only) + memory file.

- [ ] **Step 1: Full test suite**

Run: `python3 -m pytest -q`
Expected: green — Stage-1 baseline was "89 passed / 4 skipped"; this stage **adds** tests and removes one (`test_claude_search_not_implemented_yet`). Net expected: all pass, 4 skipped (the live ones). Confirm no Claude `NotImplementedError` test failure.

- [ ] **Step 2: Doc gate**

Run: `python3 scripts/stamp_docs.py --check`
Expected: exit 0 (no doc-gen spans or phase counts touched by code/test changes).

- [ ] **Step 3: Re-run the signal-reader mate check explicitly** (defence-in-depth)

Run: `python3 -m pytest tests/test_providers_search.py::test_claude_search_blob_feeds_parse_signals tests/test_adaptive.py -q`
Expected: green — proves the live blob shape still satisfies the loop engine and the adaptive tests are untouched.

- [ ] **Step 4: Update project memory**

Edit `~/.claude/projects/-Users-ivanteresenko-Downloads-claude-deep-research/memory/phase5-stage2-design.md`: change status from "design" to "IMPLEMENTED" with the date and the final `pytest -q` result. Update the `MEMORY.md` pointer line accordingly.

- [ ] **Step 5: No commit here** — verification + memory only. (Memory lives outside the repo.) Stage 2 code was already committed task-by-task. **Do not push or open a PR** — outward-facing actions stay with the user.

---

## Self-Review (done by plan author)

**Spec coverage** — every spec section maps to a task:
- two-call flow → Task 5; search model = mid → Task 2; `SIGNALS_SCHEMA` shape → Task 1; "call 2 must not replay messages" → Task 5 + `test_claude_search_call2_user_text_is_plain_not_tool_blocks`; `subquestion_id` ownership → Task 4/5; `pause_turn` → Task 5; refusal/malformed fail-safe → Task 4; live smoke → Task 6; regression + doc gate → Task 7; `parse_signals` round-trip → Task 5.
- Edge cases from spec: "no web_search_tool_result" → `test_collect_call1_handles_no_search`; "malformed/refusal call 2" → `test_parse_call2_failsafe_on_garbage`.

**Placeholder scan** — no TBD/TODO; every code step has complete code. Prompts are concrete strings.

**Type consistency** — `_search_model`, `_collect_call1`, `_parse_call2`, `_empty_signals`, `SIGNALS_SCHEMA`, `_SEARCH_PROMPT`, `_SIGNALS_PROMPT` are named identically across the tasks that define and use them. Blob keys (`subquestion_id`/`sources`/`signals`) match `parse_signals` (verified verbatim against `adaptive.py`). Signal entry shape `{fired, detail}` matches schema and `parse_signals`.

**Known follow-through:** Task 5 deletes `test_claude_search_not_implemented_yet` (it would fail once the stub is gone) — this is intended and called out in the spec.
