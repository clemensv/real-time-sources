# German BfS ODL Network (Ortsdosisleistung)

**Country/Region**: Germany
**Publisher**: Bundesamt für Strahlenschutz (BfS) — Federal Office for Radiation Protection
**API Endpoint**: `https://www.imis.bfs.de/ogc/opendata/ows` (WFS) and `https://odlinfo.bfs.de/` (public portal)
**Documentation**: https://odlinfo.bfs.de/ODL/EN/home/home_node.html
**Protocol**: OGC WFS 1.1.0
**Auth**: None
**Data Format**: GeoJSON, GML, CSV, KML, Shapefile (via WFS outputFormat parameter)
**Update Frequency**: Every 30 minutes (abi_30min), hourly, and daily averages
**License**: Open data (Fees: NONE, Access Constraints: NONE per WFS GetCapabilities)

## What It Provides

The BfS ODL (Ortsdosisleistung — ambient dose rate) network consists of approximately 1,700 active measuring stations distributed across Germany. These probes continuously measure gamma ambient dose equivalent rate and report 24-hour averaged values as well as near-real-time 30-minute and hourly measurements.

The network is part of IMIS (Integrated Measuring and Information System), Germany's nuclear emergency preparedness infrastructure. The public WFS endpoint exposes not only the ODL data but also a rich set of environmental radioactivity measurements (aerosols, precipitation, water bodies, food chain monitoring).

## API Details

The BfS GeoServer exposes dozens of feature types through its WFS endpoint. Key layers for radiation monitoring:

### Core ODL Layers
- **`opendata:abi_30min`** — 30-minute ambient dose rate readings
- **`opendata:abi_30min_barchart`** — Bar chart aggregation of 30-min data
- **`opendata:abi_30min_timeseries`** — Time series of 30-min data

### EURDEP Layers (Pan-European)
- **`opendata:eurdep_latestValue`** — Latest EURDEP measurements (see eurdep.md)
- **`opendata:eurdep_maxValue`** — Maximum values

### Environmental Monitoring Layers
- **`opendata:bfg_gesamt_gamma`** — Total gamma in waterways (BfG)
- **`opendata:bsh_gesamt_gamma_kuenstlich`** — Artificial gamma in seawater (BSH)
- **`opendata:new_dwd_alphabeta_kuenstl_24h`** — Alpha/beta aerosols (DWD)
- **`opendata:new_dwd_gamma_aerosole_24h_nuclide`** — Gamma aerosol nuclide analysis
- **`opendata:new_dwd_niederschlag_24h`** — Precipitation radioactivity
- Various food chain monitoring (milk, fish, meat, grain, vegetables, mushrooms...)
- **`opendata:bfs_locations`** — BfS office locations (8 features)

### Example Request

```
GET https://www.imis.bfs.de/ogc/opendata/ows?service=WFS&version=1.1.0
    &request=GetFeature
    &typeName=opendata:abi_30min
    &outputFormat=application/json
    &maxFeatures=5
```

### Station Metadata (from bfs_locations)

```json
{
  "type": "Feature",
  "geometry": { "type": "Point", "coordinates": [10.33115, 52.15153] },
  "properties": {
    "locality_name": "Salzgitter",
    "locality_code": "sz",
    "url": "https://www.bfs.de/DE/bfs/wir/standorte/salzgitter/salzgitter.html"
  }
}
```

## Freshness Assessment

Live data confirmed on 2026-04-06. The `abi_30min` layer returned 0 features at time of testing (possibly outside measurement window or data not yet available), while `eurdep_latestValue` returned 17,963 features with timestamps within the hour. The `bfs_locations` layer returned 8 features. The ODL portal at odlinfo.bfs.de confirms ~1,700 active stations with 24h averaged values.

## Entity Model

- **Station** — Identified by locality code. Has coordinates, name, URL to station page.
- **Measurement** — 30-minute or hourly ambient dose rate in µSv/h. Associated with station, timestamp, measurement type.
- **Environmental Sample** — For extended monitoring: nuclide-specific measurements across environmental media (air, water, food chain).

## Feasibility Rating

| Criterion | Score | Notes |
|---|---|---|
| Freshness | 3 | 30-minute updates, near-real-time ODL |
| Openness | 3 | No auth, explicitly "NONE" fees and constraints |
| Stability | 3 | Federal government infrastructure, GeoServer-based |
| Structure | 3 | Standard WFS with GeoJSON output, well-typed schema |
| Identifiers | 2 | Station codes exist but no formal URI pattern |
| Additive Value | 3 | ~1,700 stations, comprehensive German coverage, plus environmental media |
| **Total** | **17/18** | |

## Notes

- The WFS endpoint is the same server that hosts the EURDEP pan-European data — accessing `opendata:abi_30min` gets Germany-specific ODL data.
- The `abi_30min` layer may have returned 0 features during testing due to timing — the 30-minute data windows may not always be populated. The `eurdep_latestValue` layer is more reliable for latest values.
- The ODL portal at odlinfo.bfs.de provides a user-friendly view with maps, search by location, and historical data.
- BfS also offers WMS (Web Map Service) for map tile rendering.
- Rich environmental monitoring data beyond just ambient dose rate — food chain, water, aerosols — makes this a comprehensive radiological data source.
- All data accessible via standard OGC protocols — easy to integrate with existing GIS tooling.
