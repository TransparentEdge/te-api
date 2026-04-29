import click
import requests
import json
from te_api.auth import get_auth_headers
from te_api.config import Config

@click.group()
def cli():
    """Autoprovisioning operations."""
    pass

@cli.group(name='get')
def get_group():
    """Get operations."""
    pass

@get_group.command(name='api-protection-rules')
@click.option('--search', 'search', help='A search term. (only used when listing)', type=str)
@click.option('--offset', 'offset', help='The number of items to **skip** before returning results. - Requires `limit` to be set. - Used for pagination to retrieve the next set of results. - Example: `offset=10` skips the first 10 items. (only used when listing)', type=int)
@click.option('--limit', 'limit', help='The maximum number of items to return per page. - If not provided, the response will return **all** items. - If provided, the response will be **paginated**. - Use in combination with `offset` for pagination. (only used when listing)', type=int)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
@click.argument('site_id', required=False, type=str, default=None)
def get_api_protection_rules(company_id, limit, offset, search, site_id):
    """Protection rule List (omit ID) / Protection rule Details (with ID)"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    if site_id is not None:
        url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/api-protection-rules/{site_id}/"
        params = {}
    else:
        url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/api-protection-rules/"
        params = {
            'limit': limit,
            'offset': offset,
            'search': search,
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

@get_group.command(name='backendproblem')
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
@click.argument('backendproblem_id', required=False, type=str, default=None)
def get_backendproblem(company_id, backendproblem_id):
    """Backend errors List (omit ID) / Backend error Details (with ID)"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    if backendproblem_id is not None:
        url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/backendproblem/{backendproblem_id}/"
        params = {}
    else:
        url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/backendproblem/"
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

@get_group.command(name='backends')
@click.option('--ordering', 'ordering', help='Which field to use when ordering the results. (only used when listing)', type=str)
@click.option('--offset', 'offset', help='The number of items to **skip** before returning results. - Requires `limit` to be set. - Used for pagination to retrieve the next set of results. - Example: `offset=10` skips the first 10 items. (only used when listing)', type=int)
@click.option('--limit', 'limit', help='The maximum number of items to return per page. - If not provided, the response will return **all** items. - If provided, the response will be **paginated**. - Use in combination with `offset` for pagination. (only used when listing)', type=int)
@click.option('--format', 'format', help=' (only used when listing)', type=click.Choice(['json', 'txt']))
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
@click.argument('backend_id', required=False, type=str, default=None)
def get_backends(company_id, format, limit, offset, ordering, backend_id):
    """Backend configurations List (omit ID) / Backend Details (with ID)"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    if backend_id is not None:
        url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/backends/{backend_id}/"
        params = {}
    else:
        url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/backends/"
        params = {
            'format': format,
            'limit': limit,
            'offset': offset,
            'ordering': ordering,
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

@get_group.command(name='blockedlist')
@click.option('--kind', 'kind', help='List type', type=click.Choice(['blacklist', 'captcha', 'jschallenge']))
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
def get_blockedlist(company_id, kind):
    """Blocked address List"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/blockedlist/"
    headers = get_auth_headers()
    params = {
        'kind': kind,
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

@get_group.command(name='config')
@click.option('--search', 'search', help='A search term. (only used when listing)', type=str)
@click.option('--offset', 'offset', help='The number of items to **skip** before returning results. - Requires `limit` to be set. - Used for pagination to retrieve the next set of results. - Example: `offset=10` skips the first 10 items. (only used when listing)', type=int)
@click.option('--limit', 'limit', help='The maximum number of items to return per page. - If not provided, the response will return **all** items. - If provided, the response will be **paginated**. - Use in combination with `offset` for pagination. (only used when listing)', type=int)
@click.option('--deployed', 'deployed', help='Get Deployed Settings (only used when listing)', is_flag=True)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
@click.option('--active', 'active', help='Get Active Settings (only used when listing)', is_flag=True)
@click.argument('config_id', required=False, type=str, default=None)
def get_config(active, company_id, deployed, limit, offset, search, config_id):
    """Autoprovisioning configuration List (omit ID) / Autoprovisioning configuration Details (with ID)"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    if config_id is not None:
        url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/config/{config_id}/"
        params = {}
    else:
        url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/config/"
        params = {
            'active': active,
            'deployed': deployed,
            'limit': limit,
            'offset': offset,
            'search': search,
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

@get_group.command(name='customconfig')
@click.option('--search', 'search', help='A search term. (only used when listing)', type=str)
@click.option('--offset', 'offset', help='The number of items to **skip** before returning results. - Requires `limit` to be set. - Used for pagination to retrieve the next set of results. - Example: `offset=10` skips the first 10 items. (only used when listing)', type=int)
@click.option('--limit', 'limit', help='The maximum number of items to return per page. - If not provided, the response will return **all** items. - If provided, the response will be **paginated**. - Use in combination with `offset` for pagination. (only used when listing)', type=int)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
@click.argument('custom_config_id', required=False, type=str, default=None)
def get_customconfig(company_id, limit, offset, search, custom_config_id):
    """Custom autoprovisioning List (omit ID) / Custom autoprovisioning Detail (with ID)"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    if custom_config_id is not None:
        url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/customconfig/{custom_config_id}/"
        params = {}
    else:
        url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/customconfig/"
        params = {
            'limit': limit,
            'offset': offset,
            'search': search,
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

@get_group.command(name='dnscertrequest')
@click.option('--search', 'search', help='A search term. (only used when listing)', type=str)
@click.option('--offset', 'offset', help='The number of items to **skip** before returning results. - Requires `limit` to be set. - Used for pagination to retrieve the next set of results. - Example: `offset=10` skips the first 10 items. (only used when listing)', type=int)
@click.option('--limit', 'limit', help='The maximum number of items to return per page. - If not provided, the response will return **all** items. - If provided, the response will be **paginated**. - Use in combination with `offset` for pagination. (only used when listing)', type=int)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
@click.argument('dns_cert_request_id', required=False, type=str, default=None)
def get_dnscertrequest(company_id, limit, offset, search, dns_cert_request_id):
    """DNS cert requests List (omit ID) / DNS cert request Details (with ID)"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    if dns_cert_request_id is not None:
        url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/dnscertrequest/{dns_cert_request_id}/"
        params = {}
    else:
        url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/dnscertrequest/"
        params = {
            'limit': limit,
            'offset': offset,
            'search': search,
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

@get_group.command(name='dnscredential')
@click.option('--search', 'search', help='A search term. (only used when listing)', type=str)
@click.option('--offset', 'offset', help='The number of items to **skip** before returning results. - Requires `limit` to be set. - Used for pagination to retrieve the next set of results. - Example: `offset=10` skips the first 10 items. (only used when listing)', type=int)
@click.option('--limit', 'limit', help='The maximum number of items to return per page. - If not provided, the response will return **all** items. - If provided, the response will be **paginated**. - Use in combination with `offset` for pagination. (only used when listing)', type=int)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
@click.argument('dns_credential_id', required=False, type=str, default=None)
def get_dnscredential(company_id, limit, offset, search, dns_credential_id):
    """DNS Credentials List (omit ID) / DNS Credential Details (with ID)"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    if dns_credential_id is not None:
        url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/dnscredential/{dns_credential_id}/"
        params = {}
    else:
        url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/dnscredential/"
        params = {
            'limit': limit,
            'offset': offset,
            'search': search,
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

@get_group.command(name='domain')
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
@click.argument('domain_id', required=False, type=str, default=None)
def get_domain(company_id, domain_id):
    """Domains List (omit ID) / Domain Details (with ID)"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    if domain_id is not None:
        url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/domain/{domain_id}/"
        params = {}
    else:
        url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/domain/"
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

@get_group.command(name='domain-record')
@click.option('--search', 'search', help='A search term. (only used when listing)', type=str)
@click.option('--offset', 'offset', help='The number of items to **skip** before returning results. - Requires `limit` to be set. - Used for pagination to retrieve the next set of results. - Example: `offset=10` skips the first 10 items. (only used when listing)', type=int)
@click.option('--limit', 'limit', help='The maximum number of items to return per page. - If not provided, the response will return **all** items. - If provided, the response will be **paginated**. - Use in combination with `offset` for pagination. (only used when listing)', type=int)
@click.argument('domain_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
@click.argument('record_id', required=False, type=str, default=None)
def get_domain_record(company_id, domain_id, limit, offset, search, record_id):
    """Record List (omit ID) / Record Details (with ID)"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    if record_id is not None:
        url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/domain/{domain_id}/record/{record_id}/"
        params = {}
    else:
        url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/domain/{domain_id}/record/"
        params = {
            'limit': limit,
            'offset': offset,
            'search': search,
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

@get_group.command(name='generate-vcl')
@click.option('--site', 'site', help='Optional site ID to filter rules for a specific site', type=int)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
def get_generate_vcl(company_id, site):
    """Generate VCL configuration"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/generate-vcl/"
    headers = get_auth_headers()
    params = {
        'site': site,
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

@get_group.command(name='rules')
@click.option('--search', 'search', help='A search term. (only used when listing)', type=str)
@click.option('--offset', 'offset', help='The number of items to **skip** before returning results. - Requires `limit` to be set. - Used for pagination to retrieve the next set of results. - Example: `offset=10` skips the first 10 items. (only used when listing)', type=int)
@click.option('--limit', 'limit', help='The maximum number of items to return per page. - If not provided, the response will return **all** items. - If provided, the response will be **paginated**. - Use in combination with `offset` for pagination. (only used when listing)', type=int)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
@click.argument('rule_id', required=False, type=str, default=None)
def get_rules(company_id, limit, offset, search, rule_id):
    """Rules List (omit ID) / Rule Details (with ID)"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    if rule_id is not None:
        url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/rules/{rule_id}/"
        params = {}
    else:
        url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/rules/"
        params = {
            'limit': limit,
            'offset': offset,
            'search': search,
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

@get_group.command(name='rules-count')
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
def get_rules_count(company_id):
    """Rule Count per Site"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/rules/count/"
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

@get_group.command(name='rules-reorder-update')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.option('--site', 'site', help='Filter rules by site ID', type=int)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
def get_rules_reorder_update(company_id, site, json_body):
    """Reorder Rules"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/rules/reorder/"
    headers = get_auth_headers()
    params = {
        'site': site,
    }
    params = {k: v for k, v in params.items() if v is not None}
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

@get_group.command(name='sslcertificaterequest')
@click.option('--search', 'search', help='A search term. (only used when listing)', type=str)
@click.option('--offset', 'offset', help='The number of items to **skip** before returning results. - Requires `limit` to be set. - Used for pagination to retrieve the next set of results. - Example: `offset=10` skips the first 10 items. (only used when listing)', type=int)
@click.option('--limit', 'limit', help='The maximum number of items to return per page. - If not provided, the response will return **all** items. - If provided, the response will be **paginated**. - Use in combination with `offset` for pagination. (only used when listing)', type=int)
@click.option('--filters', 'filters', help='Filters. JSON object with keys:   orphan(boolean)   error(boolean)   cn(string) (only used when listing)', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
@click.argument('request_id', required=False, type=str, default=None)
def get_sslcertificaterequest(company_id, filters, limit, offset, search, request_id):
    """SSL certificate List (omit ID) / SSL certificate Details (with ID)"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    if request_id is not None:
        url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/sslcertificaterequest/{request_id}/"
        params = {}
    else:
        url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/sslcertificaterequest/"
        params = {
            'filters': filters,
            'limit': limit,
            'offset': offset,
            'search': search,
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

@get_group.command(name='sslconfig')
@click.option('--search', 'search', help='A search term. (only used when listing)', type=str)
@click.option('--offset', 'offset', help='The number of items to **skip** before returning results. - Requires `limit` to be set. - Used for pagination to retrieve the next set of results. - Example: `offset=10` skips the first 10 items. (only used when listing)', type=int)
@click.option('--limit', 'limit', help='The maximum number of items to return per page. - If not provided, the response will return **all** items. - If provided, the response will be **paginated**. - Use in combination with `offset` for pagination. (only used when listing)', type=int)
@click.option('--filters', 'filters', help='Filters. JSON object with keys:   autogenerated(boolean)   dns_challenge(boolean) (only used when listing)', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
@click.argument('ssl_id', required=False, type=str, default=None)
def get_sslconfig(company_id, filters, limit, offset, search, ssl_id):
    """SSL Configuration List (omit ID) / SSL configuration Details (with ID)"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    if ssl_id is not None:
        url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/sslconfig/{ssl_id}/"
        params = {}
    else:
        url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/sslconfig/"
        params = {
            'filters': filters,
            'limit': limit,
            'offset': offset,
            'search': search,
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

@get_group.command(name='uam')
@click.option('--company-id', 'company_id', required=False, type=int, help='ID of the company to get attack modes for (Default: from context)')
@click.argument('site_id', required=False, type=str, default=None)
def get_uam(company_id, site_id):
    """Under Attack mode List (omit ID) / Under Attack mode Details (with ID)"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    if site_id is not None:
        url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/uam/{site_id}/"
        params = {}
    else:
        url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/uam/"
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

@get_group.command(name='uam-create')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.argument('site_id', type=int)
@click.option('--company-id', 'company_id', required=False, type=int, help='ID of the company that owns the site (Default: from context)')
def get_uam_create(company_id, site_id, json_body):
    """Activate Under Attack mode"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/uam/{site_id}/"
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

@get_group.command(name='dnshookkeyvalue')
@click.argument('dns_hook_name_id', type=str)
@click.argument('dns_hook_key_value_id', required=False, type=str, default=None)
def get_dnshookkeyvalue(dns_hook_name_id, dns_hook_key_value_id):
    """DNS Key Values List (omit ID) / DNS Key Value Details (with ID)"""
    if dns_hook_key_value_id is not None:
        url = f"{Config.API_URL}/v1/autoprovisioning/{dns_hook_name_id}/dnshookkeyvalue/{dns_hook_key_value_id}"
        params = {}
    else:
        url = f"{Config.API_URL}/v1/autoprovisioning/{dns_hook_name_id}/dnshookkeyvalue/"
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

@get_group.command(name='action-templates')
@click.option('--search', 'search', help='A search term.', type=str)
@click.option('--offset', 'offset', help='The number of items to **skip** before returning results. - Requires `limit` to be set. - Used for pagination to retrieve the next set of results. - Example: `offset=10` skips the first 10 items.', type=int)
@click.option('--limit', 'limit', help='The maximum number of items to return per page. - If not provided, the response will return **all** items. - If provided, the response will be **paginated**. - Use in combination with `offset` for pagination.', type=int)
def get_action_templates(limit, offset, search):
    """Action Templates List"""
    url = f"{Config.API_URL}/v1/autoprovisioning/action_templates/"
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

@get_group.command(name='actions-context-retrieve')
def get_actions_context_retrieve():
    """Action Contexts List"""
    url = f"{Config.API_URL}/v1/autoprovisioning/actions/context/"
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

@get_group.command(name='conditions-logic-operators-retrieve')
def get_conditions_logic_operators_retrieve():
    """Logic Operators List"""
    url = f"{Config.API_URL}/v1/autoprovisioning/conditions/logic_operators/"
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

@get_group.command(name='conditions-operators-retrieve')
def get_conditions_operators_retrieve():
    """Functional Operators List"""
    url = f"{Config.API_URL}/v1/autoprovisioning/conditions/operators/"
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

@get_group.command(name='dnscertificateauthority')
@click.option('--search', 'search', help='A search term.', type=str)
@click.option('--offset', 'offset', help='The number of items to **skip** before returning results. - Requires `limit` to be set. - Used for pagination to retrieve the next set of results. - Example: `offset=10` skips the first 10 items.', type=int)
@click.option('--limit', 'limit', help='The maximum number of items to return per page. - If not provided, the response will return **all** items. - If provided, the response will be **paginated**. - Use in combination with `offset` for pagination.', type=int)
def get_dnscertificateauthority(limit, offset, search):
    """DNS Cert Authorities List"""
    url = f"{Config.API_URL}/v1/autoprovisioning/dnscertificateauthority/"
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

@get_group.command(name='dnshook-retrieve')
def get_dnshook_retrieve():
    """DNS Hook List"""
    url = f"{Config.API_URL}/v1/autoprovisioning/dnshook/"
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

@get_group.command(name='dnshook')
@click.argument('dns_hook_id', type=str)
def get_dnshook(dns_hook_id):
    """DNS Hook Details"""
    url = f"{Config.API_URL}/v1/autoprovisioning/dnshook/{dns_hook_id}/"
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

@get_group.command(name='dnshook-dnshookkeyname')
@click.argument('dns_hook_id', type=str)
@click.argument('dns_hook_key_name_id', required=False, type=str, default=None)
def get_dnshook_dnshookkeyname(dns_hook_id, dns_hook_key_name_id):
    """DNS Key Name List (omit ID) / DNS Key Name Details (with ID)"""
    if dns_hook_key_name_id is not None:
        url = f"{Config.API_URL}/v1/autoprovisioning/dnshook/{dns_hook_id}/dnshookkeyname/{dns_hook_key_name_id}/"
        params = {}
    else:
        url = f"{Config.API_URL}/v1/autoprovisioning/dnshook/{dns_hook_id}/dnshookkeyname/"
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

@get_group.command(name='parameters-types-retrieve')
def get_parameters_types_retrieve():
    """Parameter Types List"""
    url = f"{Config.API_URL}/v1/autoprovisioning/parameters/types/"
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

@get_group.command(name='properties')
@click.option('--search', 'search', help='A search term.', type=str)
@click.option('--offset', 'offset', help='The number of items to **skip** before returning results. - Requires `limit` to be set. - Used for pagination to retrieve the next set of results. - Example: `offset=10` skips the first 10 items.', type=int)
@click.option('--limit', 'limit', help='The maximum number of items to return per page. - If not provided, the response will return **all** items. - If provided, the response will be **paginated**. - Use in combination with `offset` for pagination.', type=int)
def get_properties(limit, offset, search):
    """Condition Templates List"""
    url = f"{Config.API_URL}/v1/autoprovisioning/properties/"
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

@get_group.command(name='staging-generate-vcl')
@click.option('--site', 'site', help='Optional site ID to filter rules for a specific site', type=int)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
def get_staging_generate_vcl(company_id, site):
    """Generate VCL configuration"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/staging/{company_id}/generate-vcl/"
    headers = get_auth_headers()
    params = {
        'site': site,
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

@get_group.command(name='staging-rules')
@click.option('--search', 'search', help='A search term. (only used when listing)', type=str)
@click.option('--offset', 'offset', help='The number of items to **skip** before returning results. - Requires `limit` to be set. - Used for pagination to retrieve the next set of results. - Example: `offset=10` skips the first 10 items. (only used when listing)', type=int)
@click.option('--limit', 'limit', help='The maximum number of items to return per page. - If not provided, the response will return **all** items. - If provided, the response will be **paginated**. - Use in combination with `offset` for pagination. (only used when listing)', type=int)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
@click.argument('rule_id', required=False, type=str, default=None)
def get_staging_rules(company_id, limit, offset, search, rule_id):
    """Rules List (omit ID) / Rule Details (with ID)"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    if rule_id is not None:
        url = f"{Config.API_URL}/v1/staging/{company_id}/rules/{rule_id}/"
        params = {}
    else:
        url = f"{Config.API_URL}/v1/staging/{company_id}/rules/"
        params = {
            'limit': limit,
            'offset': offset,
            'search': search,
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

@get_group.command(name='staging-rules-count')
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
def get_staging_rules_count(company_id):
    """Rule Count per Site"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/staging/{company_id}/rules/count/"
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

@get_group.command(name='staging-rules-reorder-update')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.option('--site', 'site', help='Filter rules by site ID', type=int)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
def get_staging_rules_reorder_update(company_id, site, json_body):
    """Reorder Rules"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/staging/{company_id}/rules/reorder/"
    headers = get_auth_headers()
    params = {
        'site': site,
    }
    params = {k: v for k, v in params.items() if v is not None}
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

@create_group.command(name='api-protection-rules')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
def create_api_protection_rules(company_id, json_body):
    """Create Protection rule"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/api-protection-rules/"
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

@create_group.command(name='backendproblem')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
def create_backendproblem(company_id, json_body):
    """Create Backend error"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/backendproblem/"
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

@create_group.command(name='backends')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.option('--format', 'format', help='', type=click.Choice(['json', 'txt']))
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
def create_backends(company_id, format, json_body):
    """Create Backend configuration"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/backends/"
    headers = get_auth_headers()
    params = {
        'format': format,
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

@create_group.command(name='backendtest-check')
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
def create_backendtest_check(company_id):
    """Backend test health check"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/backendtest/check/"
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

@create_group.command(name='blockedlist')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
def create_blockedlist(company_id, json_body):
    """Block Address"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/blockedlist/"
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

@create_group.command(name='config')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
def create_config(company_id, json_body):
    """Create Autoprovisioning configuration"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/config/"
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

@create_group.command(name='dnscertrequest')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
def create_dnscertrequest(company_id, json_body):
    """Create DNS cert request"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/dnscertrequest/"
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

@create_group.command(name='dnscredential')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
def create_dnscredential(company_id, json_body):
    """Create DNS Credential"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/dnscredential/"
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

@create_group.command(name='domain')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
def create_domain(company_id, json_body):
    """Create Domain"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/domain/"
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

@create_group.command(name='domain-record')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.argument('domain_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
def create_domain_record(company_id, domain_id, json_body):
    """Create Record"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/domain/{domain_id}/record/"
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

@create_group.command(name='rules')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
def create_rules(company_id, json_body):
    """Create Rule"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/rules/"
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

@create_group.command(name='sslcertificaterequest')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
def create_sslcertificaterequest(company_id, json_body):
    """Create SSL certificate"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/sslcertificaterequest/"
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

@create_group.command(name='sslconfig')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
def create_sslconfig(company_id, json_body):
    """Create SSL Configuration"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/sslconfig/"
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

@create_group.command(name='vcl-recommendation')
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
def create_vcl_recommendation(company_id):
    """Generate VCL recommendation"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/vcl_recommendation/"
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

@create_group.command(name='staging-rules')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
def create_staging_rules(company_id, json_body):
    """Create Rule"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/staging/{company_id}/rules/"
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

@update_group.command(name='api-protection-rules')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.argument('site_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
def update_api_protection_rules(company_id, site_id, json_body):
    """Update Protection rule"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/api-protection-rules/{site_id}/"
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

@update_group.command(name='backends')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.option('--format', 'format', help='', type=click.Choice(['json', 'txt']))
@click.option('--company-id', 'company_id', required=False, type=int, help='ID of the company that owns the backend (Default: from context)')
@click.argument('backend_id', type=int)
def update_backends(backend_id, company_id, format, json_body):
    """Update Backend"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/backends/{backend_id}/"
    headers = get_auth_headers()
    params = {
        'format': format,
    }
    params = {k: v for k, v in params.items() if v is not None}
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

@update_group.command(name='dnscertrequest')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.argument('dns_cert_request_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
def update_dnscertrequest(company_id, dns_cert_request_id, json_body):
    """Update DNS cert request"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/dnscertrequest/{dns_cert_request_id}/"
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

@update_group.command(name='dnscredential')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.argument('dns_credential_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
def update_dnscredential(company_id, dns_credential_id, json_body):
    """Update DNS credential"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/dnscredential/{dns_credential_id}/"
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

@update_group.command(name='domain-record')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.argument('record_id', type=str)
@click.argument('domain_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
def update_domain_record(company_id, domain_id, record_id, json_body):
    """Edit Record"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/domain/{domain_id}/record/{record_id}/"
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

@update_group.command(name='rules')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.argument('rule_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
def update_rules(company_id, rule_id, json_body):
    """Edit Rule"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/rules/{rule_id}/"
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

@update_group.command(name='sslconfig')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.argument('ssl_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
def update_sslconfig(company_id, ssl_id, json_body):
    """Edit SSL configuration"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/sslconfig/{ssl_id}/"
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

@update_group.command(name='staging-rules')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.argument('rule_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
def update_staging_rules(company_id, rule_id, json_body):
    """Edit Rule"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/staging/{company_id}/rules/{rule_id}/"
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

@delete_group.command(name='api-protection-rules')
@click.argument('site_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
def delete_api_protection_rules(company_id, site_id):
    """Delete Protection rule"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/api-protection-rules/{site_id}/"
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

@delete_group.command(name='backends')
@click.option('--format', 'format', help='', type=click.Choice(['json', 'txt']))
@click.option('--company-id', 'company_id', required=False, type=int, help='ID of the company that owns the backend (Default: from context)')
@click.argument('backend_id', type=int)
def delete_backends(backend_id, company_id, format):
    """Delete Backend"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/backends/{backend_id}/"
    headers = get_auth_headers()
    params = {
        'format': format,
    }
    params = {k: v for k, v in params.items() if v is not None}
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

@delete_group.command(name='blockedlist')
@click.argument('kind', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
@click.argument('address', type=str)
def delete_blockedlist(address, company_id, kind):
    """Unblock Address"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/blockedlist/{kind}/{address}"
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

@delete_group.command(name='dnscertrequest')
@click.argument('dns_cert_request_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
def delete_dnscertrequest(company_id, dns_cert_request_id):
    """Delete DNS cert request"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/dnscertrequest/{dns_cert_request_id}/"
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

@delete_group.command(name='dnscredential')
@click.argument('dns_credential_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
def delete_dnscredential(company_id, dns_credential_id):
    """Delete DNS credential"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/dnscredential/{dns_credential_id}/"
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

@delete_group.command(name='domain')
@click.argument('domain_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
def delete_domain(company_id, domain_id):
    """Delete Domain"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/domain/{domain_id}/"
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

@delete_group.command(name='domain-record')
@click.argument('record_id', type=str)
@click.argument('domain_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
def delete_domain_record(company_id, domain_id, record_id):
    """Delete Record"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/domain/{domain_id}/record/{record_id}/"
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

@delete_group.command(name='rules')
@click.argument('rule_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
def delete_rules(company_id, rule_id):
    """Delete Rule"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/rules/{rule_id}/"
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

@delete_group.command(name='sslconfig')
@click.argument('ssl_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
def delete_sslconfig(company_id, ssl_id):
    """Delete SSL Configuration"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/sslconfig/{ssl_id}/"
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

@delete_group.command(name='uam')
@click.argument('site_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
def delete_uam(company_id, site_id):
    """Deactivate Under Attack mode"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/autoprovisioning/{company_id}/uam/{site_id}/"
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

@delete_group.command(name='staging-rules')
@click.argument('rule_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
def delete_staging_rules(company_id, rule_id):
    """Delete Rule"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/staging/{company_id}/rules/{rule_id}/"
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

