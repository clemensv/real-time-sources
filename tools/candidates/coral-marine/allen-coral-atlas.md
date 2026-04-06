# Allen Coral Atlas
**Country/Region**: Global (all tropical/subtropical coral reef regions)
**Publisher**: Vulcan Inc. / Allen Institute / Arizona State University / University of Queensland
**API Endpoint**: `https://allencoralatlas.org/atlas/` (web portal + GCS downloads)
**Documentation**: https://allencoralatlas.org/methods/ (methodology), download instructions
**Protocol**: Web portal, Google Cloud Storage (GCS) for data tiles
**Auth**: None for web portal; GCS access may require account
**Data Format**: GeoTIFF (raster), GeoJSON (vector), WMS tiles
**Update Frequency**: Periodic (satellite imagery reprocessing campaigns)
**License**: CC BY 4.0 (Creative Commons Attribution)

## What It Provides
The Allen Coral Atlas provides the first comprehensive, high-resolution global map of the world's shallow coral reefs:
- **Benthic habitat classification**: Coral/Algae, Rock, Rubble, Sand, Seagrass, Microalgal Mats
- **Geomorphic zonation**: Reef Crest, Reef Flat, Back Reef, Fore Reef, Lagoon, Slope, Plateau
- **Coral bleaching monitoring**: Satellite-detected bleaching events (since 2023)
- **Reef extent mapping**: Global reef boundaries at ~5m resolution
- **Coverage**: All tropical/subtropical reefs between 30°N and 30°S
- **Resolution**: ~3.7m (Planet satellite imagery) classified to ~5m products
- **Area**: Maps 348,000 km² of shallow reef habitat globally

Built using Planet satellite imagery and machine learning classification, validated by reef scientists worldwide.

## API Details
- **Web portal**: `https://allencoralatlas.org/atlas/` — interactive map viewer (HTTP 200)
- **Data download**: Available as GeoTIFF tiles via Google Cloud Storage
  - GCS bucket: `storage.googleapis.com/coral-atlas-static-files/`
  - Download instructions PDF available on site
- **No REST API discovered**:
  - `https://api.allencoralatlas.org/` — DNS resolution failure
  - `https://tiles.allencoralatlas.org/` — DNS resolution failure
  - ArcGIS endpoints — 404
- **Tile access**: Map tiles served for the web viewer; URL patterns discoverable via DevTools
- **Regional downloads**: Data available by country/region for manageable file sizes

## Probe Results
```
https://allencoralatlas.org/atlas/: HTTP 200 OK (interactive map)
https://api.allencoralatlas.org/: DNS failure
https://tiles.allencoralatlas.org/: DNS failure
GCS references found in page source: storage.googleapis.com/coral-atlas-static-files/
Assessment: Portal active, data via GCS downloads, no REST API
```

## Freshness Assessment
Moderate. The Atlas is updated through periodic reprocessing campaigns (typically annual or when new satellite imagery warrants reclassification). Bleaching detection products are more frequent. This is a mapping product, not a real-time monitoring system.

## Entity Model
- **ReefArea** (geographic polygon, country, region)
- **BenthicClass** (Coral/Algae, Rock, Rubble, Sand, Seagrass — per pixel)
- **GeomorphicZone** (Reef Crest, Flat, Slope, Lagoon — per pixel)
- **BleachingEvent** (location, date detected, severity)
- **Tile** (GeoTIFF raster, bounding box, resolution, CRS)

## Feasibility Rating
| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 1 | Periodic reprocessing, not real-time |
| Openness | 2 | CC BY 4.0, but GCS download required |
| Stability | 3 | Major philanthropic/academic consortium |
| Structure | 2 | GeoTIFF raster + GeoJSON vector, no JSON API |
| Identifiers | 2 | Geographic coordinates, country/region |
| Additive Value | 3 | Only global high-res coral reef classification |
| **Total** | **13/18** | |

## Notes
- First and only comprehensive global coral reef map at this resolution
- Planet satellite imagery provides unprecedented ~3.7m resolution
- Bleaching detection is a newer feature — may get more frequent updates
- GCS download model is practical for spatial analysis but not ideal for API integration
- Consider using the GeoTIFF tiles with a spatial database (PostGIS) for local querying
- Pairs with NOAA CRW (thermal stress), OBIS (biodiversity), and AIMS (in-situ data)
- Paul Allen's (Microsoft co-founder) conservation initiative — well-funded and maintained
