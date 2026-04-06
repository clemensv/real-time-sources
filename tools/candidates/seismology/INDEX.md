# Seismology & Earthquake — Candidate Source Index

Scouted: 2026-04-06 (Round 1), 2026-04-06 (Round 2 — deep dive)

## Already Implemented

| Source | Directory | Coverage | Notes |
|--------|-----------|----------|-------|
| USGS Earthquakes | `usgs-earthquakes/` | Global | GeoJSON feeds + FDSN; polled every minute; 20+ feed variants |

## Candidates Evaluated

| # | Candidate | File | Score | Coverage | Verdict |
|---|-----------|------|-------|----------|---------|
| 1 | **EMSC SeismicPortal** | [emsc-seismicportal.md](emsc-seismicportal.md) | **17/18** | Global | ✅ **Build** — WebSocket push + FDSN REST; best real-time option |
| 2 | **GFZ GEOFON** | [gfz-geofon.md](gfz-geofon.md) | **17/18** | Global (M4+) | ✅ **Build** — FDSN-compliant; major research center; complements USGS |
| 3 | **GeoNet New Zealand** | [geonet-nz.md](geonet-nz.md) | **16/18** | NZ / Pacific | ✅ **Build** — Cleanest API in this roundup; GeoJSON native |
| 4 | **INGV Italy** | [ingv-fdsnws.md](ingv-fdsnws.md) | **16/18** | Italy / Euro-Med | ✅ **Build** — FDSN-compliant; high-seismicity region |
| 5 | **ETHZ Switzerland** | [ethz-switzerland.md](ethz-switzerland.md) | **16/18** | Switzerland / Alps | ✅ **Build** — FDSN; zero-cost addition via generic adapter |
| 6 | **RESIF France** | [resif-france.md](resif-france.md) | **16/18** | France / Global M5+ | ✅ **Build** — FDSN; includes global teleseismic catalog |
| 7 | **BMKG Indonesia** | [bmkg-indonesia.md](bmkg-indonesia.md) | **16/18** | Indonesia | ✅ **Build** — JSON API; most seismically active country; tsunami potential data |
| 8 | **JMA Japan** | [jma-japan.md](jma-japan.md) | **15/18** | Japan | ✅ **Build** — Uniquely detailed intensity data; custom JSON parsing needed |
| 9 | **FDSN Network Survey** | [fdsn-network-survey.md](fdsn-network-survey.md) | **15/18** | Multi-node | ✅ **Build** — Survey of 14 nodes; ETHZ+RESIF+NIEP+IPGP confirmed working |
| 10 | **EMSC Felt Reports** | [emsc-felt-reports.md](emsc-felt-reports.md) | **15/18** | Global | ⚠️ **Maybe** — Crowdsourced felt data; USGS DYFI already in existing feed |
| 11 | **IGP Peru** | [igp-peru.md](igp-peru.md) | **14/18** | Peru / S. America | ⚠️ **Maybe** — JSON API works but quirky format; major subduction zone |
| 12 | **GCMT Moment Tensors** | [gcmt-moment-tensors.md](gcmt-moment-tensors.md) | **13/18** | Global | ⏭️ **Skip** — Not real-time; no API; invaluable for future enrichment |
| 13 | **ISC Bulletin** | [isc-bulletin.md](isc-bulletin.md) | **12/18** | Global | ⏭️ **Skip** — Not real-time (months-years delay); IRIS successor |
| 14 | **AFAD Turkey** | [afad-turkey.md](afad-turkey.md) | **11/18** | Turkey | ⚠️ **Maybe** — Unique local detail but flaky API; Turkey in EMSC already |
| 15 | **BGS UK** | [bgs-uk.md](bgs-uk.md) | **10/18** | UK | ⏭️ **Skip** — RSS only; very low seismicity; UK in EMSC already |
| 16 | **Geoscience Australia** | [geoscience-australia.md](geoscience-australia.md) | **9/18** | Australia | ⏭️ **Skip** — No public API; low seismicity; data in USGS/EMSC |

### Round 3 — Africa

| # | Candidate | File | Score | Coverage | Verdict |
|---|-----------|------|-------|----------|---------|
| 17 | **East Africa Rift (EMSC)** | [east-africa-rift-seismicity.md](east-africa-rift-seismicity.md) | **16/18** | East Africa / S. Africa | ✅ **Build** — FDSN standard, EMSC+SASN data, verified M3.6–4.5 events |
| 18 | **USGS Africa Bounding Box** | [usgs-africa-earthquakes.md](usgs-africa-earthquakes.md) | **17/18** | Pan-African | ✅ **Build** — Same as existing USGS bridge with Africa bounding box |

## Candidates Not Reachable / Dismissed

| Candidate | Reason |
|-----------|--------|
| **IRIS DMC** | Deprecated; retiring June 2026. Redirects to ISC and USGS. Returned HTTP 400. |
| **CSN Chile** | FDSN endpoint at `evtdb.csn.uchile.cl` returned 404 (re-confirmed Round 2). Web API also 404. |
| **SSN Mexico** | `ssn.unam.mx` connection timeout (re-confirmed Round 2). No accessible API. |
| **Kandilli Observatory (KOERI, Turkey)** | FDSN endpoint at `eida.koeri.boun.edu.tr` returned 404 (re-confirmed). Waveform-only node. |
| **PHIVOLCS Philippines** | Connection failed (Round 1). Not re-tested. |
| **INPRES Argentina** | Connection timeout. No accessible API found. |
| **ISN Ireland** | Website behind Cloudflare challenge (PoW). No data API found. |
| **India NCS** | Website loads (HTML/Drupal CMS) but no data API at `/MIS/riseq/` (404). |
| **Pakistan Met Seismic** | `seismic.pmd.gov.pk` returned 403 Forbidden. |
| **NOA Greece** | FDSN endpoint at `eida.gein.noa.gr` timed out. |
| **BGR Germany** | FDSN event service returned 404 — waveform-only node. |
| **ORFEUS/ODC Belgium** | FDSN event service returned 404 — waveform-only node. |
| **ISC-GEM** | ISC mirror at `isc-mirror.iris.washington.edu` — SSL error / timeout. |
| **ShakeAlert (US EEW)** | Website only; no public API. EEW data is not publicly accessible in real-time. |
| **FUNVISIS Venezuela** | Website loads but redirects; no API found. |
| **RSN Costa Rica** | Website loads (Joomla CMS); RSS/Atom feeds listed but no JSON API. |

### Round 4 — South Asia, SE Asia, Middle East

| # | Candidate | File | Score | Coverage | Verdict |
|---|-----------|------|-------|----------|---------|
| 19 | **AFAD Turkey (Deep Dive)** | [afad-turkey-deep-dive.md](afad-turkey-deep-dive.md) | **15/18** | Turkey | ✅ **Build** — Confirmed M5.2 Van event; date-range filter works; score revised up |
| 20 | **Nepal BIPAD Earthquakes** | [nepal-bipad-seismology.md](nepal-bipad-seismology.md) | **13/18** | Nepal / HKH | ⚠️ **Maybe** — Historical catalog via BIPAD Django REST; same API as hydrology |
| 21 | **PHIVOLCS Philippines** | [phivolcs-philippines.md](phivolcs-philippines.md) | **7/18** | Philippines | ⏭️ **Skip** — Connection timeout consistently; Ring of Fire gap |
| 22 | **Iran IIEES (FDSN)** | [iran-iiees.md](iran-iiees.md) | **10/18** | Iran | ⚠️ **Maybe** — FDSN endpoint documented but unverified due to connectivity |

## Architecture Notes

### The FDSN Opportunity — Expanded

The generic FDSN adapter case is now even stronger. Beyond the original three (EMSC, GFZ, INGV), the deep dive confirmed **four more working FDSN event nodes**:

| Node | Base URL | Status | Catalog |
|------|----------|--------|---------|
| EMSC | `seismicportal.eu/fdsnws/event/1/` | ✅ | EMSC-RTS (global) |
| GFZ | `geofon.gfz-potsdam.de/fdsnws/event/1/` | ✅ | GEOFON (global M4+) |
| INGV | `webservices.ingv.it/fdsnws/event/1/` | ✅ | INGV (Italy) |
| **ETHZ** | `eida.ethz.ch/fdsnws/event/1/` | ✅ | SED (Switzerland/Alps) |
| **RESIF** | `ws.resif.fr/fdsnws/event/1/` | ✅ | Namazu (France + global) |
| **NIEP** | `eida-sc3.infp.ro/fdsnws/event/1/` | ✅ | NIEP (Romania/Vrancea) |
| **IPGP** | `ws.ipgp.fr/fdsnws/event/1/` | ✅ | REVOSIMA (Mayotte) |

Seven nodes, one adapter. The FDSN text format is identical:
`#EventID|Time|Latitude|Longitude|Depth/km|Author|Catalog|...`

### Recommended Build Order (updated)

1. **EMSC SeismicPortal** — WebSocket gives genuine real-time push; highest value
2. **FDSN Generic** (GFZ + INGV + ETHZ + RESIF) — reusable adapter; four config targets
3. **BMKG Indonesia** — Custom JSON; critical Ring of Fire coverage
4. **GeoNet NZ** — Clean GeoJSON API; distinct from FDSN pattern
5. **JMA Japan** — Custom parsing; unique intensity data
6. **IGP Peru** — If South American subduction zone is a priority

### Push vs. Poll

| Source | Mechanism | Latency |
|--------|-----------|---------|
| EMSC | WebSocket (SockJS) | Seconds |
| GeoNet NZ | Poll REST | Minutes |
| GFZ GEOFON | Poll FDSN | Minutes |
| INGV | Poll FDSN | Minutes |
| ETHZ | Poll FDSN | Minutes |
| RESIF | Poll FDSN | Minutes |
| BMKG | Poll JSON | Minutes |
| JMA | Poll JSON | Minutes |
| AFAD | Poll REST | Minutes |
| IGP Peru | Poll JSON | Hours (bulk) |
| USGS (existing) | Poll GeoJSON | ~60 seconds |

Only EMSC provides genuine push delivery. All others require polling.

## Latin America Deep Dive — April 2026

Scouted: 2026-04-06 (Latin America research round)

| # | Candidate | File | Score | Coverage | Verdict |
|---|-----------|------|-------|----------|---------|
| 19 | **CSN Chile** (api.xor.cl) | [chile-csn.md](chile-csn.md) | **16/18** | Chile (national) | ✅ **Build** — Clean JSON API; 20-40+ quakes/day; world's most seismically active country |
| 20 | **RSN Costa Rica** | [rsn-costa-rica.md](rsn-costa-rica.md) | **9/18** | Costa Rica | ⚠️ **Maybe** — Joomla HTML; parseable article titles; Ring of Fire + volcanoes |
| 21 | **SGC Colombia** | [sgc-colombia.md](sgc-colombia.md) | **7/18** | Colombia | ⏭️ **Skip** — FDSN 403; React SPA; covered by USGS/EMSC for M4+ |
| 22 | **SSN Mexico** | [ssn-mexico.md](ssn-mexico.md) | **6/18** | Mexico | ⏭️ **Skip** — Server unreachable; UNAM infrastructure issues |
| 23 | **IGEPN Ecuador** | [igepn-ecuador.md](igepn-ecuador.md) | **5/18** | Ecuador + Galápagos | ⏭️ **Skip** — 403 on all endpoints |
| 24 | **LatAm FDSN Survey** | [latam-fdsn-survey.md](latam-fdsn-survey.md) | N/A | Regional survey | 📋 Survey — Zero working FDSN nodes in Latin America |

### Latin America Seismology Summary

Chile's CSN (via api.xor.cl community API) is the standout — clean JSON, no auth, high throughput. The rest of Latin America is a FDSN desert: not a single working node despite the region sitting on the Pacific Ring of Fire. USGS with geographic filtering provides M4+ coverage for the entire region.
