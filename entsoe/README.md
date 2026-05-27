# ENTSO-E Transparency Platform feeder

Companion docs:

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://transparency.entsoe.eu/>
- API / data documentation: <https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html>

<!-- upstream-links:end -->

- [CONTAINER.md](CONTAINER.md) — container images, runtime configuration, and ARM deployments.
- [EVENTS.md](EVENTS.md) — CloudEvents contracts, schemas, and routing metadata.

## Why this bridge

This bridge ingests **ENTSO-E Transparency Platform REST API** and republishes normalized CloudEvents so downstream systems subscribe instead of implementing and maintaining custom source clients.

- Stream power-market transparency data into operational and analytical systems.
- Correlate load, generation, and cross-border flows in one event contract.
- Build market monitoring and forecasting pipelines over continuously refreshed data.
- Feed Fabric/Eventhouse with typed electricity-domain events.
- Replace repeated XML pull/parsing logic across consuming teams.

## Overview

| Variant | Dockerfile | Image | Default delivery shape |
|---|---|---|---|
| Kafka | `Dockerfile` | `ghcr.io/clemensv/real-time-sources-entsoe-kafka:latest` | CloudEvents to Kafka-compatible endpoints |
| MQTT | `Dockerfile.mqtt` | `ghcr.io/clemensv/real-time-sources-entsoe-mqtt:latest` | CloudEvents over MQTT 5.0 topic hierarchy |
| AMQP | `Dockerfile.amqp` | `ghcr.io/clemensv/real-time-sources-entsoe-amqp:latest` | CloudEvents over AMQP 1.0 address |

All variants share:

- The same upstream acquisition logic and normalization model.
- The same xRegistry contract in `xreg/`.
- The same event-family semantics documented in [EVENTS.md](EVENTS.md).

## Key features

- Covers by-domain, by-domain+PSR-type, and cross-border document families.
- Supports Kafka, MQTT/UNS, and AMQP outputs from the same acquisition core.
- Filterable domains, document types, and cross-border pairs.
- State-backed incremental polling with configurable lookback.

## Repository layout

```text
entsoe/
  xreg/entsoe.xreg.json
  entsoe/
  entsoe_amqp/
  entsoe_core/
  entsoe_kafka/
  entsoe_mqtt/
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
  -e ENTSOE_SECURITY_TOKEN="<token>" -e CONNECTION_STRING="<connection-string>" \
  ghcr.io/clemensv/real-time-sources-entsoe-kafka:latest
```

### MQTT
```bash
docker run --rm \
  -e ENTSOE_SECURITY_TOKEN="<token>" -e MQTT_BROKER_URL="mqtt://<broker>:1883" \
  ghcr.io/clemensv/real-time-sources-entsoe-mqtt:latest
```

### AMQP
```bash
docker run --rm \
  -e ENTSOE_SECURITY_TOKEN="<token>" -e AMQP_BROKER_URL="amqp://<user>:<password>@<broker>:5672/entsoe" \
  ghcr.io/clemensv/real-time-sources-entsoe-amqp:latest
```

## Configuration reference

Use [CONTAINER.md](CONTAINER.md) for the full per-image variable matrix. Commonly used knobs:

- **Kafka image:** `ENTSOE_SECURITY_TOKEN`, `CONNECTION_STRING or KAFKA_BOOTSTRAP_SERVERS`, `KAFKA_TOPIC`, `ENTSOE_DOMAINS`, `ENTSOE_DOCUMENT_TYPES`, `ENTSOE_CROSS_BORDER_PAIRS`, `POLLING_INTERVAL`, `STATE_FILE`
- **MQTT image:** `ENTSOE_SECURITY_TOKEN`, `MQTT_BROKER_URL`, `MQTT_AUTH_MODE`, `MQTT_USERNAME / MQTT_PASSWORD`, `MQTT_ENTRA_CLIENT_ID`
- **AMQP image:** `ENTSOE_SECURITY_TOKEN`, `AMQP_BROKER_URL`, `AMQP_ADDRESS`, `AMQP_AUTH_MODE`, `AMQP_ENTRA_CLIENT_ID`, `AMQP_SAS_KEY_NAME / AMQP_SAS_KEY`

## Data model

- `eu.entsoe.transparency.ByDomain.*` families (prices, load, forecasts, generation, reservoirs).
- `eu.entsoe.transparency.ByDomainPsrType.*` families (PSR-type specific generation/capacity).
- `eu.entsoe.transparency.CrossBorder.CrossBorderPhysicalFlows` telemetry.


Primary message groups in xRegistry: `eu.entsoe.transparency.ByDomain`, `eu.entsoe.transparency.ByDomainPsrType`, `eu.entsoe.transparency.CrossBorder`.

## Deploying into Microsoft Fabric

For this streaming-style bridge, deploy the container via the **Fabric ACI** path:

```powershell
tools/deploy-fabric/deploy-fabric-aci.ps1 -Source entsoe -ResourceGroup <rg> -Location <azure-region> -Workspace <fabric-workspace>
```

The script provisions the Fabric Eventhouse, applies the source KQL schema when the source checks one in, creates the Event Stream custom endpoint, and deploys the Azure Container Instance with the resulting connection string wired into the feeder container.

## Deploying into Azure Container Instances

ARM templates currently present in this source folder:

- `azure-template-amqp.json` — AMQP deployment targeting an existing AMQP 1.0 broker
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fentsoe%2Fazure-template-amqp.json)
- `azure-template-mqtt-eg.json` — MQTT deployment plus Azure Event Grid namespace broker provisioning
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fentsoe%2Fazure-template-mqtt-eg.json)
- `azure-template-mqtt.json` — MQTT deployment targeting an existing MQTT broker
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fentsoe%2Fazure-template-mqtt.json)
- `azure-template-with-eventgrid-mqtt.json` — MQTT deployment plus Azure Event Grid namespace broker provisioning
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fentsoe%2Fazure-template-with-eventgrid-mqtt.json)
- `azure-template-with-eventhub.json` — Kafka deployment plus Azure Event Hubs provisioning
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fentsoe%2Fazure-template-with-eventhub.json)
- `azure-template-with-servicebus.json` — AMQP deployment plus Azure Service Bus provisioning
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fentsoe%2Fazure-template-with-servicebus.json)
- `azure-template.json` — Kafka deployment targeting an existing Kafka/Event Hubs endpoint
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fentsoe%2Fazure-template.json)

## Next steps

- Review [EVENTS.md](EVENTS.md) before implementing consumers.
- Select the transport image that matches your broker and auth model.
- Use [CONTAINER.md](CONTAINER.md) for complete runtime and deployment options.
