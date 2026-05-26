# Transit Real-Time Data — Candidate Sources

Candidates for real-time public transit data bridges, focusing on SIRI-native systems and high-value individual feeds that go beyond the generic GTFS-RT bridge.

## Already Implemented

| Source | Protocol | Directory |
|--------|----------|-----------|
| Generic GTFS-RT Bridge | GTFS-RT (Protobuf) | `gtfs/` |
| NextBus | XML (proprietary) | `nextbus/` |

## Candidates

### Tier 1 — SIRI-Native (High Additive Value)

These sources use the SIRI protocol natively. They can't be covered by the existing GTFS-RT bridge and represent genuinely new protocol territory.

| # | Candidate | Country | Protocol | Score | File |
|---|-----------|---------|----------|-------|------|
| 1 | [UK BODS (SIRI-VM)](uk-bods-siri.md) | 🇬🇧 UK | SIRI-VM 2.0 | **17/18** | `uk-bods-siri.md` |
| 2 | [Trafiklab SIRI Regional](trafiklab-siri.md) | 🇸🇪 Sweden | SIRI 2.0 (ET/VM/SX) | **18/18** | `trafiklab-siri.md` |
| 3 | [SNCF / France PAN](sncf-france.md) | 🇫🇷 France | SIRI-Lite + GTFS-RT | **16/18** | `sncf-france.md` |

**Recommendation**: Build a generic SIRI bridge (akin to the GTFS-RT bridge) that handles SIRI-ET, SIRI-VM, and SIRI-SX. Trafiklab (CC0, full SIRI 2.0) is the ideal development target. UK BODS is the highest-volume production deployment. France's SIRI-Lite variant offers a REST-friendly entry point.

### Tier 2 — Push / Event-Driven (Architecturally Interesting)

These sources use push-based protocols that align naturally with event-driven bridge design.

| # | Candidate | Country | Protocol | Score | File |
|---|-----------|---------|----------|-------|------|
| 4 | [Network Rail DARWIN](network-rail-darwin.md) | 🇬🇧 UK | STOMP push + SOAP | **16/18** | `network-rail-darwin.md` |
| 5 | [MBTA V3 API](mbta-v3-api.md) | 🇺🇸 USA (Boston) | REST + SSE streaming | **17/18** | `mbta-v3-api.md` |

**Recommendation**: Darwin's STOMP push and MBTA's SSE streaming are both genuinely push-based — they emit events rather than requiring polling. These are natural fits for CloudEvents bridges.

### Tier 3 — REST / Proprietary (Unique Sources)

These are high-value sources with proprietary REST APIs that provide data not available elsewhere.

| # | Candidate | Country | Protocol | Score | File |
|---|-----------|---------|----------|-------|------|
| 6 | [TfL Unified API](tfl-unified-api.md) | 🇬🇧 UK (London) | REST/JSON | **17/18** | `tfl-unified-api.md` |
| 7 | [DB Timetables (IRIS)](db-timetables.md) | 🇩🇪 Germany | REST/XML | **15/18** | `db-timetables.md` |
| 8 | [NS Dutch Railways](ns-dutch-rail.md) | 🇳🇱 Netherlands | REST/JSON | **14/18** | `ns-dutch-rail.md` |
| 9 | [iRail Belgium Rail API](irail-belgium.md) | 🇧🇪 Belgium | REST/JSON | **16/18** | `irail-belgium.md` |
| 10 | [STIB-MIVB Brussels Open Data](stib-mivb-brussels.md) | 🇧🇪 Belgium | REST/JSON + GTFS-RT | **14/18** | `stib-mivb-brussels.md` |
| 11 | [MTA NYC](mta-nyc.md) | 🇺🇸 USA (NYC) | GTFS-RT + SIRI | **14/18** | `mta-nyc.md` |

**Recommendation**: TfL is the easiest to start with — works without authentication, returns clean JSON, and covers a massive multimodal network. DB Timetables is the only source for German rail real-time. MTA's bus SIRI feeds are notable as a US-based SIRI deployment.

### Tier 4 — European Expansion (Nordic + Central Europe)

Deep-dive round 1 added coverage across Scandinavia, Central Europe, and the Alpine region.

| # | Candidate | Country | Protocol | Score | File |
|---|-----------|---------|----------|-------|------|
| 12 | [Entur Norway](entur-norway.md) | 🇳🇴 Norway | SIRI 2.0 + GTFS-RT + GraphQL | **18/18** | `entur-norway.md` |
| 13 | [Digitransit Finland](digitransit-finland.md) | 🇫🇮 Finland | OTP2 GraphQL + GTFS-RT | **16/18** | `digitransit-finland.md` |
| 14 | [SBB / Open Transport CH](sbb-opentransport.md) | 🇨🇭 Switzerland | REST/JSON + SIRI-SX + OJP | **15/18** | `sbb-opentransport.md` |
| 15 | [BKK Budapest](bkk-budapest.md) | 🇭🇺 Hungary | GTFS-RT + REST/JSON (Futár) | **14/18** | `bkk-budapest.md` |
| 16 | [Rejseplanen Denmark](rejseplanen-denmark.md) | 🇩🇰 Denmark | REST/JSON (HAFAS) | **11/18** | `rejseplanen-denmark.md` |
| 17 | [HSL MQTT Helsinki](hsl-mqtt.md) | 🇫🇮 Finland | MQTT 3.1.1 (push, ~1 Hz) | **18/18** | `hsl-mqtt.md` |
| 17a | [Danish NAP — SIRI over AMQP](dk-nap-siri-amqp.md) 🆕 | 🇩🇰 Denmark | **SIRI 2.x over AMQP** (CC BY 4.0) | **16/18** (⚠️ gated on eIDAS) | `dk-nap-siri-amqp.md` |

**SIRI transport bindings — May 2026 survey**: a comprehensive Europe-wide search (see [`_research-rounds/2026-05-eu-siri-amqp-survey.md`](../_research-rounds/2026-05-eu-siri-amqp-survey.md)) confirmed that **the Danish NAP is the only publicly accessible SIRI-over-AMQP endpoint in Europe**. Every other public European SIRI source (Entur, Trafiklab, opentransportdata.swiss, IDFM PRIM, TfL) publishes over HTTP only. Skånetrafiken's Azure Service Bus deployment is internal-only and not subscribable by third parties. The Danish NAP requires MitID Erhverv or an eIDAS-federated foreign eID for credential signup — this is the only friction blocking a clean upstream-AMQP build. **Implication for the repo**: an AMQP downstream variant on the existing `entur-norway` source ships a complete SIRI/AMQP feeder pattern *today* without depending on the Danish IDP. See the survey doc for the full plan.

**Recommendation**: Entur is a standout — 18/18, no auth needed, native SIRI with pub/sub, full national coverage. It pairs perfectly with Trafiklab for a Nordic SIRI bridge. HSL's MQTT stream is a dream for an MQTT-to-CloudEvents bridge — high-frequency push telemetry with zero authentication friction.

### Tier 5 — Asia-Pacific and Americas (High-Value Global Sources)

Deep-dive round 2 covered the most data-rich transit APIs outside Europe.

| # | Candidate | Country | Protocol | Score | File |
|---|-----------|---------|----------|-------|------|
| 18 | [Taiwan TDX](taiwan-tdx.md) | 🇹🇼 Taiwan | REST/JSON (OData) | **16/18** | `taiwan-tdx.md` |
| 19 | [Hong Kong Transit](hk-transit.md) | 🇭🇰 Hong Kong | REST/JSON (KMB + MTR) | **14/18** | `hk-transit.md` |
| 20 | [Transport for NSW](tfnsw-australia.md) | 🇦🇺 Australia | GTFS-RT + REST + SIRI-FM | **16/18** | `tfnsw-australia.md` |
| 21 | [Singapore LTA DataMall](singapore-lta.md) | 🇸🇬 Singapore | REST/JSON (OData) | **14/18** | `singapore-lta.md` |
| 22 | [Seoul TOPIS](seoul-topis.md) | 🇰🇷 South Korea | REST/XML + JSON | **14/18** | `seoul-topis.md` |
| 23 | [ODPT Japan](odpt-japan.md) | 🇯🇵 Japan | REST/JSON-LD (Linked Data) | **16/18** | `odpt-japan.md` |
| 24 | [SPTrans São Paulo](sptrans-saopaulo.md) | 🇧🇷 Brazil | REST/JSON (session auth) | **11/18** | `sptrans-saopaulo.md` |
| 25 | [Canadian Transit (TTC/TransLink/STM)](canadian-transit.md) | 🇨🇦 Canada | GTFS-RT | **15/18** | `canadian-transit.md` |
| 26 | [Dubai RTA](dubai-rta.md) | 🇦🇪 UAE | REST/JSON (CKAN) | **9/18** | `dubai-rta.md` |

### Africa

| # | Candidate | Country | Protocol | Score | File |
|---|-----------|---------|----------|-------|------|
| 27 | [Nairobi Digital Matatus](nairobi-digital-matatus.md) | 🇰🇪 Kenya | GTFS (static) | **10/18** | `nairobi-digital-matatus.md` |

**Recommendation**: Taiwan TDX is the standout in this tier — clean OData API, bilingual output, live train delays confirmed working without auth. Hong Kong's zero-auth KMB/MTR APIs are excellent for prototyping. ODPT Japan's JSON-LD approach is architecturally unique. TfNSW's SIRI-FM (elevator/escalator status) is a rare accessibility data source.

### Tier 6 — Aggregators, Discovery, and Meta-Sources

Deep-dive round 3 covered platforms that index, aggregate, or abstract over individual feeds.

| # | Candidate | Country | Protocol | Score | File |
|---|-----------|---------|----------|-------|------|
| 28 | [Transitland](transitland.md) | 🌍 Global | REST + GraphQL | **15/18** | `transitland.md` |
| 29 | [Navitia](navitia.md) | 🌍 Global (France+) | REST/JSON (HAL hypermedia) | **14/18** | `navitia.md` |
| 30 | [MobilityData Catalog](mobilitydata-catalog.md) | 🌍 Global | CSV catalog + API | **15/18** | `mobilitydata-catalog.md` |

**Recommendation**: MobilityData's catalog and Transitland's Atlas are essential discovery tools — they tell us where every GTFS-RT feed is worldwide. Use them as configuration sources for automated GTFS-RT bridge deployment. Navitia's open-source engine and HAL hypermedia API are architecturally interesting.

## Priority Order for Implementation

1. **Generic SIRI Bridge** — using Trafiklab as dev target, then deploy against UK BODS, France PAN, Entur Norway, MTA Bus, Swiss SIRI-SX
2. **DARWIN STOMP Bridge** — push-based GB rail (pairs with BODS for full UK coverage)
3. **HSL MQTT Bridge** — MQTT-to-CloudEvents: ~1 Hz vehicle telemetry, zero-auth, push-native 🆕
4. **TfL Unified API Bridge** — low barrier, high data value, clean JSON
5. **MBTA SSE Bridge** — demonstrates SSE-to-CloudEvents pattern
6. **Entur Pub/Sub Bridge** — SIRI with webhook-style push delivery, national Norwegian coverage 🆕
7. **Taiwan TDX Bridge** — OData REST, bilingual, excellent real-time — best Asian transit API 🆕
8. **DB Timetables Bridge** — German rail, unique XML format
9. **NS API Bridge** — Dutch rail (lower priority due to licensing)
10. **Hong Kong Transit Bridge** — zero-auth, trilingual, KMB + MTR combined 🆕
11. **GTFS-RT Bridge Curated Feeds** — use MobilityData/Transitland catalogs to auto-discover feeds for BKK Budapest, Canadian cities, TfNSW, and 800+ other agencies 🆕

## Candidates Not Pursued (Yet)

| Candidate | Country | Reason |
|-----------|---------|--------|
| Indian Railways (IRCTC) | 🇮🇳 India | No verified open real-time API; third-party scrapers exist but no official open feed |
| Oxyfi Train Positions | 🇸🇪 Sweden | WebSocket + NMEA GPS — interesting but niche (subset of Swedish trains only) |

### Tier 7 — Asia & Middle East (Deep Dive Round 5)

| # | Candidate | Country | Protocol | Score | File |
|---|-----------|---------|----------|-------|------|
| 31 | [Israel MOT Transit](israel-mot-transit.md) | 🇮🇱 Israel | CKAN + SIRI real-time | **17/18** | `israel-mot-transit.md` |
| 32 | [Indian Railways](indian-railways.md) | 🇮🇳 India | REST (commercial/third-party) | **14/18** | `indian-railways.md` |

**Key finding**: Israel's Ministry of Transport publishes 180 transportation datasets through a CKAN data portal at data.gov.il with SIRI real-time bus feeds. This is a top-tier discovery — no auth for CKAN, SIRI for real-time. Indian Railways lacks any official open API despite being the world's 4th largest rail network.
| NDOV Loket (NL) | 🇳🇱 Netherlands | Raw KV6/KV17 feeds — complex Dutch-specific protocols, lower priority |
| ÖBB (Austria) | 🇦🇹 Austria | ScottyMobile web endpoint works but no documented public API; HAFAS-based like DB |
| RENFE / TMB / EMT Madrid | 🇪🇸 Spain | Fragmented — no single national API; individual city APIs exist but poorly documented |
| Trenitalia / ATAC Roma | 🇮🇹 Italy | No open real-time API found; Trenitalia has a mobile API but undocumented/unofficial |
| PKP / ZTM (Poland) | 🇵🇱 Poland | ZTM Warsaw has GTFS-RT; PKP national rail has limited open data; covered by GTFS-RT bridge |
| DPP Prague | 🇨🇿 Czech Republic | GTFS-RT available through Golemio (Prague data platform); covered by GTFS-RT bridge |
| De Lijn / Belgian Mobility portal | 🇧🇪 Belgium | GTFS-RT available; important for operator onboarding, but lower additive value than iRail and STIB's direct operator datasets |
| Mexico City Metrobús | 🇲🇽 Mexico | GTFS-RT published but feed quality is variable |
| Dubai RTA | 🇦🇪 UAE | Documented but currently more static than real-time; platform endpoint was unreachable |
| OneBusAway instances | 🌍 Various | BKK Budapest and several US cities use OBA; covered by GTFS-RT bridge |
| OpenTripPlanner instances | 🌍 Various | Entur and Digitransit are the premier OTP2 deployments; covered in their own candidates |

## See Also — Social / News / Wiki Feeds

These are not transit but are relevant real-time open data sources in the social/news domain. Most are already covered or trivially covered by existing bridges.

### Already Covered
- **Bluesky AT Protocol Firehose** (`bluesky/`) — full firehose of the Bluesky social network via AT Protocol Jetstream
- **RSS/Atom Generic** (`rss/`) — covers any RSS/Atom feed including news sites, blogs, government announcements

### Worth Noting

| Source | Protocol | Notes |
|--------|----------|-------|
| **Hacker News Firebase API** | REST + Firebase SSE | `https://hacker-news.firebaseio.com/v0/` — live story/comment IDs. Supports SSE streaming via Firebase's real-time database. Endpoints: `/topstories`, `/newstories`, `/beststories`, `/askstories`, `/showstories`, `/jobstories` (each returns array of item IDs). Individual items via `/item/{id}.json`. No auth required. Could bridge to CloudEvents for "new story" / "new comment" events. |
| **Mastodon / ActivityPub Streaming** | SSE (Server-Sent Events) | Any Mastodon instance exposes `GET /api/v1/streaming/public` for the local/federated timeline via SSE. Streams: `public`, `public:local`, `hashtag:{tag}`, `user` (authenticated). Events: `update` (new post), `delete`, `notification`. JSON payloads. No auth for public streams. Every instance is independent — connect to any instance's streaming endpoint. Relay servers aggregate multiple instances. |
| **Wikipedia Recent Changes** | SSE (EventStreams) | `https://stream.wikimedia.org/v2/stream/recentchange` — SSE stream of all edits across all Wikimedia projects. Already noted in `wikimedia-osm` candidates. |

### Assessment
The RSS bridge already covers most news sources (including HN via its RSS feed). Mastodon streaming is interesting as an ActivityPub/SSE source but overlaps with Bluesky's social feed niche. The HN Firebase API's SSE capability makes it a clean candidate for a small, focused bridge demonstrating Firebase SSE-to-CloudEvents conversion.


## Latin America  April 2026

| # | Source | City | Score | File | Status |
|---|--------|------|-------|------|--------|
| 28 | **Santiago RED/Metro** | Santiago, Chile | **11/18** | [santiago-red-metro.md](santiago-red-metro.md) |  **Maybe**  GTFS-RT likely exists; endpoints unreachable; largest electric bus fleet outside China |
| 29 | **TransMilenio Bogotá** | Bogotá, Colombia | **8/18** | [bogota-transmilenio.md](bogota-transmilenio.md) |  **Skip**  Open data portal unreachable; THE reference BRT system |

### Latin America Transit Summary

SPTrans São Paulo (already documented, 11/18) remains the strongest Latin American transit candidate. Santiago's RED system likely has GTFS-RT (all 6,000+ buses have GPS; historical GTFS feeds known at gtfs.transantiago.cl), but endpoints were unreachable. TransMilenio Bogotá's open data portal was also down. Mexico City Metro and Buenos Aires SUBE were not tested. The region has extensive BRT networks (TransMilenio, Metropolitano Lima, RED Santiago, Metrobús CDMX) but open data APIs lag behind European and North American cities.

## Round 2026-05 — Gulf + Satellite EO sweep

Added in May 2026 by the Gulf (KW/AE/OM/SA/BH/QA/IQ) and satellite-EO (NASA/ESA/NOAA/EUMETSAT/JAXA/ISRO/KARI/CNSA/Other) research fleets.

| Candidate | File | Score | Verdict |
|---|---|---|---|
| Etihad Rail - Future Passenger Rail GTFS (2025–2026 Launch) | [ae-etihad-rail-future.md](ae-etihad-rail-future.md) | ?/18 | — |
| UAE Public Transit GTFS-RT (Dubai Metro, Tram, Bus + Abu Dhabi Bus) | [ae-uae-gtfs-transit.md](ae-uae-gtfs-transit.md) | ?/18 | — |
| Bahrain Public Transport - GTFS/GTFS-RT Coverage | [bh-bahrain-public-transport-gtfs.md](bh-bahrain-public-transport-gtfs.md) | 2/18 | — |
| Iraq Railways - Passenger Train Tracking | [iq-railways-trains.md](iq-railways-trains.md) | 0/18 | ❌ |
| Kuwait Public Transit GTFS Real-Time | [kw-kuwait-gtfs-kptc.md](kw-kuwait-gtfs-kptc.md) | ?/18 | ❌ |
| Mwasalat Oman - Public Transit (GTFS / GTFS-RT) | [om-mwasalat-gtfs.md](om-mwasalat-gtfs.md) | 12/18 | ❌ Skip |
| Qatar Public Transport Ridership (Monthly) | [qa-monthly-transit-ridership.md](qa-monthly-transit-ridership.md) | 8/18 | — |
| Riyadh Metro - GTFS Real-Time | [sa-riyadh-metro.md](sa-riyadh-metro.md) | 12/18 | ⚠️ |
| Saudi Public Transport Company (SAPTCO) - Bus GTFS | [sa-saptco-buses.md](sa-saptco-buses.md) | 8/18 | ⏭️ |
| Saudi Arabian Railways (SAR) - Passenger Rail Tracking | [sa-sar-railways.md](sa-sar-railways.md) | 9/18 | ⏭️ |

