# Pacific Tsunami Warning Center
**Country/Region**: Pacific Basin / Global
**Publisher**: NWS Pacific Tsunami Warning Center (PTWC) / NOAA
**API Endpoint**: `https://tsunami.gov/events/xml/PAAQAtom.xml`
**Documentation**: https://tsunami.gov/
**Protocol**: Atom / CAP
**Auth**: None
**Data Format**: XML (Atom feed with CAP links)
**Update Frequency**: Real-time (per seismic event)
**License**: US Government public domain

## What It Provides
The Pacific Tsunami Warning Center issues tsunami warnings, watches, advisories, and information statements for the Pacific Basin and other ocean regions. The Atom feed provides:
- Tsunami warning/watch/advisory bulletins
- Information statements (earthquake occurred, no tsunami threat)
- Event details: magnitude, location, affected region
- Links to full CAP XML documents per event
- Geographic coordinates of the seismic event

## API Details
- **PTWC Atom Feed (Pacific)**: `https://tsunami.gov/events/xml/PAAQAtom.xml`
- **NTWC Atom Feed (Atlantic/Gulf)**: `https://tsunami.gov/events/xml/PHEBAtom.xml`
- **Per-event CAP**: Linked via `<link rel="related" type="application/cap+xml">` in each entry
- **Per-event Bulletin**: Plain text bulletins linked via `<link rel="alternate">`
- **Entry structure**: `<title>`, `<summary>` (XHTML with category, magnitude, lat/lon, affected region), `<geo:lat>`, `<geo:long>`, `<updated>`
- **Summary fields**: Category (Warning/Watch/Advisory/Information), Bulletin Issue Time, Preliminary Magnitude, Lat/Lon, Affected Region, Definition

## Freshness Assessment
Excellent. Bulletins are issued within minutes of significant seismic events. The feed is continuously updated. Confirmed live with recent earthquake information statements.

## Entity Model
- **Bulletin** (UUID, title, updated, category)
- **Event** (magnitude, lat, lon, affected region)
- **Category** (Warning, Watch, Advisory, Information)
- **CAP Document** (linked, full alert details)

## Feasibility Rating
| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | Real-time, minutes after seismic events |
| Openness | 3 | Public domain, no auth |
| Stability | 3 | NOAA/NWS critical infrastructure |
| Structure | 2 | Atom XML with XHTML summary, CAP links |
| Identifiers | 2 | UUID-based, but no persistent event IDs across updates |
| Additive Value | 3 | Authoritative tsunami alerting |
| **Total** | **16/18** | |

## Notes
- Two separate feeds: PTWC (Pacific) and NTWC (US Atlantic/Gulf/Caribbean)
- CAP documents provide machine-readable structured alert data
- Bulletins text is also available for human-readable display
- Could be combined with GDACS for comprehensive tsunami coverage
- Information statements (no threat) are also included and are the most common entries
