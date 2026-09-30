"""The usage guide printed by ``te-api agents``.

It is aimed at whoever drives the tool unattended: a script or an AI
agent. It states the contract (what goes to stdout, what an error looks
like, what the exit codes mean) and the few things that are not
discoverable from --help alone, such as scoping the company through the
environment. ``--skill`` wraps it as a Claude Code skill file.
"""

from __future__ import annotations

import textwrap


def agent_guide(prog: str = "te-api", read_only: bool = False) -> str:
    verbs = "get" if read_only else "get, create, update, delete or action"
    scope = "read-only: only GET operations are available" if read_only else "full access"
    write_section = "" if read_only else textwrap.dedent(f"""
        ## Request bodies

        Commands that take a body accept `--json-body '<json>'` or
        `--body-file <path>` (`-` reads stdin). `--help` and `describe`
        show the body schema: property names, types and which are required.
        Properties marked readOnly in `describe` are returned by the API,
        never sent.
        """)

    return textwrap.dedent(f"""
        # {prog}: guide for scripts and agents

        `{prog}` wraps the Transparent Edge CDN API ({scope}). Commands are
        generated from the live OpenAPI schema, so every endpoint your
        credentials can reach is here.

        ## Command shape

            {prog} <module> <verb> <resource> [ARGUMENTS] [OPTIONS]

        `<verb>` is one of {verbs}. Path parameters are positional
        arguments, query parameters are `--kebab-case` options.

        ## Finding a command

        - `{prog} search <words>`: JSON list of matching commands, best first.
        - `{prog} describe <module> <verb> <resource>`: the command's full
          definition as JSON (parameters, types, required, choices, body
          schema, HTTP method and path). Prefer it over `--help`: it is
          structured and complete.
        - `{prog} describe <module> [<verb>]`: lists the commands under a prefix.

        ## Output contract

        - stdout holds the API response and nothing else. JSON is compact
          when stdout is not a terminal and pretty-printed when it is;
          `--output pretty|compact` (before the module name) or
          `TE_API_OUTPUT` forces one.
        - On failure stdout is empty and stderr holds one JSON object:
          `{{"error": {{"type", "message", "status", "url", "body"}}}}`.
        - Exit codes: 0 success, 1 the API answered with an error status,
          2 bad command line (missing or unknown option, invalid JSON),
          3 the API or the token endpoint could not be reached.

        Filter large responses with `jq` instead of reading them whole.

        ## Company scope

        Most commands act on one company. Set `TRANSPARENT_COMPANY_ID` in
        the environment for the call: it scopes that invocation only and
        is ignored by commands that take no company. Do not pass
        `--company-id` blindly: commands without a company parameter reject
        it. `{prog} set-company <id>` persists a default for interactive use.

        ## Query parameters from a file

        Any command with query parameters accepts `--file <path>`: a JSON
        object mapping parameter names to values. Nested objects such as
        `filters` are written as real JSON, no shell quoting needed.
        Explicit options win over the file.
        {write_section}
        ## Authentication

        `TRANSPARENT_CLIENT_ID` and `TRANSPARENT_CLIENT_SECRET` from the
        environment, `./.env` or `~/.env`. Tokens are cached in
        `~/.te-api/` and refreshed automatically; nothing to do per call.
        `{prog} login` checks credentials and exits 3 if they fail.
        """).strip() + "\n"


def skill_file(prog: str = "te-api", read_only: bool = False) -> str:
    """The guide as a Claude Code skill: frontmatter plus the guide."""
    action = "query (read-only)" if read_only else "query and manage"
    frontmatter = textwrap.dedent(f"""
        ---
        name: {prog}
        description: Use the `{prog}` CLI to {action} the Transparent Edge CDN API: statistics, WAF, sites, cache invalidation, users, billing. Use whenever the user asks about Transparent Edge / TCDN data or configuration from the terminal.
        ---
        """).lstrip()
    return frontmatter + "\n" + agent_guide(prog, read_only)
