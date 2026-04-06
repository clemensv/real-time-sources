# Hydrology and Water Monitoring — Candidate Sources

## Already Implemented

| Source | Country | Directory |
|--------|---------|-----------|
| PegelOnline | Germany | `pegelonline/` |
| RWS Waterwebservices | Netherlands | `rws-waterwebservices/` |
| Hub'Eau Hydrometrie | France | `hubeau-hydrometrie/` |
| BAFU Hydro via existenz.ch | Switzerland | `bafu-hydro/` |
| CHMI Hydro | Czech Republic | `chmi-hydro/` |
| IMGW Hydro | Poland | `imgw-hydro/` |
| NVE Hydro | Norway | `nve-hydro/` |
| SMHI Hydro | Sweden | `smhi-hydro/` |
| SYKE Hydro | Finland | `syke-hydro/` |
| EA Flood Monitoring | UK (England) | `uk-ea-flood-monitoring/` |
| USGS Instantaneous Values | USA | `usgs-iv/` |
| VMM Waterinfo | Belgium | `waterinfo-vmm/` |
| WSV (German Waters) | Germany | `german-waters/` |

## Considered but Dismissed

| Source | Country | Reason |
|--------|---------|--------|
| Austria eHYD | Austria | SPA-only portal; no public REST API found despite extensive probing |
| Spain SAIH (various confederaciones) | Spain | Multiple regional portals (Ebro, Duero, Segura, Guadalquivir) — all behind firewalls or non-responsive; no public API |
| Portugal SNIRH | Portugal | Returns 403 Forbidden; no public API access |
| India CWC | India | Returns 401 Unauthorized; requires authentication |
| South Africa DWS | South Africa | Returns 403 Forbidden; no public API access |
| Japan MLIT river.go.jp | Japan | Web-only interface; no structured API found |
| South Korea WAMIS/K-water | South Korea | Portals non-responsive or API requires Korean-language registration |
| Taiwan WRA | Taiwan | Service endpoints unreachable |
| Denmark DMI/SDFI | Denmark | Water level data requires API key registration; hydrology-specific endpoints not found |
| Latvia LVĢMC | Latvia | SPA portal without public API |
| Croatia HVZ | Croatia | Static file server; no structured API |
| Serbia Srbijavode | Serbia | Endpoints unreachable |
| Iceland IMO | Iceland | API exists for weather/quakes but no hydrology endpoints |

## New Candidates

| Source | Country | Score | Status | File |
|--------|---------|-------|--------|------|
| ECCC Water Survey / MSC GeoMet | Canada | 18/18 | Research complete | [canada-eccc-wateroffice.md](canada-eccc-wateroffice.md) |
| BOM Water Data Online | Australia | 16/18 | Research complete | [australia-bom-waterdata.md](australia-bom-waterdata.md) |
| OPW waterlevel.ie | Ireland | 18/18 | Research complete | [ireland-opw-waterlevel.md](ireland-opw-waterlevel.md) |
| ARSO Hidro | Slovenia | 17/18 | Research complete | [slovenia-arso-hidro.md](slovenia-arso-hidro.md) |
| SEPA Water Levels | Scotland | 16/18 | Research complete | [scotland-sepa-waterlevels.md](scotland-sepa-waterlevels.md) |
| Hilltop (Regional Councils) | New Zealand | 15/18 | Research complete | [newzealand-hilltop.md](newzealand-hilltop.md) |
| ANA Telemetria | Brazil | 15/18 | Research complete | [brazil-ana-telemetria.md](brazil-ana-telemetria.md) |

## Summary

Seven new hydrological data sources have been identified and documented with verified API endpoints. The top candidates by feasibility score are:

1. **Canada ECCC** (18/18) — OGC API Features with GeoJSON, 5-minute intervals, 2100+ stations, no auth. The gold standard for open hydrometric data APIs.
2. **Ireland OPW** (18/18) — Elegant GeoJSON + CSV API, 15-minute intervals, CC BY 4.0. Single request returns all stations.
3. **Slovenia ARSO** (17/18) — Single XML document with entire national network, includes water temperature and flood thresholds. 30-minute updates.
4. **Australia BOM** (16/18) — Kisters WISKI API, ~3500 stations, CC BY 3.0 AU. Array-based JSON format requires custom parsing.
5. **Scotland SEPA** (16/18) — Same Kisters WISKI protocol as BOM Australia. Could share integration code.
6. **New Zealand Hilltop** (15/18) — XML-based, 5-minute intervals. Multiple regional council servers need to be polled independently.
7. **Brazil ANA** (15/18) — SOAP/REST XML service covering the world's largest river network. Performance can be inconsistent.

### Integration Notes

- **Kisters WISKI pattern**: Australia BOM and Scotland SEPA both use the same Kisters WISKI API protocol. A generic Kisters adapter could serve both.
- **Geographic coverage**: These candidates fill major gaps — Southern Hemisphere (Australia, NZ, Brazil), North America (Canada), and European countries not yet covered (Ireland, Slovenia, Scotland).
- **Protocol diversity**: OGC API Features (Canada), REST/JSON (Ireland), REST/XML (Slovenia, NZ, Brazil), Kisters WISKI (Australia, Scotland).
