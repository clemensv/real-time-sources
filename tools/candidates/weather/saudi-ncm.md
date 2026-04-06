# Saudi Arabia PME — Presidency of Meteorology and Environment

**Country/Region**: Saudi Arabia
**Publisher**: National Centre for Meteorology (NCM, formerly PME)
**API Endpoint**: `https://ncm.gov.sa/` (web portal)
**Documentation**: https://ncm.gov.sa/
**Protocol**: Web portal (HTML/Arabic)
**Auth**: N/A
**Data Format**: HTML
**Update Frequency**: Synoptic observations; daily forecasts
**License**: Saudi government data

## What It Provides

Saudi Arabia's National Centre for Meteorology monitors weather across the world's largest country without permanent rivers. The Arabian Peninsula presents extreme meteorological conditions:

- **Extreme heat**: Regularly 50°C+ in summer; Saudi cities among the hottest inhabited places
- **Haboobs**: Massive dust/sand storms
- **Flash floods**: Rare but devastating — wadi floods in mountainous Asir and Hejaz regions
- **Shamal winds**: Strong northwesterly winds affecting the Persian Gulf
- **Hajj weather**: Mecca/Mina weather monitoring for 2M+ annual pilgrims (heat stroke risk)
- **NEOM/Line City**: Saudi Arabia's futuristic city projects need detailed climate data

### Saudi Open Data

Saudi Arabia has `data.gov.sa` open data portal, but it was inaccessible during testing (connection failure). Saudi Arabia's Vision 2030 includes digitalization goals that may lead to open weather APIs.

### Riyadh Metro

Riyadh is building one of the world's largest single-phase metro projects (6 lines, 176 km, 85 stations). Real-time transit data for this system would be significant once operational.

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Data exists |
| Openness | 0 | No API; data.gov.sa inaccessible |
| Stability | 1 | Government service |
| Structure | 0 | HTML; Arabic primary |
| Identifiers | 1 | Station names; ICAO codes for airports |
| Additive Value | 2 | Arabian Peninsula coverage; Hajj weather; extreme heat monitoring |
| **Total** | **5/18** | |

## Verdict

Documented gap. Saudi Arabia has meteorological infrastructure but no public API. The Hajj weather monitoring dimension is unique (heat stroke prevention for 2M+ pilgrims). Vision 2030 digitalization may yield APIs in the future. The upcoming Riyadh Metro would be an interesting transit data source once operational.
