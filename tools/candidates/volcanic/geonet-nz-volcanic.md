# GeoNet New Zealand — Volcanic Alert Level API

**Country/Region**: New Zealand
**Publisher**: GNS Science / GeoNet (funded by EQC — Earthquake Commission)
**API Endpoint**: `https://api.geonet.org.nz/volcano/val`
**Documentation**: https://api.geonet.org.nz/
**Protocol**: REST (GeoJSON)
**Auth**: None
**Data Format**: GeoJSON (application/vnd.geo+json;version=2)
**Update Frequency**: As conditions change (alert level reviews)
**License**: Creative Commons Attribution 3.0 New Zealand (CC BY 3.0 NZ)

## What It Provides

GeoNet operates New Zealand's geological hazard monitoring network. The volcanic API provides:

- **Volcanic Alert Levels (VAL)** — Current alert level for all monitored NZ volcanoes (0-5 scale)
- **Activity descriptions** — Current volcanic unrest status in plain English
- **Hazard summaries** — What hazards to expect at the current level
- **Volcano locations** — GeoJSON point geometries for each volcano
- **Aviation colour codes** — Mapped from alert levels (Green/Yellow/Orange/Red)

Additionally, the broader GeoNet API offers volcanic earthquake data via the `volcquakes` endpoint.

## API Details

**Volcanic Alert Levels:**
```
GET https://api.geonet.org.nz/volcano/val
Accept: application/vnd.geo+json;version=2
```

Returns a GeoJSON FeatureCollection with all monitored NZ volcanoes:
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {"type": "Point", "coordinates": [177.183, -37.521]},
      "properties": {
        "volcanoID": "whiteisland",
        "volcanoTitle": "White Island",
        "level": 2,
        "acc": "Orange",
        "activity": "Moderate to heightened volcanic unrest.",
        "hazards": "Volcanic unrest hazards, potential for eruption hazards."
      }
    }
  ]
}
```

**Volcanic Earthquakes:**
```
GET https://api.geonet.org.nz/volcquakes/{volcanoID}
```

**API versioning** via Accept header:
```
Accept: application/vnd.geo+json;version=2
```

Monitored volcanoes (as of testing): Taupo, Tongariro, Auckland Volcanic Field, Kermadec Islands, Mayor Island, Ngauruhoe, Northland, Okataina, Rotorua, Taranaki/Egmont, White Island (Whakaari), Ruapehu.

## Freshness Assessment

Alert levels are updated as conditions change — this can be minutes during a crisis or weeks/months during quiescence. The API always returns the current state. White Island was at Level 2 (Orange) and Ruapehu at Level 1 (Green, minor unrest) during testing, showing active monitoring.

## Entity Model

**Volcano feature:**
- `volcanoID` — Slug identifier (e.g., "whiteisland")
- `volcanoTitle` — Display name
- `level` — Numeric alert level (0-5)
- `acc` — Aviation colour code ("Green", "Yellow", "Orange", "Red")
- `activity` — Activity description text
- `hazards` — Hazard description text
- `geometry` — Point coordinates [lon, lat]

**Alert level scale (NZ-specific):**
- 0: No volcanic unrest
- 1: Minor volcanic unrest
- 2: Moderate to heightened volcanic unrest
- 3: Minor volcanic eruption
- 4: Moderate volcanic eruption
- 5: Major volcanic eruption

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Current state always available; updates event-driven |
| Openness | 3 | CC BY 3.0, no auth, clean REST API |
| Stability | 3 | Government-funded, long-running, well-documented API |
| Structure | 3 | Standard GeoJSON, versioned API, clean schema |
| Identifiers | 3 | Consistent volcano IDs, stable endpoints |
| Additive Value | 2 | NZ-specific but excellent API quality |
| **Total** | **16/18** | |

## Notes

- This is a model of how volcanic monitoring APIs should be built. Clean GeoJSON, versioned API, good documentation, no auth.
- The broader GeoNet API also provides earthquakes (general and volcanic), strong motion, and intensity data.
- 12 volcanoes currently monitored — small dataset but high quality.
- White Island (Whakaari) at Level 2 during testing confirms active data updates.
- The NZ volcanic alert level scale (0-5) differs from the USGS system (Normal/Advisory/Watch/Warning).
- Bug reports accepted via GitHub: https://github.com/GeoNet/help
- Compression (gzip) is supported and recommended for efficient data transfer.
