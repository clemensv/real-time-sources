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


## MQTT and AMQP companion transports

This source now ships separate Kafka, MQTT, and AMQP containers. MQTT publishes binary-mode CloudEvents to the UNS topic tree below; AMQP publishes the same CloudEvents to the configured AMQP address with subject and routing axes in message/application properties.

Topic templates:
- `seismic/jp/jma/jma-bosai-quake/{prefecture}/{magnitude_bucket}/{event_id}/{serial}/report`

- MQTT image: `ghcr.io/clemensv/real-time-sources-jma-bosai-quake-mqtt:latest` (`Dockerfile.mqtt`)
- AMQP image: `ghcr.io/clemensv/real-time-sources-jma-bosai-quake-amqp:latest` (`Dockerfile.amqp`)
- Azure templates: `azure-template-mqtt.json`, `azure-template-with-eventgrid-mqtt.json`, `azure-template-with-servicebus.json`.
- `magnitude_bucket` uses `m0` through `m9`; unknown or negative magnitude uses `mx`.
