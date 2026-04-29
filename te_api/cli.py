import click
import os
import sys
import subprocess
import importlib

from .config import Config
from . import builder


class _AutoBuildGroup(click.Group):
    """Click group that lazily downloads the OpenAPI schema and generates
    the API command modules on first use. The static commands declared
    below remain available without any build, so `te-api build`,
    `te-api login`, etc. can still run before the API has been
    generated."""

    def __init__(self, *args, api_module: str = "te_api.api",
                 read_only: bool = False, **kwargs):
        super().__init__(*args, **kwargs)
        self._api_module = api_module
        self._read_only = read_only
        self._api_loaded = False

    def _load_api_commands(self):
        if self._api_loaded:
            return
        builder.ensure_api_built(read_only=self._read_only)
        importlib.invalidate_caches()
        registry = importlib.import_module(f"{self._api_module}.registry")
        registry.register_api_commands(self)
        self._api_loaded = True

    def list_commands(self, ctx):
        self._load_api_commands()
        return super().list_commands(ctx)

    def get_command(self, ctx, cmd_name):
        cmd = super().get_command(ctx, cmd_name)
        if cmd is not None:
            return cmd
        # Trigger the auto-build only if the requested command is not one
        # of the static ones; this keeps `build`, `login`, etc. usable
        # without credentials.
        self._load_api_commands()
        return super().get_command(ctx, cmd_name)


def create_cli(api_module="te_api.api", description="Transparent Edge API CLI Tool.",
               read_only: bool = False):
    """Factory that builds a CLI group. API commands are registered
    lazily on first invocation."""

    @click.group(cls=_AutoBuildGroup, api_module=api_module, read_only=read_only)
    def cli():
        pass

    cli.help = description

    @cli.command()
    @click.argument("shell", type=click.Choice(["bash", "fish", "zsh"]), required=True)
    def completion(shell):
        """Generate shell completion script."""
        env_var = "_TE_API_COMPLETE"
        shell_val = f"{shell}_source"

        env = os.environ.copy()
        env[env_var] = shell_val

        try:
            subprocess.run([sys.argv[0]], env=env, check=True)
        except subprocess.CalledProcessError:
            click.echo("Error generating completion script.", err=True)

    @cli.command()
    def login():
        """Authenticate and store the access token."""
        try:
            Config.validate()
            from .auth import get_valid_token

            get_valid_token()
            click.echo("Authenticated successfully. Token stored.")
        except Exception as e:
            click.echo(f"Authentication failed: {e}")

    @cli.command()
    @click.argument("company_id", type=str)
    def set_company(company_id):
        """Set the default company ID for subsequent commands."""
        Config.set_context("company_id", company_id)
        click.echo(f"Default company ID set to: {company_id}")

    @cli.command()
    def clear_company():
        """Clear the default company ID."""
        Config.set_context("company_id", None)
        click.echo("Default company ID cleared.")

    @cli.command()
    def show_context():
        """Show the current context configuration."""
        company_id = Config.get_context("company_id")
        click.echo("Current Context:")
        click.echo(f"  Company ID: {company_id or 'Not set'}")
        click.echo(f"  Token File: {Config.TOKEN_FILE}")

    @cli.command(name="build")
    @click.option(
        "--from-file",
        "from_file",
        type=click.Path(exists=True, dir_okay=False),
        default=None,
        help="Use a local OpenAPI YAML/JSON file instead of downloading.",
    )
    @click.option(
        "--schema-url",
        default=builder.DEFAULT_SCHEMA_URL,
        show_default=True,
        help="URL to download the OpenAPI spec from.",
    )
    @click.option(
        "--client-id",
        default=None,
        help="OAuth2 client ID. Overrides TRANSPARENT_CLIENT_ID.",
    )
    @click.option(
        "--client-secret",
        default=None,
        help="OAuth2 client secret. Overrides TRANSPARENT_CLIENT_SECRET.",
    )
    def build_cmd(from_file, schema_url, client_id, client_secret):
        """(Re)generate the API command modules from the OpenAPI schema.

        Downloads the schema from `--schema-url` (default:
        https://api.transparentcdn.com/schema) using your OAuth2
        credentials, unless `--from-file` points at a local copy."""
        if from_file:
            click.echo(f"Loading spec from {from_file}...")
            spec = builder.load_spec(from_file)
        else:
            click.echo(f"Downloading spec from {schema_url}...")
            spec = builder.download_spec(schema_url, client_id, client_secret)

        # Always rebuild both layers so they stay in sync.
        builder.generate_from_spec(
            spec, str(builder._api_dir(read_only=False)), read_only=False
        )
        builder.generate_from_spec(
            spec, str(builder._api_dir(read_only=True)), read_only=True
        )
        click.echo("Build complete.")

    return cli


# Default full CLI
cli = create_cli(api_module="te_api.api", description="Transparent Edge API CLI Tool.")

# Read-only CLI
cli_ro = create_cli(
    api_module="te_api.api_ro",
    description="Transparent Edge API CLI Tool (read-only).",
    read_only=True,
)

if __name__ == "__main__":
    cli()
