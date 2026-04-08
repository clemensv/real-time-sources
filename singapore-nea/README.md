# Singapore NEA Weather and Air Quality Bridge

This bridge fetches real-time weather observations and regional air quality
data from the
[Singapore National Environment Agency (NEA)](https://data.gov.sg/datasets?topics=environment)
and emits them as CloudEvents into Apache Kafka or Azure Event Hubs.

## Data Model

The bridge emits weather and air quality data into two Kafka topics:

### Topic: `singapore-nea`

Key: `{station_id}` (NEA device IDs like `S109`, `S50`)

| Event Type | Description |
|---|---|
| `SG.Gov.NEA.Weather.Station` | Reference data for each station (emitted at startup) |
| `SG.Gov.NEA.Weather.WeatherObservation` | Real-time observations: temperature, rainfall, humidity, wind speed/direction |

### Topic: `singapore-nea-airquality`

Key: `{region}` (`west`, `east`, `central`, `south`, `north`)

| Event Type | Description |
|---|---|
| `SG.Gov.NEA.AirQuality.Region` | Reference data for NEA air quality regions |
| `SG.Gov.NEA.AirQuality.PSIReading` | Hourly PSI and pollutant sub-index readings per region |
| `SG.Gov.NEA.AirQuality.PM25Reading` | Hourly PM2.5 concentration per region |

## Upstream API

- **Base URL**: `https://api.data.gov.sg/v1/environment/`
- **Auth**: None (fully open, Singapore Open Data License)
- **Rate limit**: Fair use — weather polls every 5 minutes by default and air quality every hour
- **Coverage**: ~62 rainfall stations, ~13 temperature/wind/humidity stations
- **Weather endpoints**: `air-temperature`, `rainfall`, `relative-humidity`, `wind-speed`, `wind-direction`
- **Air quality endpoints**: `psi`, `pm25`

## Source Files

| File | Description |
|---|---|
| [xreg/singapore_nea.xreg.json](xreg/singapore_nea.xreg.json) | xRegistry manifest |
| [singapore_nea/singapore_nea.py](singapore_nea/singapore_nea.py) | Runtime bridge |
| [singapore_nea/air_quality.py](singapore_nea/air_quality.py) | Air quality polling helpers |
| [singapore_nea_producer/](singapore_nea_producer/) | Generated producer (xrcg 0.10.1) |
| [tests/](tests/) | Unit tests |
| [Dockerfile](Dockerfile) | Container image |
| [CONTAINER.md](CONTAINER.md) | Deployment contract |
| [EVENTS.md](EVENTS.md) | Event catalog |
