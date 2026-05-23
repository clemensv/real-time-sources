# ReliefWeb API - Iraq Humanitarian Alerts and Reports

- **Country/Region**: Global (Iraq filter available)
- **Endpoint**: `https://api.reliefweb.int/v1/reports`
- **Protocol**: HTTP REST API
- **Auth**: None (optional app registration for higher rate limits)
- **Format**: JSON
- **Freshness**: Near-real-time (reports appear within minutes to hours of publication)
- **Docs**: https://apidoc.reliefweb.int/
- **Score**: 10/18

## Overview

ReliefWeb is a humanitarian information service run by OCHA (UN Office for the Coordination of Humanitarian Affairs). It aggregates alerts, situation reports, and press releases from UN agencies, NGOs, governments, and media covering humanitarian crises worldwide.

For Iraq, ReliefWeb tracks:
- **Conflict incidents** — attacks, explosions, civilian casualties
- **Displacement** — IDP movements, camp populations
- **Natural disasters** — floods, extreme heat, dust storms
- **Health emergencies** — disease outbreaks, hospital attacks
- **Food security** — WFP alerts, crop failures

ReliefWeb is **not real-time sensor data** (it's text reports, not telemetry), but it is a **near-real-time alert feed** for humanitarian events in Iraq.

## Endpoint Analysis

**API partially accessible** — basic queries work without auth, but full access requires app registration.

Sample query for Iraq reports (last 5):
```
GET https://api.reliefweb.int/v1/reports?appname=rwint-user-0&filter[field]=country.iso3&filter[value]=IRQ&limit=5
```

Attempted this query earlier — connection failed (possibly rate-limited or network issue). Retrying with curl:

```bash
curl -s "https://api.reliefweb.int/v1/reports?appname=rwint-user-0&filter[field]=country.iso3&filter[value]=IRQ&limit=5"
```

Expected response structure:
```json
{
  "data": [{
    "id": "1234567",
    "fields": {
      "title": "Iraq: Displacement Update - May 2026",
      "country": [{"iso3": "IRQ", "name": "Iraq"}],
      "date": {"created": "2026-05-23T12:00:00+00:00"},
      "source": [{"name": "IOM"}],
      "format": [{"name": "Situation Report"}],
      "url": "https://reliefweb.int/report/iraq/..."
    }
  }]
}
```

Key fields:
- `id` — unique report ID
- `title` — report headline
- `date.created` — publication timestamp (ISO 8601)
- `source` — publishing organization
- `format` — report type (News, Situation Report, Alert, etc.)
- `url` — link to full report

## Integration Notes

- **Polling bridge**: Query every 5-15 minutes for new reports (`filter[field]=date.created&filter[value][from]=<last_check>`)
- **Kafka key**: Use `id` (unique report ID)
- **Not telemetry**: This is a **text document feed**, not numeric sensor data. Events would be report publications (metadata + summary text), not measurements.
- **Volume**: Iraq typically has 2-10 new reports per day (varies with conflict intensity and humanitarian activity)
- **Relevance**: Useful for situational awareness and correlating with other Iraq data sources (e.g., ACLED conflict events, IOM displacement)
- **Alternative: RSS** — ReliefWeb also offers RSS feeds by country, which might be simpler than the API for polling
- **App name required**: The API requires an `appname` query parameter (can be generic like `rwint-user-0`, or register for a custom app name for higher rate limits)

## Use Cases for Iraq

- **Humanitarian dashboard** — track UN/NGO reports on Iraq crises in near-real-time
- **Correlation** — link ReliefWeb conflict reports with ACLED event data or seismic events (e.g., earthquake → relief response)
- **News aggregation** — feed into a real-time Iraq news and alerts system

This is a **different pattern** from the existing repo sources (most are sensor telemetry). ReliefWeb is a **document/alert feed**. But it fits the "real-time data" definition (sub-hour publication latency).

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Near-real-time (minutes to hours after publication) |
| Openness | 2 | No auth for basic use, app name required, rate limits |
| Stability | 3 | OCHA operational, documented API |
| Structure | 2 | JSON, documented schema |
| Identifiers | 3 | Unique report IDs, perfect keys |
| Richness | 1 | Metadata + summary, full text requires link follow |

**Verdict**: ⚠️ **Marginal** — ReliefWeb is a **near-real-time alert feed** for humanitarian reports, not sensor telemetry. For Iraq, it tracks conflict, displacement, disasters, and relief operations. This is a **different data type** from the repo's typical sensor/observation sources, but it is structured, real-time, and has stable IDs. **Only add if the repo's scope includes text alert feeds alongside telemetry.** If the focus is strictly numeric observations (weather, earthquakes, water levels), skip this. If humanitarian/news alerts are in scope, this is a viable source.
