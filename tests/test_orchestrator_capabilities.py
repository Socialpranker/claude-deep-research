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
    assert "## Hypotheses" in plan  # original plan body preserved (append, not overwrite)
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
