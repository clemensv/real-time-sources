# Kuwait Public Transit GTFS Real-Time

- **Country/Region**: Kuwait
- **Endpoint**: Unknown (no GTFS or GTFS-RT feed discovered)
- **Protocol**: N/A
- **Auth**: N/A
- **Format**: N/A
- **Freshness**: N/A
- **Docs**: None
- **Score**: N/A (source does not exist)

## Overview

Kuwait's public transportation system is **underdeveloped** compared to its Gulf neighbors (Dubai, Doha, Riyadh). The country relies heavily on private vehicles, with limited public transit options:

**Current public transit operators**:
1. **Kuwait Public Transportation Company (KPTC)** — state-owned bus operator
   - Operates ~30 bus routes in Kuwait City metropolitan area
   - Fleet: ~500 buses
   - Ridership: Low (most residents own cars)
   - Website: https://kptc.com.kw (connection failed during probe)

2. **CityBus** — private bus service (limited routes)

3. **Taxis** — mix of traditional taxis and app-based (Careem, Talabat Go)

**Planned but not operational** (as of 2025):
- **Kuwait Metro** — multi-line metro system proposed since 2009, still in planning/tendering phase, no construction start date
- **Kuwait Tramway** — proposed light rail, concept stage
- **Integrated transport authority** — Kuwait has discussed creating a unified transport authority but implementation is pending

## GTFS/GTFS-RT Discovery Attempts

Searched multiple catalogs and resources to find Kuwait transit feeds:

**MobilityData GTFS catalog** (global authoritative catalog):
- Checked https://database.mobilitydata.org/ (accessible via web interface)
- Searched for "Kuwait" — **0 results**
- Searched for "KPTC" — **0 results**
- Checked GCC/Middle East section — only found UAE (Dubai RTA, Abu Dhabi) and Saudi Arabia (Riyadh Metro)

**TransitFeeds (archive.org historical)** (formerly TransitFeeds.com, now offline):
- Historical archives show no Kuwait feeds ever published

**Transitland** (global transit aggregator):
- No Kuwait operators listed (as of 2025-05-23)

**Google Transit Partner Program**:
- Checked if Kuwait buses appear in Google Maps transit directions — **no results**
- Google Maps does not show public transit routing in Kuwait (as of 2025)
- This confirms no GTFS feed is shared with Google

**KPTC website probe**:
```
GET https://kptc.com.kw
GET https://www.kptc.com.kw
GET https://kptc.com.kw/en/routes
GET https://kptc.com.kw/gtfs
```
All attempts: Connection timeout or DNS failure

**Alternative searches**:
- Searched "Kuwait bus schedule API" — no results
- Searched "KPTC real-time bus tracking" — no official system found
- Searched Arabic: "الشركة الكويتية للنقل العام" (KPTC in Arabic), "مواعيد الحافلات الكويت" (Kuwait bus schedules) — only news articles, no data portals

## Why GTFS Likely Does Not Exist

| Reason | Explanation |
|--------|-------------|
| Low transit ridership | Most Kuwaitis own cars; public transit is used primarily by low-income expatriate workers |
| Limited network | ~30 bus routes do not justify the overhead of GTFS implementation |
| No open data culture | Kuwait government agencies rarely publish open data APIs |
| Lack of integration with global platforms | Kuwait buses do not appear in Google Maps, Apple Maps, or other trip planners |
| No real-time tracking | KPTC does not appear to operate GPS-based bus tracking systems |

## Comparison to Gulf Neighbors

| Country | Public Transit | GTFS Status | Notes |
|---------|----------------|-------------|-------|
| **UAE (Dubai)** | Dubai Metro, Dubai Tram, RTA buses | ✅ GTFS + GTFS-RT | Available via Dubai RTA open data portal |
| **UAE (Abu Dhabi)** | Abu Dhabi buses | ✅ GTFS | Documented in MobilityData catalog |
| **Qatar (Doha)** | Doha Metro, Metrolink, Mowasalat buses | ✅ GTFS | Available via Mowasalat (Karwa) |
| **Saudi Arabia (Riyadh)** | Riyadh Metro, Riyadh Bus | ✅ GTFS + GTFS-RT | Launched 2024 with open data commitment |
| **Saudi Arabia (Jeddah)** | Makkah Metro (Haramain) | ✅ GTFS | Religious pilgrimage transit |
| **Bahrain** | Bahrain Bus | ⚠️ Partial | Limited data availability |
| **Oman** | Mwasalat (buses) | ❌ None | Similar to Kuwait — no GTFS found |
| **Kuwait** | KPTC buses | ❌ None | No GTFS or real-time data |

Kuwait is an **outlier** in the Gulf — the only major oil-rich state without a metro system or GTFS-compliant transit data.

## Future Prospects

**Kuwait Metro** (if ever built):
- If Kuwait Metro launches, it would likely publish GTFS data (following Dubai/Riyadh precedent)
- Current timeline: Indefinite (project has stalled multiple times since 2009)
- Scale: Proposed 160km, 5 lines, 69 stations

**KPTC digitalization**:
- If KPTC modernizes and implements real-time bus tracking (GPS-equipped fleet), GTFS-RT could become feasible
- No public announcements of such initiatives as of 2025

## Verdict

**Verdict**: ❌ **Skip** — Kuwait does not publish GTFS or GTFS-RT data. KPTC bus network exists but is not digitized to the point of real-time tracking or standardized schedule publishing. Documented here as a **negative finding** to avoid future redundant searches.

**Recommendation**:
- Monitor **Kuwait Vision 2035** (national development plan) for public transit digitalization initiatives
- If Kuwait Metro project advances, revisit GTFS availability
- For now, Kuwait has **no viable real-time public transit data source**

**Next steps** (if pursuing):
1. Contact KPTC directly to inquire about real-time bus tracking systems or API availability (unlikely to succeed)
2. Check if Kuwait has an official open data portal (data.gov.kw) that might host transit data (probe failed)
3. Monitor MobilityData catalog for Kuwait additions (set up alert for "Kuwait" keyword)

**Cross-Gulf observation**:
Recommend a **GCC-wide GTFS aggregation project** that covers Dubai, Abu Dhabi, Doha, and Riyadh in a single bridge. Kuwait and Oman would be added once/if they publish feeds. This is more efficient than per-country bridges.
