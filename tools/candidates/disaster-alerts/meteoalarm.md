# Meteoalarm (European Weather Warnings)
**Country/Region**: Europe (30+ countries)
**Publisher**: EUMETNET (Network of European National Meteorological Services)
**API Endpoint**: `https://feeds.meteoalarm.org/api/v1/warnings/feeds-{country}`
**Documentation**: https://feeds.meteoalarm.org/
**Protocol**: REST / CAP-based JSON
**Auth**: None
**Data Format**: JSON (CAP-structured warnings)
**Update Frequency**: Real-time (as national met services issue warnings)
**License**: Open (EUMETNET member services)

## What It Provides
Meteoalarm aggregates severe weather warnings from all European national meteorological services into a single feed. Warning types include:
- Wind, storms, hurricanes
- Rain, flooding
- Snow, ice
- Thunderstorms, lightning
- Extreme temperatures (heat/cold)
- Fog, avalanche, coastal events
- Forest fire risk

Each warning includes awareness level (green/yellow/orange/red) and awareness type codes.

## API Details
- **Country feed**: `https://feeds.meteoalarm.org/api/v1/warnings/feeds-{country}` where `{country}` is lowercase English name (e.g., `feeds-france`, `feeds-germany`)
- **Response structure**: JSON array of `warnings`, each containing a full CAP `alert` object
- **CAP fields**: `identifier`, `sender`, `sent`, `status`, `msgType`, `scope`
- **Info block**: `category`, `event`, `urgency`, `severity`, `certainty`, `headline`, `description`, `instruction`, `web`
- **Area block**: `areaDesc` with NUTS3 geocodes
- **Parameters**: `awareness_level` (0-3 with color) and `awareness_type` (numbered hazard types)
- **Multi-language**: Each warning typically includes both native language and English info blocks

## Freshness Assessment
Excellent. Warnings are pushed as soon as national services issue them. Data confirmed live with current-day timestamps. Legacy RSS feeds were sunset January 2026 in favor of this JSON/Atom API.

## Entity Model
- **Alert** (identifier, sender, sent, msgType, status, scope, uuid)
- **Info** (event, severity, urgency, certainty, headline, description, instruction, language, web)
- **Area** (areaDesc, geocode with NUTS3 codes)
- **Parameters** (awareness_level, awareness_type)

## Feasibility Rating
| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | Real-time as warnings are issued |
| Openness | 3 | No auth, public API |
| Stability | 3 | EUMETNET consortium, operational since 2007 |
| Structure | 3 | Clean JSON with CAP structure, NUTS3 geocodes |
| Identifiers | 3 | CAP identifiers, NUTS3 area codes |
| Additive Value | 3 | Pan-European severe weather in one feed |
| **Total** | **18/18** | |

## Notes
- The API migrated from RSS to JSON/Atom in January 2026
- Country names in the endpoint must be lowercase English
- Some countries may have limited or delayed data availability
- Excellent candidate: clean JSON, standard CAP structure, no auth, broad geographic coverage
