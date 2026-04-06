# Czech Republic SURO / MonRaS

**Country/Region**: Czech Republic
**Publisher**: NRPI (National Radiation Protection Institute / SÚRO) and SONS (State Office for Nuclear Safety / SÚJB)
**API Endpoint**: `https://www.sujb.cz/aplikace/monras` and `https://www.suro.cz/aplikace/monras/`
**Documentation**: https://www.suro.cz/en/rms
**Protocol**: Web portal (MonRaS); data shared via EURDEP
**Auth**: None (public portal)
**Data Format**: HTML portal; data contributed to EURDEP
**Update Frequency**: Continuous (Early Warning Network)
**License**: Czech government open data

## What It Provides

The Czech Republic operates a comprehensive Radiation Monitoring Network (RMN) under the legal framework of the Atomic Act (Law No. 263/2016). The system includes:

- **Early Warning Network** — 169 measurement sites providing continuous photon dose equivalent rate:
  - 71 measuring sites from RC SONS, NRPI, Czech Hydro-Meteorological Institute, Fire-Rescue Brigades, and Army
  - 98 teledosimetric system (TDS) sites around Dukovany and Temelin Nuclear Power Stations (24–27 on area boundary + 23–24 in surrounding settlements for each)
- **TLD Territorial Network** — 180 measurement sites (127 outdoor, 53 indoor)
- **TLD Local Networks** — 123 sites near nuclear power stations
- **Environmental Sampling Networks** — Air contamination, laboratory analysis of soil, water, food

### MonRaS Portal

The MonRaS (Monitoring Radiation Situation) web application provides access to:
- External irradiation (Early Warning, TLD, car-borne, air-borne)
- Environmental media (aerosols, fallout, surface water, drinking water)
- Food chain (milk, meat, fish, potatoes, berries, mushrooms, grain, fruit, vegetables)
- Measurement campaigns (ZÓNA exercises)

## API Details

### MonRaS Web Portal

Available at two URLs (primary + backup):
- Primary: `https://www.sujb.cz/aplikace/monras?lng=en_GB`
- Backup: `https://www.suro.cz/aplikace/monras/?lng=en_GB`

The portal is a traditional server-rendered web application (not SPA). Data appears to be loaded through HTML page navigation rather than a REST API.

### No Confirmed REST API

Direct API endpoint probing returned no results:
- `https://www.suro.cz/aplikace/monras/rest/svz/getData` — 404

### Data Access via EURDEP

Czech stations contribute to EURDEP. Accessible via the WFS with "CZ" prefix:

```
GET https://www.imis.bfs.de/ogc/opendata/ows?service=WFS&version=1.1.0
    &request=GetFeature
    &typeName=opendata:eurdep_latestValue
    &outputFormat=application/json
    &CQL_FILTER=id LIKE 'CZ%'
```

## Freshness Assessment

The MonRaS portal is live as of 2026-04-06. Both primary and backup URLs responded with the application interface. However, actual data retrieval requires navigating the web portal — no programmatic API was confirmed. Czech Early Warning Network data flows to EURDEP.

## Entity Model

- **Measurement Site** — Part of one of several networks (Early Warning, TLD, Environmental). Has location, operator, and network affiliation.
- **Measurement** — Photon dose equivalent rate (for Early Warning) or integrated dose (for TLD) or activity concentration (for environmental samples).
- **Nuclear Power Station Zone** — Special dense monitoring around Dukovany and Temelin NPPs.

## Feasibility Rating

| Criterion | Score | Notes |
|---|---|---|
| Freshness | 3 | Continuous Early Warning Network monitoring |
| Openness | 1 | No REST API; web portal only, EURDEP as proxy |
| Stability | 3 | Government infrastructure, legally mandated by Atomic Act |
| Structure | 0 | No programmatic API, HTML-only portal |
| Identifiers | 2 | Station identifiers exist within MonRaS system |
| Additive Value | 2 | 169 Early Warning stations, but accessible via EURDEP |
| **Total** | **11/18** | |

## Notes

- Czech radiation monitoring is comprehensive (legally mandated, multi-layered networks around NPPs) but locked behind a traditional web portal without API access.
- The MonRaS portal provides both a primary (SÚJB) and backup (SÚRO) instance — good redundancy.
- The dense monitoring around Dukovany and Temelin NPPs (98 TDS sites) is valuable for nuclear safety but only accessible through EURDEP or portal scraping.
- For programmatic access, EURDEP is the recommended route.
- The portal also offers a "blindfriendly" version, suggesting some accessibility consideration.
- Multiple Czech government organizations collaborate on monitoring — this complexity may explain the lack of a unified API.
