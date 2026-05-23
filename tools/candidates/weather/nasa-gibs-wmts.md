# NASA GIBS / Worldview WMTS Tiles

- **Country/Region**: Global
- **Endpoint**: `https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/wmts.cgi`
- **Protocol**: WMTS (Web Map Tile Service), WMS
- **Auth**: None
- **Format**: PNG, JPEG (raster tiles)
- **Freshness**: Near real-time (3 hours to 1 day, varies by layer)
- **Docs**: https://wiki.earthdata.nasa.gov/display/GIBS/
- **Score**: 10/18

## Overview

NASA's Global Imagery Browse Services (GIBS) provides a WMTS endpoint for over 900 satellite imagery layers from MODIS, VIIRS, AIRS, OMI, and other NASA Earth-observing instruments. GIBS powers NASA's Worldview web application (worldview.earthdata.nasa.gov) and delivers pre-rendered map tiles at multiple zoom levels and projections (geographic, Arctic polar, Antarctic polar).

Near real-time layers are updated within 3 hours to 1 day of satellite observation and include true-color imagery, false-color composites, land surface temperature, snow cover, sea ice, aerosol optical depth, chlorophyll-a, and fire/thermal anomalies. GIBS is optimized for visualization (web maps, dashboards, time-lapse videos) rather than quantitative analysis.

Tiles are delivered as PNG or JPEG images via standard OGC WMTS requests. No auth required. Temporal layers support date/time parameters to retrieve historical imagery. The service is operated by NASA EOSDIS and handles billions of tile requests per month.

## Endpoint Analysis

**GIBS WMTS GetCapabilities:**
```
GET https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/1.0.0/WMTSCapabilities.xml
```

**Sample tile request (MODIS Terra True Color, date 2024-01-15, zoom level 5, tile 10,5):**
```
GET https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/MODIS_Terra_CorrectedReflectance_TrueColor/default/2024-01-15/250m/5/10/5.jpg
```

Returns a 512×512 JPEG tile of Earth imagery.

**Available NRT layers (sample):**
- `MODIS_Terra_CorrectedReflectance_TrueColor` — RGB imagery, 250m, daily
- `VIIRS_SNPP_CorrectedReflectance_TrueColor` — RGB, 250m, daily
- `MODIS_Aqua_Land_Surface_Temp_Day` — LST, 1km, daily
- `MODIS_Combined_Thermal_Anomalies_All` — Active fire/thermal hotspots, 1km, daily
- `VIIRS_SNPP_CorrectedReflectance_BandsM11-I2-I1` — False color (fires), 250m, daily
- `AIRS_L2_Surface_Air_Temperature_Day` — Atmospheric temperature, 50km, twice daily
- `OMI_Aerosol_Optical_Depth` — Aerosol, 25km, daily
- `MODIS_Aqua_Snow_Cover` — Binary snow/no-snow, 500m, daily

**Layer metadata** (from Worldview config):
```json
{
  "id": "MODIS_Terra_CorrectedReflectance_TrueColor",
  "title": "Corrected Reflectance (True Color, Terra/MODIS)",
  "subtitle": "Terra / MODIS",
  "description": "True-color corrected reflectance imagery from MODIS on NASA's Terra satellite",
  "format": "image/jpeg",
  "type": "wmts",
  "period": "daily",
  "startDate": "2000-02-24T00:00:00Z"
}
```

## Why Strong

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | 3 hours to 1 day, varies by layer; MODIS/VIIRS NRT ~3-6 hours |
| Openness | 3 | No auth, no registration, generous usage limits |
| Stability | 3 | NASA EOSDIS production system since 2012, WMTS standard |
| Structure | 1 | Raster tiles (PNG/JPEG), not structured data; no per-pixel API |
| Identifiers | 1 | Tile coordinates (zoom/x/y) + date, but no entity IDs |
| Richness | 0 | Visual imagery only; no numeric values, metadata, or attribution per pixel |

**GIBS excels for visualization, not for event streaming.** It's designed to power web maps and dashboards, not to emit structured CloudEvents. Tiles are pre-rendered images — you cannot query "all fire pixels in this region" or "temperature at this point"; you get a picture. This makes it unsuitable for a Kafka bridge that emits event records with schema.

**Why it's here:** GIBS provides *imagery basemaps* for geospatial event visualization (e.g., overlaying FIRMS fire points on MODIS true-color tiles), but it is not itself a real-time data source with identifiers and measurements. It's a rendering service, not a data API.

## Limitations

- **Raster tiles, not structured data.** WMTS returns images, not JSON/CSV with measurements. Extracting numeric values (e.g., fire pixel locations, temperature grids) from PNG tiles would require reverse-engineering tile-to-lat/lon math and image analysis — fragile and lossy.
- **No per-pixel metadata.** You get a picture of aerosol optical depth, but not "AOD = 0.35 at lat/lon X,Y with timestamp T and quality flag Q."
- **Visualization-optimized rendering.** Colors, contrast, and blending are tuned for human readability, not quantitative accuracy. True scientific data is available from the upstream sources (MODIS/VIIRS Level 2/3 products), not from GIBS.
- **No change detection or delta API.** WMTS is stateless; you request tiles by date, not "give me pixels that changed since yesterday."
- **Volume.** A global daily mosaic at zoom level 5 (250m) is thousands of tiles. Fetching and diffing entire tile pyramids is impractical.

**GIBS is a companion service, not a primary data source.** If you're building a wildfire bridge, you query FIRMS for fire pixel data *and* fetch GIBS tiles for background imagery in a dashboard. But GIBS itself is not the event stream.

## Final Verdict

**Verdict**: ⏭️ **Reference**

GIBS is an excellent NASA service for satellite imagery visualization, but it does not fit the repo's CloudEvents-over-Kafka model. It delivers raster tiles (images), not structured event records with identifiers and measurements. Use GIBS to *visualize* events from other NASA feeds (FIRMS fire pixels, EONET natural events, GPM precipitation grids), but do not bridge GIBS itself.

**If the repo ever adds a "satellite basemap tile cache" pattern** (e.g., pre-fetch MODIS true-color tiles for known wildfire regions and serve them alongside fire event streams), GIBS is the ideal source. But that's a different use case than real-time event bridging.

**For structured NASA satellite data,** use the upstream L2/L3 products (MODIS/VIIRS active fire from FIRMS, IMERG precipitation, SMAP soil moisture, etc.) rather than GIBS's pre-rendered imagery.

**Bridge type:** N/A (visualization service, not event source)
