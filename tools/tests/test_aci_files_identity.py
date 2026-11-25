import copy
import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("aci_files_identity", ROOT / "tools" / "aci_files_identity.py")
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
TEMPLATES = [
    path
    for slug in ("usgs-waterdata", "usgs-iv", "usgs-nwis-wq")
    for path in sorted((ROOT / "feeders" / slug).rglob("azure-template*.json"))
]


@pytest.mark.parametrize("path", TEMPLATES, ids=lambda path: str(path.relative_to(ROOT)))
def test_keyless_state_preserves_mounts_and_transport_configuration(path):
    template = json.loads(path.read_text(encoding="utf-8"))
    assert MODULE.configure(template) == template
    for resource in template["resources"]:
        if resource["type"] == "Microsoft.ContainerInstance/containerGroups":
            for volume in resource["properties"]["volumes"]:
                if "azureFile" in volume:
                    volume["azureFile"]["storageAccountKey"] = "[listKeys('synthetic-state', '2023-05-01').keys[0].value]"
                    volume["azureFile"]["storageAccountKeyReference"] = "synthetic-key-reference"
    original = copy.deepcopy(template)
    result = MODULE.configure(template)
    assert template == original
    assert MODULE.configure(result) == result
    store = next(r for r in result["resources"] if r["type"] == "Microsoft.Storage/storageAccounts")
    assert store["properties"]["allowSharedKeyAccess"] is False
    assert store["properties"]["azureFilesIdentityBasedAuthentication"]["smbOAuthSettings"]["isSmbOAuthEnabled"] is True
    assert store["apiVersion"] == "2025-08-01"
    service = next(r for r in result["resources"] if r["type"] == "Microsoft.Storage/storageAccounts/fileServices")
    assert service["properties"]["protocolSettings"]["smb"]["authenticationMethods"] == "Kerberos"
    share = next(r for r in result["resources"] if r["type"] == "Microsoft.Storage/storageAccounts/fileServices/shares")
    assert "[resourceId('Microsoft.Storage/storageAccounts/fileServices', variables('storageAccountName'), 'default')]" in share["dependsOn"]
    old_group = next(r for r in original["resources"] if r["type"] == "Microsoft.ContainerInstance/containerGroups")
    group = next(r for r in result["resources"] if r["type"] == "Microsoft.ContainerInstance/containerGroups")
    assert group["apiVersion"] == "2026-07-01"
    assert group["properties"] == {
        **old_group["properties"],
        "volumes": [
            {**volume, "azureFile": {
                **{k: v for k, v in volume["azureFile"].items()
                   if k not in ("storageAccountKey", "storageAccountKeyReference", "userAssignedIdentityClientId")},
                "userManagedIdentityClientId": MODULE.CLIENT_ID,
            }} if "azureFile" in volume else volume
            for volume in old_group["properties"]["volumes"]
        ],
    }
    old_identities = old_group.get("identity", {}).get("userAssignedIdentities", {})
    assert old_identities.items() <= group["identity"]["userAssignedIdentities"].items()
    assert MODULE.IDENTITY_ID in group["identity"]["userAssignedIdentities"]
    assert MODULE.ROLE_ID in group["dependsOn"]
    assert "storageAccountKey" not in json.dumps(result)
    role = next(r for r in result["resources"] if r["type"] == "Microsoft.Authorization/roleAssignments" and r["name"] == MODULE.ROLE_NAME)
    assert role["scope"] == MODULE.STORAGE_ID
    assert MODULE.SMB_MI_ADMIN_ROLE in role["properties"]["roleDefinitionId"]
    assert role["dependsOn"] == [MODULE.STORAGE_ID, MODULE.IDENTITY_ID]


@pytest.mark.parametrize("failure", ("no-storage", "conditional-storage", "foreign-volume", "no-volume", "windows"))
def test_unsupported_topology_fails_without_modifying_input(failure):
    template = json.loads(TEMPLATES[0].read_text(encoding="utf-8"))
    store = next(r for r in template["resources"] if r["type"] == "Microsoft.Storage/storageAccounts")
    group = next(r for r in template["resources"] if r["type"] == "Microsoft.ContainerInstance/containerGroups")
    if failure == "no-storage":
        template["resources"].remove(store)
    elif failure == "conditional-storage":
        store["condition"] = "[parameters('createState')]"
    elif failure == "foreign-volume":
        group["properties"]["volumes"][0]["azureFile"]["storageAccountName"] = "other-account"
    elif failure == "no-volume":
        group["properties"]["volumes"] = []
    else:
        group["properties"]["osType"] = "Windows"
    original = copy.deepcopy(template)
    with pytest.raises(ValueError):
        MODULE.configure(template)
    assert template == original
