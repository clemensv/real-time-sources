# Tokyo Docomo Bikeshare feeder

Companion docs:

- [CONTAINER.md](CONTAINER.md) — container images, runtime configuration, and ARM deployments.
- [EVENTS.md](EVENTS.md) — CloudEvents contracts, schemas, and routing metadata.

## Why this bridge

This bridge ingests **Tokyo Docomo Bikeshare GBFS feed via ODPT** and republishes normalized CloudEvents so downstream systems subscribe instead of implementing and maintaining custom source clients.

- Build station-availability dashboards for bike-share operations in Tokyo.
- Trigger mobility workflows when stations run low on bikes or docks.
- Ingest bike-share status into Fabric/Eventhouse without building custom pollers.
- Correlate bike-share utilization with weather, transit, or event demand.
- Feed low-latency APIs and map experiences from one normalized stream.

## Overview

| Variant | Dockerfile | Image | Default delivery shape |
|---|---|---|---|
| Kafka | `Dockerfile` | `ghcr.io/clemensv/real-time-sources-tokyo-docomo-bikeshare:latest` | CloudEvents to Kafka-compatible endpoints |
| MQTT | `Dockerfile.mqtt` | `ghcr.io/clemensv/real-time-sources-tokyo-docomo-bikeshare-mqtt:latest` | CloudEvents over MQTT 5.0 topic hierarchy |
| AMQP | `Dockerfile.amqp` | `ghcr.io/clemensv/real-time-sources-tokyo-docomo-bikeshare-amqp:latest` | CloudEvents over AMQP 1.0 address |

All variants share:

- The same upstream acquisition logic and normalization model.
- The same xRegistry contract in `xreg/`.
- The same event-family semantics documented in [EVENTS.md](EVENTS.md).

## Key features

- Emits system, station metadata, and live station status as CloudEvents.
- Shared data contract across Kafka, MQTT, and AMQP variants.
- Connection-string support for Event Hubs/Fabric Event Streams.
- Transport-specific binaries with the same source model.

## Repository layout

```text
tokyo-docomo-bikeshare/
  xreg/tokyo-docomo-bikeshare.xreg.json
  tokyo_docomo_bikeshare/
  tokyo_docomo_bikeshare_amqp/
  tokyo_docomo_bikeshare_mqtt/
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
  ghcr.io/clemensv/real-time-sources-tokyo-docomo-bikeshare:latest
```

### MQTT
```bash
docker run --rm \
  -e MQTT_BROKER_URL="mqtts://<broker>:8883" -e MQTT_USERNAME="<user>" -e MQTT_PASSWORD="<password>" \
  ghcr.io/clemensv/real-time-sources-tokyo-docomo-bikeshare-mqtt:latest
```

### AMQP
```bash
docker run --rm \
  -e AMQP_BROKER_URL="amqp://<user>:<password>@<broker>:5672/tokyo-docomo-bikeshare" \
  ghcr.io/clemensv/real-time-sources-tokyo-docomo-bikeshare-amqp:latest
```

## Configuration reference

Use [CONTAINER.md](CONTAINER.md) for the full per-image variable matrix. Commonly used knobs:

- **Kafka image:** `CONNECTION_STRING`, `KAFKA_ENABLE_TLS`
- **MQTT image:** `MQTT_BROKER_URL`, `MQTT_USERNAME`, `MQTT_PASSWORD`, `MQTT_TLS`
- **AMQP image:** `AMQP_BROKER_URL or AMQP_HOST/AMQP_PORT/AMQP_ADDRESS`, `AMQP_USERNAME`, `AMQP_PASSWORD`, `AMQP_AUTH_MODE`

## Data model

- `JP.ODPT.DocomoBikeshare.BikeshareSystem` — operator/system reference data.
- `JP.ODPT.DocomoBikeshare.BikeshareStation` — station reference metadata.
- `JP.ODPT.DocomoBikeshare.BikeshareStationStatus` — live bike/dock availability telemetry.


Primary message groups in xRegistry: `JP.ODPT.DocomoBikeshare.System`, `JP.ODPT.DocomoBikeshare.Stations`.

## Deploying into Microsoft Fabric

For this streaming-style bridge, deploy the container via the **Fabric ACI** path:

```powershell
tools/deploy-fabric/deploy-fabric-aci.ps1 -Source tokyo-docomo-bikeshare -WorkspaceId <id> -CapacityId <id>
```

## Deploying into Azure Container Instances

ARM templates currently present in this source folder:

- `azure-template-mqtt.json` — MQTT deployment targeting an existing MQTT broker
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ftokyo-docomo-bikeshare%2Fazure-template-mqtt.json)
- `azure-template-with-eventgrid-mqtt.json` — MQTT deployment plus Azure Event Grid namespace broker provisioning
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ftokyo-docomo-bikeshare%2Fazure-template-with-eventgrid-mqtt.json)

## Next steps

- Review [EVENTS.md](EVENTS.md) before implementing consumers.
- Select the transport image that matches your broker and auth model.
- Use [CONTAINER.md](CONTAINER.md) for complete runtime and deployment options.
