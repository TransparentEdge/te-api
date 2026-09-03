"""Runtime helpers shared by the generated API commands.

Several endpoints take a query parameter holding a whole JSON document
-- ``--filters`` on the statistics endpoints is the usual one. Passing
that on a command line is fragile: unless the value is quoted exactly
right the shell strips the inner quotes and the JSON arrives broken, and
callers that build the command programmatically get it wrong often.

``--file`` sidesteps the quoting entirely: write the same parameters as a
JSON object in a file and point the command at it.

    {
      "filters": {
        "timestamp": {"from": 1779898235, "to": 1779899135},
        "vhost": ["www.example.com"]
      }
    }

The generated commands call ``load_param_file`` and ``merge_params``; the
logic lives here so it stays readable and testable instead of being
emitted as generated source.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import click


def option_flag(name: str) -> str:
    """Return the command-line flag for a parameter name."""
    return "--" + name.replace("_", "-").strip("-")


def load_param_file(path: str | None) -> dict[str, Any]:
    """Read a JSON object of parameter values from ``path``.

    Returns an empty mapping when no path was given, so callers can pass
    the option straight through.
    """
    if not path:
        return {}

    try:
        raw = Path(path).read_text(encoding="utf-8")
    except OSError as exc:
        raise click.UsageError(f"Cannot read --file '{path}': {exc}") from exc

    try:
        loaded = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise click.UsageError(f"--file '{path}' is not valid JSON: {exc}") from exc

    if not isinstance(loaded, dict):
        raise click.UsageError(
            f"--file '{path}' must hold a JSON object mapping parameter names to "
            f"values, got {type(loaded).__name__}."
        )

    return loaded


def encode_param(value: Any) -> Any:
    """Serialise a structured value the way the API expects it.

    Object and array parameters travel in the query string as compact
    JSON, so a nested structure read from a ``--file`` has to be encoded
    back. Values already given as strings are passed through untouched,
    which keeps the ``--filters '{...}'`` form working exactly as before.
    """
    if isinstance(value, (dict, list)):
        return json.dumps(value, separators=(",", ":"))
    if isinstance(value, bool):
        return "true" if value else "false"
    return value


def merge_params(
    params: dict[str, Any],
    file_params: dict[str, Any],
    known: tuple[str, ...] = (),
    required: tuple[str, ...] = (),
) -> dict[str, Any]:
    """Merge ``--file`` values into the ones given on the command line.

    Command-line options win: ``--file`` only fills in what was left out.
    Unknown keys are an error rather than a silent no-op, so a typo shows
    up instead of producing a query that quietly misses a filter.
    """
    unknown = sorted(set(file_params) - set(known))
    if unknown:
        accepted = ", ".join(known) if known else "(none)"
        raise click.UsageError(
            f"--file has parameters this command does not accept: "
            f"{', '.join(unknown)}. Accepted: {accepted}."
        )

    merged = dict(params)
    for name, value in file_params.items():
        if merged.get(name) is None:
            merged[name] = value

    missing = [name for name in required if merged.get(name) is None]
    if missing:
        flags = ", ".join(option_flag(name) for name in missing)
        raise click.UsageError(
            f"Missing required parameter(s): {flags}. Pass them as options or "
            f"supply them in --file."
        )

    return {name: encode_param(value) for name, value in merged.items() if value is not None}
