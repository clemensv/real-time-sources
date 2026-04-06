# Eskom Loadshedding Status API

- **Country/Region**: South Africa
- **Endpoint**: `https://loadshedding.eskom.co.za/LoadShedding/GetStatus`
- **Protocol**: REST (HTTP GET)
- **Auth**: None
- **Format**: Plain text (integer)
- **Freshness**: Real-time (updates within minutes of stage changes)
- **Docs**: None (undocumented, reverse-engineered)
- **Score**: 11/18

## Overview

Eskom is South Africa's sole electricity utility, and loadshedding — rolling blackouts
to prevent grid collapse — is a defining feature of daily life for 60 million people.
This undocumented API returns the current loadshedding stage as a single integer. The
simplicity is almost comical: call the endpoint, get a number. Stage 0 means no
loadshedding, stages 1–8 represent increasingly severe load reduction (each stage sheds
an additional ~1,000 MW).

This is the raw source that downstream services like EskomSePush build upon. For a
CloudEvents bridge, it's the most upstream signal available.

## Endpoint Analysis

**Verified live** — returns `1` (integer, plain text).

Additional endpoints discovered through reverse engineering:

| Endpoint | Returns |
|---|---|
| `/LoadShedding/GetStatus` | Current stage (integer) |
| `/LoadShedding/GetScheduleM/{suburb_id}/{stage}/{province}/{total_days}` | Schedule for a suburb |
| `/LoadShedding/GetMunicipalities?Id={province_id}` | Municipality list |
| `/LoadShedding/GetSurburbData/?pageSize=100&pageNum=1&id={municipality_id}` | Suburb lookup |

The stage value semantics:
- `1` = Stage 0 (no loadshedding)
- `2` = Stage 1 (1,000 MW shed)
- `3` = Stage 2 (2,000 MW shed)
- ... up to `9` = Stage 8

Note the off-by-one: the API returns `stage + 1`.

## Integration Notes

Building a bridge is straightforward but requires nuance:

- **Polling**: No push mechanism exists. Poll every 1–2 minutes.
- **Change detection**: Emit a CloudEvent only when the stage changes. The value is
  often stable for hours, then changes suddenly.
- **Off-by-one correction**: Subtract 1 from the returned value for the actual stage.
- **Schedule enrichment**: Combine the status endpoint with the schedule endpoint to
  produce richer events that include affected suburbs and time windows.
- **Reliability**: The Eskom website itself goes down under load during stage changes
  (ironic for a power utility). Implement retries with backoff.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time stage changes |
| Openness | 3 | No auth required |
| Stability | 1 | Undocumented, Eskom website frequently unstable |
| Structure | 1 | Single integer, no JSON wrapper |
| Identifiers | 1 | Province/suburb IDs are opaque integers |
| Richness | 2 | Stage is the critical signal; schedules add depth |
