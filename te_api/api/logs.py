import click
import requests
import json
from te_api.auth import get_auth_headers
from te_api.config import Config

@click.group()
def cli():
    """Logs operations."""
    pass

@cli.group(name='get')
def get_group():
    """Get operations."""
    pass

@get_group.command(name='index')
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_index(company_id):
    """Get Logs List"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/logs/{company_id}/"
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

@get_group.command(name='connection-status')
@click.argument('log_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_connection_status(company_id, log_id):
    """Check Log Storage Connection"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/logs/{company_id}/{log_id}/connection_status/"
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

@get_group.command(name='streaming-ip')
@click.option('--search', 'search', help='A search term....', type=str)
@click.option('--offset', 'offset', help='The number of items to **skip** before returning results. - Requires `limit` to be set. - Used for p...', type=int)
@click.option('--limit', 'limit', help='The maximum number of items to return per page. - If not provided, the response will return **all**...', type=int)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_streaming_ip(company_id, limit, offset, search):
    """Get Streaming Logs IP List"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/logs/{company_id}/streaming/ip/"
    headers = get_auth_headers()
    params = {
        'limit': limit,
        'offset': offset,
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

@get_group.command(name='streaming-template')
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_streaming_template(company_id):
    """Get Streaming Logs Template List"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/logs/{company_id}/streaming/template/"
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

@create_group.command(name='index')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def create_index(company_id, json_body):
    """Create Log"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/logs/{company_id}/"
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

@create_group.command(name='streaming-ip')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def create_streaming_ip(company_id, json_body):
    """Set Streaming Logs IP"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/logs/{company_id}/streaming/ip/"
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

@update_group.command(name='index')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.argument('log_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def update_index(company_id, log_id, json_body):
    """Edit Log"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/logs/{company_id}/{log_id}/"
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

@update_group.command(name='streaming-ip')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.argument('ip_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def update_streaming_ip(company_id, ip_id, json_body):
    """Edit Streaming Log IP"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/logs/{company_id}/streaming/ip/{ip_id}/"
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

@delete_group.command(name='index')
@click.argument('log_id', type=int)
@click.option('--company-id', 'company_id', required=False, type=int, help='ID of the company that owns the log... (Default: from context)')
def delete_index(company_id, log_id):
    """Delete Log"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/logs/{company_id}/{log_id}/"
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

@delete_group.command(name='streaming-ip')
@click.argument('ip_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def delete_streaming_ip(company_id, ip_id):
    """Delete Streaming Log IP"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/logs/{company_id}/streaming/ip/{ip_id}/"
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

