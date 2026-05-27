# Entur Norway SIRI feeder

Companion docs:

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://entur.no/>
- API / data documentation: <https://developer.entur.org/>

<!-- upstream-links:end -->

- [CONTAINER.md](CONTAINER.md) — container images, runtime configuration, and ARM deployments.
- [EVENTS.md](EVENTS.md) — CloudEvents contracts, schemas, and routing metadata.

> [!NOTE]
> Entur data is published under NLOD. Keep attribution and license obligations in downstream use.

## Why this bridge

This bridge ingests **Entur real-time SIRI ET/VM/SX feeds** and republishes normalized CloudEvents so downstream systems subscribe instead of implementing and maintaining custom source clients.

- Power national or regional public-transport situation rooms with one feed.
- Blend ETA predictions, vehicle positions, and disruption notices in near real time.
- Feed transit analytics and passenger-information systems from a normalized contract.
- Stream alerts and journey updates into Eventhouse/Fabric for SLA and reliability tracking.
- Reduce bespoke API polling and SIRI parsing in downstream services.

## Overview

| Variant | Dockerfile | Image | Default delivery shape |
|---|---|---|---|
| Kafka | `Dockerfile` | `ghcr.io/clemensv/real-time-sources-entur-norway:latest` | CloudEvents to Kafka-compatible endpoints |
| MQTT | `Dockerfile.mqtt` | `ghcr.io/clemensv/real-time-sources-entur-norway-mqtt:latest` | CloudEvents over MQTT 5.0 topic hierarchy |
| AMQP | `Dockerfile.amqp` | `ghcr.io/clemensv/real-time-sources-entur-norway-amqp:latest` | CloudEvents over AMQP 1.0 address |

All variants share:

- The same upstream acquisition logic and normalization model.
- The same xRegistry contract in `xreg/`.
- The same event-family semantics documented in [EVENTS.md](EVENTS.md).

## Key features

- Publishes ET, VM, and SX families as CloudEvents.
- Consistent contract across Kafka, MQTT, and AMQP builds.
- Supports batching/pagination controls for Entur payloads.
- Ready for Event Hubs/Fabric connection-string deployments.

## Repository layout

```text
entur-norway/
  xreg/entur-norway.xreg.json
  entur_norway/
  entur_norway_amqp/
  entur_norway_mqtt/
  tests/
  Dockerfile
  Dockerfile.mqtt
  Dockerfile.amqp
  README.md
  CONTAINER.md
  EVENTS.md
```

## Prerequisites

- Docker 20.10+ (or compatible OCI runtime).
- Outbound connectivity to the upstream source endpoint(s).
- Network access to your target messaging broker (Kafka, MQTT, or AMQP).

## Quick start with Docker

### Kafka
```bash
docker run --rm \
  -e CONNECTION_STRING="<connection-string>" \
  ghcr.io/clemensv/real-time-sources-entur-norway:latest
```

### MQTT
```bash
docker run --rm \
  -e MQTT_BROKER_URL="mqtts://<broker>:8883" -e MQTT_USERNAME="<user>" -e MQTT_PASSWORD="<password>" \
  ghcr.io/clemensv/real-time-sources-entur-norway-mqtt:latest
```

### AMQP
```bash
docker run --rm \
  -e AMQP_BROKER_URL="amqp://<user>:<password>@<broker>:5672/entur-norway" \
  ghcr.io/clemensv/real-time-sources-entur-norway-amqp:latest
```

## Configuration reference

Use [CONTAINER.md](CONTAINER.md) for the full per-image variable matrix. Commonly used knobs:

- **Kafka image:** `CONNECTION_STRING`, `KAFKA_ENABLE_TLS`, `POLLING_INTERVAL`, `STATE_FILE`, `MAX_SIZE`
- **MQTT image:** `MQTT_BROKER_URL`, `MQTT_USERNAME`, `MQTT_PASSWORD`, `MQTT_CLIENT_ID`, `MQTT_CONTENT_MODE`
- **AMQP image:** `AMQP_BROKER_URL`, `AMQP_ADDRESS`, `AMQP_AUTH_MODE`, `AMQP_ENTRA_CLIENT_ID`, `AMQP_SAS_KEY_NAME / AMQP_SAS_KEY`

## Data model

- `no.entur.journeys.DatedServiceJourney` — reference journey context.
- `no.entur.journeys.EstimatedVehicleJourney` — ETA and prediction updates.
- `no.entur.journeys.MonitoredVehicleJourney` — live vehicle monitoring data.
- `no.entur.situations.PtSituationElement` — disruption and situation messages.


Primary message groups in xRegistry: `no.entur.journeys`, `no.entur.situations`.

## Deploying into Microsoft Fabric

For this streaming-style bridge, deploy the container via the **Fabric ACI** path:

```powershell
tools/deploy-fabric/deploy-fabric-aci.ps1 -Source entur-norway -ResourceGroup <rg> -Location <azure-region> -Workspace <fabric-workspace>
```

The script provisions the Fabric Eventhouse, applies the source KQL schema when the source checks one in, creates the Event Stream custom endpoint, and deploys the Azure Container Instance with the resulting connection string wired into the feeder container.

## Deploying into Azure Container Instances

ARM templates currently present in this source folder:

- `azure-template-with-eventhub.json` — Kafka deployment plus Azure Event Hubs provisioning
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fentur-norway%2Fazure-template-with-eventhub.json)
- `azure-template-with-servicebus.json` — AMQP deployment plus Azure Service Bus provisioning
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fentur-norway%2Fazure-template-with-servicebus.json)
- `azure-template.json` — Kafka deployment targeting an existing Kafka/Event Hubs endpoint
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fentur-norway%2Fazure-template.json)

## Next steps

- Review [EVENTS.md](EVENTS.md) before implementing consumers.
- Select the transport image that matches your broker and auth model.
- Use [CONTAINER.md](CONTAINER.md) for complete runtime and deployment options.
