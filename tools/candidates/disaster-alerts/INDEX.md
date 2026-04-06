# Disaster Alerts — Candidate Sources

| Slug | Source | Region | Protocol | Auth | Score |
|------|--------|--------|----------|------|-------|
| [gdacs](gdacs.md) | GDACS | Global | RSS/CAP | None | 17/18 |
| [meteoalarm](meteoalarm.md) | Meteoalarm | Europe | REST/JSON | None | 18/18 |
| [nws-cap-alerts](nws-cap-alerts.md) | NWS CAP Alerts (IPAWS) | US | REST/GeoJSON | None | 18/18 |
| [nina-bbk](nina-bbk.md) | NINA / BBK Warn-App | Germany | REST/JSON (CAP) | None | 17/18 |
| [ptwc-tsunami](ptwc-tsunami.md) | Pacific Tsunami Warning Center | Pacific/Global | Atom/CAP | None | 16/18 |
| [emdat](emdat.md) | EM-DAT International Disaster Database | Global | GraphQL | Account | 15/18 |
| [efas](efas.md) | EFAS (European Flood Awareness) | Europe | CDS API/WMS | Account | 14/18 |
| [copernicus-ems](copernicus-ems.md) | Copernicus EMS Rapid Mapping | Global (EU) | Web portal | None | 14/18 |

## Summary
Eight candidates covering global (GDACS, EM-DAT), European (Meteoalarm, EFAS, Copernicus EMS), German (NINA/BBK), US (NWS), and Pacific (PTWC) disaster alerting. NINA/BBK is a standout addition — Germany's official multi-source warning system aggregating six providers (MoWaS, DWD, KATWARN, BIWAPP, LHP, Police) into a single unauthenticated REST API with CAP-aligned JSON and 8-language support. EM-DAT adds the world's most comprehensive disaster impact database via GraphQL. Copernicus EMS provides unique satellite-derived rapid mapping but lacks a proper API.
