#!/usr/bin/env python3
"""Generate ARM templates for all bridges in the repository.

For each bridge directory with a Dockerfile, generates:
  - azure-template.json (BYOH: bring your own Event Hub)
  - azure-template-with-eventhub.json (deploys Event Hub + container)
Also updates CONTAINER.md and README.md with Deploy to Azure buttons.
"""

import json
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/clemensv/real-time-sources/main"

# Env vars that are always handled by the template framework, not bridge-specific
STANDARD_ENVS = {
    "CONNECTION_STRING", "KAFKA_BOOTSTRAP_SERVERS", "KAFKA_TOPIC",
    "SASL_USERNAME", "SASL_PASSWORD", "LOG_LEVEL", "PYTHONUNBUFFERED",
    "KAFKA_ENABLE_TLS",
}

# Env vars that look like secrets (API keys, passwords, tokens)
SECRET_PATTERNS = re.compile(r"(API_KEY|PASSWORD|TOKEN|SECRET|ACCESS_CODE)", re.IGNORECASE)

# Env vars that are state/cursor files
STATE_FILE_PATTERNS = re.compile(r"(STATE_FILE|LAST_POLLED|CURSOR_FILE|POLLED_FILE)", re.IGNORECASE)


def parse_dockerfile_envs(bridge_dir: str) -> list[dict]:
    """Parse ENV lines from Dockerfile, return list of {name, default, is_secret, is_state_file}."""
    dockerfile = os.path.join(bridge_dir, "Dockerfile")
    if not os.path.exists(dockerfile):
        return []
    envs = []
    seen = set()
    with open(dockerfile, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line.startswith("ENV "):
                continue
            # Parse ENV KEY="value" or ENV KEY=value
            m = re.match(r'ENV\s+(\w+)\s*=\s*"?([^"]*)"?', line)
            if not m:
                continue
            name, default = m.group(1), m.group(2)
            if name in STANDARD_ENVS or name in seen:
                continue
            seen.add(name)
            envs.append({
                "name": name,
                "default": default,
                "is_secret": bool(SECRET_PATTERNS.search(name)),
                "is_state_file": bool(STATE_FILE_PATTERNS.search(name)),
            })
    return envs


def get_bridge_display_name(bridge_dir_name: str) -> str:
    """Convert directory name to display name."""
    return bridge_dir_name.replace("-", " ").replace("_", " ").title()


def make_env_vars_section(bridge_envs: list[dict], include_connection_string_param: bool) -> list[dict]:
    """Build the environmentVariables array for the ACI container."""
    env_vars = []
    if include_connection_string_param:
        env_vars.append({
            "name": "CONNECTION_STRING",
            "secureValue": "[parameters('connectionString')]"
        })
    else:
        env_vars.append({
            "name": "CONNECTION_STRING",
            "secureValue": "[listKeys(variables('authRuleResourceId'), '2024-01-01').primaryConnectionString]"
        })
    env_vars.append({"name": "LOG_LEVEL", "value": "INFO"})

    for env in bridge_envs:
        if env["is_secret"]:
            env_vars.append({
                "name": env["name"],
                "secureValue": f"[parameters('{_param_name(env['name'])}')]"
            })
        elif env["is_state_file"]:
            fname = os.path.basename(env["default"]) if env["default"] else "state.json"
            if not fname or fname == "/":
                fname = "state.json"
            env_vars.append({
                "name": env["name"],
                "value": f"/mnt/bridge-state/{fname}"
            })
        else:
            if env["default"]:
                env_vars.append({
                    "name": env["name"],
                    "value": f"[parameters('{_param_name(env['name'])}')]"
                })
            else:
                env_vars.append({
                    "name": env["name"],
                    "value": f"[parameters('{_param_name(env['name'])}')]"
                })

    env_vars.append({"name": "PYTHONUNBUFFERED", "value": "1"})
    return env_vars


def _param_name(env_name: str) -> str:
    """Convert ENV_NAME to camelCase parameter name."""
    parts = env_name.lower().split("_")
    return parts[0] + "".join(p.capitalize() for p in parts[1:])


def make_parameters(bridge_envs: list[dict], include_connection_string: bool) -> dict:
    """Build the parameters section."""
    params = {}
    if include_connection_string:
        params["connectionString"] = {
            "type": "securestring",
            "minLength": 1,
            "metadata": {
                "description": "Azure Event Hubs or Fabric Event Streams connection string (e.g. Endpoint=sb://...;SharedAccessKeyName=...;SharedAccessKey=...;EntityPath=...)"
            }
        }
    return params


def make_bridge_specific_params(bridge_envs: list[dict]) -> dict:
    """Build parameters for bridge-specific env vars."""
    params = {}
    for env in bridge_envs:
        pname = _param_name(env["name"])
        if env["is_secret"]:
            params[pname] = {
                "type": "securestring",
                "defaultValue": "",
                "metadata": {"description": f"{env['name']} configuration value."}
            }
        elif env["is_state_file"]:
            continue  # state files are handled automatically
        else:
            params[pname] = {
                "type": "string",
                "defaultValue": env["default"] or "",
                "metadata": {"description": f"{env['name']} configuration value."}
            }
    return params


def generate_byoh_template(bridge_name: str, bridge_envs: list[dict], display_name: str) -> dict:
    """Generate the BYOH (bring your own hub) ARM template."""
    params = {
        "connectionString": {
            "type": "securestring",
            "minLength": 1,
            "metadata": {
                "description": "Azure Event Hubs or Fabric Event Streams connection string (e.g. Endpoint=sb://...;SharedAccessKeyName=...;SharedAccessKey=...;EntityPath=...)"
            }
        },
        "containerGroupName": {
            "type": "string",
            "defaultValue": bridge_name,
            "metadata": {"description": "Name for the container group resource."},
            "maxLength": 63,
            "minLength": 1
        },
        "location": {
            "type": "string",
            "defaultValue": "[resourceGroup().location]",
            "metadata": {"description": "Azure region for all resources."}
        }
    }
    params.update(make_bridge_specific_params(bridge_envs))

    template = {
        "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
        "contentVersion": "1.0.0.0",
        "metadata": {
            "description": f"Deploys the {display_name} bridge as an Azure Container Instance with persistent state storage and Log Analytics diagnostics."
        },
        "parameters": params,
        "variables": {
            "storageAccountName": "[take(concat(replace(replace(parameters('containerGroupName'), '-', ''), '_', ''), 'stg'), 24)]",
            "fileShareName": "bridge-state",
            "imageName": f"ghcr.io/clemensv/real-time-sources-{bridge_name}:latest",
            "logAnalyticsWorkspaceName": "[concat(parameters('containerGroupName'), '-logs')]"
        },
        "resources": [
            {
                "type": "Microsoft.OperationalInsights/workspaces",
                "apiVersion": "2022-10-01",
                "name": "[variables('logAnalyticsWorkspaceName')]",
                "location": "[parameters('location')]",
                "properties": {
                    "sku": {"name": "PerGB2018"},
                    "retentionInDays": 30
                }
            },
            {
                "type": "Microsoft.Storage/storageAccounts",
                "apiVersion": "2023-05-01",
                "name": "[variables('storageAccountName')]",
                "location": "[parameters('location')]",
                "sku": {"name": "Standard_LRS"},
                "kind": "StorageV2",
                "properties": {"accessTier": "Hot", "minimumTlsVersion": "TLS1_2"}
            },
            {
                "type": "Microsoft.Storage/storageAccounts/fileServices",
                "apiVersion": "2023-05-01",
                "name": "[concat(variables('storageAccountName'), '/default')]",
                "dependsOn": [
                    "[resourceId('Microsoft.Storage/storageAccounts', variables('storageAccountName'))]"
                ],
                "properties": {}
            },
            {
                "type": "Microsoft.Storage/storageAccounts/fileServices/shares",
                "apiVersion": "2023-05-01",
                "name": "[concat(variables('storageAccountName'), '/default/', variables('fileShareName'))]",
                "dependsOn": [
                    "[resourceId('Microsoft.Storage/storageAccounts', variables('storageAccountName'))]"
                ],
                "properties": {"shareQuota": 1}
            },
            {
                "type": "Microsoft.ContainerInstance/containerGroups",
                "apiVersion": "2023-05-01",
                "name": "[parameters('containerGroupName')]",
                "location": "[parameters('location')]",
                "dependsOn": [
                    "[resourceId('Microsoft.OperationalInsights/workspaces', variables('logAnalyticsWorkspaceName'))]",
                    "[resourceId('Microsoft.Storage/storageAccounts/fileServices/shares', variables('storageAccountName'), 'default', variables('fileShareName'))]"
                ],
                "properties": {
                    "osType": "Linux",
                    "restartPolicy": "Always",
                    "diagnostics": {
                        "logAnalytics": {
                            "workspaceId": "[reference(resourceId('Microsoft.OperationalInsights/workspaces', variables('logAnalyticsWorkspaceName')), '2022-10-01').customerId]",
                            "workspaceKey": "[listKeys(resourceId('Microsoft.OperationalInsights/workspaces', variables('logAnalyticsWorkspaceName')), '2022-10-01').primarySharedKey]",
                            "logType": "ContainerInstanceLogs"
                        }
                    },
                    "containers": [{
                        "name": "[parameters('containerGroupName')]",
                        "properties": {
                            "image": "[variables('imageName')]",
                            "resources": {"requests": {"cpu": 0.5, "memoryInGB": 1.0}},
                            "environmentVariables": make_env_vars_section(bridge_envs, True),
                            "volumeMounts": [{"name": "bridge-state", "mountPath": "/mnt/bridge-state"}]
                        }
                    }],
                    "volumes": [{
                        "name": "bridge-state",
                        "azureFile": {
                            "shareName": "[variables('fileShareName')]",
                            "storageAccountName": "[variables('storageAccountName')]",
                            "storageAccountKey": "[listKeys(resourceId('Microsoft.Storage/storageAccounts', variables('storageAccountName')), '2023-05-01').keys[0].value]"
                        }
                    }]
                }
            }
        ],
        "outputs": {
            "containerGroupId": {
                "type": "string",
                "value": "[resourceId('Microsoft.ContainerInstance/containerGroups', parameters('containerGroupName'))]"
            },
            "logAnalyticsWorkspaceId": {
                "type": "string",
                "value": "[reference(resourceId('Microsoft.OperationalInsights/workspaces', variables('logAnalyticsWorkspaceName')), '2022-10-01').customerId]"
            }
        }
    }
    return template


def generate_with_eventhub_template(bridge_name: str, bridge_envs: list[dict], display_name: str) -> dict:
    """Generate the with-Event-Hub ARM template."""
    params = {
        "containerGroupName": {
            "type": "string",
            "defaultValue": bridge_name,
            "metadata": {"description": "Name for the container group and base name for all resources."},
            "maxLength": 63,
            "minLength": 1
        },
        "eventHubSku": {
            "type": "string",
            "defaultValue": "Standard",
            "allowedValues": ["Basic", "Standard"],
            "metadata": {"description": "Event Hub namespace SKU."}
        },
        "location": {
            "type": "string",
            "defaultValue": "[resourceGroup().location]",
            "metadata": {"description": "Azure region for all resources."}
        }
    }
    params.update(make_bridge_specific_params(bridge_envs))

    template = {
        "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
        "contentVersion": "1.0.0.0",
        "metadata": {
            "description": f"Deploys the {display_name} bridge with a new Event Hub namespace, event hub, and Azure Container Instance with Log Analytics diagnostics."
        },
        "parameters": params,
        "variables": {
            "storageAccountName": "[take(concat(replace(replace(parameters('containerGroupName'), '-', ''), '_', ''), 'stg'), 24)]",
            "fileShareName": "bridge-state",
            "imageName": f"ghcr.io/clemensv/real-time-sources-{bridge_name}:latest",
            "eventHubNamespaceName": "[concat(parameters('containerGroupName'), '-ehns')]",
            "eventHubName": "[parameters('containerGroupName')]",
            "authRuleName": "bridge-send-listen",
            "authRuleResourceId": "[resourceId('Microsoft.EventHub/namespaces/eventhubs/authorizationRules', variables('eventHubNamespaceName'), variables('eventHubName'), variables('authRuleName'))]",
            "logAnalyticsWorkspaceName": "[concat(parameters('containerGroupName'), '-logs')]"
        },
        "resources": [
            {
                "type": "Microsoft.OperationalInsights/workspaces",
                "apiVersion": "2022-10-01",
                "name": "[variables('logAnalyticsWorkspaceName')]",
                "location": "[parameters('location')]",
                "properties": {
                    "sku": {"name": "PerGB2018"},
                    "retentionInDays": 30
                }
            },
            {
                "type": "Microsoft.EventHub/namespaces",
                "apiVersion": "2024-01-01",
                "name": "[variables('eventHubNamespaceName')]",
                "location": "[parameters('location')]",
                "sku": {
                    "name": "[parameters('eventHubSku')]",
                    "tier": "[parameters('eventHubSku')]",
                    "capacity": 1
                },
                "properties": {
                    "minimumTlsVersion": "1.2",
                    "isAutoInflateEnabled": False,
                    "kafkaEnabled": True
                }
            },
            {
                "type": "Microsoft.EventHub/namespaces/eventhubs",
                "apiVersion": "2024-01-01",
                "name": "[concat(variables('eventHubNamespaceName'), '/', variables('eventHubName'))]",
                "dependsOn": [
                    "[resourceId('Microsoft.EventHub/namespaces', variables('eventHubNamespaceName'))]"
                ],
                "properties": {"partitionCount": 4, "messageRetentionInDays": 1}
            },
            {
                "type": "Microsoft.EventHub/namespaces/eventhubs/authorizationRules",
                "apiVersion": "2024-01-01",
                "name": "[concat(variables('eventHubNamespaceName'), '/', variables('eventHubName'), '/', variables('authRuleName'))]",
                "dependsOn": [
                    "[resourceId('Microsoft.EventHub/namespaces/eventhubs', variables('eventHubNamespaceName'), variables('eventHubName'))]"
                ],
                "properties": {"rights": ["Send", "Listen"]}
            },
            {
                "type": "Microsoft.Storage/storageAccounts",
                "apiVersion": "2023-05-01",
                "name": "[variables('storageAccountName')]",
                "location": "[parameters('location')]",
                "sku": {"name": "Standard_LRS"},
                "kind": "StorageV2",
                "properties": {"accessTier": "Hot", "minimumTlsVersion": "TLS1_2"}
            },
            {
                "type": "Microsoft.Storage/storageAccounts/fileServices",
                "apiVersion": "2023-05-01",
                "name": "[concat(variables('storageAccountName'), '/default')]",
                "dependsOn": [
                    "[resourceId('Microsoft.Storage/storageAccounts', variables('storageAccountName'))]"
                ],
                "properties": {}
            },
            {
                "type": "Microsoft.Storage/storageAccounts/fileServices/shares",
                "apiVersion": "2023-05-01",
                "name": "[concat(variables('storageAccountName'), '/default/', variables('fileShareName'))]",
                "dependsOn": [
                    "[resourceId('Microsoft.Storage/storageAccounts', variables('storageAccountName'))]"
                ],
                "properties": {"shareQuota": 1}
            },
            {
                "type": "Microsoft.ContainerInstance/containerGroups",
                "apiVersion": "2023-05-01",
                "name": "[parameters('containerGroupName')]",
                "location": "[parameters('location')]",
                "dependsOn": [
                    "[resourceId('Microsoft.OperationalInsights/workspaces', variables('logAnalyticsWorkspaceName'))]",
                    "[variables('authRuleResourceId')]",
                    "[resourceId('Microsoft.Storage/storageAccounts/fileServices/shares', variables('storageAccountName'), 'default', variables('fileShareName'))]"
                ],
                "properties": {
                    "osType": "Linux",
                    "restartPolicy": "Always",
                    "diagnostics": {
                        "logAnalytics": {
                            "workspaceId": "[reference(resourceId('Microsoft.OperationalInsights/workspaces', variables('logAnalyticsWorkspaceName')), '2022-10-01').customerId]",
                            "workspaceKey": "[listKeys(resourceId('Microsoft.OperationalInsights/workspaces', variables('logAnalyticsWorkspaceName')), '2022-10-01').primarySharedKey]",
                            "logType": "ContainerInstanceLogs"
                        }
                    },
                    "containers": [{
                        "name": "[parameters('containerGroupName')]",
                        "properties": {
                            "image": "[variables('imageName')]",
                            "resources": {"requests": {"cpu": 0.5, "memoryInGB": 1.0}},
                            "environmentVariables": make_env_vars_section(bridge_envs, False),
                            "volumeMounts": [{"name": "bridge-state", "mountPath": "/mnt/bridge-state"}]
                        }
                    }],
                    "volumes": [{
                        "name": "bridge-state",
                        "azureFile": {
                            "shareName": "[variables('fileShareName')]",
                            "storageAccountName": "[variables('storageAccountName')]",
                            "storageAccountKey": "[listKeys(resourceId('Microsoft.Storage/storageAccounts', variables('storageAccountName')), '2023-05-01').keys[0].value]"
                        }
                    }]
                }
            }
        ],
        "outputs": {
            "containerGroupId": {
                "type": "string",
                "value": "[resourceId('Microsoft.ContainerInstance/containerGroups', parameters('containerGroupName'))]"
            },
            "eventHubNamespaceName": {
                "type": "string",
                "value": "[variables('eventHubNamespaceName')]"
            },
            "eventHubName": {
                "type": "string",
                "value": "[variables('eventHubName')]"
            },
            "logAnalyticsWorkspaceId": {
                "type": "string",
                "value": "[reference(resourceId('Microsoft.OperationalInsights/workspaces', variables('logAnalyticsWorkspaceName')), '2022-10-01').customerId]"
            }
        }
    }
    return template


def make_deploy_buttons(bridge_name: str) -> str:
    """Generate the Deploy to Azure markdown section."""
    byoh_url = f"{GITHUB_RAW_BASE}/{bridge_name}/azure-template.json"
    with_eh_url = f"{GITHUB_RAW_BASE}/{bridge_name}/azure-template-with-eventhub.json"
    byoh_encoded = byoh_url.replace(":", "%3A").replace("/", "%2F")
    with_eh_encoded = with_eh_url.replace(":", "%3A").replace("/", "%2F")

    return f"""## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/{byoh_encoded})

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/{with_eh_encoded})"""


def update_container_md(bridge_dir: str, bridge_name: str) -> bool:
    """Update CONTAINER.md with deploy buttons. Returns True if modified."""
    container_md = os.path.join(bridge_dir, "CONTAINER.md")
    if not os.path.exists(container_md):
        return False
    with open(container_md, "r", encoding="utf-8") as f:
        content = f.read()

    deploy_section = make_deploy_buttons(bridge_name)

    # Check if deploy section already exists
    if "Deploying into Azure Container Instances" in content:
        # Replace existing section
        pattern = r"## Deploying into Azure Container Instances.*$"
        new_content = re.sub(pattern, deploy_section, content, flags=re.DOTALL)
    else:
        # Append at end
        new_content = content.rstrip() + "\n\n" + deploy_section + "\n"

    if new_content != content:
        with open(container_md, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True
    return False


def update_readme_md(bridge_dir: str, bridge_name: str) -> bool:
    """Update bridge README.md with deploy buttons. Returns True if modified."""
    readme = os.path.join(bridge_dir, "README.md")
    if not os.path.exists(readme):
        return False
    with open(readme, "r", encoding="utf-8") as f:
        content = f.read()

    deploy_section = make_deploy_buttons(bridge_name)

    if "Deploying into Azure Container Instances" in content:
        pattern = r"## Deploying into Azure Container Instances.*$"
        new_content = re.sub(pattern, deploy_section, content, flags=re.DOTALL)
    elif "Deploy to Azure" in content and "deploytoazurebutton" in content:
        # Has deploy buttons but in different format - replace from that section
        pattern = r"## Deploy to Azure.*$"
        new_content = re.sub(pattern, deploy_section, content, flags=re.DOTALL)
    else:
        new_content = content.rstrip() + "\n\n" + deploy_section + "\n"

    if new_content != content:
        with open(readme, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True
    return False


def find_bridges() -> list[str]:
    """Find all bridge directories (those with a Dockerfile)."""
    bridges = []
    for entry in sorted(os.listdir(REPO_ROOT)):
        bridge_dir = os.path.join(REPO_ROOT, entry)
        if os.path.isdir(bridge_dir) and os.path.exists(os.path.join(bridge_dir, "Dockerfile")):
            bridges.append(entry)
    return bridges


def main():
    bridges = find_bridges()
    print(f"Found {len(bridges)} bridges")

    stats = {"templates_created": 0, "templates_updated": 0, "gen_scripts_deleted": 0,
             "container_md_updated": 0, "readme_updated": 0, "skipped": 0}

    for bridge_name in bridges:
        bridge_dir = os.path.join(REPO_ROOT, bridge_name)
        display_name = get_bridge_display_name(bridge_name)
        bridge_envs = parse_dockerfile_envs(bridge_dir)

        # Generate BYOH template
        byoh_path = os.path.join(bridge_dir, "azure-template.json")
        byoh = generate_byoh_template(bridge_name, bridge_envs, display_name)
        is_new = not os.path.exists(byoh_path)
        with open(byoh_path, "w", encoding="utf-8") as f:
            json.dump(byoh, f, indent=2)
            f.write("\n")
        if is_new:
            stats["templates_created"] += 1
        else:
            stats["templates_updated"] += 1

        # Generate with-eventhub template
        eh_path = os.path.join(bridge_dir, "azure-template-with-eventhub.json")
        eh = generate_with_eventhub_template(bridge_name, bridge_envs, display_name)
        is_new = not os.path.exists(eh_path)
        with open(eh_path, "w", encoding="utf-8") as f:
            json.dump(eh, f, indent=2)
            f.write("\n")
        if is_new:
            stats["templates_created"] += 1
        else:
            stats["templates_updated"] += 1

        # Delete generate-template.ps1 if it exists
        gen_script = os.path.join(bridge_dir, "generate-template.ps1")
        if os.path.exists(gen_script):
            os.remove(gen_script)
            stats["gen_scripts_deleted"] += 1
            print(f"  Deleted {bridge_name}/generate-template.ps1")

        # Update CONTAINER.md
        if update_container_md(bridge_dir, bridge_name):
            stats["container_md_updated"] += 1

        # Update README.md
        if update_readme_md(bridge_dir, bridge_name):
            stats["readme_updated"] += 1

        env_info = f" ({len(bridge_envs)} custom envs)" if bridge_envs else ""
        print(f"  {bridge_name}{env_info}")

    print(f"\nDone! Stats:")
    print(f"  Templates created: {stats['templates_created']}")
    print(f"  Templates updated: {stats['templates_updated']}")
    print(f"  generate-template.ps1 deleted: {stats['gen_scripts_deleted']}")
    print(f"  CONTAINER.md updated: {stats['container_md_updated']}")
    print(f"  README.md updated: {stats['readme_updated']}")


if __name__ == "__main__":
    main()
