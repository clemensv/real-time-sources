# UK Met Office Weather DataHub

**Country/Region**: United Kingdom
**Publisher**: Met Office (UK national meteorological service)
**API Endpoint**: `https://data.hub.metoffice.gov.uk/`
**Documentation**: https://www.metoffice.gov.uk/services/data/met-office-weather-datahub
**Protocol**: REST (GeoJSON for site-specific, GRIB2 for atmospheric models, PNG for map images)
**Auth**: API Key (free tier available via registration on DataHub)
**Data Format**: GeoJSON, GRIB2, PNG
**Update Frequency**: Hourly (spot data), per model run (atmospheric models ~6h), every few minutes (warnings)
**License**: Open Government Licence v3 (for Public Task data)

## What It Provides

The Met Office Weather DataHub is the successor to the legacy DataPoint API. It provides:

- **Atmospheric models**: Global deterministic (10 km), UK deterministic (2 km standard and lat/lon), MOGREPS-G (global ensemble), MOGREPS-UK (UK ensemble) — all in GRIB2.
- **Site-specific forecasts**: Global hourly, 3-hourly, and daily spot data via GeoJSON for any lat/lon coordinate.
- **Blended probabilistic forecasts**: BETA product combining NWP model outputs for probabilistic site-specific forecasts.
- **Map images**: PNG overlays for temperature, precipitation rate, total cloud cover, and MSLP — by time step and model run.
- **Warnings**: UK national weather warnings (severe weather alerts).

## API Details

The DataHub uses an IBM API Connect gateway. Users register at `https://datahub.metoffice.gov.uk/`, obtain an API key, and make REST calls. Site-specific endpoints accept latitude/longitude and return GeoJSON with hourly/3-hourly/daily forecasts.

Example endpoints:
- Global hourly spot data: `/sitespecific/v0/point/hourly?latitude={lat}&longitude={lon}`
- Atmospheric model data: `/atmospheric/v0/{model}/{run}/{step}`

Rate limits apply depending on the tier (free vs. commercial).

## Freshness Assessment

- Site-specific data updates hourly from the latest model run.
- Atmospheric model data is available within ~2–3 hours of model run time (00Z, 06Z, 12Z, 18Z).
- The UK 2 km model runs every hour, making this one of the freshest NWP sources for the UK.

## Entity Model

- **Location**: Arbitrary lat/lon point (site-specific) or grid (models)
- **Forecast parameters**: Temperature, feels-like temperature, wind speed/direction/gust, visibility, humidity, UV index, precipitation probability, weather type code, pressure
- **Time series**: Hourly, 3-hourly, or daily steps out to 5–7 days

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Hourly site-specific updates, frequent model runs |
| Openness | 2 | Free tier with registration, but rate-limited; some data Public Task (OGL) |
| Stability | 3 | UK national met service, long-term commitment to open data |
| Structure | 3 | Clean GeoJSON for spot data, well-structured GRIB2 for models |
| Identifiers | 2 | Lat/lon based (no fixed station IDs for spot data), model runs by datetime |
| Additive Value | 3 | High-resolution UK 2km model unique, global coverage too |
| **Total** | **16/18** | |

## Notes

- The legacy DataPoint API is being phased out in favor of the DataHub.
- The free tier has generous limits for non-commercial use.
- GeoJSON site-specific endpoints are very easy to integrate — no GRIB decoding needed for basic use cases.
- The UK 2 km model (UKV) is exceptionally high-resolution for real-time weather data.
- Weather warnings are available as a separate feed.
