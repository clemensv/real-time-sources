# Brazil ANA SNIRH — Hydrotelemetry Expanded

**Country/Region**: Brazil (national)
**Publisher**: ANA — Agência Nacional de Águas e Saneamento Básico
**API Endpoint**: `https://www.snirh.gov.br/hidrotelemetria/` (partially accessible)
**Documentation**: https://www.snirh.gov.br/
**Protocol**: REST (suspected; requires endpoint discovery)
**Auth**: Unknown
**Data Format**: Unknown (web portal)
**Update Frequency**: Near-real-time (hydrotelemetry)
**License**: Brazilian government

## What It Provides — Beyond Existing Candidate

This document expands on the existing brazil-ana-telemetria.md with additional findings about the SNIRH (Sistema Nacional de Informações sobre Recursos Hídricos) platform.

### SNIRH Hydrotelemetry Portal

The portal at `https://www.snirh.gov.br/hidrotelemetria/` loaded during testing, displaying:

> "Este sistema tem por objetivo realizar a aquisição, qualificação e gestão dos dados hidrometeorológicos, transmitidos em tempo quase real"

Translation: "This system aims to acquire, qualify, and manage hydrometeorological data, transmitted in near-real-time"

### REST Service (partially tested)

```
GET https://www.snirh.gov.br/hidrotelemetria/RestServiceExterno/TelemetriaAdotada/Estacao/00047000/Nivel/01-04-2026/06-04-2026
```

Returned the portal's general description text rather than data — suggesting the endpoint exists but requires correct parameters or the station/date combination had no data.

### Alternative: telemetriaws1.ana.gov.br (SOAP)

```
GET https://telemetriaws1.ana.gov.br/ServiceANA.asmx/DadosHidrometeorologicos?codEstacao=00047000&dataInicio=06/04/2026&dataFim=06/04/2026
```

Timeout — the SOAP web service was unreachable.

## Key Hydrological Context

Brazil's hydrology is continental-scale:

- **Amazon basin**: 20% of world's freshwater discharge; monitoring critical for climate science
- **Paraná-Plata system**: Largest hydroelectric system in the world (Itaipu, Yacyretá)
- **São Francisco**: Northeast Brazil's lifeline; transposition project (massive water transfer)
- **Porto Alegre flooding**: The 2024 Rio Grande do Sul floods were Brazil's worst natural disaster — monitoring of the Guaíba/Jacuí system is critical

ANA operates 4,500+ telemetric stations across all basins.

## Integration Notes

- The REST endpoint pattern (`/RestServiceExterno/TelemetriaAdotada/Estacao/{code}/Nivel/{start}/{end}`) suggests a structured API
- Station codes follow the ANA numbering system (8 digits)
- Parameters include: Nivel (level), Chuva (rainfall), Vazao (discharge)
- The existing brazil-ana-telemetria.md likely documents the primary access methods
- 2024 Porto Alegre floods highlighted the urgent need for real-time monitoring of the Guaíba basin

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | "Tempo quase real" (near-real-time) per portal |
| Openness | 1 | REST endpoint exists but returns generic page |
| Stability | 2 | National water agency; operational system |
| Structure | 2 | REST URL pattern suggests structured API |
| Identifiers | 3 | ANA 8-digit station codes; parameter types standardized |
| Additive Value | 2 | Expands existing ANA candidate; 4,500+ stations |
| **Total** | **12/18** | |

## Verdict

⚠️ **Maybe** — Complements existing brazil-ana-telemetria.md. The REST endpoint pattern is promising but didn't return data during testing. The SOAP service was unreachable. The 2024 Porto Alegre floods make Brazilian hydrology monitoring politically urgent. Worth deeper investigation of the REST API parameters.
