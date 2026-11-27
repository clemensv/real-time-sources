"""Deployment resolution must verify the exact registered source and history."""

import copy
import hashlib
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import pytest
import requests

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "resolve_schema_bindings", ROOT / "tools" / "deploy-fabric" / "resolve_schema_bindings.py")
assert SPEC and SPEC.loader
resolver = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(resolver)

WS, ES, SOURCE, CAPACITY, SCHEMA_SET, HISTORY = (
    "00000000-0000-0000-0000-00000000000" + str(index) for index in range(1, 7)
)
ORIGINAL = "xreg://./schemagroups/example/schemas/Reading/versions/1"
SCHEMA_URL = f"https://test.messagingcatalog.azure.net/schemagroups/{SCHEMA_SET}/schemas/canonical-reading"
SCHEMA = '{"type":"record","name":"Reading","fields":[{"name":"value","type":"double"}]}'


def fixture(encoding="json"):
    selection = {"eventSetWorkspaceId": WS, "eventSetArtifactId": SCHEMA_SET,
                 "eventTypeId": "reading-alias", "schemaVersionId": "2"}
    return {
        "expected": {"reading-alias": {"source_uri": ORIGINAL, "projected_version": "2",
                                      "schema_sha256": hashlib.sha256(SCHEMA.encode()).hexdigest()}},
        "model": {"properties": {"dataSources": [
            {"id": SOURCE, "direction": "Source", "properties": {"eventTypes": [selection]}},
            {"id": HISTORY, "direction": "Destination", "type": "Kusto", "properties": {
                "eventTypes": [copy.deepcopy(selection)],
                "inputSerialization": {"type": "Json" if encoding == "json" else "Avro"},
                "tableCreationMode": "PerCloudEventSchemaVersion",
            }},
        ]}},
        "event_type": {"id": "reading-alias", "schemaUrl": SCHEMA_URL,
                       "envelopeMetadata": {"datacontenttype": {
                           "value": "application/json" if encoding == "json"
                           else "application/vnd.apache.org.avro+avro",
                       }}},
        "versions": [
            {"id": "9", "schemaId": "canonical-reading", "format": "Avro/1.12.0",
             "selfUrl": SCHEMA_URL + "/versions/9$details", "schema": "{}"},
            {"id": "2", "schemaId": "canonical-reading", "format": "Avro/1.12.0",
             "selfUrl": SCHEMA_URL + "/versions/2$details", "schema": SCHEMA},
        ],
    }


def install_session(monkeypatch, data):
    calls = []

    class Session:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def mount(self, *args):
            pass

        def request(self, method, url, **kwargs):
            calls.append((method, url, kwargs))
            status, headers = 200, {}
            if url.startswith(resolver.PUBLIC):
                result = {"id": WS, "capacityId": CAPACITY}
            elif url.startswith("https://api.powerbi.com"):
                status = 307
                headers["Location"] = data.get(
                    "redirect", url.replace("api.powerbi.com", "test.analysis.windows.net"))
                result = {}
            elif "/v1.0/myorg/groups/" in url:
                result = {"id": WS, "capacityId": CAPACITY}
            elif url.endswith("/generatemwctokenv2"):
                result = {"TargetUriHost": data.get("host", "test.analysis.windows.net"),
                          "CapacityObjectId": CAPACITY, "Token": "synthetic-scoped-token"}
            elif url.endswith("/model"):
                result = data["model"]
            elif "/eventtypes/" in url:
                result = data["event_type"]
            elif url.endswith("/schemas/canonical-reading/versions"):
                result = data["versions"]
            else:
                raise AssertionError(f"Unexpected request: {method} {url}")
            assert kwargs["allow_redirects"] is False
            return SimpleNamespace(
                status_code=status, headers=headers,
                raise_for_status=lambda: None, json=lambda: result,
            )

    monkeypatch.setattr(resolver.requests, "Session", Session)
    return calls


def resolve(data, encoding="json"):
    return resolver.lookup_dataschema_overrides(
        WS, ES, SOURCE, data["expected"], lambda audience: "synthetic-approved-token",
        payload_encoding=encoding,
    )


@pytest.mark.parametrize("encoding", ["json", "avro"])
def test_pinned_resolution_preserves_inputs_without_broker_or_mutation_calls(monkeypatch, encoding):
    data = fixture(encoding)
    before = copy.deepcopy(data)
    calls = install_session(monkeypatch, data)
    assert resolve(data, encoding) == {ORIGINAL: SCHEMA_URL + "/versions/2"}
    assert data == before
    assert not any("/connection" in url for _, url, _ in calls)
    assert all(method == "GET" or url.endswith("/generatemwctokenv2") for method, url, _ in calls)


@pytest.mark.parametrize("failure", [
    "missing", "duplicate", "version", "fingerprint", "self-url", "host",
    "decoder", "metadata", "missing-history", "untyped", "history-version",
    "history-workspace", "history-schema-set", "cross-workspace",
])
def test_rejects_unqualified_registration_or_history(monkeypatch, failure):
    data = fixture()
    source = data["model"]["properties"]["dataSources"][0]["properties"]["eventTypes"]
    history = data["model"]["properties"]["dataSources"][1]["properties"]
    if failure == "missing":
        source.clear()
    elif failure == "duplicate":
        source.append(copy.deepcopy(source[0]))
    elif failure == "version":
        source[0]["schemaVersionId"] = "9"
    elif failure == "fingerprint":
        data["versions"][1]["schema"] = "{}"
    elif failure == "self-url":
        data["versions"][1]["selfUrl"] = SCHEMA_URL + "/versions/9$details"
    elif failure == "host":
        data["host"] = "evil.example?target=.analysis.windows.net"
    elif failure == "decoder":
        history["inputSerialization"]["type"] = "Avro"
    elif failure == "metadata":
        data["event_type"]["envelopeMetadata"]["datacontenttype"]["value"] = "application/octet-stream"
    elif failure == "missing-history":
        history["eventTypes"] = []
    elif failure == "untyped":
        history["tableCreationMode"] = "SingleTable"
    elif failure.startswith("history-"):
        key = {"history-version": "schemaVersionId", "history-workspace": "eventSetWorkspaceId",
               "history-schema-set": "eventSetArtifactId"}[failure]
        history["eventTypes"][0][key] = "different"
    else:
        source[0]["eventSetWorkspaceId"] = HISTORY
        history["eventTypes"][0]["eventSetWorkspaceId"] = HISTORY
    install_session(monkeypatch, data)
    with pytest.raises(RuntimeError):
        resolve(data)


@pytest.mark.parametrize("redirect", [
    "http://test.analysis.windows.net",
    "https://user:secret@test.analysis.windows.net",
    "https://test.analysis.windows.net:444",
    "https://evil.example",
])
def test_redirect_validation_does_not_forward_credentials(monkeypatch, redirect):
    data = fixture()
    data["redirect"] = redirect + f"/v1.0/myorg/groups/{WS}?preferClientRouting=true"
    calls = install_session(monkeypatch, data)
    with pytest.raises(RuntimeError, match="routing origin"):
        resolve(data)
    assert len(calls) == 2


def test_invalid_expected_bindings_fail_before_network(monkeypatch):
    data = fixture()
    data["expected"]["reading-alias"]["schema_sha256"] = "not-a-fingerprint"
    calls = install_session(monkeypatch, data)
    with pytest.raises(ValueError, match="fingerprints"):
        resolve(data)
    assert not calls


def test_network_denial_is_not_an_empty_success(monkeypatch):
    def denied(*args, **kwargs):
        raise requests.HTTPError("synthetic forbidden")

    monkeypatch.setattr(resolver.requests.Session, "request", denied)
    with pytest.raises(requests.HTTPError, match="forbidden"):
        resolve(fixture())


def test_cli_profile_is_explicit_and_token_not_printed(monkeypatch, capsys):
    seen = []
    monkeypatch.setattr(resolver.shutil, "which", lambda name: name)

    def run(command, **kwargs):
        seen.append(command)
        assert kwargs["check"] and kwargs["capture_output"]
        return SimpleNamespace(stdout="synthetic-token\n")

    monkeypatch.setattr(resolver.subprocess, "run", run)
    assert resolver.azure_cli_token("az_m", resolver.PBI_AUDIENCE) == "synthetic-token"
    assert seen[0][0] == "az_m"
    assert capsys.readouterr().out == ""


@pytest.mark.parametrize("profile,config", [("az_m", ".azure"), ("az_b", ".azure-secondary")])
def test_missing_shim_uses_process_local_config_without_changing_account(monkeypatch, profile, config):
    monkeypatch.setattr(resolver.shutil, "which", lambda name: "az" if name == "az" else None)
    calls = []
    before = dict(resolver.os.environ)

    def run(command, **kwargs):
        calls.append((command, kwargs["env"]))
        return SimpleNamespace(stdout="synthetic-token\n")

    monkeypatch.setattr(resolver.subprocess, "run", run)
    assert resolver.azure_cli_token(profile, resolver.PBI_AUDIENCE) == "synthetic-token"
    assert calls[0][0][:3] == ["az", "account", "get-access-token"]
    assert calls[0][1]["AZURE_CONFIG_DIR"] == str(Path.home() / config)
    assert dict(resolver.os.environ) == before
