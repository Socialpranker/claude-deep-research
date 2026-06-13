from runner.adaptive import parse_signals, TRIGGERS, CHEAP_TRIGGERS, EXPENSIVE_TRIGGERS


def test_trigger_taxonomy_is_fixed():
    assert TRIGGERS == ("empty_result", "citation_lead", "unexpected_finding", "contradiction")
    assert CHEAP_TRIGGERS == ("empty_result", "citation_lead")
    assert EXPENSIVE_TRIGGERS == ("unexpected_finding", "contradiction")


def test_parse_signals_extracts_fired_triggers():
    blob = {
        "signals": {
            "empty_result": {"fired": True, "detail": "0 hits"},
            "citation_lead": {"fired": True, "detail": "S07 cites Gartner"},
            "unexpected_finding": {"fired": False, "detail": None},
            "contradiction": {"fired": False, "detail": None},
        }
    }
    fired, details = parse_signals(blob)
    assert fired == {"empty_result", "citation_lead"}
    assert details["empty_result"] == "0 hits"


def test_parse_signals_missing_block_is_no_flag():
    fired, details = parse_signals({"sources": []})
    assert fired == set()
    assert details == {}


def test_parse_signals_malformed_is_fail_safe():
    # signals present but not a dict, unknown keys, missing 'fired' -> ignored, no crash
    for bad in [{"signals": "oops"}, {"signals": {"weird": {"fired": True}}},
                {"signals": {"empty_result": {"detail": "x"}}}, {"signals": None}]:
        fired, details = parse_signals(bad)
        assert fired == set(), bad


from runner.adaptive import Budget, BUDGET_BY_DEPTH, class_of


def test_budget_by_depth_matches_spec():
    assert BUDGET_BY_DEPTH["shallow"] == (2, 0, 1)
    assert BUDGET_BY_DEPTH["medium"] == (4, 1, 1)
    assert BUDGET_BY_DEPTH["deep"] == (8, 3, 2)


def test_class_of_maps_triggers():
    assert class_of("empty_result") == "cheap"
    assert class_of("citation_lead") == "cheap"
    assert class_of("unexpected_finding") == "expensive"
    assert class_of("contradiction") == "expensive"


def test_budget_for_depth_seeds_counters():
    b = Budget.for_depth("medium")
    assert b.cheap == 4 and b.expensive == 1 and b.depth_limit == 1


def test_budget_spend_decrements_and_floors_at_zero():
    b = Budget.for_depth("deep")  # 8 / 3 / 2
    assert b.can_spend("cheap") is True
    b.spend("cheap")
    assert b.cheap == 7
    # drain expensive to zero
    b.spend("expensive"); b.spend("expensive"); b.spend("expensive")
    assert b.expensive == 0
    assert b.can_spend("expensive") is False
    # spending past zero is a programming error -> raises, never goes negative
    import pytest
    with pytest.raises(ValueError):
        b.spend("expensive")


def test_budget_shallow_has_no_expensive():
    b = Budget.for_depth("shallow")  # 2 / 0 / 1
    assert b.can_spend("expensive") is False
    assert b.can_spend("cheap") is True


def test_budget_depth_limit_gate():
    b = Budget.for_depth("medium")  # depth_limit 1
    assert b.depth_ok(0) is True   # round 1 -> spawning a depth-1 round is allowed
    assert b.depth_ok(1) is False  # at the limit, no further spawn
