# Vaisala GLD360 / NLDN (Commercial Lightning Detection)

**Country/Region**: Global (GLD360) / United States (NLDN)
**Publisher**: Vaisala Oyj (Finland)
**API Endpoint**: N/A — commercial subscription required
**Documentation**: https://www.vaisala.com/en/products/systems/lightning-detection
**Protocol**: Proprietary commercial feed
**Auth**: Commercial license/subscription
**Data Format**: Proprietary
**Update Frequency**: Real-time
**License**: Commercial — all rights reserved

## What It Provides

Vaisala operates two premier lightning detection networks:

- **GLD360** (Global Lightning Dataset 360) — Global lightning detection network with claimed >80% detection efficiency worldwide and median location accuracy <5 km.
- **NLDN** (National Lightning Detection Network) — The US national network with >95% detection efficiency and median accuracy <200m for cloud-to-ground strokes.

These are the industry-standard commercial lightning data products used by aviation, utilities, insurance, and weather services.

## API Details

No public API. Access requires a commercial subscription or data license agreement with Vaisala. Data delivery options typically include:
- Real-time feed via proprietary protocols
- Batch file delivery
- Web portal access
- Integration with weather data platforms (DTN, WSI, etc.)

## Freshness Assessment

Excellent for subscribers — real-time delivery with sub-second latency. However, not accessible for open data integration.

## Entity Model

Lightning stroke/flash data includes:
- Timestamp (sub-microsecond)
- Location (lat/lon, altitude estimate)
- Peak current (kA)
- Polarity (+CG, -CG)
- Multiplicity (number of strokes per flash)
- Flash/stroke classification
- Quality/confidence metrics

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time commercial feed |
| Openness | 0 | Commercial only, no public access |
| Stability | 3 | Enterprise-grade commercial service |
| Structure | 3 | Well-defined data model (for subscribers) |
| Identifiers | 3 | Flash/stroke IDs provided |
| Additive Value | 3 | Gold standard lightning data |
| **Total** | **15/18** | |

## Notes

- **DISMISSED** — Commercial product with no open/free tier. Included for completeness and comparison.
- Vaisala's NLDN is the de facto standard for US lightning data and is used by NOAA, FAA, and most US utilities.
- GLD360 is the global equivalent, used by international aviation and meteorological agencies.
- Some national weather services that subscribe to Vaisala data may redistribute it in limited form.
- For open alternatives, see Blitzortung.org (community) or national met service lightning products.
