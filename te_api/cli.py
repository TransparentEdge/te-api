import click
import os
import sys
import subprocess
from .config import Config


@click.group()
def cli():
    """Transparent Edge API CLI Tool."""
    pass


@cli.command()
@click.argument("shell", type=click.Choice(["bash", "fish", "zsh"]), required=True)
def completion(shell):
    """Generate shell completion script."""
    env_var = "_TE_API_COMPLETE"
    shell_val = f"{shell}_source"

    # We invoke ourselves with the magic env var that triggers click's completion output
    env = os.environ.copy()
    env[env_var] = shell_val

    try:
        # We call the current executable again
        subprocess.run([sys.argv[0]], env=env, check=True)
    except subprocess.CalledProcessError:
        click.echo("Error generating completion script.", err=True)


@cli.command()
def login():
    """Authenticate and store the access token."""
    try:
        Config.validate()
        # Force getting a new token
        from .auth import get_valid_token

        token = get_valid_token()
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
    click.echo(f"Current Context:")
    click.echo(f"  Company ID: {company_id or 'Not set'}")
    click.echo(f"  Token File: {Config.TOKEN_FILE}")


# Dynamic registration of API commands
try:
    from .api.registry import register_api_commands

    register_api_commands(cli)
except ImportError:
    pass  # Registry might not exist yet during first build

if __name__ == "__main__":
    cli()
