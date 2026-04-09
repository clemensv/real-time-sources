# USGS Volcano Hazards — Cascades Volcano Observatory (CVO)

- **Country/Region**: US — Pacific Northwest (Mt. Rainier, Mt. Baker, Mt. St. Helens, Glacier Peak, Mt. Adams)
- **Publisher**: USGS Volcano Hazards Program / Cascades Volcano Observatory
- **Endpoint**: `https://volcanoes.usgs.gov/hans2/api/` (HANS API) and `https://earthquake.usgs.gov/fdsnws/event/1/query` (seismic)
- **Protocol**: REST
- **Auth**: None
- **Format**: JSON, GeoJSON
- **Freshness**: Event-driven (alerts on status change); seismic data near real-time
- **Docs**: https://volcanoes.usgs.gov/hans2/api/ and https://www.usgs.gov/observatories/cvo
- **Score**: 14/18

## Overview

The USGS Cascades Volcano Observatory (CVO) monitors five major Cascade volcanoes visible from the Puget Sound area: Mt. Rainier, Mt. Baker, Mt. St. Helens, Glacier Peak, and Mt. Adams. While the existing `usgs-volcano-hans` candidate in `tools/candidates/volcanic/` covers the national HANS API, this candidate focuses on the **Puget Sound-relevant** integration: combining HANS alert levels with USGS earthquake data filtered for volcanic regions to provide volcano safety context for outdoor recreation near these peaks.

## API Details

### HANS API (Alert Levels)
**Base URL:** `https://volcanoes.usgs.gov/hans2/api/`

See existing candidate `tools/candidates/volcanic/usgs-volcano-hans.md` for full HANS API details.

**Relevant CVO Volcanoes:**

| Volcano | USGS ID | Distance from Seattle |
|---------|---------|----------------------|
| Mt. Rainier | wa6 | ~54 miles SE |
| Mt. Baker | wa4 | ~90 miles N |
| Mt. St. Helens | wa5 | ~96 miles S |
| Glacier Peak | wa3 | ~70 miles NE |
| Mt. Adams | wa2 | ~130 miles SE |

### USGS Earthquake API (Volcanic Seismicity)
**Base URL:** `https://earthquake.usgs.gov/fdsnws/event/1/query`

**Volcano-area Seismic Query (Mt. Rainier within 20km):**
```
GET ?format=geojson&starttime=2024-01-01&latitude=46.8523&longitude=-121.7603&maxradiuskm=20&minmagnitude=0.5
```

This returns earthquakes near the volcano, which is the primary real-time monitoring signal for volcanic unrest.

### Pacific Northwest Seismic Network (PNSN)
- PNSN provides volcano-specific seismic monitoring pages
- Website: https://pnsn.org/volcanoes/mount-rainier
- CSV/GeoJSON event feeds are available for recent events

## Freshness Assessment

Good for alert-based data. HANS alert levels change only when volcanic conditions change (which is rare — most Cascade volcanoes are at "Normal" most of the time). However, seismic data near volcanoes updates near real-time as earthquakes are detected. The combination of alert levels (context) and seismic data (activity) provides a complete picture.

## Entity Model

- **Volcano** — ID, name, location, observatory (CVO), current alert level, aviation color code
- **Alert Level** — Normal, Advisory, Watch, Warning
- **Notice** — VAN/VONA (Volcano Activity Notice / Volcano Observatory Notice for Aviation)
- **Earthquake** — Time, location, magnitude, depth (near volcano)
- **Observatory** — CVO for all Cascade volcanoes

## Feasibility Rating

| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 2 | Alerts are event-driven; seismic is near real-time |
| Openness | 3 | US federal public domain, no auth |
| Stability | 3 | USGS — authoritative, decades of operation |
| Structure | 2 | HANS API is sparse; earthquake API is excellent GeoJSON |
| Identifiers | 2 | Volcano IDs, earthquake event IDs |
| Additive Value | 2 | Safety context for hiking/recreation near Cascade volcanoes |
| **Total** | **14/18** | |

## Notes

- The existing `usgs-volcano-hans` candidate covers the national HANS API. This candidate adds value by combining it with earthquake data for a Puget Sound-specific volcano monitoring feed.
- The existing `usgs-earthquakes` bridge in the repo could be parameterized for volcano proximity queries — this may not need a separate bridge.
- Mt. Rainier is the most relevant: it's a national park with heavy recreational use, visible from Seattle, and is the most dangerous volcano in the US due to lahar risk.
- Volcanic unrest is rare but extremely high-consequence — even Advisory level would be major news.
- PNSN seismic data adds granularity beyond USGS national earthquake catalog.
- Consider also: USGS lahar detection system (LAHAR) for Mt. Rainier — limited public API but the alert system exists.
