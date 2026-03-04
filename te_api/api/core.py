import click
import requests
import json
from te_api.auth import get_auth_headers
from te_api.config import Config

@click.group()
def cli():
    """Core operations."""
    pass

@cli.group(name='get')
def get_group():
    """Get operations."""
    pass

@get_group.command(name='task-status')
@click.argument('task_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_task_status(company_id, task_id):
    """Task Status"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/core/{company_id}/task-status/{task_id}/"
    headers = get_auth_headers()
    params = {}
    data = None
    try:
        response = requests.get(url, headers=headers, params=params, json=data)
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

@cli.group(name='delete')
def delete_group():
    """Delete operations."""
    pass

@delete_group.command(name='task-status')
@click.argument('task_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def delete_task_status(company_id, task_id):
    """Revoke Task"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/core/{company_id}/task-status/{task_id}/"
    headers = get_auth_headers()
    params = {}
    data = None
    try:
        response = requests.delete(url, headers=headers, params=params, json=data)
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

@cli.group(name='create')
def create_group():
    """Create operations."""
    pass

@create_group.command(name='revoke-token')
@click.option('--all', 'all', help='If set to `true`, all tokens of the user will be revoked...', is_flag=True)
def create_revoke_token(all):
    """Revoke token"""
    url = f"{Config.API_URL}/v1/core/revoke_token/"
    headers = get_auth_headers()
    params = {
        'all': all,
    }
    params = {k: v for k, v in params.items() if v is not None}
    data = None
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

