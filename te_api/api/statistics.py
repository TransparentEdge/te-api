import click
import requests
import json
from te_api.auth import get_auth_headers
from te_api.config import Config

@click.group()
def cli():
    """Statistics operations."""
    pass

@cli.group(name='get')
def get_group():
    """Get operations."""
    pass

@get_group.command(name='anomalies')
@click.option('--search', 'search', help='A search term....', type=str)
@click.option('--offset', 'offset', help='The initial index from which to return the results....', type=int)
@click.option('--limit', 'limit', help='Number of results to return per page....', type=int)
@click.option('--filters', 'filters', help='Filters...', required=True, type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_anomalies(company_id, filters, limit, offset, search):
    """Anomalies detected List"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/statistics/{company_id}/anomalies/"
    headers = get_auth_headers()
    params = {
        'filters': filters,
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

@get_group.command(name='anomalies-pdf')
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
@click.argument('anomaly_id', type=str)
def get_anomalies_pdf(anomaly_id, company_id):
    """Anomaly detected PDF"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/statistics/{company_id}/anomalies/{anomaly_id}/pdf/"
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

@get_group.command(name='anomaliesavailable')
@click.option('--search', 'search', help='A search term....', type=str)
@click.option('--offset', 'offset', help='The number of items to **skip** before returning results. - Requires `limit` to be set. - Used for p...', type=int)
@click.option('--limit', 'limit', help='The maximum number of items to return per page. - If not provided, the response will return **all**...', type=int)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_anomaliesavailable(company_id, limit, offset, search):
    """Anomalies available List"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/statistics/{company_id}/anomaliesavailable/"
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

@get_group.command(name='anomalypreferences')
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_anomalypreferences(company_id):
    """Anomaly preferences List"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/statistics/{company_id}/anomalypreferences/"
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

@get_group.command(name='anomalyreaction-retrieve')
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_anomalyreaction_retrieve(company_id):
    """Anomaly reactions List"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/statistics/{company_id}/anomalyreaction/"
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

@get_group.command(name='reaction-instance')
@click.argument('reaction_type', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_reaction_instance(company_id, reaction_type):
    """Anomaly reaction Details"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/statistics/{company_id}/anomalyreaction/{reaction_type}/"
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

@get_group.command(name='anomalythreshold')
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_anomalythreshold(company_id):
    """Anomaly thresholds List"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/statistics/{company_id}/anomalythreshold/"
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

@get_group.command(name='bot-mitigation')
@click.argument('temporality', type=str)
@click.argument('request_type', type=str)
@click.option('--filters', 'filters', help='Filters...', required=True, type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_bot_mitigation(company_id, filters, request_type, temporality):
    """Bot Mitigation statistics"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v2/statistics/{company_id}/bot_mitigation/{temporality}/{request_type}/"
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

@get_group.command(name='ddos')
@click.argument('temporality', type=str)
@click.argument('request_type', type=str)
@click.option('--filters', 'filters', help='Filters...', required=True, type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_ddos(company_id, filters, request_type, temporality):
    """DDoS statistics"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/statistics/{company_id}/ddos/{temporality}/{request_type}/"
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

@get_group.command(name='delivery')
@click.argument('temporality', type=str)
@click.argument('request_type', type=str)
@click.option('--key-field', 'key_field', help='Change the key field data for `table` type....', type=str)
@click.option('--filters', 'filters', help='Filters...', required=True, type=str)
@click.option('--company-id', 'company_id', required=False, type=int, help='ID of the company to get delivery statistics for... (Default: from context)')
def get_delivery(company_id, filters, key_field, request_type, temporality):
    """Delivery statistics"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v2/statistics/{company_id}/delivery/{temporality}/{request_type}/"
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

@get_group.command(name='dns')
@click.argument('temporality', type=str)
@click.argument('request_type', type=str)
@click.option('--key-field', 'key_field', help='Change the key field data for `table` type...', type=str)
@click.option('--filters', 'filters', help='Filters...', required=True, type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_dns(company_id, filters, key_field, request_type, temporality):
    """DNS statistics"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/statistics/{company_id}/dns/{temporality}/{request_type}/"
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

@get_group.command(name='domains-historic')
@click.argument('request_type', type=str)
@click.option('--filters', 'filters', help='Filters...', required=True, type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_domains_historic(company_id, filters, request_type):
    """Domain statistics (Old)"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/statistics/{company_id}/domains/historic/{request_type}/"
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

@get_group.command(name='i3')
@click.argument('temporality', type=str)
@click.argument('request_type', type=str)
@click.option('--filters', 'filters', help='Filters...', required=True, type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_i3(company_id, filters, request_type, temporality):
    """I3 statistics"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v2/statistics/{company_id}/i3/{temporality}/{request_type}/"
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

@get_group.command(name='ip')
@click.argument('ip', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_ip(company_id, ip):
    """IP information"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/statistics/{company_id}/ip/{ip}"
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

@get_group.command(name='ip-score')
@click.argument('ip', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_ip_score(company_id, ip):
    """IP score Details"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/statistics/{company_id}/ip_score/{ip}"
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

@get_group.command(name='service-config')
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_service_config(company_id):
    """Service Config"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/statistics/{company_id}/service_config/"
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

@get_group.command(name='storage')
@click.argument('temporality', type=str)
@click.argument('request_type', type=str)
@click.option('--filters', 'filters', help='Filters...', required=True, type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_storage(company_id, filters, request_type, temporality):
    """Storage statistics (Old)"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/statistics/{company_id}/storage/{temporality}/{request_type}/"
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

@get_group.command(name='waf')
@click.argument('temporality', type=str)
@click.argument('request_type', type=str)
@click.option('--filters', 'filters', help='Filters...', required=True, type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_waf(company_id, filters, request_type, temporality):
    """WAF statistics"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v2/statistics/{company_id}/waf/{temporality}/{request_type}/"
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

@get_group.command(name='waf-header-info')
@click.argument('waf_header_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_waf_header_info(company_id, waf_header_id):
    """WAF header Details"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/statistics/{company_id}/waf/header_info/{waf_header_id}/"
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

@get_group.command(name='consumption')
@click.option('--filters', 'filters', help='Filters...', required=True, type=str)
def get_consumption(filters):
    """Historic Consumption"""
    url = f"{Config.API_URL}/v1/statistics/consumption/"
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

@get_group.command(name='metrics-prometheus')
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_metrics_prometheus(company_id):
    """Prometheus Metrics"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/statistics/metrics/{company_id}/prometheus/"
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

@get_group.command(name='backend-delivery-analytic')
@click.argument('request_type', type=str)
@click.option('--filters', 'filters', help='Filters...', required=True, type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_backend_delivery_analytic(company_id, filters, request_type):
    """Backend delivery statistics"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v2/statistics/{company_id}/backend_delivery/analytic/{request_type}/"
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

@get_group.command(name='ip-info')
@click.argument('temporality', type=str)
@click.argument('request_type', type=str)
@click.option('--filters', 'filters', help='Filters...', required=True, type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def get_ip_info(company_id, filters, request_type, temporality):
    """IP info statistics"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v2/statistics/{company_id}/ip_info/{temporality}/{request_type}/"
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

@update_group.command(name='anomalypreferences')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def update_anomalypreferences(company_id, json_body):
    """Create/update anomaly preferences"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/statistics/{company_id}/anomalypreferences/"
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

@update_group.command(name='anomalythreshold')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.argument('threshold_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def update_anomalythreshold(company_id, threshold_id, json_body):
    """Update Anomaly threshold"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/statistics/{company_id}/anomalythreshold/{threshold_id}/"
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

@update_group.command(name='anomalythreshold-partial')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.argument('threshold_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def update_anomalythreshold_partial(company_id, threshold_id, json_body):
    """Update partially Anomaly threshold"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/statistics/{company_id}/anomalythreshold/{threshold_id}/"
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

@cli.group(name='delete')
def delete_group():
    """Delete operations."""
    pass

@delete_group.command(name='anomalypreferences')
@click.argument('site_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def delete_anomalypreferences(company_id, site_id):
    """Delete anomaly preferences for a site"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/statistics/{company_id}/anomalypreferences/{site_id}/"
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

@delete_group.command(name='anomalythreshold')
@click.argument('threshold_id', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def delete_anomalythreshold(company_id, threshold_id):
    """Delete Anomaly threshold"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/statistics/{company_id}/anomalythreshold/{threshold_id}/"
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

@create_group.command(name='anomalythreshold')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def create_anomalythreshold(company_id, json_body):
    """Create Anomaly threshold"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/statistics/{company_id}/anomalythreshold/"
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

@create_group.command(name='waf-false-positives')
@click.option('--json-body', 'json_body', help='JSON string for request body')
@click.option('--company-id', 'company_id', required=False, type=str, help='... (Default: from context)')
def create_waf_false_positives(company_id, json_body):
    """WAF False Positive Analysis"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    url = f"{Config.API_URL}/v1/statistics/{company_id}/waf/false-positives/"
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

