# JMA Bosai Warning Container

This container polls Japan Meteorological Agency public Bosai weather warning and tsunami alert JSON feeds and publishes structured CloudEvents to Kafka-compatible endpoints.

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

```powershell
docker build -t jma-bosai-warning ./jma-bosai-warning
docker run --rm -e CONNECTION_STRING="BootstrapServer=host.docker.internal:9092;EntityPath=jma-bosai-warning" -e KAFKA_ENABLE_TLS=false jma-bosai-warning
```

For Azure Event Hubs or Fabric Event Streams, pass the full connection string in `CONNECTION_STRING`. Events are CloudEvents; see `EVENTS.md` for schemas and keys.
