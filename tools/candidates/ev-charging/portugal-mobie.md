# Mobi.E — Portugal National Charging Network

**Country/Region**: Portugal
**Publisher**: MOBI.E S.A. (Portuguese national e-mobility platform)
**API Endpoint**: https://www.mobie.pt/redemobie/procurar-posto (web portal; no confirmed public API)
**Documentation**: https://www.mobie.pt/
**Protocol**: Web portal / possibly internal OCPI
**Auth**: N/A (web interface only; no public API confirmed)
**Data Format**: N/A for public API; web interface provides map/search
**Real-Time Status**: Partial — website shows station availability and out-of-service stations
**Update Frequency**: Real-time on website (for station status)
**Station Count**: 14,400+ charging points across Portugal
**License**: Unknown for data reuse

## What It Provides

MOBI.E is Portugal's unique national e-mobility platform — a government-mandated universal charging network that operates differently from other European countries. Rather than multiple competing networks, Portugal has a single interoperable network where any registered user can charge at any public station using any authorized charging card or app. MOBI.E manages the platform, while individual Charge Point Operators (OPCs) install and maintain the physical stations and Comercializadores (EMSPs) sell charging services to end users.

The MOBI.E website provides:
- Station finder with map and search
- Real-time station availability information
- Information on out-of-service stations
- Network statistics and coverage data

## API Details

No public REST API has been confirmed. The station finder is a web application at `https://www.mobie.pt/redemobie/procurar-posto` (though the exact URL has changed). There may be:
- Internal APIs powering the web map (could be reverse-engineered but not officially public)
- OCPI connections to European roaming hubs (Gireve, Hubject)
- A data portal called "MOBI.Data" referenced on the website

The website references a "MOBI.Data" portal at `https://www.mobie.pt/portal/mobi.data` which may provide data downloads or API access, but this was not publicly accessible during research.

## Freshness Assessment

The MOBI.E website clearly shows real-time station status — including a dedicated section for "Postos Indisponíveis" (unavailable stations) updated by OPCs. This indicates real-time data flows within the platform. However, this data is not exposed via a public API.

Portugal's centralized model means ALL charging data flows through one platform, which is architecturally ideal for open data publication. Whether MOBI.E chooses to publish this data openly (as the NDL Netherlands does) is a policy decision.

Under EU AFIR, Portugal will need to establish a National Access Point for charging data by 2025 — MOBI.E is the natural candidate to provide this.

## Entity Model

- **Posto de Carregamento**: Charging station/point
- **OPC (Operador de Ponto de Carregamento)**: Charge Point Operator
- **CEME (Comercializador de Eletricidade para a Mobilidade Elétrica)**: EMSP/charging card provider
- **Tipo de Tomada**: Connector type
- **Potência**: Power level

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Real-time status visible on website; not via public API |
| Openness | 0 | No public API confirmed; web-only access |
| Stability | 3 | Government-mandated national platform; legally established |
| Structure | 1 | Web interface only; no documented data format for reuse |
| Identifiers | 1 | Unknown ID scheme for external use |
| Additive Value | 2 | All of Portugal's 14,400+ public charging points in one place |
| **Total** | **9/18** | |

## Notes

- Portugal's centralized e-mobility model is unique in Europe — one platform to rule them all. This is architecturally the cleanest setup for open data publication.
- 14,400+ charging points is significant for a country of Portugal's size — one of Europe's denser networks relative to population.
- The MOBI.Data portal is worth monitoring — it may evolve into a public data access point under AFIR requirements.
- For now, Open Charge Map provides the best programmatic access to Portuguese charging data.
- Portugal's model could be the template for how national charging data should work — the challenge is just getting the data pipe opened for external access.
