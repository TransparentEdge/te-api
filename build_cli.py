"""Standalone entry point for the OpenAPI builder.

The actual implementation lives in `te_api.builder`. This script is kept
in the repository root so contributors can run `uv run build_cli.py`
without installing the package as a tool. End-users invoke the same
functionality via `te-api build` (auto-built on first run).
"""

from te_api.builder import build

if __name__ == "__main__":
    build()
