#!/usr/bin/env python3
"""Generate Azure ARM templates for fleet feeders from canonical AISstream templates."""

from __future__ import annotations

import argparse
import ast
import copy
import html
import json
import re
import shutil
import sys
from collections import Counter
from pathlib import Path, PureWindowsPath
from typing import Any


DEFAULT_CATALOG = Path(
    r"C:\Users\clemensv\.copilot\session-state\cb5ea344-87f5-406e-a13a-a66811763074\files\fleet-catalog.json"
)

VARIANT_REFERENCES = {
    "kafka": Path("feeders") / "aisstream" / "azure-template.json",
    "eventhub": Path("feeders") / "aisstream" / "azure-template-with-eventhub.json",
    "servicebus": Path("feeders") / "aisstream" / "azure-template-with-servicebus.json",
    "amqp": Path("feeders") / "aisstream" / "infra" / "azure-template-amqp.json",
    "mqtt": Path("feeders") / "aisstream" / "azure-template-mqtt.json",
    "eventgrid-mqtt": Path("feeders") / "aisstream" / "azure-template-with-eventgrid-mqtt.json",
}

TEMPLATE_VARIANTS = {
    "azure-template.json": "kafka",
    "azure-template-with-eventhub.json": "eventhub",
    "azure-template-with-servicebus.json": "servicebus",
    "azure-template-amqp.json": "amqp",
    "azure-template-mqtt.json": "mqtt",
    "azure-template-with-eventgrid-mqtt.json": "eventgrid-mqtt",
}

IMAGE_SUFFIXES = {
    "kafka": ":latest",
    "eventhub": ":latest",
    "servicebus": "-amqp:latest",
    "amqp": "-amqp:latest",
    "mqtt": "-mqtt:latest",
    "eventgrid-mqtt": "-mqtt:latest",
}

FRAMEWORK_ENV_NAMES = {"LOG_LEVEL", "PYTHONUNBUFFERED"}
# Infra parameters whose authoritative description lives in the variant
# reference template (not CONTAINER.md). Synced to every feeder on regen.
INFRA_REFERENCE_PARAMS = ("eventHubSku", "queueName")
GENERIC_DESCRIPTION_PATTERNS = (
    re.compile(r"^[A-Z0-9_]+ configuration value\.?$", re.IGNORECASE),
    re.compile(r"^Core configuration for this image variant\.?$", re.IGNORECASE),
)
DESCRIPTION_SOURCE_COUNTS: Counter[str] = Counter()
SOFT_WARNINGS: list[str] = []


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG, help="Path to fleet-catalog.json")
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1], help="Repository root")
    parser.add_argument("--filter", help="Comma-separated feeder slugs to generate")
    parser.add_argument("--dry-run", action="store_true", help="Write under tools/.gen-out instead of in-place")
    return parser.parse_args()


def variant_from_template(path: str) -> str:
    name = PureWindowsPath(path).name
    try:
        return TEMPLATE_VARIANTS[name]
    except KeyError as exc:
        raise ValueError(f"Unsupported template filename: {path}") from exc


def image_base_for(feeder: dict[str, Any]) -> str:
    raw = (feeder.get("imageBase") or "").strip()
    if not raw:
        raw = f"real-time-sources-{feeder['slug']}"
    if raw.startswith("ghcr.io/"):
        return raw
    if not raw.startswith("real-time-sources-"):
        raw = f"real-time-sources-{raw}"
    return f"ghcr.io/clemensv/{raw}"


def image_name_for(feeder: dict[str, Any], variant: str) -> str:
    return f"{image_base_for(feeder)}{IMAGE_SUFFIXES[variant]}"


def recursively_replace_aisstream(value: Any, slug: str) -> Any:
    if isinstance(value, dict):
        return {k: recursively_replace_aisstream(v, slug) for k, v in value.items()}
    if isinstance(value, list):
        return [recursively_replace_aisstream(v, slug) for v in value]
    if isinstance(value, str):
        return (
            value.replace("AISstream.io", slug)
            .replace("AISstream", slug)
            .replace("Aisstream", slug)
            .replace("aisstream", slug)
        )
    return value


def set_parameter_default(parameters: dict[str, Any], name: str, value: str) -> None:
    if name in parameters:
        parameters[name]["defaultValue"] = value


def remove_aisstream_parameters(parameters: dict[str, Any]) -> None:
    for name in list(parameters.keys()):
        if name.lower().startswith("aisstream"):
            del parameters[name]


def find_container_environment_arrays(obj: Any) -> list[list[dict[str, Any]]]:
    arrays: list[list[dict[str, Any]]] = []
    if isinstance(obj, dict):
        if isinstance(obj.get("environmentVariables"), list):
            arrays.append(obj["environmentVariables"])
        for value in obj.values():
            arrays.extend(find_container_environment_arrays(value))
    elif isinstance(obj, list):
        for item in obj:
            arrays.extend(find_container_environment_arrays(item))
    return arrays


def remove_aisstream_env_vars(env: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [item for item in env if not str(item.get("name", "")).startswith("AISSTREAM_")]


def insert_env_vars(env: list[dict[str, Any]], feeder: dict[str, Any]) -> list[dict[str, Any]]:
    feeder_env_names = {env_var["name"] for env_var in feeder.get("envVars", [])}
    if "POLL_INTERVAL" in feeder_env_names:
        feeder_env_names.add("POLLING_INTERVAL")
    base_env = [item for item in env if item.get("name") not in feeder_env_names]
    insert_at = next((i for i, item in enumerate(base_env) if item.get("name") in FRAMEWORK_ENV_NAMES), len(base_env))
    additions: list[dict[str, Any]] = []
    for env_var in feeder.get("envVars", []):
        parameter_ref = f"[parameters('{env_var['armParamName']}')]"
        item: dict[str, Any] = {"name": env_var["name"]}
        if env_var.get("isSecret"):
            item["secureValue"] = parameter_ref
        else:
            item["value"] = parameter_ref
        additions.append(item)
    return base_env[:insert_at] + additions + base_env[insert_at:]


def is_generic_description(description: str, env_name: str | None = None) -> bool:
    text = collapse_whitespace(strip_markdown(description))
    if not text:
        return True
    if any(pattern.match(text) for pattern in GENERIC_DESCRIPTION_PATTERNS):
        return True
    if env_name and text.lower() == f"{env_name.lower()} configuration value.":
        return True
    return False


def source_title(slug: str) -> str:
    known = {"entsoe": "ENTSO-E", "dwd": "DWD", "aisstream": "AISstream"}
    return known.get(slug, " ".join(part.upper() if len(part) <= 3 else part.capitalize() for part in slug.split("-")))


def friendly_env_name(env_name: str) -> str:
    words = [word for word in env_name.split("_") if word]
    if words and len(words[0]) > 2:
        words = words[1:]
    replacements = {
        "API": "API",
        "ID": "ID",
        "IDS": "IDs",
        "URL": "URL",
        "URLS": "URLs",
        "URI": "URI",
        "URIS": "URIs",
        "TLS": "TLS",
        "SASL": "SASL",
        "AMQP": "AMQP",
        "MQTT": "MQTT",
        "KAFKA": "Kafka",
        "WS": "WebSocket",
        "BBOX": "bounding box",
        "BBOXES": "bounding boxes",
        "MMSI": "MMSI",
    }
    tokens = [replacements.get(word, word.lower()) for word in words]
    if not tokens:
        return "Configuration value"
    text = " ".join(tokens)
    return text[:1].upper() + text[1:]


def fallback_description(slug: str, env_name: str) -> str:
    friendly = friendly_env_name(env_name)
    upper = env_name.upper()
    if upper.endswith("API_KEY"):
        friendly = f"{source_title(slug)} API key"
        return truncate_description(
            f"{friendly} used to authenticate upstream requests. Obtain it from the upstream provider's developer portal before deployment. See feeders/{slug}/CONTAINER.md for details."
        )
    if upper.endswith("SECURITY_TOKEN") or upper.endswith("TOKEN"):
        friendly = f"{source_title(slug)} security token"
        return truncate_description(
            f"{friendly} used to authenticate upstream requests. Register for or retrieve it from the upstream provider's account/API portal before deployment. See feeders/{slug}/CONTAINER.md for details."
        )
    return truncate_description(f"{friendly}. See feeders/{slug}/CONTAINER.md for details.")


def collapse_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def strip_markdown(text: str) -> str:
    text = html.unescape(text or "")
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"__([^_]+)__", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    return text


def clean_description(text: str) -> tuple[str, bool]:
    required = False
    cleaned = collapse_whitespace(strip_markdown(text)).replace("....", "...")
    cleaned = re.sub(r"^(Required\s*[:.]\s*)", lambda m: _mark_required(m), cleaned, flags=re.IGNORECASE)
    if getattr(clean_description, "_required", False):
        required = True
        clean_description._required = False  # type: ignore[attr-defined]
    return truncate_description(cleaned), required


def _mark_required(match: re.Match[str]) -> str:
    clean_description._required = True  # type: ignore[attr-defined]
    return ""


def truncate_description(text: str) -> str:
    text = collapse_whitespace(strip_markdown(text)).replace("....", "...")
    if len(text) <= 512:
        return text
    return text[:509].rstrip() + "..."


def split_markdown_table_row(line: str) -> list[str] | None:
    raw = line.strip()
    if not raw.startswith("|") or raw.count("|") < 2:
        return None
    if raw.endswith("|"):
        raw = raw[:-1]
    raw = raw[1:]
    cells: list[str] = []
    current: list[str] = []
    escaped = False
    for ch in raw:
        if ch == "\\" and not escaped:
            escaped = True
            current.append(ch)
            continue
        if ch == "|" and not escaped:
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(ch)
        escaped = False
    cells.append("".join(current).strip())
    return cells


def is_separator_row(cells: list[str]) -> bool:
    return all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells if cell)


def extract_env_names(cell: str) -> list[str]:
    names = re.findall(r"`([A-Z][A-Z0-9_]{2,})`", cell)
    if not names:
        names = re.findall(r"\b([A-Z][A-Z0-9_]{2,})\b", strip_markdown(cell))
    return list(dict.fromkeys(names))


def parse_markdown_env_table(path: Path) -> tuple[dict[str, str], set[str]]:
    descriptions: dict[str, str] = {}
    required: set[str] = set()
    if not path.exists():
        return descriptions, required
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    active_headers: list[str] | None = None
    previous_vars: list[str] = []
    for line in lines:
        cells = split_markdown_table_row(line)
        if not cells:
            active_headers = None
            previous_vars = []
            continue
        if is_separator_row(cells):
            continue
        lower_cells = [collapse_whitespace(strip_markdown(cell)).lower() for cell in cells]
        if any(header in {"variable", "env var", "environment variable"} for header in lower_cells) and any(
            header in {"description", "purpose", "notes"} for header in lower_cells
        ):
            active_headers = lower_cells
            previous_vars = []
            continue
        if active_headers:
            try:
                variable_idx = next(
                    i for i, header in enumerate(active_headers) if header in {"variable", "env var", "environment variable"}
                )
            except StopIteration:
                variable_idx = 0
            try:
                description_idx = next(i for i, header in enumerate(active_headers) if header in {"description", "purpose", "notes"})
            except StopIteration:
                description_idx = min(1, len(cells) - 1)
        else:
            variable_idx = 0
            description_idx = min(1, len(cells) - 1)
        if variable_idx >= len(cells) or description_idx >= len(cells):
            continue
        env_names = extract_env_names(cells[variable_idx])
        desc_text, is_required = clean_description(cells[description_idx])
        variable_cell_text = collapse_whitespace(strip_markdown(cells[variable_idx]))
        if env_names and desc_text:
            for env_name in env_names:
                descriptions.setdefault(env_name, desc_text)
                if is_required:
                    required.add(env_name)
            previous_vars = env_names
        elif previous_vars and desc_text and not variable_cell_text:
            # Only a blank variable cell indicates a wrapped continuation of the
            # previous row's description. Rows with a non-env-var label in the
            # variable cell (e.g. "topic prefix", "QoS default") are distinct
            # entries, not continuations, and must not be concatenated onto the
            # previous environment variable's description.
            for env_name in previous_vars:
                descriptions[env_name] = truncate_description(f"{descriptions.get(env_name, '')} {desc_text}")
                if is_required:
                    required.add(env_name)
        elif variable_cell_text and not env_names:
            # A labeled row that is not an environment variable terminates any
            # active continuation run so later blank rows do not attach to it.
            previous_vars = []
    return descriptions, required


def literal_text(node: ast.AST | None) -> str | None:
    if node is None:
        return None
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        parts: list[str] = []
        for value in node.values:
            if isinstance(value, ast.Constant) and isinstance(value.value, str):
                parts.append(value.value)
            else:
                return None
        return "".join(parts)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left = literal_text(node.left)
        right = literal_text(node.right)
        if left is not None and right is not None:
            return left + right
    return None


def call_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return f"{call_name(node.value)}.{node.attr}"
    return ""


def getenv_names(node: ast.AST) -> set[str]:
    names: set[str] = set()
    for child in ast.walk(node):
        if isinstance(child, ast.Call) and call_name(child.func) in {"os.getenv", "getenv"} and child.args:
            env_name = literal_text(child.args[0])
            if env_name:
                names.add(env_name)
    return names


def parse_argparse_help(feeder_dir: Path) -> dict[str, str]:
    descriptions: dict[str, str] = {}
    for path in feeder_dir.rglob("*.py"):
        if any(part.endswith("_producer") for part in path.parts) or "tests" in path.parts:
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (SyntaxError, UnicodeDecodeError):
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if not call_name(node.func).endswith("add_argument"):
                continue
            env_names = getenv_names(node)
            if not env_names:
                continue
            help_node = next((kw.value for kw in node.keywords if kw.arg == "help"), None)
            help_text = literal_text(help_node)
            if not help_text:
                continue
            description, _ = clean_description(help_text)
            for env_name in env_names:
                descriptions.setdefault(env_name, description)
    return descriptions


def feeder_description_sources(repo_root: Path, slug: str) -> tuple[dict[str, tuple[str, str]], set[str]]:
    feeder_dir = repo_root / "feeders" / slug
    container_descriptions, required_from_docs = parse_markdown_env_table(feeder_dir / "CONTAINER.md")
    readme_descriptions, readme_required = parse_markdown_env_table(feeder_dir / "README.md")
    required_from_docs |= readme_required
    argparse_descriptions = parse_argparse_help(feeder_dir)
    sources: dict[str, tuple[str, str]] = {}
    for env_name, description in container_descriptions.items():
        if not is_generic_description(description, env_name):
            sources.setdefault(env_name, (description, "container"))
    for env_name, description in readme_descriptions.items():
        if not is_generic_description(description, env_name):
            sources.setdefault(env_name, (description, "readme"))
    for env_name, description in argparse_descriptions.items():
        if not is_generic_description(description, env_name):
            sources.setdefault(env_name, (description, "argparse"))
    return sources, required_from_docs


def enrich_env_descriptions(repo_root: Path, catalog: dict[str, Any]) -> dict[str, dict[str, tuple[str, str]]]:
    catalog_existing: dict[tuple[str, str], str] = {}
    mined_by_slug: dict[str, dict[str, tuple[str, str]]] = {}
    for feeder in catalog.get("feeders", []):
        slug = feeder.get("slug")
        if not slug:
            continue
        mined, required_from_docs = feeder_description_sources(repo_root, slug)
        mined_by_slug[slug] = mined
        for env_var in feeder.get("envVars", []):
            env_name = env_var.get("name")
            if not env_name:
                continue
            old_description = str(env_var.get("description") or "")
            if old_description and not is_generic_description(old_description, env_name):
                catalog_existing[(slug, env_name)] = truncate_description(old_description)
            if env_name in required_from_docs:
                env_var["isRequired"] = True
            if env_name in mined:
                env_var["description"] = mined[env_name][0]
                DESCRIPTION_SOURCE_COUNTS[mined[env_name][1]] += 1
            elif env_var.get("isRequired") or env_var.get("isSecret"):
                raise RuntimeError(
                    f"{slug}: required/secret env var {env_name} has no CONTAINER.md, README.md, or argparse help description"
                )
            elif (slug, env_name) in catalog_existing and not env_name.upper().endswith(("API_KEY", "SECURITY_TOKEN", "TOKEN")):
                env_var["description"] = catalog_existing[(slug, env_name)]
                DESCRIPTION_SOURCE_COUNTS["fallback"] += 1
            else:
                env_var["description"] = fallback_description(slug, env_name)
                DESCRIPTION_SOURCE_COUNTS["fallback"] += 1
                message = f"{slug}: no CONTAINER.md/README.md/argparse description for {env_name}; used fallback"
                SOFT_WARNINGS.append(message)
                print(f"warning: {message}", file=sys.stderr)
    return mined_by_slug


def add_env_parameters(parameters: dict[str, Any], feeder: dict[str, Any]) -> None:
    for env_var in feeder.get("envVars", []):
        param: dict[str, Any] = {
            "type": "securestring" if env_var.get("isSecret") else "string",
            "metadata": {"description": env_var.get("description") or fallback_description(feeder["slug"], env_var["name"])},
        }
        default = env_var.get("default")
        if not env_var.get("isRequired"):
            param["defaultValue"] = "" if default is None else str(default)
        parameters[env_var["armParamName"]] = param


def apply_substitutions(template_obj: dict[str, Any], feeder: dict[str, Any], variant: str) -> dict[str, Any]:
    slug = feeder["slug"]
    name_prefix = feeder.get("namePrefix") or slug
    result = recursively_replace_aisstream(copy.deepcopy(template_obj), slug)

    parameters = result.setdefault("parameters", {})
    variables = result.setdefault("variables", {})

    remove_aisstream_parameters(parameters)

    if variant == "mqtt":
        set_parameter_default(parameters, "containerGroupName", f"{slug}-mqtt")
    else:
        set_parameter_default(parameters, "containerGroupName", slug)
    set_parameter_default(parameters, "namePrefix", name_prefix)
    set_parameter_default(parameters, "queueName", feeder.get("queueName") or slug)
    set_parameter_default(parameters, "topicRoot", feeder.get("mqttTopicRoot") or f"{slug}/#")
    set_parameter_default(parameters, "imageName", image_name_for(feeder, variant))

    if variant in {"kafka", "eventhub"}:
        variables["imageName"] = image_name_for(feeder, variant)
    if variant == "eventhub" and "eventHubName" in variables:
        variables["eventHubName"] = feeder.get("eventHubName") or slug
    if variant in {"servicebus", "amqp"} and variables.get("namespaceName") == "[concat(parameters('namePrefix'), '-sb')]":
        variables["namespaceName"] = "[concat(parameters('namePrefix'), '-sbns')]"
    if variant == "eventgrid-mqtt" and "topicSpaceName" in variables:
        variables["topicSpaceName"] = slug

    add_env_parameters(parameters, feeder)

    for env in find_container_environment_arrays(result):
        env[:] = insert_env_vars(remove_aisstream_env_vars(env), feeder)

    return result


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, obj: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(obj, handle, indent=2)
        handle.write("\n")


def output_path(repo_root: Path, relative_path: str, dry_run: bool) -> Path:
    rel = Path(PureWindowsPath(relative_path))
    if dry_run:
        return repo_root / "tools" / ".gen-out" / rel
    return repo_root / rel


def parameter_name_from_ref(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    match = re.fullmatch(r"\[parameters\('([^']+)'\)\]", value)
    return match.group(1) if match else None


def refresh_existing_template_descriptions(
    repo_root: Path,
    generated_targets: set[Path],
    staged_writes: dict[Path, dict[str, Any]],
    filters: set[str] | None,
    references: dict[str, dict[str, Any]] | None = None,
) -> int:
    updated = 0
    source_cache: dict[str, dict[str, tuple[str, str]]] = {}
    references = references or {}
    for path in (repo_root / "feeders").glob("**/azure-template*.json"):
        if path in generated_targets:
            continue
        parts = path.relative_to(repo_root).parts
        if len(parts) < 3 or parts[0] != "feeders":
            continue
        slug = parts[1]
        if filters and slug not in filters:
            continue
        source_cache.setdefault(slug, feeder_description_sources(repo_root, slug)[0])
        descriptions = source_cache[slug]
        try:
            template = load_json(path)
        except json.JSONDecodeError:
            continue
        changed = False
        parameters = template.get("parameters", {})
        for env_array in find_container_environment_arrays(template):
            for item in env_array:
                env_name = item.get("name")
                param_name = parameter_name_from_ref(item.get("value")) or parameter_name_from_ref(item.get("secureValue"))
                if not env_name or not param_name or param_name not in parameters:
                    continue
                if env_name in descriptions:
                    description, source = descriptions[env_name]
                else:
                    description, source = fallback_description(slug, env_name), "fallback"
                    warning = f"{slug}: no CONTAINER.md/README.md/argparse description for {env_name}; used fallback"
                    SOFT_WARNINGS.append(warning)
                    print(f"warning: {warning}", file=sys.stderr)
                metadata = parameters[param_name].setdefault("metadata", {})
                if metadata.get("description") != description:
                    metadata["description"] = description
                    changed = True
                    DESCRIPTION_SOURCE_COUNTS[source] += 1
        # Infrastructure parameters (eventHubSku, queueName) are not driven by
        # CONTAINER.md env-var descriptions; their authoritative description
        # lives in the variant reference template. Sync this whitelist so
        # reference-level description fixes propagate to every feeder on
        # regeneration. Scoped to known-stub infra params to avoid clobbering
        # richer per-param descriptions that already exist downstream.
        try:
            variant = variant_from_template(path.name)
        except ValueError:
            variant = None
        ref_params = references.get(variant, {}).get("parameters", {}) if variant else {}
        for param_name in INFRA_REFERENCE_PARAMS:
            if param_name not in parameters or param_name not in ref_params:
                continue
            ref_desc = ref_params[param_name].get("metadata", {}).get("description")
            if not ref_desc:
                continue
            description = recursively_replace_aisstream(ref_desc, slug)
            metadata = parameters[param_name].setdefault("metadata", {})
            if metadata.get("description") != description:
                metadata["description"] = description
                changed = True
                DESCRIPTION_SOURCE_COUNTS["reference"] += 1
        if changed:
            staged_writes[path] = template
            updated += 1
    return updated


def commit_staged_writes(repo_root: Path, staged_writes: dict[Path, dict[str, Any]], dry_run: bool) -> list[str]:
    written: list[str] = []
    if dry_run:
        for target, obj in staged_writes.items():
            write_json(target, obj)
            written.append(str(target))
        return written

    stage_root = repo_root / "tools" / ".arm-template-stage"
    if stage_root.exists():
        shutil.rmtree(stage_root)
    try:
        for target, obj in staged_writes.items():
            staged_target = stage_root / target.relative_to(repo_root)
            write_json(staged_target, obj)
        for target in staged_writes:
            staged_target = stage_root / target.relative_to(repo_root)
            target.parent.mkdir(parents=True, exist_ok=True)
            staged_target.replace(target)
            written.append(str(target))
    finally:
        if stage_root.exists():
            shutil.rmtree(stage_root)
    return written


def save_catalog(path: Path, catalog: dict[str, Any]) -> None:
    write_json(path, catalog)


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    catalog = load_json(args.catalog)
    filters = {slug.strip() for slug in args.filter.split(",")} if args.filter else None
    enrich_env_descriptions(repo_root, catalog)
    if not args.dry_run:
        save_catalog(args.catalog, catalog)

    references = {variant: load_json(repo_root / rel_path) for variant, rel_path in VARIANT_REFERENCES.items()}
    generated_targets: set[Path] = set()
    staged_writes: dict[Path, dict[str, Any]] = {}

    for feeder in catalog.get("feeders", []):
        if filters and feeder.get("slug") not in filters:
            continue
        for template_path in feeder.get("emptyTemplates", []):
            variant = variant_from_template(template_path)
            generated = apply_substitutions(references[variant], feeder, variant)
            target = output_path(repo_root, template_path, args.dry_run).resolve()
            staged_writes[target] = generated
            generated_targets.add((repo_root / Path(PureWindowsPath(template_path))).resolve())

    existing_updated = 0
    if not args.dry_run:
        existing_updated = refresh_existing_template_descriptions(repo_root, generated_targets, staged_writes, filters, references)

    generated_count = len(generated_targets)
    written = commit_staged_writes(repo_root, staged_writes, args.dry_run)
    for path in written:
        print(path)
    total_descriptions = sum(DESCRIPTION_SOURCE_COUNTS.values())
    print(f"Description sources: total={total_descriptions}, container={DESCRIPTION_SOURCE_COUNTS['container']}, readme={DESCRIPTION_SOURCE_COUNTS['readme']}, argparse={DESCRIPTION_SOURCE_COUNTS['argparse']}, fallback={DESCRIPTION_SOURCE_COUNTS['fallback']}")
    if existing_updated:
        print(f"Updated descriptions in {existing_updated} existing non-catalog template(s).")
    print(f"Generated {generated_count} ARM template(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
