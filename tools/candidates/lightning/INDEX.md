# Lightning Detection — Candidate Data Sources

Research completed: 2026-04-06 (Round 1), 2026-04-06 (Round 2 — satellite-based, Canadian, commercial survey)

## Summary

| Source | Region | Protocol | Auth | Freshness | Total | Status |
|--------|--------|----------|------|-----------|-------|--------|
| [NOAA GLM (GOES)](noaa-glm-goes.md) | Western Hemisphere | AWS S3 + SNS | None | 20-second files | **17/18** | ✅ Recommended |
| [EUMETSAT MTG-LI](eumetsat-mtg-li.md) | Europe/Africa/Atlantic | REST/OpenSearch | Free registration | ~10 min | **16/18** | ✅ Recommended |
| [Vaisala GLD360/NLDN](vaisala-gld360-nldn.md) | Global/USA | Commercial | Commercial license | Real-time | **15/18** | ❌ Dismissed (commercial) |
| [Blitzortung.org](blitzortung.md) | Global | WebSocket | None | Real-time (<1s) | **14/18** | ✅ Recommended |
| [CLDN Canada](cldn-canada.md) | Canada | OGC WMS | None | 10-min density | **14/18** | ✅ Viable |
| [Earth Networks ENTLN](earth-networks-entln.md) | Global | REST (Azure APIM) | Commercial | Real-time | **13/18** | ❌ Dismissed (commercial) |
| [DWD Lightning](dwd-lightning.md) | Germany/Europe | File download | None | ~10 min files | **13/18** | ✅ Viable |
| [WWLLN](wwlln.md) | Global | Academic | Agreement required | Delayed | **8/18** | ❌ Dismissed (restricted) |

### Investigated But Not Catalogued (No Public Data)

| Source | Region | Result |
|--------|--------|--------|
| EUCLID | Europe | Consortium data-sharing only, no public endpoints. DWD publishes derived data. |
| LINET / nowcast GmbH | Global | Commercial only, no public endpoints. |
| Météorage | Europe/Africa | Commercial only (Météo-France subsidiary). |
| GPATS / MetraWeather | Asia-Pacific | Commercial only (now part of DTN). |
| Singapore NEA | Singapore | Lightning endpoint returns 403 on all API versions. |
| Japan Lightning | Japan | Not probed (expected commercial/portal-only). |

## Recommendations

**Tier 1 — Implement first:**
- **NOAA GLM** — Best open lightning data source discovered. 20-second file cadence on AWS S3, no auth, SNS push notifications, total lightning (CG+IC), NetCDF-4. Covers entire Western Hemisphere via GOES-19 (East) and GOES-18 (West).
- **Blitzortung.org** — True real-time WebSocket streaming of global lightning strikes. Community project but remarkably capable. ToS restrict redistribution.

**Tier 2 — High value additions:**
- **EUMETSAT MTG-LI** — European counterpart to GLM. First geostationary lightning imager for Eastern Hemisphere. Free registration, six product types, ~10-minute cadence. Together with GLM, provides near-global satellite-based lightning coverage.
- **DWD Lightning** — Professional-grade European lightning data from the EUCLID network, published as open data.

**Tier 3 — Regional value:**
- **CLDN Canada** — 2.5 km gridded lightning density via WMS, 10-minute updates, fully open. Gridded density product only — no individual stroke data.

**Dismissed:**
- **Vaisala GLD360/NLDN** — Gold standard commercial product. No open access.
- **Earth Networks ENTLN** — Well-documented REST API exists (developer portal, Azure APIM) but commercial-only.
- **WWLLN** — Academic network requiring data sharing agreements. Low detection efficiency.
- **EUCLID, LINET, Météorage, GPATS** — Commercial/consortium networks with no public data.

## Notes

Round 2 research dramatically expanded the lightning landscape. The discovery of two satellite-based
lightning imagers — NOAA GLM and EUMETSAT MTG-LI — transforms the integration strategy from
"Blitzortung is the only option" to a layered architecture with professional-grade satellite data
as the foundation.

### Coverage Architecture

```
┌──────────────────────────────────────────────┐
│  Satellite Layer (Total Lightning, CG + IC)  │
│  ┌────────────────┐  ┌────────────────────┐  │
│  │ NOAA GLM       │  │ EUMETSAT MTG-LI    │  │
│  │ (GOES-19 + 18) │  │ (MTG-I1 at 0°)     │  │
│  │ W. Hemisphere  │  │ Europe/Africa/Atl   │  │
│  │ 20s cadence    │  │ 10-min cadence      │  │
│  └────────────────┘  └────────────────────┘  │
├──────────────────────────────────────────────┤
│  Ground-Based Layer                          │
│  ┌────────────┐ ┌──────────┐ ┌────────────┐ │
│  │Blitzortung │ │DWD/EUCLID│ │CLDN Canada │ │
│  │ Global WS  │ │ Europe   │ │ WMS Grid   │ │
│  └────────────┘ └──────────┘ └────────────┘ │
└──────────────────────────────────────────────┘
```

The satellite layer provides continuous, calibrated total lightning detection over large regions.
The ground-based layer fills in with higher temporal resolution (Blitzortung: sub-second) and
regional professional networks (DWD, CLDN).

### Key Insight: Total Lightning vs CG-Only

GLM and MTG-LI detect total lightning (CG + IC), capturing ~5x more events than CG-only
ground networks. Intra-cloud lightning is a strong indicator of severe weather intensification —
useful for nowcasting thunderstorm development. Most ground-based commercial networks
(Vaisala, GPATS, Météorage) focus primarily on CG detection.
