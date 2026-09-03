# TE-API Technical Documentation

**TE-API** is a Python command-line tool that wraps the Transparent Edge API. It lets you interact with every service of the platform from your terminal in a structured, secure, and efficient way.

## 1. Introduction

The goal of this project is to provide a unified interface for managing Transparent Edge resources (CDN, WAF, storage, users, etc.) without having to craft HTTP requests by hand.

The tool is **auto-generated** from the live OpenAPI schema served by the API itself, which means it always exposes 100% of the endpoints available to your account.

The project provides **two binaries**:
- **`te-api`**: Full access to every API operation (get, create, update, delete).
- **`te-api-ro`**: Read-only version, restricted to GET operations.

## 2. Installation and Requirements

This project uses **`uv`** to manage dependencies and virtual environments, which keeps installation fast and isolated.

### Prerequisites
- Python 3.12 or newer.
- [uv](https://github.com/astral-sh/uv) installed.

### Installation for End Users
If you only want to use the tool, install it directly from the git repository:

```bash
# Install as a global tool
uv tool install git+https://github.com/TransparentEdge/te-api.git
```

Once installed, the `te-api` and `te-api-ro` commands will be available on your terminal.

> **Important:** the package does not ship with pregenerated command code. The first time you run `te-api` (or `te-api-ro`) the tool will download the OpenAPI schema that matches your credentials and generate the modules automatically. Because of this, you need to configure `TRANSPARENT_CLIENT_ID` and `TRANSPARENT_CLIENT_SECRET` before the first run (see section 3). When your permissions change or the API ships new endpoints, run `te-api build` to refresh.

> **After an upgrade there is nothing to remember.** Each generated layer
> records which version of the generator produced it, so a newly
> installed `te-api` notices that the commands on disk are stale and
> rebuilds them on its next run. This matters because the generated
> modules are not part of the wheel and survive a reinstall; without the
> check, a new `te-api` would keep running the old commands. If the
> rebuild is not possible right then (no credentials, no network), the
> tool says so on stderr and keeps working with what it has.

### Installation for Developers
If you want to modify the code or work on the generator:

1.  Clone the repository:
    ```bash
    git clone https://github.com/TransparentEdge/te-api.git
    cd te-api
    ```
2.  Sync the environment:
    ```bash
    uv sync
    ```
3.  Run the tool through uv:
    ```bash
    uv run te-api       # Full version
    uv run te-api-ro    # Read-only version
    ```

## 3. Basic Usage

### Authentication
Authentication is handled automatically over OAuth2 (both `te-api` and `te-api-ro` share the same flow and token).

1.  Configure your credentials via a `.env` file or environment variables:
    ```bash
    export TRANSPARENT_CLIENT_ID="your_client_id"
    export TRANSPARENT_CLIENT_SECRET="your_client_secret"
    ```
    If you would rather not export the variables, drop a `.env` file in the working directory or in your `$HOME`:
    ```bash
    cat <<EOF >> ~/.env
    TRANSPARENT_CLIENT_ID="your_client_id"
    TRANSPARENT_CLIENT_SECRET="your_client_secret"
    EOF
    ```

2.  Log in (optional - the first request triggers it automatically):
    ```bash
    te-api login
    ```
    The token is stored in `~/.te-api/token.json` and refreshed automatically on expiry.

### First Run and CLI Generation
The first time you run `te-api` or `te-api-ro` after installing (or after a `uv tool upgrade`), the tool downloads the OpenAPI schema from `https://api.transparentcdn.com/schema` with your credentials and generates the CLI modules. You will see a single line on stderr:

```
Initializing TE-API: downloading API schema...
```

If credentials are missing, the tool prints a clear message asking you to configure them and exits without doing anything else. After the build, subsequent runs are immediate.

To force a manual rebuild (for example, after the API is updated):
```bash
te-api build                                   # downloads the schema and regenerates both versions
te-api build --from-file transparent-api.yaml  # uses a local YAML instead of downloading
```

### Context Management (Company ID)
To avoid passing `--company-id <ID>` on every command, you can set a default company:

```bash
# Set a default ID
te-api set-company 12345

# Use commands without specifying the ID
te-api companies get alerts

# Override on a single call
te-api companies get alerts --company-id 67890

# Show the current configuration
te-api show-context

# Clear the context
te-api clear-company
```

The context is shared between `te-api` and `te-api-ro`.

`TRANSPARENT_COMPANY_ID` does the same thing for a single invocation and
takes precedence over the stored context:

```bash
TRANSPARENT_COMPANY_ID=12345 te-api companies get alerts
```

That is the form to use from a script or an automated caller: `set-company`
writes a file shared by every invocation, so a caller that works on
several companies would have to mutate global state around each call and
race with itself. Commands that take no company ID simply ignore the
variable, so it can be set unconditionally -- note that 79 of the 171
read-only commands do not accept `--company-id` at all, and passing the
flag to one of those is an error.

### Shell Completion
To enable autocompletion in your shell (Bash, Fish, Zsh):

```bash
# Bash
te-api completion bash > ~/.te-api-completion.bash
echo "source ~/.te-api-completion.bash" >> ~/.bashrc

# Fish
te-api completion fish > ~/.config/fish/completions/te-api.fish

# Zsh
te-api completion zsh > ~/.te-api-completion.zsh
echo "source ~/.te-api-completion.zsh" >> ~/.zshrc
```

Completion works independently for each binary (`te-api` and `te-api-ro`).

### Command Structure
The CLI follows an intuitive hierarchical layout:

```bash
te-api [MODULE] [VERB] [RESOURCE] [OPTIONS]
```

- **MODULE**: The API section (e.g. `companies`, `security`, `statistics`).
- **VERB**: The action to perform (`get`, `create`, `update`, `delete`). In `te-api-ro` only `get` is available.
- **RESOURCE**: The specific object (e.g. `current-user`, `rules`, `cache`).

Positional arguments with a finite set of values surface those choices directly in the help. For example:

```bash
te-api statistics get delivery --help
# Shows: Usage: te-api statistics get delivery [OPTIONS] {historic|analytic} {table|histogram}
```

For object-typed parameters (such as `--filters` in statistics), the help describes the expected JSON structure with field names, types, and which keys are required:

```bash
--filters TEXT  Filters. JSON object with keys:
                timestamp(object [required]): {from(integer [required]), to(integer [required])}
                vhost(array [required]) Zone names (array of string) ...
```

#### Passing parameters from a file

Quoting JSON on a command line is easy to get wrong: unless the whole
value is wrapped in single quotes, the shell strips the inner quotes and
the JSON arrives broken. Any command that takes query parameters also
accepts `--file`, which reads them from a JSON object instead:

```bash
cat > query.json <<'EOF'
{
  "filters": {
    "timestamp": {"from": 1779898235, "to": 1779899135},
    "vhost": ["www.example.com"],
    "transaction.messages.details.ruleId": ["942100"]
  }
}
EOF

te-api statistics get waf historic table --file query.json
```

Nested objects and arrays are written as real JSON and re-encoded for the
query string, so there is no escaping to get right. The rules:

- Explicit options win over the file, so a single value can be overridden
  ad hoc: `--file query.json --filters '{"vhost":["other"]}'`.
- A required parameter may arrive from the file instead of the command
  line. If it is missing from both, the command says which one.
- A key the command does not accept is an error, not a silent no-op, so a
  typo cannot quietly drop a filter.
- If an endpoint has a parameter of its own called `file`, the option is
  named `--params-file` on that command.

#### Examples
```bash
# Show information about the current user
te-api companies get current-user

# List alerts for a company
te-api companies get alerts <COMPANY_ID>

# Purge cache (te-api only, not available in te-api-ro)
te-api companies create invalidate <COMPANY_ID> --json-body '{"urls": ["..."]}'

# Query delivery statistics (available in both binaries)
te-api statistics get delivery analytic table --company-id 12345 \
  --key-field tcdn.varnish.agent \
  --filters '{"timestamp":{"from":1774269472,"to":1774269772},"vhost":[]}'

# The same thing with the filters in a file, no quoting to get wrong
te-api statistics get delivery analytic table --company-id 12345 \
  --key-field tcdn.varnish.agent --file query.json
```

### Differences between `te-api` and `te-api-ro`

| Feature | `te-api` | `te-api-ro` |
|---------|----------|-------------|
| GET operations | Yes | Yes |
| CREATE operations | Yes | No |
| UPDATE operations | Yes | No |
| DELETE operations | Yes | No |
| `authentication` module | Yes | No |
| Login / Context / Completions | Yes | Yes |

## 4. Project Architecture

The project is split into a **static core** (hand-written) and a **dynamic API layer** (code-generated).

### Main Components

1.  **Core (`te_api/`)**:
    -   `cli.py`: Hosts the `create_cli()` factory that builds a CLI group with the static commands (`login`, `set-company`, `clear-company`, `show-context`, `completion`, `build`) and lazily registers the API commands from the requested module on first use. Exposes two instances: `cli` (full) and `cli_ro` (read-only). **Contains no API business logic.**
    -   `auth.py`: Manages the OAuth2 flow plus token storage and renewal.
    -   `config.py`: Loads configuration from environment variables and `.env`.

2.  **Generator (`te_api/builder.py`)**:
    -   The heart of maintenance. Downloads the spec from `https://api.transparentcdn.com/schema` (or reads it from a local file with `--from-file`).
    -   Normalizes names, resolves version conflicts, and groups endpoints.
    -   Produces rich help text for object-typed parameters via `build_object_help()`, detailing fields, types, and required flags.
    -   Extracts `enum`/`pattern` values from the schema to drive `click.Choice` arguments and options (`choices_from_schema()`).
    -   Supports the `--read-only` flag to emit only GET operations.
    -   Exposes `ensure_api_built()`, which the CLI calls on first run to generate the modules automatically, and again whenever the generated layer was produced by a different version of the generator.

3.  **Full API Layer (`te_api/api/`)** -- generated at runtime:
    -   One module per OpenAPI tag (e.g. `audit.py`, `billing.py`) covering every operation.
    -   `registry.py`: imports all modules and registers them on the main CLI.
    -   Not committed to git (only the `__init__.py` is tracked).

4.  **Read-Only API Layer (`te_api/api_ro/`)** -- generated at runtime:
    -   Same structure as `api/`, but only GET operations.
    -   Not committed to git (only the `__init__.py` is tracked).

### Directory Layout

```text
te-api/
├── build_cli.py          # Dev shim: delegates to te_api.builder
├── pyproject.toml        # Project config and dependencies (two entry points)
├── uv.lock               # Dependency lockfile
├── te_api/               # Main package
│   ├── __init__.py
│   ├── __main__.py       # Entry point
│   ├── auth.py           # Authentication logic
│   ├── builder.py        # Generator that turns the OpenAPI schema into CLI modules
│   ├── cli.py            # CLI factory: create_cli() -> cli + cli_ro (auto-build included)
│   ├── config.py         # Configuration
│   ├── api/              # Modules generated at runtime (FULL - all operations)
│   │   └── __init__.py   # the only tracked file; everything else is gitignored
│   └── api_ro/           # Modules generated at runtime (READ-ONLY - GET only)
│       └── __init__.py
└── .gitignore
```

## 5. Maintenance and Regeneration

When the Transparent Edge API changes (new endpoints, parameter changes), or when your OAuth permissions change, regenerate the CLI:

```bash
te-api build                                   # downloads the schema and regenerates both layers
te-api build --from-file transparent-api.yaml  # uses a local YAML instead
```

Additional flags on the `build` subcommand:
- `--schema-url <URL>`: change the URL the spec is downloaded from.
- `--client-id <ID>` / `--client-secret <SECRET>`: pass the credentials on the command line instead of reading them from the environment.

When working inside the repository, the `build_cli.py` shim at the project root exposes the same functionality directly:
```bash
uv run build_cli.py                                   # downloads + writes te_api/api
uv run build_cli.py --output-dir te_api/api_ro --read-only
uv run build_cli.py --from-file transparent-api.yaml  # local YAML alternative
```

After regenerating, verify both binaries:
```bash
uv run te-api --help
uv run te-api-ro --help
```

To distribute updates, push the changes to the git repository. Users will pick them up with:
```bash
uv tool upgrade te-api
```

## 6. Technologies Used

-   **Python 3.12+**
-   **Click**: CLI framework.
-   **Requests**: HTTP client.
-   **uv**: Modern package and environment manager.
-   **PyYAML**: OpenAPI spec parser.
