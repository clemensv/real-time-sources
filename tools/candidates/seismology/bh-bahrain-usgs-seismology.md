# Gulf Region Seismology - USGS Coverage for Bahrain

- **Country/Region**: Bahrain and Arabian Gulf region
- **Endpoint**: `https://earthquake.usgs.gov/fdsnws/event/1/query` (USGS FDSN Web Service)
- **Protocol**: REST / HTTP GET
- **Auth**: None
- **Format**: GeoJSON, QuakeML, CSV, KML, XML
- **Freshness**: Real-time (events published within minutes of detection)
- **Docs**: https://earthquake.usgs.gov/fdsnws/event/1/
- **Score**: 8/18 (global source, but Bahrain-specific relevance is minimal)

## Overview

The United States Geological Survey (USGS) operates a global earthquake monitoring
network that detects and reports seismic events worldwide, including the Arabian Gulf
region. The USGS Earthquake Hazards Program publishes data via the FDSN (International
Federation of Digital Seismograph Networks) web service standard, providing real-time
access to earthquake catalogs in multiple formats.

**Bahrain seismic context:**
Bahrain is located in a region of **very low seismic activity**. The Arabian Gulf is
tectonically stable compared to the nearby Zagros Mountains (Iran) and Gulf of Oman,
where the Arabian and Eurasian plates collide. Bahrain itself experiences:
- **Minimal local seismicity**: Few if any earthquakes originate directly beneath
  Bahrain island
- **Distant tremors felt occasionally**: Earthquakes in Iran (Zagros fault zone) or
  southern Iran can be felt in Bahrain if magnitude is large (M5.5+) and distance is
  within 500-1000 km
- **No active faults on Bahrain**: The island sits on the stable Arabian Plate interior
- **Historical record**: Very few damaging earthquakes recorded in Bahrain's history

**Recent seismicity check (May 2026):**
A query for earthquakes in the Bahrain bounding box (25.5°N-26.5°N, 50.0°E-51.0°E)
from May 1-23, 2026 returned **zero events**. This is typical for Bahrain — local
seismicity is negligible.

However, earthquakes in the broader Gulf region (especially Iran) are relatively
common and can have cross-border impacts:
- **Felt reports in Bahrain** when large Iranian earthquakes occur (M6+)
- **Infrastructure monitoring**: Bahrain's energy sector (oil/gas), desalination plants,
  and critical infrastructure may track regional seismicity for risk assessment
- **Public awareness**: Gulf residents are interested in regional earthquake activity
  due to proximity to Iran's active seismic zones

## Endpoint Analysis

**USGS FDSN Web Service tested:**
```
GET https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&minlatitude=25.5&maxlatitude=26.5&minlongitude=50.0&maxlongitude=51.0&starttime=2026-05-01&endtime=2026-05-23
```

**Result (May 2026):**
```json
{
  "type": "FeatureCollection",
  "metadata": {
    "generated": 1779522204000,
    "url": "...",
    "title": "USGS Earthquakes",
    "status": 200,
    "api": "2.4.0",
    "count": 0
  },
  "features": []
}
```

Zero earthquakes in Bahrain bounding box during the query period, as expected.

**Expanding to Gulf region (Iran included):**
If the bounding box is expanded to include the Zagros Mountains and southern Iran
(e.g., 25°N-30°N, 48°E-58°E), the query would return dozens to hundreds of events
per month, including:
- Microseismicity (M1-3): Thousands of small events, mostly not felt
- Moderate earthquakes (M4-5): Dozens per month, occasionally felt in Gulf coastal areas
- Large earthquakes (M6+): A few per year, often felt in Bahrain, UAE, Qatar, Kuwait

**Formats available:**
- **GeoJSON**: Default, includes geometry (point location), magnitude, depth, time,
  place description, felt reports, and URLs to detailed event pages
- **QuakeML**: XML standard for seismological data interchange
- **CSV**: Flat table format (lat, lon, depth, mag, time, etc.)
- **KML**: Google Earth-compatible format
- **XML**: Generic XML representation

**Parameters:**
- Geographic bounding box: `minlatitude`, `maxlatitude`, `minlongitude`, `maxlongitude`
- Time range: `starttime`, `endtime` (ISO8601 format)
- Magnitude: `minmagnitude`, `maxmagnitude`
- Depth: `mindepth`, `maxdepth` (km)
- Output format: `format=geojson|quakeml|csv|kml|xml`
- Limit: `limit={number}` (max results)
- Order by: `orderby=time|magnitude|time-asc|magnitude-asc`

## Integration Notes

**Overlap with existing coverage:**
The repo already has a USGS seismology bridge (per SKILL.md domain taxonomy). Adding
a Bahrain-specific bounding box filter to that bridge would be trivial but adds **very
limited value** because:
- Bahrain itself has negligible seismicity (zero events in most time periods)
- The existing USGS bridge likely already captures Gulf region events if it uses a
  global or broad geographic filter
- Regional events (Iran, Zagros) are already covered by the global USGS feed

**Potential Bahrain-specific use cases:**
1. **Felt reports in Bahrain**: USGS "Did You Feel It?" system collects citizen reports
   of felt shaking. If a large Iranian earthquake is felt in Bahrain, the USGS event
   page may include felt reports from Bahrain. However, this data is not always exposed
   via the FDSN API (it's available on event detail pages but not always in the core
   event feed).
2. **Infrastructure monitoring**: Bahrain critical infrastructure operators (EWA, oil/gas,
   airports, ports) may want to track regional seismicity for risk assessment. A
   "Gulf region seismicity" feed (not Bahrain-only) would be more useful.
3. **Public awareness**: A "earthquakes felt in Bahrain" feed could combine USGS data
   with filtering logic (e.g., M5+ events within 500 km of Bahrain) and USGS ShakeMap
   intensity estimates to predict which events are likely felt in Manama.

**Alternative: Regional seismicity bridge (Gulf-wide):**
Instead of a Bahrain-only bridge (which would rarely produce events), a "Gulf region
seismology" bridge could:
- Cover Bahrain, Kuwait, Qatar, UAE, Oman, southern Iraq, eastern Saudi Arabia, and
  western Iran (Zagros)
- Include all M4+ events (felt-threshold for the region)
- Provide context for Gulf residents on regional earthquake activity
- Key events by USGS event ID (globally unique, stable)
- This would be **additive** (new geographic region for seismology) and higher value
  than a Bahrain-only filter

**Alternative: National seismology network (not found):**
Bahrain does not appear to operate its own seismological network or publish local
seismic data. The University of Bahrain or the Supreme Council for Environment may
have academic/research seismometers, but no public API or data feed was found.

**Recommendation:**
Do **not** create a Bahrain-specific seismology bridge. Bahrain's local seismicity is
negligible, and the existing USGS global bridge already covers the region. If there is
demand for Gulf regional seismicity (for infrastructure monitoring or public awareness),
consider extending the USGS bridge to include a "Gulf region" geographic filter
(Bahrain, UAE, Qatar, Kuwait, Oman, Zagros) for M4+ events. This would provide context
for seismic hazards that could affect Bahrain without creating a low-value Bahrain-only
feed.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time (events published within minutes of detection) |
| Openness | 3 | No auth, fully open |
| Stability | 3 | USGS is authoritative, FDSN is international standard |
| Structure | 3 | GeoJSON, QuakeML, CSV, all well-structured |
| Identifiers | 3 | USGS event IDs are globally unique and stable |
| Additive value | 1 | Bahrain-specific filter adds no value (zero events); Gulf-wide filter would be additive but still limited |

**Verdict**: **Not recommended** for Bahrain-specific seismology bridge. Bahrain has
negligible local seismicity (zero events in typical query periods), so a Bahrain-only
feed would be empty 99.9% of the time. The existing USGS global bridge already covers
the Arabian Gulf region. If there is interest in regional seismicity (for infrastructure
risk monitoring or public awareness), a "Gulf region" filter (covering Bahrain, UAE,
Qatar, Kuwait, Oman, and the Zagros fault zone in Iran) for M4+ events would be more
useful than a Bahrain-only feed. Score reflects global USGS capabilities, not
Bahrain-specific value (which is ~1/18).
