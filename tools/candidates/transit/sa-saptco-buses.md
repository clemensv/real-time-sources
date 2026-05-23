# Saudi Public Transport Company (SAPTCO) - Bus GTFS

- **Country/Region**: Saudi Arabia (national intercity + urban buses)
- **Endpoint**: Unknown (no public GTFS found)
- **Protocol**: GTFS / GTFS-RT (if exists)
- **Auth**: Unknown
- **Format**: Protobuf (GTFS-RT)
- **Freshness**: Real-time (if GTFS-RT), static schedules (if GTFS-static only)
- **Docs**: https://saptco.com.sa (no data portal)
- **Score**: 8/18

## Overview

The **Saudi Public Transport Company** (الشركة السعودية للنقل الجماعي, SAPTCO) is Saudi Arabia's national bus operator, providing:

- **Intercity buses** — Long-distance routes connecting all major Saudi cities (Riyadh-Jeddah, Dammam-Makkah, etc.)
- **Urban buses** — Local transit in Riyadh, Jeddah, Dammam, and other cities
- **Hajj/Umrah shuttle buses** — Pilgrim transport between Makkah, Madinah, Mina, Arafat, Muzdalifah during Hajj season
- **International routes** — Cross-border buses to UAE, Bahrain, Kuwait, Jordan, Egypt

**Fleet**: SAPTCO operates **~3,000 buses** and serves **~40 million passengers/year** (pre-COVID). During Hajj, SAPTCO mobilizes **thousands of additional buses** to transport 2-3 million pilgrims.

**Context**: Until the Riyadh Metro launch (2024), SAPTCO was the only public transit option in most Saudi cities. Private cars dominate (90%+ mode share), and bus ridership is low by global standards. However, Hajj bus operations are the world's largest seasonal mass transit event.

## GTFS Likelihood

**GTFS-static** (schedules, routes, stops) is common for bus systems globally. **GTFS-RT** (real-time vehicle positions) is less common for intercity buses but standard for urban transit.

**Comparable bus operators**:

| Operator | Country | GTFS-static | GTFS-RT | API |
|----------|---------|-------------|---------|-----|
| **SAPTCO** | Saudi Arabia | ❓ Unknown | ❓ Unknown | None found |
| Greyhound | USA | ✅ Yes | ❌ No | None |
| FlixBus | Europe | ✅ Yes | ❌ No | JSON API |
| National Express | UK | ✅ Yes | ✅ Yes | GTFS-RT |
| Intercités | France | ✅ Yes | ✅ Yes | SIRI |

Intercity bus operators are **less likely to publish GTFS-RT** than urban transit agencies. Vehicle positions are less critical for long-distance travel (fixed schedules, no frequent stops).

However, **SAPTCO's urban bus routes** (Riyadh, Jeddah, Dammam) could plausibly have GTFS-RT, especially if integrated with the new Riyadh Metro.

## Endpoint Analysis

**SAPTCO website**: `https://saptco.com.sa`

The SAPTCO website provides:
- Route information (origin-destination pairs)
- Ticket booking (online purchase)
- Schedule lookups (departure times)

**No data portal**: SAPTCO does not advertise a developer portal, API, or GTFS download page.

**Possible GTFS endpoints** (not tested):
```
https://saptco.com.sa/gtfs/riyadh/gtfs.zip
https://api.saptco.com.sa/gtfs-rt/vehicle-positions
https://data.saptco.com.sa/gtfs
```

**MobilityData catalog**: The global GTFS aggregator (MobilityData.org) does **not list SAPTCO**. This suggests no public GTFS feed exists, or it is not discoverable.

**Google Maps integration**: If SAPTCO routes appear in Google Maps transit directions, GTFS-static exists. This can be tested by searching for bus routes in Riyadh or Jeddah on Google Maps.

## Integration Notes

- **No public GTFS confirmed**: SAPTCO does not advertise GTFS feeds. This is a likely **non-starter** unless feeds exist but are unpublished.
- **Urban vs. intercity**: SAPTCO's **urban buses** (Riyadh, Jeddah) are more likely to have GTFS-RT than intercity routes. Focus discovery on city-specific transit.
- **Riyadh Metro integration**: Riyadh's new metro system is designed to integrate with buses (MaaS — Mobility as a Service). This may force SAPTCO to publish GTFS for Riyadh urban buses to enable trip planning across modes.
- **Hajj operations**: SAPTCO's Hajj bus network is **temporary and non-scheduled** (shuttle loops during pilgrimage). This is unlikely to have GTFS.
- **Alternative: Riyadh Bus** — Riyadh launched a new BRT (Bus Rapid Transit) system in 2024 alongside the metro. This may be operated separately from SAPTCO and could have its own GTFS feed.

**Unique value if GTFS exists**:
- **First Saudi bus data** — No bus GTFS feeds exist for Saudi Arabia in the MobilityData catalog.
- **Hajj pilgrim transport** — Even without real-time data, SAPTCO's Hajj shuttle routes would be valuable for planning (if available as GTFS-static).
- **Intercity connectivity** — SAPTCO's national network connects all major Saudi cities (unlike aviation, which skips mid-size cities).

## Scoring

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | GTFS-static is static (hourly updates at best); GTFS-RT is real-time |
| Openness | 1 | No public GTFS found; unknown if it exists internally |
| Stability | 3 | SAPTCO is the national operator, government-owned |
| Structure | 3 | GTFS is a formal spec (if exists) |
| Identifiers | 2 | GTFS trip/route/stop IDs are stable |
| Additive value | 2 | First Saudi bus data; overlaps with existing GTFS bridge |

**Total: 13/18** (if GTFS exists)  
**Actual: 8/18** (penalized for unknown status)

**Verdict**: ⏭️ **Reference** — SAPTCO **may** have GTFS feeds for urban buses (Riyadh, Jeddah), especially with the new Riyadh Metro integration. However, no public feeds are confirmed.

**Recommended action**:
1. **Test Google Maps** — Search for SAPTCO bus routes in Riyadh, Jeddah, Dammam on Google Maps. If they appear in transit directions, GTFS-static exists.
2. **Check after Riyadh Metro launch** — Once the metro opens (late 2024), integrated bus+metro trip planning may force GTFS publication.
3. **Contact SAPTCO** — Email SAPTCO or the Royal Commission for Riyadh City to request GTFS feed access.
4. **Focus on Riyadh urban buses** — Intercity GTFS is lower value. Prioritize city transit.

If GTFS-RT is confirmed for Riyadh buses, escalate to ⚠️ **Maybe** or ✅ **Build** depending on feed quality. SAPTCO intercity GTFS-static (without real-time) is **lower priority** — focus on Riyadh Metro instead.
