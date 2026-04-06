# GDACS (Global Disaster Alert and Coordination System)
**Country/Region**: Global
**Publisher**: European Commission Joint Research Centre (JRC) / United Nations
**API Endpoint**: `https://www.gdacs.org/xml/rss.xml`
**Documentation**: https://www.gdacs.org/Knowledge/overview.aspx
**Protocol**: RSS 2.0 / CAP (per-event)
**Auth**: None
**Data Format**: XML (RSS with custom `gdacs:` namespace extensions)
**Update Frequency**: Near real-time (minutes after event detection)
**License**: Public domain — "Copyright European Union. Syndication allowed, provided the source is acknowledged."

## What It Provides
GDACS provides near real-time notifications for major sudden-onset natural disasters worldwide. Current coverage includes:
- Earthquakes (with tsunami risk assessment)
- Tropical cyclones
- Floods
- Volcanic eruptions
- Forest fires
- Droughts

Each event includes an automatic impact severity assessment with Green/Orange/Red alert levels based on calculated population exposure and vulnerability.

## API Details
- **Main RSS Feed**: `https://www.gdacs.org/xml/rss.xml` — all current events
- **Per-event RSS**: `https://www.gdacs.org/datareport/resources/{TYPE}/{ID}/rss_{ID}.xml`
- **Per-event CAP**: `https://www.gdacs.org/contentdata/resources/{TYPE}/{ID}/cap_{ID}.xml`
- **Event types**: EQ (earthquake), TC (tropical cyclone), FL (flood), VO (volcano), FF (forest fire), DR (drought)
- **GeoRSS**: Events include `georss:point` and `gdacs:bbox` for geolocation
- **Custom namespace elements**: `gdacs:alertlevel`, `gdacs:severity`, `gdacs:population`, `gdacs:vulnerability`, `gdacs:eventtype`, `gdacs:eventid`, `gdacs:episodeid`, `gdacs:country`, `gdacs:iso3`

## Freshness Assessment
Excellent. The RSS feed is updated within minutes of event detection. Earthquakes and tropical cyclones are fully automated. The feed had 236 records at probe time with events from the current day.

## Entity Model
- **Event** (eventid, eventtype, eventname, country, iso3, alertlevel, alertscore)
- **Episode** (episodeid, version, calculationtype) — an event update
- **Severity** (magnitude, wind speed, etc. with unit and value)
- **Population** (affected count with unit)
- **Geolocation** (lat, lon, bounding box)

## Feasibility Rating
| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | Near real-time, automated |
| Openness | 3 | Public domain, no auth |
| Stability | 3 | Running since 2004, EU/UN backed |
| Structure | 2 | XML/RSS with custom extensions, not pure JSON |
| Identifiers | 3 | Stable event IDs, episode IDs, GLIDE numbers |
| Additive Value | 3 | Unique global multi-hazard alerting |
| **Total** | **17/18** | |

## Notes
- CAP (Common Alerting Protocol) files available per event for standards-compliant integration
- The RSS feed includes all active/recent events globally — no regional filtering at the feed level
- GDACS also provides a GeoJSON API but it is less documented
- Excellent candidate for a bridge: poll RSS feed, emit structured events per disaster
