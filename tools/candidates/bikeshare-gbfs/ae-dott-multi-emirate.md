# Dott Abu Dhabi, Dubai, Sharjah, Ras Al Khaimah (GBFS)

- **Country/Region**: United Arab Emirates / Abu Dhabi, Dubai, Sharjah, Ras Al Khaimah
- **Endpoints**:
  - Abu Dhabi: `https://gbfs.api.ridedott.com/public/v2/abu-dhabi/gbfs.json`
  - Dubai: `https://gbfs.api.ridedott.com/public/v2/dubai/gbfs.json`
  - Dubai Hills: `https://gbfs.api.ridedott.com/public/v2/dubai-hills/gbfs.json`
  - Ras Al Khaimah: `https://gbfs.api.ridedott.com/public/v2/ras-al-khaimah/gbfs.json`
  - Sharjah: `https://gbfs.api.ridedott.com/public/v2/sharjah/gbfs.json`
- **Protocol**: GBFS 2.3
- **Auth**: None
- **Format**: JSON
- **Freshness**: Real-time (free-floating e-scooters)
- **Docs**: https://ridedott.com/, https://github.com/MobilityData/gbfs
- **Score**: 15/18

## Overview

Dott is a European micromobility operator (founded in Amsterdam) that operates free-floating e-scooter fleets across **five deployments** in the UAE: Abu Dhabi, Dubai, Dubai Hills, Ras Al Khaimah, and Sharjah. This is the **only micromobility operator with multi-emirate coverage** in the UAE.

Each deployment has a separate GBFS 2.3 feed. The feeds were successfully probed but returned **0 feeds** in the discovery response, which indicates either:
- The feeds are operational but empty at probe time (off-peak hours, winter low season)
- The endpoints require specific query parameters or headers
- The system is in maintenance/sunset mode

**This requires deeper investigation** before building a bridge.

## Endpoint Analysis

**Discovery feeds verified but empty**:

```
GET https://gbfs.api.ridedott.com/public/v2/abu-dhabi/gbfs.json
```

Returns:
```json
{
  "version": "2.3",
  "data": {
    "feeds": []
  }
}
```

The same pattern holds for all five endpoints. This is unusual for a production GBFS system.

**Possible explanations**:
1. **Seasonal shutdown** — UAE summers are extremely hot (40–50°C); scooter operations may be seasonal
2. **Sunset in progress** — Dott exited several European markets in 2024; UAE operations may be winding down
3. **API migration** — the public v2 endpoints may be deprecated; a v3 or private endpoint may exist
4. **Requires registration** — some operators gate their GBFS feeds behind a developer portal or API key despite listing in the MobilityData catalog
5. **Timezone/cache** — feeds may populate during local peak hours (UAE is UTC+4)

## Why This Could Be Strong (If Operational)

1. **Multi-emirate coverage** — only operator in Abu Dhabi, Sharjah, and Ras Al Khaimah
2. **GBFS 2.3** — mature spec
3. **Free-floating model** — real-time vehicle locations and battery
4. **No auth (if feeds work)** — listed as open in MobilityData catalog
5. **Established operator** — Dott raised $85M, operates in 11 countries (before recent market exits)

## Limitations

- **Empty feeds** — cannot assess data quality, fleet size, or update frequency without live data
- **Operator viability** — Dott's 2024 market exits (France, Italy, Belgium, Germany) raise questions about UAE sustainability
- **No documentation** — ridedott.com does not publish API docs or developer portal
- **GBFS 2.3 not 3.0** — older spec (missing some newer fields)

## Next Steps (Before Building)

1. **Re-probe during UAE peak hours** (7–9am, 5–8pm UAE time / UTC+4)
2. **Check Dott social media / UAE press** for operational status
3. **Contact Dott developer support** (if reachable) to ask about empty feeds
4. **Monitor MobilityData catalog** for updates or removal
5. **Compare with alternatives**: If Dott is defunct, Yaldi (Dubai) and Careem (Dubai) remain strong

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | GBFS should be real-time, but feeds are empty — cannot verify |
| Openness | 3 | No auth required |
| Stability | 2 | Feeds return valid JSON but empty; operator stability unclear |
| Structure | 3 | GBFS 2.3 spec |
| Identifiers | 2 | Standard GBFS IDs, but no data to confirm |
| Additive value | 3 | **Only operator in Abu Dhabi, Sharjah, RAS** — high value if operational |

**Verdict**: **Maybe** (conditional on proving feeds are operational). Dott's multi-emirate coverage is unique and valuable, but the empty feeds are a blocker. Re-probe during UAE daytime hours and investigate operator status. If feeds populate, upgrade to **Build**. If Dott has exited UAE (likely given 2024 market exits elsewhere), mark **Skip** and document as a dead end.
