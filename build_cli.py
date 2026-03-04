import yaml
import os
import re
import click
from pathlib import Path

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


def parse_operation_id(operation_id, tag):
    version = 0
    match = re.match(r"^v(\d+)_", operation_id)
    if match:
        version = int(match.group(1))

    clean_op = re.sub(r"^v\d+_", "", operation_id)

    if clean_op.lower().startswith(f"{tag.lower()}_"):
        clean_op = clean_op[len(tag) + 1 :]

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

    return version, noun, verb_found


def generate_function_code(command_name, path, method, details):
    summary = details.get("summary", "No summary").replace('"', '\\"')

    params_code = []
    args_list = []
    pass_params = []
    used_vars = set()
    path_var_map = {}

    if "parameters" in details:
        for param in details["parameters"]:
            name = param["name"]
            param_in = param["in"]

            required = param.get("required", False)
            schema = param.get("schema", {})
            param_type = schema.get("type", "string")
            raw_help = param.get("description", "").replace("\n", " ")
            # Truncate first to avoid cutting escape sequences in half later
            truncated_help = raw_help[:100].strip()

            # Remove trailing backslashes or quotes to prevent invalid escape sequences when appending '...'
            truncated_help = truncated_help.rstrip("\\'")

            help_text = truncated_help.replace("\\", "\\\\").replace("'", "\\'")

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

                option_str = f"@click.option('--company-id', '{clean_var_name}', required=False, type={click_type}, help='{help_text[:100]}... (Default: from context)')"
                params_code.append(option_str)
                args_list.append(clean_var_name)

                if param_in == "path":
                    path_var_map[name] = clean_var_name
                else:
                    pass_params.append(f"'{name}': {clean_var_name}")

            elif param_in == "path":
                params_code.append(
                    f"@click.argument('{clean_var_name}', type={click_type})"
                )
                args_list.append(clean_var_name)
                path_var_map[name] = clean_var_name
            elif param_in == "query":
                option_str = f"@click.option('--{to_kebab_case(name)}', '{clean_var_name}', help='{help_text[:100]}...'"
                if required:
                    option_str += ", required=True"
                if param_type == "boolean":
                    option_str += ", is_flag=True"
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


@click.command()
@click.argument("spec_path", type=click.Path(exists=True))
@click.option(
    "--output-dir",
    default="te_api/api",
    help="Output directory for generated API modules",
)
def build(spec_path, output_dir):
    """Build the API CLI from an OpenAPI YAML spec."""
    spec = load_spec(spec_path)

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

            version, noun, verb = parse_operation_id(op_id, tag)

            if tag not in unique_cmds:
                unique_cmds[tag] = {}
            if verb not in unique_cmds[tag]:
                unique_cmds[tag][verb] = {}

            if noun in unique_cmds[tag][verb]:
                existing_ver = unique_cmds[tag][verb][noun][0]
                if version > existing_ver:
                    unique_cmds[tag][verb][noun] = (version, details, path, method)
            else:
                unique_cmds[tag][verb][noun] = (version, details, path, method)

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
                    version, details, path, method = data

                    cmd_name = noun
                    if cmd_name == "root":
                        cmd_name = "index"

                    f.write(f"@{group_func}.command(name='{cmd_name}')\n")

                    func_name = f"{verb}_{cmd_name}".replace("-", "_")
                    if func_name == group_func:
                        func_name = f"{func_name}_cmd"

                    f.write(generate_function_code(func_name, path, method, details))
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
