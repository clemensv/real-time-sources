<!-- source-hero:begin -->

<table width="100%"><tr>
<td width="80" valign="middle" align="center">

<img src="https://flagcdn.com/64x48/gb.png" alt="United Kingdom" width="64" height="48"><br>

<sub><b>United Kingdom</b></sub>

</td>

<td valign="middle">

# UK BODS SIRI container images

<sub>configuration-only wrapper over <code>siri</code> · Kafka · MQTT · AMQP · <a href="https://www.bus-data.dft.gov.uk/">upstream</a></sub>

[📘 **Overview**](README.md) &nbsp;·&nbsp;

[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;

[🗄️ **KQL schema**](kql/uk-bods-siri.kql) &nbsp;·&nbsp;

[↗ **Upstream**](https://www.bus-data.dft.gov.uk/)

</td></tr></table>

<!-- source-hero:end -->

This document covers the published OCI container images for the UK BODS SIRI thin wrapper, their environment-variable contract, authentication modes, and one-click Azure deployments. For the project overview see [README.md](README.md); for the CloudEvents contract see [EVENTS.md](EVENTS.md).

## Upstream

- Home page: <https://www.bus-data.dft.gov.uk/>

- Default SIRI-VM bulk archive used by `SIRI_PROVIDER=bods`: <https://data.bus-data.dft.gov.uk/avl/download/bulk_archive>

## Why this container

The UK Department for Transport Bus Open Data Service (BODS) publishes a bulk SIRI VehicleMonitoring archive for bus AVL positions. The generalized [`siri`](../siri/README.md) feeder already knows how to poll, parse, deduplicate, and emit this feed as CloudEvents.

These source-specific images do **not** copy that code. They inherit the maintained `siri` transport images and bake only the non-secret BODS configuration, giving operators a stable `uk-bods-siri` deployment target while keeping the parser and event contract centralized.

> [!IMPORTANT]

> **Contract change.** The previous bespoke images emitted `uk.gov.dft.bods.*` events. These thin-wrapper images emit the generalized `siri` contract: `org.siri.Operator` and `org.siri.VehiclePosition`. Update consumers, KQL queries, and dashboards to use the `org.siri.*` event/table names.

## What ships in the box
| Image | Transport | Inherits | Baked configuration |
| --- | --- | --- | --- |
| `ghcr.io/clemensv/real-time-sources-uk-bods-siri` | Apache Kafka 2.x (Azure Event Hubs, Microsoft Fabric Event Streams, Confluent Cloud, plain Kafka) | `ghcr.io/clemensv/real-time-sources/siri:latest` | `SIRI_PROVIDER=bods`, `SIRI_DATA_TYPES=vm` |
| `ghcr.io/clemensv/real-time-sources-uk-bods-siri-mqtt` | MQTT 5.0 broker (Mosquitto, EMQX, HiveMQ, Azure Event Grid MQTT, Microsoft Fabric MQTT) | `ghcr.io/clemensv/real-time-sources/siri-mqtt:latest` | `SIRI_PROVIDER=bods`, `SIRI_DATA_TYPES=vm` |
| `ghcr.io/clemensv/real-time-sources-uk-bods-siri-amqp` | AMQP 1.0 (RabbitMQ AMQP 1.0 plugin, ActiveMQ Artemis, Qpid Dispatch, Azure Service Bus, Azure Event Hubs) | `ghcr.io/clemensv/real-time-sources/siri-amqp:latest` | `SIRI_PROVIDER=bods`, `SIRI_DATA_TYPES=vm` |
## Image contract
| Aspect | Value |
| --- | --- |
| Base image | The corresponding generalized `siri` transport image |
| Default entry point | Inherited: `python -m siri_kafka feed`, `python -m siri_mqtt feed`, or `python -m siri_amqp feed` |
| Exposed ports | none — the feeder is an outbound publisher only |
| Persistent state | `STATE_FILE` (default inherited from `siri`; mount a volume for restarts) |
| Source contract | `SIRI_PROVIDER=bods`, `SIRI_DATA_TYPES=vm`, default BODS bulk-archive URL |
| Runtime secrets | `SIRI_API_KEY` or `BODS_API_KEY`, broker credentials / connection strings |
## Installing the container images

```bash
docker pull ghcr.io/clemensv/real-time-sources-uk-bods-siri:latest
docker pull ghcr.io/clemensv/real-time-sources-uk-bods-siri-mqtt:latest
docker pull ghcr.io/clemensv/real-time-sources-uk-bods-siri-amqp:latest
```

## Environment variables

### Source configuration
| Variable | Required | Description |
| --- | --- | --- |
| `SIRI_PROVIDER` | no | Baked as `bods`; override only for diagnostics. |
| `SIRI_DATA_TYPES` | no | Baked as `vm`; BODS fold-in emits VehicleMonitoring. |
| `SIRI_URL` | no | Optional override. Empty uses the generalized feeder's `DEFAULT_BODS_URL` bulk archive. |
| `SIRI_API_KEY` | no | Runtime BODS API key. Preferred generic name. |
| `BODS_API_KEY` | no | Backward-compatible key name accepted by `siri`. |
| `SIRI_OPERATORS` | no | Optional comma-separated BODS operator filter. |
| `POLLING_INTERVAL` | no | Poll interval in seconds; default `30`. |
| `STATE_FILE` | no | Dedupe state path. Mount a volume for persistent state. |
| `ONCE_MODE` | no | `true` runs one polling cycle and exits. |
### Kafka destination
| Variable | Required | Description |
| --- | --- | --- |
| `CONNECTION_STRING` | yes, unless using raw Kafka vars | Event Hubs / Fabric Event Stream / test Kafka connection string. |
| `KAFKA_BOOTSTRAP_SERVERS` | yes, unless using `CONNECTION_STRING` | Kafka bootstrap server list. |
| `KAFKA_TOPIC` | no | Destination topic when not supplied by `CONNECTION_STRING`; inherited default is `siri`. |
| `SASL_USERNAME` / `SASL_PASSWORD` | no | Credentials when not using `CONNECTION_STRING`. |
| `KAFKA_ENABLE_TLS` | no | Set `false` for local plaintext Kafka. |
### MQTT destination
| Variable | Required | Description |
| --- | --- | --- |
| `MQTT_BROKER_URL` | yes | Broker URL (`mqtt://` or `mqtts://`). |
| `MQTT_AUTH_MODE` | no | `anonymous`, `userpass`, or `entra`. |
| `MQTT_USERNAME` / `MQTT_PASSWORD` | no | Credentials for `userpass`. |
| `MQTT_CLIENT_ID` | no | MQTT client id. |
| `MQTT_ENABLE_TLS` | no | Enable TLS when component host/port variables are used. |
### AMQP destination
| Variable | Required | Description |
| --- | --- | --- |
| `AMQP_BROKER_URL` | yes, unless using component vars | Full AMQP URL. |
| `AMQP_ADDRESS` | no | Broker node/address; inherited default is `siri`. |
| `AMQP_AUTH_MODE` | no | `password`, `entra`, or `sas`. |
| `AMQP_USERNAME` / `AMQP_PASSWORD` | no | Generic broker credentials. |
| `AMQP_ENTRA_AUDIENCE` / `AMQP_ENTRA_CLIENT_ID` | no | Entra CBS settings. |
| `AMQP_SAS_KEY_NAME` / `AMQP_SAS_KEY` | no | SAS CBS settings. |
## Using the Kafka image

### With Azure Event Hubs or Fabric Event Streams

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/uk-bods-siri.json \
  -e SIRI_API_KEY="<bods-api-key>" \
  -e CONNECTION_STRING="<event-hubs-or-fabric-connection-string>" \
  ghcr.io/clemensv/real-time-sources-uk-bods-siri:latest
```

### With a local Kafka broker

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/uk-bods-siri.json \
  -e SIRI_API_KEY="<bods-api-key>" \
  -e KAFKA_BOOTSTRAP_SERVERS="host.docker.internal:9092" \
  -e KAFKA_TOPIC="uk-bods-siri" \
  -e KAFKA_ENABLE_TLS=false \
  ghcr.io/clemensv/real-time-sources-uk-bods-siri:latest
```

## Using the MQTT image

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/uk-bods-siri.json \
  -e SIRI_API_KEY="<bods-api-key>" \
  -e MQTT_BROKER_URL="mqtts://<broker-host>:8883" \
  -e MQTT_AUTH_MODE=userpass \
  -e MQTT_USERNAME="<username>" \
  -e MQTT_PASSWORD="<password>" \
  ghcr.io/clemensv/real-time-sources-uk-bods-siri-mqtt:latest
```

The MQTT topics come from the generalized SIRI contract: `transit/siri/{operator_ref}/info` and `transit/siri/{operator_ref}/{vehicle_ref}/position`.

## Using the AMQP image

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/uk-bods-siri.json \
  -e SIRI_API_KEY="<bods-api-key>" \
  -e AMQP_BROKER_URL="amqps://<user>:<password>@<broker-host>:5671/siri" \
  ghcr.io/clemensv/real-time-sources-uk-bods-siri-amqp:latest
```

## Azure templates

The source ships the same five deployment shapes as the generalized `siri` feeder, but preconfigured for BODS:

- `azure-template.json` — Kafka container against an existing Kafka/Event Hubs/Fabric endpoint.

- `azure-template-with-eventhub.json` — Kafka container plus a new Event Hubs namespace.

- `azure-template-mqtt.json` — MQTT container against an existing MQTT broker.

- `azure-template-with-eventgrid-mqtt.json` — MQTT container plus an Event Grid namespace broker.

- `azure-template-with-servicebus.json` — AMQP container plus a Service Bus namespace.

All templates deploy the consolidated `siri` image for the transport family and set `SIRI_PROVIDER=bods` plus `SIRI_DATA_TYPES=vm`. Secrets stay as ARM secure parameters.

## Database schemas and handling

Use [kql/uk-bods-siri.kql](kql/uk-bods-siri.kql) to create typed Eventhouse / ADX tables. The emitted table names are `org.siri.Operator` and `org.siri.VehiclePosition` to match the generalized event contract.

