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
@click.option('--search', 'search', help='A search term. (only used when listing)', type=str)
@click.option('--offset', 'offset', help='The initial index from which to return the results. (only used when listing)', type=int)
@click.option('--limit', 'limit', help='Number of results to return per page. (only used when listing)', type=int)
@click.option('--filters', 'filters', help='Parameter structure for `filters` (JSON): - `timestamp` (required): Object with fields `from` and `to` (both integers, UNIX timestamps) defining the query time range. - `vhost` (required, *array of strings*): Site names. - `sites` (optional, *array of strings*): Filter by Site IDs. **Cannot** use `sites` and `vhost` at the same time, in this case priority will be given to `sites` - `service_type` (optional, *array of strings*): Filter by service types - `anomaly_type` (optional, *array of strings*): Filter by anomaly types  **Required fields:** `timestamp`, `vhost`  **Example:** `?filters={"timestamp": {"from": 1776944395, "to": 1776945295}, "vhost": []}`. JSON object with keys:   timestamp(object [required]): {from(integer [required]), to(integer [required])}   vhost(array [required]) Zone names (array of string)   sites(array) Filter by Site IDs. **Cannot** use `sites` and `vhost` at the same time, in this case priority will be given to `sites` (array of string)   service_type(array) Filter by service types (array of string)   anomaly_type(array) Filter by anomaly types (array of string) (only used when listing)', type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
@click.argument('anomaly_id', required=False, type=str, default=None)
def get_anomalies(company_id, filters, limit, offset, search, anomaly_id):
    """Anomalies detected List (omit ID) / Anomaly detected Details (with ID)"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    if anomaly_id is not None:
        url = f"{Config.API_URL}/v1/statistics/{company_id}/anomalies/{anomaly_id}/"
        params = {}
    else:
        url = f"{Config.API_URL}/v1/statistics/{company_id}/anomalies/"
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

@get_group.command(name='anomalies-pdf')
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
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
@click.option('--search', 'search', help='A search term.', type=str)
@click.option('--offset', 'offset', help='The number of items to **skip** before returning results. - Requires `limit` to be set. - Used for pagination to retrieve the next set of results. - Example: `offset=10` skips the first 10 items.', type=int)
@click.option('--limit', 'limit', help='The maximum number of items to return per page. - If not provided, the response will return **all** items. - If provided, the response will be **paginated**. - Use in combination with `offset` for pagination.', type=int)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
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
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
@click.argument('site_id', required=False, type=str, default=None)
def get_anomalypreferences(company_id, site_id):
    """Anomaly preferences List (omit ID) / Anomaly preference Details (with ID)"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    if site_id is not None:
        url = f"{Config.API_URL}/v1/statistics/{company_id}/anomalypreferences/{site_id}/"
        params = {}
    else:
        url = f"{Config.API_URL}/v1/statistics/{company_id}/anomalypreferences/"
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

@get_group.command(name='anomalyreaction-retrieve')
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
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
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
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
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
@click.argument('threshold_id', required=False, type=str, default=None)
def get_anomalythreshold(company_id, threshold_id):
    """Anomaly thresholds List (omit ID) / Anomaly threshold Details (with ID)"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    if threshold_id is not None:
        url = f"{Config.API_URL}/v1/statistics/{company_id}/anomalythreshold/{threshold_id}/"
        params = {}
    else:
        url = f"{Config.API_URL}/v1/statistics/{company_id}/anomalythreshold/"
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

@get_group.command(name='bot-mitigation')
@click.argument('temporality', type=click.Choice(['historic', 'analytic']))
@click.argument('request_type', type=click.Choice(['table', 'histogram']))
@click.option('--filters', 'filters', help='Parameter structure for `filters` (JSON): - `timestamp` (required): Object with fields `from` and `to` (both integers, UNIX timestamps) defining the query time range. - `vhost` (required, *array of strings*): Site names. - `result_size` (optional, *integer*): Maximum number of results to return. - `action` (optional, *array of strings*): Actions - `assess-ip` (optional, *array of strings*): Client IPs - `cache` (optional, *array of strings*): Caches - `country` (optional, *array of strings*): Countries - `crawler` (optional, *array of strings*): Crawlers - `reason` (optional, *array of strings*): Reasons - `status` (optional, *array of strings*): Status codes - `url` (optional, *array of strings*): URLs - `user-agent` (optional, *array of strings*): User Agents  **Required fields:** `timestamp`, `vhost`  **Example:** `?filters={"timestamp": {"from": 1776944395, "to": 1776945295}, "vhost": []}`. JSON object with keys:   timestamp(object [required]): {from(integer [required]), to(integer [required])}   vhost(array [required]) Zone names (array of string)   result_size(integer)   action(array) Actions (array of string)   assess-ip(array) Client IPs (array of string)   cache(array) Caches (array of string)   country(array) Countries (array of string)   crawler(array) Crawlers (array of string)   reason(array) Reasons (array of string)   status(array) Status codes (array of string)   url(array) URLs (array of string)   user-agent(array) User Agents (array of string)', required=True, type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
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
@click.argument('temporality', type=click.Choice(['historic', 'analytic']))
@click.argument('request_type', type=click.Choice(['table', 'histogram']))
@click.option('--filters', 'filters', help='Parameter structure for `filters` (JSON): - `timestamp` (required): Object with fields `from` and `to` (both integers, UNIX timestamps) defining the query time range. - `vhost` (required, *array of strings*): Site names. - `result_size` (optional, *integer*): Maximum number of results to return. - `debug_reason` (optional, *array of strings*): Debug Reasons - `geoip.country.country_name` (optional, *array of strings*): Country names - `geoip.asn.organization_name` (optional, *array of strings*): ASN Organizations Names - `hostname` (optional, *array of strings*): Hostnames - `accept` (optional, *array of strings*): Accept Headers - `accept_encoding` (optional, *array of strings*): Accept Encodings - `accept_language` (optional, *array of strings*): Accept Languages - `cookie` (optional, *array of strings*): Cookies - `host` (optional, *array of strings*): Sites - `referer` (optional, *array of strings*): Referers - `client_ip` (optional, *array of strings*): Client IPs - `user_agent` (optional, *array of strings*): User Agents - `ReqMethod` (optional, *array of strings*): Methods - `ReqProtocol` (optional, *array of strings*): Protocols - `ReqURL` (optional, *array of strings*): URLs  **Required fields:** `timestamp`, `vhost`  **Example:** `?filters={"timestamp": {"from": 1776944395, "to": 1776945295}, "vhost": []}`. JSON object with keys:   timestamp(object [required]): {from(integer [required]), to(integer [required])}   vhost(array [required]) Zone names (array of string)   result_size(integer)   debug_reason(array) Debug Reasons (array of string)   geoip.country.country_name(array) Country names (array of string)   geoip.asn.organization_name(array) ASN Organizations Names (array of string)   hostname(array) Hostnames (array of string)   accept(array) Accept Headers (array of string)   accept_encoding(array) Accept Encodings (array of string)   accept_language(array) Accept Languages (array of string)   cookie(array) Cookies (array of string)   host(array) Sites (array of string)   referer(array) Referers (array of string)   client_ip(array) Client IPs (array of string)   user_agent(array) User Agents (array of string)   ReqMethod(array) Methods (array of string)   ReqProtocol(array) Protocols (array of string)   ReqURL(array) URLs (array of string)', required=True, type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
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
@click.argument('temporality', type=click.Choice(['historic', 'analytic']))
@click.argument('request_type', type=click.Choice(['table', 'histogram']))
@click.option('--key-field', 'key_field', help='Change the key field data for `table` type.', type=click.Choice(['tcdn.varnish.agent', 'tcdn.varnish.asn', 'tcdn.varnish.cached', 'tcdn.varnish.clientip', 'tcdn.varnish.countrycode', 'tcdn.varnish.method', 'tcdn.varnish.path', 'tcdn.varnish.proto', 'tcdn.varnish.referer', 'tcdn.varnish.regioncode', 'tcdn.varnish.request', 'tcdn.varnish.response', 'tcdn.varnish.response_time', 'tcdn.varnish.tcdndebugreason']))
@click.option('--filters', 'filters', help='Parameter structure for `filters` (JSON): - `timestamp` (required): Object with fields `from` and `to` (both integers, UNIX timestamps) defining the query time range. - `vhost` (required, *array of strings*): Site names. - `result_size` (optional, *integer*): Maximum number of results to return. - `tcdn.varnish.clientip` (optional, *array of strings*): Client IPs - `tcdn.varnish.agent` (optional, *array of strings*): User Agents - `tcdn.varnish.asn` (optional, *array of strings*): ASN numbers - `tcdn.varnish.cached` (optional, *array of strings*): Cached status - `tcdn.varnish.countrycode` (optional, *array of strings*): Country codes - `tcdn.varnish.method` (optional, *array of strings*): HTTP methods - `tcdn.varnish.path` (optional, *array of strings*): Paths - `tcdn.varnish.proto` (optional, *array of strings*): Protocols - `tcdn.varnish.referer` (optional, *array of strings*): Referers - `tcdn.varnish.regioncode` (optional, *array of strings*): Region codes - `tcdn.varnish.request` (optional, *array of strings*): Request paths - `tcdn.varnish.response` (optional, *array of strings*): Response codes - `tcdn.varnish.response_time` (optional, *array of strings*): Response times - `tcdn.varnish.tcdndebugreason` (optional, *array of strings*): Debug reasons  **Required fields:** `timestamp`, `vhost`  **Example:** `?filters={"timestamp": {"from": 1776944395, "to": 1776945295}, "vhost": []}`. JSON object with keys:   timestamp(object [required]): {from(integer [required]), to(integer [required])}   vhost(array [required]) Zone names (array of string)   result_size(integer)   tcdn.varnish.clientip(array) Client IPs (array of string)   tcdn.varnish.agent(array) User Agents (array of string)   tcdn.varnish.asn(array) ASN numbers (array of string)   tcdn.varnish.cached(array) Cached status (array of string)   tcdn.varnish.countrycode(array) Country codes (array of string)   tcdn.varnish.method(array) HTTP methods (array of string)   tcdn.varnish.path(array) Paths (array of string)   tcdn.varnish.proto(array) Protocols (array of string)   tcdn.varnish.referer(array) Referers (array of string)   tcdn.varnish.regioncode(array) Region codes (array of string)   tcdn.varnish.request(array) Request paths (array of string)   tcdn.varnish.response(array) Response codes (array of string)   tcdn.varnish.response_time(array) Response times (array of string)   tcdn.varnish.tcdndebugreason(array) Debug reasons (array of string)', required=True, type=str)
@click.option('--company-id', 'company_id', required=False, type=int, help='ID of the company to get delivery statistics for (Default: from context)')
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
@click.argument('temporality', type=click.Choice(['historic', 'analytic']))
@click.argument('request_type', type=click.Choice(['table', 'histogram']))
@click.option('--key-field', 'key_field', help='Change the key field data for `table` type', type=click.Choice(['client.asn', 'client.geo.country', 'client.geo.region', 'client.ip', 'client.organization', 'record.name', 'record.type']))
@click.option('--filters', 'filters', help='Parameter structure for `filters` (JSON): - `timestamp` (required): Object with fields `from` and `to` (both integers, UNIX timestamps) defining the query time range. - `vhost` (required, *array of strings*): Site names. - `result_size` (optional, *integer*): Maximum number of results to return. - `client.ip` (optional, *array of strings*): IPs - `client.asn` (optional, *array of strings*): ASN numbers - `client.geo.country` (optional, *array of strings*): Country zones - `client.geo.region` (optional, *array of strings*): Region names - `client.organization` (optional, *array of strings*): Organization names - `client.record.name` (optional, *array of strings*): Record names - `client.record.type` (optional, *array of strings*): Record types  **Required fields:** `timestamp`, `vhost`  **Example:** `?filters={"timestamp": {"from": 1776944395, "to": 1776945295}, "vhost": []}`. JSON object with keys:   timestamp(object [required]): {from(integer [required]), to(integer [required])}   vhost(array [required]) Zone names (array of string)   result_size(integer)   client.ip(array) IPs (array of string)   client.asn(array) ASN numbers (array of string)   client.geo.country(array) Country zones (array of string)   client.geo.region(array) Region names (array of string)   client.organization(array) Organization names (array of string)   client.record.name(array) Record names (array of string)   client.record.type(array) Record types (array of string)', required=True, type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
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
@click.argument('request_type', type=click.Choice(['table', 'histogram']))
@click.option('--filters', 'filters', help='Parameter structure for `filters` (JSON): - `timestamp` (required): Object with fields `from` and `to` (both integers, UNIX timestamps) defining the query time range. - `vhost` (required, *array of strings*): Site names.  **Required fields:** `timestamp`, `vhost`  **Example:** `?filters={"timestamp": {"from": 1776944395, "to": 1776945295}, "vhost": []}`. JSON object with keys:   timestamp(object [required]): {from(integer [required]), to(integer [required])}   vhost(array [required]) Zone names (array of string)', required=True, type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
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
@click.argument('temporality', type=click.Choice(['historic', 'analytic']))
@click.argument('request_type', type=click.Choice(['table', 'histogram']))
@click.option('--filters', 'filters', help='Parameter structure for `filters` (JSON): - `timestamp` (required): Object with fields `from` and `to` (both integers, UNIX timestamps) defining the query time range. - `vhost` (required, *array of strings*): Site names.  **Required fields:** `timestamp`, `vhost`  **Example:** `?filters={"timestamp": {"from": 1776944395, "to": 1776945295}, "vhost": []}`. JSON object with keys:   timestamp(object [required]): {from(integer [required]), to(integer [required])}   vhost(array [required]) Zone names (array of string)', required=True, type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
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
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
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
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
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
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
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
@click.argument('temporality', type=click.Choice(['historic', 'analytic']))
@click.argument('request_type', type=click.Choice(['table', 'histogram']))
@click.option('--filters', 'filters', help='Parameter structure for `filters` (JSON): - `timestamp` (required): Object with fields `from` and `to` (both integers, UNIX timestamps) defining the query time range. - `vhost` (required, *array of strings*): Site names.  **Required fields:** `timestamp`, `vhost`  **Example:** `?filters={"timestamp": {"from": 1776944395, "to": 1776945295}, "vhost": []}`. JSON object with keys:   timestamp(object [required]): {from(integer [required]), to(integer [required])}   vhost(array [required]) Zone names (array of string)', required=True, type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
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
@click.argument('temporality', type=click.Choice(['historic', 'analytic']))
@click.argument('request_type', type=click.Choice(['table', 'histogram']))
@click.option('--filters', 'filters', help='Parameter structure for `filters` (JSON): - `timestamp` (required): Object with fields `from` and `to` (both integers, UNIX timestamps) defining the query time range. - `vhost` (required, *array of strings*): Site names. - `result_size` (optional, *integer*): Maximum number of results to return. - `clientip` (optional, *array of strings*): Client IPs - `geoip.city_name` (optional, *array of strings*): City names - `geoip.country_code2` (optional, *array of strings*): Country codes - `geoip.country_name` (optional, *array of strings*): Country names - `targetpath` (optional, *array of strings*): Target paths - `targeturi` (optional, *array of strings*): Target URIs - `transaction.messages.message` (optional, *array of strings*): Transaction messages - `transaction.messages.details.ruleId` (optional, *array of strings*): Rule IDs  **Required fields:** `timestamp`, `vhost`  **Example:** `?filters={"timestamp": {"from": 1776944395, "to": 1776945295}, "vhost": []}`. JSON object with keys:   timestamp(object [required]): {from(integer [required]), to(integer [required])}   vhost(array [required]) Zone names (array of string)   result_size(integer)   clientip(array) Client IPs (array of string)   geoip.city_name(array) City names (array of string)   geoip.country_code2(array) Country codes (array of string)   geoip.country_name(array) Country names (array of string)   targetpath(array) Target paths (array of string)   targeturi(array) Target URIs (array of string)   transaction.messages.message(array) Transaction messages (array of string)   transaction.messages.details.ruleId(array) Rule IDs (array of string)', required=True, type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
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
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
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
@click.option('--filters', 'filters', help='Parameter structure for `filters` (JSON): - `timestamp` (required): Object with fields `from` and `to` (both integers, UNIX timestamps) defining the query time range. - `vhost` (optional, *array of strings*): Site names. - `clients` (required, *type array*):  - `service` (required, *type string*):  Possible values: [\'botmitigation\', \'delivery\', \'dnsdelegation\', \'i3\', \'storage\', \'transcoding\', \'waf\'].  **Required fields:** `timestamp`, `clients`, `service`  **Example:** `?filters={"timestamp": {"from": 1776944395, "to": 1776945295}, "clients": [], "service": "botmitigation"}`. JSON object with keys:   timestamp(object [required]): {from(integer [required]), to(integer [required])}   clients(array [required]) (array of integer)   service(string [required]) choices=[\'botmitigation\', \'delivery\', \'dnsdelegation\', \'i3\', \'storage\', \'transcoding\', \'waf\'] (only used when listing)', type=str)
@click.argument('company_id', required=False, type=str, default=None)
def get_consumption(filters, company_id):
    """Historic Consumption (omit ID) / Historic Consumption Details (with ID)"""
    if company_id is None:
        company_id = Config.get_context('company_id')
    if company_id is None:
        raise click.UsageError("Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.")
    if company_id is not None:
        url = f"{Config.API_URL}/v1/statistics/consumption/{company_id}/"
        params = {}
    else:
        url = f"{Config.API_URL}/v1/statistics/consumption/"
        params = {
            'filters': filters,
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

@get_group.command(name='metrics-prometheus')
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
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
@click.argument('request_type', type=click.Choice(['table', 'histogram']))
@click.option('--filters', 'filters', help='Parameter structure for `filters` (JSON): - `timestamp` (required): Object with fields `from` and `to` (both integers, UNIX timestamps) defining the query time range. - `vhost` (required, *array of strings*): Site names. - `result_size` (optional, *integer*): Maximum number of results to return. - `tcdn.varnish.referer` (optional, *array of strings*): Referer - `tcdn.varnish.request` (optional, *array of strings*): Request - `tcdn.varnish.backend-goto` (optional, *array of strings*): Backend Go to - `tcdn.varnish.agent` (optional, *array of strings*): Agent - `tcdn.varnish.clientid` (optional, *array of strings*): Client ID - `tcdn.varnish.regioncode` (optional, *array of strings*): Region Code - `tcdn.varnish.vary` (optional, *array of strings*): Vary - `tcdn.varnish.midtier-backend` (optional, *array of strings*): Midtier Backend - `tcdn.varnish.origin` (optional, *array of strings*): Origin - `tcdn.varnish.countrycode` (optional, *array of strings*): Country Code - `tcdn.varnish.t-fetch` (optional, *array of strings*): Fetch time - `tcdn.varnish.t-beresp` (optional, *array of strings*): Backend response time - `tcdn.varnish.t-error` (optional, *array of strings*): Error time - `tcdn.varnish.t-berespbody-acc` (optional, *array of strings*): Backend response body time - `tcdn.varnish.path` (optional, *array of strings*): Path - `tcdn.varnish.t-bereq` (optional, *array of strings*): Backend request time - `tcdn.varnish.clientip` (optional, *array of strings*): Client IP - `tcdn.varnish.t-ttfb` (optional, *array of strings*): Time to first byte - `tcdn.varnish.backend` (optional, *array of strings*): Backend - `tcdn.varnish.cache-control` (optional, *array of strings*): Cache control - `tcdn.varnish.timestamp` (optional, *array of strings*): Timestamp - `tcdn.varnish.backend-name` (optional, *array of strings*): Backend name - `tcdn.varnish.method` (optional, *array of strings*): Method - `tcdn.varnish.vxid` (optional, *array of strings*): VXID - `tcdn.varnish.t-start` (optional, *array of strings*): Start time - `tcdn.varnish.t-berespbody` (optional, *array of strings*): Backend response body - `tcdn.varnish.vhost` (optional, *array of strings*): Vhost - `tcdn.varnish.t-process` (optional, *array of strings*): Process time - `tcdn.varnish.t-connected` (optional, *array of strings*): Connection time - `tcdn.varnish.orig-url` (optional, *array of strings*): Original URL - `tcdn.varnish.x-vary-tcdn` (optional, *array of strings*): Vary TCDN - `tcdn.varnish.bytes` (optional, *array of strings*): Bytes - `tcdn.varnish.response` (optional, *array of strings*): Response - `tcdn.varnish.orig-host` (optional, *array of strings*): Original host - `tcdn.varnish.response_time` (optional, *array of strings*): Response time - `tcdn.varnish.asn` (optional, *array of strings*): ASN  **Required fields:** `timestamp`, `vhost`  **Example:** `?filters={"timestamp": {"from": 1776944395, "to": 1776945295}, "vhost": []}`. JSON object with keys:   timestamp(object [required]): {from(integer [required]), to(integer [required])}   vhost(array [required]) Zone names (array of string)   result_size(integer)   tcdn.varnish.referer(array) Referer (array of string)   tcdn.varnish.request(array) Request (array of string)   tcdn.varnish.backend-goto(array) Backend Go to (array of string)   tcdn.varnish.agent(array) Agent (array of string)   tcdn.varnish.clientid(array) Client ID (array of string)   tcdn.varnish.regioncode(array) Region Code (array of string)   tcdn.varnish.vary(array) Vary (array of string)   tcdn.varnish.midtier-backend(array) Midtier Backend (array of string)   tcdn.varnish.origin(array) Origin (array of string)   tcdn.varnish.countrycode(array) Country Code (array of string)   tcdn.varnish.t-fetch(array) Fetch time (array of string)   tcdn.varnish.t-beresp(array) Backend response time (array of string)   tcdn.varnish.t-error(array) Error time (array of string)   tcdn.varnish.t-berespbody-acc(array) Backend response body time (array of string)   tcdn.varnish.path(array) Path (array of string)   tcdn.varnish.t-bereq(array) Backend request time (array of string)   tcdn.varnish.clientip(array) Client IP (array of string)   tcdn.varnish.t-ttfb(array) Time to first byte (array of string)   tcdn.varnish.backend(array) Backend (array of string)   tcdn.varnish.cache-control(array) Cache control (array of string)   tcdn.varnish.timestamp(array) Timestamp (array of string)   tcdn.varnish.backend-name(array) Backend name (array of string)   tcdn.varnish.method(array) Method (array of string)   tcdn.varnish.vxid(array) VXID (array of string)   tcdn.varnish.t-start(array) Start time (array of string)   tcdn.varnish.t-berespbody(array) Backend response body (array of string)   tcdn.varnish.vhost(array) Vhost (array of string)   tcdn.varnish.t-process(array) Process time (array of string)   tcdn.varnish.t-connected(array) Connection time (array of string)   tcdn.varnish.orig-url(array) Original URL (array of string)   tcdn.varnish.x-vary-tcdn(array) Vary TCDN (array of string)   tcdn.varnish.bytes(array) Bytes (array of string)   tcdn.varnish.response(array) Response (array of string)   tcdn.varnish.orig-host(array) Original host (array of string)   tcdn.varnish.response_time(array) Response time (array of string)   tcdn.varnish.asn(array) ASN (array of string)', required=True, type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
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
@click.argument('temporality', type=click.Choice(['historic', 'analytic']))
@click.argument('request_type', type=click.Choice(['table', 'histogram']))
@click.option('--filters', 'filters', help='Parameter structure for `filters` (JSON): - `timestamp` (required): Object with fields `from` and `to` (both integers, UNIX timestamps) defining the query time range. - `vhost` (required, *array of strings*): Site names.  **Required fields:** `timestamp`, `vhost`  **Example:** `?filters={"timestamp": {"from": 1776944395, "to": 1776945295}, "vhost": []}`. JSON object with keys:   timestamp(object [required]): {from(integer [required]), to(integer [required])}   vhost(array [required]) Zone names (array of string)', required=True, type=str)
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
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
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
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
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
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
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
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
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
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
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
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
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
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
@click.option('--company-id', 'company_id', required=False, type=str, help=' (Default: from context)')
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

