#!/usr/bin/env python3
"""Replace the per-source 'Deploy' section with a pegelonline-quality block.

The pegelonline gold standard for the Deploy section is a single `## Deploy`
H2 containing:

  ### Deploying into Microsoft Fabric
    #### Fabric Notebook feeder       (only if notebook/ exists in the source)
    #### Fabric ACI feeder
    #### Fabric Map visualization     (only if fabric/README.md exists)

  ### Deploying into Azure Container Instances
    #### Kafka  -- bring your own Event Hub / Kafka
    #### Kafka  -- provision a new Event Hub
    #### MQTT   -- bring your own broker
    #### MQTT   -- provision a new Event Grid namespace MQTT broker
    #### AMQP   -- provision a new Azure Service Bus namespace

  ### Self-hosted

Each ARM-template sub-section is emitted only if the corresponding
`azure-template*.json` file exists in the source directory. Each PowerShell
invocation uses the real script parameter names (-Workspace / -ResourceGroup
/ -Location). Sentinels `<!-- source-deploy:begin/end -->` bracket the
generated content so re-runs are idempotent.

Run from repo root:
  python tools/docs/generate_source_deploy.py
"""
from __future__ import annotations
import json
import re
from pathlib import Path

from generate_root_catalog import ROOT, FEEDERS, CATALOG, REPO, PORTAL

BEGIN = "<!-- source-deploy:begin -->"
END = "<!-- source-deploy:end -->"

# Map azure-template file basename -> (h4 title, blurb)
ARM_TEMPLATES = [
    (
        "azure-template.json",
        "Kafka — bring your own Event Hub / Kafka",
        "Deploy the Kafka container with your own Azure Event Hubs or Fabric Event Stream connection string. You pass the connection string at deploy time; the template provisions only the container and a storage account for persistent dedupe state.",
    ),
    (
        "azure-template-with-eventhub.json",
        "Kafka — provision a new Event Hub",
        "Deploy the Kafka container together with a new Event Hubs namespace (Standard SKU, 1 throughput unit) and event hub. The connection string is wired automatically.",
    ),
    (
        "azure-template-mqtt.json",
        "MQTT — bring your own broker",
        "Deploy the MQTT container against an existing MQTT 5 broker (Mosquitto, EMQX, HiveMQ, Azure Event Grid namespace MQTT, etc.). You provide the `mqtts://` URL and optional credentials.",
    ),
    (
        "azure-template-with-eventgrid-mqtt.json",
        "MQTT — provision a new Event Grid namespace MQTT broker",
        "Deploy the MQTT container together with a new [Azure Event Grid namespace](https://learn.microsoft.com/azure/event-grid/mqtt-overview) with the MQTT broker enabled, a topic space for this source, a user-assigned managed identity, and the **EventGrid TopicSpaces Publisher** role assignment. The feeder authenticates with MQTT v5 enhanced authentication (`OAUTH2-JWT`) — no shared keys to rotate.",
    ),
    (
        "azure-template-with-servicebus.json",
        "AMQP — provision a new Azure Service Bus namespace",
        "Deploy the AMQP container together with a new [Azure Service Bus Standard namespace](https://learn.microsoft.com/azure/service-bus-messaging/service-bus-messaging-overview) with a queue, a user-assigned managed identity, and the **Azure Service Bus Data Sender** role assignment. The feeder authenticates via AMQP CBS put-token with Microsoft Entra ID — no SAS key rotation required.",
    ),
    (
        "azure-template-amqp.json",
        "AMQP — bring your own AMQP 1.0 peer",
        "Deploy the AMQP container against an existing AMQP 1.0 peer (RabbitMQ AMQP 1.0 plugin, ActiveMQ Artemis, Qpid Dispatch, Azure Service Bus, Azure Event Hubs). You pass the broker URL and credentials; the template provisions only the container.",
    ),
]


def deploy_button(sid: str, template: str) -> str:
    url = f"https://raw.githubusercontent.com/{REPO}/main/feeders/{sid}/{template}"
    return (
        "[![Deploy to Azure](https://aka.ms/deploytoazurebutton)]"
        f"(https://portal.azure.com/#create/Microsoft.Template/uri/"
        f"{url.replace(':', '%3A').replace('/', '%2F')})"
    )


def fabric_section(entry: dict) -> str:
    sid = entry["id"]
    name = entry["name"]
    src = FEEDERS / sid
    has_notebook = (src / "notebook").exists() and any(
        (src / "notebook").glob("*.ipynb")
    )
    has_map = (src / "fabric" / "README.md").exists()
    has_kql = (src / "kql").exists() and any((src / "kql").glob("*.kql"))

    parts: list[str] = []
    parts.append("### Deploying into Microsoft Fabric")
    parts.append("")
    kql_phrase = (
        f"an attached **Eventhouse / KQL database** materializes the contract from [`kql/`](kql/)"
        if has_kql
        else "an attached **Eventhouse / KQL database** materializes the contract"
    )
    map_phrase = (
        ", and the bundled [Fabric Map](fabric/README.md) visualizes the live state on a basemap"
        if has_map
        else ""
    )
    parts.append(
        f"{name} targets Microsoft Fabric end-to-end: events land in a Fabric "
        f"**Event Stream** (custom endpoint), {kql_phrase}{map_phrase}."
    )
    parts.append("")
    if has_notebook:
        parts.append(
            "Two hosting models are supported. Use the deploy buttons on the "
            f"[project portal]({PORTAL}#{sid}) to launch either — both walk you "
            "through the same Fabric workspace selection and follow-up steps."
        )
    else:
        parts.append(
            f"Use the deploy button on the [project portal]({PORTAL}#{sid}) "
            "to launch the Fabric ACI hosting model — it walks you through "
            "Fabric workspace selection and follow-up steps."
        )
    parts.append("")

    if has_notebook:
        parts.append(
            "#### Fabric Notebook feeder &nbsp;<sub><i>(recommended for low-volume polling)</i></sub>"
        )
        parts.append("")
        parts.append(
            f"A scheduled Fabric Notebook in [`notebook/`](notebook/) runs the "
            f"poller inside the Fabric workspace itself, against a per-source "
            f"Fabric **Environment** that bundles the `{sid.replace('-', '_')}` "
            "package and the generated producer sub-packages. The Event Stream "
            "custom-endpoint connection string is looked up at runtime via the "
            "public Fabric Topology API using the workspace identity — no "
            "secrets in the notebook, no separate container host to manage. "
            f"Dedupe state lives in OneLake under "
            f"`/lakehouse/default/Files/feeder-state/{sid}/`."
        )
        parts.append("")
        parts.append("```powershell")
        parts.append("tools/deploy-fabric/deploy-feeder-notebook.ps1 `")
        parts.append(f"  -Source {sid} `")
        parts.append("  -Workspace <fabric-workspace-id-or-name> `")
        parts.append("  -ResourceGroup <azure-rg-for-bootstrap> `")
        parts.append("  -Location <azure-region>")
        parts.append("```")
        parts.append("")
        parts.append(
            "Best fit for poll-based sources whose update cadence aligns with "
            "scheduled execution; the notebook writes a per-run diagnostic "
            "log to OneLake on every run."
        )
        parts.append("")
        parts.append(
            f"[![Deploy Fabric Notebook](https://img.shields.io/badge/Fabric-Notebook%20Feeder-117865?logo=microsoftfabric&logoColor=white)]({PORTAL}#{sid}/fabric-notebook)"
        )
        parts.append("")

    # Fabric ACI feeder (always shown)
    aci_subtitle = (
        " &nbsp;<sub><i>(recommended for high-volume / always-on, and for MQTT or AMQP)</i></sub>"
        if has_notebook
        else " &nbsp;<sub><i>(continuous container hosting against a Fabric Event Stream)</i></sub>"
    )
    parts.append(f"#### Fabric ACI feeder{aci_subtitle}")
    parts.append("")
    parts.append(
        "A long-running Azure Container Instance hosts the container image and "
        "writes into a Fabric Event Stream custom endpoint. Use this for "
        "continuous polling, real-time MQTT/UNS publishing, or the AMQP "
        "transport — anything that does not fit a scheduled-notebook model."
    )
    parts.append("")
    parts.append("```powershell")
    parts.append("tools/deploy-fabric/deploy-fabric-aci.ps1 `")
    parts.append(f"  -Source {sid} `")
    parts.append("  -Workspace <fabric-workspace-id-or-name> `")
    parts.append("  -ResourceGroup <azure-rg> `")
    parts.append("  -Location <azure-region>")
    parts.append("```")
    parts.append("")
    kql_clause = (
        " the KQL database with the [`kql/`](kql/) schema and update policies,"
        if has_kql
        else ""
    )
    parts.append(
        f"The script creates the Eventhouse,{kql_clause} the Event Stream "
        "with a custom endpoint, the ACI with the connection string wired "
        "in, and a storage account / file share mounted at `/state` for "
        "dedupe persistence."
    )
    parts.append("")
    parts.append(
        f"[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)]({PORTAL}#{sid}/fabric-aci)"
    )
    parts.append("")

    if has_map:
        parts.append(
            "#### Fabric Map visualization &nbsp;<sub><i>(optional, post-deploy)</i></sub>"
        )
        parts.append("")
        parts.append(
            "After either hosting model has events flowing, run "
            "[`fabric/post-deploy.ps1`](fabric/README.md) (or "
            f"`tools/deploy-fabric/deploy-fabric.ps1 -Source {sid} -Workspace <ws>`) "
            "to provision the bundled Fabric Map item and wire its Kusto-backed "
            "layers onto a basemap. The map updates live as new events arrive."
        )
        parts.append("")

    return "\n".join(parts)


def aci_section(entry: dict) -> str:
    sid = entry["id"]
    src = FEEDERS / sid

    available = [
        (fname, title, blurb)
        for (fname, title, blurb) in ARM_TEMPLATES
        if (src / fname).exists()
    ]
    if not available:
        return ""

    parts: list[str] = []
    parts.append("### Deploying into Azure Container Instances")
    parts.append("")
    parts.append(
        f"{len(available)} one-click deployment template{'s' if len(available) != 1 else ''} "
        "— one per realistic Azure target. These templates host the container "
        "directly in Azure (without a Fabric workspace) and target an Azure "
        "Event Hubs namespace, an MQTT broker, or an AMQP 1.0 peer. All "
        "templates create a storage account and file share for persistent "
        "dedupe state."
    )
    parts.append("")
    for fname, title, blurb in available:
        parts.append(f"#### {title}")
        parts.append("")
        parts.append(blurb)
        parts.append("")
        parts.append(deploy_button(sid, fname))
        parts.append("")

    return "\n".join(parts)


def self_hosted_section(entry: dict) -> str:
    src = FEEDERS / entry["id"]
    dockerfiles = sorted(p.name for p in src.glob("Dockerfile*"))
    n = len(dockerfiles)
    image_word = (
        f"any of the {n} container images" if n > 1 else "the container image"
    )
    return (
        "### Self-hosted\n\n"
        f"Pull and run {image_word} directly — laptop, Kubernetes, Azure "
        "Container Apps, Cloud Run, ECS, bare metal. The full per-transport / "
        "per-auth-mode environment-variable matrix and sample `docker run` "
        "commands for every target broker live in [CONTAINER.md](CONTAINER.md)."
    )


def render_deploy(entry: dict) -> str:
    name = entry["name"]
    head = (
        "## Deploy\n\n"
        "The portal buttons wrap the underlying scripts and ARM templates "
        "documented below; pick the path that matches your destination and "
        "operational preference. Every route lands in the same Eventhouse / "
        "KQL schema if you want one — they only differ in where the feeder "
        "container or notebook runs."
    )
    chunks = [head, fabric_section(entry), aci_section(entry), self_hosted_section(entry)]
    body = "\n\n".join(c for c in chunks if c).rstrip() + "\n"
    return f"{BEGIN}\n{body}{END}\n"


# Regex matching the legacy deploy region: from the first H2 whose title
# starts with "Deploy" (e.g. "## Deploy", "## Deploying into Microsoft Fabric")
# through the LAST contiguous H2 that is also deploy-related ("Deploy*",
# "Self-hosted", "Self hosting"). Stops at the next H2 that is not deploy-
# related or at end of file.
DEPLOY_REGION = re.compile(
    r"(?ms)^##\s+(?:Deploy|Self[- ]host).*?(?=^##\s+(?!Deploy|Self[- ]host)|\Z)"
)
DEPLOY_REGION_WITH_SENTINELS = re.compile(
    re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n?", re.DOTALL
)


def upsert_deploy(path: Path, deploy_block: str) -> tuple[bool, str]:
    if not path.exists():
        return (False, "skip (file missing)")
    text = path.read_text(encoding="utf-8")
    if BEGIN in text and END in text:
        new = DEPLOY_REGION_WITH_SENTINELS.sub(
            deploy_block.rstrip() + "\n", text, count=1
        )
        action = "replaced (sentinels)"
    else:
        m = DEPLOY_REGION.search(text)
        if not m:
            return (False, "no deploy region found")
        new = text[: m.start()] + deploy_block + text[m.end():]
        action = "replaced (region)"
    if new == text:
        return (False, "no-op")
    path.write_text(new, encoding="utf-8")
    return (True, action)


def main() -> int:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    counters = {}
    total = 0
    missing = []
    for entry in catalog:
        sid = entry["id"]
        src = FEEDERS / sid
        if not src.exists():
            continue
        deploy = render_deploy(entry)
        readme = src / "README.md"
        changed, action = upsert_deploy(readme, deploy)
        counters[action] = counters.get(action, 0) + 1
        if changed:
            total += 1
        if action == "no deploy region found":
            missing.append(sid)
    print(f"Updated {total} READMEs. Actions:")
    for a, n in sorted(counters.items()):
        print(f"  {a}: {n}")
    if missing:
        print("\nSources with no deploy region detected (need manual treatment):")
        for s in missing:
            print(f"  - {s}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
