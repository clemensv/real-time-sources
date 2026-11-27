#!/usr/bin/env python3
"""Resolve pinned Fabric schema URLs for deployment, without changing the pipeline."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any, TypedDict
from urllib.parse import quote, unquote, urlparse
from uuid import UUID

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

PUBLIC = "https://api.fabric.microsoft.com/v1"
PBI_AUDIENCE = "https://analysis.windows.net/powerbi/api"


class SchemaBinding(TypedDict):
    source_uri: str
    projected_version: str
    schema_sha256: str


def validate_bindings(expected: Mapping[str, SchemaBinding]) -> None:
    if not expected:
        raise ValueError("Expected at least one selected event type")
    for event_type, binding in expected.items():
        if not isinstance(event_type, str) or not event_type:
            raise ValueError("Expected nonempty event type identities")
        if not isinstance(binding, Mapping):
            raise ValueError("Expected schema binding objects")
        source = binding.get("source_uri")
        version = binding.get("projected_version")
        fingerprint = binding.get("schema_sha256")
        if not isinstance(source, str) or not source.startswith("xreg://./"):
            raise ValueError("Expected original file-backed xreg schema URIs")
        if not isinstance(version, str) or not version:
            raise ValueError("Expected explicit projection versions")
        if not isinstance(fingerprint, str) or not re.fullmatch(r"[0-9a-f]{64}", fingerprint):
            raise ValueError("Expected lowercase SHA-256 projection fingerprints")


def lookup_dataschema_overrides(
    workspace_id: str,
    eventstream_id: str,
    source_id: str,
    expected: Mapping[str, SchemaBinding],
    get_token: Callable[[str], str],
    *,
    payload_encoding: str,
) -> dict[str, str]:
    """Read provider metadata with the caller's approved credential flow.

    Scoped metadata tokens are used only for schema readback, never to discover
    broker connection strings. Cross-workspace schema sets are not qualified.
    """
    if payload_encoding not in ("json", "avro"):
        raise ValueError("Payload encoding must be json or avro")
    validate_bindings(expected)
    workspace_id, eventstream_id, source_id = (
        str(UUID(value)) for value in (workspace_id, eventstream_id, source_id)
    )
    with requests.Session() as session:
        retry = Retry(total=3, backoff_factor=0.5, status_forcelist=(429, 500, 502, 503, 504))
        session.mount("https://", HTTPAdapter(max_retries=retry))

        def request(
            method: str, url: str, *, headers: dict[str, str] | None = None,
            body: dict[str, Any] | None = None,
        ) -> requests.Response:
            response = session.request(
                method, url,
                headers=headers or {"Authorization": "Bearer " + get_token(PBI_AUDIENCE)},
                json=body, timeout=30, allow_redirects=False,
            )
            response.raise_for_status()
            return response

        workspace = request("GET", PUBLIC + f"/workspaces/{workspace_id}").json()
        if str(UUID(workspace["id"])) != workspace_id:
            raise RuntimeError("Fabric workspace identity mismatch")
        capacity = str(UUID(workspace["capacityId"]))
        route_path = f"/v1.0/myorg/groups/{workspace_id}?preferClientRouting=true"
        origin = "https://api.powerbi.com"
        for _ in range(5):
            response = request("GET", origin + route_path)
            if response.status_code not in (301, 302, 307, 308):
                routed = response.json()
                if (str(UUID(routed["id"])) != workspace_id
                        or str(UUID(routed["capacityId"])) != capacity):
                    raise RuntimeError("Fabric workspace routing identity mismatch")
                break
            redirect = urlparse(response.headers["Location"])
            if (redirect.scheme != "https" or not redirect.hostname
                    or not redirect.hostname.endswith(".analysis.windows.net")
                    or redirect.username or redirect.password or redirect.port not in (None, 443)
                    or redirect.fragment or redirect.path + "?" + redirect.query != route_path):
                raise RuntimeError("Unexpected Fabric workspace routing origin")
            origin = f"https://{redirect.netloc}"
        else:
            raise RuntimeError("Fabric workspace routing exceeded redirect limit")

        def scoped(
            artifact_id: str, owner_workspace: str, workload: str, artifact_type: str,
        ) -> tuple[str, dict[str, str]]:
            token = request("POST", origin + "/metadata/v201606/generatemwctokenv2", body={
                "workspaceObjectId": owner_workspace, "workloadType": workload,
                "artifacts": [{"artifactType": artifact_type, "artifactObjectId": artifact_id}],
            }).json()
            host = token["TargetUriHost"]
            parsed_host = urlparse("https://" + host)
            if (str(UUID(token["CapacityObjectId"])) != capacity
                    or parsed_host.hostname != host or parsed_host.netloc != host
                    or parsed_host.path or parsed_host.query or parsed_host.fragment
                    or not host.endswith((".analysis.windows.net", ".pbidedicated.windows.net"))):
                raise RuntimeError("Unexpected Fabric scoped metadata host or capacity")
            prefix = f"https://{host}/webapi/capacities/{capacity}/workloads"
            if workload == "ES":
                base = f"{prefix}/ES/ESService/Direct/v2/workspaces/{owner_workspace}/artifacts/{artifact_id}"
            else:
                base = (f"{prefix}/OneRiver/OneRiverService/automatic/eventdefinitions/v1/"
                        f"workspaces/{owner_workspace}/artifacts/{artifact_id}")
            return base, {"Authorization": "MwcToken " + token["Token"],
                          "x-ms-workload-resource-moniker": artifact_id}

        base, headers = scoped(eventstream_id, workspace_id, "ES", "EventStream")
        model = request("GET", base + "/model", headers=headers).json()
        nodes = model["properties"]["dataSources"]
        sources = [node for node in nodes
                   if node["id"].lower() == source_id and node.get("direction") == "Source"]
        if len(sources) != 1:
            raise RuntimeError("Expected exactly one selected source in Eventstream metadata")
        selections = sources[0]["properties"].get("eventTypes") or []
        if len(selections) != len(expected) or {item["eventTypeId"] for item in selections} != set(expected):
            raise RuntimeError("Source registered event types do not match the producer contracts")
        selected = {item["eventTypeId"]: item for item in selections}
        for event_type, binding in expected.items():
            if selected[event_type]["schemaVersionId"] != binding["projected_version"]:
                raise RuntimeError(f"Unqualified selected projection version for {event_type}")

        history_types: set[str] = set()
        for node in nodes:
            if node.get("type") != "Kusto" or node.get("direction") != "Destination":
                continue
            properties = node["properties"]
            history = properties.get("eventTypes", [])
            selected_types = {item["eventTypeId"] for item in history} & set(expected)
            if not selected_types:
                continue
            if properties.get("inputSerialization", {}).get("type") != (
                "Json" if payload_encoding == "json" else "Avro"
            ):
                raise RuntimeError("History serialization does not match the selected payload encoding")
            if properties.get("tableCreationMode") != "PerCloudEventSchemaVersion":
                raise RuntimeError("Selected history destination must own per-schema typed tables")
            for item in history:
                if item["eventTypeId"] not in selected_types:
                    continue
                source_selection = selected[item["eventTypeId"]]
                for key in ("eventSetWorkspaceId", "eventSetArtifactId", "schemaVersionId"):
                    if item.get(key) != source_selection[key]:
                        raise RuntimeError("History registered selection differs from the source")
            history_types.update(selected_types)
        if history_types != set(expected):
            raise RuntimeError("Every selected family requires a qualified typed history destination")

        result: dict[str, str] = {}
        schema_sets: dict[str, tuple[str, dict[str, str]]] = {}
        for selection in selections:
            event_type_id = selection["eventTypeId"]
            binding = expected[event_type_id]
            owner_workspace = str(UUID(selection["eventSetWorkspaceId"]))
            artifact_id = str(UUID(selection["eventSetArtifactId"]))
            if owner_workspace != workspace_id:
                raise RuntimeError("Cross-workspace schema sets require separate routing qualification")
            if artifact_id not in schema_sets:
                schema_sets[artifact_id] = scoped(artifact_id, owner_workspace, "OneRiver", "EventDefinition")
            catalog, catalog_headers = schema_sets[artifact_id]
            event_type = request(
                "GET", catalog + "/eventtypes/" + quote(event_type_id, safe=""),
                headers=catalog_headers,
            ).json()
            if event_type["id"] != event_type_id:
                raise RuntimeError("Registered event type identity mismatch")
            content_type = event_type.get("envelopeMetadata", {}).get(
                "datacontenttype", {}).get("value", "")
            media_type = content_type.split(";", 1)[0].strip().lower()
            matches_encoding = (
                media_type == "application/json" or media_type.endswith("+json")
                if payload_encoding == "json" else media_type in (
                    "application/vnd.apache.avro+avro",
                    "application/vnd.apache.org.avro+avro", "avro/binary",
                )
            )
            if not matches_encoding:
                raise RuntimeError("Registered content type does not match the selected payload encoding")
            schema_url = event_type["schemaUrl"]
            parsed = urlparse(schema_url)
            prefix = f"/schemagroups/{artifact_id}/schemas/"
            if (parsed.scheme != "https" or not parsed.hostname
                    or not parsed.hostname.endswith(".messagingcatalog.azure.net")
                    or parsed.username or parsed.password or parsed.port not in (None, 443)
                    or not parsed.path.startswith(prefix) or parsed.query or parsed.fragment):
                raise RuntimeError("Registered schema URL is not a canonical catalog schema identity")
            schema_id = unquote(parsed.path[len(prefix):])
            if not schema_id or "/" in schema_id:
                raise RuntimeError("Registered schema URL must identify exactly one schema")
            versions = request(
                "GET", catalog + "/schemas/" + quote(schema_id, safe="") + "/versions",
                headers=catalog_headers,
            ).json()
            matches = [version for version in versions if version["id"] == selection["schemaVersionId"]]
            if len(matches) != 1:
                raise RuntimeError("Expected exactly one pinned registered schema version")
            version = matches[0]
            if version["schemaId"] != schema_id or version["format"] != "Avro/1.12.0":
                raise RuntimeError("Selected registered schema identity or format mismatch")
            schema = json.dumps(json.loads(version["schema"]), ensure_ascii=True, separators=(",", ":"))
            if hashlib.sha256(schema.encode()).hexdigest() != binding["schema_sha256"]:
                raise RuntimeError(f"Registered projection fingerprint mismatch for {event_type_id}")
            uri = version["selfUrl"].removesuffix("$details")
            if uri != schema_url + "/versions/" + quote(version["id"], safe=""):
                raise RuntimeError("Registered version self URL does not match the event type schema URL")
            if binding["source_uri"] in result and result[binding["source_uri"]] != uri:
                raise RuntimeError("One original schema identity resolves to conflicting registered versions")
            result[binding["source_uri"]] = uri
        return result


def azure_cli_token(profile: str, audience: str) -> str:
    if profile not in ("az_m", "az_b"):
        raise ValueError("Select the az_m or az_b Azure profile")
    environment = os.environ.copy()
    launcher = shutil.which(profile)
    if launcher is None:
        launcher = shutil.which("az")
        if launcher is None:
            raise RuntimeError("Azure CLI is not installed")
        environment["AZURE_CONFIG_DIR"] = str(
            Path.home() / (".azure" if profile == "az_m" else ".azure-secondary")
        )
    completed = subprocess.run(
        [launcher, "account", "get-access-token", "--resource", audience,
         "--query", "accessToken", "--output", "tsv"],
        check=True, capture_output=True, text=True, timeout=60, env=environment,
    )
    token = completed.stdout.strip()
    if not token:
        raise RuntimeError("Azure CLI returned no access token")
    return token


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-id", required=True)
    parser.add_argument("--eventstream-id", required=True)
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--expected-bindings", required=True, type=Path)
    parser.add_argument("--payload-encoding", required=True, choices=("json", "avro"))
    parser.add_argument("--azure-profile", required=True, choices=("az_m", "az_b"))
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    root = Path(__file__).resolve().parents[2]
    if output.is_relative_to(root) or output == args.expected_bindings.resolve():
        parser.error("Write resolved deployment bindings outside the checkout, distinct from the input")
    try:
        expected = json.loads(args.expected_bindings.read_text(encoding="utf-8-sig"))
        if not isinstance(expected, dict):
            raise ValueError("Expected an event-type-keyed schema binding object")
        result = lookup_dataschema_overrides(
            args.workspace_id, args.eventstream_id, args.source_id, expected,
            lambda audience: azure_cli_token(args.azure_profile, audience),
            payload_encoding=args.payload_encoding,
        )
        output.write_text(json.dumps(result, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    except (ValueError, KeyError, TypeError, OSError, RuntimeError,
            requests.RequestException, subprocess.SubprocessError) as error:
        parser.exit(1, f"Schema binding resolution failed: {error}\n")


if __name__ == "__main__":
    main()
