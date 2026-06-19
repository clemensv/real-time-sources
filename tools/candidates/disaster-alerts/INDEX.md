# Disaster Alerts — Candidate Sources

| Slug | Source | Region | Protocol | Auth | Score |
|------|--------|--------|----------|------|-------|
| [emdat](emdat.md) | EM-DAT International Disaster Database | Global | GraphQL | Account | 15/18 |
| [efas](efas.md) | EFAS (European Flood Awareness) | Europe | CDS API/WMS | Account | 14/18 |
| [copernicus-ems](copernicus-ems.md) | Copernicus EMS Rapid Mapping | Global (EU) | Web portal | None | 14/18 |

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


## Latin America  April 2026

| Slug | Source | Region | Protocol | Auth | Score |
|------|--------|--------|----------|------|-------|
| [cenapred-mexico](cenapred-mexico.md) | CENAPRED Mexico | Mexico | Unknown | N/A | 7/18 |
| [senapred-chile](senapred-chile.md) | SENAPRED Chile | Chile | Unknown | N/A | 8/18 |
| [alertario-rio](alertario-rio.md) | AlertaRio | Rio de Janeiro | REST + WebSocket | Unknown | 12/18 |

### Latin America Disaster Alert Summary

AlertaRio is the most promising  known REST API + WebSocket push for Rio de Janeiro's flood/weather alerts. All endpoints were unreachable during testing, but the WebSocket endpoint (websocket.alertario.rio.rj.gov.br) confirms genuine push capability. CENAPRED Mexico (unreachable, UNAM servers) has the Popocatépetl volcanic traffic light  structured alert data for 25M+ exposed population. SENAPRED Chile's multi-hazard alerts (earthquake, tsunami, volcano, wildfire) would be high-value if accessible. GDACS already provides partial coverage of Latin American disasters.

## Round 2026-05 — Gulf + Satellite EO sweep

Added in May 2026 by the Gulf (KW/AE/OM/SA/BH/QA/IQ) and satellite-EO (NASA/ESA/NOAA/EUMETSAT/JAXA/ISRO/KARI/CNSA/Other) research fleets.

| Candidate | File | Score | Verdict |
|---|---|---|---|
| UAE Disaster Alerts and Emergency Notifications | [ae-uae-disaster-alerts.md](ae-uae-disaster-alerts.md) | ?/18 | — |
| ReliefWeb API - Iraq Humanitarian Alerts and Reports | [iq-reliefweb-humanitarian-alerts.md](iq-reliefweb-humanitarian-alerts.md) | 10/18 | ⚠️ |
| Kuwait Disaster Alerts and Civil Defense | [kw-kuwait-civil-defense-alerts.md](kw-kuwait-civil-defense-alerts.md) | ?/18 | ❌ |
| GDACS - Global Disaster Alerts (Oman Filter) | [om-gdacs-disasters.md](om-gdacs-disasters.md) | 15/18 | ⏭️ Reference |
| RSMC New Delhi - Arabian Sea Tropical Cyclone Warnings | [om-rsmc-newdelhi-cyclone.md](om-rsmc-newdelhi-cyclone.md) | 8/18 | ⏭️ Reference |
| Aviation Dust SIGMETs (Qatar FIR) | [qa-dust-sigmet-aviation.md](qa-dust-sigmet-aviation.md) | 15/18 | — |
| GDACS Global Disasters (Qatar Region) | [qa-gdacs-disasters.md](qa-gdacs-disasters.md) | 13/18 | — |
| Civil Defense Directorate - Emergency Alerts and Flood Warnings | [sa-civil-defense-alerts.md](sa-civil-defense-alerts.md) | 10/18 | ⚠️ |
| Maxar Open Data Program | [spaceother-maxar-open-data.md](spaceother-maxar-open-data.md) | 10/18 | — |

