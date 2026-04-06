# Maritime AIS Vessel Tracking — Candidate Sources

Research date: 2026-04-06

## Summary

Scouted for real-time or near-real-time AIS vessel tracking APIs beyond the three already
covered in this repository. Found **6 confirmed candidates** and **1 investigation report**
(Denmark DMA — no public API discovered).

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
| 4 | [AISHub](aishub.md) | 13/18 | `aishub.md` | Global community network, 860+ stations |
| 5 | [MyShipTracking](myshiptracking.md) | 13/18 | `myshiptracking.md` | Vessels-in-zone queries, fleet management |
| 6 | [aprs.fi AIS](aprs-fi-ais.md) | 12/18 | `aprs-fi-ais.md` | Free, but lookup-only (no area monitoring) |
| 7 | [Datalastic](datalastic.md) | 12/18 | `datalastic.md` | Detailed vessel type taxonomy |

### Tier 3: Investigation Needed

| # | Source | Score | File | Status |
|---|---|---|---|---|
| 8 | [Denmark DMA AIS](denmark-dma-ais.md) | 2/18 | `denmark-dma-ais.md` | No public API found; system transferred to DEMA |

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

### Commercial benchmarks:

4. **Spire/Kpler Maritime** — The GraphQL API is the gold standard for AIS API design. Worth
   studying for API design patterns even if the commercial license makes it unsuitable for
   open-data projects. Trial available.

### Not recommended for immediate action:

5. **MyShipTracking**, **Datalastic**, **aprs.fi** — All require paid subscriptions or have
   significant limitations. Their value proposition overlaps with the open government sources
   that score higher on openness.

## Countries/Regions Not Yet Covered (Further Research Needed)

These were investigated but no accessible public AIS API was found:

- **Sweden (Sjöfartsverket)** — No open data portal or AIS API discovered. The Swedish Maritime
  Administration website does not list AIS data as an open service.
- **Estonia (Transpordiamet)** — No public AIS API found. Transport Administration site is
  focused on road transport.
- **Latvia, Lithuania** — No public AIS APIs found.
- **Singapore (MPA)** — No public vessel tracking API found on data.gov.sg.
- **Japan, Australia, Italy** — No public AIS APIs found during search.
- **Canada (CCG)** — CCG website unreachable; no API found on open.canada.ca.

The Nordic countries (Norway, Finland) remain the global leaders in open maritime AIS data
accessibility. BarentsWatch and Digitraffic are both government-backed, well-documented, and
freely accessible — a model that other maritime nations have not replicated.
