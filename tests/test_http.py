"""Tests for the output contract every generated command goes through.

stdout carries the API response only; errors are a JSON object on stderr
with a non-zero exit status that tells API, usage and transport failures
apart. Without this a script cannot tell success from failure.
"""

from __future__ import annotations

import json

import click
import pytest
import requests
from click.testing import CliRunner

from te_api import http
from te_api.auth import AuthError


class _Response:
    def __init__(self, status=200, payload=None, text=None, reason="OK"):
        self.status_code = status
        self.reason = reason
        self._payload = payload
        if payload is not None:
            self.text = json.dumps(payload)
        else:
            self.text = text or ""
        self.content = self.text.encode()

    def json(self):
        if self._payload is None:
            raise ValueError("not json")
        return self._payload


@pytest.fixture
def headers(monkeypatch):
    monkeypatch.setattr(http, "get_auth_headers", lambda: {"Authorization": "Bearer t"})


@pytest.fixture
def cli():
    """A root group with the real --output option and one command that
    performs a call, mirroring what the generated layer looks like."""

    @click.group()
    @click.option("--output", type=click.Choice(http.OUTPUT_MODES), default="auto")
    def root(output):
        pass

    @root.command()
    def hit():
        http.call("get", "https://api.example/thing/", params={"a": 1})

    return root


def _requests_returning(monkeypatch, response):
    seen = {}

    def _request(method, url, **kwargs):
        seen.update(method=method, url=url, **kwargs)
        return response

    monkeypatch.setattr(http.requests, "request", _request)
    return seen


# -- format_json --


def test_compact_when_not_a_terminal():
    class _Pipe:
        def isatty(self):
            return False

    assert http.format_json({"a": [1, 2]}, mode="auto", stream=_Pipe()) == '{"a":[1,2]}'


def test_pretty_on_a_terminal():
    class _Tty:
        def isatty(self):
            return True

    assert http.format_json({"a": 1}, mode="auto", stream=_Tty()) == '{\n  "a": 1\n}'


def test_explicit_mode_wins_over_the_stream():
    class _Tty:
        def isatty(self):
            return True

    assert http.format_json({"a": 1}, mode="compact", stream=_Tty()) == '{"a":1}'


def test_non_ascii_is_not_escaped():
    """Escaped unicode costs bytes and helps nobody."""
    assert "ñ" in http.format_json({"n": "año"}, mode="compact")


# -- call: success --


def test_response_json_goes_to_stdout_compact(cli, headers, monkeypatch):
    seen = _requests_returning(monkeypatch, _Response(payload={"id": 7, "x": [1]}))

    result = CliRunner().invoke(cli, ["hit"])

    assert result.exit_code == 0
    assert result.output == '{"id":7,"x":[1]}\n'
    assert seen["headers"] == {"Authorization": "Bearer t"}
    assert seen["params"] == {"a": 1}
    assert seen["timeout"] == http.REQUEST_TIMEOUT


def test_output_option_forces_pretty(cli, headers, monkeypatch):
    _requests_returning(monkeypatch, _Response(payload={"id": 7}))

    result = CliRunner().invoke(cli, ["--output", "pretty", "hit"])

    assert result.output == '{\n  "id": 7\n}\n'


def test_non_json_body_is_passed_through(cli, headers, monkeypatch):
    _requests_returning(monkeypatch, _Response(text="plain text"))

    result = CliRunner().invoke(cli, ["hit"])

    assert result.exit_code == 0
    assert result.output == "plain text\n"


def test_empty_body_leaves_stdout_empty(cli, headers, monkeypatch):
    _requests_returning(monkeypatch, _Response(status=204, text=""))

    result = CliRunner().invoke(cli, ["hit"])

    assert result.exit_code == 0
    assert result.stdout == ""


# -- call: failures --


def test_api_error_status_goes_to_stderr_with_exit_1(cli, headers, monkeypatch):
    _requests_returning(
        monkeypatch,
        _Response(status=404, reason="Not Found", payload={"code": "not_found"}),
    )

    result = CliRunner().invoke(cli, ["hit"])

    assert result.exit_code == http.EXIT_API_ERROR
    assert result.stdout == ""
    error = json.loads(result.stderr)["error"]
    assert error["type"] == "api"
    assert error["status"] == 404
    assert error["body"] == {"code": "not_found"}
    assert error["url"] == "https://api.example/thing/"


def test_error_honours_the_output_option(cli, headers, monkeypatch):
    """The exception is shown after the context is gone, so the mode has
    to be captured while the command still runs."""
    _requests_returning(monkeypatch, _Response(status=500, reason="Boom", text="x"))

    result = CliRunner().invoke(cli, ["--output", "pretty", "hit"])

    assert result.stderr.startswith('{\n  "error": {')


def test_transport_failure_exits_3(cli, headers, monkeypatch):
    def _request(*_a, **_k):
        raise requests.exceptions.ConnectionError("refused")

    monkeypatch.setattr(http.requests, "request", _request)

    result = CliRunner().invoke(cli, ["hit"])

    assert result.exit_code == http.EXIT_TRANSPORT
    error = json.loads(result.stderr)["error"]
    assert error["type"] == "transport"
    assert "refused" in error["message"]


def test_auth_failure_exits_3(cli, monkeypatch):
    def _no_token():
        raise AuthError("invalid_client", status=401, body={"error": "invalid_client"})

    monkeypatch.setattr(http, "get_auth_headers", _no_token)

    result = CliRunner().invoke(cli, ["hit"])

    assert result.exit_code == http.EXIT_TRANSPORT
    error = json.loads(result.stderr)["error"]
    assert error["type"] == "auth"
    assert error["status"] == 401


def test_usage_errors_keep_clicks_exit_code():
    """Exit 2 stays reserved for a bad command line."""
    assert http.EXIT_USAGE == click.UsageError.exit_code
