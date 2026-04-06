# Seismology & Earthquake — Candidate Source Index

Scouted: 2026-04-06

## Already Implemented

| Source | Directory | Coverage | Notes |
|--------|-----------|----------|-------|
| USGS Earthquakes | `usgs-earthquakes/` | Global | GeoJSON feeds + FDSN; polled every minute; 20+ feed variants |

## Candidates Evaluated

| # | Candidate | File | Score | Coverage | Verdict |
|---|-----------|------|-------|----------|---------|
| 1 | **EMSC SeismicPortal** | [emsc-seismicportal.md](emsc-seismicportal.md) | **17/18** | Global | ✅ **Build** — WebSocket push + FDSN REST; best real-time option |
| 2 | **GFZ GEOFON** | [gfz-geofon.md](gfz-geofon.md) | **17/18** | Global (M4+) | ✅ **Build** — FDSN-compliant; major research center; complements USGS |
| 3 | **GeoNet New Zealand** | [geonet-nz.md](geonet-nz.md) | **16/18** | NZ / Pacific | ✅ **Build** — Cleanest API in this roundup; GeoJSON native |
| 4 | **INGV Italy** | [ingv-fdsnws.md](ingv-fdsnws.md) | **16/18** | Italy / Euro-Med | ✅ **Build** — FDSN-compliant; high-seismicity region |
| 5 | **JMA Japan** | [jma-japan.md](jma-japan.md) | **15/18** | Japan | ✅ **Build** — Uniquely detailed intensity data; custom JSON parsing needed |
| 6 | **ISC Bulletin** | [isc-bulletin.md](isc-bulletin.md) | **12/18** | Global | ⏭️ **Skip** — Not real-time (months-years delay); IRIS successor |
| 7 | **AFAD Turkey** | [afad-turkey.md](afad-turkey.md) | **11/18** | Turkey | ⚠️ **Maybe** — Unique local detail but flaky API; Turkey in EMSC already |
| 8 | **BGS UK** | [bgs-uk.md](bgs-uk.md) | **10/18** | UK | ⏭️ **Skip** — RSS only; very low seismicity; UK in EMSC already |
| 9 | **Geoscience Australia** | [geoscience-australia.md](geoscience-australia.md) | **9/18** | Australia | ⏭️ **Skip** — No public API; low seismicity; data in USGS/EMSC |

## Candidates Not Reachable / Dismissed

| Candidate | Reason |
|-----------|--------|
| **IRIS DMC** | Deprecated; retiring June 2026. Redirects to ISC and USGS. Returned HTTP 400. |
| **CSN Chile** | FDSN endpoint at `evtdb.csn.uchile.cl` returned 404. Web API unreachable. |
| **SSN Mexico** | `ssn.unam.mx` connection failed. No accessible API found. |
| **Kandilli Observatory (KOERI, Turkey)** | FDSN endpoint at `sc3.koeri.boun.edu.tr` returned 404. |
| **PHIVOLCS Philippines** | `earthquake.phivolcs.dost.gov.ph` connection failed. |

## Architecture Notes

### The FDSN Opportunity

Three of the top candidates — EMSC, GFZ, and INGV — all implement the **FDSN event web service** specification. The query parameters, response formats (text, QuakeML, JSON), and field semantics are identical across implementations. This creates a strong case for building a **generic FDSN bridge adapter** that can be configured for any FDSN-compliant endpoint simply by changing the base URL.

FDSN text format: `#EventID|Time|Latitude|Longitude|Depth/km|Author|Catalog|...`

A single parser covers EMSC, GFZ, INGV, and any future FDSN source.

### Recommended Build Order

1. **EMSC SeismicPortal** — WebSocket gives genuine real-time push; highest value
2. **FDSN Generic** (GFZ + INGV as initial targets) — reusable adapter pattern
3. **GeoNet NZ** — Clean GeoJSON API; distinct from FDSN pattern
4. **JMA Japan** — Custom parsing; unique intensity data

### Push vs. Poll

| Source | Mechanism | Latency |
|--------|-----------|---------|
| EMSC | WebSocket (SockJS) | Seconds |
| GeoNet NZ | Poll REST | Minutes |
| GFZ GEOFON | Poll FDSN | Minutes |
| INGV | Poll FDSN | Minutes |
| JMA | Poll JSON | Minutes |
| AFAD | Poll REST | Minutes |
| USGS (existing) | Poll GeoJSON | ~60 seconds |

Only EMSC provides genuine push delivery. All others require polling.
