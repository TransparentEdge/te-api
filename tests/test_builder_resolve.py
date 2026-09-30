"""Tests for the heuristics that turn operation IDs and paths into
commands: parse_operation_id, find_list_detail_pair and
resolve_candidates. They carry the most guesswork in the generator.
"""

from __future__ import annotations

import pytest

from te_api.builder import (
    find_list_detail_pair,
    parse_operation_id,
    resolve_candidates,
)

# -- parse_operation_id: (operation_id, tag) -> (version, dup, noun, verb) --


@pytest.mark.parametrize(
    "operation_id, tag, expected",
    [
        ("v1_companies_alerts_list", "companies", (1, 0, "alerts", "get")),
        ("v1_companies_alerts_retrieve", "companies", (1, 0, "alerts", "get")),
        ("v1_companies_alerts_create", "companies", (1, 0, "alerts", "create")),
        ("v1_companies_alerts_update", "companies", (1, 0, "alerts", "update")),
        # PATCH lands on a distinct noun, so it does not collide with the
        # PUT's `update alerts` and both stay reachable.
        ("v1_companies_alerts_partial_update_detail", "companies", (1, 0, "alerts-partial", "update")),
        ("v1_companies_alerts_destroy", "companies", (1, 0, "alerts", "delete")),
        # Two-word suffixes emitted by DRF-style generators.
        ("v1_companies_rules_create_list", "companies", (1, 0, "rules", "create")),
        ("v1_companies_rules_retrieve_detail", "companies", (1, 0, "rules", "get")),
        ("v1_companies_rules_destroy_detail", "companies", (1, 0, "rules", "delete")),
        ("v1_companies_rules_check_retrieve", "companies", (1, 0, "rules", "get")),
        # Version and duplicate suffix are separated from the noun.
        ("v2_statistics_waf_retrieve_2", "statistics", (2, 2, "waf", "get")),
        # Multi-word nouns become kebab-case.
        ("v1_companies_cache_status_retrieve", "companies", (1, 0, "cache-status", "get")),
        # No verb at all: an action on the noun.
        ("v1_companies_prefetch", "companies", (1, 0, "prefetch", "action")),
        # Nothing but the verb: the tag's root resource.
        ("v1_companies_list", "companies", (1, 0, "root", "get")),
        # No version prefix.
        ("users_current_retrieve", "users", (0, 0, "current", "get")),
    ],
)
def test_parse_operation_id(operation_id, tag, expected):
    assert parse_operation_id(operation_id, tag) == expected


def test_tag_prefix_is_only_stripped_when_present():
    """An operation tagged differently from its prefix keeps the prefix
    as part of the noun."""
    assert parse_operation_id("v1_autoprovisioning_rules_list", "companies") == (
        1, 0, "autoprovisioning-rules", "get",
    )


# -- candidates: (version, dup_suffix, details, path, method) --


def _cand(path, method="get", version=1, dup=0, summary=None):
    return (version, dup, {"summary": summary or path}, path, method)


def test_list_detail_pair_is_detected():
    lst = _cand("/v1/things/")
    detail = _cand("/v1/things/{thing_id}/")

    assert find_list_detail_pair([detail, lst]) == (lst, detail, "thing_id")


def test_unrelated_paths_are_not_a_pair():
    assert find_list_detail_pair([_cand("/v1/things/"), _cand("/v1/others/{id}/")]) is None


def test_pair_needs_exactly_one_trailing_param():
    assert find_list_detail_pair([_cand("/v1/things/"), _cand("/v1/things/{a}/{b}/")]) is None


def test_get_pair_is_merged():
    lst = _cand("/v1/things/")
    detail = _cand("/v1/things/{thing_id}/")
    resolved = resolve_candidates({"tag": {"get": {"things": [lst, detail]}}})

    entry = resolved["tag"]["get"]["things"]
    assert entry["kind"] == "merged"
    assert entry["list_path"] == "/v1/things/"
    assert entry["detail_path"] == "/v1/things/{thing_id}/"
    assert entry["id_param"] == "thing_id"


def test_single_candidate_stays_single():
    resolved = resolve_candidates({"tag": {"get": {"things": [_cand("/v1/things/")]}}})

    entry = resolved["tag"]["get"]["things"]
    assert entry["kind"] == "single"
    assert entry["path"] == "/v1/things/"
    assert entry["method"] == "get"


def test_company_scoped_path_wins_over_global():
    global_ = _cand("/v1/things/", version=2)
    scoped = _cand("/v1/{company_id}/things/", version=1)
    resolved = resolve_candidates({"tag": {"get": {"things": [global_, scoped]}}})

    assert resolved["tag"]["get"]["things"]["path"] == "/v1/{company_id}/things/"


def test_newer_version_wins_when_scope_is_equal():
    resolved = resolve_candidates(
        {"tag": {"get": {"things": [_cand("/v1/things/", version=1), _cand("/v2/things/", version=2)]}}}
    )

    assert resolved["tag"]["get"]["things"]["path"] == "/v2/things/"


def test_duplicate_suffix_breaks_the_last_tie():
    resolved = resolve_candidates(
        {"tag": {"get": {"things": [_cand("/v1/a/things/", dup=0), _cand("/v1/b/things/", dup=2)]}}}
    )

    assert resolved["tag"]["get"]["things"]["path"] == "/v1/b/things/"


def test_non_get_verbs_are_never_merged():
    """A POST on the collection and a POST on an item are different
    operations; only GET list/detail collapse into one command."""
    lst = _cand("/v1/things/", method="post")
    detail = _cand("/v1/things/{thing_id}/", method="post")
    resolved = resolve_candidates({"tag": {"create": {"things": [lst, detail]}}})

    assert resolved["tag"]["create"]["things"]["kind"] == "single"
