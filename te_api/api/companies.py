import click
import requests
import json
from te_api.auth import get_auth_headers
from te_api.config import Config

@click.group()
def cli():
    """Companies operations."""
    pass

@cli.group(name='create')
def create_group():
    """Create operations."""
    pass

@create_group.command(name='autoprovisioning-ssldnsverificationcname')
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def create_autoprovisioning_ssldnsverificationcname(company_id):
    """Retrieve verification challenge CNAME"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/ssldnsverificationcname/"
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

@create_group.command(name='alerts')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def create_alerts(company_id, json_body):
    """Create Alert"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/alerts/"
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

@create_group.command(name='invalidate')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def create_invalidate(company_id, json_body):
    """Create Invalidate Urls"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/invalidate/"
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

@create_group.command(name='lists')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def create_lists(company_id, json_body):
    """Create Network ACL"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/lists/"
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

@create_group.command(name='prefetch')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def create_prefetch(company_id, json_body):
    """Warm up Cache"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/prefetch/"
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

@create_group.command(name='refetch')
@click.argument('invalidation_type', type=str)
@click.argument('invalidation_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def create_refetch(company_id, invalidation_id, invalidation_type):
    """Refetch Invalidation"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/refetch/{invalidation_type}/{invalidation_id}/"
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

@create_group.command(name='services-subscription')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def create_services_subscription(company_id, json_body):
    """Activate service"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/services/subscription/"
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

@create_group.command(name='sites')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.option('--search', 'search', help='A search term....', type=str)
@click.option('--offset', 'offset', help='The number of items to **skip** before returning results. - Requires `limit` to be set. - Used for p...', type=int)
@click.option('--limit', 'limit', help='The maximum number of items to return per page. - If not provided, the response will return **all**...', type=int)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def create_sites(company_id, limit, offset, search, json_body):
    """Create Site"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/sites/"
    headers = get_auth_headers()
    params = {
        'limit': limit,
        'offset': offset,
        'search': search,
    }
    params = {k: v for k, v in params.items() if v is not None}
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

@create_group.command(name='sites-enable-ssl')
@click.argument('id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def create_sites_enable_ssl(company_id, id):
    """Create SSL certificate for Site"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/sites/{id}/enable_ssl/"
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

@create_group.command(name='sites-wizard')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def create_sites_wizard(company_id, json_body):
    """Site Wizard - Automatic Onboarding"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/sites/wizard/"
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

@create_group.command(name='siteverification')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def create_siteverification(company_id, json_body):
    """Site verification"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/siteverification/"
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

@create_group.command(name='tag-invalidate')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def create_tag_invalidate(company_id, json_body):
    """Create Invalidate Tags"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/tag_invalidate/"
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

@create_group.command(name='users')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def create_users(company_id, json_body):
    """Create User"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/users/"
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

@create_group.command(name='clone')
@click.option('--json-body', 'json_body', help='JSON string for request body')
def create_clone(json_body):
    """Clone Company"""
    url = f"{Config.API_URL}/v1/companies/clone/"
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

@create_group.command(name='tenant-company-create')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.argument('tenant_id', type=str)
def create_tenant_company_create(tenant_id, json_body):
    """Company creation for a selected tenant"""
    url = f"{Config.API_URL}/v1/companies/tenant/{tenant_id}/company/create/"
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

@create_group.command(name='core-password')
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def create_core_password(company_id):
    """Generate Random password"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/core/password/{company_id}/"
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

@cli.group(name='get')
def get_group():
    """Get operations."""
    pass

@get_group.command(name='index')
def get_index():
    """Companies List"""
    url = f"{Config.API_URL}/v1/companies/"
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

@get_group.command(name='list')
@click.option('--search', 'search', help='A search term....', type=str)
@click.option('--offset', 'offset', help='The number of items to **skip** before returning results. - Requires `limit` to be set. - Used for p...', type=int)
@click.option('--limit', 'limit', help='The maximum number of items to return per page. - If not provided, the response will return **all**...', type=int)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_list(company_id, limit, offset, search):
    """Company Details"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/"
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

@get_group.command(name='alerts')
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_alerts(company_id):
    """Alert List"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/alerts/"
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

@get_group.command(name='alerts-list')
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
@click.argument('alert_id', type=str)
def get_alerts_list(alert_id, company_id):
    """Alert Details"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/alerts/{alert_id}/"
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

@get_group.command(name='cache-status')
@click.option('--url', 'url', help='URL completa a verificar (debe empezar con http:// o https://)...', required=True, type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_cache_status(company_id, url):
    """Check cache status"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/cachestatus/"
    headers = get_auth_headers()
    params = {
        'url': url,
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

@get_group.command(name='histogram-googlebot')
@click.option('--filters', 'filters', help='Time Filters...', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_histogram_googlebot(company_id, filters):
    """Google Bots data"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/histogram/googlebot/"
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

@get_group.command(name='invalidate')
@click.option('--search', 'search', help='A search term....', type=str)
@click.option('--output', 'output', help='Set to **\'std\'** to use standard pagination format....', type=str)
@click.option('--offset', 'offset', help='The number of items to **skip** before returning results. - Requires `limit` to be set. - Used for p...', type=int)
@click.option('--limit', 'limit', help='The maximum number of items to return per page. - If not provided, the response will return **all**...', type=int)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_invalidate(company_id, limit, offset, output, search):
    """Invalidated urls List"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/invalidate/"
    headers = get_auth_headers()
    params = {
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

@get_group.command(name='invalidate-histogram')
@click.option('--key-field', 'key_field', help='Get data for Purges & Bans...', required=True, type=str)
@click.option('--filters', 'filters', help='Time Filters...', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_invalidate_histogram(company_id, filters, key_field):
    """Invalidation BAN & PURGE Graphs data"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/invalidate/histogram/"
    headers = get_auth_headers()
    params = {
        'filters': filters,
        'key_field': key_field,
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

@get_group.command(name='lists')
@click.option('--search', 'search', help='A search term....', type=str)
@click.option('--offset', 'offset', help='The number of items to **skip** before returning results. - Requires `limit` to be set. - Used for p...', type=int)
@click.option('--limit', 'limit', help='The maximum number of items to return per page. - If not provided, the response will return **all**...', type=int)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
@click.option('--auto-generated', 'auto_generated', help='Filter by auto_generated lists...', is_flag=True)
@click.option('--address-count-only', 'address_count_only', help='If True, only the count of addresses will be shown, \'addresses\' parameter will be omitted. Useful ...', is_flag=True)
@click.option('--address', 'address', help='Filter lists that contains the requested address. Only shows the related address in the \'addresses...', type=str)
@click.option('--active', 'active', help='Filter by active lists...', is_flag=True)
def get_lists(active, address, address_count_only, auto_generated, company_id, limit, offset, search):
    """Network ACL List"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/lists/"
    headers = get_auth_headers()
    params = {
        'active': active,
        'address': address,
        'address_count_only': address_count_only,
        'auto_generated': auto_generated,
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

@get_group.command(name='lists-address-create')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.argument('network_list_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
@click.argument('address', type=str)
def get_lists_address_create(address, company_id, network_list_id, json_body):
    """Add Address to Network ACL"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/lists/{network_list_id}/address/{address}"
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

@get_group.command(name='lists-antiddos-history')
@click.option('--to', 'to', help='End date (inclusive) in format YYYY-MM-DD. Maximum range is 31 days....', required=True, type=str)
@click.option('--from', 'from_param', help='Start date (inclusive) in format YYYY-MM-DD....', required=True, type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_lists_antiddos_history(company_id, from_param, to):
    """Network Anti-DDoS History"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/lists/antiddos/history/"
    headers = get_auth_headers()
    params = {
        'from': from_param,
        'to': to,
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

@get_group.command(name='prefetch')
@click.option('--search', 'search', help='A search term....', type=str)
@click.option('--offset', 'offset', help='The number of items to **skip** before returning results. - Requires `limit` to be set. - Used for p...', type=int)
@click.option('--limit', 'limit', help='The maximum number of items to return per page. - If not provided, the response will return **all**...', type=int)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_prefetch(company_id, limit, offset, search):
    """Cached Urls List"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/prefetch/"
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

@get_group.command(name='reactioninfo-retrieve')
@click.option('--service', 'service', help='Filter by service type...', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_reactioninfo_retrieve(company_id, service):
    """Reaction Info List"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/reactioninfo/"
    headers = get_auth_headers()
    params = {
        'service': service,
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

@get_group.command(name='services-subscribable')
@click.option('--company-id', 'company_id', required=False, type=int, help='ID of the company to get subscribable services for... (Default: from context)')
def get_services_subscribable(company_id):
    """Subscribable services List"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/services/subscribable"
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

@get_group.command(name='services-subscription')
@click.option('--company-id', 'company_id', required=False, type=int, help='ID of the company to get active services for... (Default: from context)')
def get_services_subscription(company_id):
    """Active services List"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/services/subscription/"
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

@get_group.command(name='sites')
@click.option('--search', 'search', help='A search term....', type=str)
@click.option('--offset', 'offset', help='The number of items to **skip** before returning results. - Requires `limit` to be set. - Used for p...', type=int)
@click.option('--limit', 'limit', help='The maximum number of items to return per page. - If not provided, the response will return **all**...', type=int)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_sites(company_id, limit, offset, search):
    """Sites List"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/sites/"
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

@get_group.command(name='sites-wizard-status')
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_sites_wizard_status(company_id):
    """Site Wizard Status - List Pending"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/sites/wizard/status/"
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

@get_group.command(name='support')
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_support(company_id):
    """Company support information"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/support/"
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

@get_group.command(name='tag-invalidate')
@click.option('--search', 'search', help='A search term....', type=str)
@click.option('--output', 'output', help='Set to **\'std\'** to use standard pagination format....', type=str)
@click.option('--offset', 'offset', help='The number of items to **skip** before returning results. - Requires `limit` to be set. - Used for p...', type=int)
@click.option('--limit', 'limit', help='The maximum number of items to return per page. - If not provided, the response will return **all**...', type=int)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_tag_invalidate(company_id, limit, offset, output, search):
    """Invalidated tags List"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/tag_invalidate/"
    headers = get_auth_headers()
    params = {
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

@get_group.command(name='users')
@click.option('--search', 'search', help='A search term....', type=str)
@click.option('--role', 'role', help='Filter users by role name...', type=str)
@click.option('--offset', 'offset', help='The number of items to **skip** before returning results. - Requires `limit` to be set. - Used for p...', type=int)
@click.option('--limit', 'limit', help='The maximum number of items to return per page. - If not provided, the response will return **all**...', type=int)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_users(company_id, limit, offset, role, search):
    """Users List"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/users/"
    headers = get_auth_headers()
    params = {
        'limit': limit,
        'offset': offset,
        'role': role,
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

@get_group.command(name='users-tokenrequests')
@click.option('--user-id', 'user_id_opt', help='User ID...', type=int)
@click.argument('user_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_users_tokenrequests(company_id, user_id, user_id_opt):
    """User tokens List"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/users/{user_id}/tokenrequests/"
    headers = get_auth_headers()
    params = {
        'user_id': user_id_opt,
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

@get_group.command(name='current-user')
def get_current_user():
    """Current User information (New version)"""
    url = f"{Config.API_URL}/v2/companies/current_user/"
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

@get_group.command(name='ipranges')
@click.option('--group', 'group', help='Node group name to filter the IP Ranges...', type=str)
@click.option('--format', 'format', help='...', type=str)
def get_ipranges(format, group):
    """IPs Ranges List"""
    url = f"{Config.API_URL}/v2/companies/ipranges/"
    headers = get_auth_headers()
    params = {
        'format': format,
        'group': group,
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

@get_group.command(name='oauth-create')
@click.argument('user_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_oauth_create(company_id, user_id):
    """Generate User credentials"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/oauth/create/{company_id}/{user_id}/"
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

@get_group.command(name='subscribable-services-marked-4-dead')
def get_subscribable_services_marked_4_dead():
    """Deactivated services list"""
    url = f"{Config.API_URL}/v1/companies/services/subscription"
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

@get_group.command(name='users-credentials-create')
def get_users_credentials_create():
    """Create User credentials"""
    url = f"{Config.API_URL}/v1/users/credentials/"
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

@get_group.command(name='billing-current-user-client')
@click.argument('client_id', type=str)
def get_billing_current_user_client(client_id):
    """Client information"""
    url = f"{Config.API_URL}/v2/billing/current_user/client/{client_id}/"
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

@get_group.command(name='billing-current-user-clients')
def get_billing_current_user_clients():
    """Clients list information for current User"""
    url = f"{Config.API_URL}/v2/billing/current_user/clients/"
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

@get_group.command(name='billing-current-user-tenant')
@click.argument('tenant_id', type=str)
def get_billing_current_user_tenant(tenant_id):
    """Client information"""
    url = f"{Config.API_URL}/v2/billing/current_user/tenant/{tenant_id}/"
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

@get_group.command(name='billing-current-user-tenants')
def get_billing_current_user_tenants():
    """Clients list information for current User"""
    url = f"{Config.API_URL}/v2/billing/current_user/tenants/"
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

@get_group.command(name='current-user-companies')
def get_current_user_companies():
    """User related companies list"""
    url = f"{Config.API_URL}/v2/companies/current_user/companies/"
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

@get_group.command(name='current-user-company')
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_current_user_company(company_id):
    """Company information"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v2/companies/current_user/company/{company_id}/"
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

@get_group.command(name='current-user-company-roles')
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_current_user_company_roles(company_id):
    """User company roles"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v2/companies/current_user/company/{company_id}/roles/"
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

@get_group.command(name='current-user-company-services-retrieve')
@click.option('--company-id', 'company_id', required=False, type=int, help='ID of the company to get services information for... (Default: from context)')
def get_current_user_company_services_retrieve(company_id):
    """User services list"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v2/companies/current_user/company/{company_id}/services/"
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

@cli.group(name='update')
def update_group():
    """Update operations."""
    pass

@update_group.command(name='index')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def update_index(company_id, json_body):
    """Edit Company"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/"
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

@update_group.command(name='alerts')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
@click.argument('alert_id', type=str)
def update_alerts(alert_id, company_id, json_body):
    """Edit Alert"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/alerts/{alert_id}/"
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

@update_group.command(name='alerts-partial')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
@click.argument('alert_id', type=str)
def update_alerts_partial(alert_id, company_id, json_body):
    """Edit Alert"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/alerts/{alert_id}/"
    headers = get_auth_headers()
    params = {}
    data = json.loads(json_body) if json_body else None
    try:
        response = requests.patch(url, headers=headers, params=params, json=data)
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

@update_group.command(name='lists')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.argument('network_list_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def update_lists(company_id, network_list_id, json_body):
    """Update Network ACL"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/lists/{network_list_id}/"
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

@update_group.command(name='lists-partial')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.argument('network_list_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def update_lists_partial(company_id, network_list_id, json_body):
    """Partially update Network ACL"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/lists/{network_list_id}/"
    headers = get_auth_headers()
    params = {}
    data = json.loads(json_body) if json_body else None
    try:
        response = requests.patch(url, headers=headers, params=params, json=data)
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

@update_group.command(name='self-user')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.argument('user_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def update_self_user(company_id, user_id, json_body):
    """Edit User information"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/self_user/{user_id}/"
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

@update_group.command(name='sites')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.argument('id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def update_sites(company_id, id, json_body):
    """Update Site"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/sites/{id}/"
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

@update_group.command(name='sites-wizard')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def update_sites_wizard(company_id, json_body):
    """Site Wizard - Confirm Backend Creation"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/sites/wizard/"
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

@update_group.command(name='users')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.argument('user_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def update_users(company_id, user_id, json_body):
    """Update User"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/users/{user_id}/"
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

@update_group.command(name='change-password')
@click.option('--json-body', 'json_body', help='JSON string for request body')
def update_change_password(json_body):
    """Change password"""
    url = f"{Config.API_URL}/v1/companies/change_password/"
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

@update_group.command(name='users-credentials')
def update_users_credentials():
    """Update User credentials"""
    url = f"{Config.API_URL}/v1/users/credentials/"
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

@cli.group(name='delete')
def delete_group():
    """Delete operations."""
    pass

@delete_group.command(name='index')
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def delete_index(company_id):
    """Delete Company"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/"
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

@delete_group.command(name='alerts')
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
@click.argument('alert_id', type=str)
def delete_alerts(alert_id, company_id):
    """Delete Alert"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/alerts/{alert_id}/"
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

@delete_group.command(name='lists')
@click.argument('network_list_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def delete_lists(company_id, network_list_id):
    """Delete Network ACL"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/lists/{network_list_id}/"
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

@delete_group.command(name='lists-address')
@click.argument('network_list_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
@click.argument('address', type=str)
def delete_lists_address(address, company_id, network_list_id):
    """Delete Address from Network ACL"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/lists/{network_list_id}/address/{address}"
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

@delete_group.command(name='services-subscription')
@click.argument('service_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def delete_services_subscription(company_id, service_id):
    """Delete active service"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/services/subscription/{service_id}/"
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

@delete_group.command(name='sites')
@click.argument('id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def delete_sites(company_id, id):
    """Delete Site"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/sites/{id}/"
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

@delete_group.command(name='users')
@click.argument('user_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def delete_users(company_id, user_id):
    """Delete User"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/users/{user_id}/"
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

@delete_group.command(name='users-tokenrequests')
@click.argument('user_id', type=str)
@click.argument('token_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def delete_users_tokenrequests(company_id, token_id, user_id):
    """Delete User token"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/users/{user_id}/tokenrequests/{token_id}/"
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

@cli.group(name='action')
def action_group():
    """Action operations."""
    pass

@action_group.command(name='invalidate-list-2')
@click.argument('size', type=str)
@click.option('--search', 'search', help='A search term....', type=str)
@click.option('--output', 'output', help='Set to **\'std\'** to use standard pagination format....', type=str)
@click.option('--offset', 'offset', help='The number of items to **skip** before returning results. - Requires `limit` to be set. - Used for p...', type=int)
@click.option('--limit', 'limit', help='The maximum number of items to return per page. - If not provided, the response will return **all**...', type=int)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def action_invalidate_list_2(company_id, limit, offset, output, search, size):
    """Invalidated urls List"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/invalidate/{size}/"
    headers = get_auth_headers()
    params = {
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

@action_group.command(name='invalidate-create-2')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.argument('size', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def action_invalidate_create_2(company_id, size, json_body):
    """Create Invalidate Urls"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/invalidate/{size}/"
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

@action_group.command(name='tag-invalidate-list-2')
@click.argument('size', type=str)
@click.option('--search', 'search', help='A search term....', type=str)
@click.option('--output', 'output', help='Set to **\'std\'** to use standard pagination format....', type=str)
@click.option('--offset', 'offset', help='The number of items to **skip** before returning results. - Requires `limit` to be set. - Used for p...', type=int)
@click.option('--limit', 'limit', help='The maximum number of items to return per page. - If not provided, the response will return **all**...', type=int)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def action_tag_invalidate_list_2(company_id, limit, offset, output, search, size):
    """Invalidated tags List"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/tag_invalidate/{size}/"
    headers = get_auth_headers()
    params = {
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

@action_group.command(name='tag-invalidate-create-2')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.argument('size', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def action_tag_invalidate_create_2(company_id, size, json_body):
    """Create Invalidate Tags"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/companies/{company_id}/tag_invalidate/{size}/"
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

