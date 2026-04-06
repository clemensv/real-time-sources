# INMET Brazil — Weather Observation Network (Expanded)

**Country/Region**: Brazil (national)
**Publisher**: INMET — Instituto Nacional de Meteorologia
**API Endpoint**: `https://apitempo.inmet.gov.br/estacoes/T` (stations), `https://apiprevmet3.inmet.gov.br/previsao/{IBGE_code}` (forecast)
**Documentation**: https://portal.inmet.gov.br/
**Protocol**: REST (JSON)
**Auth**: None (some endpoints may require token)
**Data Format**: JSON
**Update Frequency**: Hourly (observations), daily (forecasts)
**License**: Brazilian government open data

## What It Provides — Beyond Basic Weather

This document expands on the existing inmet-brazil.md candidate with newly confirmed endpoints.

### Station Network (confirmed)

```
GET https://apitempo.inmet.gov.br/estacoes/T
```

Returns a comprehensive JSON array of all INMET automatic stations:

```json
[
  {
    "CD_OSCAR": "0-2000-0-86765",
    "DC_NOME": "ABROLHOS",
    "FL_CAPITAL": "N",
    "DT_FIM_OPERACAO": null,
    "CD_SITUACAO": "Pane",
    "TP_ESTACAO": "Automatica",
    "VL_LATITUDE": "-17.96305555",
    "CD_WSI": "0-76-0-2906907000000408",
    "CD_DISTRITO": " 04",
    "VL_ALTITUDE": "20.93",
    "SG_ESTADO": "BA",
    "SG_ENTIDADE": "INMET",
    "CD_ESTACAO": "A422",
    "VL_LONGITUDE": "-38.70333333",
    "DT_INICIO_OPERACAO": "2008-07-20T21:00:00.000-03:00"
  }
]
```

Fields include: WMO OSCAR code, WSI code, station name, type (Automatica/Convencional), status (Operante/Pane), coordinates, altitude, state, operating entity, and operational dates.

### Municipal Forecast (confirmed)

```
GET https://apiprevmet3.inmet.gov.br/previsao/{IBGE_code}
```

Where `{IBGE_code}` is the 7-digit IBGE municipality code (e.g., 3205309 = Vitória, ES).

Response includes morning and afternoon forecasts with: weather summary (Portuguese), temperature range, wind direction/intensity, and weather icon.

### Observation Data Endpoint

```
GET https://apitempo.inmet.gov.br/estacao/{start_date}/{end_date}/{station_code}
```

This endpoint was confirmed to exist (returned empty response during testing — may need active station and recent dates). The URL pattern suggests hourly observation data retrieval by station and date range.

## Integration Notes

- Brazil has 700+ automatic weather stations + conventional stations
- WMO OSCAR and WSI codes enable international cross-referencing
- The station list includes operational status (`Operante` vs `Pane`) — useful for data quality
- IBGE municipality codes link weather forecasts to Brazil's statistical geography system
- The forecast API returns Portuguese text descriptions — NLP translation may be useful
- Station entities include INMET plus partner agencies (SEMADESC-MS, etc.)
- The Abrolhos station (marine, off Bahia coast) provides oceanic weather data

## Additive Value (beyond existing inmet-brazil.md)

This document confirms:
1. The station network metadata API works and returns comprehensive station details
2. The forecast API works with IBGE municipality codes
3. The observation data API pattern exists (needs further testing with valid date ranges)
4. Partner agency stations are included in the network

## Feasibility Rating (for expanded endpoints)

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Hourly observations; daily forecasts |
| Openness | 3 | No auth for tested endpoints |
| Stability | 2 | Government API; some endpoints return 404 |
| Structure | 3 | Clean JSON with WMO identifiers |
| Identifiers | 3 | WMO OSCAR, WSI, IBGE codes — excellent cross-referencing |
| Additive Value | 2 | Expands existing INMET candidate with metadata and forecast APIs |
| **Total** | **15/18** | |

## Verdict

✅ **Build** (enhance existing INMET integration) — The station metadata and forecast APIs add value beyond raw observations. The WMO identifiers enable global cross-referencing. This is supplementary to the existing inmet-brazil.md candidate.
