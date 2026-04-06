# TAHMO — Trans-African Hydro-Meteorological Observatory

- **Country/Region**: Pan-African (20+ countries, 600+ stations)
- **Endpoint**: `https://api.tahmo.org/services/measurements/v2/stations`
- **Protocol**: REST
- **Auth**: API key (academic/research registration)
- **Format**: JSON, CSV
- **Freshness**: Near real-time (5-minute intervals)
- **Docs**: https://tahmo.org/climate-data/
- **Score**: 12/18

## Overview

TAHMO is an ambitious project to install 20,000 automatic weather stations across
Africa — one every 30 km — to close the continent's weather observation gap. Currently
operating 600+ stations in 20+ countries, TAHMO provides high-frequency (5-minute)
meteorological data that far surpasses what most African national met services can offer.

Stations measure: temperature, humidity, precipitation, wind speed/direction, solar
radiation, barometric pressure, and soil moisture. This makes TAHMO one of the most
valuable weather data sources for Africa.

## Endpoint Analysis

**Probed** — the API root at `https://api.tahmo.org` returned a 500 error, suggesting
the server exists but the root path is not a valid endpoint.

Documented API structure (from TAHMO data access documentation):
```
GET /services/measurements/v2/stations
  → List all station metadata
GET /services/measurements/v2/stations/{stationId}/measurements
  → Get measurements for a station
GET /services/measurements/v2/stations/{stationId}/measurements/{variable}
  → Get specific variable
```

Variables available:
| Variable | Description | Unit |
|----------|-------------|------|
| te | Temperature | °C |
| rh | Relative humidity | % |
| pr | Precipitation | mm |
| ws | Wind speed | m/s |
| wd | Wind direction | degrees |
| ra | Solar radiation | W/m² |
| bp | Barometric pressure | hPa |
| sm | Soil moisture | % |

Countries with TAHMO stations (documented):
Kenya, Tanzania, Uganda, Rwanda, Burkina Faso, Ghana, Nigeria, Senegal, Mozambique,
Zambia, Malawi, Niger, DRC, Cameroon, Togo, Benin, Ethiopia, and more.

## Integration Notes

- **Academic access**: TAHMO data is available to researchers and academic institutions.
  Commercial access requires a separate agreement. Register at
  https://tahmo.org/climate-data/ to request access.
- **High-frequency gold mine**: 5-minute data across 600+ African stations is unprecedented.
  This is genuinely valuable data that doesn't exist elsewhere at this resolution.
- **Quality control**: TAHMO applies automated QC algorithms. Flag data with QC issues
  in CloudEvents metadata.
- **Station density**: Highest density in East Africa (Kenya, Tanzania, Uganda) and
  West Africa (Ghana, Burkina Faso, Nigeria).
- **Partnership potential**: TAHMO is interested in data distribution partnerships.
  A CloudEvents bridge could be mutually beneficial.
- **Data gaps**: Stations occasionally go offline due to vandalism, power issues, or
  connectivity problems — common challenges for ground stations in Africa.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 5-minute intervals |
| Openness | 1 | Registration required, academic access |
| Stability | 2 | Growing network but individual stations can fail |
| Structure | 2 | JSON/CSV API (limited public documentation) |
| Identifiers | 2 | TAHMO station IDs |
| Richness | 2 | Multi-variable meteorological data + soil moisture |
