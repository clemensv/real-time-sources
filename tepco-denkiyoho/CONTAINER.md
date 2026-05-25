# TEPCO Denki Yoho Container

This container bridges TEPCO Electricity Forecast (でんき予報) open CSV data to Apache Kafka-compatible endpoints as structured JSON CloudEvents.

## Upstream

The bridge polls `https://www.tepco.co.jp/forecast/html/images/juyo-d1-j.csv`, a Shift-JIS CSV updated about every five minutes. It covers the TEPCO service area in the Kanto region and emits daily supply capacity, five-minute actual demand, and hourly demand forecast events.

Event shapes are documented in [EVENTS.md](EVENTS.md).

## Pull

```shell
docker pull ghcr.io/clemensv/real-time-sources-tepco-denkiyoho:latest
```

## Kafka broker

```shell
docker run --rm \
  -e KAFKA_BOOTSTRAP_SERVERS='broker:9092' \
  -e KAFKA_TOPIC='tepco-denkiyoho' \
  -e KAFKA_ENABLE_TLS='false' \
  ghcr.io/clemensv/real-time-sources-tepco-denkiyoho:latest
```

For SASL PLAIN, add `SASL_USERNAME` and `SASL_PASSWORD`. If TLS is enabled, omit `KAFKA_ENABLE_TLS=false`.

## Event Hubs or Fabric Event Streams

Use an Event Hubs-style connection string or the custom endpoint connection string from Fabric Event Streams:

```shell
docker run --rm \
  -e CONNECTION_STRING='Endpoint=sb://namespace.servicebus.windows.net/;SharedAccessKeyName=policy;SharedAccessKey=key;EntityPath=eventhub' \
  ghcr.io/clemensv/real-time-sources-tepco-denkiyoho:latest
```

The Docker E2E/plain Kafka convention is also supported:

```shell
CONNECTION_STRING='BootstrapServer=host:9092;EntityPath=tepco-denkiyoho'
KAFKA_ENABLE_TLS=false
```

## Environment variables

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `CONNECTION_STRING` | No | empty | Event Hubs/Fabric connection string, or `BootstrapServer=...;EntityPath=...`. Overrides explicit Kafka settings. |
| `KAFKA_BOOTSTRAP_SERVERS` | Required without `CONNECTION_STRING` | empty | Kafka bootstrap server list. |
| `KAFKA_TOPIC` | No | `tepco-denkiyoho` | Kafka topic. |
| `SASL_USERNAME` | No | empty | SASL PLAIN username. |
| `SASL_PASSWORD` | No | empty | SASL PLAIN password. |
| `KAFKA_ENABLE_TLS` | No | `true` | Set `false` for plaintext Kafka in local/E2E flows. |
| `POLLING_INTERVAL` | No | `300` | Seconds between polls. |
| `STATE_FILE` | No | `./state/tepco-denkiyoho.json` | Persistent deduplication state file. |
| `ONCE_MODE` | No | `false` | Set `true` to run one poll and exit. |

Mount a volume for `./state` if deduplication state should survive container replacement.


## Transports

This source now ships Kafka plus MQTT and AMQP companion feeders. MQTT publishes binary-mode CloudEvents into the documented topic tree for wildcard subscribers and retained last-known-value use cases. AMQP publishes the same CloudEvents to a broker address for queue/topic consumers. Deployment templates include `azure-template.json`, `azure-template-with-eventhub.json`, `azure-template-mqtt.json`, `azure-template-with-eventgrid-mqtt.json`, `azure-template-amqp.json`, and `azure-template-with-servicebus.json`. Dockerfiles: `Dockerfile`, `Dockerfile.mqtt`, `Dockerfile.amqp`.
