"""Tests for the command catalog and the search/describe commands on top.

The catalog exists so a caller can find a command and learn its
parameters in one call, instead of walking the --help tree.
"""

from __future__ import annotations

import json

import pytest
from click.testing import CliRunner

from te_api import builder, catalog
from te_api.cli import create_cli

_SPEC = {
    "paths": {
        "/v1/{company_id}/alerts/": {
            "get": {
                "operationId": "v1_alerts_list",
                "tags": ["companies"],
                "summary": "List alerts",
                "parameters": [
                    {"name": "company_id", "in": "path", "required": True, "schema": {"type": "string"}},
                    {
                        "name": "active",
                        "in": "query",
                        "required": False,
                        "schema": {"type": "boolean"},
                        "description": "Only active\nalerts",
                    },
                ],
            },
            "post": {
                "operationId": "v1_alerts_create",
                "tags": ["companies"],
                "summary": "Create alert",
                "description": "Creates a traffic threshold alert.",
                "parameters": [
                    {"name": "company_id", "in": "path", "required": True, "schema": {"type": "string"}},
                ],
                "requestBody": {
                    "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Alert"}}}
                },
            },
        },
        "/v1/{company_id}/alerts/{alert_id}/": {
            "get": {
                "operationId": "v1_alerts_retrieve",
                "tags": ["companies"],
                "summary": "Alert detail",
                "parameters": [
                    {"name": "company_id", "in": "path", "required": True, "schema": {"type": "string"}},
                    {"name": "alert_id", "in": "path", "required": True, "schema": {"type": "string"}},
                ],
            }
        },
        "/v1/statistics/waf/{temporality}/": {
            "get": {
                "operationId": "v1_statistics_waf_retrieve",
                "tags": ["statistics"],
                "summary": "WAF statistics",
                "parameters": [
                    {
                        "name": "temporality",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "string", "pattern": "^historic|analytic$"},
                    },
                    {
                        "name": "filters",
                        "in": "query",
                        "required": True,
                        "schema": {"type": "object", "properties": {"vhost": {"type": "array"}}},
                    },
                ],
            }
        },
    },
    "components": {
        "schemas": {
            "Alert": {
                "type": "object",
                "required": ["threshold"],
                "properties": {"threshold": {"type": "integer"}},
            }
        }
    },
}


@pytest.fixture
def layer(tmp_path, monkeypatch):
    """A generated layer in a temporary directory, with the CLI pointed
    at it and the auto-build turned off."""
    out = tmp_path / "api"
    builder.generate_from_spec(_SPEC, str(out), log=lambda _m: None)
    monkeypatch.setattr(builder, "_api_dir", lambda read_only: out)
    monkeypatch.setattr(builder, "ensure_api_built", lambda read_only=False: False)
    return out


def _commands(layer):
    return json.loads((layer / builder.CATALOG_FILE).read_text())["commands"]


# -- what the builder writes --


def test_catalog_lists_every_command(layer):
    names = sorted(e["command"] for e in _commands(layer))

    assert names == ["companies create alerts", "companies get alerts", "statistics get waf"]


def test_catalog_describes_body_and_options(layer):
    entry = next(e for e in _commands(layer) if e["command"] == "companies create alerts")

    assert entry["method"] == "post"
    assert entry["body"]["properties"]["threshold"]["type"] == "integer"
    assert entry["options"] == ["--json-body", "--body-file"]
    assert entry["description"] == "Creates a traffic threshold alert."
    company = entry["parameters"][0]
    assert company["flag"] == "--company-id"
    assert company["required"] is False


def test_catalog_describes_merged_list_detail(layer):
    entry = next(e for e in _commands(layer) if e["command"] == "companies get alerts")

    assert entry["path"] == "/v1/{company_id}/alerts/"
    assert entry["detail_path"] == "/v1/{company_id}/alerts/{alert_id}/"
    id_arg = entry["parameters"][-1]
    assert id_arg["name"] == "alert_id"
    assert id_arg["argument"] is True
    assert id_arg["required"] is False
    active = next(p for p in entry["parameters"] if p["name"] == "active")
    assert active["flag"] == "--active"
    assert active["description"] == "Only active alerts"
    assert entry["options"] == ["--file"]


def test_catalog_carries_choices_and_object_schemas(layer):
    entry = next(e for e in _commands(layer) if e["command"] == "statistics get waf")
    temporality, filters = entry["parameters"]

    assert temporality["argument"] is True
    assert temporality["choices"] == ["historic", "analytic"]
    assert filters["required"] is True
    assert filters["schema"]["properties"]["vhost"]["type"] == "array"


def test_read_only_catalog_is_flagged(tmp_path):
    out = tmp_path / "api_ro"
    builder.generate_from_spec(_SPEC, str(out), read_only=True, log=lambda _m: None)
    payload = json.loads((out / builder.CATALOG_FILE).read_text())

    assert payload["read_only"] is True
    assert all(e["method"] == "get" for e in payload["commands"])


def test_load_catalog_is_none_without_a_layer(tmp_path, monkeypatch):
    monkeypatch.setattr(builder, "_api_dir", lambda read_only: tmp_path)

    assert builder.load_catalog() is None


# -- search ranking --


def test_command_name_outranks_summary_outranks_text(layer):
    hits = catalog.search(_commands(layer), "waf")

    assert hits[0]["command"] == "statistics get waf"
    assert hits[0]["score"] == 3.0


def test_prefix_matching_needs_a_few_letters(layer):
    assert catalog.search(_commands(layer), "aler")
    assert not catalog.search(_commands(layer), "al")


def test_unmatched_entries_are_dropped(layer):
    assert catalog.search(_commands(layer), "zzz") == []


def test_limit_caps_the_hits(layer):
    assert len(catalog.search(_commands(layer), "alerts", limit=1)) == 1


def test_find_exact_and_subtree(layer):
    exact, under = catalog.find(_commands(layer), ["companies", "get", "alerts"])
    assert exact["command"] == "companies get alerts"
    assert under == []

    exact, under = catalog.find(_commands(layer), ["companies"])
    assert exact is None
    assert sorted(e["command"] for e in under) == ["companies create alerts", "companies get alerts"]


# -- the CLI commands --


def test_search_command_prints_json_hits(layer):
    result = CliRunner().invoke(create_cli(), ["search", "waf", "statistics"])

    assert result.exit_code == 0, result.output
    hits = json.loads(result.stdout)
    assert hits[0]["command"] == "statistics get waf"


def test_describe_command_prints_the_entry(layer):
    result = CliRunner().invoke(create_cli(), ["describe", "companies", "create", "alerts"])

    assert result.exit_code == 0, result.output
    entry = json.loads(result.stdout)
    assert entry["body"]["required"] == ["threshold"]


def test_describe_prefix_lists_the_subtree(layer):
    result = CliRunner().invoke(create_cli(), ["describe", "companies"])

    assert result.exit_code == 0, result.output
    assert [e["command"] for e in json.loads(result.stdout)] == [
        "companies get alerts",
        "companies create alerts",
    ]


def test_describe_unknown_is_a_usage_error(layer):
    result = CliRunner().invoke(create_cli(), ["describe", "nope"])

    assert result.exit_code == 2
    assert "search" in result.stderr


def test_commands_fail_cleanly_without_a_catalog(tmp_path, monkeypatch):
    monkeypatch.setattr(builder, "_api_dir", lambda read_only: tmp_path)
    monkeypatch.setattr(builder, "ensure_api_built", lambda read_only=False: False)

    result = CliRunner().invoke(create_cli(), ["search", "anything"])

    assert result.exit_code == 1
    assert "te-api build" in result.stderr
