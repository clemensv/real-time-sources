# Brazil — ANA Telemetria

**Country/Region**: Brazil (nationwide)
**Publisher**: Agência Nacional de Águas e Saneamento Básico (ANA) — National Water and Sanitation Agency
**API Endpoint**: `https://telemetriaws1.ana.gov.br/ServiceANA.asmx`
**Documentation**: https://telemetriaws1.ana.gov.br/ServiceANA.asmx (self-documenting WSDL)
**Protocol**: SOAP / REST (HTTP GET with query parameters returning XML)
**Auth**: None
**Data Format**: XML (SOAP responses)
**Update Frequency**: Sub-hourly (telemetric stations transmit at varying intervals)
**License**: Open access (Brazilian public government data)

## What It Provides

Real-time and historical hydrometeorological data from telemetric monitoring stations across Brazil — one of the largest hydrometric networks in the world. Data includes water level (cotas), discharge (vazões), and rainfall (chuvas) from fluviometric and pluviometric stations. The network is organized by major drainage basins and sub-basins.

## API Details

The service exposes multiple SOAP operations accessible via HTTP GET:

### List Telemetric Stations
```
GET https://telemetriaws1.ana.gov.br/ServiceANA.asmx/ListaEstacoesTelemetricas
  ?statusEstacoes=0
  &origem=
```
Parameters: `statusEstacoes` (0=Active, 1=Maintenance), `origem` (0=All, 1=ANA/INPE, 2=ANA/SIVAM, etc.)

### Hydrometeorological Data
```
GET https://telemetriaws1.ana.gov.br/ServiceANA.asmx/DadosHidrometeorologicos
  ?codEstacao=86480000
  &dataInicio=01/01/2024
  &dataFim=01/02/2024
```

### Station Inventory
```
GET https://telemetriaws1.ana.gov.br/ServiceANA.asmx/HidroInventario
  ?codEstDE=00047000
  &codEstATE=90300000
  &tpEst=1
  &nmEst=
  &nmRio=
  &codSubBacia=
  &codBacia=
  &nmMunicipio=
  &nmEstado=
  &sgResp=
  &sgOper=
  &telemetrica=1
```

### Historical Series
```
GET https://telemetriaws1.ana.gov.br/ServiceANA.asmx/HidroSerieHistorica
  ?codEstacao=86480000
  &dataInicio=
  &dataFim=
  &tipoDados=1
  &nivelConsistencia=1
```
`tipoDados`: 1=Cotas (levels), 2=Chuvas (rainfall), 3=Vazões (discharge)

### Reference Data Operations
- `HidroBaciaSubBacia` — list drainage basins and sub-basins
- `HidroEntidades` — list operating entities
- `HidroEstado` — list states
- `HidroRio` — list rivers
- `HidroMunicipio` — list municipalities

## Freshness Assessment

Probed 2026-04-06: The service endpoint is responsive (returns WSDL and operation documentation) but data requests timed out during testing. This suggests the service may be under load or have performance issues. ANA's telemetry network is known to be operational, but API responsiveness can be inconsistent.

## Entity Model

- **Station Code**: `codEstacao` — 8-digit numeric code, e.g., `86480000`
- **Station Type**: `tpEst` — 1 (Fluviometric), 2 (Pluviometric)
- **Basin/Sub-basin**: Numeric codes for drainage basin hierarchy
- **Operating Entity**: Abbreviation (e.g., `ANA`, `CPRM`)
- **Kafka key**: `stations/{codEstacao}`
- **CloudEvents subject**: `stations/{codEstacao}`

Station codes are stable 8-digit identifiers in the national hydrometric register.

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Sub-hourly telemetry, but API can be slow/unresponsive |
| Openness | 3 | No auth required, public government data |
| Stability | 2 | API is documented and long-running but has performance issues |
| Structure | 2 | XML/SOAP — functional but dated; date format uses DD/MM/YYYY |
| Identifiers | 3 | Stable 8-digit station codes |
| Additive Value | 3 | Brazil is a major gap — largest river network in the world |
| **Total** | **15/18** | |

## Notes

- ANA manages one of the world's largest hydrometric networks, covering the Amazon, Paraná, São Francisco, and other major river basins
- The SOAP/REST hybrid API is functional but uses older conventions (DD/MM/YYYY dates, XML-only responses)
- API performance can be inconsistent — requests may timeout under load
- The `CotaOnline` operations (insert/delete) suggest the API also supports data contribution from field stations
- Portuguese-language field names and documentation
- The `DadosHidrometeorologicosGerais` operation provides unvalidated data — useful for real-time but lower quality
- Consider using `ListaEstacoesTelemetricas` to build a station catalog first, then poll individual stations
- Alternative data source: ANA's HidroWeb portal (https://www.snirh.gov.br/hidroweb/) provides a web UI but may not have a REST API
