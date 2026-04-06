# GWIS Fire Weather Index (FWI) Forecasts

**Country/Region**: Global
**Publisher**: European Commission — Joint Research Centre (JRC) via EFFIS/GWIS
**API Endpoint**: `https://maps.effis.emergency.copernicus.eu/gwis`
**Documentation**: https://gwis.jrc.ec.europa.eu/
**Protocol**: OGC WMS 1.1.1
**Auth**: None
**Data Format**: GeoTIFF, PNG, JPEG, KML/KMZ, GeoJSON (via WMS GetMap and GetFeatureInfo)
**Update Frequency**: Daily forecast (updated daily)
**License**: CC BY 4.0

## What It Provides

The GWIS (Global Wildfire Information System) publishes daily Fire Weather Index (FWI) forecasts from three independent numerical weather prediction models. The FWI system — originally developed by the Canadian Forest Service — is the global standard for assessing fire danger conditions based on weather parameters (temperature, humidity, wind, precipitation).

Three forecast models provide independent FWI computations:

| Provider | Layer prefix | Resolution | Coverage | Period |
|---|---|---|---|---|
| ECMWF | `ecmwf.*` | ~8 km | Global | 2018–present |
| Meteo France | `mf025.*` | ~25 km | Global | 2018–present |
| NASA GEOS-5 | `nasa_geos5.*` | Variable | Global | 2014–present |

### FWI Sub-Indices Available

Each model provides the complete Canadian FWI system:

| Layer suffix | Index | Description |
|---|---|---|
| `.fwi` | Fire Weather Index | Overall fire danger rating |
| `.ffmc` | Fine Fuel Moisture Code | Moisture of fine surface fuels |
| `.dmc` | Duff Moisture Code | Moisture of moderate-depth organic fuels |
| `.dc` | Drought Code | Deep soil moisture / long-term drying |
| `.isi` | Initial Spread Index | Expected rate of fire spread |
| `.bui` | Build Up Index | Total fuel available for combustion |
| `.anomaly` | FWI Anomaly | Deviation from historical average |
| `.ranking` | FWI Ranking | Percentile ranking against history |

Additional fire danger indices (ECMWF only):

| Layer | System | Description |
|---|---|---|
| `ecmwf.mark5.kbdi` | McArthur MARK-5 | Keetch-Byram Drought Index |
| `ecmwf.mark5.fdi` | McArthur MARK-5 | Fire Danger Index |
| `ecmwf.mark5.ros` | McArthur MARK-5 | Rate of Spread |
| `ecmwf.nfdrs.erc` | US NFDRS | Energy Release Component |
| `ecmwf.nfdrs.bi` | US NFDRS | Burning Index |
| `ecmwf.nfdrs.sc` | US NFDRS | Spread Component |

## API Details

### WMS GetCapabilities

```
GET https://maps.effis.emergency.copernicus.eu/gwis?service=WMS&request=GetCapabilities
```

### Sample GetMap Request (GeoTIFF)

```
GET https://maps.effis.emergency.copernicus.eu/gwis?
    LAYERS=ecmwf.fwi
    &FORMAT=image/tiff
    &TRANSPARENT=true
    &SERVICE=WMS&VERSION=1.1.1
    &REQUEST=GetMap
    &SRS=EPSG:4326
    &BBOX=-180,-90,180,90
    &WIDTH=1600&HEIGHT=800
    &TIME=2025-06-01
```

The `TIME` parameter enables historical queries back to 2014 (NASA GEOS-5) or 2018 (ECMWF, Meteo France).

### Bulk Data (S3)

```
https://effis-gwis-cms.s3.eu-west-1.amazonaws.com/
```

Archived fire statistics, burned area datasets, and emissions data available for bulk download without authentication.

## Freshness Assessment

Daily forecasts updated once per day. Confirmed live on 2026-04-06 via WMS GetCapabilities. Three independent model runs provide redundancy and cross-validation. Historical data available for anomaly computation.

## Entity Model

- **FWI Forecast** — gridded raster product with global coverage, one value per grid cell per day
- **Time-series** — `TIME` parameter allows retrieval of any historical date
- No discrete "event" entities — this is a continuous field product

## Feasibility Rating

| Criterion | Score | Notes |
|---|---|---|
| Freshness | 2 | Daily forecast (not sub-daily) |
| Openness | 3 | No auth, CC BY 4.0, standard OGC WMS |
| Stability | 3 | EU JRC Copernicus infrastructure |
| Structure | 3 | Standard WMS with GeoTIFF output, TIME parameter for historical |
| Identifiers | 2 | Grid cells identified by coordinates |
| Additive Value | 3 | Only open global FWI forecast API; three independent models |
| **Total** | **16/18** | |

## Notes

- This is the single authoritative source for operational FWI forecasts globally. No other open API was found that provides comparable coverage.
- The three-model approach (ECMWF, Meteo France, NASA GEOS-5) provides independent assessments — useful for ensemble analysis or cross-validation.
- The TIME parameter enables both real-time monitoring and historical analysis, making this valuable for both operational and research use cases.
- FWI data complements active fire detection (FIRMS, DEA Hotspots) with predictive fire danger assessment — the "will fires happen" versus "fires are happening" distinction.
- For WFS vector data (burned area polygons, fire statistics), use the EFFIS WFS endpoint documented in the existing [effis-gwis.md](effis-gwis.md).
- Copernicus Climate Data Store (CDS) offers FWI climate projections under RCP scenarios, but for real-time operational FWI, GWIS WMS is the definitive source.
