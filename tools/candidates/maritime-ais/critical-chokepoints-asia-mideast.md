# Strait of Malacca / Bosphorus / Hormuz — Critical Maritime Chokepoints

**Country/Region**: International (Southeast Asia, Turkey, Middle East)
**Publisher**: Various national maritime authorities
**API Endpoint**: Various (AIS-based monitoring)
**Documentation**: N/A (composite research document)
**Protocol**: AIS (Automatic Identification System) VHF broadcast
**Auth**: Various
**Data Format**: AIS NMEA sentences
**Update Frequency**: Real-time (AIS position reports every 2-30 seconds)
**License**: Various

## What This Covers

Three of the world's most strategically critical maritime chokepoints fall within our research regions:

### Strait of Malacca (Malaysia/Indonesia/Singapore)
- **40% of global trade** transits this strait
- ~100,000 vessel transits per year
- Singapore's MPA monitors traffic heavily
- Width narrows to 2.8 km at Phillips Channel
- Singapore LTA/MPA data already in candidate pool

### Bosphorus Strait (Turkey)
- Connects Black Sea to Mediterranean
- ~50,000 transits/year (including massive oil tankers)
- Turkey's Directorate General of Coastal Safety monitors
- One of the most dangerous waterways for large vessels
- Istanbul IBB data (already in candidates) may include maritime

### Strait of Hormuz (Iran/Oman/UAE)
- **30% of global seaborne oil** transits here
- ~80 tankers daily
- Iran, Oman, and UAE monitor
- Geopolitically one of the most sensitive waterways on Earth

### AIS Data Availability

AIS data for these straits is available through:
- **Existing candidates**: `aisstream`, `aishub`, `barentswatch-ais`, `government-ais-programs`
- **MarineTraffic**: Commercial aggregator with chokepoint coverage
- **VesselFinder**: Commercial AIS aggregator
- **National VTS (Vessel Traffic Service)**: Each strait has a traffic management system

### Unique Value

The chokepoint dimension adds real-time supply chain intelligence — a domain not currently well-represented in the repository. Vessel transit counts and dwell times at these chokepoints correlate with:
- Oil price movements (Hormuz)
- Global supply chain disruptions (Malacca)
- Black Sea grain exports (Bosphorus)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | AIS is inherently real-time |
| Openness | 1 | AIS receivers are open; aggregated data is commercial |
| Stability | 3 | AIS is mandated by IMO for all vessels >300GT |
| Structure | 3 | AIS format is standardized (ITU-R M.1371) |
| Identifiers | 3 | MMSI, IMO numbers, vessel names |
| Additive Value | 3 | Critical chokepoints; supply chain intelligence |
| **Total** | **16/18** (for AIS at chokepoints) | |

## Verdict

Covered by existing AIS candidates but worth highlighting the regional chokepoint dimension. The Strait of Malacca, Bosphorus, and Strait of Hormuz represent three of the most strategically important real-time monitoring points on Earth. Existing AIS data sources in the candidate pool can be filtered for these chokepoints.
