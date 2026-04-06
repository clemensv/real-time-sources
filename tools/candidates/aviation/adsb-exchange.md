# ADS-B Exchange
**Country/Region**: Global
**Publisher**: ADS-B Exchange (community project, now ADSBx LLC)
**API Endpoint**: `https://adsbexchange.com/data/` (various tiers)
**Documentation**: https://www.adsbexchange.com/data/
**Protocol**: REST
**Auth**: API Key (paid tiers), RapidAPI integration
**Data Format**: JSON
**Update Frequency**: Real-time (~1-second update intervals)
**License**: Proprietary / paid API tiers

## What It Provides
ADS-B Exchange is one of the largest unfiltered ADS-B aircraft tracking networks:
- **Unfiltered data**: Unlike FlightRadar24 and FlightAware, ADS-B Exchange does not filter out military, government, or sensitive aircraft (unless legally compelled)
- **State vectors**: Real-time aircraft positions, altitude, speed, heading
- **Aircraft metadata**: Registration, aircraft type, operator
- **Historical traces**: Aircraft track history
- **Coverage**: Global via volunteer feeder network

## API Details
- **RapidAPI access**: `https://rapidapi.com/adsbx/api/adsbx-flight-sim-traffic`
- **API tiers**:
  - Individual: ~$10/month — basic access
  - Professional: Higher rate limits
  - Enterprise: Full firehose
- **Endpoints**:
  - Aircraft by ICAO hex: `/v2/hex/{icao24}`
  - Aircraft by registration: `/v2/reg/{registration}`
  - Aircraft by callsign: `/v2/callsign/{callsign}`
  - Aircraft by location: `/v2/lat/{lat}/lon/{lon}/dist/{nm}/`
  - All aircraft (firehose): Enterprise tier only
- **Response fields**: hex (ICAO24), flight (callsign), lat, lon, alt_baro, alt_geom, gs, track, baro_rate, squawk, category, type, registration, ownOp, year, mil (military flag), etc.

## Freshness Assessment
Excellent. Data updates approximately every second. The unfiltered nature means military and government aircraft are visible. Coverage depends on feeder network density.

## Entity Model
- **Aircraft** (hex/ICAO24, registration, type, category, ownOp/operator, year, mil flag)
- **State** (lat, lon, alt_baro, alt_geom, gs, track, baro_rate, geom_rate, squawk, emergency, spi, nav_modes)
- **Flight** (callsign, origin, destination)

## Feasibility Rating
| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | ~1-second updates |
| Openness | 1 | Paid API, no free tier |
| Stability | 2 | Commercial company, API tiers may change |
| Structure | 3 | Clean JSON, well-documented |
| Identifiers | 3 | ICAO24 hex, registrations, callsigns |
| Additive Value | 3 | Unfiltered tracking, military included |
| **Total** | **15/18** | |

## Notes
- The "unfiltered" policy is the key differentiator — military/government aircraft not blocked
- Paid API may be a barrier for open-source projects
- ADS-B Exchange also provides tar1090 and readsb open-source software for local receivers
- The feeder community is large and growing
- Data is noisier than curated sources (FlightAware, FR24) but more complete
- Consider combining with OpenSky for academic/non-commercial use cases
