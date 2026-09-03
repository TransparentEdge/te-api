"""Tests for how the generator wires the --file option into commands."""

from __future__ import annotations

from te_api.builder import (
    generate_function_code,
    generate_merged_function_code,
    param_file_option,
)


def _query_param(name, required=False, param_type="string"):
    return {
        "name": name,
        "in": "query",
        "required": required,
        "schema": {"type": param_type},
        "description": f"The {name}",
    }


def _path_param(name):
    return {
        "name": name,
        "in": "path",
        "required": True,
        "schema": {"type": "string"},
        "description": f"The {name}",
    }


# -- param_file_option --


def test_no_option_without_query_params():
    """There would be nothing for the file to carry."""
    assert param_file_option([], set()) == (None, None)


def test_flag_is_file_by_default():
    var, flag = param_file_option(["filters"], set())
    assert flag == "--file"
    assert var == "param_file"


def test_flag_avoids_colliding_with_a_real_file_parameter():
    """An endpoint with its own 'file' parameter must not get two --file."""
    _, flag = param_file_option(["file", "filters"], set())
    assert flag == "--params-file"


def test_variable_name_avoids_collision():
    var, _ = param_file_option(["filters"], {"param_file"})
    assert var == "param_file_1"


# -- generate_function_code --


def test_command_with_query_params_gets_the_option():
    code = generate_function_code(
        "get_waf",
        "/v2/statistics/waf/",
        "get",
        {"summary": "WAF statistics", "parameters": [_query_param("filters", required=True)]},
    )

    assert "@click.option('--file', 'param_file'" in code
    assert "file_params = load_param_file(param_file)" in code
    assert "known=('filters',)" in code
    assert "required=('filters',)" in code


def test_required_is_no_longer_enforced_by_click():
    """It moves to the merge, so --file alone can satisfy it."""
    code = generate_function_code(
        "get_waf",
        "/v2/statistics/waf/",
        "get",
        {"summary": "WAF statistics", "parameters": [_query_param("filters", required=True)]},
    )

    assert "required=True" not in code


def test_optional_query_params_are_not_reported_as_required():
    code = generate_function_code(
        "get_thing",
        "/v1/thing/",
        "get",
        {"summary": "Thing", "parameters": [_query_param("result_size", param_type="integer")]},
    )

    assert "known=('result_size',)" in code
    assert "required=()" in code


def test_command_without_query_params_gets_no_option():
    """Path-only commands stay as they were."""
    code = generate_function_code(
        "get_detail",
        "/v1/thing/{thing_id}/",
        "get",
        {"summary": "Detail", "parameters": [_path_param("thing_id")]},
    )

    assert "--file" not in code
    assert "load_param_file" not in code
    assert "params = {}" in code


# -- generate_merged_function_code --


def test_merged_command_gets_the_option_without_required():
    """The merged generator leaves required-ness to the server."""
    list_details = {"summary": "List", "parameters": [_query_param("filters", required=True)]}
    detail_details = {"summary": "Detail", "parameters": [_path_param("thing_id")]}

    code = generate_merged_function_code(
        "get_index",
        "/v1/thing/",
        list_details,
        "/v1/thing/{thing_id}/",
        detail_details,
        "thing_id",
        "get",
    )

    assert "@click.option('--file', 'param_file'" in code
    assert "known=('filters',)" in code
    assert "required=" not in code.split("merge_params")[1].split("\n")[0]
