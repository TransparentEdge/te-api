import click
import requests
import json
from te_api.auth import get_auth_headers
from te_api.config import Config

@click.group()
def cli():
    """Audit operations."""
    pass

@cli.group(name='get')
def get_group():
    """Get operations."""
    pass

@get_group.command(name='action')
@click.option('--search', 'search', help='A search term....', type=str)
@click.option('--output', 'output', help='Set to **\'std\'** to use standard pagination format....', type=str)
@click.option('--offset', 'offset', help='The number of items to **skip** before returning results. - Requires `limit` to be set. - Used for p...', type=int)
@click.option('--limit', 'limit', help='The maximum number of items to return per page. - If not provided, the response will return **all**...', type=int)
@click.option('--filters', 'filters', help='Time Filters...', required=True, type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_action(company_id, filters, limit, offset, output, search):
    """Get User actions"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/audit/action/{company_id}/"
    headers = get_auth_headers()
    params = {
        'filters': filters,
        'limit': limit,
        'offset': offset,
        'output': output,
        'search': search,
    }
    params = {k: v for k, v in params.items() if v is not None}
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

