# Wildfire Data Feeds: Portugal, Greece, Italy

Research conducted by probing live endpoints. Last updated: April 2026.

---

## 🇵🇹 PORTUGAL

### 1. Fogos.pt API — Community Fire Tracker

The Fogos.pt project is the most accessible real-time wildfire API for Portugal. It
scrapes data from ANEPC (Autoridade Nacional de Emergência e Proteção Civil) and
repackages it as a clean REST API. Open source, run by the community, and actively
maintained.

| Property | Value |
|---|---|
| **Base URL** | `https://api.fogos.pt/` |
| **Framework** | Lumen 8.3.4 (Laravel PHP) |
| **Source Code** | https://github.com/FogosPT/fogosapi (Apache 2.0) |
| **Auth** | Transitioning to token-based auth (`FOGOS-PT-AUTH` header). Some v1 endpoints still open, but rate-limited aggressively (HTTP 429). |
| **Data Source** | ANEPC (Portuguese civil protection) |
| **Update Frequency** | Real-time, every 2–10 minutes |
| **Coverage** | Portugal Continental + Madeira |
| **Formats** | JSON, KML |
| **License** | Apache 2.0 (code); data sourced from public ANEPC feeds |

#### Confirmed Working Endpoints (v1 — Legacy, partially open)

```
GET /v1/now
  → {"success":true,"data":{"date":"12:16","total":2,"cars":16,"aerial":2,"man":52}}
  Summary: current active fire count + deployed resources (vehicles, aerial, personnel)

GET /v1/now/data
  → JSON array of timestamped snapshots throughout the day
  Fields: aerial, man, terrain, total, label (time)

GET /v1/warnings
  → JSON array of road-closure / fire warnings with dates and text
  Real alert data — "A1 cortada entre o nó de Aveiro sul e nó de albergaria devido a incêndio"

GET /v1/stats
  → Text summary: "Desde as 00:00 de hoje registamos 20 ocorrências de incêndios. Setúbal - 2, Porto - 2..."

GET /v1/risk
  → Fire risk text for queried location
```

#### Documented Endpoints (v1 — from source code, may require auth)

```
GET /v1/active              → Active fires
GET /v1/aerial              → Aerial resources deployed
GET /v1/status              → System status
GET /v1/risk-today          → Today's fire risk
GET /v1/risk-tomorrow       → Tomorrow's fire risk
GET /v1/risk-after          → Day-after-tomorrow risk
GET /v1/list                → List by concelho (municipality)
GET /v1/stats/8hours        → Stats for last 8 hours
GET /v1/stats/today         → Today's statistics
GET /v1/stats/yesterday     → Yesterday's statistics
GET /v1/stats/week          → Weekly statistics
GET /v1/stats/burn-area     → Burned area last days
GET /v1/stats/motive        → Fire motives this month
```

#### Documented Endpoints (v2 — from source code, likely requires auth)

```
GET /v2/incidents/active     → Active incidents (JSON)
GET /v2/incidents/active/kml → Active incidents (KML)
GET /v2/incidents/search     → Search incidents
GET /v2/incidents/{id}/kml   → KML for specific incident
GET /v2/incidents/1000ha-burned → Fires >1000ha

GET /v2/weather/thunders     → Lightning data
GET /v2/weather/stations     → Weather stations
GET /v2/weather/daily        → Daily weather

GET /v2/rcm/today            → Fire risk map today
GET /v2/rcm/tomorrow         → Fire risk map tomorrow
GET /v2/rcm/after            → Fire risk map day after
GET /v2/rcm/parish           → Risk by parish

GET /v2/planes/{icao}        → Aerial firefighting aircraft tracking
```

#### Auth Transition Notice

Fogos.pt is moving all API access behind mandatory authentication. Requirements:
- `FOGOS-PT-AUTH: {token}` header
- Custom User-Agent
- Source IP declaration
- Formal access request via web form

---

### 2. ICNF GIS Services — Official Government Fire Data

The Instituto da Conservação da Natureza e das Florestas runs ArcGIS Server
services with historical burned area data, fire severity, and fire defense data.

| Property | Value |
|---|---|
| **Base URL** | `https://sigservices.icnf.pt/server/rest/services/` |
| **Portal** | `https://sig.icnf.pt/portal/` |
| **Technology** | ArcGIS Server 11.5 |
| **Auth** | Public for DFCI folder; token required for GIFR folder |
| **Coverage** | Portugal Continental |
| **Formats** | JSON, GeoJSON, Shapefile, CSV, GeoPackage (export) |
| **Spatial Reference** | EPSG:3763 (PT-TM06/ETRS89) |

#### Available DFCI Services (Public, No Auth)

```
Service catalog:
GET https://sigservices.icnf.pt/server/rest/services/DFCI?f=json

Services:
  DFCI/GIFR_AArdidas_IndicadorRetorno/MapServer
    → Burned area return-period indicator, 1975–2019
    → Fields: frequency, years burned, last fire year, mean return interval,
      fire causes, land use (COS 2018), fuel models
    → Tags: GIFR, Incêndios, fogos, Retorno

  DFCI/HistoricoAreasArdidas/MapServer
    → Historic burned areas — raster layers:
      Layer 0: "Eixos de Propagação" (fire spread axes)
      Layer 1: "Locais de Paragem" (stopping locations)
    → Keywords: Áreas Ardidas, DFCI, Histórico de incêndios

  DFCI/DFCI_Severidade/FeatureServer
    → Fire severity based on Sentinel-2 RdNBR/dNBR
    → Classification: 5 severity classes (Low → Extreme)
    → Fields: Legenda, Classe, Cod_SGIF, Area_ha, Id_REE, Ano
    → Supports export: sqlite, filegdb, shapefile, csv, geojson

  DFCI/DFCI_PMDFCI_ext/FeatureServer + MapServer
    → Municipal fire defense plans (Planos Municipais de Defesa da Floresta)

  DFCI/SF_RegistoAtividadeDiaria/FeatureServer + MapServer
    → Forest sappers daily activity log
```

#### Example Query

```
# Get fire severity features as GeoJSON
GET https://sigservices.icnf.pt/server/rest/services/DFCI/DFCI_Severidade/FeatureServer/0/query?where=1=1&outFields=*&f=geojson&resultRecordCount=5
```

#### GIFR Folder (Requires Token)

```
GET https://sigservices.icnf.pt/server/rest/services/GIFR?f=json
  → {"error":{"code":499,"message":"Token Required"}}
```

The GIFR application at `https://geocatalogo.icnf.pt/geovisualizador/gifr` embeds a
WebApp from `https://sig.icnf.pt/portal/apps/webappviewer/` — the underlying service
data may be accessible with a portal token.

---

### 3. dados.gov.pt — Portugal Open Data Portal

| Property | Value |
|---|---|
| **API** | `https://dados.gov.pt/api/1/datasets/?q=...` |
| **Format** | JSON (CKAN-compatible API) |
| **Auth** | None for read |

#### Relevant Datasets Found

| Dataset | Org | Format | License | Update |
|---|---|---|---|---|
| Incêndios Florestais | CM Cascais | DXF, GeoJSON | CC-0 | Occasional |
| Áreas Ardidas 2012–2021 | CM Águeda | GeoPackage, GeoJSON | CC-0 | Annual |
| Crimes de incêndio florestal | DGPJ (Justice) | CSV, XLSX, XML | CC-BY-SA | Annual |

These are municipal or sectoral datasets — there is no single national-level real-time
fire dataset on dados.gov.pt. The ICNF publishes its data through its own GIS portal
rather than the open data portal.

---

### 4. ANEPC / prociv.pt — Civil Protection

The ANEPC website (`prociv.pt` / `prociv.gov.pt`) is the authoritative source for
real-time fire incidents in Portugal. However:

- The site uses client-side JavaScript rendering (SPA)
- Direct HTTP fetches return connection errors or empty pages
- The underlying data feed is what Fogos.pt scrapes and republishes
- No documented public API exists

---

## 🇬🇷 GREECE

### 1. BEYOND/NOA FireHub — Satellite Fire Detection

The BEYOND Center of Excellence at the National Observatory of Athens operates
FireHub, a real-time fire monitoring service based on METEOSAT SEVIRI satellite data
and high-resolution EOS (Sentinel, MODIS/VIIRS) observations.

| Property | Value |
|---|---|
| **Web App** | `https://firehub.beyond-eocenter.eu/` |
| **Provider** | National Observatory of Athens (NOA), IAASARS |
| **Contact** | kontoes@noa.gr |
| **Auth** | **None** — fully public |
| **Coverage** | Greece (22.4°E–27.9°E, 34.9°N–39.5°N) |
| **Update Frequency** | Near real-time (~5–15 min for SEVIRI) |
| **License** | No explicit license stated; public government research data |

#### PHP Data API

```
GET https://firehub.beyond-eocenter.eu/php/fhubdb.php
  Parameters:
    mode=rt            (real-time mode)
    start=ISO_DATETIME (e.g., 2025-08-01T00:00:00)
    stop=ISO_DATETIME  (e.g., 2025-08-05T00:00:00)

Response JSON:
{
  "status": 0,
  "args": {"start": "...", "stop": "..."},
  "events": [
    [fire_id, pixel_count, "SEVIRI", "Municipality_Name",
     "start_datetime", "end_datetime", duration_hours,
     longitude, latitude],
    ...
  ],
  "eosevents": [...],
  "timestamps": { "datetime": [[fire_ids], null], ... }
}
```

**Sample event data** (August 2025):

| fire_id | pixels | sensor | municipality | start | end | hours | lon | lat |
|---|---|---|---|---|---|---|---|---|
| 9328 | 2685 | SEVIRI | Δ. Φαιστού | 2025-08-01 10:10 | 2025-08-01 11:55 | 1.83 | 24.808 | 34.958 |
| 9331 | 761 | SEVIRI | Δ. Ανδραβίδας-Κυλλήνης | 2025-08-01 11:15 | 2025-08-01 14:25 | 3.25 | 21.380 | 37.946 |
| 9345 | 438 | SEVIRI | Δ. Ωρωπού | 2025-08-04 10:55 | 2025-08-04 11:50 | 1.0 | 23.670 | 38.318 |

#### GeoServer WFS — OGC Standard Access

```
WFS Capabilities:
GET https://firehub-geoserver.beyond-eocenter.eu/geoserver/firehub/wfs?service=WFS&version=2.0.0&request=GetCapabilities

GeoServer Version: 2.7.1
Provider: National Observatory of Athens
Access Constraints: NONE
Fees: NONE
```

**Feature Types available:**

| Layer Name | Description |
|---|---|
| `firehub:seviri` | Real-time SEVIRI hotspot detections (MultiPolygon) |
| `firehub:fires_view` | Aggregated fire events view |
| `firehub:events_view` | Individual detection events |
| `firehub:propagation` | Fire propagation/spread data |
| `firehub:seviri_range` | SEVIRI detection range data |
| `firehub:hr_sat_raw` | High-resolution satellite raw detections |
| `firehub:hr_sat_refined` | High-resolution satellite refined detections |
| `firehub:geotags_view` | Geotagged observations |
| `firehub:bsm_fire_ref` | Burned Scar Mapping reference |
| `firehub:natura2000_view` | Natura 2000 protected areas overlay |
| `firehub:urbanatlas_view` | Urban Atlas overlay |

**Output formats:** JSON, GeoJSON, KML, CSV, GML 2/3, Shapefile (SHAPE-ZIP)

#### Example WFS Query

```
# Get latest SEVIRI hotspots as GeoJSON
GET https://firehub-geoserver.beyond-eocenter.eu/geoserver/firehub/wfs?service=WFS&request=GetFeature&typeName=firehub:seviri&maxFeatures=5&outputFormat=application/json

Sample feature:
{
  "type": "Feature",
  "id": "seviri.fid-...",
  "geometry": { "type": "MultiPolygon", "coordinates": [...] },
  "properties": {
    "id": 340371,
    "fe_id": 9482,
    "timestamp": "2025-10-11T11:30:00Z",
    "conf": 0.5
  }
}
```

#### Tile Services

```
Land Cover:  https://firehub-tilestream.beyond-eocenter.eu/v2/clc_00/{z}/{x}/{y}.png
Admin Names: https://firehub-tilestream.beyond-eocenter.eu/v2/admin_over/{z}/{x}/{y}.png
```

---

### 2. Greek Civil Protection / Open Data

| Endpoint | Status |
|---|---|
| `civilprotection.gr` | HTTP 403 Forbidden |
| `geodata.gov.gr` | Connection failed |

No accessible machine-readable fire data feeds were found from these sources.
The BEYOND/NOA FireHub is the primary publicly accessible fire data service for Greece.

---

## 🇮🇹 ITALY

### 1. Protezione Civile GitHub (pcm-dpc)

The Dipartimento della Protezione Civile publishes open data on GitHub, following
the pattern established with their widely-used COVID-19 dataset.

| Property | Value |
|---|---|
| **GitHub Org** | https://github.com/pcm-dpc (26 repos, verified domain) |
| **License** | CC-BY-4.0 (data), EUPL-1.2 (code) |
| **Auth** | None (public GitHub repos) |
| **Format** | Git-hosted files (JSON, CSV, GeoJSON varies by repo) |

#### Fire-Related Repositories

**pcm-dpc/propagator** — Wildfire Spread Simulator
- Operational cellular-automata wildfire propagation model
- Developed by CIMA Research Foundation
- Python + Numba, CLI + programmatic API
- Inputs: DEM, fuel maps, wind, moisture
- License: EUPL-1.2
- Not a data feed, but an operational tool used by DPC

**pcm-dpc/DPC-Bollettini-Criticita-Idrogeologica-Idraulica** — Daily Risk Bulletins
- Hydro-geological/hydraulic criticality bulletins
- Published daily by 16:00 UTC
- Covers 156 alert zones across Italy
- Includes severe weather that affects fire conditions
- License: CC-BY-4.0
- Updated: actively (last commit April 2026)

**pcm-dpc/DPC-Bollettini-Vigilanza-Meteorologica** — Daily Weather Bulletins
- Meteorological vigilance bulletins (significant weather)
- Published daily by 15:00 UTC
- 3-day forecasts (today, tomorrow, trend for day after)
- License: CC-BY-4.0

**pcm-dpc/DPC-Mappe** — Open Data Maps
- Repository for map content published by DPC
- License: CC-BY-4.0

#### No Dedicated Wildfire Data Feed

Italy's wildfire data is managed by the Corpo Nazionale dei Vigili del Fuoco
(fire brigades) and regional forestry services (formerly Corpo Forestale,
now Carabinieri Forestali). Unlike Portugal's ANEPC feed or Greece's SEVIRI-based
system, there is **no single national wildfire incident API** published by DPC.

The GitHub repos focus on hydro-meteorological risk. The `propagator` tool is a
simulation engine, not a data feed.

---

### 2. Protezione Civile Web Portals

| Endpoint | Status | Notes |
|---|---|---|
| `protezionecivile.gov.it` | Returns "Loading..." | SPA, no machine-readable API found |
| `protezionecivile.it` | Returns "Loading..." | Same |
| `rischi.protezionecivile.gov.it` | Returns "Loading..." | Risk portal, SPA-rendered |
| `mappe.protezionecivile.gov.it` | Returns "Loading..." | Map portal, SPA-rendered |
| `servizio-nazionale.protezionecivile.gov.it` | Returns "Loading..." | National service portal |
| `sit.protezionecivile.it` | Error page | GIS portal unavailable |
| `dati.protezionecivile.it` | HTTP 403 | Open data portal blocked |

All Italian government portals use heavy client-side rendering (Angular/React SPAs)
and are not accessible via simple HTTP requests. They likely have internal APIs
powering the SPAs, but these are undocumented.

---

## Summary Comparison

| Dimension | 🇵🇹 Portugal | 🇬🇷 Greece | 🇮🇹 Italy |
|---|---|---|---|
| **Best Source** | Fogos.pt API + ICNF GIS | BEYOND/NOA FireHub | pcm-dpc GitHub repos |
| **Real-time Fires** | ✅ Fogos.pt (via ANEPC) | ✅ FireHub SEVIRI (~5 min) | ❌ No public feed |
| **Historical Data** | ✅ ICNF (1975–2019) | ✅ FireHub archive | ⚠️ Bulletins only |
| **API Type** | REST JSON | PHP JSON + OGC WFS | GitHub raw files |
| **Auth Required** | ⚠️ Transitioning to tokens | ❌ None | ❌ None |
| **OGC Standards** | ArcGIS REST | WFS 2.0, WMS | None |
| **Open Source** | ✅ Apache 2.0 | ❌ Closed | ✅ EUPL-1.2 (tools) |
| **Data License** | CC-0/CC-BY-SA (portal) | Unstated | CC-BY-4.0 |
| **Fire Simulator** | ❌ | ❌ | ✅ PROPAGATOR |
| **Machine-Readable** | ✅ Excellent | ✅ Excellent | ⚠️ Limited |

### Integration Recommendations

1. **Portugal**: Use Fogos.pt API for real-time data (apply for auth token). Use ICNF
   ArcGIS services for historical analysis and severity data. Watch the auth transition.

2. **Greece**: FireHub is the clear winner — both the PHP API for event data and the
   GeoServer WFS for spatial queries are open, well-structured, and actively maintained.
   This is the most integration-friendly source of the three countries.

3. **Italy**: The most challenging. No real-time wildfire API exists publicly. The GitHub
   repos provide valuable meteorological risk bulletins. For actual fire incident data,
   you would need to negotiate with Vigili del Fuoco or regional authorities. The
   PROPAGATOR simulator could be useful for fire spread modeling.
