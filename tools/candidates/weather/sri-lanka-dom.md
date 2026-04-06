# Sri Lanka Department of Meteorology

**Country/Region**: Sri Lanka
**Publisher**: Department of Meteorology, Ministry of Defence
**API Endpoint**: `https://www.meteo.gov.lk/` (web portal)
**Documentation**: https://www.meteo.gov.lk/
**Protocol**: Web portal (HTML)
**Auth**: N/A
**Data Format**: HTML
**Update Frequency**: 3-hourly observations; cyclone bulletins during Bay of Bengal events
**License**: Sri Lankan government data

## What It Provides

Sri Lanka's meteorological department monitors weather for an island nation (22M people) positioned in the Indian Ocean, facing:
- **Tropical cyclones**: Bay of Bengal storms regularly affect eastern/northern coasts
- **Southwest and Northeast monsoons**: Two monsoon seasons bring 80% of annual rainfall
- **Floods and landslides**: Central hill country prone to mass casualties
- **Drought**: Dry zone (north-central) experiences periodic drought
- **Marine weather**: Critical for fishing fleet (~250,000 fishermen) and tea plantation logistics

### Probe Results

Not directly probed. Based on available information, the Department of Meteorology provides:
- Weather bulletins via website
- SMS-based warnings
- Media briefings during severe weather
- No public API has been documented

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Data exists; web only |
| Openness | 0 | No API |
| Stability | 1 | Government agency |
| Structure | 0 | HTML |
| Identifiers | 1 | Station names |
| Additive Value | 2 | Island nation; monsoon/cyclone exposure; but small network |
| **Total** | **5/18** | |

## Verdict

Documented gap. Sri Lanka has weather monitoring infrastructure but no public API. The country's position in the Indian Ocean and monsoon exposure make this data relevant, but the small network size and lack of API make it a low-priority target. Indian IMD data provides partial coverage for the region.
