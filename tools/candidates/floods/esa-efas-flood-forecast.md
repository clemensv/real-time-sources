# Copernicus EFAS Flood Forecast (European Flood Awareness System)

- **Country/Region**: Europe (pan-European river basins)
- **Endpoint**: `https://european-flood.emergency.copernicus.eu/efas-data-api/` (requires registration)
- **Protocol**: REST API (JSON)
- **Auth**: Free account registration required
- **Format**: JSON, NetCDF, CSV
- **Freshness**: Twice daily (00Z, 12Z runs), 10-day forecast
- **Docs**: https://european-flood.emergency.copernicus.eu/, https://confluence.ecmwf.int/display/EFAS
- **Score**: 11/18

## Overview

EFAS (European Flood Awareness System) is the Copernicus Emergency Management Service
for **continental-scale flood forecasting** in Europe. Operated by the Joint Research Centre
(JRC) and ECMWF, EFAS provides:

- **10-day flood forecasts** updated twice daily (00Z, 12Z)
- **Pan-European coverage** — 37 countries, major river basins (Danube, Rhine, Po, Ebro, etc.)
- **Hydrological simulations** — discharge, soil moisture, snow water equivalent
- **Flood alerts** — probabilistic exceedance thresholds for 5-year, 20-year return periods
- **Gridded + point data** — 5km resolution grids, plus ~3,600 reporting points

EFAS forecasts are used by national hydrological services, civil protection agencies, and
international organizations (e.g., ERCC - Emergency Response Coordination Centre) for:

- Early warning 3–10 days before flood peaks
- Cross-border flood risk coordination
- Humanitarian pre-positioning (Red Cross, UNICEF)

The system runs the **LISFLOOD** hydrological model forced by ECMWF meteorological forecasts
(rainfall, snowmelt, evaporation).

## Endpoint Analysis

EFAS data is distributed via:

1. **EFAS Web Interface** — interactive maps, not machine-readable
2. **WMS/WFS services** — for GIS integration
3. **FTP server** — NetCDF forecast files (restricted access)
4. **REST API** (in development as of 2026) — JSON endpoint for reporting point forecasts

The **REST API** is the best candidate for bridging but requires:
- Account registration (email verification)
- API token
- Possible usage quotas (undocumented)

**Sample endpoint** (hypothetical — actual URL requires authentication):

```
GET https://api.efas.eu/v1/forecast/discharge?
  point_id=12345&
  issue_time=2026-01-15T00:00:00Z&
  forecast_horizon=240
```

Returns JSON with ensemble discharge forecasts (51 members) at 6-hour intervals for the
next 10 days.

**WFS endpoint** (public, limited to point locations):

```
https://www.efas.eu/en/data-and-services/efas-wfs
service=WFS&request=GetFeature&typeName=efas:stations&outputFormat=application/json
```

Returns GeoJSON of EFAS reporting point metadata (station ID, name, river, basin, country).

**Actual data access workflow** (as of Jan 2026):

EFAS does **not** have a public real-time API. Data access requires:

1. Submit data request form: https://european-flood.emergency.copernicus.eu/data-access
2. Sign end-user license agreement (EULA)
3. Receive FTP credentials
4. Download NetCDF files manually or via script

This is a **human-in-the-loop** process unsuitable for automated bridging without prior
institutional agreement.

## Schema / Sample Payload

EFAS forecast NetCDF files (from FTP) contain:

```
netcdf efas_discharge_forecast {
dimensions:
    time = 41 ;  // 10 days × 4 time steps/day + initial
    ensemble = 51 ;
    station = 3600 ;
variables:
    float discharge(time, ensemble, station) ;
        discharge:units = "m3 s-1" ;
        discharge:long_name = "River discharge" ;
    double time(time) ;
        time:units = "hours since 2026-01-15 00:00:00" ;
    int station_id(station) ;
    float latitude(station) ;
    float longitude(station) ;
```

Each reporting point has:
- **station_id** — stable identifier (5-digit integer)
- **River name** — e.g., "Danube at Bratislava"
- **Upstream area** — catchment size (km²)
- **Thresholds** — 5-year, 20-year return period discharge (m³/s)

The **ensemble forecast** (51 members) quantifies uncertainty. The control member (member 0)
is the deterministic forecast; members 1–50 are perturbed ensemble members.

EFAS also provides **exceedance probability**: likelihood that discharge exceeds flood
thresholds within 10 days.

## Why Strong

| Criterion | Score | Rationale |
|-----------|-------|-----------|
| **Value** | 3 | Pan-European flood forecasting is mission-critical for civil protection, humanitarian response, and transboundary coordination. |
| **Freshness** | 2 | Twice daily (00Z, 12Z), 10-day forecast horizon. Sufficient for early warning but not sub-daily. |
| **Openness** | 1 | **Restricted access** — requires signed EULA, account approval, and FTP credentials. Not open to public automated polling. |
| **Schema clarity** | 3 | NetCDF-4 with CF conventions, well-documented station metadata and thresholds. |
| **Machine-readability** | 1 | **No public API** — FTP-based file downloads. REST API is in beta and requires institutional access. |
| **Repo fit** | 1 | Ensemble forecasts (51 members × 3,600 stations × 41 time steps = 7.5M values per run) are bulk data, not streaming. Better suited to S3 storage + notification events than Kafka payloads. |

**Total: 11/18** — High value but **access restrictions** and **bulk-data model** make it
unsuitable for open automated bridging.

## Integration Notes

### If Access Were Granted

Assume EFAS provides an authenticated REST API or FTP credentials. A bridge would:

1. **Poll twice daily** (after 03:00 and 15:00 UTC when 00Z/12Z forecasts are ready)
2. Download NetCDF or query API for ~3,600 reporting points
3. Extract ensemble mean and 90th percentile discharge
4. Emit CloudEvents:
   - **Subject**: `flood/forecast/{river_basin}/{station_id}` (e.g., `flood/forecast/danube/12345`)
   - **Kafka key**: `{station_id}` (stable 5-digit ID)
   - **Payload**: JSON with forecast array (10 days × 4 steps/day = 40 values), exceedance probability, threshold metadata
   - **Type**: `eu.copernicus.efas.forecast.discharge`

### Deduplication

Each forecast run supersedes the previous. Store `issue_time` (00Z or 12Z timestamp) in
bridge state. Only emit events if `issue_time` is newer than last-seen.

### Threshold Alerts

EFAS provides **formal flood warnings** when exceedance probability exceeds thresholds:

- **Severe**: >50% chance of exceeding 5-year return period
- **High**: >30% chance of exceeding 20-year return period

These warnings are published separately via the **EFAS Flash Flood Indicator** and
**Flood Notifications** (email to registered national focal points). Bridging the
**notification feed** (if API-accessible) would be higher value than raw discharge forecasts.

## Limitations

- **No public API** — FTP-based or requires institutional agreement
- **Restricted access** — EULA signature, account approval, usage tracking
- **Ensemble complexity** — 51-member ensembles are statistically rich but require aggregation for downstream use
- **Reporting point coverage** — 3,600 points cover major rivers but miss small tributaries and urban streams
- **Model uncertainty** — LISFLOOD is calibrated for large basins; accuracy degrades for flashy Mediterranean rivers and urban areas
- **No gridded API** — 5km gridded forecasts exist but are only available as bulk NetCDF, not via API
- **Twice-daily updates** — flashy rivers (e.g., Alpine tributaries) can flood within 6 hours; twice-daily updates are too slow

## Alternative: GloFAS (Global Flood Awareness System)

If EFAS access is restricted, consider **GloFAS** (`https://global-flood.emergency.copernicus.eu/`),
the global equivalent with:

- **Worldwide coverage** — all continents
- **Same model** (LISFLOOD) and resolution (5km)
- **Same update frequency** (twice daily)
- **Similar access model** — requires registration, but more widely available to research users

GloFAS may have a more permissive API or data sharing agreement.

## Why It Matters

European flooding causes billions in damages annually:

- **2021 Germany/Belgium floods** — 220 deaths, €30B damages
- **2023 Italy Emilia-Romagna floods** — 17 deaths, evacuations
- **2024 Central Europe floods** — Danube, Vltava, Elbe basins

EFAS issued **early warnings 7–10 days in advance** for all three events. Cross-border
coordination via EFAS reduced casualties by enabling pre-positioning and evacuations.

Bridging EFAS into Kafka enables:
- **Cross-domain correlation** — flood forecasts + precipitation radar + soil moisture
- **Humanitarian logistics** — pre-position relief supplies when exceedance probability rises
- **Insurance trigger** — parametric flood insurance payouts based on EFAS thresholds
- **Infrastructure scheduling** — hydropower, irrigation, navigation planning

## Verdict

⏭️ **Reference** — Scientifically critical and operationally valuable, but **restricted access**
and **institutional approval process** prevent open automated bridging. **Consider** only if:

1. A formal data-sharing agreement can be established with EFAS/JRC/ECMWF
2. An API (REST or FTP) is documented and stable
3. The repo is willing to handle licensed data (not fully open)

Without institutional access, **skip** in favor of openly accessible national hydrological
services (already bridged: USGS, Pegelonline, HydroPortail, etc.).

**Alternative**: Bridge the **EFAS Flash Flood Indicator** RSS feed (if it exists and is public)
as a lightweight notification service, rather than the full forecast dataset.
