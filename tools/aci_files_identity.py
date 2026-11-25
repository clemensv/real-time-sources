"""Convert canonical ACI state volumes to Azure Files SMB managed identity."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any


IDENTITY_API = "2023-01-31"
CONTAINER_API = "2026-07-01"
STORAGE_API = "2025-08-01"
SMB_MI_ADMIN_ROLE = "a235d3ee-5935-4cfb-8cc5-a3303ad5995e"
STORAGE_ID = "[resourceId('Microsoft.Storage/storageAccounts', variables('storageAccountName'))]"
IDENTITY_ID = "[resourceId('Microsoft.ManagedIdentity/userAssignedIdentities', variables('stateIdentityName'))]"
ROLE_NAME = "[guid(variables('storageAccountName'), variables('stateIdentityName'), 'files-smb-mi-admin')]"
ROLE_ID = (
    "[extensionResourceId(resourceId('Microsoft.Storage/storageAccounts', variables('storageAccountName')), "
    "'Microsoft.Authorization/roleAssignments', "
    "guid(variables('storageAccountName'), variables('stateIdentityName'), 'files-smb-mi-admin'))]"
)
CLIENT_ID = (
    "[reference(resourceId('Microsoft.ManagedIdentity/userAssignedIdentities', "
    "variables('stateIdentityName')), '2023-01-31').clientId]"
)


def configure(template: dict[str, Any]) -> dict[str, Any]:
    """Preserve canonical mounts and checkpoint paths without a storage key."""
    result = copy.deepcopy(template)
    resources = result["resources"]
    stores = [r for r in resources if r["type"] == "Microsoft.Storage/storageAccounts"]
    groups = [r for r in resources if r["type"] == "Microsoft.ContainerInstance/containerGroups"]
    if len(stores) != 1 or not groups:
        raise ValueError("Expected one dedicated state storage account and at least one ACI group")
    store = stores[0]
    if store["name"] != "[variables('storageAccountName')]" or store.get("condition") is not None:
        raise ValueError("Only unconditional canonical state storage accounts are supported")
    volumes = [
        volume["azureFile"]
        for group in groups
        for volume in group["properties"].get("volumes", [])
        if "azureFile" in volume
    ]
    if not volumes or any(v["storageAccountName"] != "[variables('storageAccountName')]" for v in volumes):
        raise ValueError("Expected Azure Files volumes referencing the canonical state account")

    properties = store.setdefault("properties", {})
    properties["allowSharedKeyAccess"] = False
    properties["allowBlobPublicAccess"] = False
    properties["supportsHttpsTrafficOnly"] = True
    properties["minimumTlsVersion"] = "TLS1_2"
    authentication = properties.setdefault("azureFilesIdentityBasedAuthentication", {})
    authentication.setdefault("directoryServiceOptions", "None")
    authentication["smbOAuthSettings"] = {"isSmbOAuthEnabled": True}
    store["apiVersion"] = STORAGE_API
    services = [r for r in resources if r["type"] == "Microsoft.Storage/storageAccounts/fileServices"]
    if services:
        if len(services) != 1 or services[0]["name"] != "[concat(variables('storageAccountName'), '/default')]":
            raise ValueError("Expected the canonical default file service")
        service = services[0]
    else:
        service = {
            "type": "Microsoft.Storage/storageAccounts/fileServices",
            "apiVersion": STORAGE_API,
            "name": "[concat(variables('storageAccountName'), '/default')]",
            "dependsOn": [STORAGE_ID],
            "properties": {},
        }
        resources.append(service)
    service["apiVersion"] = STORAGE_API
    service.setdefault("properties", {}).setdefault("protocolSettings", {}).setdefault("smb", {})[
        "authenticationMethods"
    ] = "Kerberos"
    service_id = "[resourceId('Microsoft.Storage/storageAccounts/fileServices', variables('storageAccountName'), 'default')]"
    for resource in resources:
        if resource["type"] == "Microsoft.Storage/storageAccounts/fileServices/shares":
            dependencies = resource.setdefault("dependsOn", [])
            if service_id not in dependencies:
                dependencies.append(service_id)
    result.setdefault("variables", {})["stateIdentityName"] = "[concat(variables('storageAccountName'), '-files-mi')]"
    identity = {
        "type": "Microsoft.ManagedIdentity/userAssignedIdentities",
        "apiVersion": IDENTITY_API,
        "name": "[variables('stateIdentityName')]",
        "location": store["location"],
    }
    role = {
        "type": "Microsoft.Authorization/roleAssignments",
        "apiVersion": "2022-04-01",
        "name": ROLE_NAME,
        "scope": STORAGE_ID,
        "dependsOn": [STORAGE_ID, IDENTITY_ID],
        "properties": {
            "roleDefinitionId": f"[subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '{SMB_MI_ADMIN_ROLE}')]",
            "principalId": (
                "[reference(resourceId('Microsoft.ManagedIdentity/userAssignedIdentities', "
                "variables('stateIdentityName')), '2023-01-31').principalId]"
            ),
            "principalType": "ServicePrincipal",
        },
    }
    for resource in (identity, role):
        matches = [r for r in resources if r["type"] == resource["type"] and r["name"] == resource["name"]]
        if not matches:
            resources.append(resource)
        elif len(matches) != 1 or matches[0] != resource:
            raise ValueError(f"Conflicting state resource: {resource['type']}")
    for group in groups:
        if group["properties"].get("osType") != "Linux":
            raise ValueError("The ACI Azure Files mount requires Linux containers")
        group["apiVersion"] = CONTAINER_API
        group_identity = group.setdefault("identity", {"type": "UserAssigned"})
        identity_types = {part.strip() for part in group_identity["type"].split(",")} - {"None"}
        identity_types.add("UserAssigned")
        group_identity["type"] = ", ".join(sorted(identity_types))
        group_identity.setdefault("userAssignedIdentities", {})[IDENTITY_ID] = {}
        dependencies = group.setdefault("dependsOn", [])
        for dependency in (IDENTITY_ID, ROLE_ID):
            if dependency not in dependencies:
                dependencies.append(dependency)
    for volume in volumes:
        volume.pop("storageAccountKey", None)
        volume.pop("storageAccountKeyReference", None)
        volume.pop("userAssignedIdentityClientId", None)
        volume["userManagedIdentityClientId"] = CLIENT_ID
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("templates", nargs="+", type=Path)
    args = parser.parse_args()
    staged = [(path, configure(json.loads(path.read_text(encoding="utf-8-sig")))) for path in args.templates]
    for path, template in staged:
        path.write_text(json.dumps(template, indent=2) + "\n", encoding="utf-8")
        print(f"Configured managed-identity state: {path}")


if __name__ == "__main__":
    main()
