# Eskom Load Shedding API (South Africa)

**Country/Region**: South Africa
**Publisher**: Eskom (South African state utility)
**API Endpoint**: `https://loadshedding.eskom.co.za/LoadShedding/GetStatus`
**Documentation**: None (reverse-engineered from Eskom's load shedding web app)
**Protocol**: REST
**Auth**: None
**Data Format**: JSON (plain integer for status)
**Update Frequency**: Real-time (event-driven)
**License**: Publicly accessible

## What It Provides

Eskom's load shedding API provides the current load shedding stage for South Africa. Load shedding is South Africa's controlled rolling blackout system, implemented when electricity demand exceeds available supply. The API returns a simple integer indicating the current stage.

Known endpoints:

- `/LoadShedding/GetStatus` — Current national load shedding stage ✓ verified
- `/LoadShedding/GetScheduleM/{suburb_id}/{stage}` — Schedule for a specific suburb (returned 500 during testing)
- `/LoadShedding/GetMunicipalities/{province_id}` — List of municipalities
- `/LoadShedding/GetSurburbs/{municipality_id}` — Suburbs within a municipality

Status codes:
- `1` = No load shedding (Stage 0)
- `2` = Stage 1 (1,000 MW shed)
- `3` = Stage 2 (2,000 MW shed)
- `4` = Stage 3 (3,000 MW shed)
- `5` = Stage 4 (4,000 MW shed)
- `6` = Stage 5 (5,000 MW shed)
- `7` = Stage 6 (6,000 MW shed)
- ...up to Stage 8 (8,000 MW)

## API Details

```
GET https://loadshedding.eskom.co.za/LoadShedding/GetStatus
→ 1
```

The response is a bare integer (not wrapped in JSON object). Status `1` means no load shedding. During testing (April 2026), the response was `1` — South Africa was not actively load shedding.

Schedule endpoint (suburb-specific blackout windows):

```
GET https://loadshedding.eskom.co.za/LoadShedding/GetScheduleM/{suburb_id}/{stage}/{province}
```

This returned 500 during testing — may require valid suburb IDs from the municipality/suburb lookup endpoints.

## Freshness Assessment

The status endpoint reflects the current operational state and updates immediately when Eskom declares or lifts a load shedding stage. This is genuinely real-time — the data changes when the grid operator makes a decision, not on a fixed schedule.

## Entity Model

- **Stage**: Integer 0-8 (returned as stage + 1, so 1 = Stage 0)
- **Province**: Integer ID for South African provinces
- **Municipality**: Integer ID
- **Suburb**: Integer ID
- **Schedule**: Time blocks when a specific suburb loses power during a given stage

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time event-driven updates |
| Openness | 3 | No auth required |
| Stability | 1 | Undocumented, Eskom's infrastructure is notoriously unreliable, schedule endpoint returned 500 |
| Structure | 1 | Bare integer response (not JSON object), inconsistent endpoint behavior |
| Identifiers | 1 | Internal numeric IDs for suburbs/municipalities, no standard codes |
| Additive Value | 3 | Unique source — no other API tracks South Africa's load shedding status |
| **Total** | **12/18** | |

## Notes

- Load shedding is one of South Africa's most impactful infrastructure challenges. During the 2022-2023 crisis, the country was at Stage 6 for extended periods (6,000 MW of the ~46,000 MW grid capacity deliberately shed).
- Third-party aggregators like EskomSePush (https://esp.info) provide a much better API wrapping this data with push notifications, suburb lookups, and historical tracking. Their API requires a free token.
- The bare integer response format is unusual and fragile — a simple `GET` returning `1` with no wrapper, no content-type negotiation, nothing.
- Despite the low structure score, this is culturally and socially one of the most impactful energy data points globally — millions of South Africans check load shedding status multiple times daily.
- Consider pairing with EskomSePush for a more robust integration, or using this as the authoritative upstream source with a wrapper.
