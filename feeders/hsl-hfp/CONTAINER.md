<!-- source-hero:begin -->

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://www.hsl.fi/en/hsl/open-data>
- API / data documentation: <https://digitransit.fi/en/developers/apis/4-realtime-api/vehicle-positions/>

<!-- upstream-links:end -->

<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/fi.png" alt="Finland / Helsinki" width="64" height="48"><br>
<sub><b>Finland / Helsinki</b></sub>
</td>
<td valign="middle">

# HSL HFP

<sub>transit vehicle positions via MQTT, ~1,700 vehicles @ 1 Hz · Kafka · MQTT · AMQP · <a href="https://www.hsl.fi/en/hsl/open-data">upstream</a> · <a href="https://digitransit.fi/en/developers/apis/4-realtime-api/vehicle-positions/">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-5_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Finland / Helsinki — transit vehicle positions via MQTT, ~1,700 vehicles @ 1 Hz

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#hsl-hfp) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/hsl-hfp.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://www.hsl.fi/en/hsl/open-data)

</td></tr></table>
<!-- source-hero:end -->

This document covers the published OCI container images for the HSL HFP feeder, their environment-variable contract, authentication modes, and per-transport `docker run` shapes. For the project overview see [README.md](README.md); for the CloudEvents contract see [EVENTS.md](EVENTS.md).

## Image contract

All three images share one acquisition core and one xRegistry contract, but each process publishes to exactly one downstream transport:

| Image | Tags | Base | Entrypoint | Default behavior |
|---|---|---|---|---|
| `ghcr.io/clemensv/real-time-sources-hsl-hfp-kafka` | `:latest`, `:sha-<git-sha>`, release tags | `python:3.10-slim` | `python -m hsl_hfp feed` | Subscribes to HSL HFP MQTT and publishes structured CloudEvents to Kafka topic `hsl-hfp`; telemetry key = `{operator_id}/{vehicle_number}`. |
| `ghcr.io/clemensv/real-time-sources-hsl-hfp-mqtt` | `:latest`, `:sha-<git-sha>`, release tags | `python:3.10-slim` | `python -m hsl_hfp_mqtt feed` | Subscribes to HSL HFP MQTT and republishes binary-mode MQTT 5 CloudEvents while mirroring the HFP topic tree; reference data is published under `hfp/v2/reference/...`. |
| `ghcr.io/clemensv/real-time-sources-hsl-hfp-amqp` | `:latest`, `:sha-<git-sha>`, release tags | `python:3.10-slim` | `python -m hsl_hfp_amqp feed` | Subscribes to HSL HFP MQTT and publishes binary-mode AMQP 1.0 CloudEvents to one queue, topic, event hub, or AMQP address. |

Operational contract:

| Aspect | Value |
|---|---|
| Upstream | Anonymous TLS MQTT at `mqtt.hsl.fi:8883`, default subscription `/hfp/v2/journey/#`. |
| Exposed ports | none — the feeder is an outbound subscriber/publisher only. |
| Signals | process liveness is health; stop the container to disconnect from upstream and flush the downstream producer. |
| Persistent state | none required for telemetry. GTFS reference data is re-emitted at startup and on the refresh timer. |
| License | Container metadata declares `MIT`; upstream data is CC BY 4.0 from Digitransit / HSL open data. |

Pull the images from the GitHub Container Registry:

```bash
docker pull ghcr.io/clemensv/real-time-sources-hsl-hfp-kafka:latest
docker pull ghcr.io/clemensv/real-time-sources-hsl-hfp-mqtt:latest
docker pull ghcr.io/clemensv/real-time-sources-hsl-hfp-amqp:latest
```

## Quick start

### Kafka

```bash
docker run --rm \
  -e CONNECTION_STRING='<event-hubs-or-fabric-connection-string-with-EntityPath=hsl-hfp>' \
  ghcr.io/clemensv/real-time-sources-hsl-hfp-kafka:latest
```

### MQTT

```bash
docker run --rm \
  -e MQTT_BROKER_URL='mqtts://<broker-host>:8883' \
  -e MQTT_USERNAME='<username>' \
  -e MQTT_PASSWORD='<password>' \
  ghcr.io/clemensv/real-time-sources-hsl-hfp-mqtt:latest
```

### AMQP

```bash
docker run --rm \
  -e AMQP_BROKER_URL='amqps://<broker-host>:5671/hsl-hfp' \
  -e AMQP_USERNAME='<username>' \
  -e AMQP_PASSWORD='<password>' \
  ghcr.io/clemensv/real-time-sources-hsl-hfp-amqp:latest
```

## Environment variables

### Upstream HFP MQTT subscription (all images)

| Variable | Default | Required? | Description |
|---|---:|---|---|
| `HFP_MQTT_HOST` | `mqtt.hsl.fi` | No | Upstream HSL HFP broker host. |
| `HFP_MQTT_PORT` | `8883` | No | Upstream HSL HFP broker port. |
| `HFP_MQTT_TLS` | `true` | No | Use TLS for the upstream connection. Values `false`, `0`, or `no` disable TLS. |
| `HFP_TOPIC_FILTERS` | `/hfp/v2/journey/#` | No | Comma-separated upstream topic filters. Narrow this to reduce firehose volume. |

### GTFS reference data (all images)

| Variable | Default | Required? | Description |
|---|---:|---|---|
| `REFERENCE_REFRESH_INTERVAL` | `43200` | No | Seconds between GTFS operator/route/stop refreshes. `0` means startup emission only. |
| `SKIP_REFERENCE` | `false` | No | Set `true`, `1`, or `yes` to skip GTFS reference emission entirely. |
| `HSL_GTFS_URL` | `https://infopalvelut.storage.hsldev.com/gtfs/hsl.zip` | No | HSL GTFS static ZIP used for `Operator`, `Route`, and `Stop` events. |

### Run mode (all images)

| Variable | Default | Required? | Description |
|---|---:|---|---|
| `ONCE_MODE` | `false` | No | Emit reference data and a bounded telemetry sample, then exit. |
| `ONCE_MAX_EVENTS` | `50` | No | Maximum telemetry events to forward in once mode. |
| `ONCE_MAX_SECONDS` | `60` | No | Maximum seconds to wait for telemetry in once mode. |
| `LOG_LEVEL` | `INFO` | No | Python logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`). |

### Kafka image

| Variable | Default | Required? | Description |
|---|---:|---|---|
| `CONNECTION_STRING` | unset | Yes, unless using direct broker settings | Event Hubs / Fabric Event Stream connection string, or test-harness form `BootstrapServer=host:port;EntityPath=hsl-hfp`. |
| `KAFKA_BOOTSTRAP_SERVERS` | unset | Yes, unless `CONNECTION_STRING` is set | Comma-separated Kafka bootstrap list. |
| `KAFKA_TOPIC` | unset | Yes, unless `EntityPath` is in `CONNECTION_STRING` | Target topic. Use `hsl-hfp` to match the contract. |
| `SASL_USERNAME` | unset | No | SASL PLAIN username for direct broker mode. |
| `SASL_PASSWORD` | unset | No | SASL PLAIN password for direct broker mode. |
| `KAFKA_ENABLE_TLS` | `true` | No | `false` uses plaintext / SASL_PLAINTEXT in direct broker mode. |
| `CONTENT_MODE` | `structured` | No | Kafka CloudEvents content mode: `structured` or `binary`. |

### MQTT image

| Variable | Default | Required? | Description |
|---|---:|---|---|
| `MQTT_BROKER_URL` | `mqtt://localhost:1883` | Yes for real deployments | Downstream broker URL, e.g. `mqtt://host:1883` or `mqtts://host:8883`. |
| `MQTT_USERNAME` | unset | No | Username for generic MQTT brokers when `MQTT_AUTH_MODE=password`. |
| `MQTT_PASSWORD` | unset | No | Password for generic MQTT brokers when `MQTT_AUTH_MODE=password`. |
| `MQTT_CLIENT_ID` | unset | Required for `MQTT_AUTH_MODE=entra` | MQTT client identifier. Must be unique per broker session. |
| `MQTT_CONTENT_MODE` | `binary` | No | MQTT CloudEvents content mode: `binary` or `structured`. |
| `MQTT_AUTH_MODE` | `password` | No | `password` for anonymous/username-password brokers, or `entra` for Azure Event Grid namespace MQTT. |
| `MQTT_ENTRA_AUDIENCE` | `https://eventgrid.azure.net/` | No | Entra token audience for `MQTT_AUTH_MODE=entra`. |
| `MQTT_ENTRA_CLIENT_ID` | unset | No | Optional user-assigned managed-identity client id. |
| `MQTT_CA_FILE` | unset | No | Optional CA bundle for downstream broker TLS validation. |

### AMQP image

| Variable | Default | Required? | Description |
|---|---:|---|---|
| `AMQP_BROKER_URL` | unset | Yes, unless using component settings | Full broker URL, e.g. `amqp://user:pw@host:5672/hsl-hfp` or `amqps://host:5671/hsl-hfp`. |
| `AMQP_HOST` | unset | Yes, unless `AMQP_BROKER_URL` is set | Broker host for component-level connection settings. |
| `AMQP_PORT` | transport default | No | Broker port. Use `5671` with `AMQP_TLS=true` for live Azure namespaces. |
| `AMQP_ADDRESS` | `hsl-hfp` | No | Queue, topic, event hub, or AMQP node address. |
| `AMQP_USERNAME` | unset | No | SASL PLAIN username for `AMQP_AUTH_MODE=password`. |
| `AMQP_PASSWORD` | unset | No | SASL PLAIN password for `AMQP_AUTH_MODE=password`. |
| `AMQP_TLS` | `false` | No | Use TLS for component-level settings. |
| `AMQP_CONTENT_MODE` | `binary` | No | AMQP CloudEvents content mode: `binary` or `structured`. |
| `AMQP_AUTH_MODE` | `password` | No | `password`, `entra`, or `sas`. |
| `AMQP_ENTRA_AUDIENCE` | `https://servicebus.azure.net/.default` | No | Entra token audience. Use `https://eventhubs.azure.net/.default` for Event Hubs. |
| `AMQP_ENTRA_CLIENT_ID` | unset | No | Optional user-assigned managed-identity client id. |
| `AMQP_SAS_KEY_NAME` | unset | Required for `AMQP_AUTH_MODE=sas` | SAS policy/key name for CBS SAS-token auth. |
| `AMQP_SAS_KEY` | unset | Required for `AMQP_AUTH_MODE=sas` | SAS key value for CBS SAS-token auth. |

## docker run

### Kafka — bring your own Event Hubs / Fabric Event Stream

```bash
docker run --rm \
  -e CONNECTION_STRING='Endpoint=sb://<ns>.servicebus.windows.net/;SharedAccessKeyName=<key-name>;SharedAccessKey=<key>;EntityPath=hsl-hfp' \
  ghcr.io/clemensv/real-time-sources-hsl-hfp-kafka:latest
```

### Kafka — self-hosted broker

```bash
docker run --rm \
  -e KAFKA_BOOTSTRAP_SERVERS='<broker-1>:9092,<broker-2>:9092' \
  -e KAFKA_TOPIC='hsl-hfp' \
  -e KAFKA_ENABLE_TLS=false \
  ghcr.io/clemensv/real-time-sources-hsl-hfp-kafka:latest
```

For SASL/PLAIN brokers, add `SASL_USERNAME`, `SASL_PASSWORD`, and leave `KAFKA_ENABLE_TLS=true` unless your broker explicitly uses plaintext SASL.

### MQTT — bring your own broker

```bash
docker run --rm \
  -e MQTT_BROKER_URL='mqtts://<broker-host>:8883' \
  -e MQTT_USERNAME='<username>' \
  -e MQTT_PASSWORD='<password>' \
  -e MQTT_CLIENT_ID='hsl-hfp-prod-01' \
  ghcr.io/clemensv/real-time-sources-hsl-hfp-mqtt:latest
```

### MQTT — Azure Event Grid namespace (Microsoft Entra JWT)

When the container host has a managed identity with **EventGrid TopicSpaces Publisher** on the target topic space, use MQTT v5 enhanced authentication (`OAUTH2-JWT`).

> [!IMPORTANT]
> `MQTT_CLIENT_ID` must be unique across clients connected to the same Event Grid namespace MQTT broker. A duplicate client id causes session takeover.

```bash
docker run --rm \
  -e MQTT_BROKER_URL='mqtts://<namespace>.<region>-1.ts.eventgrid.azure.net:8883' \
  -e MQTT_AUTH_MODE=entra \
  -e MQTT_ENTRA_CLIENT_ID='<user-assigned-managed-identity-client-id>' \
  -e MQTT_CLIENT_ID='hsl-hfp-prod-01' \
  ghcr.io/clemensv/real-time-sources-hsl-hfp-mqtt:latest
```

### AMQP — Azure Service Bus / Event Hubs (Microsoft Entra CBS)

For Azure Service Bus, grant the container identity **Azure Service Bus Data Sender** on the queue or topic. For Event Hubs, use **Azure Event Hubs Data Sender** and set the Event Hubs audience.

> [!IMPORTANT]
> For live Azure namespaces, set `AMQP_TLS=true` and `AMQP_PORT=5671`. Port `5672` is only valid for local or explicitly plaintext brokers.

```bash
docker run --rm \
  -e AMQP_HOST='<namespace>.servicebus.windows.net' \
  -e AMQP_PORT=5671 \
  -e AMQP_TLS=true \
  -e AMQP_ADDRESS='hsl-hfp' \
  -e AMQP_AUTH_MODE=entra \
  -e AMQP_ENTRA_AUDIENCE='https://servicebus.azure.net/.default' \
  -e AMQP_ENTRA_CLIENT_ID='<user-assigned-managed-identity-client-id>' \
  ghcr.io/clemensv/real-time-sources-hsl-hfp-amqp:latest
```

For Event Hubs over AMQP, use `AMQP_HOST='<namespace>.servicebus.windows.net'` or the Event Hubs AMQP host your deployment exposes, `AMQP_ADDRESS='<event-hub-name>'`, and `AMQP_ENTRA_AUDIENCE='https://eventhubs.azure.net/.default'`.

## Kafka / Event Hubs usage

The Kafka image accepts either a Microsoft-style connection string (`Endpoint=...;SharedAccessKeyName=...;SharedAccessKey=...;EntityPath=hsl-hfp`) or direct Kafka settings. In connection-string mode, the bridge derives bootstrap servers, SASL credentials, and topic from the string. In direct mode, provide `KAFKA_BOOTSTRAP_SERVERS` and `KAFKA_TOPIC` explicitly.

Kafka keys and CloudEvent subjects are contract-aligned: HFP telemetry uses `{operator_id}/{vehicle_number}`, while GTFS reference events use `operator/{operator_id}`, `route/{route_id}`, and `stop/{stop_id}`. This keeps all records for one vehicle ordered on the same partition and avoids route/trip keys that disappear on driver/block events.

## Faithfulness / payload contract

The feeder is a transport bridge, not a transformer. It keeps the upstream HFP topic structure and JSON payload values verbatim while adding a CloudEvents envelope and a stable typed schema.

> [!IMPORTANT]
> There are exactly three controlled deviations from a byte-verbatim echo: (1) the HFP wrapper `{"VP": {...}}` / `{"TLR": {...}}` becomes the CloudEvent `type` (`fi.hsl.hfp.vp`, `fi.hsl.hfp.tlr`, …) and the inner object becomes `data`; (2) topic-path identity levels (`operator_id`, `vehicle_number`, `temporal_type`, `transport_mode`, `route_id`, `direction_id`, `headsign`, `start_time`, `next_stop`, `geohash_level`, `geohash`) are injected into `data` so each event is self-contained; (3) absent optional HFP fields serialize as explicit JSON `null` so consumers see a stable typed schema. Present fields round-trip with their HFP wire names, including hyphenated keys such as `dr-type`, `tlp-requestid`, and `signal-groupid`.

No persistent dedupe cursor is used or needed: telemetry is streamed and fanned out as it arrives, and reference data is intentionally re-emitted at startup and on the refresh timer.

---

<sub>
📚 <a href="../README.md">← Back to catalog</a> &nbsp;·&nbsp;
🌐 <a href="https://clemensv.github.io/real-time-sources/#hsl-hfp">Portal entry</a> &nbsp;·&nbsp;
📑 <a href="EVENTS.md">EVENTS.md</a> &nbsp;·&nbsp;
📘 <a href="README.md">README.md</a> &nbsp;·&nbsp;
🗄️ <a href="kql/hsl-hfp.kql">KQL schema</a> &nbsp;·&nbsp;
↗ <a href="https://www.hsl.fi/en/hsl/open-data">HSL open data</a> &nbsp;·&nbsp;
📖 <a href="https://digitransit.fi/en/developers/apis/5-realtime-api/vehicle-positions/high-frequency-positioning/">HFP docs</a>
</sub>
