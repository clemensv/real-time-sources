# CSN Chile — Centro Sismológico Nacional (via api.xor.cl)

**Country/Region**: Chile (national)
**Publisher**: Centro Sismológico Nacional, Universidad de Chile
**API Endpoint**: `https://api.xor.cl/sismo/recent`
**Documentation**: https://api.xor.cl/ (community API wrapping sismologia.cl)
**Protocol**: REST (JSON)
**Auth**: None
**Data Format**: JSON
**Update Frequency**: Near-real-time (minutes)
**License**: Publicly accessible (university/government data)

## What It Provides

Chile is one of the most seismically active countries on Earth — home to the world's largest recorded earthquake (1960 Valdivia, M9.5) and a subduction zone running the full 4,300 km length of the country. CSN operates Chile's national seismograph network and publishes earthquake data through sismologia.cl. The api.xor.cl community API wraps CSN data into clean JSON.

Data per event:
- **Event ID** and URL to CSN detail page
- **Date/time** in both local (Chile) and UTC
- **Latitude / Longitude**
- **Depth** (km)
- **Magnitude** with unit (typically Mlv — local magnitude)
- **Geo-reference** (human-readable location, in Spanish)
- **Map image URL** for each event

## API Details

Simple GET request:

```
GET https://api.xor.cl/sismo/recent
```

Response (verified live 2026-04-06):

```json
{
  "status_code": 0,
  "status_description": "Información obtenida satisfactoriamente",
  "events": [
    {
      "id": "355844",
      "url": "http://sismologia.cl/sismicidad/informes/2026/04/355844.html",
      "map_url": "http://sismologia.cl/sismicidad/informes/2026/04/map_img/355844.jpeg",
      "local_date": "2026-04-06 17:17:17",
      "utc_date": "2026-04-06 21:17:17",
      "latitude": -24.06,
      "longitude": -67.44,
      "depth": 229,
      "magnitude": { "value": 3.3, "measure_unit": "Mlv" },
      "geo_reference": "69 km al SE de Socaire"
    }
  ]
}
```

Returns ~15 most recent events. Chile typically records 20–40+ earthquakes per day (most M2–3), making this a high-throughput source.

### CSN Direct Website (sismologia.cl)

CSN also publishes HTML catalogs organized by date:

```
https://www.sismologia.cl/sismicidad/catalogo/2026/04/20260405.html
```

These contain tabular data with event links, coordinates, depth, and magnitude. Scraping is possible but the api.xor.cl wrapper is far cleaner.

### FDSN Endpoint — NOT WORKING

The FDSN survey (see fdsn-network-survey.md) tested `evtdb.csn.uchile.cl/fdsnws/event/1/` — returned 404. CSN's FDSN node appears defunct.

## Freshness Assessment

The api.xor.cl endpoint returned events from the current day with timestamps within hours of the query. Chile's high seismicity rate means fresh data is always available. The community API appears to poll CSN data at frequent intervals (likely minutes).

## Entity Model

- **Event**: id, url, map_url, local_date, utc_date, latitude, longitude, depth, magnitude (value + measure_unit), geo_reference
- **Magnitude units**: Mlv (local), Mw (moment magnitude for larger events)
- **Coordinates**: Decimal degrees (WGS84)
- **Depth**: km

## Integration Notes

- The api.xor.cl is a community/third-party API, not official CSN infrastructure. This introduces a dependency on a single developer's maintained service. However, the underlying data is from CSN.
- Chile's seismicity is exceptional — the country sits atop the Nazca-South American plate boundary, one of the most active subduction zones on the planet. Events range from shallow coastal (10–30 km) to deep intraslab (100–300 km) in the Andes.
- Geo-reference strings are in Spanish ("km al SE de Socaire").
- CloudEvents mapping: each event becomes one CloudEvent with `subject` as the event ID and `source` as `//csn.uchile.cl/sismo`.
- Poll interval recommendation: 2–5 minutes.
- Deduplication: use `id` field (sequential integer from CSN).

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Near-real-time, minutes latency |
| Openness | 3 | No auth, no rate limits observed |
| Stability | 2 | Community API — not official; underlying CSN data is stable |
| Structure | 3 | Clean JSON with consistent field naming |
| Identifiers | 2 | Sequential IDs, Spanish geo-references |
| Additive Value | 3 | Only clean API for Chile's seismicity; world's most seismically active country |
| **Total** | **16/18** | |

## Verdict

✅ **Build** — Chile's seismic data is scientifically invaluable and this API makes it trivially accessible. The community API wrapper risk is mitigated by the fact that the underlying CSN data format is stable and HTML scraping of sismologia.cl is a viable fallback. Chile detects 20–40+ earthquakes daily, making this one of the highest-throughput seismology sources globally. A generic FDSN adapter won't work here (FDSN node is dead), so this needs a custom adapter — but the JSON format is simple.
