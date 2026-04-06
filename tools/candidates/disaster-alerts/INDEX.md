# Disaster Alerts — Candidate Sources

| Slug | Source | Region | Protocol | Auth | Score |
|------|--------|--------|----------|------|-------|
| [gdacs](gdacs.md) | GDACS | Global | RSS/CAP | None | 17/18 |
| [meteoalarm](meteoalarm.md) | Meteoalarm | Europe | REST/JSON | None | 18/18 |
| [nws-cap-alerts](nws-cap-alerts.md) | NWS CAP Alerts (IPAWS) | US | REST/GeoJSON | None | 18/18 |
| [ptwc-tsunami](ptwc-tsunami.md) | Pacific Tsunami Warning Center | Pacific/Global | Atom/CAP | None | 16/18 |
| [efas](efas.md) | EFAS (European Flood Awareness) | Europe | CDS API/WMS | Account | 14/18 |

## Summary
Five strong candidates covering global (GDACS), European (Meteoalarm, EFAS), US (NWS), and Pacific (PTWC) disaster alerting. GDACS, Meteoalarm, and NWS are top-tier with no auth, real-time data, and clean APIs. PTWC adds specialized tsunami coverage. EFAS is more complex to integrate but provides unique flood forecasting.
