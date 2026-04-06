# INPE TerraBrasilis DETER — Amazon & Cerrado Deforestation Alerts

**Country/Region**: Brazil (Amazon, Cerrado, Pantanal, Caatinga, Mata Atlântica, Pampa biomes)
**Publisher**: INPE — Instituto Nacional de Pesquisas Espaciais
**API Endpoint**: `http://terrabrasilis.dpi.inpe.br/geoserver/{workspace}/ows` (WFS)
**Documentation**: http://terrabrasilis.dpi.inpe.br/
**Protocol**: OGC WFS 2.0 (GeoServer)
**Auth**: None
**Data Format**: GeoJSON, GML, Shapefile
**Update Frequency**: Daily to weekly (satellite revisit cycle)
**License**: Brazilian government open data

## What It Provides

INPE's DETER (Real-Time Deforestation Detection System) is one of the most consequential environmental monitoring systems on Earth. It detects deforestation and forest degradation across Brazil's six biomes using satellite imagery (CBERS-4, Amazonia-1, Sentinel-2), producing polygon alerts for areas where vegetation cover has been removed or degraded.

The TerraBrasilis platform exposes this data through a standard OGC GeoServer instance with multiple WFS workspaces.

### Available Workspaces (confirmed via GetCapabilities)

| Workspace | Description |
|-----------|-------------|
| `deter-amz` | DETER Amazon deforestation alerts (445,966 features) |
| `deter-cerrado` | DETER Cerrado deforestation alerts (60,966 features) |
| `deter-pantanal-nb` | DETER Pantanal alerts |
| `deter-cerrado-nb` | DETER Cerrado new border |
| `prodes-amz` | PRODES Amazon (annual deforestation) |
| `prodes-cerrado` | PRODES Cerrado (annual) |
| `prodes-pantanal` | PRODES Pantanal |
| `prodes-caatinga` | PRODES Caatinga |
| `prodes-mata-atlantica` | PRODES Mata Atlântica |
| `prodes-pampa` | PRODES Pampa |
| `queimadas` | Fire/burned area monitoring |
| `dashboard-fires` | Fire dashboard data |

## API Details

Standard OGC WFS 2.0 queries. Examples:

### DETER Amazon (most recent alerts)
```
GET http://terrabrasilis.dpi.inpe.br/geoserver/deter-amz/ows?
    service=WFS&version=2.0.0&
    request=GetFeature&
    typeName=deter-amz:deter_amz&
    count=3&
    outputFormat=application/json
```

Response (verified live 2026-04-06):

```json
{
  "type": "FeatureCollection",
  "totalFeatures": 445966,
  "numberMatched": 445966,
  "numberReturned": 3,
  "features": [
    {
      "type": "Feature",
      "id": "deter_amz.fid-...",
      "geometry": {
        "type": "MultiPolygon",
        "coordinates": [[[[-55.6564,-1.4401], ...]]]
      },
      "properties": {
        "gid": "100003_hist",
        "classname": "DESMATAMENTO_CR",
        "path_row": "169105",
        "view_date": "2018-01-14",
        "sensor": "AWFI",
        "satellite": "CBERS-4",
        "areamunkm": 0.1017,
        "municipality": "obidos",
        "uf": "PA",
        "publish_month": "2018-01-01"
      }
    }
  ]
}
```

### DETER Cerrado
```
GET http://terrabrasilis.dpi.inpe.br/geoserver/deter-cerrado/ows?
    service=WFS&version=2.0.0&
    request=GetFeature&
    typeName=deter-cerrado:deter_cerrado&
    count=3&
    outputFormat=application/json
```

Also verified working with 60,966 features.

### CQL Filtering for Recent Alerts

WFS supports CQL_FILTER for temporal queries:
```
&CQL_FILTER=view_date>='2026-03-01'
```

This is critical for polling — request only new alerts since last check.

### GetCapabilities
```
GET http://terrabrasilis.dpi.inpe.br/geoserver/wfs?
    service=WFS&version=2.0.0&
    request=GetCapabilities
```

Returns full service description with all available layers.

## Entity Model

- **Feature type**: MultiPolygon (deforestation area boundary)
- **classname**: Alert classification — `DESMATAMENTO_CR` (clear-cut), `DEGRADACAO` (degradation), `MINERACAO` (mining), `CS_DESORDENADO` (unordered regrowth)
- **view_date**: Satellite observation date
- **satellite**: CBERS-4, Amazonia-1, etc.
- **sensor**: AWFI (wide-field), WFI, MSI
- **areamunkm**: Area in square kilometers
- **municipality**: Brazilian municipality name
- **uf**: Brazilian state code (PA = Pará, MT = Mato Grosso, etc.)
- **publish_month**: Publication month

## Freshness Assessment

DETER produces alerts based on satellite revisit cycles (typically 3-5 days for CBERS-4). New alerts are published within days of satellite acquisition. The `view_date` field enables tracking of when deforestation was observed. The total feature count (445K for Amazon) includes historical data back to 2015+. Polling with CQL temporal filters yields recent alerts efficiently.

## Integration Notes

- This is arguably the most environmentally consequential real-time dataset in the world — DETER alerts trigger law enforcement operations against illegal deforestation in the Amazon
- The GeoServer WFS is a standard OGC service, enabling use of any WFS client library
- CQL_FILTER support allows efficient temporal polling (only fetch new alerts)
- GeoJSON output is standard and integrates directly with mapping tools
- Multiple biomes can be monitored from the same GeoServer instance
- CloudEvents mapping: each new deforestation polygon becomes one CloudEvent
- **PRODES vs DETER**: PRODES is annual (higher resolution, authoritative); DETER is near-real-time (lower resolution, alerting). Both are available
- The `queimadas` workspace provides fire/burned area data — complementary to the existing inpe-queimadas-brazil.md candidate

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Daily-weekly satellite alerts; CQL temporal filtering |
| Openness | 3 | No auth, standard OGC WFS, government open data |
| Stability | 3 | INPE GeoServer has been operational for years; WFS is a standard |
| Structure | 3 | Standard GeoJSON with consistent attribute schema |
| Identifiers | 2 | Feature IDs are GeoServer-generated; gid provides stable reference |
| Additive Value | 3 | Amazon deforestation monitoring — globally significant dataset |
| **Total** | **17/18** | |

## Verdict

✅ **Build** — This is a high-priority source. The Amazon deforestation data is globally significant, the API is standard OGC WFS (zero proprietary complexity), and it requires no authentication. The GeoServer instance serves multiple biomes from one endpoint. A generic WFS adapter could serve all DETER and PRODES layers. The CQL temporal filter support makes polling efficient. This is INPE's crown jewel data service.
