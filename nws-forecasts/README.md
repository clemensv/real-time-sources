# NWS Forecast Zones

This bridge polls **NWS forecast-zone products** for Seattle/Puget Sound style use cases and emits them as CloudEvents into Kafka. It covers both:

- **Land forecast zones** from `api.weather.gov/zones/forecast/{zoneId}/forecast`
- **Marine forecast zones** from `tgftp.nws.noaa.gov/data/forecasts/marine/coastal/pz/{zone}.txt`

The identity model is deliberately zone-centric. Every event is keyed by `zone_id`, which works for both public land zones like `WAZ315` and marine zones like `PZZ135`.

## Event families

- **ForecastZone** - reference metadata for each configured forecast zone
- **LandZoneForecast** - current narrative forecast snapshot for one public land zone
- **MarineZoneForecast** - current marine bulletin snapshot for one marine zone

Reference data is emitted first at startup and refreshed periodically.

## Upstream channel review

| Family | Transport | Identity | Keep/Drop | Reason |
|---|---|---|---|---|
| Zone metadata | `GET /zones/forecast/{zoneId}` | `zone_id` | **Keep** | Stable reference data for both land and marine forecasts. |
| Land zone forecasts | `GET /zones/forecast/{zoneId}/forecast` | `zone_id` | **Keep** | Stable land-forecast product keyed by forecast zone. |
| Marine coastal bulletins | `GET /data/forecasts/marine/coastal/pz/{zone}.txt` | `zone_id` | **Keep** | Reliable marine forecast transport for Puget Sound zones. |
| Forecast zone collection | `GET /zones/forecast` | collection page | Drop | Discovery endpoint only; per-zone reference events carry the durable entity model. |
| Gridpoint forecasts | `GET /gridpoints/{wfo}/{x},{y}/forecast` | `wfo/x/y` | Drop | Different identity model than zones; better handled as a separate source if needed. |
| Gridpoint hourly forecasts | `GET /gridpoints/{wfo}/{x},{y}/forecast/hourly` | `wfo/x/y` | Drop | Different identity model and cadence than this zone-centric source. |
| Forecast grid data | `GET /gridpoints/{wfo}/{x},{y}` | `wfo/x/y` | Drop | Raw grid dataset, not the narrative zone forecast product this bridge models. |
| Alerts and observations | existing NWS endpoints | varies | Drop | Already covered by `noaa-nws` and `nws-alerts`. |

## Default scope

The container defaults to a Puget Sound-friendly zone set:

- Land: `WAZ312`, `WAZ315`, `WAZ316`, `WAZ317`
- Marine: `PZZ130`, `PZZ131`, `PZZ132`, `PZZ133`, `PZZ134`, `PZZ135`

Override with `NWS_FORECAST_ZONES`.

## Running locally

```powershell
$env:CONNECTION_STRING="BootstrapServer=localhost:9092;EntityPath=nws-forecasts"
$env:KAFKA_ENABLE_TLS="false"
python -m nws_forecasts
```

Or with explicit Kafka settings:

```powershell
$env:KAFKA_BOOTSTRAP_SERVERS="localhost:9092"
$env:KAFKA_TOPIC="nws-forecasts"
$env:KAFKA_ENABLE_TLS="false"
python -m nws_forecasts
```

## Files

- `xreg/nws_forecasts.xreg.json` - authoritative contract
- `nws_forecasts/nws_forecasts.py` - runtime bridge
- `nws_forecasts_producer/` - generated producer code
- `tests/` - unit and live API tests
