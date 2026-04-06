# GloFAS — Global Flood Awareness System (Africa)

- **Country/Region**: Pan-African
- **Endpoint**: `https://cds.climate.copernicus.eu/api/v2/resources/cems-glofas-forecast`
- **Protocol**: REST (Copernicus Climate Data Store API)
- **Auth**: CDS API key (free registration)
- **Format**: GRIB2, NetCDF
- **Freshness**: Daily forecasts (updated every 24 hours)
- **Docs**: https://www.globalfloods.eu/ and https://cds.climate.copernicus.eu/
- **Score**: 13/18

## Overview

GloFAS (Global Flood Awareness System) is the European Commission's operational flood
forecasting service, part of the Copernicus Emergency Management Service. It provides
flood forecasts for every major river basin globally, with excellent coverage of Africa.

For Africa, GloFAS is the most comprehensive flood early warning system. It uses ECMWF
weather forecasts coupled with hydrological models to predict river discharge up to 30
days ahead. The system drives the GDACS flood alerts (which we've confirmed live for
Africa).

Key African river basins monitored:
- **Nile**: Entire basin from Uganda/Ethiopia to Egypt
- **Congo/Zaire**: World's second-largest river by discharge
- **Niger**: West Africa's lifeline
- **Zambezi**: Southern Africa, including Kariba/Cahora Bassa dams
- **Limpopo**: South Africa/Mozambique, flood-prone
- **Orange**: South Africa's largest river
- **Volta**: Ghana/Burkina Faso, Akosombo Dam
- **Senegal**: Senegal/Mali/Mauritania
- **Rufiji, Tana, Jubba**: East African rivers

## Endpoint Analysis

The GloFAS data is accessible through the Copernicus Climate Data Store (CDS) API:

```python
import cdsapi
c = cdsapi.Client()
c.retrieve('cems-glofas-forecast', {
    'product_type': 'ensemble_perturbed_forecasts',
    'variable': 'river_discharge_in_the_last_24_hours',
    'hydrological_model': 'lisflood',
    'year': '2026',
    'month': '04',
    'day': '06',
    'leadtime_hour': ['24', '48', '72'],
    'area': [37, -20, -35, 55],  # Africa bounding box
    'format': 'grib'
})
```

The GDACS integration was **verified live** — GloFAS-sourced flood alerts for African
countries (Kenya, South Africa, Mozambique) were returned with severity data.

## Integration Notes

- **CDS API key**: Required. Free registration at https://cds.climate.copernicus.eu/
- **Data format**: GRIB2/NetCDF requires scientific computing libraries (xarray, cfgrib).
  This is more complex than typical JSON APIs.
- **GDACS integration**: For simpler access, use the GDACS API which publishes GloFAS
  flood alerts as GeoJSON (already probed and verified for Africa). This avoids
  the raw data complexity.
- **Threshold-based alerts**: GloFAS provides return period exceedance data (2-year,
  5-year, 20-year flood levels). Emit CloudEvents when forecast exceeds thresholds.
- **African river gauge scarcity**: GloFAS is especially valuable in Africa because
  ground-based river gauging is sparse. Satellite/model-based forecasts fill the gap.
- **Lead time**: 1–30 day forecasts enable early warning. The 3–5 day window is most
  operationally useful.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Daily forecast updates |
| Openness | 2 | Free CDS API key required |
| Stability | 3 | EU Copernicus operational infrastructure |
| Structure | 2 | GRIB2/NetCDF (complex but standard) |
| Identifiers | 2 | CDS dataset IDs, river reach identifiers |
| Richness | 2 | Discharge forecasts, return periods, probabilities |
