# IRCELINE (Belgian Interregional Environment Agency)

**Country/Region**: Belgium
**Publisher**: IRCELINE / IRCEL-CELINE (Interregionale Cel voor het Leefmilieu)
**API Endpoint**: `https://geo.irceline.be/sos/api/v1/`
**Documentation**: https://www.irceline.be/en/documentation/open-data
**Protocol**: REST (52°North SOS Timeseries API)
**Auth**: None
**Data Format**: JSON
**Update Frequency**: Hourly
**License**: Open data (Belgian government)

## What It Provides

IRCELINE operates Belgium's interregional air quality monitoring network, combining data from all three Belgian regions (Flanders/VMM, Wallonia/ISSeP/AwAC, and Brussels/Bruxelles Environnement). The SOS Timeseries API provides structured access to real-time and historical air quality measurements across ~120 stations. Pollutants include PM10, PM2.5, O₃, NO₂, SO₂, CO, benzene, and black carbon. Belgium's dense station network and small geographic size make this one of the highest-density monitoring networks in Europe.

## API Details

- **Base URL**: `https://geo.irceline.be/sos/api/v1/`
- **Key Endpoints** (52°North Timeseries API):
  - `GET /stations` — all monitoring stations as GeoJSON features with id, label, coordinates
  - `GET /stations/{id}` — station detail
  - `GET /timeseries` — list available timeseries (station × pollutant combos) with UoM
  - `GET /timeseries/{id}` — timeseries metadata
  - `GET /timeseries/{id}/getData` — actual measurement values with time range
  - `GET /phenomena` — list measured phenomena (pollutants)
  - `GET /categories` — data categories
- **Query Parameters**: `timespan` (ISO 8601), `limit`, `offset`, `expanded=true`
- **Response**: GeoJSON features; timeseries values as `{timestamp, value}` pairs
- **Sample Station**: `{"properties":{"id":1031,"label":"40AL02 - Beveren"},"geometry":{"coordinates":[4.234,51.304],"type":"Point"},"type":"Feature"}`

## Freshness Assessment

Data is updated hourly. Belgium's three regional networks feed data into IRCELINE's central platform continuously. The API reflects measurements from the current hour with a short delay (typically 1-2 hours). The same data feeds the BelAQI (Belgian Air Quality Index) displayed on irceline.be.

## Entity Model

- **Station** → id, label, coordinates (GeoJSON Point)
- **Timeseries** → links a Station to a Phenomenon (pollutant) with unit of measurement
- **Phenomenon** → pollutant type (PM10, PM2.5, O₃, NO₂, SO₂, CO, etc.)
- **Data** → timestamp + value pairs for a given timeseries

## Feasibility Rating

| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | Hourly data, responsive API |
| Openness | 3 | No auth, open government data |
| Stability | 3 | Federal agency; 52°North standard SOS platform (same as Defra AURN) |
| Structure | 3 | Clean JSON, standard Timeseries API pattern |
| Identifiers | 2 | Numeric IDs; labels combine station code + city name |
| Additive Value | 2 | Belgium-only; partially in EEA/OpenAQ but direct API gives more granularity |
| **Total** | **16/18** | |

## Notes

- Uses the identical 52°North SOS Timeseries API as UK Defra AURN — the same client code can talk to both.
- Station labels use a code-prefix format like `40AL02 - Beveren` where the code identifies the regional network and station number.
- IRCELINE also provides forecast data (BelAQI index) and interpolated maps, though these may require separate endpoints.
- Belgium's three-region structure means station codes may carry region-specific prefixes (40xx = Flanders VMM, 42xx = Brussels, 43xx = Wallonia).
- Already partially ingested by OpenAQ and EEA, but the direct SOS API offers timeseries-level granularity.
