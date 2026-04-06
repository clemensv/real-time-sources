# INPE Queimadas BDQueimadas — Fire Hotspot Database (API)

**Country/Region**: Brazil (national; all biomes) + South America
**Publisher**: INPE — Instituto Nacional de Pesquisas Espaciais
**API Endpoint**: `https://queimadas.dgi.inpe.br/queimadas/bdqueimadas/` (partially reachable)
**Documentation**: https://queimadas.dgi.inpe.br/queimadas/
**Protocol**: REST / WFS
**Auth**: None
**Data Format**: JSON, GeoJSON, CSV, KML, Shapefile
**Update Frequency**: Multiple times daily (satellite passes)
**License**: Brazilian government open data

## What It Provides

This document complements the existing inpe-queimadas-brazil.md with additional findings about the BDQueimadas (Fire Hotspot Database) API and the TerraBrasilis `queimadas` workspace.

### BDQueimadas API

The BDQueimadas portal provides a fire hotspot query interface. During testing, the direct API endpoint was unreachable:

```
https://queimadas.dgi.inpe.br/queimadas/bdqueimadas/api/focos?pais_id=33&satelite=AQUA_M-T → Connection failed
https://queimadas.dgi.inpe.br/queimadas/dados-abertos/apidoc/ → Connection failed
```

However, the BDQueimadas portal webpage loaded partially, confirming the system is operational.

### TerraBrasilis Fire Workspace

The TerraBrasilis GeoServer includes a `queimadas` workspace (confirmed in GetCapabilities):

```
xmlns:queimadas="queimadas.dgi.inpe.br"
xmlns:dashboard-fires="https://dashboard-fires.terrabrasilis.dpi.inpe.br"
```

These workspaces should be queryable via the same WFS pattern as DETER:
```
http://terrabrasilis.dpi.inpe.br/geoserver/queimadas/ows?
    service=WFS&version=2.0.0&
    request=GetFeature&typeName=queimadas:{layer_name}&
    count=3&outputFormat=application/json
```

(Layer names need to be discovered via GetCapabilities for the queimadas workspace specifically.)

### Context: Fire Season

Brazil's fire season (June-October in the Cerrado and Amazon) produces hundreds of thousands of fire hotspots annually. The 2019 Amazon fires and 2024 Pantanal fires were global news events. INPE's monitoring is the authoritative source for Brazilian fire data.

## Integration Notes

- Complements existing inpe-queimadas-brazil.md with WFS access path via TerraBrasilis
- The WFS approach avoids the BDQueimadas API availability issues
- Fire data via WFS would use the same adapter as DETER deforestation
- NASA FIRMS provides global fire data that includes Brazil — but INPE's data is more authoritative for Brazilian territory
- The queimadas and dashboard-fires workspaces on TerraBrasilis need further exploration

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Multiple satellite passes daily |
| Openness | 2 | BDQueimadas API unreachable; WFS path available via TerraBrasilis |
| Stability | 2 | INPE infrastructure; some endpoints down |
| Structure | 3 | WFS GeoJSON (same as DETER) |
| Identifiers | 2 | Satellite-specific hotspot IDs |
| Additive Value | 2 | Complements existing queimadas candidate + DETER |
| **Total** | **14/18** | |

## Verdict

✅ **Build** (integrate with DETER adapter) — The TerraBrasilis WFS path means fire data can be served through the same GeoServer adapter as DETER deforestation. Explore the queimadas workspace layers for fire hotspot polygons. This avoids the BDQueimadas API availability issues.
