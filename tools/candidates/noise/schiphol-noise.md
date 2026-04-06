# Schiphol Airport Noise Monitoring (NOMOS)
**Country/Region**: Netherlands (Amsterdam Schiphol Airport)
**Publisher**: Royal Schiphol Group / KNMI / Bewoners Aanspreekpunt Schiphol (BAS)
**API Endpoint**: `https://nomos.nl/` (monitoring platform)
**Documentation**: https://www.bezoekbas.nl/ (BAS — Community Noise Portal)
**Protocol**: Web / RSS / Data downloads
**Auth**: None (public portal)
**Data Format**: HTML / CSV exports
**Update Frequency**: Near real-time (continuous noise monitoring, flight-correlated)
**License**: Open (public information)

## What It Provides
Schiphol Airport operates one of the world's most extensive aircraft noise monitoring networks (NOMOS — Noise Monitoring System):
- Continuous noise level measurements (LAeq, LAmax, SEL)
- Flight-correlated noise events (linking noise measurements to specific flights)
- 40+ fixed noise monitoring terminals around the airport
- Noise contour maps
- Runway usage statistics
- Flight track data
- Community noise complaint data

The BAS (Bewoners Aanspreekpunt Schiphol) provides a public-facing community portal with noise data.

## API Details
- **NOMOS Portal**: `https://nomos.nl/` — Schiphol's noise monitoring platform
- **BAS Community Portal**: `https://www.bezoekbas.nl/` — public noise data and reports
- **Sensornet**: Real-time noise levels from monitoring terminals
- **Data exports**: Historical noise data available as downloads
- **Flight tracking**: Integrated with ATC data for flight-noise correlation
- **Annual reports**: Comprehensive noise exposure reports (Handhavingsrapportages)

Note: Schiphol's noise monitoring is among the most sophisticated globally, but the public API access is limited compared to the internal systems. Data is primarily available through the web portals and periodic reports.

## Freshness Assessment
Moderate. Noise monitoring is continuous and near real-time in the NOMOS system, but public-facing data may be delayed or aggregated. The BAS portal provides recent data but not a formal real-time API. Periodic data exports are available.

## Entity Model
- **Monitoring Terminal** (ID, location, lat/lon, type)
- **Noise Event** (timestamp, LAmax, SEL, duration, correlated flight)
- **Flight** (callsign, aircraft type, runway, track)
- **Noise Level** (timestamp, LAeq, monitoring terminal)
- **Noise Contour** (annual, Lden/Lnight contour lines)

## Feasibility Rating
| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 2 | Near real-time internally, but public access delayed |
| Openness | 1 | Portal access, limited formal API |
| Stability | 3 | Schiphol, legally mandated noise monitoring |
| Structure | 1 | Web portal, CSV downloads, no REST API |
| Identifiers | 2 | Terminal IDs, flight correlations |
| Additive Value | 3 | World-class airport noise monitoring |
| **Total** | **12/18** | |

## Notes
- Schiphol's noise monitoring is legally mandated under Dutch aviation law
- The NOMOS system is operated by CASPER (Computer-Aided System for Processing Environmental data around Runways)
- Consider also: Heathrow (WebTrak), Frankfurt (FRAPORT noise monitoring), Zurich Airport
- The lack of a formal public REST API is the main limitation
- Annual noise reports provide comprehensive data but not real-time
- WebTrak (used by many airports globally) may offer better API access at some locations
