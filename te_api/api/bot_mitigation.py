import click
import requests
import json
from te_api.auth import get_auth_headers
from te_api.config import Config

@click.group()
def cli():
    """Bot_mitigation operations."""
    pass

@cli.group(name='get')
def get_group():
    """Get operations."""
    pass

@get_group.command(name='allow-list-public')
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_allow_list_public(company_id):
    """Public allow lists"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/bot_mitigation/{company_id}/allow_list/public/"
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

@get_group.command(name='client-analysis')
@click.option('--filters', 'filters', help='Time Filters...', required=True, type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_client_analysis(company_id, filters):
    """Client analysis"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/bot_mitigation/{company_id}/client/analysis/"
    headers = get_auth_headers()
    params = {
        'filters': filters,
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

@get_group.command(name='deny-list-public')
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_deny_list_public(company_id):
    """Public deny lists"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/bot_mitigation/{company_id}/deny_list/public/"
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

@get_group.command(name='origin-config')
@click.option('--filters', 'filters', help='Site filters...', required=True, type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_origin_config(company_id, filters):
    """Origin config List"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/bot_mitigation/{company_id}/origin_config/"
    headers = get_auth_headers()
    params = {
        'filters': filters,
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

@get_group.command(name='origin-script-site')
@click.argument('site_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_origin_script_site(company_id, site_id):
    """Origin script"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/bot_mitigation/{company_id}/origin_script/site/{site_id}/"
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

@get_group.command(name='origin-token')
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_origin_token(company_id):
    """Token/site List"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/bot_mitigation/{company_id}/origin_token/"
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

@get_group.command(name='origin-token-site')
@click.argument('site_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_origin_token_site(company_id, site_id):
    """Token Detail"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/bot_mitigation/{company_id}/origin_token/site/{site_id}/"
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

@get_group.command(name='origin-token-site-create')
@click.argument('site_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_origin_token_site_create(company_id, site_id):
    """Create token"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/bot_mitigation/{company_id}/origin_token/site/{site_id}/"
    headers = get_auth_headers()
    params = {}
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

@get_group.command(name='site-allow-list-private')
@click.argument('site_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_site_allow_list_private(company_id, site_id):
    """Private allow lists"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/bot_mitigation/{company_id}/site/{site_id}/allow_list/private/"
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

@get_group.command(name='site-allow-list-private-list')
@click.argument('site_id', type=str)
@click.argument('list_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_site_allow_list_private_list(company_id, list_id, site_id):
    """Private allow list Details"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/bot_mitigation/{company_id}/site/{site_id}/allow_list/private/{list_id}/"
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

@get_group.command(name='site-deny-list-private')
@click.argument('site_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_site_deny_list_private(company_id, site_id):
    """Private deny lists"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/bot_mitigation/{company_id}/site/{site_id}/deny_list/private/"
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

@get_group.command(name='site-deny-list-private-list')
@click.argument('site_id', type=str)
@click.argument('list_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_site_deny_list_private_list(company_id, list_id, site_id):
    """Private deny list Details"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/bot_mitigation/{company_id}/site/{site_id}/deny_list/private/{list_id}/"
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

@get_group.command(name='traffic-analysis')
@click.option('--filters', 'filters', help='Time Filters...', required=True, type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_traffic_analysis(company_id, filters):
    """Traffic analysis"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/bot_mitigation/{company_id}/traffic/analysis/"
    headers = get_auth_headers()
    params = {
        'filters': filters,
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

@cli.group(name='update')
def update_group():
    """Update operations."""
    pass

@update_group.command(name='allow-list-public-site')
@click.argument('site_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
@click.argument('allow_list_id', type=str)
def update_allow_list_public_site(allow_list_id, company_id, site_id):
    """Update public allow list status"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/bot_mitigation/{company_id}/allow_list/public/{allow_list_id}/site/{site_id}/"
    headers = get_auth_headers()
    params = {}
    data = None
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

@update_group.command(name='deny-list-public-site')
@click.argument('site_id', type=str)
@click.argument('deny_list_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def update_deny_list_public_site(company_id, deny_list_id, site_id):
    """Updat public deny list status"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/bot_mitigation/{company_id}/deny_list/public/{deny_list_id}/site/{site_id}/"
    headers = get_auth_headers()
    params = {}
    data = None
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

@update_group.command(name='origin-config')
@click.option('--filters', 'filters', help='Site filters...', required=True, type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def update_origin_config(company_id, filters):
    """Updates Origin config"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/bot_mitigation/{company_id}/origin_config/"
    headers = get_auth_headers()
    params = {
        'filters': filters,
    }
    params = {k: v for k, v in params.items() if v is not None}
    data = None
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

@update_group.command(name='site-allow-list-private')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.argument('site_id', type=str)
@click.argument('list_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def update_site_allow_list_private(company_id, list_id, site_id, json_body):
    """Update private allow list"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/bot_mitigation/{company_id}/site/{site_id}/allow_list/private/{list_id}/"
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

@update_group.command(name='site-deny-list-private')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.argument('site_id', type=str)
@click.argument('list_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def update_site_deny_list_private(company_id, list_id, site_id, json_body):
    """Update private deny list"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/bot_mitigation/{company_id}/site/{site_id}/deny_list/private/{list_id}/"
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

@delete_group.command(name='origin-token-site')
@click.argument('site_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def delete_origin_token_site(company_id, site_id):
    """Delete token"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/bot_mitigation/{company_id}/origin_token/site/{site_id}/"
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

@delete_group.command(name='site-allow-list-private')
@click.argument('site_id', type=str)
@click.argument('list_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def delete_site_allow_list_private(company_id, list_id, site_id):
    """Delete private allow list"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/bot_mitigation/{company_id}/site/{site_id}/allow_list/private/{list_id}/"
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

@delete_group.command(name='site-deny-list-private')
@click.argument('site_id', type=str)
@click.argument('list_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def delete_site_deny_list_private(company_id, list_id, site_id):
    """Delete private deny list"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/bot_mitigation/{company_id}/site/{site_id}/deny_list/private/{list_id}/"
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

@create_group.command(name='site-allow-list-private')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.argument('site_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def create_site_allow_list_private(company_id, site_id, json_body):
    """Create private allow list"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/bot_mitigation/{company_id}/site/{site_id}/allow_list/private/"
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

@create_group.command(name='site-deny-list-private')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.argument('site_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def create_site_deny_list_private(company_id, site_id, json_body):
    """Create private deny list"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/bot_mitigation/{company_id}/site/{site_id}/deny_list/private/"
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

