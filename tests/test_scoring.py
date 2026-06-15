from runner.scoring import compute_total, render_triangulation, triangulate

def test_compute_total_sums_three_axes():
    assert compute_total({"credibility": 5, "recency": 4, "bias": 3}) == 12

def test_compute_total_none_when_axis_missing():
    assert compute_total({"credibility": 5, "recency": 4}) is None

def test_triangulate_flags_under_when_fewer_than_three_distinct_types():
    scored = [
        {"id": "s01", "type": "Forum", "hypothesis_evidence": {"H1": "supports"}},
        {"id": "s02", "type": "Forum", "hypothesis_evidence": {"H1": "supports"}},
    ]
    result = triangulate(scored, ["H1: claim"])
    h1 = next(h for h in result if h["id"] == "H1")
    assert h1["distinct_types_supporting"] == 1
    assert h1["under_triangulated"] is True

def test_triangulate_not_under_with_three_distinct_types():
    scored = [
        {"id": "s01", "type": "Primary", "hypothesis_evidence": {"H1": "supports"}},
        {"id": "s02", "type": "Academic", "hypothesis_evidence": {"H1": "supports"}},
        {"id": "s03", "type": "Forum", "hypothesis_evidence": {"H1": "supports"}},
    ]
    h1 = next(h for h in triangulate(scored, ["H1: claim"]) if h["id"] == "H1")
    assert h1["distinct_types_supporting"] == 3
    assert h1["under_triangulated"] is False

def test_triangulate_counts_contradicting_separately():
    scored = [
        {"id": "s01", "type": "Primary", "hypothesis_evidence": {"H1": "contradicts"}},
        {"id": "s02", "type": "Academic", "hypothesis_evidence": {"H1": "supports"}},
    ]
    h1 = next(h for h in triangulate(scored, ["H1: claim"]) if h["id"] == "H1")
    assert h1["distinct_types_supporting"] == 1
    assert h1["distinct_types_contradicting"] == 1


def test_render_triangulation_has_header_and_row_per_hypothesis():
    rows = [
        {"id": "H1", "distinct_types_supporting": 3, "distinct_types_contradicting": 0,
         "under_triangulated": False, "note": "well supported"},
        {"id": "H2", "distinct_types_supporting": 1, "distinct_types_contradicting": 2,
         "under_triangulated": True, "note": "single voice"},
    ]
    md = render_triangulation("my topic", rows)
    assert "# Triangulation — my topic" in md
    assert "| H1 |" in md and "| H2 |" in md
    assert "⚠️" in md
    assert md.count("⚠️") == 1


def test_render_triangulation_empty_still_has_header():
    md = render_triangulation("topic", [])
    assert "# Triangulation — topic" in md
