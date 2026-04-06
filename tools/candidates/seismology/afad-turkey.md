# AFAD — Disaster and Emergency Management Authority (Turkey)

## Source Identity

| Field            | Value |
|------------------|-------|
| **Full Name**    | AFAD Earthquake Department / Deprem Dairesi Başkanlığı |
| **Operator**     | T.C. İçişleri Bakanlığı AFAD (Republic of Turkey Ministry of Interior) |
| **URL**          | https://deprem.afad.gov.tr/ |
| **API Base**     | `https://deprem.afad.gov.tr/apiv2/event/filter` |
| **Coverage**     | Turkey and surrounding region |
| **Update Freq.** | Near-real-time; automatic locations within minutes |

## What It Does

AFAD operates Turkey's national seismic network and earthquake monitoring system. Turkey sits on the Anatolian Plate, squeezed between the Eurasian and Arabian plates — one of the most seismically active and hazardous regions on Earth. The 2023 Kahramanmaraş earthquake sequence (M7.8 + M7.5) underscored exactly why this data matters.

The API provides a JSON endpoint for querying the earthquake catalog by date range, magnitude, and other parameters. The response is a flat JSON array with detailed event metadata including province, district, and neighborhood-level location information — granularity you won't find in global catalogs.

## Endpoints Verified

| Endpoint | Status | Notes |
|----------|--------|-------|
| `/apiv2/event/filter?start=2026-04-05&end=2026-04-06&limit=5` | ✅ 200 | JSON array |
| `/apiv2/event/filter?limit=2&orderby=timedesc` | ❌ 500 | Some parameter combos fail |

### Sample JSON Response (trimmed)

```json
[
  {
    "rms": "0.19",
    "eventID": "712404",
    "location": "Doğanşehir (Malatya)",
    "latitude": "38.05306",
    "longitude": "37.66694",
    "depth": "7.39",
    "type": "ML",
    "magnitude": "1.1",
    "country": "Türkiye",
    "province": "Malatya",
    "district": "Doğanşehir",
    "neighborhood": "Beğre",
    "date": "2026-04-05T00:25:47",
    "isEventUpdate": false,
    "lastUpdateDate": null
  }
]
```

## Authentication & Licensing

- **Auth**: None observed. Anonymous access to the filter API.
- **Rate Limits**: Unknown; the API returned 500 on some queries, suggesting possible instability.
- **License**: Turkish government open data. No explicit license on the API; likely public domain within Turkey's data policy.

## Integration Notes

The API is custom (not FDSN) with a proprietary JSON schema. All values are strings (even latitude, longitude, magnitude, depth) — needs type casting on ingest. Date format is ISO 8601 without timezone offset (presumably UTC or Turkey local time — needs verification).

The `isEventUpdate` and `lastUpdateDate` fields suggest the API supports update tracking, though the observed values were `false` and `null` respectively.

Query parameters require date range (`start`, `end`) and optionally `limit`, `minmag`, `maxmag`, `minlat`, `maxlat`, `minlon`, `maxlon`. The `orderby` parameter seems unreliable (500 errors).

The hierarchical location data (country → province → district → neighborhood) is uniquely detailed — useful for localized alerting or analysis.

Some API instability observed (500 errors on certain parameter combinations). Would need defensive coding.

## Feasibility Rating

| Dimension                    | Score | Notes |
|------------------------------|-------|-------|
| **API Maturity & Docs**      | 1     | Works but poorly documented; some endpoints return 500 |
| **Data Freshness**           | 2     | Near-real-time polling; no push |
| **Format / Schema Quality**  | 2     | JSON but all-string values; custom schema |
| **Auth / Access Simplicity** | 3     | Anonymous access |
| **Coverage Relevance**       | 2     | Turkey — major seismic zone but single-country |
| **Operational Reliability**  | 1     | Server errors observed; no SLA or status page |
| **Total**                    | **11 / 18** | |

## Verdict

Interesting data from one of the world's most seismically active countries. The neighborhood-level location detail is unique. However, the API is flaky (500 errors), poorly documented, and uses a custom schema with all-string values. Turkey's seismicity is already covered by EMSC and USGS global catalogs. Consider as a secondary candidate — worthwhile mainly if there's specific demand for Turkish earthquake data with local granularity. Lower priority than FDSN-compliant sources.
