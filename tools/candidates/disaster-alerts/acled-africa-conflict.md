# ACLED — Armed Conflict Location & Event Data (Africa)

- **Country/Region**: Pan-African (all 54 countries, most detailed coverage globally)
- **Endpoint**: `https://api.acleddata.com/acled/read?key={KEY}&email={EMAIL}&country=Kenya&limit=5`
- **Protocol**: REST
- **Auth**: API key + email (free registration)
- **Format**: JSON, CSV
- **Freshness**: Weekly updates (events coded within 1–2 weeks of occurrence)
- **Docs**: https://apidocs.acleddata.com/
- **Score**: 14/18

## Overview

ACLED (Armed Conflict Location & Event Data) provides the most comprehensive
georeferenced conflict event dataset in the world, and Africa is where it started.
Every battle, protest, riot, violence against civilians, and strategic development
is coded with precise location, date, actors, and fatalities.

ACLED tracks 8 event types:
1. Battles
2. Violence against civilians
3. Explosions/Remote violence
4. Riots
5. Protests
6. Strategic developments
7. Agreements
8. Non-state actor dynamics

For African contexts, this data is critical for humanitarian planning, conflict
early warning, and understanding political stability.

## Endpoint Analysis

The ACLED API requires registration but is free for researchers and humanitarian
organizations:

```
GET https://api.acleddata.com/acled/read
  ?key={API_KEY}
  &email={EMAIL}
  &country=Kenya
  &event_date=2026-03-01|2026-04-06
  &event_date_where=BETWEEN
  &limit=10
```

Expected response:
```json
{
  "status": 200,
  "success": true,
  "data": [
    {
      "event_id_cnty": "KEN12345",
      "event_date": "2026-04-01",
      "event_type": "Protests",
      "sub_event_type": "Peaceful protest",
      "actor1": "Protesters (Kenya)",
      "country": "Kenya",
      "admin1": "Nairobi",
      "location": "Nairobi",
      "latitude": "-1.2921",
      "longitude": "36.8219",
      "fatalities": "0",
      "notes": "Description of event..."
    }
  ]
}
```

Query parameters: country, region, event_type, event_date, actor, location, admin levels.

## Integration Notes

- **Weekly bridge**: Poll the ACLED API weekly for each African country or use date
  range queries to detect new events since last poll.
- **Conflict early warning**: ACLED data drives early warning systems. A bridge could
  trigger alerts when conflict event frequency exceeds rolling averages.
- **Geospatial events**: Every event has precise lat/lon, enabling spatial CloudEvents
  with GeoJSON geometry.
- **Actor tracking**: ACLED codes specific armed groups, political parties, and
  security forces. This enables actor-level event streams.
- **Terms of use**: Free for research and humanitarian use. Commercial use requires a
  different license tier.
- **Complement with GDACS/ReliefWeb**: ACLED covers conflict; GDACS covers natural
  disasters; ReliefWeb covers humanitarian response. Together they provide comprehensive
  crisis monitoring.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Weekly updates |
| Openness | 2 | Free registration required |
| Stability | 3 | Academic institution backed, 20+ year track record |
| Structure | 3 | Clean JSON API, well-documented |
| Identifiers | 2 | ACLED event IDs |
| Richness | 2 | Event types, actors, fatalities, locations |
