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

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsensor-community%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsensor-community%2Fazure-template-with-eventhub.json)


## MQTT 5.0 / Unified Namespace feeder

Image: `real-time-sources-sensor-community-mqtt`. Publishes binary-mode CloudEvents to `air-quality/intl/sensor-community/sensor-community/...`.

| Variable | Purpose |
|---|---|
| `MQTT_BROKER_URL` | Broker URL, for example `mqtt://host:1883`. |
| `MQTT_HOST`, `MQTT_PORT`, `MQTT_TLS` | Host/port/TLS alternatives to `MQTT_BROKER_URL`. |
| `MQTT_USERNAME`, `MQTT_PASSWORD` | Optional username/password authentication. |
| `MQTT_CONTENT_MODE` | CloudEvents content mode; default `binary`. |
| `ONCE_MODE` | Exit after one publish cycle for jobs/tests. |

[![Deploy MQTT BYO](https://img.shields.io/badge/Azure-Container%20(BYO%20MQTT)-0078D4?logo=microsoftazure&logoColor=white)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsensor-community%2Fazure-template-mqtt.json)
[![Deploy MQTT Event Grid](https://img.shields.io/badge/Azure-Container%20%2B%20Event%20Grid%20MQTT-0078D4?logo=microsoftazure&logoColor=white)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsensor-community%2Fazure-template-with-eventgrid-mqtt.json)

## AMQP 1.0 feeder

Image: `real-time-sources-sensor-community-amqp`. Publishes binary-mode CloudEvents to a configurable AMQP 1.0 address.

| Variable | Purpose |
|---|---|
| `AMQP_BROKER_URL` | Broker URL, for example `amqp://user:pass@host:5672/sensor-community`. |
| `AMQP_HOST`, `AMQP_PORT`, `AMQP_TLS` | Host/port/TLS alternatives to `AMQP_BROKER_URL`. |
| `AMQP_ADDRESS` | Queue/topic/address; default `sensor-community`. |
| `AMQP_AUTH_MODE` | `password`, `entra`, or `sas`. |
| `AMQP_USERNAME`, `AMQP_PASSWORD` | SASL PLAIN credentials. |
| `AMQP_ENTRA_CLIENT_ID`, `AMQP_ENTRA_AUDIENCE` | Entra CBS authentication settings. |
| `AMQP_SAS_KEY_NAME`, `AMQP_SAS_KEY` | SAS CBS authentication settings. |
| `AMQP_CONTENT_MODE` | CloudEvents content mode; default `binary`. |
| `ONCE_MODE` | Exit after one publish cycle for jobs/tests. |

[![Deploy AMQP BYO](https://img.shields.io/badge/Azure-Container%20(BYO%20AMQP)-0078D4?logo=microsoftazure&logoColor=white)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsensor-community%2Fazure-template-amqp.json)
[![Deploy AMQP Service Bus](https://img.shields.io/badge/Azure-Container%20%2B%20Service%20Bus-0078D4?logo=microsoftazure&logoColor=white)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsensor-community%2Fazure-template-with-servicebus.json)
