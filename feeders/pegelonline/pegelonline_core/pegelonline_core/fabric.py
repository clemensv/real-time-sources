"""Read registered schema identities without changing a Fabric pipeline."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable, Mapping
from typing import TypedDict
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


def lookup_dataschema_overrides(
    workspace_id: str,
    eventstream_id: str,
    source_id: str,
    expected: Mapping[str, SchemaBinding],
    get_token: Callable[[str], str],
    *,
    payload_encoding: str | None = None,
) -> dict[str, str]:
    """Resolve the selected versions and verify their projection fingerprints.

    The caller supplies its approved credential flow. Provider-specific metadata
    APIs are required here; connection strings still use the public Topology API.
    """
    if payload_encoding not in (None, "json", "avro"):
        raise ValueError("Payload encoding must be json or avro")
    workspace_id = str(UUID(workspace_id))
    eventstream_id = str(UUID(eventstream_id))
    source_id = str(UUID(source_id))
    if not expected or any(not item["source_uri"].startswith("xreg://./") for item in expected.values()):
        raise ValueError("Expected bindings must identify original file-backed dataschema URIs")
    with requests.Session() as session:
        retry = Retry(total=3, backoff_factor=0.5, status_forcelist=(429, 500, 502, 503, 504))
        session.mount("https://", HTTPAdapter(max_retries=retry))

        def request(method, url, *, headers=None, body=None):
            response = session.request(
                method, url, headers=headers or {"Authorization": "Bearer " + get_token(PBI_AUDIENCE)},
                json=body, timeout=30, allow_redirects=False,
            )
            response.raise_for_status()
            return response

        workspace = request("GET", PUBLIC + f"/workspaces/{workspace_id}").json()
        capacity = str(UUID(workspace["capacityId"]))
        route_path = f"/v1.0/myorg/groups/{workspace_id}?preferClientRouting=true"
        origin = "https://api.powerbi.com"
        for _ in range(5):
            response = request("GET", origin + route_path)
            if response.status_code not in (301, 302, 307, 308):
                routed = response.json()
                if routed["id"].lower() != workspace_id or routed["capacityId"].lower() != capacity:
                    raise RuntimeError("Fabric workspace routing identity mismatch")
                break
            redirect = urlparse(response.headers["Location"])
            if (redirect.scheme != "https" or not redirect.hostname
                    or not redirect.hostname.endswith(".analysis.windows.net")
                    or redirect.path + "?" + redirect.query != route_path):
                raise RuntimeError("Unexpected Fabric workspace routing origin")
            origin = f"https://{redirect.netloc}"
        else:
            raise RuntimeError("Fabric workspace routing exceeded redirect limit")

        def scoped(artifact_id, owner_workspace, workload, artifact_type):
            token = request("POST", origin + "/metadata/v201606/generatemwctokenv2", body={
                "workspaceObjectId": owner_workspace, "workloadType": workload,
                "artifacts": [{"artifactType": artifact_type, "artifactObjectId": artifact_id}],
            }).json()
            host = token["TargetUriHost"]
            parsed_host = urlparse("https://" + host)
            if (token["CapacityObjectId"].lower() != capacity or "/" in host
                    or parsed_host.hostname != host
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
        sources = [node for node in model["properties"]["dataSources"]
                   if node["id"].lower() == source_id and node.get("direction") == "Source"]
        if len(sources) != 1:
            raise RuntimeError("Expected exactly one selected source in Eventstream metadata")
        selections = sources[0]["properties"].get("eventTypes") or []
        if len(selections) != len(expected) or {item["eventTypeId"] for item in selections} != set(expected):
            raise RuntimeError("Source registered event types do not match the producer contracts")
        if payload_encoding is not None:
            history_types = set()
            for node in model["properties"]["dataSources"]:
                if node.get("type") != "Kusto" or node.get("direction") != "Destination":
                    continue
                properties = node["properties"]
                selected_types = {
                    item["eventTypeId"] for item in properties.get("eventTypes", [])
                } & set(expected)
                if not selected_types:
                    continue
                serialization = properties.get("inputSerialization", {}).get("type")
                if serialization != ("Json" if payload_encoding == "json" else "Avro"):
                    raise RuntimeError("History serialization does not match the selected payload encoding")
                if properties.get("tableCreationMode") != "PerCloudEventSchemaVersion":
                    raise RuntimeError("Selected history destination must own per-schema typed tables")
                history_types.update(selected_types)
            if history_types != set(expected):
                raise RuntimeError("Every selected family requires a qualified typed history destination")
        result = {}
        schema_sets = {}
        for selection in selections:
            event_type_id = selection["eventTypeId"]
            binding = expected[event_type_id]
            if selection["schemaVersionId"] != binding["projected_version"]:
                raise RuntimeError(f"Unqualified selected projection version for {event_type_id}")
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
            if payload_encoding is not None:
                content_type = event_type.get("envelopeMetadata", {}).get(
                    "datacontenttype", {}).get("value", "")
                media_type = content_type.split(";", 1)[0].strip().lower()
                matches_encoding = (
                    media_type == "application/json" or media_type.endswith("+json")
                    if payload_encoding == "json"
                    else media_type in ("application/vnd.apache.avro+avro", "avro/binary")
                )
                if not matches_encoding:
                    raise RuntimeError("Registered content type does not match the selected payload encoding")
            schema_url = event_type["schemaUrl"]
            parsed = urlparse(schema_url)
            prefix = f"/schemagroups/{artifact_id}/schemas/"
            if (parsed.scheme != "https" or not parsed.hostname
                    or not parsed.hostname.endswith(".messagingcatalog.azure.net")
                    or not parsed.path.startswith(prefix) or parsed.query or parsed.fragment):
                raise RuntimeError("Registered schema URL is not a canonical catalog schema identity")
            schema_id = unquote(parsed.path[len(prefix):])
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
