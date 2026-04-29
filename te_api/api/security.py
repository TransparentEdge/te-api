import click
import requests
import json
from te_api.auth import get_auth_headers
from te_api.config import Config

@click.group()
def cli():
    """Security operations."""
    pass

@cli.group(name='get')
def get_group():
    """Get operations."""
    pass

@get_group.command(name='safe-route')
@click.option('--site', 'site', help='Optional site ID to filter the safe route links by site (only used when listing)', type=int)
@click.option('--search', 'search', help='A search term. (only used when listing)', type=str)
@click.option('--offset', 'offset', help='The number of items to **skip** before returning results. - Requires `limit` to be set. - Used for pagination to retrieve the next set of results. - Example: `offset=10` skips the first 10 items. (only used when listing)', type=int)
@click.option('--limit', 'limit', help='The maximum number of items to return per page. - If not provided, the response will return **all** items. - If provided, the response will be **paginated**. - Use in combination with `offset` for pagination. (only used when listing)', type=int)
@click.option('--company-id', 'company_id', required=False, type=int, help='ID of the company to get safe route links for (Default: from context)')
@click.argument('safe_route_link_id', required=False, type=str, default=None)
def get_safe_route(company_id, limit, offset, search, site, safe_route_link_id):
    """Get the safe route link list (omit ID) / Get safe route link details (with ID)"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    if safe_route_link_id is not None:
        url = f"{Config.API_URL}/v1/security/{company_id}/safe_route/{safe_route_link_id}/"
        params = {}
    else:
        url = f"{Config.API_URL}/v1/security/{company_id}/safe_route/"
        params = {
            'limit': limit,
            'offset': offset,
            'search': search,
            'site': site,
        }
        params = {k: v for k, v in params.items() if v is not None}
    headers = get_auth_headers()
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

@get_group.command(name='safe-route-history')
@click.argument('safe_route_link_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
def get_safe_route_history(company_id, safe_route_link_id):
    """Get SafeRoute link data"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/security/{company_id}/safe_route/{safe_route_link_id}/history/"
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

@cli.group(name='create')
def create_group():
    """Create operations."""
    pass

@create_group.command(name='safe-route')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
def create_safe_route(company_id, json_body):
    """Create a safe route link"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/security/{company_id}/safe_route/"
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

@cli.group(name='update')
def update_group():
    """Update operations."""
    pass

@update_group.command(name='safe-route')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.argument('safe_route_link_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
def update_safe_route(company_id, safe_route_link_id, json_body):
    """Update safe route link"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/security/{company_id}/safe_route/{safe_route_link_id}/"
    headers = get_auth_headers()
    params = {}
    data = json.loads(json_body) if json_body else None
    try:
        response = requests.put(url, headers=headers, params=params, json=data)
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

@delete_group.command(name='safe-route')
@click.argument('safe_route_link_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
def delete_safe_route(company_id, safe_route_link_id):
    """Delete safe route link"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/security/{company_id}/safe_route/{safe_route_link_id}/"
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

