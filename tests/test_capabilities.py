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
    audit = audit_env({"FRED_API_KEY": ""})
    fred = next(a for a in audit if a["key"] == "FRED_API_KEY")
    assert fred["present"] is False
