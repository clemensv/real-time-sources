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
