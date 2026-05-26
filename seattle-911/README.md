# Seattle Fire 911 feeder

This feeder turns the City of Seattle's [Real Time Fire 911 Calls](https://data.seattle.gov/Public-Safety/Seattle-Real-Time-Fire-911-Calls/kzjm-xkqj) open-data feed into a real-time CloudEvents stream over Apache Kafka, MQTT 5.0 (Unified Namespace), or AMQP 1.0.

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://data.seattle.gov/>
- API / data documentation: <https://data.seattle.gov/Public-Safety/Call-Data/33kz-ixgy>

<!-- upstream-links:end -->

Companion docs:

- [CONTAINER.md](CONTAINER.md) — published container images, environment variables, and one-click Azure deployments.
- [EVENTS.md](EVENTS.md) — CloudEvents contract, schemas, and per-transport routing.

> [!IMPORTANT]
> This feed publishes raw operational dispatch records. It is **not** an official emergency-information service: do not use it to drive citizen-facing safety alerts or to substitute for SPD/SFD public-information channels. Honour the City of Seattle Open Data [Terms of Use](https://data.seattle.gov/stories/s/Data-Policy/6ukr-c5dv/) when redistributing.

## Why this bridge

The City of Seattle publishes the **Seattle Real Time Fire 911 Calls** dataset on `data.seattle.gov`, an authoritative live dispatch feed for the Seattle Fire Department. It is updated approximately every 5 minutes and exposes every incident — alarms, medical response, fires, rescues, hazmat, marine and aircraft incidents — with the dispatch-assigned `incident_number`, the dispatch time, the responding station, the incident type, and a redacted address with latitude / longitude. The feed is open and free, but it is a Socrata SODA REST API: every consumer ends up writing the same paged-poll, dedupe, schema-validation, retry and identity glue.

This feeder turns that REST API into a first-class real-time event stream so consumers can stop polling Socrata from inside their business systems and start subscribing to a topic:

- **City and emergency-management dashboards** — drive live incident maps, response-time KPIs, and shift-handover briefings off a normalized event stream that already shares an identity with the public dataset.
- **Public-safety research and journalism** — reproducible, queryable ingest of every dispatch event into a data lake or Eventhouse for response-time studies, equity analyses, and investigative reporting.
- **Operational analytics for SFD and partner agencies** — feed long-running ingestion into Microsoft Fabric Eventhouse / Azure Data Explorer for staffing, station-load, and incident-type trends across years.
- **Smart-city and IoT correlation** — combine dispatches with traffic, weather, and air-quality streams (e.g. neighbouring feeders in this repo) for cross-domain situational awareness.
- **Civic transparency and academic study** — publish a low-friction subscribable mirror of the city dataset for universities, civic-tech groups, and 311-style services.

The bridge does the boring work — paged Socrata polling with timestamp resume, state-file dedupe, JSON-Structure–validated CloudEvents, identity plumbing, retries — so the consumer just subscribes.

## Overview

**Seattle Fire 911** is a poll-based bridge that calls the Socrata SODA endpoint for the SFD live dispatch dataset and re-emits each new incident as a CloudEvent. The source ships in three transport variants from a single upstream poller:

| Variant | Container image | Transport | Default delivery shape |
|---|---|---|---|
| **Kafka** | `ghcr.io/clemensv/real-time-sources-seattle-911` | Apache Kafka 2.x compatible (incl. Azure Event Hubs, Microsoft Fabric Event Streams, Confluent Cloud) | One topic, JSON CloudEvents (binary mode), key = `{incident_number}` |
| **MQTT** | `ghcr.io/clemensv/real-time-sources-seattle-911-mqtt` | MQTT 5.0 broker (incl. Mosquitto, EMQX, HiveMQ, Azure Event Grid MQTT, Microsoft Fabric Real-Time Hub MQTT broker) | Unified-Namespace topic tree `civic-events/us/wa/seattle/public-safety/fire-dispatch/{incident_type_slug}/{incident_number}`, JSON body, CloudEvent attributes as MQTT 5 user properties, non-retained at QoS 1 with 24 h message expiry |
| **AMQP** | `ghcr.io/clemensv/real-time-sources-seattle-911-amqp` | AMQP 1.0 (RabbitMQ AMQP 1.0 plugin, ActiveMQ Artemis, Qpid Dispatch, Azure Service Bus, Azure Event Hubs, Azure Service Bus emulator) | Single AMQP node (queue/topic), binary CloudEvents, SASL PLAIN for generic brokers, Microsoft Entra ID via AMQP CBS for Service Bus / Event Hubs, or SAS-token CBS for the emulator and SAS-only namespaces |

All three variants share:

* The upstream poller (`seattle_911` package).
* The xRegistry contract (`xreg/seattle-911.xreg.json`).
* The single CloudEvents schema for `Incident`.

## Key features

- **Live dispatch firehose** — every Seattle Fire Department 911 incident published by the City of Seattle, typically within one poll cycle of the dataset refresh.
- **Paged Socrata polling with timestamp resume** — picks up where it left off after a restart instead of reprocessing the dataset from scratch.
- **Three transport binaries** sharing the same upstream poller and the same single event family — switch transport without changing the data model.
- **Incident-type-aware MQTT routing** — the MQTT topic tree carries an `{incident_type_slug}` segment derived deterministically from the upstream `incident_type`, so subscribers can wildcard by `medical-response`, `fire`, `aid-response`, etc.
- **Azure Event Hubs / Microsoft Fabric Event Streams** ready via standard connection strings (Kafka variant).
- **Unified Namespace** ready out of the box with MQTT 5.0 binary CloudEvents and a civic-rooted topic tree (MQTT variant).
- **Azure Service Bus / Event Hubs over AMQP 1.0 with Microsoft Entra ID** (no SAS-key rotation) via the AMQP variant's CBS put-token flow, plus SAS-token CBS for the Service Bus emulator and SAS-only namespaces.

## Repository layout

```text
seattle-911/
  xreg/seattle-911.xreg.json     # shared xRegistry contract
  seattle_911/                   # Socrata poller + Kafka feeder application
  seattle_911_mqtt/              # MQTT/UNS feeder application
  seattle_911_amqp/              # AMQP 1.0 feeder application
  seattle_911_producer/          # xRegistry-generated Kafka producer
  seattle_911_mqtt_producer/     # xRegistry-generated MQTT producer
  seattle_911_amqp_producer/     # xRegistry-generated AMQP producer
  Dockerfile                     # builds the Kafka feeder image
  Dockerfile.mqtt                # builds the MQTT feeder image
  Dockerfile.amqp                # builds the AMQP feeder image
  kql/                           # Eventhouse / KQL schema and update policies
  notebook/                      # Fabric notebook feeder (scheduled in-Fabric)
  tests/                         # unit + integration tests
```

## Prerequisites

- Docker 20.10+ (or any OCI-compatible runtime).
- Outbound HTTPS to `data.seattle.gov` (the upstream Socrata API; no credentials required).
- Network access to your target Kafka broker, MQTT broker, or AMQP 1.0 peer.
- A writable host directory mounted into the container at `/state` to persist the dedupe / resume state file across restarts. Without it the bridge restarts cold on every container start and will republish records it has already emitted.

## Quick start with Docker

> [!IMPORTANT]
> Always mount a volume for `SEATTLE_911_LAST_POLLED_FILE`. The default path lives inside the container's filesystem and is lost on restart, which silently disables cross-restart deduplication and resume. The examples below mount the host directory `./state` into `/state`.

### Kafka

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e SEATTLE_911_LAST_POLLED_FILE=/state/seattle-911.json \
  -e CONNECTION_STRING="<event-hubs-connection-string>" \
  ghcr.io/clemensv/real-time-sources-seattle-911:latest
```

Replace `<event-hubs-connection-string>` with a connection string from your Azure Event Hubs namespace, Microsoft Fabric Event Stream custom endpoint, or any Kafka 2.x broker that accepts the same SASL-PLAIN-over-TLS shape.

### MQTT (Unified Namespace)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e SEATTLE_911_LAST_POLLED_FILE=/state/seattle-911.json \
  -e MQTT_BROKER_URL=mqtts://<broker-host>:8883 \
  -e MQTT_USERNAME=<username> \
  -e MQTT_PASSWORD=<password> \
  ghcr.io/clemensv/real-time-sources-seattle-911-mqtt:latest
```

Topics published (non-retained, QoS 1, 24 h message expiry):

```text
civic-events/us/wa/seattle/public-safety/fire-dispatch/{incident_type_slug}/{incident_number}
```

`{incident_type_slug}` is a deterministic lowercase kebab slug derived from the upstream `incident_type` display string (`Medical Response` → `medical-response`, `Aid Response Yellow` → `aid-response-yellow`); `{incident_number}` is the dispatch-assigned incident identifier and matches the CloudEvents `subject` / Kafka key. Subscribe with `civic-events/us/wa/seattle/public-safety/fire-dispatch/medical-response/#` for medical incidents only, or with `civic-events/us/wa/seattle/public-safety/fire-dispatch/+/+` for the entire firehose.

### AMQP 1.0

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e SEATTLE_911_LAST_POLLED_FILE=/state/seattle-911.json \
  -e AMQP_BROKER_URL='amqp://<user>:<password>@<broker-host>:5672/seattle-911' \
  ghcr.io/clemensv/real-time-sources-seattle-911-amqp:latest
```

For Azure Service Bus or Event Hubs with Microsoft Entra ID, the Service Bus emulator, or SAS-only namespaces, see [CONTAINER.md](CONTAINER.md#using-the-amqp-image) for the full environment-variable matrix.

## Configuration reference

The complete list of environment variables for every variant (Kafka, MQTT, AMQP), every authentication mode (SASL PLAIN, Microsoft Entra ID via CBS, SAS-token CBS), and every Azure deployment shape lives in [CONTAINER.md](CONTAINER.md). The runtime entry point for every image is `python -m seattle_911{,_mqtt,_amqp}`; the image's default `CMD` invokes it for you.

## Data model

The feeder emits a single event family:

- **`Incident`** — one Seattle Fire Department 911 dispatch record, keyed by `incident_number`.

The dataset does not publish a separate reference catalog for incident types or stations, so **no reference-data event type is emitted**. Field-level provenance, units, and known gaps are documented per-field in [EVENTS.md](EVENTS.md). Upstream fields explicitly dropped from the contract: `report_location` (duplicate geometry presentation of `latitude` / `longitude`) and the Socrata `:@computed_region_*` platform-derived fields (not authoritative incident attributes).

## Deploying into Microsoft Fabric

Seattle Fire 911 targets Microsoft Fabric end-to-end: events land in a Fabric **Event Stream** (custom endpoint), and an attached Eventhouse / KQL database materializes the contract from [`kql/`](kql/) with one table for `Incident` and update policies that decode the CloudEvent envelope.

Two hosting models are supported. **Use the deploy buttons on the [project portal](https://clemensv.github.io/real-time-sources/#seattle-911)** to launch either.

### Fabric Notebook feeder (recommended for this 5-minute polling cadence)

A scheduled Fabric Notebook ([`notebook/`](notebook/)) runs the poller inside the Fabric workspace itself, against a per-source Fabric **Environment** that bundles the `seattle_911` package and the generated producer sub-packages. The Event Stream custom endpoint connection string is looked up at runtime via the public Fabric Topology API using the workspace identity — no secrets in the notebook, no separate container host to manage. Resume state lives in OneLake under `/lakehouse/default/Files/feeder-state/seattle-911/`.

Deploy with `tools/deploy-fabric/deploy-feeder-notebook.ps1 -Source seattle-911 -WorkspaceId <id> -CapacityId <id>` (the portal button wraps this for you). Best fit for the dataset's ~5-minute refresh cadence; the notebook executes on a Fabric schedule and writes a per-run diagnostic log to OneLake.

[![Deploy Fabric Notebook](https://img.shields.io/badge/Fabric-Notebook%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources/#seattle-911/fabric-notebook)

### Fabric ACI feeder (recommended for MQTT / AMQP transports)

A long-running Azure Container Instance hosts one of the three container images and writes into the same Fabric Event Stream custom endpoint. Use this when you want continuous MQTT publishing for a Unified Namespace, the AMQP transport, or always-on Kafka delivery rather than the notebook's scheduled execution.

Deploy with `tools/deploy-fabric/deploy-fabric-aci.ps1 -Source seattle-911 -WorkspaceId <id> -CapacityId <id>` (the portal button wraps this for you). The script creates the Eventhouse, the KQL database with the [`kql/`](kql/) schema and update policies, the Event Stream with a custom endpoint, the ACI with the connection string wired in, and a storage account / file share mounted at `/state` for dedupe persistence.

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources/#seattle-911/fabric-aci)

## Deploying into Azure Container Instances

Three one-click deployment templates are available — one for each realistic Azure target. These templates host the container directly in Azure (without a Fabric workspace) and target an Azure Event Hubs namespace or an Azure Service Bus AMQP queue. All templates create a storage account and file share for persistent dedupe / resume state.

### Kafka — bring your own Event Hub / Kafka

Deploy the Kafka container with your own Azure Event Hubs or Fabric Event Stream connection string.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fseattle-911%2Fazure-template.json)

### Kafka — provision a new Event Hub

Deploy the Kafka container together with a new Event Hubs namespace (Standard SKU, 1 throughput unit) and event hub. The connection string is wired automatically.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fseattle-911%2Fazure-template-with-eventhub.json)

### AMQP — provision a new Azure Service Bus namespace

Deploy the AMQP container together with a new [Azure Service Bus Standard namespace](https://learn.microsoft.com/azure/service-bus-messaging/service-bus-messaging-overview) with a queue named `seattle-911`, a user-assigned managed identity, and the **Azure Service Bus Data Sender** role assignment. The feeder authenticates via AMQP CBS put-token with Microsoft Entra ID — no SAS key rotation required.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fseattle-911%2Fazure-template-with-servicebus.json)

## Next steps

- Pick a hosting model: a [Fabric Notebook or Fabric ACI feeder](#deploying-into-microsoft-fabric) if your destination is a Fabric workspace; a [direct Azure deployment](#deploying-into-azure-container-instances) if you target Event Hubs or Service Bus without Fabric.
- Review the [event contract and schemas](EVENTS.md) before writing a consumer.
- Look up authentication modes and the full environment-variable matrix in [CONTAINER.md](CONTAINER.md).
- The upstream dataset, refresh schedule, and field documentation live at [Seattle Real Time Fire 911 Calls on data.seattle.gov](https://data.seattle.gov/Public-Safety/Seattle-Real-Time-Fire-911-Calls/kzjm-xkqj); the [City of Seattle Open Data Policy](https://data.seattle.gov/stories/s/Data-Policy/6ukr-c5dv/) governs use and redistribution.
