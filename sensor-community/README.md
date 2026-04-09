# Sensor.Community

Sensor.Community, formerly Luftdaten.info, is a large citizen-science sensor network that publishes near-real-time environmental measurements from thousands of community-operated stations. This source polls the public Airrohr API and republishes selected sensor metadata and readings as CloudEvents into Kafka.

## Upstream coverage

I audited the public real-time API surface used by this bridge:

| Family | Transport | Identity | Cadence | Keep/Drop | Reason |
| --- | --- | --- | --- | --- | --- |
| Type-filter feed | `GET /filter/type={sensor_type}` | `sensor.id` | Near-real-time rolling latest value per sensor type | Keep | This is the main public bulk feed for real-time telemetry and sensor metadata. |
| Country-filter feed | `GET /filter/country={country}` | `sensor.id` | Near-real-time rolling latest value per country | Drop | It is a scoped projection of the same latest-reading data already covered by the type-filter feeds. The bridge applies country filtering locally instead. |
| Sensor detail feed | `GET /sensor/{sensor_id}/` | `sensor.id` | Near-real-time recent history for one sensor | Drop as a polled family | It is useful as a canonical source URI and ad hoc inspection endpoint, but it is a per-sensor detail projection of the same telemetry families already modeled. |

The bridge polls configured sensor types and keeps the full reading shape for the documented value types it encounters: particulate matter (`P0`, `P1`, `P2`, `P4`), temperature, humidity, pressure, pressure at sea level, and supported noise values.

## Event model

- `io.sensor.community.SensorInfo` — reference data for a sensor node, emitted when first seen and whenever metadata changes.
- `io.sensor.community.SensorReading` — the latest telemetry reading for a sensor at a specific timestamp.

Both event types use `sensor_id` as the CloudEvents `subject` and Kafka key.

## Running locally

Install the generated producer packages first, then install the source package:

```powershell
pip install .\sensor_community_producer\sensor_community_producer_data
pip install .\sensor_community_producer\sensor_community_producer_kafka_producer
pip install -e .
```

Run the feed:

```powershell
python -m sensor_community feed --connection-string "BootstrapServer=localhost:9092;EntityPath=sensor-community"
```

Limit scope:

```powershell
$env:SENSOR_TYPES = "SDS011,BME280"
$env:COUNTRIES = "DE,NL"
python -m sensor_community feed --connection-string "BootstrapServer=localhost:9092;EntityPath=sensor-community"
```

## Configuration

- `CONNECTION_STRING` — Event Hubs/Fabric or `BootstrapServer=host:port;EntityPath=topic`
- `KAFKA_BOOTSTRAP_SERVERS` — plain Kafka bootstrap servers
- `KAFKA_TOPIC` — Kafka topic if not supplied by connection string
- `SASL_USERNAME` / `SASL_PASSWORD` — optional SASL PLAIN credentials
- `POLLING_INTERVAL` — polling interval in seconds, default `300`
- `SENSOR_TYPES` — comma-separated sensor types, default `SDS011,BME280,SPS30,DHT22,PMS5003,SHT31,BMP280`
- `COUNTRIES` — optional comma-separated ISO country filter
- `STATE_FILE` — persisted dedup and metadata state file
- `KAFKA_ENABLE_TLS` — set to `false` for plain Kafka when you want an explicit `PLAINTEXT` security protocol

## Upstream links

- Sensor.Community project: https://sensor.community/
- Airrohr API base: https://data.sensor.community/airrohr/v1/

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
