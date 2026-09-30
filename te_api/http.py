"""HTTP call and output contract shared by every generated command.

The generated commands used to carry their own copy of the request and
error handling, which made the output unusable from a script: errors
went to stdout, the exit status was always 0, and the only way to tell a
failure from a result was to parse the text. Everything now funnels
through ``call`` so the contract is defined once, here:

- **stdout holds the API response and nothing else.** JSON is
  pretty-printed when stdout is a terminal and compact otherwise, so a
  human reads it comfortably and a pipe or an agent gets it in as few
  bytes as possible. ``--output pretty|compact`` (or ``TE_API_OUTPUT``)
  forces one or the other.
- **Errors go to stderr as a JSON object** ``{"error": {...}}`` with the
  HTTP status, the response body and the URL, and the process exits
  non-zero.
- **Exit codes** tell the kind of failure apart: 1 when the API answered
  with an error status, 2 for a usage error (click's own), 3 when the API
  could not be reached or the OAuth2 token could not be obtained.
"""

from __future__ import annotations

import json
import sys
from typing import Any

import click
import requests

from .auth import AuthError, get_auth_headers

EXIT_API_ERROR = 1
EXIT_USAGE = 2
EXIT_TRANSPORT = 3

OUTPUT_MODES = ("auto", "pretty", "compact")
OUTPUT_ENV_VAR = "TE_API_OUTPUT"

# Statistics queries over long windows can take a while, but a command
# that never returns is worse for an unattended caller than one that
# fails loudly.
REQUEST_TIMEOUT = 300


def output_mode() -> str:
    """The output mode in force: the root ``--output`` option if a
    command is running, ``auto`` otherwise."""
    ctx = click.get_current_context(silent=True)
    if ctx is not None:
        mode = ctx.find_root().params.get("output")
        if mode in OUTPUT_MODES:
            return mode
    return "auto"


def format_json(value: Any, mode: str | None = None, stream=None) -> str:
    """Serialise ``value`` according to ``mode``. ``auto`` pretty-prints
    when ``stream`` (stdout by default) is a terminal."""
    mode = mode or output_mode()
    if mode == "auto":
        stream = stream if stream is not None else sys.stdout
        mode = "pretty" if stream.isatty() else "compact"
    if mode == "pretty":
        return json.dumps(value, indent=2, ensure_ascii=False)
    return json.dumps(value, separators=(",", ":"), ensure_ascii=False)


def emit(value: Any) -> None:
    """Write a JSON value to stdout in the mode in force."""
    click.echo(format_json(value))


class ApiError(click.ClickException):
    """A failed call, reported to stderr as JSON with a meaningful exit
    code. Click prints and exits for us when this propagates out of a
    command."""

    def __init__(
        self,
        message: str,
        *,
        kind: str = "api",
        status: int | None = None,
        body: Any = None,
        url: str | None = None,
        exit_code: int = EXIT_API_ERROR,
    ):
        super().__init__(message)
        # Click shows the exception after the context is gone, so the
        # mode has to be captured while the command is still running.
        self.output_mode = output_mode()
        self.kind = kind
        self.status = status
        self.body = body
        self.url = url
        self.exit_code = exit_code

    def payload(self) -> dict[str, Any]:
        error: dict[str, Any] = {"type": self.kind, "message": self.message}
        if self.status is not None:
            error["status"] = self.status
        if self.url is not None:
            error["url"] = self.url
        if self.body is not None:
            error["body"] = self.body
        return {"error": error}

    def show(self, file=None) -> None:
        stream = file if file is not None else sys.stderr
        text = format_json(self.payload(), mode=self.output_mode, stream=stream)
        click.echo(text, file=file, err=True)


def _response_body(response: requests.Response) -> Any:
    if not response.content:
        return None
    try:
        return response.json()
    except ValueError:
        return response.text


def call(
    method: str,
    url: str,
    params: dict[str, Any] | None = None,
    data: Any = None,
) -> None:
    """Perform the request and print the result under the contract above.

    Raises ``ApiError`` on any failure; click turns it into the stderr
    report and the exit status.
    """
    try:
        headers = get_auth_headers()
    except AuthError as exc:
        raise ApiError(
            str(exc), kind="auth", status=exc.status, body=exc.body,
            exit_code=EXIT_TRANSPORT,
        ) from exc

    try:
        response = requests.request(
            method, url, headers=headers, params=params, json=data,
            timeout=REQUEST_TIMEOUT,
        )
    except requests.exceptions.RequestException as exc:
        raise ApiError(
            str(exc), kind="transport", url=url, exit_code=EXIT_TRANSPORT
        ) from exc

    if response.status_code >= 400:
        raise ApiError(
            f"HTTP {response.status_code} {response.reason}",
            status=response.status_code,
            body=_response_body(response),
            url=url,
        )

    if not response.content:
        # Nothing for stdout; tell the human, not the pipe.
        if sys.stdout.isatty():
            click.echo(f"HTTP {response.status_code}, no content.", err=True)
        return

    try:
        emit(response.json())
    except ValueError:
        click.echo(response.text)
