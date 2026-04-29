import click
import requests
import json
from te_api.auth import get_auth_headers
from te_api.config import Config

@click.group()
def cli():
    """Inventory operations."""
    pass

@cli.group(name='get')
def get_group():
    """Get operations."""
    pass

@get_group.command(name='node')
@click.argument('node_id', required=False, type=str, default=None)
def get_node(node_id):
    """Get Nodes List (omit ID) / Get Node Details (with ID)"""
    if node_id is not None:
        url = f"{Config.API_URL}/v1/inventory/node/{node_id}/"
        params = {}
    else:
        url = f"{Config.API_URL}/v1/inventory/node/"
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

@get_group.command(name='owasp-rules')
@click.argument('rule_id', required=False, type=str, default=None)
def get_owasp_rules(rule_id):
    """Get OWASP Core set of rules List (omit ID) / Get OWASP Core set of rules Details (with ID)"""
    if rule_id is not None:
        url = f"{Config.API_URL}/v1/inventory/owasp_rules/{rule_id}/"
        params = {}
    else:
        url = f"{Config.API_URL}/v1/inventory/owasp_rules/"
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

@get_group.command(name='pop')
def get_pop():
    """Get PoP list"""
    url = f"{Config.API_URL}/v1/inventory/pop/"
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

@get_group.command(name='pop-list')
@click.argument('pop_id', type=str)
def get_pop_list(pop_id):
    """Get PoP Details"""
    url = f"{Config.API_URL}/v1/inventory/pop/{pop_id}/"
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

@get_group.command(name='provider')
def get_provider():
    """Get Provider list"""
    url = f"{Config.API_URL}/v1/inventory/provider/"
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

@get_group.command(name='provider-list')
@click.argument('provider_id', type=str)
def get_provider_list(provider_id):
    """Get Provider Details"""
    url = f"{Config.API_URL}/v1/inventory/provider/{provider_id}/"
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

