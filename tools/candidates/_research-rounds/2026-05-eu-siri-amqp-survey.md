# Europe-wide SIRI-over-AMQP Survey — May 2026

**Question asked**: *Which European National Access Points and major transit operators publish SIRI (Service Interface for Real-time Information, CEN/TS 15531) over **AMQP** (1.0 or 0.9.1) as a subscribable pub-sub channel? Specifically — which ones can a developer subscribe to **without using a national eID**?*

**Method**: Walked every EU/EEA NAP listed in Trafiklab's European pointer page (<https://www.trafiklab.se/api/other-apis/public-transport-europe/>), plus the UK, plus every major operator portal known to publish SIRI (TfL, IDFM PRIM, SBB SKI+, Trafiklab, NDOV-Loket, NMBS, MIVB, De Lijn, DB, ÖBB). For each, verified the SIGNUP flow and the declared transport bindings. Cross-referenced OpenTripPlanner deployment configurations on GitHub to catch operators that expose AMQP only through OTP integrations.

**Headline finding**: **The Danish NAP (Vejdirektoratet's "Dataudveksleren") is the only publicly accessible SIRI-over-AMQP endpoint in Europe.** Every other public European SIRI feed is HTTP-based. One additional confirmed AMQP/SIRI deployment exists — Skånetrafiken on Azure Service Bus — but is explicitly internal-only and is not subscribable by third parties.

---

## Tally

| Class | Count |
|---|---|
| **Public SIRI-over-AMQP, no eID required** | **0** |
| Public SIRI-over-AMQP, with eID requirement | 1 (🇩🇰 Danish NAP — Movia + Lokaltog datasets 788, 799) |
| Internal-only SIRI-over-AMQP (not subscribable) | 1 (🇸🇪 Skånetrafiken Azure Service Bus) |
| Public SIRI-over-HTTP, no eID required | 7+ (🇳🇴 Entur, 🇨🇭 opentransportdata.swiss, 🇸🇪 Trafiklab, 🇫🇷 IDFM PRIM, 🇬🇧 TfL, 🇧🇪 De Lijn, 🇧🇪 STIB/MIVB, etc.) |
| No SIRI at all (static-only or other formats) | 15+ (most other NAPs publish GTFS-static, KV78, DATEX-II, or nothing at this layer) |

---

## Why this matters

The SIRI standard *defines* an AMQP binding (Part 7 of CEN/TS 15531). NAPCORE — the EU coordination body for NAPs — has been advocating pub-sub over AMQP and MQTT as the modernization path away from the original HTTP-callback push model. Both are real on paper. But adoption has been slow: the Danish NAP is the first public deployment.

For the `clemensv/real-time-sources` repo, this finding determines the bridge architecture for any SIRI source going forward:

- **For the Danish NAP**, the bridge is *upstream-AMQP, downstream-multi-transport* — we consume the publisher's AMQP and re-emit as CloudEvents on Kafka/MQTT/AMQP. Direct mapping; minimal transformation.
- **For every other European SIRI source**, the bridge is *upstream-HTTP, downstream-multi-transport* — we poll the publisher's REST endpoint and re-emit as CloudEvents. This is the existing `entur-norway` pattern. The repo *becomes* the SIRI-over-AMQP gateway for these operators.

The second pattern is more useful for the open-data ecosystem — it means consumers anywhere in Europe can subscribe to a CloudEvents-over-AMQP stream for any major operator, regardless of the operator's own protocol choices.

---

## Comprehensive country-by-country findings

### Confirmed SIRI-over-AMQP

#### 🇩🇰 Denmark — Vejdirektoratet NAP (Dataudveksleren)
- **Endpoint**: <https://du-portal-ui.dataudveksler.app.vd.dk/> (canonical) — `nap.vd.dk` is a permanent redirect
- **Transport**: **AMQP** (`GenericAmqpEvent` per NAP taxonomy). Likely AMQP 1.0 with SASL PLAIN + TLS — confirmed only after login.
- **SIRI version**: 2.x (implied by the CEN/TS 15531-2 publication date and NAPCORE alignment)
- **Services**: ET (estimated timetable) + SX (situations) — no VM exposed
- **Operators**: Movia (Sjælland buses, dataset 788), Lokaltog (Sjælland regional rail, dataset 799)
- **License**: CC BY 4.0
- **Auth**: **MitID Erhverv OR eIDAS-bridged foreign eID** (the IDP is Safewhere, configured for eIDAS federation). Service-account credentials are issued post-login with a one-shot password.
- **eID required**: **Yes** — either Danish MitID Erhverv or your national eID via eIDAS
- **Full writeup**: `transit/dk-nap-siri-amqp.md`

#### 🇸🇪 Skånetrafiken — Azure Service Bus *(internal only)*
- **Transport**: **AMQP 1.0** via Azure Service Bus — confirmed via OpenTripPlanner's `siri-azure` updater extension
- **SIRI version**: 2.0 (Nordic profile)
- **Services**: ET + SX
- **Operators**: Skånetrafiken (Skåne / Malmö region)
- **License**: Unknown (private)
- **Auth**: **Private Skånetrafiken credentials only**. From `opentripplanner/OpenTripPlanner:doc/user/examples/skanetrafiken/Readme.md`: *"The Azure Service Bus is used to propagate SIRI SX and ET real-time messages to OTP... not accessible through any public endpoint."*
- **Verdict**: **Ruled out** — not publicly subscribable. Listed here to document that the technical pattern works in production at a Swedish operator scale, and to flag `developer.otp@skanetrafiken.se` as the contact if you ever want to ask whether they'd open a public credential.

### SIRI-over-HTTP — the realistic alternatives

These are all confirmed accessible **without a national eID**. They are listed in descending order of accessibility for a developer who needs to demonstrate a SIRI-over-AMQP bridge but cannot use the Danish NAP.

#### 🇳🇴 Norway — Entur (existing repo coverage: `entur-norway/`)
- **Endpoint**: `https://api.entur.io/realtime/v1/rest/{et|vm|sx}`
- **Transport**: HTTP REST (SIRI-Lite) + HTTP-callback pub/sub
- **SIRI version**: 2.0 (Norwegian profile v1.1)
- **Services**: ET + VM + SX — all of Norway, 25+ operators
- **License**: NLOD (CC BY-equivalent)
- **Auth**: **None** — anonymous with self-generated `requestorId` UUID for incremental queries. Confirmed live: `curl "https://api.entur.io/realtime/v1/rest/et?requestorId=$(uuidgen)"` returns SIRI 2.0 XML.
- **eID required**: **No**
- **Status in this repo**: Bridge already exists at `entur-norway/`. Kafka + MQTT downstream variants ship. **AMQP downstream variant is the one gap** — closing it would give the repo a complete SIRI-over-AMQP feeder *today* without needing any new external account.

#### 🇨🇭 Switzerland — opentransportdata.swiss (SBB SKI+)
- **Endpoint**: <https://api-manager.opentransportdata.swiss/> (developer portal), `https://api.opentransportdata.swiss/la/siri-et` (data)
- **Transport**: HTTP REST GET (gzip-compressed)
- **SIRI version**: 2.0 (Swiss profile / VDV 736)
- **Services**: ET + PT (planned timetable) + SX — all of Switzerland (SBB + connected cantonal operators)
- **License**: Swiss OGD (CC BY-like)
- **Auth**: Self-service Bearer token via API Manager — email signup only. *"In the box 'Select an App', add an 'app name' and a 'description'... get to the page where you can copy the TOKEN."*
- **eID required**: **No**
- **Volume**: ET snapshot is ~100 MB; rate-limited to max one fetch per 30 seconds
- **Status in this repo**: Documented as `transit/sbb-opentransport.md` (score 15/18). Not yet built.

#### 🇸🇪 Sweden — Trafiklab / Samtrafiken (NeTEx Regional + SIRI)
- **Endpoint**: <https://developer.trafiklab.se/> (developer portal), `https://opendata.samtrafiken.se/siri-et/{operator}/siri-et.xml?key=<key>`
- **Transport**: HTTP REST polling
- **SIRI version**: 2.0 (Nordic profile)
- **Services**: ET + VM + SX
- **Operators**: SL (Stockholm), Skånetrafiken, UL, Östgötatrafiken, JLT, Kronoberg, KLT, Gotland, Blekingetrafiken, Hallandstrafiken, Värmlandstrafik, Örebro, Västmanland, Dalatrafik, X-trafik, Din Tur — 20+
- **License**: **CC0 1.0** (no attribution required)
- **Auth**: API key via Trafiklab email signup. Bronze tier = 50 calls/min, 30,000/month, free.
- **eID required**: **No**
- **Status in this repo**: Documented as `transit/trafiklab-siri.md` (score 18/18 — the highest-rated SIRI candidate). Not yet built.

#### 🇫🇷 France — IDFM PRIM (Île-de-France Mobilités)
- **Endpoint**: <https://prim.iledefrance-mobilites.fr/>
- **Transport**: HTTP REST (SIRI-Lite / Navitia-based)
- **Services**: Real-time departures, traffic info, vehicle positions — RATP, SNCF Transilien, the lot
- **Auth**: Email account signup. All real-time APIs marked "Connexion requise".
- **eID required**: **No** (despite FranceConnect being available, basic email signup works)
- **License**: IDFM custom (open)

#### 🇫🇷 France — transport.data.gouv.fr (national NAP)
- **Endpoint**: <https://transport.data.gouv.fr/>
- **Transport**: File downloads + scattered SIRI-Lite REST endpoints
- **Auth**: None for files; per-operator portal signup for live APIs
- **eID required**: **No**
- **License**: Licence Ouverte / ODbL

#### 🇧🇪 Belgium — De Lijn (data.delijn.be)
- **Endpoint**: <https://data.delijn.be/>
- **Transport**: HTTP REST
- **Services**: Real-time departures, vehicle positions (Flemish bus/tram)
- **Auth**: Self-service API key via portal. *"Subscribe via this self-service portal. You will receive an api-key and can start immediately."*
- **eID required**: **No**
- **License**: Free reuse license

#### 🇧🇪 Belgium — STIB/MIVB (opendata.stib-mivb.be)
- **Endpoint**: <https://opendata.stib-mivb.be/>
- **Transport**: HTTP REST (WSO2 API manager backed)
- **Services**: Vehicle positions, line info (Brussels metro/tram/bus)
- **Auth**: Self-service API key, email signup
- **eID required**: **No**
- **License**: Open data terms

#### 🇬🇧 UK — Transport for London (api.tfl.gov.uk)
- **Endpoint**: <https://api.tfl.gov.uk/>
- **Transport**: HTTP REST
- **SIRI**: Some SIRI-SM (Stop Monitoring) over REST; otherwise TfL's own JSON API and GTFS-RT
- **Auth**: App key via email signup
- **eID required**: **No**
- **License**: TfL Transport Data Terms

### Confirmed *no* SIRI / *no* AMQP

These NAPs were checked and explicitly do not expose SIRI as a subscription channel — most offer GTFS-static, KV78, DATEX-II, or nothing:

| Country | NAP | Finding |
|---|---|---|
| 🇧🇬 Bulgaria | lima.api.bg | Not reachable / no real-time data |
| 🇭🇷 Croatia | promet-info.hr | No SIRI |
| 🇨🇿 Czech Republic | data.gov.cz | Static GTFS only (Prague DPP via Golemio) |
| 🇪🇪 Estonia | peatus.ee | Static GTFS only |
| 🇫🇮 Finland | finap.fi | NAP registration portal returns 401 anonymously; no public real-time SIRI confirmed. Contact: `nap@fintraffic.fi` |
| 🇩🇪 Germany | Mobilithek + opendata-oepnv.de + DELFI | GTFS-static + NeTEx; **no SIRI real-time**; Deutsche Bahn API is REST station-level only |
| 🇬🇷 Greece | nap.gov.gr | Static catalog |
| 🇭🇺 Hungary | napportal.kozut.hu | Static; BKK Budapest publishes GTFS-RT (covered by generic GTFS-RT bridge) |
| 🇮🇪 Ireland | data.gov.ie | Static GTFS only |
| 🇱🇹 Lithuania | visimarsrutai.lt | Static GTFS |
| 🇱🇺 Luxembourg | data.public.lu | Static |
| 🇲🇹 Malta | news.transport.gov.mt | No real-time |
| 🇳🇱 Netherlands | GOVI / NDOV-Loket | Uses **KV78** (Dutch-specific, not SIRI) over **ZeroMQ** (legacy) or REST. Access requires signed "gebruikersovereenkomst" — borderline contract requirement, not eID but not zero-friction either. Format is not standard SIRI. |
| 🇵🇱 Poland | dane.gov.pl | Static; ZTM Warsaw GTFS-RT covered by generic bridge |
| 🇵🇹 Portugal | nap-portugal.imt-ip.pt | Static |
| 🇸🇰 Slovakia | odoprave.info | Static |
| 🇸🇮 Slovenia | ncup.si | Static |
| 🇪🇸 Spain | nap.mitma.es + Madrid CRTM + Barcelona TMB | GTFS-static + per-city REST; **no SIRI** |
| 🇦🇹 Austria | mobilitydata.gv.at + data.oebb.at | Static GTFS / NeTEx; **no SIRI real-time** |
| 🇮🇹 Italy | cciss.it + 5T Torino | 5T historically used SIRI-SM over ZeroMQ (not AMQP); portal appears inactive in 2026 |

---

## Recommendations for `clemensv/real-time-sources`

### Tier-1: Already-in-the-bag

1. **Close the AMQP downstream gap on `entur-norway/`**. The Norwegian source already polls SIRI 2.0 and re-emits as Kafka + MQTT CloudEvents. Adding the AMQP variant follows the `amqp-feeder` skill verbatim — same as how Pegelonline got its AMQP container. This delivers a shipped SIRI-over-AMQP feeder *today* with no external dependency.

### Tier-2: Test the eID barrier

2. **Spend five minutes testing eIDAS on the Danish NAP** (`du-portal-ui.dataudveksler.app.vd.dk` → Log ind → MitID / eID → choose your country). If your national eID federates successfully, the original `dk-nap-siri` source becomes viable as a clean upstream-AMQP demonstration. Score 16/18. Full writeup at `transit/dk-nap-siri-amqp.md`.

### Tier-3: Build a new HTTP-SIRI source if the eID test fails

3. **opentransportdata.swiss** is the strongest fit if a new SIRI source is wanted: clean English+German docs, full Switzerland coverage, SIRI 2.0 with ET + PT + SX, email-only signup, OGD license. The current `transit/sbb-opentransport.md` (15/18) understates its value once the AMQP-binding angle is excluded as universal — at that point, Switzerland's HTTP-SIRI is genuinely the best non-eID alternative.

4. **Trafiklab** (18/18 in existing docs) is the obvious second-strongest target — CC0 license, 20+ Nordic operators, email signup, Bronze-tier free.

### Things not worth pursuing for the SIRI/AMQP goal

- Skånetrafiken's internal Service Bus — closed off, no public access
- Per-country NAPs without SIRI (the bottom 15+ countries listed) — wrong tool layer entirely
- NDOV-Loket — Dutch-specific format (KV78), legacy transport (ZeroMQ), contract barrier

---

## What changes about the build plan

The original plan was: *new source `dk-nap-siri`, upstream AMQP, downstream multi-transport.* That plan still works **if the eID test succeeds**.

If it fails, the corrected plan is:
1. **Phase A — `entur-norway` AMQP downstream**: close the existing gap, ship a SIRI/AMQP feeder this week.
2. **Phase B — new source `opentransportdata-ch` (or similar)**: bring Switzerland into the repo with the full Kafka + MQTT + AMQP triple, demonstrating the SIRI-Lite → AMQP CloudEvents bridge pattern at scale.
3. **Phase C — Trafiklab follow-up**: optional, brings Nordic operators including Skånetrafiken into the repo with CC0 licensing.

The repo *becomes* the European SIRI-over-AMQP gateway under this plan — converting the messy mix of upstream protocols into one clean CloudEvents-over-AMQP fan-out.

---

## Citations

| Claim | Source |
|---|---|
| Danish NAP exposes SIRI over AMQP (`GenericAmqpEvent`) | `https://businessservice.dataudveksler.app.vd.dk/api/Dataset/788` (anonymous GET) — `dataFlowConfig.adapterType=GenericAmqpEvent` + `metadata.dataFormatDataModel=SIRI` |
| Movia + Lokaltog datasets CC BY 4.0 | Same response — `metadata.license=CC_BY`, `metadata.licenseUrl=https://creativecommons.org/licenses/by/4.0/` |
| Danish NAP dataset owner contact | Same — `owner.email=lbe@rejseplanen.dk`, `owner.fullName="Lene Marianne Bergsler"` |
| MitID Erhverv requirement | <https://du-portal-ui.dataudveksler.app.vd.dk/guides> — *"Dansk bruger: Du skal logge ind med MitID Erhverv"* |
| MitID / eID option accepts eIDAS | IDP page at `idp.vejdirektoratet.dk/runtime/oauth2/authorize.idp` exposes three login methods; Safewhere IDP supports eIDAS federation by product design |
| Entur HTTP-only SIRI, anonymous access | <https://developer.entur.org/pages-real-time-intro> — confirmed live: `https://api.entur.io/realtime/v1/rest/et?requestorId=<uuid>` returns SIRI 2.0 XML |
| Skånetrafiken internal-only Service Bus | `opentripplanner/OpenTripPlanner:doc/user/examples/skanetrafiken/Readme.md` — *"The Azure Service Bus is used to propagate SIRI SX and ET real-time messages to OTP... not accessible through any public endpoint"* |
| OTP SiriAzureUpdater confirms AMQP 1.0 SIRI pattern works | `opentripplanner/OpenTripPlanner:application/src/ext/java/org/opentripplanner/ext/siri/updater/azure/SiriAzureUpdater.java` |
| opentransportdata.swiss API Manager email signup | <https://api-manager.opentransportdata.swiss/> — *"In the box 'Select an App', add an 'app name'... copy the TOKEN"* |
| Trafiklab CC0 + email signup | <https://www.trafiklab.se/api/netex-datasets/netex-regional/> — *"API key levels Bronze/Silver/Gold... CC0 1.0"* |
| Trafiklab European pointer page (Denmark = Rejseplanen only) | <https://www.trafiklab.se/api/other-apis/public-transport-europe/> |
| Netherlands GOVI contract requirement | <https://govi.nu/faq.html> — *"na aanmelding en ondertekening van de GOVI-gebruikersovereenkomst"* |

Catalog records archived at `files/nap-movia-datasets.json` (Danish NAP dataset 788 + 799 full responses) and `files/nap-movia-xhr.json` (anonymous Search API capture).
