# ACLED - Iraq Conflict and Political Violence Events

- **Country/Region**: Global (Iraq coverage available)
- **Endpoint**: `https://api.acleddata.com/acled/read`
- **Protocol**: HTTP REST API
- **Auth**: API key required (free tier limited, commercial licenses available)
- **Format**: JSON, CSV
- **Freshness**: Near-real-time (events typically appear within 24-72 hours)
- **Docs**: https://acleddata.com/acleddatanew/wp-content/uploads/dlm_uploads/2021/11/ACLED_API-User-Guide_11.2021.pdf
- **Score**: 8/18

## Overview

ACLED (Armed Conflict Location & Event Data Project) is a global conflict tracking database that codes violent and non-violent political events from news reports, NGO alerts, and local sources. For Iraq, ACLED tracks:
- **Battles** — clashes between armed groups, state forces vs ISIS remnants
- **Explosions/Remote violence** — IEDs, rockets, airstrikes
- **Violence against civilians** — killings, kidnappings, attacks on civilians
- **Protests and riots** — demonstrations, civil unrest (Iraq has frequent protests over services)
- **Strategic developments** — arrests, checkpoints, looting

Iraq has consistently been one of the highest-event-density countries in ACLED's global dataset, particularly during:
- 2014-2017 — ISIS insurgency
- 2019-2021 — protest movements and government crackdowns
- 2020s — ongoing low-intensity conflict with ISIS remnants, militia violence

ACLED data is widely used by journalists, researchers, and humanitarian organizations for situational awareness.

## Endpoint Analysis

**API exists but requires authentication** — ACLED requires an API key.

Attempted request without key:
```
curl https://api.acleddata.com/acled/read?country=Iraq&limit=1
# Result: Authentication error or connection block
```

ACLED API access tiers:
- **Free tier** — 10,000 rows per year, API key required (email registration)
- **Academic tier** — 100,000 rows per year, API key required
- **Commercial tier** — paid licenses for higher volumes and real-time access

The **free tier is not viable for real-time bridging** (10,000 rows/year = ~27 events/day globally, Iraq alone has 5-20 events/day during active periods, so the quota would be exhausted in weeks).

Sample response structure (from documentation):
```json
{
  "data": [{
    "event_id_cnty": "IRQ12345",
    "event_date": "2026-05-22",
    "year": 2026,
    "time_precision": 1,
    "event_type": "Battles",
    "sub_event_type": "Armed clash",
    "actor1": "Iraqi Security Forces",
    "actor2": "Islamic State (Iraq)",
    "country": "Iraq",
    "admin1": "Ninawa",
    "admin2": "Mosul",
    "latitude": 36.34,
    "longitude": 43.11,
    "fatalities": 3,
    "notes": "...",
    "source": "Reuters"
  }]
}
```

Key fields:
- `event_id_cnty` — unique event ID (country-prefixed)
- `event_date` — date of event (ISO 8601 date, no time)
- `event_type`, `sub_event_type` — classification
- `latitude`, `longitude` — location (estimated from place names, not GPS)
- `fatalities` — casualty count (if known)
- `actor1`, `actor2` — parties involved

## Integration Notes

- **Free tier not viable**: 10,000 rows/year is too limited for a continuous bridge.
- **Commercial/academic tiers**: Would require negotiation with ACLED for API access.
- **Alternative**: ACLED publishes weekly CSV exports on their website (free download, no API key). A polling bridge could download the CSV weekly and emit new events. But this is **batch (weekly)**, not real-time.
- **Latency**: ACLED events typically appear 24-72 hours after the incident (time for news reports to be coded), so even with full API access, this is **near-real-time**, not real-time.
- **Kafka keying**: Use `event_id_cnty` (unique per event).
- **Volume**: Iraq has 5-20 ACLED events per day during active conflict periods, 2-5 per day during quieter periods.

## Use Cases

- **Humanitarian situational awareness** — track conflict intensity by region
- **Correlation with other data** — e.g., ACLED battle events in oil fields correlating with gas flaring changes, protests correlating with power outages
- **Research** — analyze spatial and temporal conflict patterns

## Licensing Concerns

ACLED data has **terms of use** that may restrict redistribution:
- Free tier: personal use, research, limited publication
- Commercial tier: requires license

Emitting ACLED data into a public Kafka topic may require commercial licensing or explicit permission. This is a **legal/licensing question**, not a technical one.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | 24-72 hour latency, batch weekly for free tier |
| Openness | 1 | Free tier limited, API key required, licensing restrictions |
| Stability | 3 | Established project, documented API |
| Structure | 3 | JSON/CSV, documented schema |
| Identifiers | 3 | Unique event IDs, perfect keys |
| Richness | 2 | Event type, location, actors, casualties, notes |

**Verdict**: ⚠️ **Marginal / Licensing concerns** — ACLED is a high-quality conflict event dataset for Iraq. But:
1. **Free tier is too limited** for real-time bridging (10,000 rows/year)
2. **Near-real-time, not real-time** (24-72 hour latency)
3. **Licensing restrictions** may prohibit redistribution into a public Kafka topic without commercial license

**Only viable if**:
- ACLED grants permission for public redistribution (unlikely without paid license)
- OR, the bridge is for private/research use with API access via academic tier
- OR, weekly batch CSV download is acceptable (not real-time)

For Iraq frontier discovery, **note ACLED as a high-value source but blocked by licensing and rate limits**. Not viable for open real-time bridging without negotiation.
