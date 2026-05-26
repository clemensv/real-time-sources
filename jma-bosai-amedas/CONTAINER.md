# JMA Bosai AMeDAS Container

This container bridges Japan Meteorological Agency Bosai AMeDAS station metadata and ten-minute meteorological observations to Kafka-compatible endpoints using CloudEvents structured JSON.

## Upstream source

- Publisher: Japan Meteorological Agency (JMA / 気象庁)
- Authentication: none
- Cadence: 10 minutes for observation snapshots
- License: Japanese government open data, free for use and redistribution

The bridge fetches station metadata from `amedastable.json` at startup and every `STATION_METADATA_REFRESH_HOURS` hours, then polls `latest_time.txt` and the corresponding `data/map/{YYYYMMDDHHMM}00.json` snapshot. Optional per-station detail enrichment can fetch `data/point/{station_code}/{YYYYMMDD_HH}.json` for selected station codes.

## Environment variables

| Variable | Required | Default | Description |
|---|---:|---|---|
| `CONNECTION_STRING` | Yes for container use | empty | Event Hubs/Fabric connection string or local form `BootstrapServer=host:port;EntityPath=topic`. |
| `KAFKA_TOPIC` | No | `jma-bosai-amedas` | Kafka topic when not supplied by `EntityPath`. |
| `POLLING_INTERVAL` | No | `600` | Seconds between poll cycles. |
| `STATION_METADATA_REFRESH_HOURS` | No | `168` | Hours between station reference-data re-emission. |
| `STATE_FILE` | No | `./state/jma-bosai-amedas.json` | Persistent state file for last snapshot and metadata refresh timestamps. |
| `POINT_STATION_CODES` | No | empty | Comma-separated station codes, or `all`, for point-detail enrichment. Empty avoids fetching ~1300 detail files every cycle. |
| `POINT_REQUEST_DELAY` | No | `0.25` | Seconds to wait between point-detail requests, limiting enrichment to about four station files per second by default. |
| `KAFKA_ENABLE_TLS` | No | `true` | Set to `false` for local non-TLS Kafka, including Docker E2E. |

## Docker examples

### Local Kafka

```shell
docker run --rm \
  -e CONNECTION_STRING='BootstrapServer=host.docker.internal:9092;EntityPath=jma-bosai-amedas' \
  -e KAFKA_ENABLE_TLS=false \
  ghcr.io/clemensv/real-time-sources-jma-bosai-amedas:latest
```

### Azure Event Hubs or Fabric Event Streams

```shell
docker run --rm \
  -e CONNECTION_STRING='Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy>;SharedAccessKey=<key>;EntityPath=<eventhub>' \
  ghcr.io/clemensv/real-time-sources-jma-bosai-amedas:latest
```

## Event contract

Events are emitted as CloudEvents 1.0 structured JSON. Both `JP.JMA.Amedas.Station` and `JP.JMA.Amedas.Observation` use Kafka key and CloudEvents subject `jp.jma.amedas/{station_code}`. See [EVENTS.md](EVENTS.md).


## MQTT and AMQP companion transports

This source now ships separate Kafka, MQTT, and AMQP containers. MQTT publishes binary-mode CloudEvents to the UNS topic tree below; AMQP publishes the same CloudEvents to the configured AMQP address with subject and routing axes in message/application properties.

Topic templates:
- `weather/jp/jma/jma-bosai-amedas/{prefecture}/{station_code}/info`
- `weather/jp/jma/jma-bosai-amedas/{prefecture}/{station_code}/observation`

- MQTT image: `ghcr.io/clemensv/real-time-sources-jma-bosai-amedas-mqtt:latest` (`Dockerfile.mqtt`)
- AMQP image: `ghcr.io/clemensv/real-time-sources-jma-bosai-amedas-amqp:latest` (`Dockerfile.amqp`)
- Azure templates: `azure-template-mqtt.json`, `azure-template-with-eventgrid-mqtt.json`, `azure-template-with-servicebus.json`.
