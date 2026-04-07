# Singapore NEA Weather Observation Bridge

This bridge fetches real-time weather observations from the
[Singapore National Environment Agency (NEA)](https://data.gov.sg/datasets?topics=environment)
and emits them as CloudEvents into Apache Kafka or Azure Event Hubs.

## Data Model

The bridge emits two event types into the `singapore-nea` topic, keyed by
`{station_id}` (NEA device IDs like S109, S50):

| Event Type | Description |
|---|---|
| `SG.Gov.NEA.Weather.Station` | Reference data for each station (emitted at startup) |
| `SG.Gov.NEA.Weather.WeatherObservation` | Real-time observations: temperature, rainfall, humidity, wind speed/direction |

## Upstream API

- **Base URL**: `https://api.data.gov.sg/v1/environment/`
- **Auth**: None (fully open, Singapore Open Data License)
- **Rate limit**: Fair use — the bridge polls every 5 minutes by default
- **Coverage**: ~62 rainfall stations, ~13 temperature/wind/humidity stations
- **Endpoints**: `air-temperature`, `rainfall`, `relative-humidity`, `wind-speed`, `wind-direction`

## Source Files

| File | Description |
|---|---|
| [xreg/singapore_nea.xreg.json](xreg/singapore_nea.xreg.json) | xRegistry manifest |
| [singapore_nea/singapore_nea.py](singapore_nea/singapore_nea.py) | Runtime bridge |
| [singapore_nea_producer/](singapore_nea_producer/) | Generated producer (xrcg 0.10.1) |
| [tests/](tests/) | Unit tests |
| [Dockerfile](Dockerfile) | Container image |
| [CONTAINER.md](CONTAINER.md) | Deployment contract |
| [EVENTS.md](EVENTS.md) | Event catalog |
