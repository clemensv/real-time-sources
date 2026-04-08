# EU AFIR / EAFO / National Access Points — EV Charging Data Landscape

- **Country/Region**: EU-27 + EEA
- **Regulation**: EU Regulation 2023/1804 (AFIR — Alternative Fuels Infrastructure Regulation)
- **Coordination**: NAPCORE (National Access Point Coordination Organisation for Europe)
- **Observatory**: EAFO (European Alternative Fuels Observatory) — `alternative-fuels-observatory.ec.europa.eu`
- **Standards**: DATEX II v3.6 (EV Charging domain), OCPI v2.2, OICP
- **Score**: See per-NAP assessment below
- **Verdict**: **FRAGMENTED — no single EU-wide real-time feed exists**

## Overview

EU AFIR (entered into force 13 April 2024) requires Member States to:
- Establish National Access Points (NAPs) for alternative fuels data
- Publish both **static** (location, connectors, pricing) and **dynamic** (real-time
  availability, occupancy) data for publicly accessible charging points
- Use standardized data formats and unique ID codes (EVSE IDs via IDACS scheme)

EU Delegated Regulation 2022/670 under the ITS Directive also matters here. It
explicitly lists the location and availability of EV recharging points/stations
and ad hoc recharging price within EU-wide real-time traffic information
services. That reinforces the NAP discoverability expectation, but AFIR remains
the more direct EV-charging publication mandate.

NAPCORE coordinates 30+ NAPs (77 partners across 33 countries in phase 2, starting
July 2025, running until December 2027). NAPs are **wildly inconsistent** in setup,
data formats, and API availability. The official NAPCORE directory now exposes NAP
URLs for virtually all EU Member States, but the EV-charging layer behind those
portals remains uneven. As of April 2026, there is no single EU-wide aggregated
real-time feed.

---

## EU-Level Coordination Systems

### EAFO — European Alternative Fuels Observatory

**Not a data API**. EAFO (`alternative-fuels-observatory.ec.europa.eu`) is a
dashboard/reporting site run by DG MOVE. It:
- Publishes **aggregate statistics** (total recharging points by country, monthly)
- Tracks AFIR fleet-based targets per Member State
- No API endpoint found (404 on `/api`). Home page redirects to ECAS login.

**Verdict**: REJECTED. Reporting tool only, not a real-time data source.

### DATEX II v3.6 — EV Charging Domain

DATEX II added an explicit EV Charging user domain in v3.6 (June 2025). The
official DATEX II site now exposes charging-specific profile documentation for
the delegated-regulation categories that matter here, including 2022/670 RTTI
profiles for EV recharging-point location, availability, and ad hoc price, plus
older 962/2015 and MMTIS alternative-fuel profiles with IDACS-to-DATEX mapping.
The dedicated EV Charging user-domain page still says the cross-stakeholder EV
Charging Recommended Reference Profiles are being rolled into the DATEX II
webtool after v3.6, so the guidance is real but still evolving.

Slovenia's official NAP (`nap.si`) already publishes `Prometej IDACS Energy
Infrastructure Status` and `Prometej IDACS Energy Infrastructure Table` in DATEX II
v3.6, plus a TPEG EMI variant, all described as updating **up to 1 minute**.
During this probe, the Slovenian B2B pull URLs returned `401`, so DATEX II
deployment is confirmed, but fully open anonymous access is not.

**Verdict**: Strong standards path and real deployment exist, but open access
remains inconsistent.

### IDACS — ID Issuing and Data Collection

PSA (2019–2021) for 15 Member States (AT, BE, CZ, HR, FR, DE, GR, HU, LT, LU,
NL, PL, PT, SI, ES). Assigned unique EVSE IDs. Website `idacs.eu` not publicly
accessible.

**Verdict**: Coordination programme, not a data feed.

---

## Complete National Access Points Catalog

### Tier 1 — Confirmed Public Real-Time EV Charging Data

These NAPs have **verified, publicly accessible, real-time** EV charging data:

#### Netherlands 🟢 — opendata.ndw.nu
- **Platform**: Static file server (gzipped files, refreshed every few minutes)
- **NAP operator**: NDW (Nationale Databank Wegverkeergegevens)
- **EV Charging files** (all updated 2026-04-08, live):
  - `charging_point_locations_ocpi.json.gz` — **20 MB**, OCPI v2.2 format, full locations+status
  - `charging_point_tariffs_ocpi.json.gz` — **4.2 MB**, OCPI tariff data
  - `charging_point_locations.geojson.gz` — **3.3 MB**, GeoJSON format
- **Format**: OCPI v2.2 JSON + GeoJSON
- **Auth**: None — direct HTTP download
- **License**: Open (NDW open data terms)
- **Existing candidate**: `ndl-netherlands.md` (scored 18/18)
- **Status**: **BEST SOURCE IN EU** — primary target for implementation

#### Germany 🟢 — mobilithek.info / regional live offers
- **Platform**: Mobilithek catalog + MobiData BW public DATEX/OCPI + Hamburg OGC API / SensorThings
- **NAP operator**: BMDV / Mobilithek; live offers currently confirmed from MobiData BW and Hamburg
- **Verified live offers**:
  - `Gebündelte Daten E-Ladesäulen Baden-Württemberg` (Mobilithek offer `-2035239451501556619`)
  - `Elektro Ladestandorte Hamburg` (Mobilithek offer `-5494354146735462252`)
- **Verified public access URLs**:
  - `https://api.mobidata-bw.de/ocpdb/api/public/v1/sources`
  - `https://api.mobidata-bw.de/ocpdb/api/public/datex/v3.5/json/realtime`
  - `https://api.mobidata-bw.de/ocpdb/api/ocpi/3.0/evses?limit=1`
  - `https://api.hamburg.de/datasets/v1/emobility`
  - `https://iot.hamburg.de/v1.1/Datastreams?$filter=properties/layerName%20eq%20'Status_E-Ladepunkt'&$count=true`
- **Format**: DATEX II v3.5 JSON realtime + OCPI 3.0 JSON + OGC API / SensorThings JSON
- **Auth**: None observed during this probe
- **Verified characteristics**:
  - MobiData BW's public source inventory currently lists 10 integrated sources, with realtime `ACTIVE` for nine provider feeds and `PROVISIONED` for the Bundesnetzagentur baseline
  - MobiData BW's DATEX realtime payload exposes per-refill-point states including `available`, `charging`, and `outOfOrder`
  - Hamburg's dataset landing page explicitly states that real-time charge-point status is published as `frei`, `belegt`, `außer Betrieb`, and `keine Daten`
  - Hamburg's SensorThings feed exposed 1,066 station `Things` and 2,152 charge-point datastreams with observed values including `AVAILABLE`, `CHARGING`, `FINISHING`, `PREPARING`, `SUSPENDEDEV`, `SUSPENDEDEVSE`, and `UNAVAILABLE`
- **Additional public metadata signals**:
  - GovData and data.europa.eu now index two Tesla Germany GmbH JSON datasets created in March 2026: `AFIR-recharging-dyn-Tesla` (charging availability information) and `AFIR-recharging-stat-Tesla` (static charging information)
  - Their CKAN records point to Mobilithek offers `953843379766972416` and `953828817873125376` under CC0/DCAT metadata, but the raw payload URL could not be recovered from the public JS-only Mobilithek offer page during this pass
- **Coverage nuance**: Confirmed open live data is now regional rather than singular: Baden-Württemberg and Hamburg are proven, while Tesla AFIR publication is now visible in public metadata but not yet payload-verified. The state-by-state Mobilithek sweep still did not surface equally strong public live feeds for most other Länder. NRW's `mobilitaetsdaten.nrw` / MOBIDROM platform is a real public CKAN-style catalog with mobilityDCAT-AP metadata exports and machine-readable `systemadapter-mobilithek-exporter` distributions, including minute-level DATEX II parking JSON (`parken-nrw.json`) and roadworks XML (`verkehrsinformationen-deutschland.xml`). That proves the platform is operational for regulated road and parking data, but repeated EV-charging keyword probes (`ladesäule`, `elektro`, `charging`, `idacs`, `AFIR`) still returned no matching public charging datasets during this pass. The nationwide NOW/Bundesnetzagentur CSVs remain the broader German baseline.
- **Existing candidates**: `mobidata-bw.md`, `hamburg-emobility.md`, `bundesnetzagentur-ladesaeulen.md`
- **Score**: 17/18

#### Norway 🟢 — nobil.no
- **Platform**: Custom REST API
- **EV Charging**: `api.nobil.no/v3` with `realtime=TRUE` parameter
- **Format**: Custom JSON, CC BY 4.0
- **Auth**: API key (free registration)
- **Existing candidate**: `nobil-norway.md` (scored 18/18)
- **Status**: **Ready for implementation**

#### Switzerland 🟢 — ich-tanke-strom.ch → uvek-gis.admin.ch/BFE/diemo
- **Platform**: BFE DiEMo (Daten- und Informationsaustausch Elektromobilität)
- **EV Charging**: OICP format, real-time EVSE availability
- **Format**: JSON (OICP)
- **Auth**: None for public endpoint
- **Existing candidate**: `switzerland-bfe.md` (scored 16/18)
- **Status**: **Ready for implementation**

---

### Tier 2 — Confirmed EV Data, Public or NAP-Backed, Needs Semantic/Access Verification

These NAPs have EV charging datasets, public machine-readable exports, or official
NAP-backed access URLs, but real-time semantics or access conditions still need
verification:

#### Slovenia 🟡 — nap.si / Prometej IDACS
- **Platform**: Official Slovenian NAP dataset catalog (`nap.si`)
- **NAP operator**: NCUP / Ministry of Infrastructure; EV datasets published by MOPE
- **EV charging datasets discovered**:
  - `Prometej IDACS Energy Infrastructure Table (DATEX II v3.6)` — locations, operational hours, and charging station details
  - `Prometej IDACS Energy Infrastructure Status` — DATEX II v3.6 status publication
  - `Prometej IDACS Energy Infrastructure TPEG EMI` — status and locations in TPEG EMI
- **Format**: XML (DATEX II v3.6, TPEG EMI)
- **Auth**: Public metadata and sample pages; live B2B access URLs returned `401` during this probe
- **Quality metadata**:
  - update frequency `Up to 1 min`
  - availability `24/7`
  - free-of-charge licence published on the dataset pages
- **Key insight**: This is the first confirmed official EU NAP deployment of DATEX II v3.6 EV charging data found in this survey
- **Existing candidate**: `slovenia-prometej.md`
- **Score**: 15/18

#### Belgium 🟡 — transportdata.be
- **Platform**: CKAN 2.11 (`/api/3` available)
- **NAP operator**: ITS Steering Committee / NGI
- **EV Charging datasets** (12 found for "charging"):
  - **Monta**: AFIR Art. 20 compliant static+dynamic JSON endpoint
  - **Gireve EVCI**: EU-wide charging infrastructure, XML
  - **Eco-Movement**: AFIR static dataset for multiple CPOs (Allego, bp pulse, Blink, ChargePoint, Circle K…), JSON
  - **Tesla-API**: Tesla location data, HTTP
  - **Road Public Charging Network**: Belgium, JSON
  - **H2 Mobility**: Hydrogen refueling real-time availability, JSON
  - **Clean Hydrogen JU**: E-HRS-AS real-time HRS availability, JSON
- **Auth**: Public CKAN API, individual datasets may vary
- **License**: Mixed (CC0, CC BY 4.0, ODC-BY, Others)
- **Key insight**: Functions as **cross-border aggregation point** — operators
  publish EU-wide data here. Monta and Eco-Movement datasets are explicitly
  AFIR Article 20 compliant.
- **Next step**: Probe CKAN API for Monta/Gireve/Eco-Movement resource URLs
  to confirm dynamic data presence and refresh frequency
- **Score**: 12/18

#### France 🟡 — transport.data.gouv.fr
- **Platform**: Custom (udata-based), Swagger API available
- **NAP operator**: Ministère des Transports / PAN (Point d'Accès National)
- **EV Charging datasets**:
  - **Base nationale des IRVE**: 80K+ terminals, CSV/GeoJSON, created 2014
  - **Prix des carburants — Flux temps réel**: Real-time fuel prices (not EV)
  - **Prix des carburants — Flux quotidien**: Daily fuel prices
  - **Stations GNV publiques**: CNG stations
- **Real-time**: Listed as "with real time (0)" — **no real-time EV data yet**
- **Format**: CSV, GeoJSON, JSON, ZIP
- **License**: Licence Ouverte
- **Note**: IRVE schema v2 exists (`schema.data.gouv.fr/etalab/schema-irve/`)
  with dynamic fields; not consolidated nationally yet
- **Score**: 10/18

#### Luxembourg 🟡 — data.public.lu
- **Platform**: udata-based open data portal
- **NAP operator**: Ministère de la Mobilité et des Travaux publics
- **EV Charging datasets** (4 found):
  - **Chargy**: INSPIRE Annex I formatted public charging stations (updated monthly)
  - **Public charging stations for electric cars of several operators**: direct `bornes.xml` download on `data.public.lu`, updated 18 February 2026
  - **IDACS alternative fuels infrastructure data**: Historic (2019-2021), static
  - **Charging stations 2021**: Static snapshot with 40km border radius
- **Auth**: Public direct download
- **Note**: `bornes.xml` is a directly downloadable DATEX II v3 `EnergyInfrastructureTablePublication` from `Eco-Movement BV`. It is structured and standards-aligned, but it appears to be table/static infrastructure data rather than a verified live availability feed.
- **Score**: 10/18 (public DATEX II, but still static/table-oriented)

#### Ireland 🟡 — data.gov.ie
- **Platform**: CKAN 2.9 (`/api/3` available)
- **NAP operator**: Department of Public Expenditure / Open Data Unit
- **EV Charging datasets** (6 found):
  - **ESB EV Public Charging Network**: Location data, connector types, power
    output, price, availability hours. CSV.
  - Local council datasets (DLR, SDCC, Fingal, Cork) — GeoJSON/CSV/ArcGIS
- **Auth**: Public CKAN API
- **License**: Mixed
- **Note**: ESB dataset is the most comprehensive. Needs probing for dynamic
  availability (opening hours listed, but not real-time connector status).
- **Score**: 8/18

---

### Tier 3 — Official NAP Exists, EV Content Still Unclear or Access-Restricted

These NAPs exist but EV charging data couldn't be confirmed via programmatic probing:

#### Austria 🔴 — mobilitydata.gv.at / data.gv.at
- **Platform**: Custom NAP + data.gv.at (OGD portal, 68K+ datasets)
- **NAP operator**: Bundesministerium für Klimaschutz / ASFINAG
- **EV Charging**: ÖAMTC publishes "Standort + Verfügbarkeit von Ladestationen"
  via REST+OAuth2. E-Control had a Stromtankstellen page (now 404).
- **Note**: data.gv.at search for "Ladestation" returns general results but
  not a specific EV charging dataset. ÖAMTC feed is OAuth2-protected and
  covers only ÖAMTC-network chargers.
- **Next step**: Probe mobilitydata.gv.at directly, check ÖAMTC API docs

#### Italy 🔴 — piattaformaunicanazionale.it / dati.mit.gov.it
- **Platform**: PUN (custom), dati.mit.gov.it (CKAN)
- **NAP operator**: Ministero delle Infrastrutture e dei Trasporti
- **EV Charging**: PUN lists 68,102 charging points. June 2025: API for
  automated data ingestion announced. dati.mit.gov.it search for "ricarica
  elettrica" returns 0 results — data not yet on CKAN open data catalog.
  SPID auth required for citizen access.
- **Next step**: Monitor PUN for public API launch

#### Spain 🔴 — nap.transportes.gob.es / nap.dgt.es
- **Platform**: Custom NAP portal
- **NAP operator**: Ministerio de Transportes y Movilidad Sostenible / DGT
- **EV Charging**: nap.transportes.gob.es focuses on multimodal transport
  (bus 122 datasets, rail 28, maritime 3, air 1). No EV charging category visible.
  nap.dgt.es (probed earlier) has "Puntos de recarga eléctrica" but format/freshness
  unclear.
- **Next step**: Search nap.dgt.es for the specific EV charging dataset

#### Finland 🔴 — finap.fi
- **Platform**: Fintraffic NAP (National Access Point for mobility services)
- **NAP operator**: Fintraffic / Traficom
- **EV Charging**: NAP is a service catalog (registry of mobility service APIs),
  not a direct data portal. Links to Digitraffic ecosystem. EV charging services
  would be listed as entries but data served by individual operators.
- **Note**: Finnish text-heavy. Digitraffic (digitraffic.fi) covers road/rail/marine/
  aviation but not specifically EV charging.
- **Next step**: Search finap.fi registry for EV charging service entries

#### Sweden 🔴 — nap.transportportal.se / trafiklab.se
- **Platform**: JS-based portals (couldn't extract content)
- **NAP operator**: Trafikverket / Samtrafiken (Trafiklab)
- **EV Charging**: Trafiklab focuses on public transport data (GTFS). Sweden's
  NAP at nap.transportportal.se couldn't be probed (JS-only).
- **Next step**: Use browser-based probing for transportportal.se

#### Denmark 🔴 — registreringsportalen.dk
- **Platform**: JS-based (couldn't extract content)
- **NAP operator**: Energistyrelsen / Danish Transport Authority
- **EV Charging**: data.europa.eu lists a Danish "electric car recharging points"
  dataset (Copenhagen, GeoJSON) hosted on OPEN DATA DK.
- **Next step**: Probe registreringsportalen.dk with browser

#### Poland 🔴 — dane.gov.pl
- **Platform**: Custom OGD portal (44K+ APIs, 168 transport datasets)
- **NAP operator**: Ministry of Digital Affairs
- **EV Charging**: IDACS consortium member. 168 transport datasets on dane.gov.pl
  but EV charging not confirmed. Needs targeted search.
- **API**: DCAT-AP-PL documentation available
- **Next step**: Search `dane.gov.pl/en/dataset?q=ladowanie+stacja+ev` or similar

#### Portugal 🔴 — dados.gov.pt
- **Platform**: udata-based OGD portal (20.8K datasets)
- **NAP operator**: ARTE (Agência para a Reforma Tecnológica do Estado)
- **EV Charging**: Search for "charging electric" returned 0 results. Mobi.E
  operates the national EV charging network (14.4K+ points) but no open data
  API confirmed.
- **Next step**: Search for "Mobi.E" or "veículo elétrico" in Portuguese

#### Greece 🔴 — data.gov.gr
- **Platform**: Custom portal (84 datasets)
- **NAP operator**: Ministry of Digital Governance
- **EV Charging**: 84 datasets cover telecom, transport, traffic, hydrology,
  government transparency. No EV charging datasets found. Has Swagger API
  at `/api/v1/docs/swagger/`.
- **Next step**: Greece's IDACS membership suggests eventual data; monitor

---

### Tier 4 — Official NAP URL Now Known, EV Content Still Unconfirmed

These member states now have official NAP URLs confirmed from the NAPCORE
directory, but this probe did not verify AFIR EV charging datasets on them yet:

| Country | Official NAP URL(s) | What was confirmed | EV charging status |
|---------|---------------------|--------------------|--------------------|
| **Bulgaria** | `https://www.mtc.government.bg/en/category/294/national-access-points-transport-related-data` | Official ministry NAP page with multimodal and road-traffic sections | No charging dataset surfaced |
| **Croatia** | `https://www.promet-info.hr/en` | Official NAP portal per NAPCORE | EV charging not yet confirmed |
| **Cyprus** | `https://www.traffic4cyprus.org.cy/` | Official NAP portal per NAPCORE | EV charging content not extractable in simple fetch |
| **Czech Republic** | `https://registr.dopravniinfo.cz/en/` | Official metadata directory / source registry | No charging dataset surfaced |
| **Estonia** | `https://web.peatus.ee/`; `https://tarktee.mnt.ee/#/en` | Split NAP for MMTIS and RTTI/SRTI | No charging dataset surfaced |
| **Hungary** | `https://napportal.kozut.hu/` | Official NAP confirmed by NAPCORE | Content still JS/cookie-gated in this probe |
| **Latvia** | `https://www.transportdata.gov.lv/` | Official NPP with real-time transport APIs and 52 API-capable datasets | No charging dataset surfaced |
| **Lithuania** | `https://www.visimarsrutai.lt/gtfs/`; `https://maps.eismoinfo.lt/portal/apps/sites/#/npp/pages/counters` | Official NAP components from NAPCORE | No charging dataset surfaced |
| **Malta** | `https://geoservices.transport.gov.mt/egis` | Official transport geoportal / live traffic portal | No charging dataset surfaced |
| **Romania** | `https://pna.cestrin.ro/` | Official PNA with traffic, parking, car-sharing, and bike-sharing information | No charging dataset surfaced |
| **Slovakia** | `https://www.cdb.sk/en/traffic-information-rds-tmc/data-service-in-the-DATEX-II.alej`; `https://ndsas.sk/sluzby/dopravne-informacie`; `https://aplikacie.zsr.sk/MapaVylukZsr/index.aspx` | Fragmented official NAP links from NAPCORE | EV charging not yet confirmed |

---

### Tier 5 — EEA Edge Cases

| Country | Notes |
|---------|-------|
| **Iceland** | NAPCORE lists official RTTI/SRTI road web services at `https://www.vegagerdin.is/vegagerdin/gagnasafn/vefthjonustur`; EV charging not found in this probe. |
| **Liechtenstein** | No independent NAP was confirmed in this probe; likely dependent on Swiss and Austrian ecosystems. |

---

## Key Findings

### 1. Netherlands NDW is the Gold Standard

The Netherlands `opendata.ndw.nu` is the single best EV charging data source in
Europe:
- **OCPI v2.2 format** — industry standard for EV charging
- **20 MB of location+status data** updated every few minutes
- **4.2 MB of tariff data** updated hourly
- **No auth required** — direct gzipped file download
- Covers all public charging points in the Netherlands
- Already catalogued as `ndl-netherlands.md` (18/18)

### 2. Germany Does Have Public Live Status Endpoints

Germany's charging-data picture is now materially stronger than the earlier pass
suggested. Mobilithek now exposes at least two confirmed public German live
offers:
- **MobiData BW** — `api.mobidata-bw.de` returned a live DATEX JSON status feed and documented OCPI 3.0 endpoints without auth, with observed per-refill-point states including `available`, `charging`, and `outOfOrder`
- **Hamburg** — `api.hamburg.de/datasets/v1/emobility` explicitly states that real-time operating status is published, and the public SensorThings service exposed 1,066 station `Things`, 2,152 charge-point datastreams, and observed values including `AVAILABLE`, `CHARGING`, `FINISHING`, `PREPARING`, `SUSPENDEDEV`, `SUSPENDEDEVSE`, and `UNAVAILABLE`
- **Important nuance** — Germany is now clearly proven to have public live charging-status endpoints, but the proof is still regional. The state-by-state Mobilithek sweep did not yet surface equally strong public live feeds for most other Länder, and the nationwide NOW/Bundesnetzagentur CSVs remain the broader baseline rather than a connector-occupancy feed

### 3. Slovenia Proves DATEX II EV Charging Is Already Live

Slovenia's official NAP (`nap.si`) already lists EV charging datasets in DATEX II
v3.6 and TPEG EMI:
- `Prometej IDACS Energy Infrastructure Table` — locations, operational hours, charging-station details
- `Prometej IDACS Energy Infrastructure Status` — status publication
- `Prometej IDACS Energy Infrastructure TPEG EMI` — status and locations

The NAP metadata says **up to 1 minute** update frequency and **24/7** availability.
The important caveat is that the B2B pull URLs returned `401`, so DATEX II EV
deployment is confirmed, but anonymous open access is not.

### 4. Belgium NAP as Cross-Border Aggregation Point

The Belgian CKAN NAP (`transportdata.be`) is the most interesting discovery. Major
roaming platforms publish their EU-wide data here:

| Dataset | Org | Scope | Format | AFIR Art. 20? |
|---------|-----|-------|--------|:-------------:|
| Public_charging_infrastructure_monta | Monta | Multi-country | JSON | Yes |
| EVCI | Gireve | EU-wide | XML | Yes |
| AFIR static dataset selected CPOs | Eco-Movement | Multi-country | JSON | Yes |
| Tesla-API | Tesla Belgium | EU-wide | HTTP | Partial |
| H2 Mobility HRS | H2 Mobility | EU-wide | JSON | — |
| Clean Hydrogen E-HRS-AS | CHJU | EU-wide | JSON | — |

### 5. All EU-27 Member States Are Accounted For

The landscape note now explicitly covers every EU Member State. NAPCORE's official
`National Access Point` directory closed most of the remaining portal-discovery gap.
The main unresolved work is no longer country coverage; it is proving which national
or regional publications already expose reusable AFIR EV charging data openly and in
machine-readable form.

---

## Recommendations

1. **Implement Netherlands NDW first** — already scored 18/18, OCPI v2.2, no auth,
   refreshed every few minutes. This is the primary target.

2. **Add MobiData BW and Hamburg to the German shortlist immediately** — MobiData BW is the strongest state-level DATEX/OCPI feed currently confirmed on Mobilithek, and Hamburg adds a second public German live-status source with an OGC API / SensorThings delivery pattern.

3. **Keep the NOW/Bundesnetzagentur CSV offer as Germany's national baseline** — it
  remains the broader official pull source for station, point, and connector IDs,
  even though the stronger live-status evidence currently comes from Baden-Württemberg and Hamburg.

4. **Probe Belgium CKAN API next** — `transportdata.be/api/3/action/package_show?id=public_charging_infrastructure_monta`
  to check Monta's AFIR endpoint for dynamic data fields (availability, status).
  Also try Gireve EVCI and Eco-Movement AFIR datasets.

5. **Probe Slovenia Prometej access control next** — if the B2B credentials are
  obtainable without restrictive terms, this becomes the strongest DATEX II EV
  source found in the survey.

6. **Use the NAPCORE directory as the country checklist** — the official NAP URLs
  are now known for all EU-27 member states covered here, so the remaining work is
  dataset-level EV verification, not portal discovery.

7. **Monitor Italy PUN** — with 68K+ points and a recently announced API, this
   could become a major source once the public consumer API materializes.

8. **Skip EAFO** — dashboard only, not a data API.

9. **Do not skip DATEX II anymore** — MobiData BW and Slovenia already deploy it for
  EV charging; the remaining blockers are coverage and access policy, not standard maturity.

10. **Revisit the remaining official NAPs quarterly** — AFIR mandates are driving
  data publication; new charging endpoints will appear as Member States comply.

---

## Scoring (EAFO as a source)

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Monthly aggregate stats, not real-time |
| Openness | 1 | Requires ECAS login for full access |
| Stability | 2 | EU Commission managed, will persist |
| Structure | 0 | No API, dashboard-only |
| Identifiers | 0 | Aggregate numbers, no per-EVSE data |
| Richness | 1 | Country-level statistics only |
| **Total** | **5/18** | |

**EAFO Verdict**: REJECTED as a real-time data source.

## Scoring (Belgium NAP as discovery/aggregation point)

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Depends on operator feed; Monta/Gireve may be near-real-time |
| Openness | 2 | CKAN API public; individual datasets may have license restrictions |
| Stability | 2 | Government-backed NAP, AFIR mandate |
| Structure | 2 | CKAN API; datasets in JSON/XML; AFIR-aligned |
| Identifiers | 2 | EVSE IDs per AFIR/IDACS scheme |
| Richness | 2 | Static + potentially dynamic; multi-operator |
| **Total** | **12/18** | |

**Belgium NAP Verdict**: WORTH DEEPER INVESTIGATION — probe CKAN API for the
Monta and Gireve AFIR datasets to confirm dynamic data availability.
