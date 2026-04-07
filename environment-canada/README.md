# Environment Canada Weather Observation Bridge

This bridge fetches real-time Surface Weather Observations (SWOB) from
[Environment and Climate Change Canada (ECCC)](https://api.weather.gc.ca/)
via the OGC API and emits them as CloudEvents into Apache Kafka or Azure
Event Hubs.

## Data Model

The bridge emits two event types into the `environment-canada` topic, both
keyed by `{msc_id}` (Meteorological Service of Canada station identifier):

| Event Type | Description |
|---|---|
| `CA.Gov.ECCC.Weather.Station` | Reference data for SWOB stations (emitted at startup) |
| `CA.Gov.ECCC.Weather.WeatherObservation` | Hourly obs: temperature, humidity, dew point, pressure, wind, precipitation |

## Upstream API

- **Base URL**: `https://api.weather.gc.ca/collections`
- **Collections**: `swob-stations` (metadata), `swob-realtime` (observations)
- **Auth**: None (open data, Open Government Licence - Canada)
- **Rate limit**: Fair use — the bridge polls every 15 minutes by default
- **Coverage**: ~963 stations across Canada
- **Protocol**: OGC API - Features with GeoJSON output

## Source Files

| File | Description |
|---|---|
| [xreg/environment_canada.xreg.json](xreg/environment_canada.xreg.json) | xRegistry manifest (authoritative contract) |
| [environment_canada/environment_canada.py](environment_canada/environment_canada.py) | Runtime bridge |
| [environment_canada_producer/](environment_canada_producer/) | Generated producer (xrcg 0.10.1) |
| [tests/](tests/) | Unit tests |
| [Dockerfile](Dockerfile) | Container image |
| [CONTAINER.md](CONTAINER.md) | Deployment contract |
| [EVENTS.md](EVENTS.md) | Event catalog |
