<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/be.png" alt="Belgium / Wallonia" width="64" height="48"><br>
<sub><b>Belgium / Wallonia</b></sub>
</td>
<td valign="middle">

# Wallonia ISSeP

<sub>low-cost air quality sensors · Kafka · MQTT · AMQP · <a href="https://www.issep.be/">upstream</a> · <a href="https://www.odwb.be/explore/dataset/last-data-capteurs-qualite-de-l-air-issep/information/">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-3_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Belgium / Wallonia — low-cost air quality sensors

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#wallonia-issep) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/wallonia_issep.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://www.issep.be/)

</td></tr></table>
<!-- source-hero:end -->

This source bridges the Wallonia ISSeP (Institut Scientifique de Service Public) air quality sensor API into Kafka as CloudEvents. It covers the low-cost sensor network deployed across Wallonia, Belgium, and emits both reference data and near-real-time telemetry into a single topic.

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://www.issep.be/>
- API / data documentation: <https://www.odwb.be/explore/dataset/last-data-capteurs-qualite-de-l-air-issep/information/>

<!-- upstream-links:end -->

## What it publishes

- Sensor configuration reference events for each deployed sensor unit
- Observation events for near-real-time air quality measurements, deduplicated per configuration and timestamp

## Data families reviewed

| Family | Endpoint | Identity | Keep / drop | Reason |
|---|---|---|---|---|
| Sensor records | Opendatasoft `records` endpoint | `id_configuration` + `moment` | Keep | This is the core telemetry feed containing all pollutant and environmental readings. |
| Sensor configurations | Derived from records | `id_configuration` | Keep | Each distinct configuration ID represents a deployed sensor unit. Since the API has no separate station list endpoint, configurations are derived from the data records. |

## Upstream notes

- API: `https://www.odwb.be/api/explore/v2.1/catalog/datasets/last-data-capteurs-qualite-de-l-air-issep/records`
- Transport: REST over HTTPS (Opendatasoft API v2.1)
- Auth: none
- License: CC BY 4.0
- Update cadence: near-real-time (sensors report every ~10 minutes)
- The dataset contains only the latest reading per configuration (7 sensors currently active)
- Negative raw values (e.g. `no2=-4`) are valid electrochemical sensor readings
- Fields include raw sensor readings, calibrated ppb and µg/m³ values, PM concentrations, environmental data (temperature, pressure, humidity), battery/solar status, and reference station comparison values

## Event model

- `be.issep.airquality.SensorConfiguration` — sensor configuration reference data keyed by `{configuration_id}`
- `be.issep.airquality.Observation` — air quality observation telemetry keyed by `{configuration_id}`

## Running locally

Generate the producer code first:

```powershell
.\generate_producer.ps1
pip install wallonia_issep_producer\wallonia_issep_producer_data
pip install wallonia_issep_producer\wallonia_issep_producer_kafka_producer
pip install -e .
```

Then start the bridge:

```powershell
python -m wallonia_issep feed --kafka-bootstrap-servers localhost:9092 --kafka-enable-tls false
```

## Running the MQTT/UNS bridge

Generate the MQTT producer code:

```powershell
.\generate_mqtt_producer.ps1
pip install wallonia_issep_mqtt_producer\wallonia_issep_mqtt_producer_data
pip install wallonia_issep_mqtt_producer\wallonia_issep_mqtt_producer_mqtt_client
pip install -e wallonia_issep_mqtt
```

Start the MQTT bridge:

```powershell
python -m wallonia_issep_mqtt feed --broker-url mqtt://localhost:1883
```

Topic tree: `air-quality/be/issep/wallonia-issep/{province}/{configuration_id}/{info|observation}`

## Upstream links

- Dataset: `https://www.odwb.be/explore/dataset/last-data-capteurs-qualite-de-l-air-issep/`
- API: `https://www.odwb.be/api/explore/v2.1/catalog/datasets/last-data-capteurs-qualite-de-l-air-issep/records`
- ISSeP: `https://www.issep.be/`

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwallonia-issep%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwallonia-issep%2Fazure-template-with-eventhub.json)

## AMQP 1.0 companion feeder

This source now ships the standard Kafka + MQTT + AMQP transport trio. The AMQP companion runs from `wallonia_issep_amqp/`, uses the generated `wallonia_issep_amqp_producer/` package, and publishes the same CloudEvents and schemas documented in `EVENTS.md` to one AMQP 1.0 address (default `wallonia-issep`). It supports generic AMQP 1.0 brokers with SASL PLAIN and Azure Service Bus / Event Hubs with CBS token authentication.

Build and run locally:

```bash
docker build -f Dockerfile.amqp -t wallonia-issep-amqp .
docker run --rm \
  -e AMQP_BROKER_URL=amqp://user:password@broker:5672/wallonia-issep \
  -e ONCE_MODE=true \
  wallonia-issep-amqp
```

For Azure Service Bus, deploy `azure-template-with-servicebus.json` (also mirrored at `infra/azure-template-amqp.json`) or run the container with `AMQP_AUTH_MODE=entra`, `AMQP_HOST=<namespace>.servicebus.windows.net`, `AMQP_TLS=true`, and `AMQP_ADDRESS=wallonia-issep`.

