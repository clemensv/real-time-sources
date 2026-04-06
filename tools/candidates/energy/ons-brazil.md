# ONS — Operador Nacional do Sistema Elétrico (Brazil)

**Country/Region**: Brazil (National Interconnected System — SIN)
**Publisher**: ONS (National Electric System Operator)
**API Endpoint**: `https://tr.ons.org.br/Content/GetBalancoEnergetico/null`
**Documentation**: https://www.ons.org.br/ (Portuguese; API is undocumented)
**Protocol**: REST (ASP.NET MVC JSON endpoints)
**Auth**: None
**Data Format**: JSON
**Update Frequency**: ~1 minute
**License**: Publicly accessible (Brazilian government entity)

## What It Provides

ONS operates Brazil's national interconnected power system (SIN), the largest in South America. The `GetBalancoEnergetico` endpoint returns a real-time energy balance snapshot for the entire country, broken down by its four major subsystems.

Data per subsystem (Southeast/Central-West, South, Northeast, North):

- **Generation total** (MW) with breakdown:
  - Hydraulic (hidraulica)
  - Thermal (termica)
  - Wind (eolica)
  - Nuclear (nuclear)
  - Solar (solar)
  - Itaipu 50Hz (Brazil's share) and 60Hz — specific to the binational Itaipu dam
- **Verified load** (cargaVerificada) — actual system demand in MW
- **Import** and **Export** between subsystems (MW)

Also includes:

- **International interchange**: Argentina, Paraguay, Uruguay flows
- **Inter-regional interchange**: Flows between all subsystem pairs (South↔Southeast, Southeast↔Northeast, etc.)

## API Details

Simple GET request, no parameters needed for real-time snapshot:

```
GET https://tr.ons.org.br/Content/GetBalancoEnergetico/null
```

Response (verified live):

```json
{
  "Data": "2026-04-06T08:10:00-03:00",
  "sudesteECentroOeste": {
    "geracao": {
      "total": 43248.86,
      "hidraulica": 21435.71,
      "termica": 2740.44,
      "eolica": 229.50,
      "nuclear": 1822.89,
      "solar": 12602.77,
      "itaipu50HzBrasil": 305.62,
      "itaipu60Hz": 4111.92
    },
    "cargaVerificada": 48047.59,
    "importacao": 12300.83,
    "exportacao": 7502.10
  },
  "sul": { ... },
  "nordeste": { ... },
  "norte": { ... },
  "internacional": {
    "argentina": 0.003,
    "paraguai": 0.0,
    "uruguai": 0.999
  },
  "intercambio": {
    "internacional_sul": -0.948,
    "sul_sudeste": -7502.10,
    "sudeste_nordeste": -5767.08,
    ...
  }
}
```

The `Data` field is an ISO 8601 timestamp with Brazil timezone offset (BRT, UTC-3). Values are in MW.

## Freshness Assessment

The endpoint returns a snapshot that updates approximately every minute. The `Data` timestamp in the response shows the exact time of the data. During testing, consecutive calls 1 minute apart returned different timestamps and values. This is genuinely real-time operational data from the system operator.

## Entity Model

- **Subsystem**: sudesteECentroOeste (SE/CO), sul (S), nordeste (NE), norte (N)
- **Generation Type**: hidraulica, termica, eolica, nuclear, solar, itaipu50HzBrasil, itaipu60Hz
- **Flow Types**: importacao (import), exportacao (export), intercambio (inter-regional)
- **International Partners**: argentina, paraguai, uruguai
- **Time**: ISO 8601 with BRT offset
- **Values**: MW

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | ~1-minute real-time updates |
| Openness | 3 | No auth, no rate limits observed |
| Stability | 2 | Undocumented endpoint, ASP.NET backend could change without notice |
| Structure | 3 | Clean, well-structured JSON with consistent naming |
| Identifiers | 2 | Portuguese field names, non-standard subsystem codes |
| Additive Value | 3 | Only source for Brazil's real-time grid data, largest hydro system globally |
| **Total** | **16/18** | |

## Notes

- Brazil's grid is ~65% hydroelectric — making this uniquely valuable for understanding hydro-dominated power systems and their interaction with growing wind and solar.
- The Itaipu dam data (split into 50Hz Brazil side and 60Hz) is a fascinating detail — Itaipu operates at two frequencies because it supplies both Brazil (60Hz) and Paraguay (50Hz).
- The Northeast subsystem had 10,120 MW of wind generation during testing — Brazil is a major wind power producer.
- The inter-regional flow data reveals the massive power transfers across Brazil's continental-scale grid (e.g., 7,500+ MW flowing from South to Southeast).
- There may be additional endpoints on `tr.ons.org.br` — the `Content/` path suggests an MVC controller pattern.
- All field names are in Portuguese; a mapping layer would be needed for internationalized use.
