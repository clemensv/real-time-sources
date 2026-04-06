# Government AIS Data Programs — Global Survey

**Research date**: 2026-04-06
**Scope**: National maritime administration AIS data accessibility across 20+ countries

## Summary

An exhaustive investigation of government-operated AIS data programs worldwide. The goal:
identify which national maritime administrations provide public API access to their
shore-based AIS data. The answer, with few exceptions, is: almost none of them do.

Norway (Kystverket/BarentsWatch) and Finland (Digitraffic) remain the global gold standard.
Every other country investigated either has no public AIS API, restricts access to
operational stakeholders, or makes data available only in non-real-time aggregate form.

## Nordic Countries

### Sweden — Sjöfartsverket (Swedish Maritime Administration)

| Item | Status |
|---|---|
| Website | `sjofartsverket.se` (minimal content on English/Swedish pages) |
| AIS API | ❌ Not found |
| Open data portal | ❌ No open data pages found (404 on multiple URL patterns) |
| AIS page | ❌ `sjofartsverket.se/sjofart--hamnar/maritima-tjanster/ais/` returns 404 |

**Assessment**: The Swedish Maritime Administration's website appears to have been recently
restructured — many URLs return 404. No evidence of public AIS data sharing was found.
Sweden operates a comprehensive shore-based AIS network covering Swedish waters, but access
appears restricted to operational users (VTS, coast guard, SAR).

The website structure suggests a focus on maritime safety services and fairway management
rather than open data. Sweden does participate in HELCOM AIS data sharing for Baltic traffic
analysis, but this is aggregate/historical data, not real-time.

### Denmark — DMA / DEMA

See [denmark-dma-ais.md](denmark-dma-ais.md) for detailed investigation. The Danish
land-based AIS system has been transferred from the Danish Maritime Authority to the Danish
Emergency Management Agency (DEMA/Beredskabsstyrelsen). No public API was discovered.
Historical AIS data has been available through academic channels (ITU Copenhagen) but no
current programmatic access was found.

## Baltic States

### Estonia — Transpordiamet (Transport Administration)

| Item | Status |
|---|---|
| Maritime authority | Transpordiamet (merged transport agency) |
| AIS API | ❌ Not found |
| Notes | Website focused on road/rail transport; maritime section minimal |

Estonia does operate shore-based AIS stations, contributing to HELCOM Baltic coverage.
No public data access discovered.

### Latvia — Maritime Administration of Latvia

| Item | Status |
|---|---|
| Maritime authority | Jūras administrācija |
| AIS API | ❌ Not found |
| Notes | VTS system operational for Riga and Ventspils ports |

Latvia operates VTS (Vessel Traffic Services) at major ports with AIS integration, but
this is an operational system without public data access.

### Lithuania — Lithuanian Maritime Safety Administration (LMSA)

| Item | Status |
|---|---|
| Maritime authority | Lietuvos jūrų saugumo administracija |
| AIS API | ❌ Not found |
| Notes | Klaipėda VTS operational |

Klaipėda is Lithuania's only significant port. The VTS system uses AIS but data is not
publicly accessible.

## Asia-Pacific

### Singapore — Maritime and Port Authority (MPA)

| Item | Status |
|---|---|
| Website | `mpa.gov.sg` |
| AIS API | ❌ Not found |
| data.gov.sg | No vessel tracking datasets found in search |
| VTIS | MPA operates VTIS (Vessel Traffic Information System) — operational only |

Singapore's Strait is one of the busiest waterways in the world. MPA operates a
comprehensive VTIS with AIS integration, but this is a controlled operational system.
Port arrival/departure data may be available through MPA's separate shipping information
portals, but real-time vessel positions are not publicly exposed.

The data.gov.sg platform was searched for vessel-related datasets — no AIS or vessel
tracking data was found.

### Japan — Japan Coast Guard (JCG)

| Item | Status |
|---|---|
| Maritime authority | 海上保安庁 (JCG) |
| AIS API | ❌ Not found |
| Notes | Operates extensive AIS network; AIS data used for marine traffic safety |

Japan Coast Guard operates one of the most comprehensive AIS networks in Asia, covering
Tokyo Bay, Osaka Bay, Seto Inland Sea, and other critical waterways. However, data access
is restricted to operational and research purposes. No public API was discovered.

### South Korea — KOMSA / MOF

| Item | Status |
|---|---|
| Maritime authority | Korea Maritime Safety Tribunal (KOMSA) / Ministry of Oceans and Fisheries (MOF) |
| AIS API | ❌ Not found |
| GICOMS | Korea operates GICOMS (General Information Center on Maritime Safety & Security) |

South Korea operates GICOMS, an integrated maritime safety information system with AIS
coverage of Korean waters. The system is accessible to registered operational users
(shipping companies, port authorities) but not as a public API.

### Australia — AMSA (Australian Maritime Safety Authority)

| Item | Status |
|---|---|
| Website | `amsa.gov.au` |
| AIS API | ❌ Not found |
| AIS data page | 404 at `amsa.gov.au/safety-navigation/navigation-systems/ais-data` |

AMSA operates a shore-based AIS network around the Australian coast. Historical AIS data
has been used in research collaborations but no public real-time API was found. The previous
AIS data information page now returns 404.

### New Zealand — Maritime NZ

| Item | Status |
|---|---|
| Maritime authority | Maritime New Zealand |
| AIS API | ❌ Not found |
| Notes | LRIT and AIS used for SAR and vessel monitoring |

New Zealand's maritime authority uses AIS for safety and search-and-rescue purposes.
No public data access was found.

### India — DGS / DGPS / VTMS

| Item | Status |
|---|---|
| Maritime authority | Directorate General of Shipping (DGS) |
| VTS | VTMS systems at major ports (Mumbai, Chennai, Cochin, etc.) |
| AIS API | ❌ Not found |

India has been expanding its Vessel Traffic Management Systems (VTMS) at major ports with
AIS integration. These are operational systems managed by individual port trusts. No
centralized public AIS API exists.

## Americas

### Canada — CCG (Canadian Coast Guard)

| Item | Status |
|---|---|
| Maritime authority | Canadian Coast Guard (CCG) |
| MCTS | Marine Communications and Traffic Services |
| AIS API | ❌ Not found |
| open.canada.ca | No real-time AIS datasets found |

Canada's CCG operates MCTS with AIS integration across Canadian waters. AIS data is used
operationally and for marine traffic analysis. The open.canada.ca portal does not list
real-time AIS datasets, though historical AIS data has been shared for research purposes
through specific agreements.

### Brazil — Marinha do Brasil

| Item | Status |
|---|---|
| Maritime authority | Diretoria de Hidrografia e Navegação (DHN) |
| AIS API | ❌ Not found |
| SISTRAM | Brazil operates SISTRAM (Sistema de Informações sobre o Tráfego Marítimo) |

Brazil's Navy operates SISTRAM for vessel traffic monitoring along the extensive Brazilian
coast. This is a classified operational system with no public API.

## Africa

### South Africa — SAMSA

| Item | Status |
|---|---|
| Maritime authority | South African Maritime Safety Authority (SAMSA) |
| AIS API | ❌ Not found |
| Notes | AIS coverage focused on major ports (Durban, Cape Town, Richards Bay) |

SAMSA operates AIS shore stations at major South African ports. Data access is restricted
to operational purposes.

## Mediterranean

### Italy — IMAT (Italian Maritime Authority)

| Item | Status |
|---|---|
| Maritime authority | Guardia Costiera / Comando Generale delle Capitanerie di Porto |
| AIS/VTS | IMAT system covers Italian waters |
| AIS API | ❌ Not found |

Italy operates the IMAT (Integrated Maritime Assistance and Traffic) system with
comprehensive AIS coverage. Data is shared with EMSA SafeSeaNet for European vessel
tracking but not publicly accessible.

### Greece — HCGS (Hellenic Coast Guard)

| Item | Status |
|---|---|
| Maritime authority | Λιμενικό Σώμα (HCGS) |
| AIS API | ❌ Not found |
| Notes | AIS network covers Greek islands and shipping lanes |

Greece operates extensive AIS coverage given its massive archipelago and heavy international
shipping traffic. No public data access found.

### Turkey — Coastal AIS

| Item | Status |
|---|---|
| Maritime authority | Directorate General of Coastal Safety (Kıyı Emniyeti) |
| AIS/VTS | Turkish Straits VTS (Bosphorus/Dardanelles) |
| AIS API | ❌ Not found |

Turkey operates critical VTS systems for the Turkish Straits (Bosphorus and Dardanelles),
among the most important and dangerous shipping passages in the world. AIS data is tightly
controlled for safety and security reasons.

## Conclusions

The pattern is clear and consistent across all investigated countries:

1. **Every maritime nation operates shore-based AIS** — the infrastructure exists everywhere.
2. **Almost none make it publicly accessible** via API — it's treated as operational/security
   data.
3. **Norway and Finland are the exceptions** — their open data policies extend to AIS, making
   them genuine outliers in global maritime data transparency.
4. **HELCOM provides aggregate access** — Baltic states share AIS data through HELCOM, but
   only as processed traffic intensity maps, not real-time positions.
5. **EU SafeSeaNet** aggregates European AIS data, but access is restricted to member state
   maritime authorities.
6. **Academic access** exists in some countries (Denmark, Canada, Australia) through specific
   research agreements, but not via public APIs.

For real-time government AIS data, the project should focus on the known open sources:
- **Norway**: Kystverket raw TCP + BarentsWatch structured API
- **Finland**: Digitraffic Maritime MQTT + REST
- **Commercial alternatives**: Spire/Kpler (satellite), AISHub/AISstream (community)
