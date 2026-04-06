# EFFIS / GWIS (European Forest Fire Information System / Global Wildfire Information System)

**Country/Region**: Europe, Middle East, North Africa (EFFIS) / Global (GWIS)
**Publisher**: European Commission Joint Research Centre (JRC) / Copernicus Emergency Management Service
**API Endpoint**: `https://maps.effis.emergency.copernicus.eu/effis?service=WFS&request=getfeature&typename={LAYER}&version=1.1.0&outputformat={FORMAT}`
**Documentation**: https://effis.jrc.ec.europa.eu/applications/data-and-services
**Protocol**: OGC WFS / WMS
**Auth**: None
**Data Format**: GML, Shapefile, SpatiaLite (via WFS outputformat parameter)
**Update Frequency**: Daily (active fires/burnt areas updated from MODIS/VIIRS)
**License**: Copernicus data license (free, attribution required)

## What It Provides

EFFIS provides an integrated European fire monitoring system with several data layers:

- **Active Fire detections** — MODIS and VIIRS hotspots (last 1/7/30 days and full season)
- **Burnt Area mapping** — MODIS and VIIRS-derived burnt area polygons (real-time updated)
- **Fire Danger Forecast** — Fire Weather Index (FWI) system with multiple sub-indices (1-day forecast)
- **Fire severity** — Annual severity rasters (GeoTIFF)
- **Country statistics** — Annual burnt area and fire count totals

The GWIS extension provides global coverage using similar methodologies.

## API Details

WFS endpoints for key layers:

**Burnt Areas (real-time):**
```
https://maps.effis.emergency.copernicus.eu/effis?service=WFS&request=getfeature&typename=ms:modis.ba.poly&version=1.1.0&outputformat=SHAPEZIP
```

**Active Fire Hotspots (MODIS/VIIRS last N days):**
```
https://maps.effis.emergency.copernicus.eu/gwis?service=WFS&request=getfeature&typename=ms:viirs.hs.7d&version=1.1.0&outputformat=application/json
```

**WMS for map tiles:**
```
https://maps.effis.emergency.copernicus.eu/gwis?service=WMS&request=GetMap&layers={LAYER}&format=image/png&...
```

Available WFS layers include:
- `ms:modis.hs` — MODIS hotspots
- `ms:viirs.hs` — VIIRS hotspots
- `ms:modis.ba.poly` — MODIS burnt area polygons
- Fire danger forecast layers (FWI, ISI, BUI, FFMC, DMC, DC)

## Freshness Assessment

Good. Active fire layers are updated daily from satellite overpasses. Burnt area perimeters are derived and updated with some processing delay (typically 1-2 days). Fire danger forecasts are published daily. Not as fast as FIRMS for point detections, but the burnt area polygons provide unique value.

## Entity Model

**Burnt Area polygons** include:
- Geometry (polygon)
- Fire ID / area identifier
- Area (hectares)
- Detection date range
- Country / NUTS region

**Hotspot points** follow similar schema to FIRMS with:
- Coordinates, brightness, FRP, confidence, satellite, datetime

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Daily updates, not real-time streaming |
| Openness | 3 | Open, no auth required |
| Stability | 3 | EU-backed Copernicus service, operational since 2003 |
| Structure | 2 | OGC WFS — standard but verbose; JSON output available |
| Identifiers | 2 | Burnt areas have IDs; hotspots are point-level |
| Additive Value | 3 | Burnt area polygons are unique; FWI forecast adds value |
| **Total** | **15/18** | |

## Notes

- The WFS endpoint was returning 502 errors during testing — may have intermittent availability issues.
- Burnt area polygons are the key differentiator vs FIRMS (which only provides point detections).
- Data request form available for historical/custom extracts.
- GWIS (`maps.effis.emergency.copernicus.eu/gwis`) extends coverage globally.
- Consider pairing with FIRMS for real-time detections + EFFIS for aggregated burnt area analysis.
