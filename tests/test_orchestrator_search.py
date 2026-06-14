import re

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
    # provenance: urls come from provider.search() blobs (hash-derived shape),
    # not the old /source-{i} placeholder that this change deleted.
    assert any(re.search(r"/source-[0-9a-f]{8}-\d", x["url"]) for x in s.sources), \
        "expected hash-derived fixture urls, not the deleted /source-{i} placeholder"
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
