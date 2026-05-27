# Fienta Public Events feeder

Companion docs:

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://fienta.com/>
- API / data documentation: <https://fienta.com/api-public-events>

<!-- upstream-links:end -->

- [CONTAINER.md](CONTAINER.md) — container images, runtime configuration, and ARM deployments.
- [EVENTS.md](EVENTS.md) — CloudEvents contracts, schemas, and routing metadata.

> [!IMPORTANT]
> Redistribution and downstream use must comply with [Fienta Terms of Service](https://fienta.com/terms).

## Why this bridge

This bridge ingests **Fienta public events API** and republishes normalized CloudEvents so downstream systems subscribe instead of implementing and maintaining custom source clients.

- Track public ticketed events and sale-status transitions across Fienta markets.
- Drive event-discovery and campaign workflows from near-real-time event changes.
- Observe sale lifecycle transitions (`onSale`, `soldOut`, `saleEnded`, etc.).
- Feed analytics platforms with both reference and sale-status telemetry events.
- Avoid rebuilding paging, polling, and status-dedupe logic in downstream apps.

## Overview

| Variant | Dockerfile | Image | Default delivery shape |
|---|---|---|---|
| Kafka | `Dockerfile` | `ghcr.io/clemensv/real-time-sources-fienta:latest` | CloudEvents to Kafka-compatible endpoints |
| MQTT | `Dockerfile.mqtt` | `ghcr.io/clemensv/real-time-sources-fienta-mqtt:latest` | CloudEvents over MQTT 5.0 topic hierarchy |
| AMQP | `Dockerfile.amqp` | `ghcr.io/clemensv/real-time-sources-fienta-amqp:latest` | CloudEvents over AMQP 1.0 address |

All variants share:

- The same upstream acquisition logic and normalization model.
- The same xRegistry contract in `xreg/`.
- The same event-family semantics documented in [EVENTS.md](EVENTS.md).

## Key features

- Emits full event reference records and sale-status change telemetry.
- Supports upstream country and locale filtering.
- Shared CloudEvents contract across Kafka, MQTT, and AMQP variants.
- State-based sale-status change detection for targeted telemetry.

## Repository layout

```text
fienta/
  xreg/fienta.xreg.json
  fienta/
  fienta_amqp/
  fienta_mqtt/
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
  -e CONNECTION_STRING="<connection-string>" -e FIENTA_COUNTRY="EE" -e FIENTA_LOCALE="en" \
  ghcr.io/clemensv/real-time-sources-fienta:latest
```

### MQTT
```bash
docker run --rm \
  -e MQTT_BROKER_URL="mqtts://<broker>:8883" -e MQTT_USERNAME="<user>" -e MQTT_PASSWORD="<password>" \
  ghcr.io/clemensv/real-time-sources-fienta-mqtt:latest
```

### AMQP
```bash
docker run --rm \
  -e AMQP_BROKER_URL="amqp://<user>:<password>@<broker>:5672/fienta" \
  ghcr.io/clemensv/real-time-sources-fienta-amqp:latest
```

## Configuration reference

Use [CONTAINER.md](CONTAINER.md) for the full per-image variable matrix. Commonly used knobs:

- **Kafka image:** `CONNECTION_STRING`, `KAFKA_ENABLE_TLS`, `FIENTA_STATE_FILE`, `FIENTA_COUNTRY`, `FIENTA_LOCALE`
- **MQTT image:** `MQTT_BROKER_URL`, `MQTT_USERNAME`, `MQTT_PASSWORD`, `MQTT_CLIENT_ID`, `FIENTA_COUNTRY`, `FIENTA_LOCALE`
- **AMQP image:** `AMQP_BROKER_URL`, `AMQP_ADDRESS`, `AMQP_AUTH_MODE`, `FIENTA_COUNTRY`, `FIENTA_LOCALE`

## Data model

- `Com.Fienta.Event` — public listing metadata (schedule, venue, organizer, links).
- `Com.Fienta.EventSaleStatus` — status transition telemetry with observed timestamps.


Primary message groups in xRegistry: `Com.Fienta`.

## Deploying into Microsoft Fabric

For this streaming-style bridge, deploy the container via the **Fabric ACI** path:

```powershell
tools/deploy-fabric/deploy-fabric-aci.ps1 -Source fienta -ResourceGroup <rg> -Location <azure-region> -Workspace <fabric-workspace>
```

The script provisions the Fabric Eventhouse, applies the source KQL schema when the source checks one in, creates the Event Stream custom endpoint, and deploys the Azure Container Instance with the resulting connection string wired into the feeder container.

## Deploying into Azure Container Instances

ARM templates currently present in this source folder:

- `azure-template-amqp.json` — AMQP deployment targeting an existing AMQP 1.0 broker
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffienta%2Fazure-template-amqp.json)
- `azure-template-mqtt.json` — MQTT deployment targeting an existing MQTT broker
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffienta%2Fazure-template-mqtt.json)
- `azure-template-with-eventgrid-mqtt.json` — MQTT deployment plus Azure Event Grid namespace broker provisioning
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffienta%2Fazure-template-with-eventgrid-mqtt.json)
- `azure-template-with-eventhub.json` — Kafka deployment plus Azure Event Hubs provisioning
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffienta%2Fazure-template-with-eventhub.json)
- `azure-template-with-servicebus.json` — AMQP deployment plus Azure Service Bus provisioning
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffienta%2Fazure-template-with-servicebus.json)
- `azure-template.json` — Kafka deployment targeting an existing Kafka/Event Hubs endpoint
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffienta%2Fazure-template.json)

## Next steps

- Review [EVENTS.md](EVENTS.md) before implementing consumers.
- Select the transport image that matches your broker and auth model.
- Use [CONTAINER.md](CONTAINER.md) for complete runtime and deployment options.
