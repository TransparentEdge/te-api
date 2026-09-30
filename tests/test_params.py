"""Tests for the --file parameter helpers."""

from __future__ import annotations

import json

import click
import pytest

from te_api.params import encode_param, load_param_file, merge_params, option_flag


# -- load_param_file --


def test_no_path_yields_no_params():
    """Commands pass the option straight through, unset included."""
    assert load_param_file(None) == {}
    assert load_param_file("") == {}


def test_loads_a_json_object(tmp_path):
    """A JSON object maps parameter names to values."""
    f = tmp_path / "q.json"
    f.write_text(json.dumps({"filters": {"vhost": ["www.example.com"]}}))

    assert load_param_file(str(f)) == {"filters": {"vhost": ["www.example.com"]}}


def test_unreadable_file_is_a_usage_error(tmp_path):
    """A missing file is the caller's mistake, not a traceback."""
    with pytest.raises(click.UsageError, match="Cannot read"):
        load_param_file(str(tmp_path / "nope.json"))


def test_invalid_json_is_a_usage_error(tmp_path):
    """Broken JSON reports where it broke."""
    f = tmp_path / "q.json"
    f.write_text("{not json")

    with pytest.raises(click.UsageError, match="not valid JSON"):
        load_param_file(str(f))


def test_non_object_json_is_a_usage_error(tmp_path):
    """A bare list or scalar cannot name parameters."""
    f = tmp_path / "q.json"
    f.write_text('["filters"]')

    with pytest.raises(click.UsageError, match="must hold a JSON object"):
        load_param_file(str(f))


# -- encode_param --


def test_structured_values_become_compact_json():
    """Object and array parameters travel as JSON in the query string."""
    encoded = encode_param({"timestamp": {"from": 1, "to": 2}})
    assert encoded == '{"timestamp":{"from":1,"to":2}}'
    assert encode_param(["a", "b"]) == '["a","b"]'


def test_scalars_pass_through():
    """A value already given as a string is left exactly as it was."""
    assert encode_param('{"already":"encoded"}') == '{"already":"encoded"}'
    assert encode_param(7) == 7


def test_booleans_become_query_string_literals():
    """Python's True would reach the API as 'True' otherwise."""
    assert encode_param(True) == "true"
    assert encode_param(False) == "false"


# -- merge_params --


def test_file_fills_in_what_the_command_line_left_out():
    params = {"filters": None, "result_size": None}
    file_params = {"filters": {"vhost": ["a"]}}

    merged = merge_params(params, file_params, known=("filters", "result_size"))

    assert merged == {"filters": '{"vhost":["a"]}'}


def test_command_line_wins_over_the_file():
    """Explicit options beat the file, so one can be overridden ad hoc."""
    params = {"filters": '{"vhost":["cli"]}'}
    file_params = {"filters": {"vhost": ["file"]}}

    merged = merge_params(params, file_params, known=("filters",))

    assert merged == {"filters": '{"vhost":["cli"]}'}


def test_unknown_keys_are_rejected():
    """A typo must surface, not silently drop a filter."""
    with pytest.raises(click.UsageError, match="does not accept: vhost"):
        merge_params({"filters": None}, {"vhost": ["a"]}, known=("filters",))


def test_required_params_may_come_from_the_file():
    """The whole point: a required parameter need not be on the command line."""
    merged = merge_params(
        {"filters": None},
        {"filters": {"vhost": ["a"]}},
        known=("filters",),
        required=("filters",),
    )

    assert "filters" in merged


def test_required_params_missing_everywhere_is_a_usage_error():
    """Relaxing click's required= must not lose the error."""
    with pytest.raises(click.UsageError, match=r"Missing required parameter\(s\): --filters"):
        merge_params({"filters": None}, {}, known=("filters",), required=("filters",))


def test_none_values_are_dropped():
    """Unset options must not reach the API as empty query parameters."""
    merged = merge_params({"a": 1, "b": None}, {}, known=("a", "b"))
    assert merged == {"a": 1}


# -- option_flag --


def test_option_flag_is_kebab_case():
    assert option_flag("result_size") == "--result-size"
    assert option_flag("filters") == "--filters"


# -- load_body --


def test_load_body_without_either_is_none():
    from te_api.params import load_body

    assert load_body(None, None) is None


def test_load_body_inline():
    from te_api.params import load_body

    assert load_body('{"a": 1}', None) == {"a": 1}


def test_load_body_from_file(tmp_path):
    from te_api.params import load_body

    path = tmp_path / "body.json"
    path.write_text('[1, 2]')

    assert load_body(None, str(path)) == [1, 2]


def test_load_body_from_stdin(monkeypatch):
    import io

    from te_api.params import load_body

    monkeypatch.setattr("sys.stdin", io.StringIO('{"from": "stdin"}'))

    assert load_body(None, "-") == {"from": "stdin"}


def test_load_body_rejects_both():
    import click
    import pytest

    from te_api.params import load_body

    with pytest.raises(click.UsageError, match="not both"):
        load_body("{}", "x.json")


def test_load_body_reports_invalid_json_as_usage_error():
    import click
    import pytest

    from te_api.params import load_body

    with pytest.raises(click.UsageError, match="--json-body is not valid JSON"):
        load_body("{oops", None)


def test_load_body_reports_a_missing_file_as_usage_error(tmp_path):
    import click
    import pytest

    from te_api.params import load_body

    with pytest.raises(click.UsageError, match="Cannot read --body-file"):
        load_body(None, str(tmp_path / "nope.json"))
