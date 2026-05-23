# King Fahd Causeway - Border Crossing Wait Times

- **Country/Region**: Bahrain-Saudi Arabia border (BH/SA)
- **Endpoint**: Unknown (no public API found)
- **Protocol**: N/A
- **Auth**: N/A
- **Format**: N/A
- **Freshness**: Unknown
- **Docs**: None found
- **Score**: 2/18

## Overview

The King Fahd Causeway is a 25 km bridge-causeway connecting Bahrain (island) to
mainland Saudi Arabia. Opened in 1986, it is the only land border between the two
countries and one of the busiest border crossings in the Gulf region. The causeway
handles vehicle, pedestrian, and commercial traffic in both directions.

The General Authority for the King Fahd Causeway (KFCA — https://www.kfca.com.sa) is
a joint Saudi-Bahraini organization that manages and operates the causeway, including
customs, immigration, and traffic flow. The authority has won multiple international
awards for customer experience (2024-2025), indicating a focus on service quality
and modernization.

Traffic wait times at the causeway are significant for:
- **Cross-border commuters**: Many Bahrainis work in Saudi Arabia's Eastern Province,
  and many Saudis visit Bahrain (especially weekends/holidays)
- **Tourism**: Bahrain is a popular weekend destination for Saudi visitors
- **Commercial transport**: Goods flow between Bahrain port and Saudi markets
- **Holiday peaks**: Wait times can exceed 2-3 hours during Eid, national holidays,
  and Formula 1 race weekends

Despite the operational importance and customer experience focus, **no public real-time
API or data feed for causeway wait times was found**. The KFCA website (kfca.com.sa)
publishes news and announcements in Arabic but does not expose traffic data, lane
status, or wait time estimates via any documented endpoint.

## Endpoint Analysis

**Searched for but not found:**
- Public API for wait times or traffic flow
- JSON/XML data feeds
- Real-time dashboard with embeddable data
- RSS/Atom feeds with traffic updates
- Mobile app API (if a public app exists, its API is not documented)

**Website reviewed:**
- https://www.kfca.com.sa — Arabic-language news and announcements, no data portal
- No English-language API documentation
- No open data section or developer portal
- Recent news focuses on awards, but no mention of public data sharing

**US CBP Border Wait Times analogy:**
The US Customs and Border Protection agency publishes real-time wait times for all
land border crossings (US-Mexico, US-Canada) via a well-documented REST API:
```
https://bwt.cbp.gov/api/v2/BorderWaitTimes
```
This API provides wait times in minutes for pedestrian, vehicle, and commercial lanes,
updated every few minutes. No authentication required. The King Fahd Causeway could
adopt a similar model, but no such service currently exists publicly.

## Integration Notes

**Why this source would be valuable:**
- **High traffic volume**: Millions of crossings per year
- **Practical utility**: Real-time wait times help travelers plan crossings and avoid
  peak congestion
- **Regional interest**: Unique cross-border flow data for Gulf region
- **Niche domain**: Border crossing wait times are covered by the repo for US borders
  (if CBP API is added), but Gulf crossings would be a geographic extension

**Current blockers:**
- No public API or documented endpoint
- No evidence of real-time data publication in any machine-readable format
- KFCA may collect wait time data internally (for operations and customer experience
  metrics) but does not expose it publicly

**Potential future developments:**
KFCA's recent awards for "best digital transformation" and "customer experience" suggest
ongoing modernization. Future initiatives could include:
- Public wait time dashboard (web/mobile)
- REST API for integration with navigation apps (Google Maps, Waze, Apple Maps)
- Open data feeds as part of Saudi/Bahrain eGovernment programs

Monitor KFCA announcements and Saudi/Bahrain open data portals for any new services.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 0 | No data feed found |
| Openness | 0 | No public access |
| Stability | 1 | KFCA is stable institutional entity, but no API exists |
| Structure | 0 | N/A |
| Identifiers | 1 | Could key by crossing direction (BH→SA, SA→BH), lane type, but not applicable without data |
| Additive value | 0 | Cannot assess without endpoint |

**Verdict**: **Not viable** at this time. No public API or data feed for King Fahd
Causeway wait times, traffic, or lane status was found. The crossing is operationally
significant and KFCA appears focused on customer experience, but real-time data is not
publicly shared. This would be a strong candidate if an API becomes available — it
would extend the border crossings domain (currently US-only in the repo) to the Gulf
region and provide practical utility for cross-border travelers.

**Recommendation**: Periodically check KFCA website (kfca.com.sa), Saudi/Bahrain open
data portals (data.gov.sa, data.gov.bh), and eGovernment initiatives for future API
announcements. Contact KFCA public affairs office to inquire about plans to publish
real-time traffic data.
