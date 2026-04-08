# Sensor.Community Container

This container polls the public Sensor.Community Airrohr API and emits CloudEvents for sensor metadata and readings into Kafka.

## Environment variables

- `CONNECTION_STRING` — Kafka/Event Hubs/Fabric connection string. For plain Kafka use `BootstrapServer=host:port;EntityPath=topic`.
- `KAFKA_BOOTSTRAP_SERVERS` — bootstrap server list when you do not use `CONNECTION_STRING`.
- `KAFKA_TOPIC` — Kafka topic name when it is not embedded in `CONNECTION_STRING`.
- `SASL_USERNAME` — SASL PLAIN username.
- `SASL_PASSWORD` — SASL PLAIN password.
- `POLLING_INTERVAL` — polling interval in seconds. Default: `300`.
- `SENSOR_TYPES` — comma-separated upstream sensor types to poll. Default: `SDS011,BME280,SPS30,DHT22,PMS5003,SHT31,BMP280`.
- `COUNTRIES` — optional comma-separated ISO country codes used to filter records after fetch.
- `STATE_FILE` — file path for dedup and reference snapshot state.
- `KAFKA_ENABLE_TLS` — optional boolean. Set to `false` for plain Kafka brokers when you want the producer configured explicitly with `PLAINTEXT`.

## Run with plain Kafka

```powershell
docker run --rm `
  -e CONNECTION_STRING="BootstrapServer=host.docker.internal:9092;EntityPath=sensor-community" `
  -e KAFKA_ENABLE_TLS=false `
  -e SENSOR_TYPES="SDS011,BME280" `
  ghcr.io/clemensv/real-time-sources/sensor-community:latest
```

## Run with Azure Event Hubs

```powershell
docker run --rm `
  -e CONNECTION_STRING="Endpoint=sb://namespace.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=...;EntityPath=sensor-community" `
  -e SENSOR_TYPES="SDS011,BME280,SPS30" `
  ghcr.io/clemensv/real-time-sources/sensor-community:latest
```

## Behavior

The bridge emits:

- `SensorInfo` reference events when a sensor appears for the first time or its metadata changes.
- `SensorReading` telemetry events when a sensor reports a new timestamp.

Both events share the same Kafka key and CloudEvents subject: `{sensor_id}`.
