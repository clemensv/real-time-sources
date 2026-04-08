# Wallonia ISSeP

This source bridges the Wallonia ISSeP (Institut Scientifique de Service Public) air quality sensor API into Kafka as CloudEvents. It covers the low-cost sensor network deployed across Wallonia, Belgium, and emits both reference data and near-real-time telemetry into a single topic.

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

## Upstream links

- Dataset: `https://www.odwb.be/explore/dataset/last-data-capteurs-qualite-de-l-air-issep/`
- API: `https://www.odwb.be/api/explore/v2.1/catalog/datasets/last-data-capteurs-qualite-de-l-air-issep/records`
- ISSeP: `https://www.issep.be/`
