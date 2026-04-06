# Maritime AIS Vessel Tracking — Candidate Sources

Research date: 2026-04-06 (updated — Round 2 deep dive)

## Summary

Scouted for real-time or near-real-time AIS vessel tracking APIs beyond the three already
covered in this repository. Found **6 confirmed candidates**, **2 aggregate intelligence sources**,
**1 consolidated government survey** (20+ countries), and **1 investigation report** (Denmark DMA).

The Round 2 deep dive investigated government AIS programs across 20+ countries, alternative
marine data sources (vessel density, port statistics, satellite AIS), and regional marine
data networks. Key finding: Norway and Finland remain the only countries with truly open
real-time AIS APIs. All other investigated governments restrict AIS data to operational use.

## Already Covered in Repository

| Source | Directory | Protocol | Coverage |
|---|---|---|---|
| Norway Kystverket AIS | `kystverket-ais/` | Raw TCP/NMEA | Norwegian waters |
| Finland Digitraffic Maritime | `digitraffic-maritime/` | MQTT over WebSocket | Baltic Sea |
| AISstream.io | `aisstream/` | WebSocket | Global (currently broken) |

## Dismissed

| Source | Reason |
|---|---|
| USA MarineCadastre | Historical only, not real-time |
| USCG NAIS | Restricted access, not public |

## New Candidates — Ranked by Feasibility

### Tier 1: Excellent (16+ / 18)

| # | Source | Score | File | Key Advantage |
|---|---|---|---|---|
| 1 | [Finland Digitraffic Maritime REST](digitraffic-maritime-rest.md) | 17/18 | `digitraffic-maritime-rest.md` | No auth, GeoJSON, exceptionally rich port call data |
| 2 | [BarentsWatch AIS Live](barentswatch-ais.md) | 16/18 | `barentswatch-ais.md` | Structured JSON streaming over same Kystverket data |

### Tier 2: Good (12-15 / 18)

| # | Source | Score | File | Key Advantage |
|---|---|---|---|---|
| 3 | [Spire/Kpler Maritime](spire-kpler-maritime.md) | 15/18 | `spire-kpler-maritime.md` | Global satellite AIS, GraphQL, but commercial |
| 4 | [EMODnet Human Activities](emodnet-human-activities.md) | 13/18 | `emodnet-human-activities.md` | EU vessel density WMS/WFS, port traffic stats |
| 5 | [AISHub](aishub.md) | 13/18 | `aishub.md` | Global community network, 860+ stations |
| 6 | [MyShipTracking](myshiptracking.md) | 13/18 | `myshiptracking.md` | Vessels-in-zone queries, fleet management |
| 7 | [aprs.fi AIS](aprs-fi-ais.md) | 12/18 | `aprs-fi-ais.md` | Free, but lookup-only (no area monitoring) |
| 8 | [Datalastic](datalastic.md) | 12/18 | `datalastic.md` | Detailed vessel type taxonomy |

### Tier 3: Aggregate Intelligence (not real-time)

| # | Source | Score | File | Key Value |
|---|---|---|---|---|
| 9 | [HELCOM Shipping Data](helcom-shipping.md) | 11/18 | `helcom-shipping.md` | Baltic Sea traffic intensity, accident data |

### Tier 4: Investigation Reports

| # | Source | Score | File | Status |
|---|---|---|---|---|
| 10 | [Denmark DMA AIS](denmark-dma-ais.md) | 2/18 | `denmark-dma-ais.md` | No public API found; system transferred to DEMA |
| 11 | [Government AIS Programs](government-ais-programs.md) | — | `government-ais-programs.md` | Survey of 20+ countries — none offer public AIS APIs |

### Africa-Focused

| # | Source | Score | File | Key Value |
|---|---|---|---|---|
| 12 | [ASAM Africa Piracy](asam-africa-piracy.md) | 14/18 | `asam-africa-piracy.md` | NGA anti-piracy data for Gulf of Guinea, Horn of Africa |
| 13 | [Africa AIS Coastal](africa-ais-coastal.md) | 12/18 | `africa-ais-coastal.md` | AIS coverage for Suez Canal, Cape route, Gulf of Guinea |

## Recommendations

### For immediate integration:

1. **BarentsWatch AIS Live** — This is the clear winner for a new integration. It wraps the same
   Norwegian AIS data already available via raw TCP in kystverket-ais, but through a modern
   REST/JSON streaming API with OAuth2 auth, GeoJSON output, and an OpenAPI spec. Could
   potentially replace the raw TCP integration entirely.

2. **Digitraffic Maritime REST** — The REST API complements the existing MQTT integration. The
   port call data alone justifies adding REST endpoints: it's the richest open port call
   dataset available, with agent info, berth assignments, cargo declarations, crew counts,
   and security levels.

### For evaluation:

3. **AISHub** — Worth evaluating if the project operates its own AIS receiver. The reciprocal
   sharing model means you must contribute to access, but the global coverage from 860+ stations
   is unique among non-commercial sources.

4. **EMODnet Human Activities** — Not real-time, but the vessel density WMS/WFS services are
   valuable as contextual layers. Port vessel statistics by type and tonnage provide useful
   aggregate intelligence. No auth required.

### Commercial benchmarks:

5. **Spire/Kpler Maritime** — The GraphQL API is the gold standard for AIS API design. Worth
   studying for API design patterns even if the commercial license makes it unsuitable for
   open-data projects. Trial available.

### Not recommended for immediate action:

6. **MyShipTracking**, **Datalastic**, **aprs.fi** — All require paid subscriptions or have
   significant limitations. Their value proposition overlaps with the open government sources
   that score higher on openness.

7. **HELCOM Shipping** — Useful for Baltic research context but not real-time data integration.

## Countries/Regions Investigated — No Public AIS API Found

The [government-ais-programs.md](government-ais-programs.md) survey documents detailed findings
for 20+ countries. Key conclusions:

- **Every maritime nation operates shore-based AIS** — the infrastructure is universal.
- **Almost none provide public API access** — AIS is treated as operational/security data.
- **Norway and Finland are global outliers** in open maritime AIS data.
- **No new government AIS APIs were discovered** in Round 2 despite investigating:
  Sweden, Denmark, Estonia, Latvia, Lithuania, Canada, Singapore, Japan, South Korea,
  Australia, New Zealand, India, Brazil, South Africa, Italy, Greece, Turkey.

### Satellite AIS (commercial):
- **Spire/Kpler**: Global coverage, GraphQL API, commercial licensing. Already documented.
- **exactEarth**: Acquired by Kpler — merged into Kpler AIS platform.
- **ORBCOMM**: Satellite AIS via OG2 constellation, enterprise-only API.
- **Academic access**: Some providers offer academic/research programs (Spire, historically
  exactEarth), but these require institutional agreements and are not self-service APIs.

### Regional marine data:
- **EMODnet**: EU vessel density and port statistics. Documented above.
- **HELCOM**: Baltic Sea AIS-derived aggregate data. Documented above.
- **Arctic vessel tracking**: No dedicated public API found. Polar vessel monitoring relies on
  satellite AIS (commercial) and national AIS within coastal range.

The Nordic countries (Norway, Finland) remain the global leaders in open maritime AIS data
accessibility. BarentsWatch and Digitraffic are both government-backed, well-documented, and
freely accessible — a model that other maritime nations have not replicated.

### Asia & Middle East — Deep Dive Round 5

| # | Source | Score | File | Key Value |
|---|--------|-------|------|-----------|
| 14 | [Critical Chokepoints](critical-chokepoints-asia-mideast.md) | 16/18 | `critical-chokepoints-asia-mideast.md` | Malacca Strait, Bosphorus, Hormuz — AIS monitoring analysis |

**Key finding**: Three of the world's most critical maritime chokepoints (Malacca, Bosphorus, Hormuz) are in the Asia/Middle East region. This document analyzes AIS data availability and monitoring approaches for each, connecting to existing AIS infrastructure (Digitraffic, Kystverket, AISstream) and identifying regional gaps.
