# PHIVOLCS — Philippine Volcanic Monitoring

**Country/Region**: Philippines
**Publisher**: Philippine Institute of Volcanology and Seismology (PHIVOLCS-DOST)
**API Endpoint**: `https://www.phivolcs.dost.gov.ph/` (web portal — connection failed)
**Documentation**: https://www.phivolcs.dost.gov.ph/
**Protocol**: Web portal (HTML)
**Auth**: N/A
**Data Format**: HTML
**Update Frequency**: Daily volcanic advisories; continuous monitoring during elevated activity
**License**: Philippine government data

## What It Provides

The Philippines has **24 classified active volcanoes** — one of the highest concentrations of volcanic hazards in the world. PHIVOLCS maintains a 5-level Alert Level System:

| Level | Classification | Description |
|-------|---------------|-------------|
| 0 | No Alert | Background/normal |
| 1 | Abnormal | Low-level unrest |
| 2 | Increasing Unrest | Moderate seismicity/gas |
| 3 | Increased Tendency | Magmatic intrusion |
| 4 | Hazardous Eruption Imminent | Intense activity |
| 5 | Hazardous Eruption Ongoing | Active eruption |

### Key Monitored Volcanoes

- **Taal** (Batangas, near Manila): Erupted January 2020; ~1M people in caldera hazard zone
- **Mayon** (Albay): Most active; 50+ historical eruptions; perfect stratovolcano
- **Pinatubo** (Zambales/Tarlac/Pampanga): 1991 VEI-6 eruption; still lahar-prone
- **Kanlaon** (Negros): Erupted 2024; phreatic explosions
- **Bulusan** (Sorsogon): Frequent phreatic events
- **Mount Apo** (Mindanao): Tallest Philippine peak; geothermal

### Monitoring Data Types

- **Volcanic earthquakes**: Tremor type and count (harmonic tremor, explosion quakes)
- **SO₂ flux**: Gas emission measurements
- **Ground deformation**: Tilt, GPS, InSAR
- **Crater observations**: Visual, thermal imaging
- **Lahar monitoring**: Rain gauges + wire sensors on major drainages

## Probe Results

Connection to `phivolcs.dost.gov.ph` **failed** (timeout). Same result as the seismology endpoint. PHIVOLCS web infrastructure appears to have connectivity issues from international origins.

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Daily bulletins during normal; hourly during eruption; but inaccessible |
| Openness | 0 | Connection failed; no API |
| Stability | 1 | Agency exists and functions; web infrastructure unreliable |
| Structure | 0 | HTML/PDF bulletins only |
| Identifiers | 2 | Named volcanoes; alert levels standardized |
| Additive Value | 3 | 24 active volcanoes; Taal/Mayon/Pinatubo are globally significant |
| **Total** | **8/18** | |

## Integration Notes

- **Not currently viable** — infrastructure inaccessible
- Alternative: Smithsonian Global Volcanism Program (GVP) at `volcano.si.edu` aggregates PHIVOLCS bulletins
- MIROVA satellite thermal monitoring covers Philippine volcanoes
- The existing `magma-indonesia-pvmbg.md` candidate covers Indonesian volcanoes via similar agency
- If PHIVOLCS becomes API-accessible, it would be one of the most valuable volcanic monitoring additions
- Philippine volcanic monitoring is particularly valuable because of the population density near active volcanoes

## Verdict

High geoscientific importance, zero API accessibility. Philippine volcanoes are among the world's most monitored and most dangerous. PHIVOLCS data is available through intermediaries (GVP, MIROVA) but the primary source remains web-only. A significant gap in the volcanic monitoring domain.
