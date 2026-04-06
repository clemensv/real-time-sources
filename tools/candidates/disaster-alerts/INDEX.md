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

| [gdacs-africa](gdacs-africa.md) | GDACS Africa Disaster Alerts | Pan-African | REST/GeoJSON | None | 15/18 |
| [reliefweb-africa](reliefweb-africa.md) | OCHA ReliefWeb Africa | Pan-African | REST/JSON | None | 14/18 |
| [acled-africa-conflict](acled-africa-conflict.md) | ACLED Conflict Events (Africa) | Pan-African | REST/JSON | API Key | 14/18 |
| [open-africa-data-platform](open-africa-data-platform.md) | open.africa Data Platform | Pan-African | REST/JSON (CKAN) | None | 11/18 |

## Summary
Twelve candidates covering global (GDACS, EM-DAT), European (Meteoalarm, EFAS, Copernicus EMS), German (NINA/BBK), US (NWS), Pacific (PTWC), and now **four African sources**. GDACS Africa returns verified GeoJSON for floods, droughts, earthquakes, and cyclones affecting African countries — the drought in Ethiopia/Kenya/Somalia and floods in Mozambique/South Africa/Zimbabwe were confirmed live. ReliefWeb provides humanitarian crisis reports for every African country. ACLED covers armed conflict and political violence across all 54 African states with precise geolocation. open.africa serves as a discovery platform for additional African open datasets.

### Asia — Deep Dive Round 5

| Slug | Source | Region | Protocol | Auth | Score |
|------|--------|--------|----------|------|-------|
| [india-ndma-sachet](india-ndma-sachet.md) | India NDMA SACHET | India | REST/JSON (CAP-format) | **None** | 15/18 |
| [rimes-asia-pacific](rimes-asia-pacific.md) | RIMES Asia-Pacific | 48 countries (S/SE Asia) | Unknown | Unknown | 7/18 |

**Key finding**: India's National Disaster Management Authority publishes real-time CAP-format disaster alerts through the SACHET platform with no authentication. Confirmed working — returns JSON array of active alerts covering cyclones, floods, heat waves, and other natural hazards across India.
