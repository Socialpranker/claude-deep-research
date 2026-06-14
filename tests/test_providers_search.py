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
