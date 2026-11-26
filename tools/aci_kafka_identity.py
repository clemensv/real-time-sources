"""Replace Event Hubs Kafka SAS bindings with explicit managed identity."""

import argparse
import copy
import json
from pathlib import Path
from typing import Any


def configure(template: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(template)
    namespaces = [r for r in result["resources"] if r["type"] == "Microsoft.EventHub/namespaces"]
    groups = [r for r in result["resources"] if r["type"] == "Microsoft.ContainerInstance/containerGroups"]
    if len(namespaces) != 1 or len(groups) != 1:
        raise ValueError("Expected one Event Hubs namespace and one container group")
    namespace, group = namespaces[0], groups[0]
    namespace["properties"]["disableLocalAuth"] = True
    result["resources"] = [r for r in result["resources"]
                           if not r["type"].startswith("Microsoft.EventHub/namespaces/eventhubs/authorizationRules")]
    variables = result["variables"]
    for key in ("authRuleName", "authRuleResourceId"):
        variables.pop(key, None)
    variables["kafkaIdentityName"] = "[concat(parameters('containerGroupName'), '-kafka-mi')]"
    identity_id = "[resourceId('Microsoft.ManagedIdentity/userAssignedIdentities', variables('kafkaIdentityName'))]"
    role_id = "[guid(resourceGroup().id, variables('kafkaIdentityName'), 'eventhubs-data-sender')]"
    identity = {"type": "Microsoft.ManagedIdentity/userAssignedIdentities", "apiVersion": "2023-01-31",
                "name": "[variables('kafkaIdentityName')]", "location": "[parameters('location')]"}
    role = {
        "type": "Microsoft.Authorization/roleAssignments", "apiVersion": "2022-04-01", "name": role_id,
        "scope": "[concat('Microsoft.EventHub/namespaces/', variables('eventHubNamespaceName'))]",
        "dependsOn": [identity_id, "[resourceId('Microsoft.EventHub/namespaces', variables('eventHubNamespaceName'))]"],
        "properties": {
            "roleDefinitionId": "[subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '2b629674-e913-4c01-ae53-ef4638d8f975')]",
            "principalId": "[reference(resourceId('Microsoft.ManagedIdentity/userAssignedIdentities', variables('kafkaIdentityName')), '2023-01-31').principalId]",
            "principalType": "ServicePrincipal",
        },
    }
    for resource in (identity, role):
        if not any(r["type"] == resource["type"] and r["name"] == resource["name"] for r in result["resources"]):
            result["resources"].append(resource)
    group["dependsOn"] = [dep for dep in group["dependsOn"]
                          if "authRule" not in dep and "authorizationRules" not in dep]
    role_dependency = "[extensionResourceId(resourceId('Microsoft.EventHub/namespaces', variables('eventHubNamespaceName')), 'Microsoft.Authorization/roleAssignments', guid(resourceGroup().id, variables('kafkaIdentityName'), 'eventhubs-data-sender'))]"
    for dependency in (identity_id, role_dependency):
        if dependency not in group["dependsOn"]:
            group["dependsOn"].append(dependency)
    identity_config = group.setdefault("identity", {"type": "UserAssigned", "userAssignedIdentities": {}})
    if identity_config["type"] != "UserAssigned":
        raise ValueError("Expected a user-assigned container identity configuration")
    identity_config["userAssignedIdentities"][identity_id] = {}
    for container in group["properties"]["containers"]:
        environment = container["properties"]["environmentVariables"]
        environment[:] = [item for item in environment
                          if item["name"] not in ("CONNECTION_STRING", "KAFKA_AUTH_MODE", "KAFKA_ENTRA_CLIENT_ID",
                                                  "KAFKA_BOOTSTRAP_SERVERS", "KAFKA_TOPIC", "KAFKA_ENABLE_TLS")]
        environment.extend([
            {"name": "KAFKA_AUTH_MODE", "value": "azure-entra"},
            {"name": "KAFKA_ENTRA_CLIENT_ID", "value": "[reference(resourceId('Microsoft.ManagedIdentity/userAssignedIdentities', variables('kafkaIdentityName')), '2023-01-31').clientId]"},
            {"name": "KAFKA_BOOTSTRAP_SERVERS", "value": "[concat(variables('eventHubNamespaceName'), '.servicebus.windows.net:9093')]"},
            {"name": "KAFKA_TOPIC", "value": "[variables('eventHubName')]"},
            {"name": "KAFKA_ENABLE_TLS", "value": "true"},
        ])
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("templates", type=Path, nargs="+")
    args = parser.parse_args()
    converted = [(path, configure(json.loads(path.read_text(encoding="utf-8-sig"))))
                 for path in args.templates]
    for path, template in converted:
        path.write_text(json.dumps(template, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
