# JMA Bosai Earthquake Bridge Container

The Kafka container polls the JMA Bosai earthquake list and detail JSON endpoints and writes new earthquake reports to Kafka-compatible endpoints as structured JSON CloudEvents. `Dockerfile.mqtt` builds the MQTT/UNS feeder for the same earthquake report stream. Event types and schemas are documented in [EVENTS.md](EVENTS.md).

## Image

```shell
docker pull ghcr.io/clemensv/real-time-sources-jma-bosai-quake:latest
```

## Kafka broker

```shell
docker run --rm \
  -e KAFKA_BOOTSTRAP_SERVERS='<host:port>' \
  -e KAFKA_TOPIC='jma-bosai-quake' \
  -e KAFKA_ENABLE_TLS='false' \
  ghcr.io/clemensv/real-time-sources-jma-bosai-quake:latest
```

For SASL/PLAIN brokers, also set `SASL_USERNAME` and `SASL_PASSWORD`. TLS is enabled by default unless `KAFKA_ENABLE_TLS=false`.

## Azure Event Hubs or Fabric Event Streams

Use an Event Hubs-style or Fabric custom endpoint connection string. The `EntityPath` value becomes the Kafka topic unless `KAFKA_TOPIC` is supplied separately.

```shell
docker run --rm \
  -e CONNECTION_STRING='<connection-string>' \
  ghcr.io/clemensv/real-time-sources-jma-bosai-quake:latest
```

## MQTT/UNS

```shell
docker build -f ./jma-bosai-quake/Dockerfile.mqtt -t jma-bosai-quake-mqtt ./jma-bosai-quake
docker run --rm -e MQTT_BROKER_URL='mqtt://host.docker.internal:1883' jma-bosai-quake-mqtt
```

The MQTT feeder publishes non-retained QoS 1 CloudEvents to `seismic/jp/jma/jma-bosai-quake/{prefecture}/{magnitude_bucket}/{event_id}/{serial}/report`, keeping the JMA serial in the topic so revisions are visible to subscribers.

## Environment variables

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `CONNECTION_STRING` | No | empty | Event Hubs or Fabric Event Stream connection string. Replaces explicit Kafka bootstrap and SASL settings. |
| `KAFKA_BOOTSTRAP_SERVERS` | Yes, unless `CONNECTION_STRING` is set | empty | Kafka bootstrap servers. |
| `KAFKA_TOPIC` | No | `jma-bosai-quake` | Kafka topic for emitted CloudEvents. |
| `SASL_USERNAME` | No | empty | SASL/PLAIN username. |
| `SASL_PASSWORD` | No | empty | SASL/PLAIN password. |
| `KAFKA_ENABLE_TLS` | No | `true` | Set to `false`, `0`, or `no` for plaintext Kafka, including local Docker E2E brokers. |
| `POLLING_INTERVAL` | No | `60` | Polling interval in seconds. |
| `STATE_FILE` | No | `.\\state\\jma-bosai-quake.json` | JSON file that stores the latest 1000 seen `(eid, ser)` report keys. |
| `ONCE_MODE` | No | `false` | Set to `true` to run exactly one polling cycle and exit. |

## Delivery behavior

The bridge polls `list.json`, skips already-seen `(eid, ser)` report serials, fetches the detail JSON when available, and emits one `JP.JMA.Quake.EarthquakeReport` per new report. State is persisted only after Kafka flush returns success.

## AMQP 1.0 container

The AMQP companion image publishes the same `Jma Bosai Quake` CloudEvents to a generic AMQP 1.0 broker, Azure Service Bus with Entra ID CBS, or a SAS-token Service Bus-compatible endpoint.

```bash
docker pull ghcr.io/clemensv/real-time-sources-jma-bosai-quake-amqp:latest
```

### Generic AMQP broker (SASL PLAIN)

```bash
docker run --rm   -e AMQP_BROKER_URL=amqp://broker:5672   -e AMQP_USERNAME=admin   -e AMQP_PASSWORD=admin   -e AMQP_ADDRESS=jma-bosai-quake   ghcr.io/clemensv/real-time-sources-jma-bosai-quake-amqp:latest
```

### Azure Service Bus (Entra ID)

```bash
docker run --rm   -e AMQP_HOST=<namespace>.servicebus.windows.net   -e AMQP_PORT=5671   -e AMQP_TLS=true   -e AMQP_ADDRESS=jma-bosai-quake   -e AMQP_AUTH_MODE=entra   -e AMQP_ENTRA_AUDIENCE=https://servicebus.azure.net/.default   ghcr.io/clemensv/real-time-sources-jma-bosai-quake-amqp:latest
```

### Service Bus emulator / SAS CBS

```bash
docker run --rm   -e AMQP_HOST=servicebus-emulator   -e AMQP_PORT=5672   -e AMQP_ADDRESS=jma-bosai-quake   -e AMQP_AUTH_MODE=sas   -e AMQP_SAS_KEY_NAME=RootManageSharedAccessKey   -e AMQP_SAS_KEY=<base64-key>   ghcr.io/clemensv/real-time-sources-jma-bosai-quake-amqp:latest
```

| Variable | Description | Default |
|---|---|---|
| `AMQP_BROKER_URL` | Optional AMQP URI for generic brokers. | unset |
| `AMQP_HOST` / `AMQP_PORT` | Broker host and port when no URI is supplied. | `localhost` / `5672` |
| `AMQP_ADDRESS` | Queue/topic/address to publish to. | `jma-bosai-quake` |
| `AMQP_USERNAME` / `AMQP_PASSWORD` | SASL PLAIN credentials for `AMQP_AUTH_MODE=password`. | unset |
| `AMQP_TLS` | Use TLS (`true`, `1`, or `yes`). | `false` |
| `AMQP_AUTH_MODE` | `password`, `entra`, or `sas`. | `password` |
| `AMQP_ENTRA_AUDIENCE` / `AMQP_ENTRA_CLIENT_ID` | Entra token scope and optional managed identity client ID. | Service Bus scope / unset |
| `AMQP_SAS_KEY_NAME` / `AMQP_SAS_KEY` | SAS CBS credentials. | unset |
| `AMQP_CONTENT_MODE` | CloudEvents content mode: `binary` or `structured`. | `binary` |

[![Deploy AMQP to Azure Service Bus](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fjma-bosai-quake%2Fazure-template-amqp.json)

