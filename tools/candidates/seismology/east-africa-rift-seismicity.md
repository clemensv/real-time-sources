# East Africa Rift Seismicity (EMSC + USGS)

- **Country/Region**: East Africa (Ethiopia, Tanzania, Mozambique, Malawi, DRC, Kenya, Uganda, Rwanda, Botswana, South Africa)
- **Endpoint**: `https://seismicportal.eu/fdsnws/event/1/query?format=json&minlat=-35&maxlat=15&minlon=20&maxlon=55&limit=50&orderby=time`
- **Protocol**: REST (FDSN standard)
- **Auth**: None
- **Format**: JSON, GeoJSON, QuakeML (XML)
- **Freshness**: Near real-time (events appear within minutes)
- **Docs**: https://www.seismicportal.eu/fdsn-wsevent.html
- **Score**: 16/18

## Overview

The East African Rift System is one of the most seismically active zones on the
continent, stretching from the Afar Triangle in Ethiopia down through Kenya, Tanzania,
Malawi, and into Mozambique. The region produces frequent moderate earthquakes (M3–5)
and occasional larger events. South Africa also sees mining-induced seismicity.

Both EMSC (European) and USGS provide FDSN-compliant APIs that cover Africa. The
EMSC SeismicPortal is particularly good because it aggregates data from the South African
Seismological Network (SASN) and other regional networks.

## Endpoint Analysis

**EMSC SeismicPortal** (verified live):
```
GET https://seismicportal.eu/fdsnws/event/1/query?format=json&minlat=-35&maxlat=15&minlon=20&maxlon=55&limit=5&orderby=time
```

Recent African events returned:
| Date | Location | Mag | Source |
|------|----------|-----|--------|
| 2026-04-01 | South Africa | M3.6 | SASN |
| 2026-04-01 | Ethiopia | M4.4 | EMSC |
| 2026-03-30 | Botswana | M4.3 | SASN |
| 2026-03-28 | Mozambique Channel | M4.2 | SASN |
| 2026-03-28 | Mozambique Channel | M4.5 | EMSC |

**USGS** (verified live):
```
GET https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&minlatitude=-35&maxlatitude=35&minlongitude=-20&maxlongitude=55&limit=5&orderby=time
```

Returns GeoJSON FeatureCollection with Ethiopia and Mozambique Channel events.

Both sources follow the FDSN Web Service specification, making them interchangeable.

## Integration Notes

- **Dual-source bridge**: Poll both EMSC and USGS, deduplicate by event time/location.
  EMSC often has African events faster due to SASN contribution.
- **FDSN standard**: The protocol is identical to what the existing `usgs-earthquakes`
  bridge uses — the same code can work with a different bounding box.
- **Event types**: The `auth` field indicates the contributing network (SASN for South
  Africa, EMSC for European detections). This is useful metadata.
- **Mining seismicity**: Many South African events are mine-related (shallow, ~10km depth).
  The `evtype` field distinguishes these (`ke` = known earthquake).
- **Polling interval**: Every 2–5 minutes is sufficient. Africa generates perhaps 5–15
  detectable events per day.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Events appear within minutes |
| Openness | 3 | No auth, FDSN open standard |
| Stability | 3 | EMSC/USGS operational infrastructure |
| Structure | 3 | GeoJSON, QuakeML, well-documented schema |
| Identifiers | 3 | EMSC unid / USGS event IDs |
| Richness | 1 | Seismic data only (but comprehensive) |
