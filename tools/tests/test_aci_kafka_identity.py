import importlib.util
import json
from pathlib import Path


SPEC = importlib.util.spec_from_file_location(
    "aci_kafka_identity", Path(__file__).parents[1] / "aci_kafka_identity.py"
)
assert SPEC is not None and SPEC.loader is not None
identity = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(identity)


def test_eventhub_conversion_is_idempotent_and_preserves_state_identity():
    root = Path(__file__).parents[2]
    source = json.loads((root / "feeders" / "usgs-waterdata" / "azure-template-with-eventhub.json").read_text())
    namespace = next(r for r in source["resources"] if r["type"] == "Microsoft.EventHub/namespaces")
    namespace["properties"]["disableLocalAuth"] = False
    source["resources"].append({"type": "Microsoft.EventHub/namespaces/eventhubs/authorizationRules",
                                "name": "synthetic/send"})
    original_group = next(r for r in source["resources"] if r["type"] == "Microsoft.ContainerInstance/containerGroups")
    original_group["properties"]["containers"][0]["properties"]["environmentVariables"].append(
        {"name": "CONNECTION_STRING", "secureValue": "synthetic-sas-binding"})
    converted = identity.configure(source)
    assert identity.configure(converted) == converted
    namespaces = [r for r in converted["resources"] if r["type"] == "Microsoft.EventHub/namespaces"]
    assert namespaces[0]["properties"]["disableLocalAuth"] is True
    assert not any("authorizationRules" in r["type"] for r in converted["resources"])
    group = next(r for r in converted["resources"] if r["type"] == "Microsoft.ContainerInstance/containerGroups")
    before = next(r for r in source["resources"] if r["type"] == group["type"])
    assert set(before["identity"]["userAssignedIdentities"]) <= set(group["identity"]["userAssignedIdentities"])
    env = {v["name"]: v for v in group["properties"]["containers"][0]["properties"]["environmentVariables"]}
    assert "CONNECTION_STRING" not in env
    assert env["KAFKA_AUTH_MODE"]["value"] == "azure-entra"
    assert "STATE_AZURE_FILES_CLIENT_ID" in env
    assert namespace["properties"]["disableLocalAuth"] is False
