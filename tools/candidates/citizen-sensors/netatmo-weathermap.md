# Netatmo Weathermap

**Country/Region**: Global (densest in Europe)
**Publisher**: Netatmo (Legrand Group)
**API Endpoint**: `https://api.netatmo.com/api/getpublicdata`
**Documentation**: https://dev.netatmo.com/apidocumentation/weather#getpublicdata
**Protocol**: REST (JSON)
**Auth**: OAuth2 (free developer account required)
**Data Format**: JSON
**Update Frequency**: ~5-10 minutes (station reporting interval)
**License**: Netatmo API Terms of Use (free for non-commercial; commercial requires agreement)

## What It Provides

Netatmo operates one of the world's largest citizen weather station networks, with hundreds of thousands of personal weather stations deployed in homes worldwide. Each station measures temperature, humidity, barometric pressure, CO2 (indoor), and noise level. Many owners add rain gauges and wind modules. The `getpublicdata` API endpoint returns anonymized readings from all stations in a geographic bounding box.

The density in European cities is remarkable — in Paris or London, you can see temperature gradients across neighborhoods. This is urban microclimate monitoring at a resolution official weather networks can't match.

## API Details

- **Public data**: `POST /api/getpublicdata` — body: `lat_ne`, `lon_ne`, `lat_sw`, `lon_sw` (bounding box), `required_data` (filter by measurement type), `filter` (boolean — filter out outliers)
- **Response**: Array of station objects, each with `_id`, `place` (location), `measures` (keyed by module MAC address), `modules`
- **Measurements**: Temperature (°C), humidity (%), pressure (mbar), rain (mm), wind (km/h, direction), noise (dB)
- **Auth**: OAuth2 bearer token — requires registering an app at dev.netatmo.com (free)
- **Rate limit**: 500 requests per hour per token
- **No station identification**: Stations are anonymized; only approximate location and readings are exposed

## Freshness Assessment

Stations report every 5-10 minutes. The public data endpoint returns the latest reading for each station in the bounding box. The `time_server` field indicates when the Netatmo cloud last received data from each station.

API confirmed accessible (developer portal returns 200). Endpoint requires OAuth2 token, which is free to obtain via the Netatmo developer portal.

## Entity Model

- **Station**: `_id` (anonymized), `place` (approximate location with city/country), `mark` (position for map display)
- **Module**: MAC address (anonymized), measurement type
- **Measurement**: Type (temperature, humidity, etc.), value, timestamp
- **Bounding box**: Geographic query area

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 5-10 minute reporting cadence |
| Openness | 2 | Free OAuth2 required; anonymized stations; non-commercial terms |
| Stability | 3 | Commercial product backed by Legrand Group; API stable for years |
| Structure | 2 | JSON but nested module structure is complex; measurement keys are module MAC addresses |
| Identifiers | 1 | Stations anonymized; no stable public identifiers |
| Additive Value | 2 | Unmatched urban weather station density in Europe |
| **Total** | **13/18** | |

## Notes

- Developer portal confirmed accessible; OAuth2 registration required but free.
- Station anonymization limits time-series analysis — you can't reliably track one station over time via the public API.
- The urban density is the key differentiator: hundreds of stations per city in European capitals.
- Rain and wind modules are optional add-ons — not all stations report these.
- Indoor CO2 and noise data are unique among weather APIs.
- Pairs with Sensor.Community (air quality overlay on weather data), OpenWeatherMap (which ingests some Netatmo data), and CWOP/MADIS.
