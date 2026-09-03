"""Tests for context resolution (company_id and friends)."""

from __future__ import annotations

import json

import pytest

from te_api.config import Config


@pytest.fixture
def context_file(tmp_path, monkeypatch):
    """An isolated context file, so tests never touch ~/.te-api."""
    path = tmp_path / "context.json"
    monkeypatch.setattr(Config, "CONTEXT_FILE", str(path), raising=False)
    monkeypatch.setattr(Config, "BASE_DIR", str(tmp_path), raising=False)
    monkeypatch.delenv("TRANSPARENT_COMPANY_ID", raising=False)
    return path


def test_no_context_at_all(context_file):
    assert Config.get_context("company_id") is None


def test_reads_the_persisted_context(context_file):
    context_file.write_text(json.dumps({"company_id": "145"}))
    assert Config.get_context("company_id") == "145"


def test_environment_wins_over_the_file(context_file, monkeypatch):
    """A caller handling several companies scopes one invocation."""
    context_file.write_text(json.dumps({"company_id": "145"}))
    monkeypatch.setenv("TRANSPARENT_COMPANY_ID", "66")

    assert Config.get_context("company_id") == "66"


def test_environment_alone_is_enough(context_file, monkeypatch):
    """No set-company needed, which is the point for automated callers."""
    monkeypatch.setenv("TRANSPARENT_COMPANY_ID", "66")

    assert Config.get_context("company_id") == "66"


def test_empty_environment_value_falls_through(context_file, monkeypatch):
    """An unset-but-present variable must not shadow the file."""
    context_file.write_text(json.dumps({"company_id": "145"}))
    monkeypatch.setenv("TRANSPARENT_COMPANY_ID", "")

    assert Config.get_context("company_id") == "145"


def test_corrupt_context_file_is_ignored(context_file):
    context_file.write_text("not json{")
    assert Config.get_context("company_id") is None


def test_set_context_roundtrips(context_file):
    Config.set_context("company_id", "312")
    assert Config.get_context("company_id") == "312"
