import click
import requests
import json
from te_api.auth import get_auth_headers
from te_api.config import Config

@click.group()
def cli():
    """Billing operations."""
    pass

@cli.group(name='get')
def get_group():
    """Get operations."""
    pass

@get_group.command(name='billing-info')
@click.argument('client_id', type=str)
def get_billing_info(client_id):
    """Billing info List"""
    url = f"{Config.API_URL}/v1/billing/{client_id}/billing_info/"
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

@get_group.command(name='tenant')
@click.argument('client_id', type=str)
@click.argument('tenant_id', required=False, type=str, default=None)
def get_tenant(client_id, tenant_id):
    """Client tenants list information (omit ID) / Client tenant detail information (with ID)"""
    if tenant_id is not None:
        url = f"{Config.API_URL}/v1/billing/{client_id}/tenant/{tenant_id}"
        params = {}
    else:
        url = f"{Config.API_URL}/v1/billing/{client_id}/tenant/"
        params = {}
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

@get_group.command(name='account-verify')
@click.argument('client_id', type=str)
def get_account_verify(client_id):
    """Check if client is marked for deletion"""
    url = f"{Config.API_URL}/v1/billing/account/{client_id}/verify/"
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

@get_group.command(name='tenant-create')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.argument('tenant_id', type=str)
def get_tenant_create(tenant_id, json_body):
    """Tenant creation"""
    url = f"{Config.API_URL}/v1/billing/tenant/{tenant_id}/"
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

@get_group.command(name='tenant-service')
@click.argument('tenant_id', type=str)
@click.argument('service_id', required=False, type=str, default=None)
def get_tenant_service(tenant_id, service_id):
    """Tenant services list information (omit ID) / Tenant service detail information (with ID)"""
    if service_id is not None:
        url = f"{Config.API_URL}/v1/billing/tenant/{tenant_id}/service/{service_id}/"
        params = {}
    else:
        url = f"{Config.API_URL}/v1/billing/tenant/{tenant_id}/service/"
        params = {}
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

@cli.group(name='update')
def update_group():
    """Update operations."""
    pass

@update_group.command(name='billing-info')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.argument('client_id', type=str)
def update_billing_info(client_id, json_body):
    """Update billing info"""
    url = f"{Config.API_URL}/v1/billing/{client_id}/billing_info/"
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

@update_group.command(name='tenant')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.argument('tenant_id', type=str)
def update_tenant(tenant_id, json_body):
    """Tenant update"""
    url = f"{Config.API_URL}/v1/billing/tenant/{tenant_id}/"
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

@cli.group(name='create')
def create_group():
    """Create operations."""
    pass

@create_group.command(name='download')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.argument('client_id', type=str)
def create_download(client_id, json_body):
    """Download Bill(s)"""
    url = f"{Config.API_URL}/v1/billing/{client_id}/download/"
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

@create_group.command(name='tenant-service')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.argument('tenant_id', type=str)
def create_tenant_service(tenant_id, json_body):
    """Add service to tenant"""
    url = f"{Config.API_URL}/v1/billing/tenant/{tenant_id}/service/"
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

@cli.group(name='delete')
def delete_group():
    """Delete operations."""
    pass

@delete_group.command(name='account')
@click.argument('client_id', type=str)
def delete_account(client_id):
    """Marks companies for deletion"""
    url = f"{Config.API_URL}/v1/billing/account/{client_id}/"
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

@delete_group.command(name='tenant')
@click.argument('tenant_id', type=str)
def delete_tenant(tenant_id):
    """Delete tenant"""
    url = f"{Config.API_URL}/v1/billing/tenant/{tenant_id}/"
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

@delete_group.command(name='tenant-service')
@click.argument('tenant_id', type=str)
@click.argument('service_id', type=str)
def delete_tenant_service(service_id, tenant_id):
    """Remove service from tenant"""
    url = f"{Config.API_URL}/v1/billing/tenant/{tenant_id}/service/{service_id}/"
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

