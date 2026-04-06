# BEYOND/NOA FireHub — Greece Fire Monitoring

**Country/Region**: Greece
**Publisher**: National Observatory of Athens (NOA) — BEYOND Centre of Earth Observation Research and Satellite Remote Sensing
**API Endpoint**: `https://firehub-geoserver.beyond-eocenter.eu/geoserver/firehub/ows`
**Documentation**: https://beyond-eocenter.eu/
**Protocol**: OGC WFS 2.0.0
**Auth**: None
**Data Format**: GeoJSON, GML2, GML3, KML, CSV, Shapefile
**Update Frequency**: Near real-time (satellite overpass based — SEVIRI, VIIRS, MODIS)
**License**: Fees: NONE, AccessConstraints: NONE (per WFS GetCapabilities)

## What It Provides

The BEYOND/NOA FireHub is a comprehensive fire monitoring system for Greece operated by the National Observatory of Athens. It integrates detections from multiple satellite sensors — SEVIRI (geostationary, ~15-minute revisit), VIIRS, and MODIS (polar-orbiting) — into a single GeoServer-based data platform.

The system provides:
- Active fire detections from three satellite sensor families
- Fire propagation modeling
- Burned scar mapping (diachronic archive)
- Contextual overlays (Natura 2000 protected areas, urban atlas)
- User-submitted fire geotags

## API Details

### WFS GetCapabilities

```
GET https://firehub-geoserver.beyond-eocenter.eu/geoserver/wfs?service=WFS&request=GetCapabilities
```

### Feature Types

| Layer | Description | Features |
|---|---|---|
| `firehub:fires_view` | Fire events with centroid, area, sensor, municipality | **8,298** |
| `firehub:events_view` | Events with hazard type, alert source, rich metadata JSON | **8,589** |
| `firehub:seviri` | SEVIRI geostationary satellite hotspots | — |
| `firehub:seviri_range` | SEVIRI detection range/coverage | — |
| `firehub:hr_sat_raw` | High-resolution satellite raw detections | — |
| `firehub:hr_sat_refined` | High-resolution satellite refined detections | — |
| `firehub:propagation` | Fire propagation modeling | — |
| `firehub:geotags_view` | User-submitted fire geotags | — |
| `firehub:natura2000_view` | Natura 2000 protected areas | — |
| `firehub:urbanatlas_view` | Urban Atlas land use | — |

Additional namespaces: `diachronicbsm:bsm_archive` (burned scar maps), `flammap:flammap_ignition/isoline/isopoly` (fire behavior modeling).

### Sample Request (GeoJSON)

```
GET https://firehub-geoserver.beyond-eocenter.eu/geoserver/firehub/ows?
    service=WFS&version=1.0.0&request=GetFeature
    &typeName=firehub:fires_view
    &maxFeatures=10
    &outputFormat=application/json
```

### Sample Response

```json
{
  "type": "FeatureCollection",
  "totalFeatures": 8298,
  "features": [{
    "type": "Feature",
    "geometry": {"type": "Point", "coordinates": [2955832.87, 4730702.86]},
    "properties": {
      "id": "fe1",
      "area": 55,
      "sensor": "NPP",
      "municipality": "Δ. Λέσβου",
      "sensing_start": "2015-06-05T07:54:00Z"
    }
  }],
  "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::3857"}}
}
```

Output formats: GeoJSON, GML2, GML3, KML, Shapefile (SHAPE-ZIP), CSV.

CRS default is EPSG:3857; request `srsName=EPSG:4326` for WGS84 output.

## Freshness Assessment

Live data confirmed on 2026-04-06. 8,298 fire features and 8,589 events in the database. SEVIRI provides near-continuous geostationary monitoring (~15-minute revisit for Greece); VIIRS/MODIS add higher-resolution detections on each polar-orbiting pass. Municipality-level attribution makes this uniquely useful for Greek fire management.

## Entity Model

- **Fire Event** — point feature with ID, area (hectares), sensor source, municipality name, sensing timestamp. 8,298 events in archive.
- **Event** — broader event type with hazard classification, alert source, rich metadata in JSON properties. 8,589 events.
- **Burned Scar** — polygon archive in `diachronicbsm` namespace.
- **Fire Propagation** — modeled fire spread polygons in `flammap` namespace.

## Feasibility Rating

| Criterion | Score | Notes |
|---|---|---|
| Freshness | 3 | Near real-time via SEVIRI geostationary + polar-orbit sensors |
| Openness | 3 | No auth, no stated restrictions, standard WFS |
| Stability | 2 | Academic institution (NOA) — good but not government infrastructure |
| Structure | 3 | Full GeoServer WFS, 6 output formats, rich schema |
| Identifiers | 2 | Event IDs exist but no formal URI scheme |
| Additive Value | 3 | Unique regional depth: municipality-level attribution, fire propagation modeling, burned scar archive |
| **Total** | **16/18** | |

## Notes

- This is a gem — one of the best-structured regional fire monitoring APIs discovered. Full OGC WFS with multiple output formats, no authentication, rich data model.
- Greece experiences severe wildfire seasons, making this data operationally relevant.
- The SEVIRI layer provides rapid geostationary detection that complements the higher-resolution but less frequent VIIRS/MODIS detections.
- The fire propagation modeling layers (`flammap:*`) are unique — few open APIs provide modeled fire spread.
- Complements EFFIS/GWIS for detailed Greek coverage with municipality-level granularity.
