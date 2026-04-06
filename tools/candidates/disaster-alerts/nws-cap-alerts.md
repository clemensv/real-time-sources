# NWS CAP Alerts (FEMA IPAWS)
**Country/Region**: United States
**Publisher**: National Weather Service (NWS) / NOAA
**API Endpoint**: `https://api.weather.gov/alerts/active`
**Documentation**: https://www.weather.gov/documentation/services-web-api
**Protocol**: REST
**Auth**: None (User-Agent header recommended)
**Data Format**: GeoJSON (application/geo+json)
**Update Frequency**: Real-time (as alerts are issued)
**License**: US Government public domain

## What It Provides
The NWS alerts API provides all current weather and non-weather alerts for the United States via the Integrated Public Alert and Warning System (IPAWS). This includes:
- Severe weather warnings (tornado, hurricane, thunderstorm)
- Flood warnings and watches
- Winter storm warnings
- Heat/cold advisories
- Tsunami warnings
- Fire weather watches
- Marine warnings
- Special weather statements

All alerts use the Common Alerting Protocol (CAP) standard and are distributed through IPAWS.

## API Details
- **Active alerts**: `GET /alerts/active` — all currently active alerts
- **By area**: `GET /alerts/active?area={state}` — e.g., `area=TX`
- **By zone**: `GET /alerts/active/zone/{zoneId}`
- **By severity**: `GET /alerts?severity=Extreme,Severe`
- **By event**: `GET /alerts?event=Tornado%20Warning`
- **Single alert**: `GET /alerts/{id}`
- **Pagination**: Link headers for paging
- **Response format**: GeoJSON FeatureCollection with full CAP properties
- **Key properties**: `event`, `severity`, `certainty`, `urgency`, `headline`, `description`, `instruction`, `areaDesc`, `geocode` (SAME/UGC codes), `sent`, `effective`, `onset`, `expires`, `ends`
- **VTEC codes**: Included in parameters for event tracking

## Freshness Assessment
Excellent. Alerts appear within seconds of issuance. The API returns IPAWSv1.0 coded alerts. Confirmed live with current alerts including real weather events.

## Entity Model
- **Alert** (id as URN, areaDesc, event, status, messageType, category)
- **Severity/Urgency/Certainty** (CAP standard values)
- **Geocode** (SAME codes, UGC zone codes, VTEC event tracking codes)
- **Geometry** (GeoJSON polygon when available)
- **Parameters** (AWIPS identifier, WMO identifier, NWS headline)

## Feasibility Rating
| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | Real-time, seconds after issuance |
| Openness | 3 | Public domain, no API key |
| Stability | 3 | Official US Government API, well-maintained |
| Structure | 3 | Clean GeoJSON with CAP properties |
| Identifiers | 3 | URN-based IDs, VTEC tracking, UGC/SAME zone codes |
| Additive Value | 3 | All US weather alerts in one endpoint |
| **Total** | **18/18** | |

## Notes
- User-Agent header is recommended (e.g., `(myapp, contact@example.com)`) but not enforced
- Rate limiting is lenient but exists
- Geometry may be null for some alerts (zone-based only)
- VTEC codes enable precise event tracking and correlation
- This is the same data that drives Emergency Alert System (EAS) broadcasts
