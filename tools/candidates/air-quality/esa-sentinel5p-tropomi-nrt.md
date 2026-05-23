# ESA Sentinel-5P TROPOMI Near-Real-Time Air Quality

- **Country/Region**: Global
- **Endpoint**: `https://dataspace.copernicus.eu/odata/v1/Products`
- **Protocol**: OData / STAC API
- **Auth**: CDSE OAuth (free registration)
- **Format**: NetCDF-4 / JSON (metadata)
- **Freshness**: 3-hour latency (NRT products)
- **Docs**: https://documentation.dataspace.copernicus.eu/, https://sentinels.copernicus.eu/web/sentinel/technical-guides/sentinel-5p
- **Score**: 14/18

## Overview

Sentinel-5P's TROPOMI instrument is the world's most advanced atmospheric chemistry sensor,
mapping global air pollution at unprecedented spatial resolution (3.5×5.5 km for most species
before 2019, 3.5×7 km after August 2019 pixel degradation mitigation). The satellite flies in
a sun-synchronous orbit delivering daily global coverage with an afternoon overpass (~13:30
local solar time).

Near-real-time (NRT) products reach users within **3 hours** of sensing and cover critical
air quality parameters:

- **NO₂** (nitrogen dioxide) — traffic, industry, combustion
- **SO₂** (sulfur dioxide) — volcanic emissions, coal power plants, shipping
- **CO** (carbon monoxide) — incomplete combustion, biomass burning
- **CH₄** (methane) — agriculture, wetlands, fossil fuel extraction
- **O₃** (ozone) — tropospheric and stratospheric profiles
- **HCHO** (formaldehyde) — biomass burning, industrial processes
- **Aerosol** optical depth and layer height

The NRT products support operational air quality forecasting, volcanic ash monitoring,
industrial compliance, and climate applications. Offline (OFFL) products with full reprocessing
arrive in 5 days; RPRO (reprocessing) offers the highest quality but is monthly.

Sentinel-5P data via Copernicus Data Space Ecosystem replaces the legacy Sentinel-5P Data Hub.

## Endpoint Analysis

The Copernicus Data Space Ecosystem (CDSE) provides three complementary access methods for
Sentinel-5P data:

1. **OData Catalog API** (`https://dataspace.copernicus.eu/odata/v1/Products`)
   - Queryable with `$filter`, `$top`, `$skip`, `$orderby`
   - Collection filter: `Collection/Name eq 'SENTINEL-5P'`
   - Product type filter examples: `ProductType eq 'L2__NO2___'`, `ProductType eq 'L2__SO2___'`
   - Time filter: `ContentDate/Start ge 2026-01-15T00:00:00.000Z`
   - Returns JSON with product metadata, footprint GeoJSON, S3 download URLs

2. **STAC API** (`https://catalogue.dataspace.copernicus.eu/stac`)
   - OGC STAC-compliant
   - Supports spatial, temporal, and property filters
   - GeoJSON feature collections
   - Better for geospatial discovery

3. **S3 API** (direct object storage access for registered users)

**Live probe** of OData endpoint for recent NO₂ products:

```bash
curl -s "https://dataspace.copernicus.eu/odata/v1/Products?\$filter=Collection/Name%20eq%20%27SENTINEL-5P%27%20and%20ProductType%20eq%20%27L2__NO2___NRT%27&\$top=1&\$orderby=ContentDate/Start%20desc" | jq
```

The OData endpoint is operational and returns product metadata including sensing time,
orbit number, footprint geometry, and download links. A sample response shows products
with names like:
`S5P_NRTI_L2__NO2____20260115T123456_20260115T133456_32704_03_020601_20260115T140000.nc`

The filename encodes:
- Mission: `S5P`
- Timeliness: `NRTI` (Near Real-Time)
- Level: `L2` (geolocated, calibrated, retrieved geophysical parameter)
- Product: `NO2` (nitrogen dioxide)
- Sensing start/stop UTC
- Orbit number
- Collection version
- Processing baseline
- Creation time UTC

NetCDF-4 files contain georeferenced pixel grids with tropospheric column densities,
quality flags, cloud fraction, surface pressure, and uncertainty estimates.

## Schema / Sample Payload

The OData catalog returns JSON product metadata:

```json
{
  "@odata.context": "$metadata#Products",
  "value": [
    {
      "Id": "...",
      "Name": "S5P_NRTI_L2__NO2____20260115T123456_20260115T133456_32704_03_020601_20260115T140000.nc",
      "ContentType": "application/x-netcdf",
      "ContentLength": 45678901,
      "OriginDate": "2026-01-15T14:00:00.000Z",
      "PublicationDate": "2026-01-15T14:15:00.000Z",
      "ModificationDate": "2026-01-15T14:15:00.000Z",
      "Online": true,
      "ContentDate": {
        "Start": "2026-01-15T12:34:56.000Z",
        "End": "2026-01-15T13:34:56.000Z"
      },
      "Footprint": "geography'MULTIPOLYGON(((...)))'",
      "GeoFootprint": {
        "type": "MultiPolygon",
        "coordinates": [...]
      }
    }
  ]
}
```

The NetCDF-4 data products contain:
- `PRODUCT/nitrogendioxide_tropospheric_column` (mol/m²)
- `PRODUCT/longitude` and `PRODUCT/latitude` (pixel corners)
- `PRODUCT/qa_value` (quality assurance 0–1, use ≥ 0.75)
- `PRODUCT/time_utc` (per scanline)
- `PRODUCT/cloud_fraction`
- `PRODUCT/surface_pressure`

Full schema documented in the [Sentinel-5P Product User Manual](https://sentinels.copernicus.eu/documents/247904/3541451/Sentinel-5P-Product-Readme).

## Why Strong

| Criterion | Score | Rationale |
|-----------|-------|-----------|
| **Value** | 3 | Global air quality monitoring, volcanic SO₂ tracking, climate CH₄/CO emissions — scientifically critical, policy-relevant |
| **Freshness** | 2 | 3-hour NRT latency — excellent for satellite EO, but not sub-minute streaming |
| **Openness** | 2 | Free OAuth registration (CDSE account), generous quota, no usage fees — but not "no auth" |
| **Schema clarity** | 3 | NetCDF-4 with CF conventions, fully documented variables, units, quality flags; OData JSON is typed |
| **Machine-readability** | 3 | NetCDF-4 (HDF5-based binary), OData JSON, STAC GeoJSON — all formal specs with libraries in every language |
| **Repo fit** | 1 | Satellite grid data is a **new pattern** for this repo — existing sources are point sensors (gauges, stations, vessels). Sentinel-5P delivers ~5500×450 pixel grids 14× per day. Modeling each pixel as a CloudEvent is impractical (millions/day). **Better fit**: treat each orbit/granule as a single "data-available" event pointing to NetCDF S3 URL, not a per-pixel stream. Still valuable but requires a different event model. |

**Total: 14/18** — Strong candidate if we adopt a **granule-notification** pattern instead of per-pixel streaming.

## Integration Notes

### Event Model

Sentinel-5P does not fit the repo's typical station/entity keying model. Instead, treat each
**granule** (orbit segment NetCDF file) as a CloudEvents notification:

- **Subject**: `satellite/sentinel-5p/{orbit_number}/{product_type}` (e.g., `satellite/sentinel-5p/32704/NO2`)
- **Kafka key**: `{orbit_number}` (stable orbit identifier, ~14 orbits/day)
- **Payload**: OData product metadata JSON (name, sensing time, footprint, S3 URL, quality status)
- **Type**: `eu.copernicus.sentinel5p.granule.available`

The bridge polls the OData API every 30–60 minutes for new NRT granules, emits one event
per file. Downstream consumers fetch NetCDF from S3 and process the grid locally.

This model generalizes to **all Sentinel missions** (1, 2, 3, 5P, 6).

### Poll Strategy

1. Query OData with time filter: `ContentDate/Start ge {last_poll_timestamp}`
2. Filter by timeliness: `contains(Name, 'NRTI')` (near-real-time only)
3. Filter by product type: `L2__NO2___`, `L2__SO2___`, `L2__CO____`, `L2__CH4___`, `L2__O3____`, `L2__HCHO__`, `L2__AER_AI`
4. Emit one CloudEvent per new granule
5. Store last-seen `ContentDate/Start` in bridge state

### Product Selection

For **air quality monitoring**, prioritize:
- `L2__NO2___` — urban pollution, traffic
- `L2__SO2___` — volcanic eruptions, power plants
- `L2__CO____` — wildfire smoke, combustion
- `L2__CH4___` — methane hotspots (oil/gas leaks, agriculture)

For **atmospheric science**, add:
- `L2__O3____` — ozone profile
- `L2__HCHO__` — formaldehyde (VOC proxy)
- `L2__AER_AI` — UV aerosol index

## Limitations

- **Not true streaming** — 3-hour latency, poll-based. Not millisecond real-time like AIS or lightning.
- **Large files** — NetCDF granules are 40–150 MB each. Not suitable for inline Kafka payloads; events must reference external S3 URLs.
- **OAuth required** — CDSE account needed. Free but not anonymous.
- **Grid vs. point data** — existing repo bridges stream point observations (station IDs, MMSI). Sentinel-5P is gridded imagery. Requires new consumption pattern.
- **Cloud masking** — NO₂/SO₂/HCHO retrievals are poor under clouds. Users must filter by `qa_value` and `cloud_fraction`.
- **Afternoon bias** — single daily overpass at ~13:30 local time. Misses morning/evening pollution peaks.

## Why It Matters

Sentinel-5P TROPOMI transformed atmospheric science when it launched in 2017. It exposed:
- **COVID-19 lockdown NO₂ drops** — first global evidence of air quality improvement during 2020 lockdowns
- **Permian Basin methane superemitters** — pinpointed oil/gas leaks in Texas/New Mexico
- **La Soufrière 2021 eruption** — tracked SO₂ plume across the Atlantic in real-time
- **China coal power plant compliance** — revealed provincial emission reductions
- **Shipping lanes** — NO₂ and SO₂ corridors from marine fuel combustion

Bridging Sentinel-5P into Kafka enables:
- **Air quality forecasting** — CAMS/regional models can ingest NRT NO₂/O₃ for data assimilation
- **Volcanic ash early warning** — combine with VAAC advisories
- **Industrial monitoring** — detect emission anomalies at refineries, smelters, power plants
- **Climate accounting** — CH₄ emissions for national inventories
- **Cross-domain fusion** — correlate satellite NO₂ with ground station PM2.5, GTFS transit ridership, electricity load

## Alternative: CAMS Global Forecast (Derived Product)

If raw Sentinel-5P granules are too coarse-grained for the repo, consider instead bridging
the **CAMS Global Air Quality Forecast** (`cams-global-atmospheric-composition-forecasts`),
which assimilates Sentinel-5P data and provides:
- 5-day forecasts updated twice daily (00Z, 12Z)
- Regular lat/lon grid (0.4° or 0.1° resolution)
- Hourly time steps
- Ready-to-use concentration fields

But CAMS is a **model**, not raw observations — it inherits model biases and does not
preserve the attribution of individual satellite pixels.

**Verdict**: ✅ **Build** (granule-notification pattern) or ⚠️ **Maybe** (if repo scope is strictly station/entity streams)
