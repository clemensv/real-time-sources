# India CPCB Air Quality via data.gov.in API

**Country/Region**: India
**Publisher**: Central Pollution Control Board (CPCB) via data.gov.in Open Data Platform
**API Endpoint**: `https://api.data.gov.in/resource/3b01bcb8-0b14-4abf-b6f2-c1bfd384ba69`
**Documentation**: https://data.gov.in/resource/real-time-air-quality-index-various-locations
**Protocol**: REST (JSON)
**Auth**: API Key (free registration at data.gov.in)
**Data Format**: JSON
**Update Frequency**: Hourly (aligned with CAAQMS station reporting)
**License**: India Government Open Data License (GODL)

## What It Provides

This is the official REST API for India's real-time air quality data — and it's one of the most important air quality monitoring networks on the planet. With 400+ Continuous Ambient Air Quality Monitoring Stations (CAAQMS) across India, this endpoint delivers live pollutant readings from the world's most polluted cities: Delhi, Mumbai, Kolkata, Lucknow, Kanpur, and hundreds more.

The data includes per-station, per-pollutant records with:
- PM2.5, PM10, SO₂, NO₂, CO, O₃, NH₃, benzene, toluene, xylene
- Min, max, and average values for each pollutant per reporting period
- Station location (latitude/longitude), city, state, and station name
- Last update timestamp

This is fundamentally different from the existing `india-cpcb.md` candidate, which documents the CPCB web dashboard (no public API). This data.gov.in endpoint is a proper, documented REST API with stable structure.

## API Details

The endpoint follows data.gov.in's standard resource API pattern:

```
GET https://api.data.gov.in/resource/3b01bcb8-0b14-4abf-b6f2-c1bfd384ba69
    ?api-key={YOUR_KEY}
    &format=json
    &limit=100
    &offset=0
    &filters[city]=Delhi
```

### Probed Response (live, April 2026)

```json
{
  "status": "ok",
  "total": 3434,
  "count": 5,
  "records": [
    {
      "country": "India",
      "state": "Andhra_Pradesh",
      "city": "Amaravati",
      "station": "Secretariat, Amaravati - APPCB",
      "last_update": "07-04-2026 02:00:00",
      "latitude": "16.5150833",
      "longitude": "80.5181667",
      "pollutant_id": "SO2",
      "min_value": "6",
      "max_value": "11",
      "avg_value": "8"
    }
  ]
}
```

Key observations:
- **3,434 total records** at time of probe — this is the full real-time dataset across all stations and pollutants
- Data updated within the last hour (confirmed fresh timestamp)
- Standard pagination via `limit` and `offset`
- Filterable by `city`, `state`, `station`, `pollutant_id`
- The `last_update` field is in IST (Indian Standard Time)

### Supported Filters

| Parameter | Example | Notes |
|-----------|---------|-------|
| `filters[state]` | `Delhi` | State/UT name |
| `filters[city]` | `Delhi` | City name |
| `filters[pollutant_id]` | `PM2.5` | Pollutant identifier |
| `limit` | `1000` | Max records per page |
| `offset` | `0` | Pagination offset |

## Freshness Assessment

The dataset metadata shows `updated_date: 2026-04-06T21:06:48Z` — confirming continuous updates. Station data refreshes hourly, aligned with CAAQMS reporting cycles. During Delhi's winter smog season (October–February), this data becomes globally critical for health advisories.

## Entity Model

- **Station**: Identified by name string (e.g., "ITO, Delhi - DPCC"), with lat/lon coordinates
- **Pollutant**: One record per pollutant per station per reporting period
- **State/City**: Hierarchical geography (country → state → city → station)
- No WMO or standardized station IDs — station names serve as identifiers

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Hourly updates, confirmed live data |
| Openness | 2 | Free API key required (instant registration); GODL license |
| Stability | 3 | data.gov.in is the national open data platform; API has been stable since 2016 |
| Structure | 2 | Clean JSON but flat per-pollutant rows; station IDs are name-strings, not codes |
| Identifiers | 1 | No standardized station codes; string-based matching needed |
| Additive Value | 3 | Only real-time API for world's most polluted major cities; Delhi AQI is globally watched |
| **Total** | **14/18** | |

## Integration Notes

- Polling at 1-hour intervals would capture all station updates
- Each poll returns ~3,400 rows — manageable payload
- Deduplication key: `station` + `pollutant_id` + `last_update`
- The data.gov.in API is well-established with libraries in Python, JavaScript
- Consider enriching with station metadata (no altitude or station type in the real-time feed)
- The API key `579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b` is the public demo key — works but rate-limited; register for a dedicated key
- CloudEvents mapping: one event per station-pollutant update, or aggregate per-station with all pollutants

## Relationship to Existing india-cpcb.md

The existing `india-cpcb.md` documents the CPCB web dashboard at `app.cpcbccr.com`, which has no public API. This candidate covers the same underlying data but through India's official open data API at data.gov.in — a proper, documented, stable REST endpoint. This is the recommended integration path.
