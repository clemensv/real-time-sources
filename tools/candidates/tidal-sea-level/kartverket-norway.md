# Kartverket — Norway Tide and Water Level API

**Country/Region**: Norway (entire coastline)
**Publisher**: Kartverket (Norwegian Mapping Authority), Hydrographic Service
**API Endpoint**: `https://vannstand.kartverket.no/tideapi.php`
**Documentation**: https://vannstand.kartverket.no/tideapi_en.html
**Protocol**: REST API (XML responses by default; JSON available for some endpoints)
**Auth**: None — open for everybody, free of charge
**Data Format**: XML, JSON
**Update Frequency**: Real-time (observations), 5-day forecasts
**License**: CC BY 4.0

## What It Provides

Kartverket operates Norway's authoritative tide gauge network, providing observed water levels, tidal predictions, and storm surge forecasts for the entire Norwegian coastline. The service "Se havnivå" covers:

- **Observed water levels** from permanent tide gauges
- **Tidal predictions** (astronomical tide) for any point along the coast
- **Water level forecasts** (up to 5 days, including meteorological effects)
- **Datum references**: multiple vertical datums including chart datum, NN2000
- **Land uplift data** — postglacial rebound corrections

Norway's coastline is one of the longest in the world (~100,000 km including fjords and islands), making this dataset uniquely valuable for Nordic maritime operations.

## API Details

The API uses query parameters on a single PHP endpoint:

```
https://vannstand.kartverket.no/tideapi.php?tide_request=locationdata
  &lat=59.91&lon=10.74
  &fromtime=2025-01-01T00:00:00
  &totime=2025-01-02T00:00:00
  &datatype=obs
  &refcode=cd
  &place=Oslo
  &lang=en
```

Key parameters:
- `tide_request`: `locationlist` (station list), `locationdata` (observations/predictions), `locationlevel` (datum levels)
- `datatype`: `obs` (observations), `pre` (predictions), `all` (both), `tab` (tide tables)
- `refcode`: datum reference — `cd` (chart datum), `nn2000`, `msl`, etc.

Rate limit: ~20 requests/second shared across all users.

The API specification PDF is regularly updated (latest revision June 2025).

## Freshness Assessment

Excellent. Observations are real-time from permanent tide gauges. Forecasts extend 5 days ahead. Historical observations available back to the late 1980s through the API; older data via Copernicus Marine Service.

## Entity Model

- **Location**: name, latitude, longitude, type (permanent/temporary)
- **Observation**: timestamp, water level (cm), datum reference
- **Prediction**: timestamp, predicted water level, high/low tide indicators
- **Datum Level**: reference code, offset values between datums

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time observations + 5-day forecasts |
| Openness | 3 | No auth, no registration, CC BY 4.0 |
| Stability | 3 | Government agency, legally mandated maritime safety |
| Structure | 2 | REST API but XML-primary; query structure is somewhat idiosyncratic |
| Identifiers | 2 | Station names + lat/lon; links to PSMSL and IOC SLSMF |
| Additive Value | 3 | Unique fjord coverage; 100,000 km coastline; land uplift corrections |
| **Total** | **16/18** | |

## Notes

- The API is mature and well-documented with a formal communication protocol specification.
- Norway's fjord geography means tidal patterns vary dramatically over short distances — this granular data isn't available from global aggregators.
- The widget embeddable on third-party sites suggests Kartverket is serious about data reuse.
- Older data (pre-1990) requires querying Copernicus Marine Service instead.
- Complementary to IOC SLSMF — Norwegian stations report there too, but Kartverket adds datum-referenced precision and forecast data.
