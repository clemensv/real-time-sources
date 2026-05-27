<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/un.png" alt="Global" width="64" height="48"><br>
<sub><b>Global</b></sub>
</td>
<td valign="middle">

# GDACS

<sub>earthquakes, floods, cyclones, volcanoes, droughts · Kafka · MQTT · AMQP · <a href="https://www.gdacs.org/">upstream</a> · <a href="https://www.gdacs.org/xml/rss.xml">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-3_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Global — earthquakes, floods, cyclones, volcanoes, droughts

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#gdacs) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/gdacs.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://www.gdacs.org/)

</td></tr></table>
<!-- source-hero:end -->

## Overview

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://www.gdacs.org/>
- API / data documentation: <https://www.gdacs.org/xml/rss.xml>

<!-- upstream-links:end -->

**GDACS** is a bridge that polls the [Global Disaster Alert and Coordination
System](https://www.gdacs.org) RSS feed to fetch real-time disaster alert data.
The bridge converts alerts into [CloudEvents](https://cloudevents.io/) structured
JSON format and publishes them to Kafka, Azure Event Hubs, or Microsoft Fabric
Event Streams.

GDACS aggregates disaster information from multiple scientific sources worldwide,
covering six event types: earthquakes (EQ), tropical cyclones (TC), floods (FL),
volcanic eruptions (VO), forest fires (FF), and droughts (DR). The RSS feed
typically contains ~220 items and is updated within minutes of event detection.
No API key is required.

## Key Features

- **Multi-hazard coverage**: Earthquakes, tropical cyclones, floods, volcanoes, forest fires, and droughts in a single feed.
- **Episode-level tracking**: State file tracks each event+episode combination by version number — only new or updated episodes are emitted.
- **Three-tier alert levels**: Green (low), Orange (moderate), Red (high humanitarian impact).
- **Kafka integration**: Sends disaster alerts as CloudEvents, supporting Azure Event Hubs and Fabric Event Streams.

## Installation

The tool is written in Python and requires Python 3.10 or later.

### From Source

```bash
git clone https://github.com/clemensv/real-time-sources.git
cd real-time-sources/gdacs
pip install .
```

For a containerized deployment, see [CONTAINER.md](CONTAINER.md).

## How to Use

After installation, the bridge can be run with `python -m gdacs`.

### With Azure Event Hubs or Fabric Event Streams

```bash
python -m gdacs --connection-string '<connection-string>'
```

### With a Kafka Broker

```bash
python -m gdacs \
    --bootstrap-servers '<kafka-bootstrap-servers>' \
    --topic 'gdacs' \
    --sasl-username '<username>' \
    --sasl-password '<password>'
```

### One-shot Mode

Poll once and exit (useful for testing or scheduled runs):

```bash
python -m gdacs --connection-string '<connection-string>' --once
```

## Environment Variables

| Variable | Description |
|---|---|
| `CONNECTION_STRING` or `GDACS_CONNECTION_STRING` | Azure Event Hubs / Fabric Event Stream connection string |
| `KAFKA_BOOTSTRAP_SERVERS` | Comma-separated list of Kafka bootstrap servers |
| `KAFKA_TOPIC` | Kafka topic name |
| `SASL_USERNAME` | SASL PLAIN username |
| `SASL_PASSWORD` | SASL PLAIN password |
| `GDACS_STATE_FILE` | Path to state file for tracking seen events (default: `~/.gdacs_state.json`) |
| `LOG_LEVEL` | Logging level (default: `INFO`) |
| `KAFKA_ENABLE_TLS` | Enable TLS for Kafka (default: `true`) |

## CLI Arguments

| Argument | Description |
|---|---|
| `--connection-string` | Azure Event Hubs or Fabric Event Stream connection string |
| `--bootstrap-servers` | Comma-separated Kafka bootstrap servers |
| `--topic` | Kafka topic |
| `--sasl-username` | SASL PLAIN username |
| `--sasl-password` | SASL PLAIN password |
| `--state-file` | Path to persist seen-event state |
| `--poll-interval` | Polling interval in seconds (default: 300) |
| `--once` | Poll once and exit |
| `--log-level` | Logging level |

## Events

The event format is documented in [EVENTS.md](EVENTS.md).

## Testing

Run the unit tests:

```bash
cd gdacs
pip install pytest pytest-asyncio
python -m pytest tests/ -v
```

## Data Source

- **Provider**: [GDACS](https://www.gdacs.org) — a joint UN/European Commission initiative
- **Feed**: `https://www.gdacs.org/xml/rss.xml`
- **Update frequency**: Within minutes of event detection
- **Authentication**: None required
- **License**: Public data for humanitarian use

<!-- source-deploy:begin -->
## Deploy

The portal buttons wrap the underlying scripts and ARM templates documented below; pick the path that matches your destination and operational preference. Every route lands in the same Eventhouse / KQL schema if you want one — they only differ in where the feeder container or notebook runs.

### Deploying into Microsoft Fabric

GDACS targets Microsoft Fabric end-to-end: events land in a Fabric **Event Stream** (custom endpoint), an attached **Eventhouse / KQL database** materializes the contract from [`kql/`](kql/).

Use the deploy button on the [project portal](https://clemensv.github.io/real-time-sources#gdacs) to launch the Fabric ACI hosting model — it walks you through Fabric workspace selection and follow-up steps.

#### Fabric ACI feeder &nbsp;<sub><i>(continuous container hosting against a Fabric Event Stream)</i></sub>

A long-running Azure Container Instance hosts the container image and writes into a Fabric Event Stream custom endpoint. Use this for continuous polling, real-time MQTT/UNS publishing, or the AMQP transport — anything that does not fit a scheduled-notebook model.

```powershell
tools/deploy-fabric/deploy-fabric-aci.ps1 `
  -Source gdacs `
  -Workspace <fabric-workspace-id-or-name> `
  -ResourceGroup <azure-rg> `
  -Location <azure-region>
```

The script creates the Eventhouse, the KQL database with the [`kql/`](kql/) schema and update policies, the Event Stream with a custom endpoint, the ACI with the connection string wired in, and a storage account / file share mounted at `/state` for dedupe persistence.

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources#gdacs/fabric-aci)


### Deploying into Azure Container Instances

3 one-click deployment templates — one per realistic Azure target. These templates host the container directly in Azure (without a Fabric workspace) and target an Azure Event Hubs namespace, an MQTT broker, or an AMQP 1.0 peer. All templates create a storage account and file share for persistent dedupe state.

#### Kafka — bring your own Event Hub / Kafka

Deploy the Kafka container with your own Azure Event Hubs or Fabric Event Stream connection string. You pass the connection string at deploy time; the template provisions only the container and a storage account for persistent dedupe state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgdacs%2Fazure-template.json)

#### Kafka — provision a new Event Hub

Deploy the Kafka container together with a new Event Hubs namespace (Standard SKU, 1 throughput unit) and event hub. The connection string is wired automatically.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgdacs%2Fazure-template-with-eventhub.json)

#### AMQP — provision a new Azure Service Bus namespace

Deploy the AMQP container together with a new [Azure Service Bus Standard namespace](https://learn.microsoft.com/azure/service-bus-messaging/service-bus-messaging-overview) with a queue, a user-assigned managed identity, and the **Azure Service Bus Data Sender** role assignment. The feeder authenticates via AMQP CBS put-token with Microsoft Entra ID — no SAS key rotation required.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgdacs%2Fazure-template-with-servicebus.json)


### Self-hosted

Pull and run any of the 3 container images directly — laptop, Kubernetes, Azure Container Apps, Cloud Run, ECS, bare metal. The full per-transport / per-auth-mode environment-variable matrix and sample `docker run` commands for every target broker live in [CONTAINER.md](CONTAINER.md).
<!-- source-deploy:end -->
## Transports

This source now ships separate Kafka and MQTT containers over the same xRegistry contract. The Kafka image is the best fit when consumers need replay, batch catch-up, or a single ordered stream. The MQTT image (`ghcr.io/clemensv/real-time-sources-gdacs-mqtt:latest`) is the better fit for operational dashboards and Unified Namespace subscribers that want to subscribe directly to the current state or live event slice for this source.

The MQTT contract is source-specific: MQTT/5.0 transport variant for GDACS disaster alerts. Non-retained QoS-1 alert events route by disaster event type, event-level GDACS alert color, affected country, and event id under alerts/intl/gdacs/gdacs/... GDACS is both provider and source in this single-feed namespace branch; subscribe with wildcards across the color axis to follow episode-level alert transitions.

MQTT publishes binary-mode CloudEvents with JSON payloads and CloudEvent attributes in MQTT 5 user properties. Topic patterns from `xreg/gdacs.xreg.json`:

| Topic pattern | Message type | Delivery |
|---|---|---|
| `alerts/intl/gdacs/gdacs/{event_type}/{alert_color}/{country}/{event_id}/alert` | `GDACS.DisasterAlert` | QoS 1, retain=false |

Four Azure Container Instance deployment shapes are documented for this source:

| Transport | Template |
|---|---|
| Kafka, bring your own Event Hub or compatible broker | `azure-template.json` |
| Kafka, create an Event Hubs namespace and hub | `azure-template-with-eventhub.json` |
| MQTT, bring your own MQTT 5 broker | `azure-template-mqtt.json` |
| MQTT, create an Azure Event Grid namespace MQTT broker | `azure-template-with-eventgrid-mqtt.json` |

See [CONTAINER.md](CONTAINER.md) for runtime environment variables and deployment badges, and [EVENTS.md](EVENTS.md) for the full CloudEvents and MQTT topic contract.

## AMQP 1.0 companion

This source also ships an AMQP 1.0 companion feeder (`Dockerfile.amqp`) alongside the Kafka and MQTT variants. It publishes the same CloudEvents to a single AMQP address named after the source, with CloudEvent `subject` and AMQP application properties mirroring the Kafka key/MQTT topic axes for broker-side filtering. Use `azure-template-with-servicebus.json` to deploy the AMQP feeder to Azure Service Bus with Entra ID/CBS authentication, or set `AMQP_BROKER_URL` for a generic AMQP 1.0 broker.
