import yaml
import os
import re
import click
import requests
from pathlib import Path

DEFAULT_SCHEMA_URL = "https://api.transparentcdn.com/schema"

# Mapping OpenAPI types to Click types
TYPE_MAP = {
    "integer": "int",
    "boolean": "bool",
    "string": "str",
    "number": "float",
    "array": "list",
    "object": "str",
}

# Standardized verbs mapping
VERB_MAP = {
    "list": "get",
    "retrieve": "get",
    "detail": "get",
    "check": "get",
    "view": "get",
    "create": "create",
    "add": "create",
    "post": "create",
    "update": "update",
    "edit": "update",
    "change": "update",
    "modify": "update",
    "partial_update": "update",
    "destroy": "delete",
    "delete": "delete",
    "remove": "delete",
}


def build_object_help(schema, description=""):
    """Build a descriptive help text from an object schema's properties."""
    properties = schema.get("properties", {})
    if not properties:
        return description

    required_fields = set(schema.get("required", []))
    parts = []
    if description:
        parts.append(description + ".")

    parts.append("JSON object with keys:")

    for prop_name, prop_schema in properties.items():
        prop_type = prop_schema.get("type", "string")
        prop_desc = prop_schema.get("description", "")
        req_marker = " [required]" if prop_name in required_fields else ""

        # Handle nested objects (e.g., timestamp with from/to)
        if prop_type == "object":
            nested_props = prop_schema.get("properties", {})
            nested_req = set(prop_schema.get("required", []))
            if nested_props:
                sub_keys = []
                for sub_name, sub_schema in nested_props.items():
                    sub_type = sub_schema.get("type", "string")
                    sub_desc = sub_schema.get("description", "")
                    sub_req = " [required]" if sub_name in nested_req else ""
                    entry = f"{sub_name}({sub_type}{sub_req})"
                    if sub_desc:
                        entry += f" {sub_desc}"
                    # Handle enum in nested properties
                    if "enum" in sub_schema:
                        entry += f" choices={sub_schema['enum']}"
                    sub_keys.append(entry)
                parts.append(
                    f"  {prop_name}(object{req_marker}): {{{', '.join(sub_keys)}}}"
                )
                continue

        entry = f"  {prop_name}({prop_type}{req_marker})"
        if prop_desc:
            entry += f" {prop_desc}"

        # Handle enum values
        if "enum" in prop_schema:
            entry += f" choices={prop_schema['enum']}"

        # Handle array items description
        if prop_type == "array" and "items" in prop_schema:
            items_type = prop_schema["items"].get("type", "string")
            entry += f" (array of {items_type})"

        parts.append(entry)

    return " ".join(parts)


def choices_from_schema(schema):
    """Extract choice values from a schema's enum or pattern field.

    Returns a list of string choices if found, otherwise None.
    Supports:
      - schema.enum: ['val1', 'val2']
      - schema.pattern: '^val1|val2|val3$'
    """
    enum_values = schema.get("enum")
    if enum_values:
        return [str(v) for v in enum_values]

    pattern = schema.get("pattern", "")
    # Match patterns like ^word1|word2|word3$ (literal alternatives)
    match = re.match(r"^\^?([\w]+(?:\|[\w]+)+)\$?$", pattern)
    if match:
        return match.group(1).split("|")

    return None


def clean_name(name):
    # Ensure name is not a python keyword
    keywords = [
        "from",
        "import",
        "class",
        "def",
        "return",
        "pass",
        "with",
        "as",
        "if",
        "else",
        "elif",
        "for",
        "while",
        "try",
        "except",
        "raise",
        "finally",
        "break",
        "continue",
        "in",
        "is",
        "not",
        "and",
        "or",
        "True",
        "False",
        "None",
        "global",
        "nonlocal",
        "lambda",
        "yield",
        "del",
        "assert",
    ]
    cleaned = re.sub(r"\W|^(?=\d)", "_", name)
    if cleaned in keywords:
        return f"{cleaned}_param"
    return cleaned


def to_kebab_case(name):
    name = re.sub(r"([A-Z])", r"_\1", name).lower()
    return name.replace("_", "-").strip("-")


def load_spec(spec_path):
    with open(spec_path, "r") as f:
        return yaml.safe_load(f)


def download_spec(schema_url, client_id=None, client_secret=None):
    """Fetch the OpenAPI spec from a remote URL using the same OAuth2
    flow as the runtime CLI. CLI overrides for client id/secret take
    precedence over `.env` / environment variables."""
    from te_api.config import Config
    from te_api.auth import get_auth_headers

    if client_id:
        Config.CLIENT_ID = client_id
    if client_secret:
        Config.CLIENT_SECRET = client_secret
    Config.validate()

    headers = get_auth_headers()
    response = requests.get(schema_url, headers=headers)
    response.raise_for_status()
    return yaml.safe_load(response.text)


def parse_operation_id(operation_id, tag):
    version = 0
    match = re.match(r"^v(\d+)_", operation_id)
    if match:
        version = int(match.group(1))

    clean_op = re.sub(r"^v\d+_", "", operation_id)

    if clean_op.lower().startswith(f"{tag.lower()}_"):
        clean_op = clean_op[len(tag) + 1 :]

    # Strip trailing duplicate-resolver suffix like `_2`, `_3` that the
    # OpenAPI generator adds when the same logical name collides on
    # different paths. We keep its value as a secondary tiebreaker so
    # the company-scoped variant (usually the higher number) wins.
    dup_suffix = 0
    m_dup = re.search(r"_(\d+)$", clean_op)
    if m_dup:
        dup_suffix = int(m_dup.group(1))
        clean_op = clean_op[: m_dup.start()]

    parts = clean_op.split("_")

    verb_found = "action"
    noun_parts = parts

    if len(parts) >= 2:
        suffix_2 = f"{parts[-2]}_{parts[-1]}"
        if suffix_2 in [
            "create_list",
            "destroy_detail",
            "update_detail",
            "retrieve_detail",
            "partial_update_detail",
            "check_retrieve",
        ]:
            if "create" in suffix_2:
                verb_found = "create"
            elif "destroy" in suffix_2:
                verb_found = "delete"
            elif "update" in suffix_2:
                verb_found = "update"
            elif "retrieve" in suffix_2 or "check" in suffix_2:
                verb_found = "get"
            noun_parts = parts[:-2]
        elif parts[-1] in VERB_MAP:
            verb_found = VERB_MAP[parts[-1]]
            noun_parts = parts[:-1]
    elif len(parts) == 1 and parts[0] in VERB_MAP:
        verb_found = VERB_MAP[parts[0]]
        noun_parts = []
    elif len(parts) > 0 and parts[-1] in VERB_MAP:
        verb_found = VERB_MAP[parts[-1]]
        noun_parts = parts[:-1]

    noun = "-".join(noun_parts).replace("_", "-")
    if not noun:
        noun = "root"

    return version, dup_suffix, noun, verb_found


def generate_function_code(command_name, path, method, details):
    summary = details.get("summary", "No summary").replace('"', '\\"')

    params_code = []
    args_list = []
    pass_params = []
    # Reserve variable names used in the generated function body to avoid collisions
    used_vars = {"url", "headers", "params", "data", "response"}
    path_var_map = {}

    if "parameters" in details:
        for param in details["parameters"]:
            name = param["name"]
            param_in = param["in"]

            required = param.get("required", False)
            schema = param.get("schema", {})
            param_type = schema.get("type", "string")
            raw_help = param.get("description", "").replace("\n", " ").strip()

            # Enrich help text for object-type parameters with schema properties
            if param_type == "object" and "properties" in schema:
                raw_help = build_object_help(schema, raw_help)

            help_text = raw_help.replace("\\", "\\\\").replace("'", "\\'")

            clean_var_name = clean_name(name)

            if clean_var_name in used_vars:
                if param_in == "path":
                    clean_var_name = f"{clean_var_name}_arg"
                else:
                    clean_var_name = f"{clean_var_name}_opt"

            base_clean = clean_var_name
            idx = 1
            while clean_var_name in used_vars:
                clean_var_name = f"{base_clean}_{idx}"
                idx += 1

            used_vars.add(clean_var_name)

            click_type = TYPE_MAP.get(param_type, "str")

            if name == "company_id":
                # Special handling for company_id to allow context usage

                option_str = f"@click.option('--company-id', '{clean_var_name}', required=False, type={click_type}, help='{help_text} (Default: from context)')"
                params_code.append(option_str)
                args_list.append(clean_var_name)

                if param_in == "path":
                    path_var_map[name] = clean_var_name
                else:
                    pass_params.append(f"'{name}': {clean_var_name}")

            elif param_in == "path":
                path_choices = choices_from_schema(schema)
                if path_choices:
                    params_code.append(
                        f"@click.argument('{clean_var_name}', type=click.Choice({path_choices}))"
                    )
                else:
                    params_code.append(
                        f"@click.argument('{clean_var_name}', type={click_type})"
                    )
                args_list.append(clean_var_name)
                path_var_map[name] = clean_var_name
            elif param_in == "query":
                query_choices = choices_from_schema(schema)
                option_str = f"@click.option('--{to_kebab_case(name)}', '{clean_var_name}', help='{help_text}'"
                if required:
                    option_str += ", required=True"
                if param_type == "boolean":
                    option_str += ", is_flag=True"
                elif query_choices:
                    option_str += f", type=click.Choice({query_choices})"
                else:
                    option_str += f", type={click_type}"
                if "default" in schema:
                    option_str += f", default={repr(schema['default'])}"
                option_str += ")"
                params_code.append(option_str)
                args_list.append(clean_var_name)
                pass_params.append(f"'{name}': {clean_var_name}")

    json_body_var = None
    if "requestBody" in details:
        json_body_var = "json_body"
        if json_body_var in used_vars:
            json_body_var = "request_body_json"
        used_vars.add(json_body_var)
        params_code.append(
            f"@click.option('--json-body', '{json_body_var}', help='JSON string for request body')"
        )
        args_list.append(json_body_var)

    final_path = path
    for raw, final in path_var_map.items():
        final_path = final_path.replace(f"{{{raw}}}", f"{{{final}}}")

    code = ""
    for p in reversed(params_code):
        code += f"{p}\n"

    code += f"def {command_name}({', '.join(args_list)}):\n"
    code += f'    """{summary}"""\n'

    # Inject context logic for company_id
    if "company_id" in args_list:
        code += f"    if company_id is None:\n"
        code += f"        company_id = Config.get_context('company_id')\n"
        code += f"    if company_id is None:\n"
        code += f"        raise click.UsageError(\"Missing 'company_id'. Specify it with --company-id or set a default with 'te-api set-company <id>'.\")\n"

    code += f'    url = f"{{Config.API_URL}}{final_path}"\n'
    code += f"    headers = get_auth_headers()\n"

    if pass_params:
        code += f"    params = {{\n"
        for pp in pass_params:
            code += f"        {pp},\n"
        code += f"    }}\n"
        code += f"    params = {{k: v for k, v in params.items() if v is not None}}\n"
    else:
        code += f"    params = {{}}\n"

    if json_body_var:
        code += f"    data = json.loads({json_body_var}) if {json_body_var} else None\n"
    else:
        code += f"    data = None\n"

    code += f"    try:\n"
    code += f"        response = requests.{method}(url, headers=headers, params=params, json=data)\n"
    code += f"        response.raise_for_status()\n"
    code += f"        if response.content:\n"
    code += f"            try:\n"
    code += f"                click.echo(json.dumps(response.json(), indent=2))\n"
    code += f"            except json.JSONDecodeError:\n"
    code += f"                click.echo(response.text)\n"
    code += f"        else:\n"
    code += f"            click.echo('Success (No content)')\n"
    code += f"    except requests.exceptions.RequestException as e:\n"
    code += f'        click.echo(f"Error: {{e}}")\n'
    code += f"        if e.response is not None:\n"
    code += f"             click.echo(e.response.text)\n"

    return code


def _path_segments(path):
    return [p for p in path.strip("/").split("/") if p]


def _path_param_name(segment):
    """Return the param name if a segment is `{name}`, else None."""
    m = re.match(r"^\{(\w+)\}$", segment)
    return m.group(1) if m else None


def find_list_detail_pair(candidates):
    """Locate a (list, detail) candidate pair where the detail path equals
    the list path plus one trailing `{param}/` segment. Returns
    (list_candidate, detail_candidate, param_name) or None."""
    for detail in candidates:
        d_path = detail[3]
        d_segments = _path_segments(d_path)
        if not d_segments:
            continue
        param_name = _path_param_name(d_segments[-1])
        if not param_name:
            continue
        list_prefix_segments = d_segments[:-1]
        for lst in candidates:
            if lst is detail:
                continue
            if _path_segments(lst[3]) == list_prefix_segments:
                return lst, detail, param_name
    return None


def _candidate_priority(candidate):
    """Sort key used to prefer company-scoped, newer, dup-suffix-newer paths."""
    version, dup_suffix, _details, path, _method = candidate
    company_scoped = "{company_id}" in path
    return (company_scoped, version, dup_suffix)


def resolve_candidates(unique_cmds):
    """Collapse the per-(tag,verb,noun) candidate lists into the final
    structure consumed by code generation. Each value becomes a dict with
    a `kind` discriminator: `single` for the regular case, `merged` when
    a GET list+detail pair was detected and combined into one command."""
    resolved = {}
    for tag, verbs in unique_cmds.items():
        resolved[tag] = {}
        for verb, nouns in verbs.items():
            resolved[tag][verb] = {}
            for noun, candidates in nouns.items():
                if verb == "get" and len(candidates) > 1:
                    pair = find_list_detail_pair(candidates)
                    if pair:
                        lst, detail, param_name = pair
                        resolved[tag][verb][noun] = {
                            "kind": "merged",
                            "method": detail[4],
                            "list_path": lst[3],
                            "list_details": lst[2],
                            "detail_path": detail[3],
                            "detail_details": detail[2],
                            "id_param": param_name,
                        }
                        continue

                best = max(candidates, key=_candidate_priority)
                resolved[tag][verb][noun] = {
                    "kind": "single",
                    "method": best[4],
                    "path": best[3],
                    "details": best[2],
                }
    return resolved


def generate_merged_function_code(command_name, list_path, list_details,
                                  detail_path, detail_details, id_param,
                                  method):
    """Generate a click command that lists when no ID is supplied and
    fetches the detail when an ID is provided. Built on top of the list
    operation's parameter set, with the detail's path-final argument
    added as an optional positional."""
    summary_list = list_details.get("summary", "List").replace('"', '\\"')
    summary_detail = detail_details.get("summary", "Detail").replace('"', '\\"')
    summary = f"{summary_list} (omit ID) / {summary_detail} (with ID)"

    used_vars = {"url", "headers", "params", "data", "response"}
    params_code = []
    args_list = []
    pass_params = []
    path_var_map = {}

    id_var_name = clean_name(id_param)
    if id_var_name in used_vars:
        id_var_name = f"{id_var_name}_arg"
    used_vars.add(id_var_name)

    for param in list_details.get("parameters", []):
        name = param["name"]
        param_in = param["in"]
        if param_in == "path" and name == id_param:
            continue

        required = param.get("required", False)
        schema = param.get("schema", {})
        param_type = schema.get("type", "string")
        raw_help = param.get("description", "").replace("\n", " ").strip()

        if param_type == "object" and "properties" in schema:
            raw_help = build_object_help(schema, raw_help)

        help_text = raw_help.replace("\\", "\\\\").replace("'", "\\'")

        clean_var_name = clean_name(name)
        if clean_var_name in used_vars:
            clean_var_name = (
                f"{clean_var_name}_arg" if param_in == "path" else f"{clean_var_name}_opt"
            )
        base_clean = clean_var_name
        idx = 1
        while clean_var_name in used_vars:
            clean_var_name = f"{base_clean}_{idx}"
            idx += 1
        used_vars.add(clean_var_name)

        click_type = TYPE_MAP.get(param_type, "str")

        if name == "company_id":
            params_code.append(
                f"@click.option('--company-id', '{clean_var_name}', required=False, "
                f"type={click_type}, help='{help_text} (Default: from context)')"
            )
            args_list.append(clean_var_name)
            if param_in == "path":
                path_var_map[name] = clean_var_name
            else:
                pass_params.append((name, clean_var_name))
        elif param_in == "path":
            path_choices = choices_from_schema(schema)
            if path_choices:
                params_code.append(
                    f"@click.argument('{clean_var_name}', type=click.Choice({path_choices}))"
                )
            else:
                params_code.append(
                    f"@click.argument('{clean_var_name}', type={click_type})"
                )
            args_list.append(clean_var_name)
            path_var_map[name] = clean_var_name
        elif param_in == "query":
            query_choices = choices_from_schema(schema)
            # Query params are never enforced as required client-side here:
            # the OpenAPI spec sometimes marks `filters` as required even
            # though the API accepts the list call without it. Let the
            # server be the source of truth and surface its 400 if needed.
            option_str = (
                f"@click.option('--{to_kebab_case(name)}', '{clean_var_name}', "
                f"help='{help_text} (only used when listing)'"
            )
            if param_type == "boolean":
                option_str += ", is_flag=True"
            elif query_choices:
                option_str += f", type=click.Choice({query_choices})"
            else:
                option_str += f", type={click_type}"
            if "default" in schema:
                option_str += f", default={repr(schema['default'])}"
            option_str += ")"
            params_code.append(option_str)
            args_list.append(clean_var_name)
            pass_params.append((name, clean_var_name))

    # Optional ID positional argument (must be last in click decorator stack
    # since decorators apply bottom-up; we prepend later when writing).
    id_arg_decorator = (
        f"@click.argument('{id_var_name}', required=False, type=str, default=None)"
    )
    args_list.append(id_var_name)

    final_list_path = list_path
    final_detail_path = detail_path
    for raw, final in path_var_map.items():
        final_list_path = final_list_path.replace(f"{{{raw}}}", f"{{{final}}}")
        final_detail_path = final_detail_path.replace(f"{{{raw}}}", f"{{{final}}}")
    final_detail_path = final_detail_path.replace(
        f"{{{id_param}}}", f"{{{id_var_name}}}"
    )

    code = ""
    for p in reversed(params_code):
        code += f"{p}\n"
    code += f"{id_arg_decorator}\n"

    code += f"def {command_name}({', '.join(args_list)}):\n"
    code += f'    """{summary}"""\n'

    if "company_id" in args_list:
        code += "    if company_id is None:\n"
        code += "        company_id = Config.get_context('company_id')\n"
        code += "    if company_id is None:\n"
        code += (
            "        raise click.UsageError(\"Missing 'company_id'. Specify it with "
            "--company-id or set a default with 'te-api set-company <id>'.\")\n"
        )

    code += f"    if {id_var_name} is not None:\n"
    code += f'        url = f"{{Config.API_URL}}{final_detail_path}"\n'
    code += "        params = {}\n"
    code += "    else:\n"
    code += f'        url = f"{{Config.API_URL}}{final_list_path}"\n'
    if pass_params:
        code += "        params = {\n"
        for spec_name, var_name in pass_params:
            code += f"            '{spec_name}': {var_name},\n"
        code += "        }\n"
        code += "        params = {k: v for k, v in params.items() if v is not None}\n"
    else:
        code += "        params = {}\n"

    code += "    headers = get_auth_headers()\n"
    code += "    data = None\n"
    code += "    try:\n"
    code += f"        response = requests.{method}(url, headers=headers, params=params, json=data)\n"
    code += "        response.raise_for_status()\n"
    code += "        if response.content:\n"
    code += "            try:\n"
    code += "                click.echo(json.dumps(response.json(), indent=2))\n"
    code += "            except json.JSONDecodeError:\n"
    code += "                click.echo(response.text)\n"
    code += "        else:\n"
    code += "            click.echo('Success (No content)')\n"
    code += "    except requests.exceptions.RequestException as e:\n"
    code += '        click.echo(f"Error: {e}")\n'
    code += "        if e.response is not None:\n"
    code += "             click.echo(e.response.text)\n"

    return code


@click.command()
@click.option(
    "--from-file",
    "from_file",
    type=click.Path(exists=True, dir_okay=False),
    default=None,
    help="Use a local OpenAPI YAML/JSON file instead of downloading the schema.",
)
@click.option(
    "--schema-url",
    default=DEFAULT_SCHEMA_URL,
    show_default=True,
    help="URL to download the OpenAPI spec from when --from-file is not used.",
)
@click.option(
    "--client-id",
    "client_id",
    default=None,
    help="OAuth2 client ID to authenticate the schema download. Overrides "
    "TRANSPARENT_CLIENT_ID from the environment / .env.",
)
@click.option(
    "--client-secret",
    "client_secret",
    default=None,
    help="OAuth2 client secret to authenticate the schema download. Overrides "
    "TRANSPARENT_CLIENT_SECRET from the environment / .env.",
)
@click.option(
    "--output-dir",
    default="te_api/api",
    help="Output directory for generated API modules",
)
@click.option(
    "--read-only",
    is_flag=True,
    default=False,
    help="Generate only read (GET) operations, excluding create/update/delete/action verbs.",
)
def build(from_file, schema_url, client_id, client_secret, output_dir, read_only):
    """Build the API CLI from an OpenAPI spec.

    By default, the spec is downloaded from the remote schema URL using the
    OAuth2 credentials configured for the runtime CLI. Pass --from-file to
    use a local copy instead.
    """
    if from_file:
        click.echo(f"Loading spec from {from_file}...")
        spec = load_spec(from_file)
    else:
        click.echo(f"Downloading spec from {schema_url}...")
        spec = download_spec(schema_url, client_id, client_secret)

    unique_cmds = {}

    for path, methods in spec["paths"].items():
        for method, details in methods.items():
            if method not in ["get", "post", "put", "delete", "patch"]:
                continue

            tags = details.get("tags", ["default"])
            tag = tags[0] if tags else "default"
            tag = clean_name(tag.lower())

            op_id = details.get("operationId", "")
            if not op_id:
                continue

            version, dup_suffix, noun, verb = parse_operation_id(op_id, tag)

            if tag not in unique_cmds:
                unique_cmds[tag] = {}
            if verb not in unique_cmds[tag]:
                unique_cmds[tag][verb] = {}
            unique_cmds[tag][verb].setdefault(noun, []).append(
                (version, dup_suffix, details, path, method)
            )

    # Resolve candidate lists into final commands. For verb=get we look
    # for list+detail pairs (paths that differ only by a trailing
    # `{param}/`) and merge them into a single command with an optional
    # ID argument; for everything else we pick the highest-priority
    # candidate (preferring company-scoped paths, then version, then
    # duplicate-suffix index).
    unique_cmds = resolve_candidates(unique_cmds)

    # Filter to read-only operations if requested
    if read_only:
        filtered_cmds = {}
        for tag, verbs in unique_cmds.items():
            if "get" in verbs:
                # Drop commands whose real HTTP method is not GET (e.g. POST list searches)
                get_only = {
                    noun: data
                    for noun, data in verbs["get"].items()
                    if data["method"] == "get"
                }
                if get_only:
                    filtered_cmds[tag] = {"get": get_only}
        unique_cmds = filtered_cmds
        if not unique_cmds:
            click.echo("Warning: No GET operations found in the spec.")
            return

    out_path = Path(output_dir)
    os.makedirs(out_path, exist_ok=True)

    generated_tags = []

    # 1. Generate Tag Files
    for tag, verbs in unique_cmds.items():
        file_path = out_path / f"{tag}.py"
        print(f"Generating {file_path}...")

        with open(file_path, "w") as f:
            f.write("import click\n")
            f.write("import requests\n")
            f.write("import json\n")
            f.write("from te_api.auth import get_auth_headers\n")
            f.write("from te_api.config import Config\n\n")

            f.write("@click.group()\n")
            f.write(f"def cli():\n")
            f.write(f'    """{tag.capitalize()} operations."""\n')
            f.write(f"    pass\n\n")

            for verb in verbs.keys():
                group_func = f"{verb}_group"

                f.write(f"@cli.group(name='{verb}')\n")
                f.write(f"def {group_func}():\n")
                f.write(f'    """{verb.capitalize()} operations."""\n')
                f.write(f"    pass\n\n")

                for noun, data in verbs[verb].items():
                    cmd_name = noun
                    if cmd_name == "root":
                        cmd_name = "index"

                    f.write(f"@{group_func}.command(name='{cmd_name}')\n")

                    func_name = f"{verb}_{cmd_name}".replace("-", "_")
                    if func_name == group_func:
                        func_name = f"{func_name}_cmd"

                    if data["kind"] == "merged":
                        f.write(
                            generate_merged_function_code(
                                func_name,
                                data["list_path"],
                                data["list_details"],
                                data["detail_path"],
                                data["detail_details"],
                                data["id_param"],
                                data["method"],
                            )
                        )
                    else:
                        f.write(
                            generate_function_code(
                                func_name,
                                data["path"],
                                data["method"],
                                data["details"],
                            )
                        )
                    f.write("\n")

        generated_tags.append(tag)

    # 2. Generate Registry File
    registry_path = out_path / "registry.py"
    print(f"Generating {registry_path}...")
    with open(registry_path, "w") as f:
        f.write("# Auto-generated registry file. Do not edit manually.\n")
        for tag in generated_tags:
            f.write(f"from . import {tag}\n")

        f.write("\ndef register_api_commands(cli):\n")
        for tag in generated_tags:
            f.write(f"    cli.add_command({tag}.cli, name='{to_kebab_case(tag)}')\n")


if __name__ == "__main__":
    build()
