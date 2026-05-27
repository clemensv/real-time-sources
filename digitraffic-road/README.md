<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/fi.png" alt="Finland" width="64" height="48"><br>
<sub><b>Finland</b></sub>
</td>
<td valign="middle">

# Digitraffic Road

<sub>TMS sensors, road weather, traffic messages · Kafka · MQTT · AMQP · <a href="https://www.digitraffic.fi/en/road-traffic/">upstream</a> · <a href="https://tie.digitraffic.fi/swagger/">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-5_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Finland — TMS sensors, road weather, traffic messages

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#digitraffic-road) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/digitraffic_road.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://www.digitraffic.fi/en/road-traffic/)

</td></tr></table>
<!-- source-hero:end -->

This feeder turns the Finnish national [Digitraffic Road](https://www.digitraffic.fi/en/road-traffic/) stream into real-time CloudEvents over Apache Kafka, MQTT 5.0 (Unified Namespace), or AMQP 1.0.

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://www.digitraffic.fi/en/road-traffic/>
- API / data documentation: <https://tie.digitraffic.fi/swagger/>

<!-- upstream-links:end -->

Companion docs:

- [CONTAINER.md](CONTAINER.md) — published container images, environment variables, and one-click Azure deployments.
- [EVENTS.md](EVENTS.md) — CloudEvents contract, schemas, and per-transport routing.

> [!CAUTION]
> **Creative Commons 4.0 BY attribution is required when you use this data.** Use this exact attribution text in downstream products and documentation: **"Licensed materials from the Finnish Transport Infrastructure Agency (Väylävirasto) and the Finnish Transport and Communications Agency (Traficom) Digitraffic service, www.digitraffic.fi"**

## Why this bridge

Digitraffic Road exposes Finland's national road traffic network as a live MQTT-over-WebSocket feed at `wss://tie.digitraffic.fi/mqtt` plus reference-data REST endpoints under `https://tie.digitraffic.fi/api/`. The source covers automatic traffic measurement stations, road weather stations, traffic announcements, road works, weight restrictions, exempted transports, and maintenance vehicle tracking.

This bridge turns that upstream stream into a production-friendly event source so consumers can subscribe on their messaging fabric of choice instead of writing and operating their own long-lived MQTT client, REST bootstrap, gzip/base64 decoding, CloudEvents wrapping, and transport-specific publishing.

Typical consumers include:

- **Traffic operations centers** — live road-network monitoring, congestion dashboards, and hazard response.
- **Winter maintenance and contractor analytics** — route, task, and vehicle tracking for maintenance fleets.
- **Logistics and fleet planning** — weather, flow, and incident awareness for routing decisions.
- **Microsoft Fabric / Eventhouse / ADX pipelines** — queryable real-time telemetry and reference data.
- **Research and public-interest applications** — reproducible ingest of Finnish road traffic data.

## Overview

**Digitraffic Road** is a streaming bridge: it keeps an open connection to `tie.digitraffic.fi` for telemetry and fetches reference catalogs from the REST API at startup. The source ships in three transport variants:

| Variant | Container image | Transport | Default delivery shape |
|---|---|---|---|
| **Kafka** | `ghcr.io/clemensv/real-time-sources-digitraffic-road:latest` | Apache Kafka 2.x compatible (including Azure Event Hubs and Microsoft Fabric Event Streams) | Three Kafka topics, JSON CloudEvents, keys aligned to source identity (`{station_id}`, `{station_id}/{sensor_id}`, `{situation_id}`, `{domain}`, `{task_id}`) |
| **MQTT** | `ghcr.io/clemensv/real-time-sources-digitraffic-road-mqtt:latest` | MQTT 5.0 broker / Unified Namespace | Topic tree under `traffic/fi/fintraffic/digitraffic-road/...`, telemetry non-retained, reference data retained |
| **AMQP** | `ghcr.io/clemensv/real-time-sources-digitraffic-road-amqp:latest` | AMQP 1.0 (RabbitMQ AMQP 1.0 plugin, ActiveMQ Artemis, Qpid Dispatch, Azure Service Bus, Azure Event Hubs) | Single AMQP node, binary or structured CloudEvents, SASL PLAIN or Microsoft Entra ID |

All three variants share:

- The same upstream Digitraffic Road data source.
- The same xRegistry contract in `xreg/digitraffic-road.xreg.json`.
- The same ten event types: three reference-data types and seven live telemetry types.

## Key features

- **No API key required** — the upstream Digitraffic Road road-traffic feed is open.
- **Streaming telemetry + reference bootstrap** — station catalogs and maintenance task types are emitted first, then live telemetry flows continuously.
- **Ten event types** spanning stations, sensors, traffic messages, and maintenance tracking.
- **Three transport targets** with the same source semantics: Kafka, MQTT/UNS, and AMQP 1.0.
- **Selective subscriptions** via `DIGITRAFFIC_ROAD_SUBSCRIBE` (`tms`, `weather`, `traffic-messages`, `maintenance`).
- **Station filtering** for sensor families via `DIGITRAFFIC_ROAD_STATION_FILTER`.
- **Azure-ready packaging** with published images and ARM templates for Event Hubs, Event Grid MQTT, and Service Bus.

## Repository layout

```text
digitraffic-road/
  xreg/digitraffic-road.xreg.json   # shared xRegistry contract
  digitraffic_road/                 # Kafka feeder application
  digitraffic_road_mqtt/            # MQTT/UNS feeder application
  digitraffic_road_amqp/            # AMQP 1.0 feeder application
  digitraffic_road_producer/        # xRegistry-generated Kafka producer
  digitraffic_road_mqtt_producer/   # xRegistry-generated MQTT producer
  digitraffic_road_amqp_producer/   # xRegistry-generated AMQP producer
  Dockerfile                        # Kafka image
  Dockerfile.mqtt                   # MQTT image
  Dockerfile.amqp                   # AMQP image
  kql/digitraffic-road.kql          # Eventhouse / KQL schema
  tests/                            # unit + integration tests
```

## Prerequisites

- Docker 20.10+ (or another OCI-compatible runtime).
- Outbound HTTPS / WSS access to `tie.digitraffic.fi` on port 443.
- Network access to your target Kafka broker, MQTT broker, or AMQP 1.0 broker.

This is a pure streaming feeder. It does **not** require a persistent state file or mounted host volume.

## Quick start with Docker

### Kafka

```bash
docker run --rm \
  -e CONNECTION_STRING="<event-hubs-or-fabric-connection-string>" \
  ghcr.io/clemensv/real-time-sources-digitraffic-road:latest
```

You can also target a plain Kafka broker with explicit bootstrap servers and topics:

```bash
docker run --rm \
  -e KAFKA_BOOTSTRAP_SERVERS="broker:9092" \
  -e KAFKA_TOPIC_SENSORS="digitraffic-road-sensors" \
  -e KAFKA_TOPIC_MESSAGES="digitraffic-road-messages" \
  -e KAFKA_TOPIC_MAINTENANCE="digitraffic-road-maintenance" \
  -e KAFKA_ENABLE_TLS=false \
  ghcr.io/clemensv/real-time-sources-digitraffic-road:latest
```

### MQTT (Unified Namespace)

```bash
docker run --rm \
  -e MQTT_BROKER_URL="mqtts://<broker-host>:8883" \
  -e MQTT_AUTH_MODE=userpass \
  -e MQTT_USERNAME="<username>" \
  -e MQTT_PASSWORD="<password>" \
  ghcr.io/clemensv/real-time-sources-digitraffic-road-mqtt:latest
```

Topics published include:

```text
traffic/fi/fintraffic/digitraffic-road/{station_id}/{sensor_id}/tms-sensor-data
traffic/fi/fintraffic/digitraffic-road/{station_id}/{sensor_id}/weather-sensor-data
traffic/fi/fintraffic/digitraffic-road/messages/{situation_id}/traffic-announcement
traffic/fi/fintraffic/digitraffic-road/messages/{situation_id}/road-work
traffic/fi/fintraffic/digitraffic-road/messages/{situation_id}/weight-restriction
traffic/fi/fintraffic/digitraffic-road/messages/{situation_id}/exempted-transport
traffic/fi/fintraffic/digitraffic-road/maintenance/{domain}/tracking
traffic/fi/fintraffic/digitraffic-road/stations/{station_id}/tms-station
traffic/fi/fintraffic/digitraffic-road/stations/{station_id}/weather-station
traffic/fi/fintraffic/digitraffic-road/maintenance-tasks/{task_id}/task-type
```

### AMQP 1.0

```bash
docker run --rm \
  -e AMQP_BROKER_URL='amqp://<user>:<password>@<broker-host>:5672/digitraffic-road' \
  ghcr.io/clemensv/real-time-sources-digitraffic-road-amqp:latest
```

For Azure Service Bus with Microsoft Entra ID:

```bash
docker run --rm \
  -e AMQP_HOST='<namespace>.servicebus.windows.net' \
  -e AMQP_PORT=5671 \
  -e AMQP_TLS=true \
  -e AMQP_ADDRESS='digitraffic-road' \
  -e AMQP_AUTH_MODE=entra \
  -e AMQP_ENTRA_CLIENT_ID='<managed-identity-client-id>' \
  ghcr.io/clemensv/real-time-sources-digitraffic-road-amqp:latest
```

## Configuration reference

The full environment-variable matrix for Kafka, MQTT, and AMQP images lives in [CONTAINER.md](CONTAINER.md). Runtime entry points are:

- `python -m digitraffic_road feed`
- `python -m digitraffic_road_mqtt feed`
- `python -m digitraffic_road_amqp feed`

## Event families

### Reference data (emitted at startup)

| Event type | Description |
|---|---|
| `fi.digitraffic.road.stations.TmsStation` | Automatic traffic measurement station metadata |
| `fi.digitraffic.road.stations.WeatherStation` | Road weather station metadata |
| `fi.digitraffic.road.maintenance.tasks.MaintenanceTaskType` | Maintenance task-type catalog |

### Telemetry (streamed continuously)

| Event type | Description |
|---|---|
| `fi.digitraffic.road.sensors.TmsSensorData` | TMS sensor measurements such as vehicle count, speed, and occupancy |
| `fi.digitraffic.road.sensors.WeatherSensorData` | Weather measurements such as temperature, wind, and humidity |
| `fi.digitraffic.road.messages.TrafficAnnouncement` | Traffic incidents and hazard announcements |
| `fi.digitraffic.road.messages.RoadWork` | Planned or active road works |
| `fi.digitraffic.road.messages.WeightRestriction` | Weight restrictions on roads or bridges |
| `fi.digitraffic.road.messages.ExemptedTransport` | Oversize / heavy transport notices |
| `fi.digitraffic.road.maintenance.MaintenanceTracking` | Maintenance vehicle position and active task tracking |

## Deploying into Azure Container Instances

Five one-click deployment templates are available:

### Kafka — bring your own Event Hub / Kafka

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdigitraffic-road%2Fazure-template.json)

### Kafka — provision a new Event Hub

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdigitraffic-road%2Fazure-template-with-eventhub.json)

### MQTT — bring your own broker

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdigitraffic-road%2Fazure-template-mqtt.json)

### MQTT — provision an Event Grid namespace

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdigitraffic-road%2Fazure-template-with-eventgrid-mqtt.json)

### AMQP — provision a new Azure Service Bus namespace

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdigitraffic-road%2Fazure-template-with-servicebus.json)

## Next steps

- Review [EVENTS.md](EVENTS.md) before writing consumers.
- Use [CONTAINER.md](CONTAINER.md) for the full container and environment-variable contract.
- Consult the upstream Digitraffic Road documentation at <https://www.digitraffic.fi/en/road-traffic/>.
