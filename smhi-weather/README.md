# SMHI Weather Observation Bridge

This bridge fetches real-time meteorological observations from the [Swedish
Meteorological and Hydrological Institute (SMHI)](https://opendata.smhi.se/apidocs/metobs/)
and emits them as CloudEvents into Apache Kafka or Azure Event Hubs.

## Data Model

The bridge emits two event types into the `smhi-weather` topic, both keyed
by `{station_id}`:

| Event Type | Description |
|---|---|
| `SE.Gov.SMHI.Weather.Station` | Reference data for each active station (emitted at startup) |
| `SE.Gov.SMHI.Weather.WeatherObservation` | Hourly observations: temperature, wind gust, dew point, pressure, humidity, precipitation |

## Upstream API

- **Base URL**: `https://opendata-download-metobs.smhi.se/api/version/1.0`
- **Auth**: None (open data, CC BY 4.0)
- **Rate limit**: Fair use — the bridge polls every 15 minutes by default
- **Coverage**: ~232 SMHI core stations across Sweden
- **Parameters**: Air temperature (1), Wind gust (21), Dew point (39),
  Air pressure (9), Relative humidity (6), Precipitation last hour (7)

## Source Files

| File | Description |
|---|---|
| [xreg/smhi_weather.xreg.json](xreg/smhi_weather.xreg.json) | xRegistry manifest (authoritative contract) |
| [smhi_weather/smhi_weather.py](smhi_weather/smhi_weather.py) | Runtime bridge |
| [smhi_weather_producer/](smhi_weather_producer/) | Generated producer (xrcg 0.10.1) |
| [tests/](tests/) | Unit tests |
| [Dockerfile](Dockerfile) | Container image |
| [CONTAINER.md](CONTAINER.md) | Deployment contract |
| [EVENTS.md](EVENTS.md) | Event catalog |
