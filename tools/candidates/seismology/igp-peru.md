# IGP Peru — Instituto Geofísico del Perú

## Source Identity

| Field            | Value |
|------------------|-------|
| **Full Name**    | Instituto Geofísico del Perú (IGP) |
| **Operator**     | IGP, Peruvian Government |
| **URL**          | https://www.igp.gob.pe/ |
| **API Base**     | `https://ultimosismo.igp.gob.pe/api/ultimo-sismo/ajaxb/` |
| **Coverage**     | Peru and surrounding South American subduction zone |
| **Update Freq.** | Event-driven; new quakes within minutes |

## What It Does

Peru sits atop one of Earth's most active subduction zones — the Nazca Plate diving under South America. The country experiences frequent large earthquakes, including the devastating 1970 Ancash earthquake (M7.9) and 2007 Pisco earthquake (M8.0). IGP is Peru's official geophysical monitoring institute, operating the national seismic network.

The `ultimosismo` (latest earthquake) API provides JSON feeds of recent seismicity with location, magnitude, depth, and local reference descriptions.

## Endpoints Verified

| Endpoint | Status | Notes |
|----------|--------|-------|
| `/ajaxb/2026` | ✅ 200 | JSON array of earthquakes for year |
| `/ajaxb` | ❌ 404 | Year parameter appears required |
| Web portal | ✅ 200 | Full interactive map at ultimosismo.igp.gob.pe |

### Sample Response (trimmed)

```json
[
  {
    "codigo": "2026-0001",
    "fecha_local": "2026-01-01T00:00:00.000Z",
    "hora_local": "1970-01-01T05:20:25.000Z",
    "fecha_utc": "2026-01-01T00:00:00.000Z",
    "hora_utc": "1970-01-01T10:20:25.000Z",
    "latitud": "-15.26",
    "longitud": "-76",
    "magnitud": "4.4",
    "profundidad": 32,
    "referencia": "70 km al O de San Juan, Nasca - Ica",
    "reporte_acelerometrico_pdf": "https://www.igp.gob.pe/servicios/api-acelerometrica/ran/file/..."
  }
]
```

## Authentication & Licensing

- **Auth**: None. Anonymous access.
- **Rate Limits**: Not documented.
- **License**: Peruvian government public data. Attribution to IGP expected.

## Integration Notes

The JSON schema has some quirks. Date and time are in separate fields (`fecha_local` / `hora_local`), and the time field oddly has a `1970-01-01` date prefix — it's just the time component. Combining `fecha_utc` and `hora_utc` gives the actual event datetime. Coordinates are string values that need numeric parsing.

The `codigo` field (e.g., "2026-0001") provides a sequential event identifier. `profundidad` (depth) is numeric in km. `referencia` gives a Spanish-language locality description. The accelerometric report PDF link is a unique addition — actual strong-motion records.

The API appears to return all events for a given year, which could be a large response. Pagination or date-range filtering was not observed.

## Feasibility Rating

| Dimension                    | Score | Notes |
|------------------------------|-------|-------|
| **API Maturity & Docs**      | 2     | Working JSON; undocumented API |
| **Data Freshness**           | 2     | Events appear within hours; year-based endpoint |
| **Format / Schema Quality**  | 2     | JSON with date/time quirks; string coordinates |
| **Auth / Access Simplicity** | 3     | Anonymous, open |
| **Coverage Relevance**       | 3     | Major subduction zone; frequent large earthquakes |
| **Operational Reliability**  | 2     | Government institute; API stability unknown |
| **Total**                    | **14 / 18** | |

## Verdict

⚠️ **Maybe** — Peru's seismicity is globally significant and the JSON API works, but the data format is quirky (split date/time, string coordinates, year-based bulk endpoint). Most Peruvian events appear in USGS and EMSC with cleaner formats. The unique value is local detail (Spanish references, accelerometric PDFs). Worth building if South American subduction zone coverage is a priority, but not before the FDSN sources and BMKG.
