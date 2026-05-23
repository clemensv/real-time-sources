# Bahrain Public Transport - GTFS/GTFS-RT Coverage

- **Country/Region**: Bahrain (BH)
- **Endpoint**: Unknown (no GTFS feed found)
- **Protocol**: N/A
- **Auth**: N/A
- **Format**: N/A
- **Freshness**: N/A
- **Docs**: None found
- **Score**: 2/18

## Overview

Bahrain operates a public bus network managed by the Bahrain Public Transport Company
(under the Ministry of Transportation and Telecommunications). The network serves
Manama (capital), surrounding towns, and industrial areas. According to MTT announcements,
Bahrain is planning a metro system (Bahrain Metro) with Phase 1 covering 29 km and 20
stations, connecting Bahrain International Airport, Seef District, Juffair, and Isa Town.
However, the metro is still in planning/development and not yet operational (as of 2026).

**Current public transport:**
- **Bus network**: Urban and intercity routes operated by Bahrain Public Transport Co.
- **Coverage**: Manama, Muharraq, Riffa, Isa Town, industrial areas
- **Payment**: Smartcard system (similar to Oyster/Charlie Card)
- **Real-time info**: Unknown — no public GTFS-RT feed found

**Planned transport (future):**
- **Bahrain Metro**: 109 km total planned, Phase 1 (29 km, 20 stations) targeting
  airport-to-city and educational-area links
- **Enhanced bus infrastructure**: MTT announcements mention upgrades to bus shelters,
  stops, and supporting infrastructure

GTFS (General Transit Feed Specification) is the global standard for publishing public
transit schedules, routes, and stops. GTFS-RT (Real-Time) extends this with live
vehicle positions, arrival predictions, and service alerts. Over 1,400 transit agencies
worldwide publish GTFS/GTFS-RT feeds, many listed in the MobilityData catalog.

## Endpoint Analysis

**Searches conducted:**

**1. MobilityData API (global GTFS catalog):**
```
GET https://api.mobilitydata.org/v1/feeds
```
**Result:** DNS resolution failure (API endpoint may have changed or been deprecated)
- MobilityData maintains a public catalog at https://database.mobilitydata.org/
- API access method unclear; web interface may be the primary discovery tool

**2. TransitFeeds.com search:**
```
https://transitfeeds.com/search?q=bahrain
```
**Result:** HTTP 403 Forbidden (site blocking automated requests or down)
- TransitFeeds.com was a popular GTFS aggregator, but appears to have access restrictions

**3. Manual search via MobilityData web catalog:**
- Could not be performed programmatically during discovery
- Recommend manual browse of https://database.mobilitydata.org/ filtering by country "Bahrain"

**4. MTT website review:**
```
https://www.mtt.gov.bh
```
**Result:** No mention of GTFS, open data, or developer API for public transport
- Site focuses on policy announcements, infrastructure projects, and service overviews
- No "Open Data" or "Developer" section
- No links to real-time bus tracking app or API

**5. Google Transit / Apple Maps integration:**
If Bahrain buses appear in Google Maps or Apple Maps with real-time arrival predictions,
the transit agency is providing GTFS/GTFS-RT to those platforms. However, this does not
guarantee public access — Google/Apple often sign data-sharing agreements that do not
include public redistribution rights.

## Integration Notes

**Why Bahrain public transport would be valuable:**
- **Gulf region representation**: No existing public transit bridges for Gulf states
  in the repo
- **Island nation**: Compact geography makes full network coverage achievable with a
  small number of routes/vehicles
- **Metro development**: When Bahrain Metro launches (Phase 1 targeted for late 2020s),
  it will likely publish GTFS-RT for real-time train positions and arrival predictions
- **GTFS domain fit**: The repo has a generic GTFS bridge that works for any agency;
  Bahrain would be an easy addition once a feed is discovered

**Current blockers:**
- No GTFS feed found in public catalogs (MobilityData, TransitFeeds)
- MTT website does not mention open data or developer API
- Unknown whether Bahrain Public Transport Co. publishes any real-time data
- No evidence of GTFS-RT even for internal use (e.g., for Google Maps integration)

**Potential reasons for absence:**
1. **No GTFS at all**: Bahrain may not have adopted GTFS standard (less likely, as most
   modern transit systems use it for internal scheduling)
2. **Private/restricted GTFS**: Feed exists but shared only with partners (Google,
   Apple, Moovit) under non-redistribution agreements
3. **Static GTFS only**: Schedule data exists but no real-time layer (common for smaller
   agencies)
4. **Development in progress**: GTFS-RT may be planned as part of bus network upgrades
   or metro rollout

**Recommended next steps:**
1. **Manual search MobilityData catalog:**
   - Browse https://database.mobilitydata.org/
   - Filter by country "Bahrain" (BH)
   - Check for any Bahrain Public Transport Co. feeds (static or real-time)
2. **Check Google Maps integration:**
   - Search for bus routes in Bahrain on Google Maps
   - If real-time arrivals are shown, Bahrain has GTFS-RT (but may not be public)
3. **Contact Bahrain Public Transport Company:**
   - Inquire about GTFS feed availability for developers
   - Ask about real-time API or data sharing policy
4. **Contact MTT:**
   - Request information on open data initiatives for public transport
   - Ask about plans for GTFS/GTFS-RT publication as part of metro or bus network upgrades
5. **Monitor Bahrain Metro development:**
   - Metro projects typically launch with GTFS-RT for real-time train tracking
   - Phase 1 timeline (late 2020s) suggests GTFS-RT may become available in 2-5 years
6. **Check for third-party apps:**
   - If a "Bahrain Bus" or similar app exists, reverse-engineer its API (if permissible
     and documented)

**Comparison to other Gulf transit systems:**
- **Dubai (RTA)**: GTFS available for Dubai Metro, Tram, Bus (check MobilityData catalog)
- **Doha (Qatar Rail/Mowasalat)**: Doha Metro GTFS available (check catalog)
- **Riyadh Metro (Saudi Arabia)**: Under construction, GTFS-RT likely on launch
- **Kuwait**: No known GTFS feed
- **Oman**: No known GTFS feed

Bahrain lags behind Dubai and Doha in transit open data, but may catch up with metro
development.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 0 | No feed found |
| Openness | 0 | No public access |
| Stability | 1 | Transit agency is stable, but no API exists |
| Structure | 0 | N/A |
| Identifiers | 1 | GTFS uses stable vehicle/trip/route IDs, but not applicable without feed |
| Additive value | 0 | Cannot assess without feed |

**Verdict**: **Not viable at this time**. No GTFS or GTFS-RT feed for Bahrain public
transport (buses) was found in public catalogs or on MTT/transit agency websites. The
network exists and appears operational, but real-time data is not publicly available.
This **could become viable** in 2-5 years when Bahrain Metro launches (Phase 1), as
metro projects typically publish GTFS-RT for real-time train tracking.

**Recommendation**: Monitor Bahrain Metro development timeline and contact MTT/Bahrain
Public Transport Co. to inquire about GTFS feed publication plans. If Google Maps shows
real-time bus arrivals for Bahrain, investigate whether the underlying GTFS-RT feed
can be accessed publicly. Add Bahrain to a "watch list" for future GTFS availability,
especially as metro construction progresses.
