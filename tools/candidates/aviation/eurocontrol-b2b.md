# EUROCONTROL B2B Services
**Country/Region**: Europe (ECAC member states)
**Publisher**: EUROCONTROL (European Organisation for the Safety of Air Navigation)
**API Endpoint**: `https://www.b2b.nm.eurocontrol.int/` (NM B2B portal)
**Documentation**: https://www.eurocontrol.int/service/network-manager-business-business-b2b-web-services
**Protocol**: SOAP / REST (NM B2B Web Services)
**Auth**: Certificate-based authentication (organizational registration)
**Data Format**: XML (SOAP), JSON (newer REST endpoints)
**Update Frequency**: Real-time (streaming and request/reply)
**License**: EUROCONTROL restricted — approved operational stakeholders only

## What It Provides
EUROCONTROL's Network Manager B2B services provide real-time European air traffic management data:
- **Flight data**: Real-time flight positions, filed and actual routes, flight plans
- **Flow management**: Regulations, ATFCM measures, slot allocations
- **Airspace data**: Airspace availability, route network, restricted areas
- **Airport data**: Runway configurations, capacity, demand
- **Delay information**: ATFCM delay causes and durations
- **Demand/capacity balancing**: Network-wide traffic loads

## API Details
- **B2B Web Services**: SOAP-based services with WSDL definitions
- **NM Portal**: `https://www.b2b.nm.eurocontrol.int/` — access management
- **Services categories**:
  - Flight services (flight list, flight data)
  - Flow services (regulations, ATFCM measures)
  - Airspace services (airspace availability)
  - General information services
- **Authentication**: X.509 client certificates, organizational registration required
- **Preops environment**: Testing environment available for development
- **Connectivity**: Internet or PENS (Pan-European Network Service)

## Freshness Assessment
Excellent for approved consumers. Real-time streaming and request/reply services provide current NAS data. However, access is strictly controlled and limited to operational stakeholders.

## Entity Model
- **Flight** (IFPL ID, callsign, aircraft type, departure, arrival, route, CTOT)
- **Regulation** (regulation ID, location, reason, rate, start/end time)
- **Airspace** (designator, type, availability, restrictions)
- **Airport** (ICAO code, capacity, demand, runway configuration)
- **Delay** (flight ID, ATFCM delay minutes, delay cause)

## Feasibility Rating
| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | Real-time streaming/request-reply |
| Openness | 0 | Certificate auth, organizational registration only |
| Stability | 3 | EUROCONTROL, intergovernmental treaty org |
| Structure | 3 | Well-defined SOAP/WSDL, moving to REST |
| Identifiers | 3 | IFPL IDs, ICAO codes, regulation IDs |
| Additive Value | 3 | Authoritative European ATM data |
| **Total** | **15/18** | |

## Notes
- Access is restricted to aviation operational stakeholders (airlines, ANSPs, airports)
- The registration process involves organizational agreements with EUROCONTROL
- SOAP/WSDL services are well-documented but complex to implement
- Newer REST endpoints are being developed but may not cover all services
- For most external consumers, OpenSky Network is a more accessible alternative for European flight data
- EUROCONTROL also publishes some open data (statistics, performance data) through different channels
