import json
import subprocess
from runner.orchestrator import Orchestrator, RunState
from runner.providers import DryRunProvider


def _prep(tmp_path, depth="medium"):
    o = Orchestrator(DryRunProvider())
    s = RunState(question="does X cause Y", depth=depth, root=tmp_path)
    o.reframe(s)
    o.choose_genre(s)
    o.plan(s)
    o.search(s)
    o.score(s)
    o.synthesize(s)
    return o, s


def _report_path(s):
    import datetime as dt
    return s.dir / f"{dt.date.today().isoformat()}_{s.genre}.md"


def test_verify_replaces_placeholder_with_metric(tmp_path, monkeypatch):
    o, s = _prep(tmp_path)
    def fake_run(cmd, **kwargs):
        out_idx = cmd.index("--out") + 1
        base = cmd[out_idx]
        from pathlib import Path
        jp = Path(base).with_suffix(".json")
        jp.parent.mkdir(parents=True, exist_ok=True)
        jp.write_text(json.dumps({
            "citation_integrity": 1.0,
            "results": [{"sid": "s01", "alive": True, "red_flag": False}],
        }), encoding="utf-8")
        return subprocess.CompletedProcess(cmd, 0)
    monkeypatch.setattr(subprocess, "run", fake_run)

    o.verify(s)
    report = _report_path(s).read_text(encoding="utf-8")
    assert "1/1 verified" in report
    assert "pending — run eval/check_citations.py" not in report


def test_verify_unavailable_when_no_json(tmp_path, monkeypatch):
    o, s = _prep(tmp_path)
    monkeypatch.setattr(subprocess, "run",
                        lambda cmd, **kw: subprocess.CompletedProcess(cmd, 0))
    o.verify(s)
    report = _report_path(s).read_text(encoding="utf-8")
    assert "verification unavailable" in report


def test_verify_survives_subprocess_oserror(tmp_path, monkeypatch):
    o, s = _prep(tmp_path)
    def boom(cmd, **kw):
        raise OSError("no python")
    monkeypatch.setattr(subprocess, "run", boom)
    o.verify(s)  # must NOT raise
    report = _report_path(s).read_text(encoding="utf-8")
    assert "verification unavailable" in report
