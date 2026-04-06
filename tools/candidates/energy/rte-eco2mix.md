# RTE éCO2mix (France)

**Country/Region**: France (national + regional)
**Publisher**: RTE (Réseau de Transport d'Électricité) — French TSO
**API Endpoint**: `https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/eco2mix-national-tr/records`
**Documentation**: https://odre.opendatasoft.com/explore/dataset/eco2mix-national-tr/information/
**Protocol**: REST (Opendatasoft v2.1 API)
**Auth**: None (open access, quota: 50,000 API calls/user/month)
**Data Format**: JSON, CSV, GeoJSON
**Update Frequency**: Every 15 minutes (quarter-hourly)
**License**: Open Data (Licence Ouverte / Open Licence)

## What It Provides

éCO2mix is RTE's flagship real-time dataset for the French electricity system. It provides a comprehensive quarter-hourly snapshot of France's entire power system.

Quarter-hourly data:

- **Consumption**: Actual consumption (MW)
- **Forecasts**: Day-ahead (J-1) and intraday (J) consumption forecasts
- **Generation by fuel type**: Nuclear, wind (onshore + offshore), solar, hydro (run-of-river, lakes, pumped storage), gas (CCGT, CHP, peaking), oil, coal, bioenergies (waste, biomass, biogas)
- **Pumped storage**: Pumping consumption (STEP)
- **Cross-border exchanges**: Physical flows with England, Spain, Italy, Switzerland, Germany/Belgium
- **CO2 emission rate**: Estimated carbon intensity (gCO2/kWh)
- **Battery storage**: Charging and discharging

Half-hourly data:

- **Commercial exchanges** at borders

## API Details

Uses the Opendatasoft Explore v2.1 API:

```
GET https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/eco2mix-national-tr/records?limit=2
```

Returns:

```json
{
  "total_count": 6336,
  "results": [{
    "date_heure": "2026-01-31T23:45:00+00:00",
    "consommation": 56460,
    "nucleaire": 47802,
    "eolien": 5814,
    "eolien_terrestre": 4834,
    "eolien_offshore": 980,
    "solaire": 0,
    "hydraulique": 7788,
    "gaz": 3491,
    "taux_co2": 31,
    "ech_physiques": -9500,
    "ech_comm_angleterre": -2568,
    "ech_comm_espagne": 1600
  }]
}
```

All generation/consumption values in MW. Exchange values are signed (negative = export). Supports standard Opendatasoft parameters: `limit`, `offset`, `where`, `order_by`, `select`, `refine`.

## Freshness Assessment

The dataset refreshes every 15 minutes with telemetry data. Values are initially "real-time" estimates from telemetry, later replaced by consolidated metered data, then by definitive data (mid-year A+1). The 15-minute cadence is genuinely real-time for a national grid.

## Entity Model

- **Perimeter**: "France" (national)
- **Nature**: "Données temps réel" (real-time data)
- **Time**: Quarter-hourly timestamps (UTC)
- **Generation**: By fuel type in MW — nuclear, wind (on/offshore), solar, hydro (3 subtypes), gas (3 subtypes), oil (3 subtypes), bioenergies (3 subtypes), coal
- **Exchange**: Per border, physical and commercial
- **CO2**: Emission rate in gCO2/kWh
- **Battery**: Storage charge/discharge

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 15-minute updates, real-time telemetry |
| Openness | 2 | Open but 50,000 calls/month quota (contact for more) |
| Stability | 3 | Government TSO, Opendatasoft hosted, long-running |
| Structure | 3 | Clean JSON, Opendatasoft standard API, well-documented |
| Identifiers | 2 | French field names, no standardized fuel type codes |
| Additive Value | 3 | Uniquely detailed French nuclear/hydro generation mix, sub-fuel breakdown |
| **Total** | **16/18** | |

## Notes

- The 50,000 calls/month quota was introduced because robots were hammering the API at disproportionate frequencies. Contact rte-opendata@rte-france.com for higher limits.
- Field names are in French (consommation, nucleaire, eolien, hydraulique, solaire, etc.).
- The sub-fuel breakdowns are exceptionally detailed: wind split into terrestre/offshore, hydro into fil_eau_eclusee/lacs/step_turbinage, gas into tac/cogen/ccg, bioenergies into dechets/biomasse/biogaz.
- A regional dataset (`eco2mix-regional-tr`) also exists with per-region generation data.
- France's grid is ~70% nuclear, making this dataset particularly interesting for carbon intensity analysis.
