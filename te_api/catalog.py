"""Search over the generated command catalog.

The builder writes ``catalog.json`` beside the command modules: one
record per command with its summary, parameters and body schema. This
module ranks those records against a free-text query so a caller can
find the right command without walking the ``--help`` tree. A few
hundred commands do not justify an index or a dependency: token overlap
with a little prefix matching is enough.
"""

from __future__ import annotations

import re
from typing import Any

_TOKEN = re.compile(r"[a-z0-9]+")

# Where a query token matches decides how much it is worth: the command
# name is what the caller will type, the summary is what the API calls
# it, everything else is supporting text.
_WEIGHTS = (("command", 3.0), ("summary", 2.0), ("text", 1.0))

# Shortest query token that may match a longer field token by prefix,
# so "cert" finds "certificate" but "id" does not find "identity".
_MIN_PREFIX = 4


def tokenize(text: str) -> list[str]:
    return _TOKEN.findall(text.lower())


def _fields(entry: dict[str, Any]) -> dict[str, set[str]]:
    text_parts = [entry.get("description", ""), entry.get("path", "")]
    for param in entry.get("parameters", []):
        text_parts.append(param.get("name", ""))
        text_parts.append(param.get("description", ""))
    body = entry.get("body")
    if isinstance(body, dict):
        text_parts.extend(body.get("properties", {}).keys())
    return {
        "command": set(tokenize(entry.get("command", ""))),
        "summary": set(tokenize(entry.get("summary", ""))),
        "text": set(tokenize(" ".join(text_parts))),
    }


def _matches(token: str, field: set[str]) -> bool:
    if token in field:
        return True
    if len(token) < _MIN_PREFIX:
        return False
    return any(word.startswith(token) or token.startswith(word) and len(word) >= _MIN_PREFIX
               for word in field)


def score(entry: dict[str, Any], query_tokens: list[str]) -> float:
    fields = _fields(entry)
    total = 0.0
    for token in query_tokens:
        for name, weight in _WEIGHTS:
            if _matches(token, fields[name]):
                total += weight
                break
    return total


def search(entries: list[dict[str, Any]], query: str, limit: int = 10) -> list[dict[str, Any]]:
    """Rank ``entries`` against ``query``; entries matching no token are
    dropped. Each hit carries the command, its summary and the score."""
    tokens = tokenize(query)
    if not tokens:
        return []
    hits = []
    for entry in entries:
        value = score(entry, tokens)
        if value > 0:
            hits.append((value, entry))
    hits.sort(key=lambda item: (-item[0], item[1]["command"]))
    return [
        {
            "command": entry["command"],
            "summary": entry.get("summary", ""),
            "method": entry.get("method"),
            "path": entry.get("path"),
            "score": value,
        }
        for value, entry in hits[:limit]
    ]


def find(entries: list[dict[str, Any]], words: list[str]) -> tuple[dict[str, Any] | None, list[dict[str, Any]]]:
    """Look a command up by its words. Returns ``(exact, under)``: the
    exact match if there is one, and every command whose name starts
    with those words, so ``describe companies get`` lists a subtree."""
    wanted = " ".join(words).strip().lower()
    exact = None
    under = []
    for entry in entries:
        name = entry["command"].lower()
        if name == wanted:
            exact = entry
        elif name.startswith(wanted + " "):
            under.append(entry)
    return exact, under
