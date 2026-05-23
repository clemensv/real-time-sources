# Civil Defense Directorate - Emergency Alerts and Flood Warnings

- **Country/Region**: Saudi Arabia (KSA)
- **Endpoint**: Unknown (emergency services, likely closed)
- **Protocol**: CAP-XML (Common Alerting Protocol, OASIS/ITU standard)
- **Auth**: Unknown
- **Format**: CAP-XML (if standard is followed)
- **Freshness**: Real-time (alerts issued as events occur)
- **Docs**: https://www.998.gov.sa (website unreachable during probing)
- **Score**: 10/18

## Overview

The **General Directorate of Civil Defense** (المديرية العامة للدفاع المدني, 998) is Saudi Arabia's emergency response agency, responsible for:

- **Firefighting** — Urban and wildland fires
- **Flood rescue** — Flash flood evacuations (frequent in Jeddah, mountain valleys)
- **Hazmat response** — Industrial chemical spills, oil refinery incidents
- **Disaster coordination** — Earthquakes, building collapses, mass casualty events
- **Public alerts** — Weather warnings, evacuation orders

**Emergency number**: **998** (analogous to 911 in the US)

**Saudi Arabia's disaster risks**:
1. **Flash floods** — Jeddah has experienced deadly floods (2009: 123 deaths, 2011: 10 deaths) when rare rainstorms overwhelm drainage systems in the coastal plain.
2. **Dust storms (haboobs)** — Reduce visibility to <50m, cause respiratory issues, traffic accidents.
3. **Heat waves** — Summer temperatures exceed 50°C; heatstroke, power outages.
4. **Earthquakes** — Red Sea rift zone (western Saudi Arabia) and Harrat volcanic fields.
5. **Industrial accidents** — Jubail Industrial City, Yanbu, Ras Tanura (oil refineries, petrochemicals).
6. **Hajj emergencies** — Crowd crushes, fires, heatstroke during pilgrimage (2015: 2,400+ deaths).

## Common Alerting Protocol (CAP)

**CAP-XML** is the international standard for emergency alerts (OASIS standard, adopted by ITU). CAP is used globally for:
- Weather warnings (tornado, hurricane, flood)
- Earthquake early warnings (Japan, Mexico, California)
- Tsunami alerts (Pacific, Indian Ocean)
- Civil emergency alerts (evacuations, amber alerts)

**CAP structure**:
- **Alert ID** — Unique identifier for each alert
- **Sender** — Authority issuing the alert (e.g., "Civil Defense Directorate")
- **Event type** — Flood, dust storm, earthquake, hazmat, etc.
- **Severity** — Extreme, severe, moderate, minor
- **Area** — Geographic polygon or place name
- **Onset / expires** — When the event starts / when alert expires
- **Description** — Human-readable text (Arabic and/or English)

**Global CAP feeds**:

| Country | Authority | CAP feed? | Public? |
|---------|-----------|-----------|---------|
| **Saudi Arabia** | Civil Defense | ❓ Unknown | ❓ Unknown |
| USA | FEMA IPAWS | ✅ Yes | ✅ Public |
| Japan | JMA | ✅ Yes | ✅ Public |
| Canada | Environment Canada | ✅ Yes | ✅ Public |
| Australia | BOM | ✅ Yes | ✅ Public |
| Mexico | CENAPRED | ✅ Yes | ✅ Public |

**Saudi Arabia's CAP status**: It is **unknown** whether Saudi Civil Defense publishes CAP alerts. The website (998.gov.sa) was **unreachable during probing**, preventing verification.

## Endpoint Analysis

**Civil Defense website**: `https://www.998.gov.sa`

**Probe result**: Website was **unreachable** (timeout or network error).

**Possible CAP endpoints** (not tested):
```
https://www.998.gov.sa/alerts/cap
https://alerts.998.gov.sa/feed
https://api.998.gov.sa/v1/alerts
```

**Alternative: NCM (Meteorology)**: Weather warnings (dust storms, flash floods) may be issued by **NCM (National Center for Meteorology)**, not Civil Defense. Check NCM for alert feeds.

**SMS/mobile alerts**: Saudi Arabia has a **mobile emergency alert system** (push notifications to all phones in an area). These alerts are **not public APIs** — they are broadcast via cell towers (Cell Broadcast Service, CBS). To monitor, one would need a physical phone in Saudi Arabia.

## Integration Notes

- **Website unreachable**: The primary obstacle is that 998.gov.sa could not be accessed during probing. This may be:
  - **Geo-restriction** (blocking non-Saudi IPs)
  - **Temporary downtime**
  - **Security policy** (Civil Defense sites often restrict public access)
- **CAP is a standard**: If Saudi Civil Defense follows international best practices (OASIS CAP), alerts would be in XML format with predictable structure.
- **No confirmation of public CAP feed**: Even if CAP exists, it may be restricted to authorized users (emergency services, government agencies), not public.
- **Alternative: NCM weather warnings** — For weather-related alerts (floods, dust storms), check **NCM (National Center for Meteorology)** instead of Civil Defense.
- **Alternative: Twitter** — Civil Defense may post alerts on Twitter (@SaudiCivilDefense or Arabic equivalent). These could be scraped, but are narrative text, not structured CAP.

**Unique value if CAP feed exists**:
- **Jeddah flood warnings** — Recurring deadly floods in Red Sea coastal city
- **Dust storm alerts** — Frequent haboobs disrupt aviation, health
- **Hajj emergency alerts** — Real-time alerts during pilgrimage (critical public safety)
- **Earthquake early warnings** — Red Sea rift and Harrat volcanic seismicity

## Scoring

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Emergency alerts are real-time (if feed exists) |
| Openness | 1 | Unknown if public; many emergency feeds are restricted |
| Stability | 3 | Civil Defense is a permanent government agency |
| Structure | 3 | CAP-XML is a formal standard (if used) |
| Identifiers | 2 | CAP alert IDs, event types, areas |
| Additive value | 2 | First Saudi emergency alerts; overlaps with global alerting systems |

**Total: 14/18** (if CAP feed exists and is public)  
**Actual: 10/18** (penalized for unreachable website and unknown status)

**Verdict**: ⚠️ **Maybe** — Saudi Civil Defense **may** publish CAP emergency alerts, but the website was unreachable and no public feed was confirmed. This is worth deeper investigation because:
1. **Jeddah flood warnings** are life-saving and globally significant (recurring urban flash floods).
2. **Hajj emergency alerts** are unique and affect 2-3 million pilgrims.
3. **CAP is a global standard** — if Saudi Arabia publishes CAP, it will integrate seamlessly with global alerting systems.

**Recommended action**:
1. **Retry 998.gov.sa** from a Saudi IP (or via VPN) to check for geo-blocking.
2. **Search for CAP feeds** — Look for `/alerts`, `/cap`, `/rss`, `/atom` paths on 998.gov.sa.
3. **Contact Civil Defense** — Email or call to request access to public alert feeds.
4. **Check NCM** — National Center for Meteorology may issue weather-related alerts (floods, dust storms) in CAP format.
5. **Monitor Twitter** — Civil Defense may post alerts on social media; scrape as a fallback.

If a public CAP feed is confirmed, **immediately escalate to ✅ Build**. Jeddah flood warnings and Hajj alerts are high-value, globally unique datasets.

**Alternative**: If no CAP feed exists, check **GDACS (Global Disaster Alert and Coordination System)** which aggregates alerts from Saudi Arabia (earthquakes, floods) as part of global coverage.
