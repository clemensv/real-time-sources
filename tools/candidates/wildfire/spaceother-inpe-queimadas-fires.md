# INPE Queimadas (Brazil Fire Hotspot Monitoring)

- **Country/Region**: Brazil + global (INPE-operated)
- **Endpoint**: `https://terrabrasilis.dpi.inpe.br/geoserver/wfs` (WFS layer `queimadas:focos`)
- **Protocol**: WFS 2.0, WMS, REST (GeoJSON)
- **Auth**: None (fully open)
- **Format**: GeoJSON, CSV, Shapefile, KML
- **Freshness**: Near-real-time (~3-6 hours, updated every 10 minutes)
- **Docs**: https://queimadas.dgi.inpe.br/, http://www.inpe.br/queimadas/
- **Score**: 16/18

## Overview

INPE Queimadas (Programa de Monitoramento de Queimadas / Fire Monitoring Program) provides **near-real-time fire hotspot detection** for Brazil and globally using **MODIS, VIIRS, NOAA-20, NPP-Suomi, GOES-16, and Meteosat** satellites.

The program publishes **active fire detections** (thermal anomalies) via **OGC WFS/WMS** services integrated with the TerraBrasilis platform. Each hotspot includes detection timestamp, satellite source, confidence level, fire radiative power (FRP), and geocoded coordinates.

**Key features**:
- **NRT latency** (~3-6 hours after satellite overpass)
- **Multi-sensor fusion** (MODIS + VIIRS + GOES-16 + Meteosat)
- **Daily updates** (new hotspots every 10 minutes)
- **Brazil focus** but **global coverage** (MODIS/VIIRS data is worldwide)
- **Fire radiative power (FRP)** included (fire intensity metric)

**Data sources**:
- **AQUA/TERRA MODIS** — 1km resolution, 4× daily overpasses
- **NPP-Suomi / NOAA-20 VIIRS** — 375m resolution, 2× daily overpasses
- **GOES-16** — Geostationary, hourly for South America
- **Meteosat** — Geostationary, hourly for Africa/Europe

## Endpoint Analysis

**WFS service verified** — `https://terrabrasilis.dpi.inpe.br/geoserver/wfs` layer `queimadas:focos`

**Example: Query fire hotspots in last 24 hours (Amazon)**
```
GET https://terrabrasilis.dpi.inpe.br/geoserver/wfs?service=WFS&version=2.0.0&request=GetFeature&typeName=queimadas:focos&outputFormat=application/json&CQL_FILTER=datahora>=2024-01-14 AND datahora<=2024-01-15 AND BBOX(geom,-70,-10,-60,-5)
```

Returns GeoJSON:
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "id": "focos.123456",
      "geometry": {
        "type": "Point",
        "coordinates": [-62.5, -8.3]
      },
      "properties": {
        "id": 123456,
        "lat": -8.3,
        "lon": -62.5,
        "datahora": "2024-01-15T14:23:00",
        "satelite": "AQUA_M-T",
        "pais": "Brasil",
        "estado": "Amazonas",
        "municipio": "Lábrea",
        "bioma": "Amazônia",
        "precipitacao": 0.0,
        "diasemchuva": 15,
        "frp": 45.2,
        "riscofogo": "crítico"
      }
    }
  ]
}
```

**Field definitions**:
- `id` — Unique hotspot ID
- `datahora` — Detection timestamp (YYYY-MM-DD HH:MM:SS)
- `satelite` — Satellite source (AQUA_M-T, NPP-375, NOAA20-375, GOES-16, MSG-03)
- `lat` / `lon` — Coordinates (WGS84)
- `pais` / `estado` / `municipio` / `bioma` — Country, state, municipality, biome
- `precipitacao` — Precipitation (mm, last 24h)
- `diasemchuva` — Days without rain
- `frp` — Fire Radiative Power (MW, fire intensity)
- `riscofogo` — Fire risk level (baixo, médio, alto, crítico)

**Stable identifiers**: Hotspot `id` is unique. Keyed by `{id}` or `{date}/{satellite}/{lat}/{lon}`.

## Why Strong

1. **NRT latency** — 3-6 hours, updated every 10 minutes. True real-time fire monitoring.
2. **Multi-sensor fusion** — MODIS + VIIRS + GOES-16 + Meteosat (best available global fire detection).
3. **Fire radiative power (FRP)** — Fire intensity metric enables severity classification.
4. **Brazil-focused attribution** — State, municipality, biome, precipitation, days-without-rain, fire risk level.
5. **Fully open** — OGC WFS/WMS, no auth, GeoJSON/CSV/Shapefile export.
6. **Global coverage** — MODIS/VIIRS data is worldwide (not just Brazil).

## Limitations

- **Point data only** — Hotspots are geocoded pixels (1km or 375m), not burn perimeters (use DETER for burn scars).
- **False positives** — Industrial heat sources, gas flares, volcanoes may trigger detections (filter by `riscofogo`).
- **Cloud occlusion** — Hotspots not detected under clouds (optical sensors only).
- **Duplicate detections** — Same fire may be detected by multiple satellites (requires deduplication).

## Integration Notes

**Pattern**: **WFS poller** (every 10-30 minutes)

1. Query WFS with `CQL_FILTER=datahora>=lastPollTime`
2. Extract new hotspots
3. Emit to Kafka

**Message groups**:
- `inpe_fire_hotspots` — keyed by `{id}` (unique hotspot ID)
- Subject: `inpe-queimadas/hotspot/{id}`
- Payload: All hotspot attributes (timestamp, satellite, coords, FRP, municipality, biome, fire risk)

**Reference data**:
- Brazilian biomes (Amazon, Cerrado, Pantanal, Caatinga, Mata Atlântica) — emit at startup
- Satellite metadata (MODIS, VIIRS, GOES-16, Meteosat specs) — emit at startup

## Verdict

**STRONG ACCEPT** — This is a **Tier-1 fire monitoring source** with **NRT latency** (3-6 hours), **multi-sensor fusion**, and **operational authority** (Brazilian government environmental monitoring). The **FRP metric** and **rich attribution** (municipality, biome, precipitation, fire risk) make this excellent for wildfire risk modeling and disaster response.

**Recommended as the primary fire hotspot source** for South America. For **global coverage**, combine with:
- **NASA FIRMS** (MODIS/VIIRS, global, similar data source but different portal)
- **Copernicus EFFIS** (Europe fire monitoring)

INPE Queimadas has **better attribution** (Brazilian municipality/biome/fire risk) than NASA FIRMS for South America.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 3 | NRT fire hotspots, multi-sensor (MODIS/VIIRS/GOES/Meteosat), FRP included |
| Freshness | 3 | 3-6h latency, updated every 10 minutes (true NRT) |
| Openness | 3 | Fully open, OGC WFS/WMS, no auth |
| Schema clarity | 3 | Well-documented GeoJSON schema, rich attribution |
| Machine-readability | 3 | GeoJSON, CSV, Shapefile, KML — all standard formats |
| Repo fit | 1 | WFS polling required (not REST/STAC), but excellent data |
