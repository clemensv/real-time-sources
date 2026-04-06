# CLDN / GeoMet — Canadian Lightning Detection Network

**Country/Region**: Canada (+ 250 km buffer from borders)
**Publisher**: Environment and Climate Change Canada (ECCC) / Meteorological Service of Canada (MSC)
**API Endpoint**: `https://geo.weather.gc.ca/geomet?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&LAYERS=Lightning_2.5km_Density`
**Documentation**: https://eccc-msc.github.io/open-data/msc-geomet/readme_en/
**Protocol**: OGC WMS 1.3.0
**Auth**: None — fully open, anonymous access
**Data Format**: WMS image tiles (PNG, JPEG, GeoTIFF via GetMap) — gridded density product, not raw stroke data
**Update Frequency**: Every 10 minutes
**License**: Open Government Licence — Canada

## What It Provides

The Canadian Lightning Detection Network (CLDN) is a national lightning detection system operated by ECCC. Lightning data is published as a gridded density product via the GeoMet WMS service — showing flash density in flashes/km²/min at 2.5 km resolution, aggregated over 10-minute windows.

The CLDN detects both cloud-to-ground (CG) and intra-cloud (IC) lightning across Canada and a 250 km buffer zone extending into adjacent areas.

This is a gridded density product — not individual stroke/flash data. It's excellent for spatial analysis, visualization, and area-based alerting but not for tracking individual lightning events.

## API Details

### WMS GetMap

```
GET https://geo.weather.gc.ca/geomet?
    SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap
    &BBOX=40,-130,70,-50
    &CRS=EPSG:4326
    &WIDTH=800&HEIGHT=600
    &LAYERS=Lightning_2.5km_Density
    &FORMAT=image/png
```

Returns: PNG image with lightning density overlay.

### Layer Details

| Property | Value |
|---|---|
| Layer name | `Lightning_2.5km_Density` |
| Resolution | 2.5 km × 2.5 km grid |
| Content | Flash density (flashes/km²/min) |
| Update frequency | Every 10 minutes |
| Coverage | Canada + 250 km border buffer |
| Lightning types | CG + IC |

### Metadata Record

```
GET https://csw.open.canada.ca/geonetwork/srv/csw?service=CSW&version=2.0.2
    &request=GetRecordById
    &outputschema=csw:IsoRecord
    &elementsetname=full
    &id=75dfb8cb-9efc-4c15-bcb5-7562f89517ce
```

### What's Not Available

- No OGC API Features endpoint for lightning (404)
- No raw stroke/flash data on MSC Datamart (dd.weather.gc.ca)
- No individual lightning event data — gridded density only

## Freshness Assessment

10-minute updates confirmed via layer metadata. WMS endpoint verified live on 2026-04-06. The GeoMet infrastructure is production-grade — part of Canada's national meteorological data delivery system.

## Entity Model

- **Grid Cell** — 2.5 km × 2.5 km cell with flash density value (flashes/km²/min)
- No discrete lightning event entities — this is a continuous density field product
- TIME dimension allows historical queries

## Feasibility Rating

| Criterion | Score | Notes |
|---|---|---|
| Freshness | 3 | 10-minute updates |
| Openness | 3 | No auth, Open Government Licence, standard WMS |
| Stability | 3 | ECCC/MSC production infrastructure |
| Structure | 2 | WMS raster only — no vector/JSON output for individual events |
| Identifiers | 1 | Grid cells only, no event IDs |
| Additive Value | 2 | Canadian coverage fills gap between Blitzortung density and professional networks |
| **Total** | **14/18** | |

## Notes

- This is a density product, not raw event data. The distinction matters: you can see "5 flashes/km²/min in this area" but not "a flash occurred at lat X, lon Y at time T."
- For raw lightning event data in Canada, Blitzortung provides crowdsourced individual strike data, or commercial sources (Vaisala) provide professional-grade data.
- The GeoMet platform hosts many other meteorological layers — radar, satellite imagery, forecasts — that could complement lightning data for a severe weather monitoring system.
- WMS raster output means you get images, not queryable data. GetFeatureInfo may return point values but not full dataset export.
- Canada's CLDN uses ~100 sensors and detects ~2-3 million CG flashes per year.
