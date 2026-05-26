# Ticketmaster Discovery API feeder

Companion docs:

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://www.ticketmaster.com/>
- API / data documentation: <https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/>

<!-- upstream-links:end -->

- [CONTAINER.md](CONTAINER.md) — container images, runtime configuration, and ARM deployments.
- [EVENTS.md](EVENTS.md) — CloudEvents contracts, schemas, and routing metadata.

> [!WARNING]
> You are responsible for complying with Ticketmaster Terms, branding rules, and rate limits when using or redistributing this data.

## Why this bridge

This bridge ingests **Ticketmaster Discovery API v2** and republishes normalized CloudEvents so downstream systems subscribe instead of implementing and maintaining custom source clients.

- Stream event listings and reference entities from Ticketmaster into one contract.
- Power event-search and recommendation features with frequent refreshes.
- Track venue, attraction, and classification reference changes alongside events.
- Push Ticketmaster data into Fabric/Eventhouse for operational analytics.
- Apply market filters centrally instead of in every consumer service.

## Overview

| Variant | Dockerfile | Image | Default delivery shape |
|---|---|---|---|
| Kafka | `Dockerfile` | `ghcr.io/clemensv/real-time-sources-ticketmaster:latest` | CloudEvents to Kafka-compatible endpoints |
| MQTT | `Dockerfile.mqtt` | `ghcr.io/clemensv/real-time-sources-ticketmaster-mqtt:latest` | CloudEvents over MQTT 5.0 topic hierarchy |
| AMQP | `Dockerfile.amqp` | `ghcr.io/clemensv/real-time-sources-ticketmaster-amqp:latest` | CloudEvents over AMQP 1.0 address |

All variants share:

- The same upstream acquisition logic and normalization model.
- The same xRegistry contract in `xreg/`.
- The same event-family semantics documented in [EVENTS.md](EVENTS.md).

## Key features

- Emits event telemetry plus reference entities (venue, attraction, classification, info).
- Supports rich Discovery API filter surface via env vars.
- Shared event model across Kafka, MQTT, and AMQP container variants.
- Configurable poll and reference refresh intervals.

## Repository layout

```text
ticketmaster/
  xreg/ticketmaster.xreg.json
  ticketmaster/
  ticketmaster_amqp/
  ticketmaster_mqtt/
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
  -e TICKETMASTER_API_KEY="<api-key>" -e CONNECTION_STRING="<connection-string>" \
  ghcr.io/clemensv/real-time-sources-ticketmaster:latest
```

### MQTT
```bash
docker run --rm \
  -e TICKETMASTER_API_KEY="<api-key>" -e MQTT_BROKER_URL="mqtts://<broker>:8883" -e MQTT_USERNAME="<user>" -e MQTT_PASSWORD="<password>" \
  ghcr.io/clemensv/real-time-sources-ticketmaster-mqtt:latest
```

### AMQP
```bash
docker run --rm \
  -e TICKETMASTER_API_KEY="<api-key>" -e AMQP_BROKER_URL="amqp://<user>:<password>@<broker>:5672/ticketmaster" \
  ghcr.io/clemensv/real-time-sources-ticketmaster-amqp:latest
```

## Configuration reference

Use [CONTAINER.md](CONTAINER.md) for the full per-image variable matrix. Commonly used knobs:

- **Kafka image:** `TICKETMASTER_API_KEY`, `CONNECTION_STRING or KAFKA_BOOTSTRAP_SERVERS`, `KAFKA_TOPIC`, `COUNTRY_CODES`, `POLL_INTERVAL`, `REFERENCE_REFRESH`, `STATE_FILE`, `KAFKA_ENABLE_TLS`
- **MQTT image:** `TICKETMASTER_API_KEY`, `MQTT_BROKER_URL`, `MQTT_USERNAME`, `MQTT_PASSWORD`, `MQTT_CLIENT_ID`, `COUNTRY_CODES`
- **AMQP image:** `TICKETMASTER_API_KEY`, `AMQP_BROKER_URL`, `AMQP_ADDRESS`, `AMQP_AUTH_MODE`, `COUNTRY_CODES`

## Data model

- `Ticketmaster.Events.Event` — event telemetry listings.
- `Ticketmaster.Reference.Venue` / `Attraction` / `Classification` / `Info` — reference entities.


Primary message groups in xRegistry: `Ticketmaster.Events`, `Ticketmaster.Reference`.

## Deploying into Microsoft Fabric

For this streaming-style bridge, deploy the container via the **Fabric ACI** path:

```powershell
tools/deploy-fabric/deploy-fabric-aci.ps1 -Source ticketmaster -WorkspaceId <id> -CapacityId <id>
```

## Deploying into Azure Container Instances

ARM templates currently present in this source folder:

- `azure-template-amqp.json` — AMQP deployment targeting an existing AMQP 1.0 broker
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fticketmaster%2Fazure-template-amqp.json)
- `azure-template-mqtt.json` — MQTT deployment targeting an existing MQTT broker
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fticketmaster%2Fazure-template-mqtt.json)
- `azure-template-with-eventgrid-mqtt.json` — MQTT deployment plus Azure Event Grid namespace broker provisioning
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fticketmaster%2Fazure-template-with-eventgrid-mqtt.json)
- `azure-template-with-eventhub.json` — Kafka deployment plus Azure Event Hubs provisioning
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fticketmaster%2Fazure-template-with-eventhub.json)
- `azure-template-with-servicebus.json` — AMQP deployment plus Azure Service Bus provisioning
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fticketmaster%2Fazure-template-with-servicebus.json)
- `azure-template.json` — Kafka deployment targeting an existing Kafka/Event Hubs endpoint
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fticketmaster%2Fazure-template.json)

## Next steps

- Review [EVENTS.md](EVENTS.md) before implementing consumers.
- Select the transport image that matches your broker and auth model.
- Use [CONTAINER.md](CONTAINER.md) for complete runtime and deployment options.
