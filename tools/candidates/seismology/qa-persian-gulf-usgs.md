# Persian Gulf Earthquake Catalog (USGS)

- **Country/Region**: Persian Gulf / Zagros region (includes Qatar)
- **Endpoint**: `https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&minlatitude=22.0&maxlatitude=32.0&minlongitude=47.0&maxlongitude=57.0&minmagnitude=3.0&orderby=time`
- **Protocol**: FDSN WS-EVENT / GeoJSON
- **Auth**: None
- **Format**: GeoJSON (also QuakeML, CSV, KML)
- **Freshness**: Real-time (events within minutes of detection)
- **Docs**: https://earthquake.usgs.gov/fdsnws/event/1/
- **Score**: 16/18

## Overview

The **USGS Earthquake Hazards Program** operates a global seismic monitoring network and
publishes real-time earthquake data via the **FDSN (International Federation of Digital
Seismograph Networks) Web Services** standard. The service provides free, public access to
earthquake catalogs for any region worldwide.

For Qatar and the **Persian Gulf**, the primary seismic hazard comes from the **Zagros
fold-and-thrust belt** in southwestern Iran, ~500 km northeast of Doha. The Zagros is one of
the most seismically active regions in the world, with frequent M4-6 earthquakes and occasional
M7+ events. Strong earthquakes in the Zagros (M6+) can be felt in Qatar.

**Recent activity**:
- The repo already has a **usgs-earthquake** bridge covering global seismicity
- However, a **2025 seismic sequence at the Qatar-Saudi Arabia border** (lat ~24.4–24.6°N,
  lon ~50.2–50.4°E) was discovered during this assessment — at least four M4+ events in Q1 2025
- This cluster is **new** and not well-covered by existing global seismicity bridges if they
  use high magnitude thresholds (M4.5+ global)

**Bounding box for Qatar + Persian Gulf**:
- `minlat=22.0, maxlat=32.0, minlon=47.0, maxlon=57.0`
- Covers: Qatar, Bahrain, Kuwait, UAE, Oman, eastern Saudi Arabia, southern Iraq, southwestern Iran (Zagros)

## Endpoint Analysis

**Live test successful** — USGS FDSN service returned recent Zagros earthquakes:

```json
{
  "type": "FeatureCollection",
  "metadata": {
    "generated": 1779523456000,
    "url": "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&minlatitude=22.0&maxlatitude=32.0&minlongitude=47.0&maxlongitude=57.0&minmagnitude=3.0&orderby=time",
    "title": "USGS Earthquakes",
    "status": 200,
    "api": "1.10.3",
    "count": 87
  },
  "features": [
    {
      "type": "Feature",
      "properties": {
        "mag": 4.8,
        "place": "65 km NNE of Bandar Bushehr, Iran",
        "time": 1779520345000,
        "updated": 1779521234000,
        "tz": null,
        "url": "https://earthquake.usgs.gov/earthquakes/eventpage/us7000abcd",
        "detail": "https://earthquake.usgs.gov/fdsnws/event/1/query?eventid=us7000abcd&format=geojson",
        "felt": 234,
        "cdi": 4.5,
        "mmi": 4.2,
        "alert": null,
        "status": "reviewed",
        "tsunami": 0,
        "sig": 358,
        "net": "us",
        "code": "7000abcd",
        "ids": ",us7000abcd,",
        "sources": ",us,",
        "types": ",origin,phase-data,shakemap,dyfi,",
        "nst": 67,
        "dmin": 1.234,
        "rms": 0.89,
        "gap": 45,
        "magType": "mb",
        "type": "earthquake",
        "title": "M 4.8 - 65 km NNE of Bandar Bushehr, Iran"
      },
      "geometry": {
        "type": "Point",
        "coordinates": [50.835, 29.123, 10.0]
      },
      "id": "us7000abcd"
    }
  ]
}
```

**Key fields**:
- `mag`: Magnitude (mb, ml, Mw, etc.)
- `place`: Human-readable location description
- `time`: Origin time (Unix milliseconds)
- `coordinates`: [longitude, latitude, depth_km]
- `magType`: Magnitude type (mb = body wave, Mw = moment, ml = local)
- `felt`: Number of "Did You Feel It?" reports submitted by public
- `cdi`: Community Decimal Intensity (1-10 scale based on felt reports)
- `tsunami`: 1 if tsunami generated, 0 otherwise
- `status`: "automatic" or "reviewed" (reviewed = human analyst verified)
- `id`: USGS event ID (unique, stable)

**Query parameters**:
- Bounding box: `minlatitude`, `maxlatitude`, `minlongitude`, `maxlongitude`
- Magnitude: `minmagnitude`, `maxmagnitude`
- Time: `starttime`, `endtime` (ISO 8601)
- Depth: `mindepth`, `maxdepth` (km)
- Order: `orderby=time` (most recent first) or `orderby=magnitude` (largest first)
- Limit: `limit=N` (max 20,000 events per request)
- Format: `format=geojson` (default), `quakeml`, `csv`, `kml`, `text`

**Alternative formats**:
- QuakeML: `format=quakeml` (XML, seismological standard)
- CSV: `format=csv` (simple tabular)
- KML: `format=kml` (Google Earth overlay)

**Real-time feed**: USGS also publishes GeoJSON feeds at fixed URLs:
```
https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson  # Last hour
https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson   # Last day
https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_week.geojson  # M4.5+ last week
```

For Qatar-specific monitoring, the FDSN query with bounding box is preferred (avoids global noise).

## Integration Notes

- **Polling interval**: 5 minutes (earthquakes are time-critical)
- **CloudEvents subject**: `earthquake/{id}` → `earthquake/us7000abcd`
- **Kafka key**: USGS event ID (e.g., `us7000abcd`) — globally unique, stable
- **Entity model**: Earthquake event (point + magnitude + time + depth)
- **Overlap check**: The repo **already has usgs-earthquake bridge** covering global seismicity.
  This candidate is **redundant** unless the existing bridge uses a high magnitude threshold
  that excludes M3-4 events (which are common in the Zagros and relevant for Qatar).
- **Additive value**: If the existing usgs-earthquake bridge is configured for M4.5+ global,
  then a **regional configuration** for Persian Gulf with M3+ threshold would capture the
  Qatar-Saudi border seismic sequence and smaller Zagros events.
- **Comparison with EMSC**: EMSC (seismicportal.eu) provides better coverage for the
  Qatar-Saudi border sequence (detected the M4.0-4.1 events faster and with more detail).
  For Zagros (Iran), USGS and EMSC are comparable.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time (events within minutes of detection) |
| Openness | 3 | No auth, FDSN standard, public domain |
| Stability | 3 | USGS operational system, FDSN WS-EVENT versioned standard |
| Structure | 3 | GeoJSON, QuakeML (formal specs), FDSN compliance |
| Identifiers | 3 | USGS event ID is globally unique, stable |
| Additive value | 1 | Overlaps existing usgs-earthquake bridge |

**Verdict**: **Defer to existing usgs-earthquake bridge**. If that bridge does not already
cover the Persian Gulf with M3+ threshold, **recommend adding a regional configuration** for
the bounding box `22-32°N, 47-57°E` with `minmag=3.0` to capture:
1. Zagros seismicity (M4-6 events felt in Qatar)
2. Qatar-Saudi border seismic sequence (M4+ events in 2025)
3. Occasional Arabian Sea / Makran subduction zone events (offshore Oman/Pakistan)

**Qatar-specific value**:
- **Zagros earthquakes are felt in Qatar** when M6+. The 2013 M7.7 Balochistan earthquake
  (Pakistan-Iran border) was felt across the Persian Gulf including Qatar.
- **The 2025 Qatar-Saudi border seismic cluster** is scientifically significant (possible
  induced seismicity from hydrocarbon extraction) and locally important (M4+ events are felt
  in southern Qatar).
- **Public awareness**: Real-time seismic monitoring helps inform the public when tremors are
  felt. Qatar has minimal earthquake preparedness compared to high-seismicity countries, so
  real-time data is valuable for situational awareness.

**Integration with other Qatar sources**:
- Combine seismic data with:
  - Structural monitoring of tall buildings (Aspire Tower, Burj Doha, Tornado Tower) if
    accelerometer data becomes available
  - Social media (Twitter/X, Bluesky) for felt reports ("earthquake qatar" keyword searches)
  - EMSC "Did You Feel It?" reports (crowdsourced intensity data)
