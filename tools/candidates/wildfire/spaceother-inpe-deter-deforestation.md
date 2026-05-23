# INPE DETER (Real-Time Deforestation Detection System) - Brazil

- **Country/Region**: Brazil (Amazon, Cerrado, Pantanal, Caatinga, Mata Atlântica biomes)
- **Endpoint**: `https://terrabrasilis.dpi.inpe.br/geoserver/wfs` (OGC WFS 2.0)
- **Protocol**: WFS 2.0, WMS, REST (GeoJSON, GML, Shapefile)
- **Auth**: None (fully open)
- **Format**: GeoJSON, GML, Shapefile, KML, CSV
- **Freshness**: Daily updates (DETER-B uses daily Sentinel-1/2, Landsat-8/9, CBERS-4/4A)
- **Docs**: https://terrabrasilis.dpi.inpe.br/, http://www.obt.inpe.br/OBT/assuntos/programas/amazonia/deter
- **Score**: 15/18

## Overview

DETER (Sistema de Detecção de Desmatamento em Tempo Real / Real-Time Deforestation Detection System) is **Brazil's operational deforestation alert system** operated by INPE (Instituto Nacional de Pesquisas Espaciais). It provides **daily near-real-time detection** of clear-cutting, forest degradation, logging, and burn scars across all Brazilian biomes.

The system processes **daily satellite imagery** (Sentinel-1 SAR, Sentinel-2 optical, Landsat-8/9, CBERS-4/4A) and publishes **polygon alerts** via OGC WFS/WMS services. Each alert includes deforestation type (clear-cutting, degradation, mining, logging, burn scar), detection date, area (hectares), and geometry.

DETER is **the authoritative source for Brazilian deforestation monitoring**, used by IBAMA (Brazilian environmental police), ICMBio (protected areas agency), and the Ministry of Environment for enforcement and REDD+ reporting.

**Key variants**:
- **DETER-B** (Biomes) — Amazon, Cerrado, Pantanal, Caatinga, Mata Atlântica (all Brazilian biomes)
- **DETER-Amazônia** — Amazon Legal region (9 states)
- **DETER-Cerrado** — Savanna biome (central Brazil)
- **DETER-Pantanal** — Wetlands biome
- **DETER-Caatinga** — Semi-arid northeast biome
- **DETER-Mata Atlântica** — Atlantic Forest biome (coastal)

**Deforestation categories**:
- **DESMATAMENTO_CR** — Clear-cutting (total forest removal)
- **DESMATAMENTO_VEG** — Vegetation suppression
- **DEGRADACAO** — Forest degradation (selective logging, understory fire)
- **MINERACAO** — Mining operations
- **CICATRIZ_DE_QUEIMADA** — Burn scars (wildfire or slash-and-burn)
- **CS_DESORDENADO** — Disorderly deforestation (illegal)
- **CS_GEOMETRICO** — Geometric deforestation (agricultural clearing)

## Endpoint Analysis

**WFS 2.0 service verified** — `https://terrabrasilis.dpi.inpe.br/geoserver/wfs?service=WFS&request=GetCapabilities`

The service exposes **100+ feature types** including:
- `deter-amz:deter_public` — Amazon Legal alerts (current year)
- `deter-amz:deter_history` — Amazon historical alerts (2016-present)
- `deter-cerrado:deter_cerrado` — Cerrado alerts
- `deter-pantanal-nb:deter_pantanal` — Pantanal alerts
- `prodes-legal-amz:accumulated_deforestation_2007` — PRODES annual deforestation masks (1988-present)
- `prodes-legal-amz:yearly_deforestation_2023` — PRODES 2023 polygons
- `queimadas:focos` — Fire hotspots (INPE Queimadas program)

**Example: Query recent DETER-Amazônia alerts (last 30 days)**
```
GET https://terrabrasilis.dpi.inpe.br/geoserver/wfs?service=WFS&version=2.0.0&request=GetFeature&typeName=deter-amz:deter_public&outputFormat=application/json&CQL_FILTER=view_date>=2024-01-01
```

Returns GeoJSON FeatureCollection:
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "id": "deter_public.123456",
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[-60.5, -8.2], [-60.5, -8.1], [-60.4, -8.1], [-60.4, -8.2], [-60.5, -8.2]]]
      },
      "properties": {
        "gid": 123456,
        "origin_gid": 789012,
        "classname": "DESMATAMENTO_CR",
        "quadrant": "220067",
        "path_row": "002/067",
        "view_date": "2024-01-15",
        "sensor": "AMAZONIA1_WFI",
        "satellite": "AMAZONIA-1",
        "areatotalkm": 0.52,
        "areamunkm": 0.45,
        "areauckm": 0.07,
        "county": "Novo Progresso",
        "uf": "PA",
        "uc": null,
        "geom_wkb": "..."
      }
    }
  ]
}
```

**WMS service** for visualization:
```
GET https://terrabrasilis.dpi.inpe.br/geoserver/wms?service=WMS&request=GetMap&layers=deter-amz:deter_public&bbox=-65,-12,-55,-8&width=800&height=600&srs=EPSG:4326&format=image/png&CQL_FILTER=view_date>=2024-01-01
```

Returns PNG map of recent deforestation alerts.

**REST API** (GeoServer REST):
```
GET https://terrabrasilis.dpi.inpe.br/geoserver/rest/workspaces/deter-amz/datastores/deter_public/featuretypes.json
```

Returns metadata about available layers.

## Schema/Sample

**DETER alert feature structure** (GeoJSON):
```json
{
  "gid": 123456,
  "origin_gid": 789012,
  "classname": "DESMATAMENTO_CR",
  "quadrant": "220067",
  "path_row": "002/067",
  "view_date": "2024-01-15",
  "date": "2024-01-15T12:00:00Z",
  "sensor": "AMAZONIA1_WFI",
  "satellite": "AMAZONIA-1",
  "areatotalkm": 0.52,
  "areamunkm": 0.45,
  "areauckm": 0.07,
  "county": "Novo Progresso",
  "uf": "PA",
  "uc": null,
  "ti": null,
  "obs": null,
  "geometry": {
    "type": "Polygon",
    "coordinates": [[[-60.5, -8.2], [-60.5, -8.1], [-60.4, -8.1], [-60.4, -8.2], [-60.5, -8.2]]]
  }
}
```

**Field definitions**:
- `gid` — Unique alert ID (integer, stable)
- `classname` — Deforestation type (DESMATAMENTO_CR, DEGRADACAO, MINERACAO, CICATRIZ_DE_QUEIMADA, etc.)
- `view_date` — Detection date (YYYY-MM-DD)
- `sensor` — Satellite sensor (MSI, OLI, WFI, SAR C, etc.)
- `satellite` — Satellite platform (Sentinel-2A/B, Landsat-8/9, AMAZONIA-1, Sentinel-1A/B, CBERS-4/4A)
- `areatotalkm` — Total alert area (km²)
- `areamunkm` — Area within municipality (km²)
- `areauckm` — Area within protected area (km²)
- `county` — Municipality name (e.g., "Novo Progresso")
- `uf` — Brazilian state code (e.g., "PA" for Pará, "AM" for Amazonas, "MT" for Mato Grosso)
- `uc` — Protected area name (if applicable, else null)
- `ti` — Indigenous territory name (if applicable, else null)
- `path_row` — Landsat WRS-2 path/row (e.g., "002/067")
- `quadrant` — INPE 1:250,000 map sheet code (e.g., "220067")

**Stable identifiers**: `gid` is unique and stable. Suitable for Kafka keys: `{biome}/{gid}` (e.g., `amazon/123456`)

## Why Strong

1. **Operational authority** — DETER is **the official Brazilian deforestation alert system**. Data is used by IBAMA, ICMBio, Federal Police, and Ministério Público for enforcement. Legally authoritative.
2. **Daily updates** — Alerts are published **daily** based on cloud-free satellite imagery. True near-real-time monitoring (vs. annual PRODES reports).
3. **Multi-sensor fusion** — Combines Sentinel-1 SAR (all-weather), Sentinel-2 optical, Landsat-8/9, CBERS-4/4A, and AMAZONIA-1. No single-source dependency.
4. **Multi-biome coverage** — Amazon, Cerrado, Pantanal, Caatinga, Mata Atlântica (all Brazilian biomes, not just Amazon).
5. **Rich attribution** — Each alert includes deforestation type, municipality, state, protected area, indigenous territory, area (hectares), sensor, and detection date.
6. **Fully open** — OGC WFS/WMS, no API keys, GeoJSON/Shapefile export. Standard geospatial protocols.
7. **Historical archive** — DETER data back to 2016, PRODES (annual) back to 1988. Enables change detection and trend analysis.

## Limitations

- **Brazil-only** — No coverage outside Brazilian territory. Not useful for global deforestation monitoring.
- **Cloud-dependent** — Alerts require cloud-free imagery. Dense cloud cover (rainy season) causes detection gaps. SAR (Sentinel-1) helps but is not always available.
- **Minimum mapping unit** — DETER-Amazônia detects patches >3 ha (0.03 km²). Smaller clearings are missed (PRODES annual survey captures <3 ha patches).
- **No fire radiative power** — Burn scars are classified (CICATRIZ_DE_QUEIMADA) but active fire intensity is not provided. For fire hotspots, use INPE Queimadas (separate program).
- **WFS query limits** — GeoServer default is 50,000 features per request. Large time ranges may require paging.
- **No STAC** — OGC WFS only. Not compatible with STAC tooling (pystac-client, odc-stac).

## Integration Notes

**Recommended bridge pattern**: **Daily WFS poller**

1. **WFS GetFeature polling** — Every day, query `deter-amz:deter_public` (and other biomes) with `CQL_FILTER=view_date>=lastPollDate`.
2. **Delta detection** — Track latest `view_date` and `gid` in persistent state (SQLite or Kafka compacted topic). Emit only new alerts.
3. **Message groups** — One group per biome:
   - `deter_amazon_alerts` — keyed by `{gid}` (e.g., `123456`)
   - Subject: `inpe-deter/amazon/alert/{gid}`
   - Payload: Alert metadata (classname, view_date, sensor, area, county, uf, uc, ti, geometry)
4. **Deforestation types as reference data** — Emit a reference event for each `classname` at startup:
   - `deter_deforestation_types` — keyed by `{classname}` (e.g., `DESMATAMENTO_CR`)
   - Payload: Portuguese name, English translation, description
5. **Municipality/state lookup** — Emit Brazilian municipality and state metadata at startup (from IBGE or embedded in bridge):
   - `brazil_municipalities` — keyed by `{county}/{uf}`
   - Payload: Municipality name, state code, bbox, population, GDP, etc.

**Why not just expose WFS directly?** Kafka adds:
- **Durability** — Alerts persist in topic, historical replays possible
- **Ordering** — Time-series guarantees per municipality or grid cell
- **Fan-out** — Multiple consumers without re-polling WFS
- **Enrichment** — Bridge could pre-compute daily/weekly area statistics per state, protected area overlap %, or cumulative deforestation metrics

**Alternative**: For **fire hotspots**, add INPE Queimadas (`queimadas:focos` layer) to the same bridge. Fire hotspots are daily active fire detections from MODIS/VIIRS/NOAA-20.

## Verdict

**STRONG ACCEPT** — This is a **Tier-1 deforestation monitoring source** with **daily NRT alerts**, **operational authority** (Brazilian government enforcement), **multi-sensor fusion** (Sentinel-1/2, Landsat, CBERS, AMAZONIA-1), and **multi-biome coverage** (Amazon + Cerrado + Pantanal + Caatinga + Mata Atlântica).

The **open OGC WFS/WMS** interface is excellent for integration. The **rich attribution** (deforestation type, municipality, protected area, indigenous territory) makes this a valuable source for environmental monitoring, REDD+, carbon accounting, and illegal logging detection.

**Recommended as the primary deforestation alert source** for South America. Covers all Brazilian biomes (60% of South American forests). For **other tropical regions**, combine with:
- **Planet NICFI** (monthly 4.77m mosaics, global tropics)
- **Global Forest Watch** (annual tree cover loss, global)
- **Sentinel-2 change detection** (custom bridge, global)

Alternative: If **fire hotspots** are also needed, add INPE Queimadas (`queimadas:focos` WFS layer) to the same bridge. Fire + deforestation together provide comprehensive Brazilian environmental monitoring.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 3 | Daily deforestation alerts, multi-sensor fusion, authoritative for Brazil |
| Freshness | 3 | Daily updates, NRT detection (cloud-dependent) |
| Openness | 3 | Fully open, OGC WFS/WMS, no auth required |
| Schema clarity | 3 | Well-documented GeoJSON schema, rich attribution |
| Machine-readability | 3 | GeoJSON, GML, Shapefile, KML, CSV — all standard formats |
| Repo fit | 0 | Brazil-only (narrow geographic scope limits global repo utility) |
