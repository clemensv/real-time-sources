# GraceDB — Gravitational Wave Candidate Alerts

**Country/Region**: Global
**Publisher**: LIGO/Virgo/KAGRA Collaboration
**API Endpoint**: `https://gracedb.ligo.org/api/`
**Documentation**: https://gracedb.ligo.org/documentation/
**Protocol**: REST (JSON)
**Auth**: None (read public events), X.509 cert (submit)
**Data Format**: JSON
**Update Frequency**: Real-time — events posted within seconds of detection
**License**: Public data for confirmed events; MDC (Mock Data Challenge) events always public

## What It Provides

GraceDB (Gravitational-wave Candidate Event Database) is the central repository for gravitational wave detection candidates from LIGO, Virgo, and KAGRA. When these interferometers detect a candidate event — a possible merger of black holes, neutron stars, or other compact objects — it gets registered in GraceDB within seconds. The database tracks the full lifecycle: initial trigger, parameter estimation, sky localization maps, classification probabilities, and follow-up observations.

This is arguably the most exotic real-time data source in this entire catalog. You're watching spacetime itself ripple.

## API Details

- **List superevents**: `GET /api/superevents/?format=json&count={n}&category={cat}` — paginated list of events
- **Single event**: `GET /api/superevents/{id}/` — full event details
- **Event log**: `GET /api/superevents/{id}/logs/` — activity log for an event
- **Sky maps**: `GET /api/superevents/{id}/files/` — localization sky maps (FITS, PNG)
- **Labels**: Events carry labels like `EM_READY`, `ADVOK`, `SKYMAP_READY`, `PASTRO_READY`, `GCN_PRELIM_SENT`
- **Categories**: `Production` (real observations), `MDC` (mock data challenges), `Test`
- **Pagination**: `count` parameter, cursor-based pagination via `numRows` / links
- **No auth for reads**: Public API returns JSON without authentication

## Freshness Assessment

During observing runs (O4, O5, etc.), real gravitational wave candidates appear within seconds of detection. The `created` timestamp on events reflects the moment of registration. Labels are added as the pipeline progresses — from initial trigger to parameter estimation to public alert (via GCN). Between observing runs, MDC events continue to populate the database for testing.

Confirmed live: API returned 6190 superevents, with the latest (`MS260406k`) created 2026-04-06 10:57:13 UTC with labels including `EM_READY` and `GCN_PRELIM_SENT`.

## Entity Model

- **Superevent**: `superevent_id` (e.g., `S240414a`, `MS260406k`), `category`, `created`, `t_0` (GPS time), `far` (false alarm rate)
- **Labels**: Set of strings indicating pipeline status and data quality
- **Files**: Sky maps, source properties, classification probabilities
- **Preferred event**: Best pipeline result for the superevent
- **Links**: HATEOAS-style links to sub-resources (labels, logs, files, events)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Seconds from detection to database entry |
| Openness | 3 | No auth for reads, public JSON API |
| Stability | 3 | Major scientific collaboration infrastructure, running since 2015 |
| Structure | 3 | Clean JSON, HATEOAS links, well-documented schema |
| Identifiers | 3 | Unique superevent IDs, GPS timestamps, pipeline identifiers |
| Additive Value | 3 | Utterly unique — no other source for gravitational wave candidates |
| **Total** | **18/18** | |

## Notes

- Perfect score. This is a unique, well-structured, real-time, no-auth API for one of the most extraordinary data streams in physics.
- During LIGO/Virgo observing runs, expect ~1 event per few days to weeks (mergers are rare).
- MDC events provide a continuous stream for testing and development even between observing runs.
- GraceDB events trigger GCN (already cataloged in space-orbital) — they're the upstream source.
- The sky localization maps (FITS files) are computationally derived probability distributions over the sky.
- False alarm rate (`far`) is a key quality metric — lower is better (more likely to be real).
