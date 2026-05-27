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

This document covers the published OCI container images for the Digitraffic Road feeder, their environment-variable contract, authentication modes, and one-click Azure deployments. For the project overview see [README.md](README.md); for the CloudEvents contract see [EVENTS.md](EVENTS.md).

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://www.digitraffic.fi/en/road-traffic/>
- API / data documentation: <https://tie.digitraffic.fi/swagger/>

<!-- upstream-links:end -->

> [!CAUTION]
> **Creative Commons 4.0 BY attribution is required when you use this data.** Use this exact attribution text in downstream products and documentation: **"Licensed materials from the Finnish Transport Infrastructure Agency (Väylävirasto) and the Finnish Transport and Communications Agency (Traficom) Digitraffic service, www.digitraffic.fi"**

## Why this container

Digitraffic Road exposes Finland's national road traffic data through a live MQTT-over-WebSocket broker at `wss://tie.digitraffic.fi/mqtt` and reference-data REST endpoints at `https://tie.digitraffic.fi/api/`. The source is open, requires no API key, and covers traffic measurement stations, road weather stations, incident and road-work messages, weight restrictions, exempted transports, and road-maintenance tracking.

These images consume that upstream feed and re-emit it as CloudEvents on Kafka, MQTT 5.0, or AMQP 1.0 so downstream systems can subscribe on standard infrastructure instead of implementing their own long-lived Digitraffic client, startup reference-data fetch, payload normalization, and transport publishing.

## What ships in the box

This source ships three container images backed by the same upstream client and the same xRegistry contract:

| Image | Transport | Default behavior |
|---|---|---|
| `ghcr.io/clemensv/real-time-sources-digitraffic-road:latest` | Apache Kafka 2.x / Azure Event Hubs / Microsoft Fabric Event Streams | Three Kafka topics, JSON CloudEvents, reference data first, live telemetry thereafter |
| `ghcr.io/clemensv/real-time-sources-digitraffic-road-mqtt:latest` | MQTT 5.0 broker / Unified Namespace | UNS topic tree under `traffic/fi/fintraffic/digitraffic-road/...`; telemetry non-retained, reference data retained |
| `ghcr.io/clemensv/real-time-sources-digitraffic-road-amqp:latest` | AMQP 1.0 | Single AMQP address, binary or structured CloudEvents, SASL PLAIN or Microsoft Entra ID |

All three images emit the same ten event types documented in [EVENTS.md](EVENTS.md).

## Database schemas and handling

If you want to build a full data pipeline with all events ingested into a database, the integration with Microsoft Fabric Eventhouse and Azure Data Explorer is described in [DATABASE.md](../DATABASE.md). The KQL schema for this source lives in [`kql/digitraffic-road.kql`](kql/digitraffic-road.kql).

## Image contract

All three images share the same operational contract:

| Aspect | Value |
| --- | --- |
| Base images | Kafka image: `python:3.12-slim`; MQTT and AMQP images: `python:3.10-slim` |
| Default entry point | `python -m digitraffic_road feed`, `python -m digitraffic_road_mqtt feed`, `python -m digitraffic_road_amqp feed` |
| Default user | root |
| Exposed ports | none — the feeders are outbound publishers only |
| Health check | none defined; process liveness is the health signal |
| Signals | clean shutdown on `SIGTERM` |
| Persistent state | **none required** — this is a pure streaming bridge with startup reference-data fetch |
| Upstream connectivity | outbound WSS/HTTPS to `tie.digitraffic.fi:443` |
| Image tags | `:latest` plus immutable release / SHA tags published in GHCR |

## Installing the container images

Pull the container images from the GitHub Container Registry:

```bash
docker pull ghcr.io/clemensv/real-time-sources-digitraffic-road:latest
docker pull ghcr.io/clemensv/real-time-sources-digitraffic-road-mqtt:latest
docker pull ghcr.io/clemensv/real-time-sources-digitraffic-road-amqp:latest
```

## Using the Kafka image

The Kafka image connects to Digitraffic Road and writes JSON CloudEvents to Kafka topics for sensors, messages, and maintenance.

### With a Kafka broker

```bash
docker run --rm \
  -e KAFKA_BOOTSTRAP_SERVERS='broker:9092' \
  -e KAFKA_TOPIC_SENSORS='digitraffic-road-sensors' \
  -e KAFKA_TOPIC_MESSAGES='digitraffic-road-messages' \
  -e KAFKA_TOPIC_MAINTENANCE='digitraffic-road-maintenance' \
  -e KAFKA_ENABLE_TLS='false' \
  ghcr.io/clemensv/real-time-sources-digitraffic-road:latest
```

### With Azure Event Hubs or Fabric Event Streams

```bash
docker run --rm \
  -e CONNECTION_STRING='<connection-string>' \
  ghcr.io/clemensv/real-time-sources-digitraffic-road:latest
```

### Kafka topics and key model

| Kafka topic | Key | Event families |
|---|---|---|
| `digitraffic-road-sensors` | `{station_id}` | `TmsStation`, `WeatherStation` |
| `digitraffic-road-sensors` | `{station_id}/{sensor_id}` | `TmsSensorData`, `WeatherSensorData` |
| `digitraffic-road-messages` | `{situation_id}` | `TrafficAnnouncement`, `RoadWork`, `WeightRestriction`, `ExemptedTransport` |
| `digitraffic-road-maintenance` | `{task_id}` | `MaintenanceTaskType` |
| `digitraffic-road-maintenance` | `{domain}` | `MaintenanceTracking` |

## Using the MQTT image

The MQTT image republishes Digitraffic Road events into a Unified Namespace topic tree. Telemetry topics are published with `retain=false`; reference-data topics are published with `retain=true` so new subscribers can bootstrap immediately.

### Topic tree

| Topic | Notes |
|---|---|
| `traffic/fi/fintraffic/digitraffic-road/{station_id}/{sensor_id}/tms-sensor-data` | QoS 0, non-retained |
| `traffic/fi/fintraffic/digitraffic-road/{station_id}/{sensor_id}/weather-sensor-data` | QoS 0, non-retained |
| `traffic/fi/fintraffic/digitraffic-road/messages/{situation_id}/traffic-announcement` | QoS 1, non-retained |
| `traffic/fi/fintraffic/digitraffic-road/messages/{situation_id}/road-work` | QoS 1, non-retained |
| `traffic/fi/fintraffic/digitraffic-road/messages/{situation_id}/weight-restriction` | QoS 1, non-retained |
| `traffic/fi/fintraffic/digitraffic-road/messages/{situation_id}/exempted-transport` | QoS 1, non-retained |
| `traffic/fi/fintraffic/digitraffic-road/maintenance/{domain}/tracking` | QoS 0, non-retained |
| `traffic/fi/fintraffic/digitraffic-road/stations/{station_id}/tms-station` | QoS 1, retained |
| `traffic/fi/fintraffic/digitraffic-road/stations/{station_id}/weather-station` | QoS 1, retained |
| `traffic/fi/fintraffic/digitraffic-road/maintenance-tasks/{task_id}/task-type` | QoS 1, retained |

### With a generic MQTT broker (username/password)

```bash
docker run --rm \
  -e MQTT_BROKER_URL='mqtts://<broker-host>:8883' \
  -e MQTT_ENABLE_TLS=true \
  -e MQTT_AUTH_MODE=userpass \
  -e MQTT_USERNAME='<username>' \
  -e MQTT_PASSWORD='<password>' \
  ghcr.io/clemensv/real-time-sources-digitraffic-road-mqtt:latest
```

### With Azure Event Grid namespace MQTT broker (Microsoft Entra ID)

```bash
docker run --rm \
  -e MQTT_BROKER_URL='mqtts://<namespace>.<region>-1.ts.eventgrid.azure.net:8883' \
  -e MQTT_AUTH_MODE=entra \
  -e MQTT_ENTRA_CLIENT_ID='<managed-identity-client-id>' \
  ghcr.io/clemensv/real-time-sources-digitraffic-road-mqtt:latest
```

## Using the AMQP image

The AMQP image publishes CloudEvents over AMQP 1.0 to a single address, queue, or topic.

### Generic AMQP 1.0 broker (SASL PLAIN)

```bash
docker run --rm \
  -e AMQP_BROKER_URL='amqp://<user>:<password>@<broker-host>:5672/digitraffic-road' \
  ghcr.io/clemensv/real-time-sources-digitraffic-road-amqp:latest
```

### Azure Service Bus / Event Hubs with Microsoft Entra ID

```bash
docker run --rm \
  -e AMQP_HOST='<namespace>.servicebus.windows.net' \
  -e AMQP_PORT=5671 \
  -e AMQP_TLS=true \
  -e AMQP_ADDRESS='digitraffic-road' \
  -e AMQP_AUTH_MODE=entra \
  -e AMQP_ENTRA_AUDIENCE='https://servicebus.azure.net/.default' \
  -e AMQP_ENTRA_CLIENT_ID='<managed-identity-client-id>' \
  ghcr.io/clemensv/real-time-sources-digitraffic-road-amqp:latest
```

## Environment variables

### Common source selection

| Variable | Description |
|---|---|
| `DIGITRAFFIC_ROAD_SUBSCRIBE` | Comma-separated family selectors: `tms`, `weather`, `traffic-messages`, `maintenance`. Default: all families. Use this to reduce traffic volume or split families across deployments. |
| `DIGITRAFFIC_ROAD_STATION_FILTER` | Comma-separated station IDs to include for station-based sensor families. Default: all stations. Useful for regional or corridor-specific deployments. |

### Kafka image

| Variable | Description |
|---|---|
| `CONNECTION_STRING` | Azure Event Hubs / Fabric Event Stream style connection string. When present, it supplies broker and SASL details automatically. |
| `KAFKA_BOOTSTRAP_SERVERS` | Comma-separated Kafka `host:port` list when not using `CONNECTION_STRING`. |
| `KAFKA_TOPIC_SENSORS` | Target topic for station metadata and sensor telemetry. Default `digitraffic-road-sensors`. |
| `KAFKA_TOPIC_MESSAGES` | Target topic for traffic message families. Default `digitraffic-road-messages`. |
| `KAFKA_TOPIC_MAINTENANCE` | Target topic for maintenance tracking and maintenance task catalog. Default `digitraffic-road-maintenance`. |
| `SASL_USERNAME` / `SASL_PASSWORD` | SASL PLAIN credentials for Kafka brokers that require explicit username/password settings. |
| `KAFKA_ENABLE_TLS` | Enables TLS. Default `true`; set `false` only for local plaintext Kafka. |
| `DIGITRAFFIC_ROAD_FLUSH_INTERVAL` | Flush Kafka producer every N events. Default `1000`. Lower values reduce latency; higher values favor throughput. |

### MQTT image

| Variable | Description |
|---|---|
| `MQTT_BROKER_URL` | Target broker URL, for example `mqtts://broker:8883`. |
| `MQTT_ENABLE_TLS` | Enable TLS for broker connections. Default `true`. |
| `MQTT_AUTH_MODE` | `anonymous`, `userpass`, or `entra`. Default `anonymous`. |
| `MQTT_USERNAME` / `MQTT_PASSWORD` | Username/password credentials used when `MQTT_AUTH_MODE=userpass`. |
| `MQTT_ENTRA_CLIENT_ID` | Optional managed identity client id used when `MQTT_AUTH_MODE=entra`. |
| `MQTT_ENTRA_AUDIENCE` | JWT audience for Entra authentication. Default `https://eventgrid.azure.net/`. |
| `DIGITRAFFIC_ROAD_SUBSCRIBE` | Same source-family selection described above. |
| `DIGITRAFFIC_ROAD_STATION_FILTER` | Same station filter described above. |

### AMQP image

| Variable | Description |
|---|---|
| `AMQP_BROKER_URL` | Full AMQP broker URL, for example `amqp://user:pass@host:5672/digitraffic-road`. |
| `AMQP_HOST` / `AMQP_PORT` | Component-level alternative to `AMQP_BROKER_URL`. |
| `AMQP_ADDRESS` | Queue, topic, or node name. Default `digitraffic-road`. |
| `AMQP_USERNAME` / `AMQP_PASSWORD` | SASL PLAIN credentials for generic brokers when `AMQP_AUTH_MODE=password`. |
| `AMQP_AUTH_MODE` | `password` or `entra`. Default `password`. |
| `AMQP_TLS` | Enable TLS. Default `false`; automatically appropriate for secure Azure deployments when combined with port `5671` / Entra auth. |
| `AMQP_ENTRA_AUDIENCE` | Default `https://servicebus.azure.net/.default`. Use Event Hubs audience when targeting Event Hubs over AMQP. |
| `AMQP_ENTRA_CLIENT_ID` | Optional managed identity client id for Entra auth. |
| `DIGITRAFFIC_ROAD_SUBSCRIBE` | Same source-family selection described above. |
| `DIGITRAFFIC_ROAD_STATION_FILTER` | Same station filter described above. |

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

## Related

- [README.md](README.md) — project overview, audience, and operational summary.
- [EVENTS.md](EVENTS.md) — CloudEvents contract, schemas, routing, and payload details.
- [`xreg/digitraffic-road.xreg.json`](xreg/digitraffic-road.xreg.json) — the xRegistry manifest the generated producers derive from.
