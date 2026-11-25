"""Configure canonical ACI state with Azure Files managed-identity access."""

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
FILES_REST_CONTRIBUTOR_ROLE = "69566ab7-960f-475b-8e7c-b3118f30c6bd"
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
REST_ROLE_NAME = ROLE_NAME.replace("files-smb-mi-admin", "files-rest-contributor")
REST_ROLE_ID = ROLE_ID.replace("files-smb-mi-admin", "files-rest-contributor")
ACCOUNT_URL = (
    "[reference(resourceId('Microsoft.Storage/storageAccounts', variables('storageAccountName')), "
    "'2025-08-01').primaryEndpoints.file]"
)


def configure(template: dict[str, Any], mode: str = "smb") -> dict[str, Any]:
    """Preserve canonical mounts and checkpoint paths without a storage key."""
    if mode not in ("smb", "azure-files-rest"):
        raise ValueError("State access mode must be smb or azure-files-rest")
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
    containers = [container for group in groups for container in group["properties"]["containers"]]
    if not volumes and mode == "azure-files-rest":
        for container in containers:
            environment = {item["name"]: item.get("value") for item in container["properties"]["environmentVariables"]}
            if (environment.get("STATE_BACKEND") != "azure-files-rest"
                    or environment.get("STATE_AZURE_FILES_ACCOUNT_URL") != ACCOUNT_URL
                    or environment.get("STATE_AZURE_FILES_CLIENT_ID") != CLIENT_ID
                    or not environment.get("STATE_AZURE_FILES_ROOT")
                    or not environment.get("STATE_AZURE_FILES_SHARE")):
                raise ValueError("Expected a complete existing Azure Files REST state binding")
            volumes.append({"storageAccountName": "[variables('storageAccountName')]",
                            "shareName": environment["STATE_AZURE_FILES_SHARE"]})
    if not volumes or any(v["storageAccountName"] != "[variables('storageAccountName')]" for v in volumes):
        raise ValueError("Expected Azure Files volumes referencing the canonical state account")

    properties = store.setdefault("properties", {})
    properties["allowSharedKeyAccess"] = False
    properties["allowBlobPublicAccess"] = False
    properties["supportsHttpsTrafficOnly"] = True
    properties["minimumTlsVersion"] = "TLS1_2"
    authentication = properties.setdefault("azureFilesIdentityBasedAuthentication", {})
    authentication.setdefault("directoryServiceOptions", "None")
    if mode == "smb":
        authentication["smbOAuthSettings"] = {"isSmbOAuthEnabled": True}
    else:
        authentication.pop("smbOAuthSettings", None)
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
        "name": ROLE_NAME if mode == "smb" else REST_ROLE_NAME,
        "scope": STORAGE_ID,
        "dependsOn": [STORAGE_ID, IDENTITY_ID],
        "properties": {
            "roleDefinitionId": (
                "[subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '"
                + (SMB_MI_ADMIN_ROLE if mode == "smb" else FILES_REST_CONTRIBUTOR_ROLE) + "')]"
            ),
            "principalId": (
                "[reference(resourceId('Microsoft.ManagedIdentity/userAssignedIdentities', "
                "variables('stateIdentityName')), '2023-01-31').principalId]"
            ),
            "principalType": "ServicePrincipal",
        },
    }
    replaced_name = REST_ROLE_NAME if mode == "smb" else ROLE_NAME
    resources[:] = [resource for resource in resources
                    if not (resource["type"] == "Microsoft.Authorization/roleAssignments"
                            and resource["name"] == replaced_name)]
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
        replaced_id = REST_ROLE_ID if mode == "smb" else ROLE_ID
        dependencies[:] = [dependency for dependency in dependencies if dependency != replaced_id]
        for dependency in (IDENTITY_ID, ROLE_ID if mode == "smb" else REST_ROLE_ID):
            if dependency not in dependencies:
                dependencies.append(dependency)
    if mode == "smb":
        for volume in volumes:
            volume.pop("storageAccountKey", None)
            volume.pop("storageAccountKeyReference", None)
            volume.pop("userAssignedIdentityClientId", None)
            volume["userManagedIdentityClientId"] = CLIENT_ID
    else:
        for group in groups:
            properties = group["properties"]
            azure_volumes = {volume["name"]: volume["azureFile"]
                             for volume in properties.get("volumes", []) if "azureFile" in volume}
            for container in properties["containers"]:
                settings = container["properties"]
                environment = settings["environmentVariables"]
                existing = {item["name"]: item.get("value") for item in environment}
                mounts = [mount for mount in settings.get("volumeMounts", []) if mount["name"] in azure_volumes]
                if azure_volumes and len(mounts) != 1:
                    raise ValueError("REST checkpoints require one canonical state mount per container")
                if mounts:
                    root = mounts[0]["mountPath"]
                    share = azure_volumes[mounts[0]["name"]]["shareName"]
                else:
                    root, share = existing["STATE_AZURE_FILES_ROOT"], existing["STATE_AZURE_FILES_SHARE"]
                values = {"STATE_BACKEND": "azure-files-rest", "STATE_AZURE_FILES_ACCOUNT_URL": ACCOUNT_URL,
                          "STATE_AZURE_FILES_SHARE": share, "STATE_AZURE_FILES_CLIENT_ID": CLIENT_ID,
                          "STATE_AZURE_FILES_ROOT": root}
                if "STATE_FILE" not in existing:
                    values["STATE_FILE"] = root.rstrip("/") + "/state.json"
                for name, value in values.items():
                    matches = [item for item in environment if item["name"] == name]
                    if len(matches) > 1:
                        raise ValueError(f"Duplicate state environment variable: {name}")
                    if matches:
                        matches[0].clear()
                        matches[0].update(name=name, value=value)
                    else:
                        environment.append({"name": name, "value": value})
                remaining_mounts = [mount for mount in settings.get("volumeMounts", [])
                                    if mount["name"] not in azure_volumes]
                if remaining_mounts:
                    settings["volumeMounts"] = remaining_mounts
                else:
                    settings.pop("volumeMounts", None)
            remaining_volumes = [volume for volume in properties.get("volumes", []) if "azureFile" not in volume]
            if remaining_volumes:
                properties["volumes"] = remaining_volumes
            else:
                properties.pop("volumes", None)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("templates", nargs="+", type=Path)
    parser.add_argument("--mode", choices=("smb", "azure-files-rest"), default="azure-files-rest")
    args = parser.parse_args()
    staged = [(path, configure(json.loads(path.read_text(encoding="utf-8-sig")), args.mode)) for path in args.templates]
    for path, template in staged:
        path.write_text(json.dumps(template, indent=2) + "\n", encoding="utf-8")
        print(f"Configured managed-identity state: {path}")


if __name__ == "__main__":
    main()
