# JMA Bosai Volcano Container

This container polls public Japan Meteorological Agency (JMA) Bosai volcano JSON feeds and publishes structured JSON CloudEvents to Apache Kafka, Azure Event Hubs, or Microsoft Fabric Event Streams. It emits volcano reference data first, then active volcanic warnings and eruption observations.

## Upstream source

- Volcano catalog: `https://www.jma.go.jp/bosai/volcano/const/volcano_list.json`
- Active warnings: `https://www.jma.go.jp/bosai/volcano/data/warning.json`
- Eruptions: `https://www.jma.go.jp/bosai/volcano/data/eruption.json`

The feeds require no authentication and are published under Japanese government open-data terms.

## Environment variables

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `CONNECTION_STRING` | no | empty | Azure Event Hubs/Fabric Event Stream or `BootstrapServer=host:port;EntityPath=topic` connection string. |
| `KAFKA_BOOTSTRAP_SERVERS` | required without `CONNECTION_STRING` | empty | Kafka bootstrap servers. |
| `KAFKA_TOPIC` | no | `jma-bosai-volcano` | Kafka topic. |
| `SASL_USERNAME` / `SASL_PASSWORD` | no | empty | SASL PLAIN credentials for Kafka. |
| `KAFKA_ENABLE_TLS` | no | `true` | Set to `false` for local plaintext Kafka. |
| `POLLING_INTERVAL` | no | `60` | Seconds between warning and eruption polls. |
| `VOLCANO_METADATA_REFRESH_HOURS` | no | `720` | Hours between reference catalog re-emissions. |
| `STATE_FILE` | no | `./state/jma-bosai-volcano.json` | Persistent dedupe state file. |
| `ONCE_MODE` | no | `false` | Exit after one poll cycle when true. |

## Docker examples

```shell
docker pull ghcr.io/clemensv/real-time-sources-jma-bosai-volcano:latest
```

Plain Kafka broker:

```shell
docker run --rm \
  -e KAFKA_BOOTSTRAP_SERVERS='broker:9092' \
  -e KAFKA_TOPIC='jma-bosai-volcano' \
  -e KAFKA_ENABLE_TLS='false' \
  ghcr.io/clemensv/real-time-sources-jma-bosai-volcano:latest
```

Azure Event Hubs or Fabric Event Streams:

```shell
docker run --rm \
  -e CONNECTION_STRING='<connection-string>' \
  ghcr.io/clemensv/real-time-sources-jma-bosai-volcano:latest
```

Events are CloudEvents documented in [EVENTS.md](EVENTS.md).


## MQTT and AMQP companion transports

This source now ships separate Kafka, MQTT, and AMQP containers. MQTT publishes binary-mode CloudEvents to the UNS topic tree below; AMQP publishes the same CloudEvents to the configured AMQP address with subject and routing axes in message/application properties.

Topic templates:
- `weather/jp/jma/jma-bosai-volcano/{prefecture}/{volcano_code}/info`
- `weather/jp/jma/jma-bosai-volcano/{prefecture}/{volcano_code}/warning`
- `weather/jp/jma/jma-bosai-volcano/{prefecture}/{volcano_code}/eruption`

- MQTT image: `ghcr.io/clemensv/real-time-sources-jma-bosai-volcano-mqtt:latest` (`Dockerfile.mqtt`)
- AMQP image: `ghcr.io/clemensv/real-time-sources-jma-bosai-volcano-amqp:latest` (`Dockerfile.amqp`)
- Azure templates: `azure-template-mqtt.json`, `azure-template-with-eventgrid-mqtt.json`, `azure-template-with-servicebus.json`.
