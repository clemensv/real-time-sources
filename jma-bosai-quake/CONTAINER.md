# JMA Bosai Earthquake Bridge Container

This container polls the JMA Bosai earthquake list and detail JSON endpoints and writes new earthquake reports to Kafka-compatible endpoints as structured JSON CloudEvents. Event types and schemas are documented in [EVENTS.md](EVENTS.md).

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
