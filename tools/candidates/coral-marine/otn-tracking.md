# Ocean Tracking Network (OTN) ERDDAP
**Country/Region**: Global (primarily North Atlantic, but worldwide coverage)
**Publisher**: Ocean Tracking Network, Dalhousie University, Halifax, Canada
**API Endpoint**: `https://members.oceantrack.org/erddap/`
**Documentation**: https://members.oceantrack.org/erddap/ (ERDDAP interface)
**Protocol**: ERDDAP (REST-like, multiple output formats)
**Auth**: None for published datasets (some datasets may require member access)
**Data Format**: JSON, CSV, NetCDF, XML, HTML (ERDDAP multi-format)
**Update Frequency**: Continuous (as detection data is processed and published)
**License**: Various (per dataset, typically CC-BY)

## What It Provides
OTN tracks marine animal movements using acoustic telemetry — the world's largest such network:
- **Animal detections**: Timestamped, geolocated detections of tagged marine animals
- **Species data**: Taxonomic information for tracked animals (fish, sharks, turtles, marine mammals)
- **Receiver deployments**: Locations and metadata for underwater acoustic receivers
- **Tag releases**: Where and when animals were tagged
- **Platform data**: Information about mooring platforms and infrastructure
- **13 active datasets** covering animals, detections, receivers, releases, and joined views

This is essentially a real-time(ish) GPS-for-fish system spanning the world's oceans.

## API Details
- **Dataset catalog**: `GET /erddap/info/index.json` — all available datasets with metadata
- **Key datasets**:
  - `otn_aat_animals` — animal morphology, species, sex, life stage
  - `otn_aat_detections` — acoustic detections with lat/lon/time/depth
  - `otn_aat_receivers` — receiver deployment locations and periods
  - `otn_aat_tag_releases` — tag deployment data
  - `detection_extracts` — detection data with extended metadata
  - `view_otn_aat_detections_stations_projects` — joined view of detections + stations + projects
  - `view_otn_aat_animal_tag_releases` — animals joined with tag and release info
- **ERDDAP query pattern**: `/erddap/tabledap/{datasetId}.json?{constraints}`
  - Example: `/erddap/tabledap/otn_aat_detections.json?time>=2024-01-01&scientificname="Carcharodon carcharias"`
- **Output formats**: `.json`, `.csv`, `.nc`, `.html`, `.mat`, `.tsv`, `.kml`
- **Subsetting**: Filter by time, lat/lon bounding box, species, depth, etc.
- **Services**: tabledap (table data), WMS (maps), SOS (sensor observation), RSS (updates)

## Probe Results
```
https://members.oceantrack.org/erddap/info/index.json
  Status: 200 OK
  Datasets: 13 active datasets
  Includes: animals, detections, receivers, tag_releases, platforms, projects
  ERDDAP server: operational, full multi-format support

Key dataset variables:
  otn_aat_detections: detection_id, time, latitude, longitude, depth,
    transmitter_id, scientificname, detection_quality
  otn_aat_animals: vernacularname, scientificname, aphiaid, length,
    weight, life_stage, age, sex
```

## Freshness Assessment
Good. Detection data is processed in batches — typically quarterly or more frequently for active projects. The ERDDAP server reflects the latest published data. Real-time detection data exists but is typically embargoed for researcher priority before public release.

## Entity Model
- **Animal** (animal_guid, scientificName, vernacularName, aphiaID, sex, length, weight, life_stage)
- **Detection** (detection_id, time, latitude, longitude, depth, transmitter_id, quality)
- **Receiver** (deployment_id, latitude, longitude, depth, model, deployment/recovery dates)
- **TagRelease** (tag_device_id, release time/location, tag_model, tag_frequency, expected_enddate)
- **Project** (project_reference, name, PI, DOI, geographic bounds, time coverage)
- **Datacenter** (datacenter_reference, name, PI, geographic/temporal coverage)

## Feasibility Rating
| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 2 | Batch-processed, not real-time |
| Openness | 2 | Public ERDDAP, some datasets may need member access |
| Stability | 3 | Dalhousie University, major research infrastructure |
| Structure | 3 | ERDDAP multi-format, well-typed schemas, rich metadata |
| Identifiers | 3 | GUIDs for animals/detections, aphiaID (WoRMS), DOIs for projects |
| Additive Value | 3 | Only global marine animal tracking network of this scale |
| **Total** | **16/18** | |

## Notes
- OTN operates 1000+ acoustic receivers across global oceans
- Tagged species include great white sharks, Atlantic sturgeon, sea turtles, bluefin tuna, and more
- ERDDAP is the same platform used by NOAA — standardized and well-understood
- WoRMS aphiaID linkage connects to OBIS marine species taxonomy
- Detection data enables questions like "which sharks pass through this reef corridor?"
- KML output enables direct Google Earth visualization of animal tracks
- RSS feeds available per dataset for change notification
- Pairs with OBIS (biodiversity) and NOAA CRW (thermal stress) for marine ecosystem monitoring
