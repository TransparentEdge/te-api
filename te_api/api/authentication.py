import click
import requests
import json
from te_api.auth import get_auth_headers
from te_api.config import Config

@click.group()
def cli():
    """Authentication operations."""
    pass

@cli.group(name='action')
def action_group():
    """Action operations."""
    pass

@action_group.command(name='get-token')
@click.option('--json-body', 'json_body', help='JSON string for request body')
def action_get_token(json_body):
    """Get API token"""
    url = f"{Config.API_URL}/v1/oauth2/access_token/"
    headers = get_auth_headers()
    params = {}
    data = json.loads(json_body) if json_body else None
    try:
        response = requests.post(url, headers=headers, params=params, json=data)
        response.raise_for_status()
        if response.content:
            try:
                click.echo(json.dumps(response.json(), indent=2))
            except json.JSONDecodeError:
                click.echo(response.text)
        else:
            click.echo('Success (No content)')
    except requests.exceptions.RequestException as e:
        click.echo(f"Error: {e}")
        if e.response is not None:
             click.echo(e.response.text)

