# AISstream.io feeder

This feeder turns the global [AISstream.io](https://aisstream.io/) WebSocket firehose into a real-time CloudEvents stream over Apache Kafka, MQTT 5.0 (Unified Namespace), or AMQP 1.0.

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://aisstream.io/>
- API / data documentation: <https://aisstream.io/documentation>

<!-- upstream-links:end -->

Companion docs:

- [CONTAINER.md](CONTAINER.md) — published container images, environment variables, and one-click Azure deployments.
- [EVENTS.md](EVENTS.md) — CloudEvents contract, schemas, and per-transport routing.

> [!WARNING]
> **AISstream.io is a free, community-run service with no SLA.** During testing on 2026-04-02 the WebSocket accepted connections and API keys without error but delivered **zero messages** over sustained periods — the upstream pipeline behind the socket was simply dry. Silent outages lasting hours to days have been [reported by multiple users](https://github.com/aisstream/issues/issues/134). This feeder reconnects with exponential backoff, but you should expect data gaps. For reliable AIS coverage of Norwegian waters use the [Kystverket AIS feeder](../kystverket-ais/); for guaranteed global coverage use a commercial provider.

## Why this bridge

[AISstream.io](https://aisstream.io/) aggregates **terrestrial AIS** (Automatic Identification System) traffic from ground stations worldwide and delivers pre-decoded JSON for every standard ITU-R M.1371-5 message type — vessel positions, voyages, static identity, navigation aids, base stations, safety broadcasts, binary payloads, and protocol control — over a single WebSocket. Coverage is approximately **200 km from shore** wherever a community station is in range; satellite AIS is **not included**, so the open ocean is dark.

This bridge turns that firehose into a first-class real-time event stream so consumers can stop holding their own WebSocket and start subscribing to a topic:

- **Port operations and pilotage** — drive berth-availability dashboards, pilot dispatch, and tug scheduling from live AIS positions for vessels approaching your waters.
- **Maritime situational awareness** — feed naval / coast-guard plots, fisheries monitoring, and dark-vessel detection workflows with a normalized AIS stream.
- **Logistics and supply-chain ETA** — combine AIS positions with carrier schedules to compute live vessel ETAs into port terminals; close the loop on cargo and container tracking.
- **Environmental and emissions analytics** — long-running, ingestion-ready CloudEvents into Microsoft Fabric Eventhouse / Azure Data Explorer / a data lake for vessel-emissions modelling, MRV reporting, and shipping-route analysis.
- **Research and journalism** — reproducible, queryable ingest of global AIS for academic studies and investigative reporting on shipping behaviour.

The bridge does the boring work — WebSocket reconnect with exponential backoff, server-side and client-side filtering, JSON-Structure–validated CloudEvents, identity plumbing — so the consumer just subscribes.

## Overview

**AISstream** is a streaming bridge that holds an open WebSocket connection to AISstream.io and re-emits every received AIS message as a CloudEvent. The source ships in three transport variants from a single upstream WebSocket client:

| Variant | Container image | Transport | Default delivery shape |
|---|---|---|---|
| **Kafka** | `ghcr.io/clemensv/real-time-sources-aisstream` | Apache Kafka 2.x compatible (incl. Azure Event Hubs, Microsoft Fabric Event Streams, Confluent Cloud) | One topic, JSON CloudEvents (binary mode), key = `{mmsi}` |
| **MQTT** | `ghcr.io/clemensv/real-time-sources-aisstream-mqtt` | MQTT 5.0 broker (incl. Mosquitto, EMQX, HiveMQ, Azure Event Grid MQTT, Microsoft Fabric Real-Time Hub MQTT broker) | Unified-Namespace topic tree under `maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/{msg_type}`, JSON body, CloudEvent attributes as MQTT 5 user properties, non-retained at QoS 0 |
| **AMQP** | `ghcr.io/clemensv/real-time-sources-aisstream-amqp` | AMQP 1.0 (RabbitMQ AMQP 1.0 plugin, ActiveMQ Artemis, Qpid Dispatch, Azure Service Bus, Azure Event Hubs, Azure Service Bus emulator) | Single AMQP node (queue/topic), binary CloudEvents, SASL PLAIN for generic brokers, Microsoft Entra ID via AMQP CBS for Service Bus / Event Hubs, or SAS-token CBS for the emulator and SAS-only namespaces |

All three variants share:

* The upstream WebSocket client (`aisstream` package).
* The xRegistry contract (`xreg/aisstream.xreg.json`).
* CloudEvents schemas for all 23 ITU-R M.1371-5 message families (Kafka), or an enriched routing-friendly subset (MQTT).

## Key features

- **Global AIS coverage** — terrestrial AIS aggregated from community ground stations worldwide (~200 km from coast).
- **23 AIS event types** on the Kafka transport — every standard ITU-R M.1371-5 message family.
- **Server-side filtering** — geographic bounding boxes, MMSI lists, and message-type filters applied at the AISstream.io API.
- **Client-side MMSI filter** — additional local filter for fine-grained downstream control.
- **Auto-reconnect** — exponential backoff on WebSocket failures, critical given the service's reliability profile.
- **Three transport binaries** with identical configuration knobs upstream (API key, bounding boxes, filters) — switch transport without changing the data model.
- **Azure Event Hubs / Microsoft Fabric Event Streams** ready via standard connection strings (Kafka variant).
- **Unified Namespace** ready out of the box with MQTT 5.0 binary CloudEvents enriched with flag, ship-type bucket, and geohash5 routing axes (MQTT variant).
- **Azure Service Bus / Event Hubs over AMQP 1.0 with Microsoft Entra ID** (no SAS-key rotation) via the AMQP variant's CBS put-token flow, plus SAS-token CBS for the Service Bus emulator and SAS-only namespaces.

## Repository layout

```text
aisstream/
  xreg/aisstream.xreg.json       # shared xRegistry contract
  aisstream/                     # WebSocket client + Kafka feeder application
  aisstream_mqtt/                # MQTT/UNS feeder application (with enrichment)
  aisstream_amqp/                # AMQP 1.0 feeder application
  aisstream_producer/            # xRegistry-generated Kafka producer
  aisstream_mqtt_producer/       # xRegistry-generated MQTT producer
  aisstream_amqp_producer/       # xRegistry-generated AMQP producer
  Dockerfile                     # builds the Kafka feeder image
  Dockerfile.mqtt                # builds the MQTT feeder image
  Dockerfile.amqp                # builds the AMQP feeder image
  kql/aisstream.kql              # Eventhouse / KQL schema and update policies
  tests/                         # unit + integration tests
```

## Prerequisites

- Docker 20.10+ (or any OCI-compatible runtime).
- An AISstream.io API key — register at [aisstream.io](https://aisstream.io/) via GitHub OAuth (free).
- Outbound TLS (port 443) to `stream.aisstream.io`.
- Network access to your target Kafka broker, MQTT broker, or AMQP 1.0 peer.

This feeder is a pure streaming bridge — it holds an open WebSocket and forwards messages live. No local dedupe state is persisted, so no host volume is required.

## Quick start with Docker

### Kafka

```bash
docker run --rm \
  -e AISSTREAM_API_KEY="<aisstream-api-key>" \
  -e CONNECTION_STRING="<event-hubs-connection-string>" \
  ghcr.io/clemensv/real-time-sources-aisstream:latest
```

Replace `<event-hubs-connection-string>` with a connection string from your Azure Event Hubs namespace, Microsoft Fabric Event Stream custom endpoint, or any Kafka 2.x broker that accepts the same SASL-PLAIN-over-TLS shape.

### MQTT (Unified Namespace)

```bash
docker run --rm \
  -e AISSTREAM_API_KEY="<aisstream-api-key>" \
  -e MQTT_BROKER_URL=mqtts://<broker-host>:8883 \
  -e MQTT_USERNAME=<username> \
  -e MQTT_PASSWORD=<password> \
  ghcr.io/clemensv/real-time-sources-aisstream-mqtt:latest
```

Topics published (non-retained, QoS 0):

```text
maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/{msg_type}
```

`{flag}` is the ISO-3166-1 alpha-2 code derived from the MMSI MID, `{ship_type}` is a kebab bucket (`cargo`, `tanker`, `passenger`, …), `{geohash5}` is a 5-character geohash of the last known position, and `{msg_type}` is `position-report`, `static`, or `aid-to-navigation`. See [CONTAINER.md](CONTAINER.md#mqtt-image) for the full enrichment table.

### AMQP 1.0

```bash
docker run --rm \
  -e AISSTREAM_API_KEY="<aisstream-api-key>" \
  -e AMQP_BROKER_URL='amqp://<user>:<password>@<broker-host>:5672/aisstream' \
  ghcr.io/clemensv/real-time-sources-aisstream-amqp:latest
```

For Azure Service Bus or Event Hubs with Microsoft Entra ID, the Service Bus emulator, or SAS-only namespaces, see [CONTAINER.md](CONTAINER.md#using-the-amqp-image) for the full environment-variable matrix.

## Configuration reference

The complete list of environment variables for every variant (Kafka, MQTT, AMQP), every authentication mode (SASL PLAIN, Microsoft Entra ID via CBS, SAS-token CBS), every filter knob (bounding boxes, MMSI list, message-type allow-list, flush interval), and every Azure deployment shape lives in [CONTAINER.md](CONTAINER.md). The runtime entry point for every image is `python -m aisstream{,_mqtt,_amqp} stream`; the image's default `CMD` invokes it for you.

## AIS message types (Kafka transport)

The Kafka transport carries every standard ITU-R M.1371-5 AIS message family. The MQTT transport carries a routing-friendly subset (`PositionReport`, `ShipStatic`, `AidToNavigation`); see [CONTAINER.md](CONTAINER.md#mqtt-image) for why.

### Vessel position and movement

| Type name | AIS type | Description |
|---|---|---|
| `PositionReport` | 1, 2, 3 | Class A position reports (SOLAS vessels) |
| `StandardClassBPositionReport` | 18 | Class B CS position reports (smaller vessels) |
| `ExtendedClassBPositionReport` | 19 | Extended Class B position reports |
| `LongRangeAisBroadcastMessage` | 27 | Long-range AIS broadcast |
| `StandardSearchAndRescueAircraftReport` | 9 | SAR aircraft position |

### Vessel identity and static data

| Type name | AIS type | Description |
|---|---|---|
| `ShipStaticData` | 5 | Ship name, IMO, callsign, dimensions, destination |
| `StaticDataReport` | 24 | Class B static data (name, callsign, dimensions) |

### Infrastructure and safety

| Type name | AIS type | Description |
|---|---|---|
| `BaseStationReport` | 4 | Base station position and UTC time |
| `AidsToNavigationReport` | 21 | Buoys, lighthouses, navigational aids |
| `SafetyBroadcastMessage` | 14 | Safety-related text broadcasts |
| `AddressedSafetyMessage` | 12 | Addressed safety messages |

### Binary and data messages

| Type name | AIS type | Description |
|---|---|---|
| `AddressedBinaryMessage` | 6 | Addressed binary data |
| `BinaryBroadcastMessage` | 8 | Binary broadcast data |
| `SingleSlotBinaryMessage` | 25 | Single-slot binary |
| `MultiSlotBinaryMessage` | 26 | Multi-slot binary |
| `GnssBroadcastBinaryMessage` | 17 | GNSS corrections broadcast |

### Protocol and control

| Type name | AIS type | Description |
|---|---|---|
| `BinaryAcknowledge` | 7, 13 | Binary message acknowledgement |
| `Interrogation` | 15 | AIS interrogation |
| `AssignedModeCommand` | 16 | Assigned mode command |
| `DataLinkManagementMessage` | 20 | Data link management |
| `ChannelManagement` | 22 | Channel management |
| `GroupAssignmentCommand` | 23 | Group assignment |
| `CoordinatedUTCInquiry` | 10 | UTC inquiry |

## Deploying into Microsoft Fabric

AISstream targets Microsoft Fabric end-to-end: events land in a Fabric **Event Stream** (custom endpoint), and an attached Eventhouse / KQL database materializes the contract from [`kql/aisstream.kql`](kql/aisstream.kql) with one table per AIS message family and update policies that decode the CloudEvent envelope.

Because AISstream is a **streaming** source (open WebSocket), only the always-on Fabric ACI hosting model applies — the scheduled Fabric Notebook model used by poll-based feeders is not a fit for a long-lived WebSocket connection.

### Fabric ACI feeder

A long-running Azure Container Instance hosts one of the three container images and writes into a Fabric Event Stream custom endpoint. Use this whenever the destination is a Fabric workspace.

Deploy with `tools/deploy-fabric/deploy-fabric-aci.ps1 -Source aisstream -ResourceGroup <rg> -Location <azure-region> -Workspace <fabric-workspace>` (the portal button wraps this for you). The script creates the Eventhouse, the KQL database with the [`kql/aisstream.kql`](kql/aisstream.kql) schema and update policies, the Event Stream with a custom endpoint, and the ACI with the connection string and your AISstream.io API key wired in.

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources/#aisstream/fabric-aci)

## Deploying into Azure Container Instances

Three one-click deployment templates are available — one for each realistic Azure target. These templates host the container directly in Azure (without a Fabric workspace) and target an Azure Event Hubs namespace or an Azure Service Bus AMQP queue.

### Kafka — bring your own Event Hub / Kafka

Deploy the Kafka container with your own Azure Event Hubs or Fabric Event Stream connection string.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faisstream%2Fazure-template.json)

### Kafka — provision a new Event Hub

Deploy the Kafka container together with a new Event Hubs namespace (Standard SKU, 1 throughput unit) and event hub. The connection string is wired automatically.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faisstream%2Fazure-template-with-eventhub.json)

### AMQP — provision a new Azure Service Bus namespace

Deploy the AMQP container together with a new [Azure Service Bus Standard namespace](https://learn.microsoft.com/azure/service-bus-messaging/service-bus-messaging-overview) with a queue named `aisstream`, a user-assigned managed identity, and the **Azure Service Bus Data Sender** role assignment. The feeder authenticates via AMQP CBS put-token with Microsoft Entra ID — no SAS key rotation required.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faisstream%2Fazure-template-with-servicebus.json)

## Next steps

- Pick a hosting model: a [Fabric ACI feeder](#deploying-into-microsoft-fabric) if your destination is a Fabric workspace; a [direct Azure deployment](#deploying-into-azure-container-instances) if you target Event Hubs or Service Bus without Fabric.
- Review the [event contract and schemas](EVENTS.md) before writing a consumer.
- Look up authentication modes and the full environment-variable matrix in [CONTAINER.md](CONTAINER.md).
- The upstream API, terms of use, and registration flow live at the [AISstream.io portal](https://aisstream.io/); silent-outage history is tracked in [aisstream/issues#134](https://github.com/aisstream/issues/issues/134).
