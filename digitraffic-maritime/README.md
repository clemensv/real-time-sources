# Digitraffic Maritime feeder

This feeder turns the upstream Digitraffic Maritime feed into a real-time CloudEvents stream over KAFKA.

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://www.digitraffic.fi/en/marine-traffic/>
- API / data documentation: <https://meri.digitraffic.fi/swagger/>

<!-- upstream-links:end -->

Companion docs:

- [CONTAINER.md](CONTAINER.md) — published container images, environment variables, and one-click Azure deployments.
- [EVENTS.md](EVENTS.md) — CloudEvents contract, schemas, and per-transport routing.

## Why this bridge

Digitraffic Maritime publishes operational real-time data that is useful across hazard and mobility analytics workflows, but each consumer otherwise has to build and operate its own source connector, transport adapter, and schema normalization.

This bridge provides one reusable feed for common scenarios:

- **Operations dashboards** — power near-real-time fleet, traffic, or incident views.
- **Streaming analytics** — ingest directly into Eventhouse, ADX, or a lakehouse pipeline.
- **Cross-source correlation** — join this stream with weather, hydrology, and public-safety feeds in this repository.
- **Alerting and automation** — trigger rules based on stable CloudEvents payloads and keys.
- **Research and reporting** — keep a reproducible event archive for retrospective analysis.

## Overview

**Digitraffic Maritime** in this repository is a streaming bridge and ships in the transport variants below:

| Variant | Container image | Transport | Default delivery shape |
|---|---|---|---|
| **Kafka** | `ghcr.io/clemensv/real-time-sources-digitraffic-maritime` | Apache Kafka 2.x compatible (incl. Azure Event Hubs and Fabric Event Streams) | Topic(s): `digitraffic-maritime`, key = `{locode}`, `{mmsi}`, `{port_call_id}`, `{vessel_id}` |

All variants share:

- The xRegistry contract (`xreg/digitraffic_maritime.xreg.json`).
- A common upstream acquisition path and normalized event payloads.
- Stable CloudEvents subject/key identity derived from source-native identifiers.

## Key features

- Real-time source ingestion for **Finland / Baltic Sea — AIS via MQTT**.
- Contract-first CloudEvents output with JsonStructure schemas.
- Transport variants aligned to the same core event model.
- Deployment-ready container images for local, Azure, and Fabric-aligned topologies.

## Repository layout

```text
digitraffic-maritime/
  xreg/                           # xRegistry contracts
  digitraffic_maritime/
  digitraffic_maritime_producer/
  digitraffic_maritime_producer_data/
  fabric/
  kql/
  tests/
  Dockerfile
```

## Prerequisites

- Docker 20.10+ (or any OCI-compatible runtime).
- Network access to the upstream data endpoint(s).
- Network access to your target broker (Kafka, MQTT, or AMQP).

This source is handled as a streaming feeder in this batch; no notebook runtime section is included.

## Quick start with Docker

### Kafka

```bash
docker run --rm \
  -e CONNECTION_STRING="<event-hubs-or-fabric-connection-string>" \
  ghcr.io/clemensv/real-time-sources-digitraffic-maritime:latest
```

## Configuration reference

The complete environment-variable contract per image is documented in [CONTAINER.md](CONTAINER.md), including connection-string mode, direct broker parameters, authentication options, and transport-specific knobs.

## Data model

This source exposes **5 event type(s)** across **4 base message group(s)**:

- `fi.digitraffic.marine.ais.VesselLocation`
- `fi.digitraffic.marine.ais.VesselMetadata`
- `fi.digitraffic.marine.portcall.PortCall`
- `fi.digitraffic.marine.portcall.VesselDetails`
- `fi.digitraffic.marine.portcall.PortLocation`

See [EVENTS.md](EVENTS.md) for the full field-level schema contract and routing metadata.

## Deploying into Microsoft Fabric

Digitraffic Maritime targets Microsoft Fabric end-to-end: events land in a Fabric **Event Stream** (custom endpoint), and an attached Eventhouse / KQL database materializes the contract from [`kql/digitraffic_maritime.kql`](kql/digitraffic_maritime.kql).

This source's catalog entry is container-only (`notebook: false`), so the supported Fabric hosting model is the always-on **Fabric ACI feeder**.

### Fabric ACI feeder

Deploy with `tools/deploy-fabric/deploy-fabric-aci.ps1 -Source digitraffic-maritime -ResourceGroup <rg> -Location <azure-region> -Workspace <fabric-workspace>` (the portal button wraps the same flow for you). The script provisions the Eventhouse, applies [`kql/digitraffic_maritime.kql`](kql/digitraffic_maritime.kql), creates the Event Stream custom endpoint, and deploys the Azure Container Instance with the resulting connection string wired into the feeder container.

If you want to inspect or re-run the Fabric-side bootstrap manually, see [`fabric/README.md`](fabric/README.md) plus the included [`fabric/setup.ps1`](fabric/setup.ps1) / [`fabric/setup.sh`](fabric/setup.sh) scripts.

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources/#digitraffic-maritime/fabric-aci)

## Deploying into Azure Container Instances

The following ARM templates exist in this source folder:

- **azure-template-with-eventhub.json** (with eventhub)
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdigitraffic-maritime%2Fazure-template-with-eventhub.json)
- **azure-template.json** (default (BYO Event Hubs/Kafka))
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdigitraffic-maritime%2Fazure-template.json)

## Next steps

- Review [EVENTS.md](EVENTS.md) before writing consumers.
- Use [CONTAINER.md](CONTAINER.md) for the full env-var matrix and auth variants.
- Choose Fabric ACI or direct Azure deployment based on your runtime target.
