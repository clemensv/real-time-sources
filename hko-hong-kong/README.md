# HKO Hong Kong Weather Observation Bridge

This bridge fetches real-time weather observations from the
[Hong Kong Observatory (HKO)](https://www.hko.gov.hk/en/abouthko/opendata_intro.htm)
and emits them as CloudEvents into Apache Kafka or Azure Event Hubs.

## Data Model

The bridge emits two event types into the `hko-hong-kong` topic, keyed by
`{place_id}` (a URL-safe slug of the English place name):

| Event Type | Description |
|---|---|
| `HK.Gov.HKO.Weather.Station` | Reference data for each place (emitted at startup) |
| `HK.Gov.HKO.Weather.WeatherObservation` | Current observations: temperature, rainfall, humidity, UV index |

## Upstream API

- **Base URL**: `https://data.weather.gov.hk/weatherAPI/opendata/weather.php`
- **Auth**: None (fully open, HK Open Government Data License)
- **Rate limit**: Fair use — the bridge polls every 10 minutes by default
- **Coverage**: 27 temperature stations, 18 rainfall districts, 1 humidity station (HKO HQ), 1 UV station (King's Park)
- **Endpoint**: `?dataType=rhrread&lang=en` — Regional Weather in Hong Kong

## Source Files

| File | Description |
|---|---|
| [xreg/hko_hong_kong.xreg.json](xreg/hko_hong_kong.xreg.json) | xRegistry manifest |
| [hko_hong_kong/hko_hong_kong.py](hko_hong_kong/hko_hong_kong.py) | Runtime bridge |
| [hko_hong_kong_producer/](hko_hong_kong_producer/) | Generated producer (xrcg 0.10.1) |
| [tests/](tests/) | Unit tests |
| [Dockerfile](Dockerfile) | Container image |
| [CONTAINER.md](CONTAINER.md) | Deployment contract |
| [EVENTS.md](EVENTS.md) | Event catalog |
