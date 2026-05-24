# JMA Bosai Warning Container

The Kafka container polls Japan Meteorological Agency public Bosai weather warning and tsunami alert JSON feeds and publishes structured CloudEvents to Kafka-compatible endpoints. `Dockerfile.mqtt` builds the MQTT/UNS weather-warning feeder.

## Environment

Required: one of `CONNECTION_STRING` or `KAFKA_BOOTSTRAP_SERVERS`.

Optional:

- `KAFKA_TOPIC_WARNING` (default `jma-bosai-warning`)
- `KAFKA_TOPIC_TSUNAMI` (default `jma-bosai-tsunami`)
- `POLLING_INTERVAL_WARNING` (default `60` seconds)
- `POLLING_INTERVAL_TSUNAMI` (default `30` seconds)
- `OFFICE_METADATA_REFRESH_HOURS` (default `720`)
- `STATE_FILE` (default `.\state\jma-bosai-warning.json`)
- `KAFKA_ENABLE_TLS` (set `false` for plain Kafka)

## Run

Kafka:

```powershell
docker build -t jma-bosai-warning ./jma-bosai-warning
docker run --rm -e CONNECTION_STRING="BootstrapServer=host.docker.internal:9092;EntityPath=jma-bosai-warning" -e KAFKA_ENABLE_TLS=false jma-bosai-warning
```

MQTT/UNS:

```powershell
docker build -f ./jma-bosai-warning/Dockerfile.mqtt -t jma-bosai-warning-mqtt ./jma-bosai-warning
docker run --rm -e MQTT_BROKER_URL="mqtt://host.docker.internal:1883" jma-bosai-warning-mqtt
```

The MQTT feeder publishes retained office references to `alerts/jp/jma/jma-bosai-warning/{prefecture}/REFERENCE/{office_code}/{area_code}/office` and non-retained warning records to `alerts/jp/jma/jma-bosai-warning/{prefecture}/{severity}/{office_code}/{area_code}/warning`.

For Azure Event Hubs or Fabric Event Streams, pass the full connection string in `CONNECTION_STRING`. Events are CloudEvents; see `EVENTS.md` for schemas and keys.
