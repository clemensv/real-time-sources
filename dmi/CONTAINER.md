# DMI Observation Triad → Apache Kafka & MQTT/UNS

This source ships two container images backed by the same upstream poller
and xRegistry contract:

| Image | Transport | Default behavior |
|---|---|---|
| `ghcr.io/clemensv/real-time-sources-dmi-kafka` | Apache Kafka 2.x (Azure Event Hubs, Fabric Event Streams, Confluent Cloud, plain Kafka) | Single topic `dmi`, JSON CloudEvents (binary mode); subscribers route by `ce_type` |
| `ghcr.io/clemensv/real-time-sources-dmi-mqtt` | MQTT 5.0 broker (Mosquitto, EMQX, HiveMQ, Azure Event Grid MQTT, Microsoft Fabric MQTT) | Unified-Namespace topic tree under `weather/dk/dmi/…` and `ocean/dk/dmi/…`, retained QoS 1, CloudEvent attributes as MQTT 5 user properties |

Both images consume the [DMI Open Data REST API](https://opendatadocs.dmi.govcloud.dk/)
operated by the Danish Meteorological Institute and emit the
**observation triad**: `metObs` (land weather), `oceanObs` (sea-state and
tidewater), and `lightningData` (per-strike events, Kafka only).

The on-the-wire schemas live in [EVENTS.md](EVENTS.md). The container images
work with any Apache Kafka–compatible service that supports TLS with
SASL/PLAIN, and with any MQTT 5.0 broker.

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a
database, the integration with Fabric Eventhouse and Azure Data Explorer is
described in [DATABASE.md](../DATABASE.md). The DMI-specific KQL schema is
in [kql/dmi.kql](kql/dmi.kql).

## Installing the Container Images

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-dmi-kafka:latest
$ docker pull ghcr.io/clemensv/real-time-sources-dmi-mqtt:latest
```

## Using the Kafka image

The Kafka image (`…-dmi-kafka`) reads from the three DMI APIs and writes
JSON CloudEvents (binary mode) to a **single** Kafka topic. Subscribers
route by the CloudEvent `type` attribute.

### With a Kafka Broker

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='dmi' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    -e DMI_METOBS_API_KEY='<key>' \
    -e DMI_OCEANOBS_API_KEY='<key>' \
    -e DMI_LIGHTNING_API_KEY='<key>' \
    ghcr.io/clemensv/real-time-sources-dmi-kafka:latest
```

### With Azure Event Hubs or Fabric Event Streams

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    -e DMI_METOBS_API_KEY='<key>' \
    -e DMI_OCEANOBS_API_KEY='<key>' \
    -e DMI_LIGHTNING_API_KEY='<key>' \
    ghcr.io/clemensv/real-time-sources-dmi-kafka:latest
```

## Using the MQTT image

The MQTT image (`…-dmi-mqtt`) publishes MQTT 5.0 binary-mode CloudEvents
into a Unified-Namespace topic tree at QoS 1 with `retain=true` on each
leaf. **Lightning is excluded** — per-strike events have no LKV fit.

Topics (retained):

```
weather/dk/dmi/met-obs/{station_id}/info
weather/dk/dmi/met-obs/{station_id}/{parameter_id}
ocean/dk/dmi/ocean-obs/{station_id}/info
ocean/dk/dmi/ocean-obs/{station_id}/{parameter_id}
ocean/dk/dmi/tidewater/{station_id}/info
ocean/dk/dmi/tidewater/{station_id}/prediction
```

### With a generic MQTT 5 broker (username/password)

```shell
$ docker run --rm \
    -e MQTT_BROKER_URL='mqtts://broker.example.com:8883' \
    -e MQTT_USERNAME='<username>' \
    -e MQTT_PASSWORD='<password>' \
    -e DMI_METOBS_API_KEY='<key>' \
    -e DMI_OCEANOBS_API_KEY='<key>' \
    ghcr.io/clemensv/real-time-sources-dmi-mqtt:latest
```

### With Azure Event Grid namespace MQTT broker (Microsoft Entra JWT)

When the host has a managed identity that holds the
**EventGrid TopicSpaces Publisher** role on the target topic space, the
feeder uses MQTT v5 enhanced authentication (`OAUTH2-JWT`) with a token
issued for audience `https://eventgrid.azure.net/`.

```shell
$ docker run --rm \
    -e MQTT_BROKER_URL='mqtts://<ns>.<region>-1.ts.eventgrid.azure.net:8883' \
    -e MQTT_AUTH_MODE=entra \
    -e MQTT_ENTRA_CLIENT_ID='<user-assigned-managed-identity-client-id>' \
    -e MQTT_CLIENT_ID='<unique-client-id>' \
    -e DMI_METOBS_API_KEY='<key>' \
    -e DMI_OCEANOBS_API_KEY='<key>' \
    ghcr.io/clemensv/real-time-sources-dmi-mqtt:latest
```

## Environment Variables

### Common (both images)

| Variable | Description |
|---|---|
| `DMI_API_KEY` | Fallback DMI Gravitee key used for any API without a dedicated key. |
| `DMI_METOBS_API_KEY` | Per-API key for the MetObs API. |
| `DMI_OCEANOBS_API_KEY` | Per-API key for the OceanObs API. |
| `DMI_LIGHTNING_API_KEY` | Per-API key for the Lightning API (Kafka image only). |
| `DMI_OBSERVATION_PERIOD` | DMI period filter (default `latest-hour`). |
| `DMI_REFERENCE_REFRESH_HOURS` | Hours between re-emit of reference data (default `6`). |
| `POLLING_INTERVAL` | Seconds between polling cycles (default `300`). |
| `STATE_FILE` | Path to the dedupe state file. |
| `ONCE_MODE` | `true` runs a single polling cycle and exits. |

### Kafka image

| Variable | Description |
|---|---|
| `CONNECTION_STRING` | Azure Event Hubs / Fabric Event Stream connection string. Supersedes `KAFKA_*` and `SASL_*`. |
| `KAFKA_BOOTSTRAP_SERVERS` | Comma-separated `host:port` list of TLS-enabled Kafka brokers. |
| `KAFKA_TOPIC` | Target Kafka topic (default `dmi`). |
| `SASL_USERNAME` / `SASL_PASSWORD` | SASL PLAIN credentials. |
| `KAFKA_ENABLE_TLS` | `false` disables TLS (default `true`). |

### MQTT image

| Variable | Description |
|---|---|
| `MQTT_BROKER_URL` | Broker URL, e.g. `mqtt://host:1883` or `mqtts://host:8883`. |
| `MQTT_HOST` / `MQTT_PORT` / `MQTT_TLS` | Component-level alternative to `MQTT_BROKER_URL`. |
| `MQTT_USERNAME` / `MQTT_PASSWORD` | Optional credentials when `MQTT_AUTH_MODE=password`. |
| `MQTT_AUTH_MODE` | `password` (default), `anonymous`, `tls-cert`, or `entra`. |
| `MQTT_ENTRA_AUDIENCE` | JWT audience (default `https://eventgrid.azure.net/`). |
| `MQTT_ENTRA_CLIENT_ID` | Optional user-assigned managed-identity client id. |
| `MQTT_CLIENT_ID` | MQTT client identifier. |
| `MQTT_CONTENT_MODE` | `binary` (default) or `structured` CloudEvents content mode. |
| `MQTT_CA_FILE` | Path to broker CA chain. |
| `MQTT_CLIENT_CERT` / `MQTT_CLIENT_KEY` | PEM paths for `tls-cert` auth. |

## Deploying into Azure Container Instances

### Kafka — bring your own Event Hub / Kafka

Deploy the Kafka container with your own Azure Event Hubs or Fabric Event
Stream connection string. The template creates a storage account and file
share for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdmi%2Fazure-template.json)

### Kafka — provision a new Event Hub

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdmi%2Fazure-template-with-eventhub.json)

### MQTT — bring your own broker

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdmi%2Fazure-template-mqtt.json)

### MQTT — provision a new Event Grid namespace MQTT broker

Deploys the MQTT container together with an Azure Event Grid namespace,
topic space rooted at `weather/#` and `ocean/#`, a user-assigned managed
identity, and an `EventGrid TopicSpaces Publisher` role assignment scoped
to the topic space.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdmi%2Fazure-template-with-eventgrid-mqtt.json)
