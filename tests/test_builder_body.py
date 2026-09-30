"""Tests for how the generator describes and accepts request bodies.

`--json-body` used to say "JSON string for request body" and nothing
else, while the schema sat unused in the spec behind a `$ref`. A caller
knew there was a body but not what to put in it.
"""

from __future__ import annotations

from te_api.builder import (
    body_schema,
    build_body_help,
    build_object_help,
    dereference_spec,
    generate_function_code,
    generate_from_spec,
    normalize_schema,
)

_COMPONENTS = {
    "Alert": {
        "type": "object",
        "required": ["threshold"],
        "properties": {
            "id": {"type": "integer", "readOnly": True},
            "threshold": {"type": "integer", "description": "Trigger\nlevel"},
            "reactions": {"type": "array", "items": {"$ref": "#/components/schemas/Reaction"}},
        },
    },
    "Reaction": {
        "type": "object",
        "properties": {"name": {"type": "string"}},
    },
    "Node": {
        "type": "object",
        "properties": {"child": {"$ref": "#/components/schemas/Node"}},
    },
}


def _spec(body_ref="#/components/schemas/Alert"):
    return {
        "paths": {
            "/v1/alerts/": {
                "post": {
                    "operationId": "v1_alerts_create",
                    "tags": ["alerts"],
                    "summary": "Create alert",
                    "requestBody": {
                        "content": {"application/json": {"schema": {"$ref": body_ref}}}
                    },
                }
            }
        },
        "components": {"schemas": _COMPONENTS},
    }


# -- dereference --


def test_refs_under_paths_are_inlined():
    spec = dereference_spec(_spec())
    schema = spec["paths"]["/v1/alerts/"]["post"]["requestBody"]["content"]["application/json"]["schema"]

    assert schema["properties"]["threshold"]["type"] == "integer"
    assert schema["properties"]["reactions"]["items"]["properties"]["name"]["type"] == "string"


def test_recursive_refs_terminate():
    spec = dereference_spec(_spec("#/components/schemas/Node"))
    schema = spec["paths"]["/v1/alerts/"]["post"]["requestBody"]["content"]["application/json"]["schema"]

    child = schema["properties"]["child"]
    assert child["type"] == "object"
    assert "properties" not in child


def test_unknown_ref_becomes_a_plain_object():
    spec = dereference_spec(_spec("#/components/schemas/Missing"))
    schema = spec["paths"]["/v1/alerts/"]["post"]["requestBody"]["content"]["application/json"]["schema"]

    assert schema == {"type": "object"}


def test_the_input_spec_is_not_mutated():
    spec = _spec()
    dereference_spec(spec)

    assert "$ref" in spec["paths"]["/v1/alerts/"]["post"]["requestBody"]["content"]["application/json"]["schema"]


# -- normalize_schema --


def test_all_of_is_folded_into_one_object():
    schema = normalize_schema(
        {
            "allOf": [
                {"type": "object", "properties": {"a": {"type": "string"}}, "required": ["a"]},
                {"type": "object", "properties": {"b": {"type": "integer"}}},
            ]
        }
    )

    assert schema["type"] == "object"
    assert set(schema["properties"]) == {"a", "b"}
    assert schema["required"] == ["a"]


def test_one_of_becomes_a_type_union():
    schema = normalize_schema(
        {"oneOf": [{"type": "integer"}, {"type": "array", "items": {"type": "integer"}}]}
    )

    assert schema["type"] == "integer|array of integer"


# -- help text --


def test_read_only_properties_are_left_out():
    """They describe what the API returns, never what a caller sends."""
    text = build_object_help(_COMPONENTS["Alert"])

    assert "id(" not in text
    assert "threshold(integer [required])" in text


def test_descriptions_are_collapsed_to_one_line():
    text = build_object_help(_COMPONENTS["Alert"])

    assert "\n" not in text
    assert "Trigger level" in text


def test_array_items_are_typed():
    text = build_object_help(dereference_spec(_spec())["paths"]["/v1/alerts/"]["post"]["requestBody"]["content"]["application/json"]["schema"])

    assert "reactions(array of object)" in text


def test_body_help_for_an_array_body():
    text = build_body_help(
        {"type": "array", "items": {"type": "integer"}, "description": "IDs in order"}
    )

    assert text == "JSON request body: array of integer. IDs in order"


def test_body_help_without_schema():
    assert build_body_help(None) == "JSON request body"


def test_body_schema_ignores_non_json_media():
    details = {
        "requestBody": {
            "content": {"application/x-www-form-urlencoded": {"schema": {"type": "object"}}}
        }
    }

    assert body_schema(details) is None


# -- generated code --


def test_command_with_a_body_gets_both_options():
    details = dereference_spec(_spec())["paths"]["/v1/alerts/"]["post"]
    code = generate_function_code("create_alerts", "/v1/alerts/", "post", details)

    assert "@click.option('--json-body', 'json_body', help='JSON request body. JSON object with keys:" in code
    assert "threshold(integer [required])" in code
    assert "@click.option('--body-file', 'body_file'" in code
    assert "data = load_body(json_body, body_file)" in code


def test_command_without_a_body_gets_neither():
    code = generate_function_code("get_alerts", "/v1/alerts/", "get", {"summary": "List"})

    assert "--json-body" not in code
    assert "--body-file" not in code
    assert "data = None" in code


def test_generated_module_compiles_with_a_multiline_description(tmp_path):
    """The help string is emitted inside quotes; a newline would break it."""
    out = tmp_path / "api"
    generate_from_spec(_spec(), str(out), log=lambda _m: None)

    compile((out / "alerts.py").read_text(), "alerts.py", "exec")
