# Panama Canal — Maritime Traffic

**Country/Region**: Panama (Canal Zone)
**Publisher**: Autoridad del Canal de Panamá (ACP)
**API Endpoint**: Not found
**Documentation**: https://www.pancanal.com/
**Protocol**: Unknown
**Auth**: Unknown
**Data Format**: Unknown
**Update Frequency**: Real-time (vessel transits occur 24/7)
**License**: Panamanian state entity

## What It Provides

The Panama Canal is one of the world's most critical maritime chokepoints — approximately 5% of world trade transits the canal annually. The expanded canal (Neopanamax locks, opened 2016) handles vessels up to 366m length and 49m beam.

Potential data of interest:
- **Vessel transit scheduling**: Queue positions, expected transit times
- **Water level / lake levels**: Gatun Lake level is critical — drought conditions in 2023 forced transit restrictions
- **Transit counts**: Daily number of vessels transited
- **Draft restrictions**: Maximum vessel draft varies with Gatun Lake level
- **Auction prices**: For priority transit slots (can exceed $4M during peak demand)

## API Details

No public API found:

```
https://pancanal.com/en/maritime-operations/vessel-information/ → 404
https://www.pancanal.com/api/vessels → 404
```

The ACP website provides PDF reports and dashboards for transit statistics. Real-time vessel positions in the canal approaches are visible on AIS platforms (MarineTraffic, VesselFinder).

### Alternative Data Sources

- **AIS feeds** (see maritime-ais/) provide vessel positions in canal approaches
- **Kystverket/AISHub** data includes ships in Panama Canal anchorage
- **ACP monthly reports**: Published as PDFs with transit counts by vessel type

## Integration Notes

- The 2023 drought (low Gatun Lake levels) restricted transits to 22/day (from normal 36), causing massive shipping disruption — real-time lake level data would be invaluable
- Canal transit data is commercially sensitive — the ACP likely restricts API access
- AIS data provides ship positions in the approaches but not queue/scheduling information
- The canal's draft restrictions directly impact global commodity shipping routes (LNG, containers, bulk)
- El Niño correlation: ENSO events affect Panama rainfall, Gatun Lake level, and therefore canal capacity

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 0 | No data access found |
| Openness | 0 | No API; commercially sensitive data |
| Stability | 1 | ACP is a major international institution |
| Structure | 0 | Cannot assess |
| Identifiers | 0 | Cannot assess |
| Additive Value | 3 | 5% of world trade; drought/climate vulnerability |
| **Total** | **4/18** | |

## Verdict

⏭️ **Skip** — No public API. Panama Canal operational data is commercially sensitive. AIS feeds provide vessel position data in the approaches. Gatun Lake level data (critical for transit capacity) would be the most valuable single data point if it became available.
