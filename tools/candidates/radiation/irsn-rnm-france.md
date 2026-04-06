# France IRSN / RNM (Réseau National de Mesures de la Radioactivité)

**Country/Region**: France
**Publisher**: IRSN (Institut de Radioprotection et de Sûreté Nucléaire) via RNM
**API Endpoint**: `https://www.mesure-radioactivite.fr/` (web portal)
**Documentation**: https://www.mesure-radioactivite.fr/en
**Protocol**: Web portal (SPA); data shared via EURDEP
**Auth**: None (public portal)
**Data Format**: HTML/JavaScript SPA; data contributed to EURDEP
**Update Frequency**: Continuous monitoring; portal updated regularly
**License**: French government open data

## What It Provides

The RNM (Réseau National de Mesures de la Radioactivité de l'environnement) is France's national environmental radioactivity measurement network. It aggregates data from multiple operators including IRSN, EDF (nuclear power operator), CEA, and others.

The network provides:

- **Ambient dose rate** — Gamma dose equivalent rate from fixed monitoring stations (~460+ teleray stations operated by IRSN)
- **Atmospheric radioactivity** — Aerosol monitoring
- **Environmental media** — Water (rivers, groundwater, marine), soil, food chain
- **Expert and simple modes** — The portal offers both public-friendly and expert-level views of the data

France operates 58 nuclear power reactors (19 power stations), making comprehensive radiation monitoring particularly important.

## API Details

### RNM Web Portal

The portal at `https://www.mesure-radioactivite.fr/` provides interactive maps and data visualization. It loads as a JavaScript SPA. Direct API endpoint probing returned limited results:

- `https://www.mesure-radioactivite.fr/api` — 404
- The portal suggests two modes: "expert" mode with all measurement types, and a simplified mode with pre-selected controls

### IRSN Teleray Network

IRSN operates the "Teleray" network of ~460 automatic ambient dose rate monitoring stations across France. These provide continuous gamma dose rate measurements.

### Data Access via EURDEP

France contributes monitoring data to EURDEP. French stations are accessible through the EURDEP WFS with "FR" prefix:

```
GET https://www.imis.bfs.de/ogc/opendata/ows?service=WFS&version=1.1.0
    &request=GetFeature
    &typeName=opendata:eurdep_latestValue
    &outputFormat=application/json
    &CQL_FILTER=id LIKE 'FR%'
```

## Freshness Assessment

The RNM portal is live as of 2026-04-06 but rendered as a JavaScript SPA — actual data was not directly extractable. French stations are confirmed flowing through EURDEP. The Teleray network provides continuous near-real-time data internally.

## Entity Model

- **Station** — Monitoring station with identifier, coordinates, operator, and measurement type.
- **Measurement** — Value with unit, timestamp, measurement type (ambient dose rate, activity concentration, etc.), operator, and quality flags.
- **Control** — A defined measurement protocol/type combining medium, radionuclide, and analysis method.

## Feasibility Rating

| Criterion | Score | Notes |
|---|---|---|
| Freshness | 3 | Continuous Teleray monitoring, ~460 stations |
| Openness | 1 | No documented public API; SPA-only portal, EURDEP as proxy |
| Stability | 3 | Government nuclear safety infrastructure (IRSN) |
| Structure | 1 | No REST API; SPA with no documented backend endpoints |
| Identifiers | 2 | Station IDs exist in EURDEP (FR prefix) |
| Additive Value | 2 | ~460 stations but accessible via EURDEP already |
| **Total** | **12/18** | |

## Notes

- Like STUK Finland, France's radiation data is best accessed through EURDEP rather than directly.
- The RNM portal appears to be a comprehensive SPA that loads data dynamically — reverse-engineering its API calls is possible but fragile.
- France's data includes not just ambient dose rate but extensive environmental media monitoring (water, food, soil) — the RNM database is one of the richest environmental radioactivity databases in Europe.
- IRSN also publishes annual reports and open data sets, but these tend to be retrospective rather than real-time.
- The "expert" mode on the RNM portal suggests a richer data API exists behind the SPA — worth deeper investigation.
