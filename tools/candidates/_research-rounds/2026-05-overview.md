# Research Rounds — May 2026

Two parallel research fleets ran in May 2026 against the candidate scouting
process described in `.github/skills/find-real-time-sources/SKILL.md`. They
added **233 candidate files across 42 topic folders**. No source was built
yet — every candidate carries its own verdict (✅ Build / ⚠️ Maybe /
⏭️ Reference / ❌ Skip) and the orchestrator queues only the ✅-Build
items into the global build backlog.

The four per-fleet narrative reports (Asian satellite survey, NOAA satellite
summary, Spaceother summary, UAE discovery report) sit next to this file
under `_research-rounds/` so they don't pollute the topic catalog.

---

## Fleet 1 — Gulf states (7 agents)

**Scope**: Kuwait, UAE, Oman, Saudi Arabia, Bahrain, Qatar, Iraq. Each
agent searched Arabic-first (Kurdish for KRG), probed every endpoint live,
and was constrained to a per-country filename prefix to avoid concurrent
write collisions.

| Country | Files | ✅ Build | ⚠️ Maybe | ⏭️ Ref | ❌ Skip | Top pick |
|---|---|---|---|---|---|---|
| Saudi Arabia (`sa-`) | 24 | 0 | 5 | 7 | 12 | SGS/Harrat volcanic seismicity (M6+ threat to Madinah) |
| UAE (`ae-`) | 24 | 2 | 17 | 0 | 5 | Careem BIKE + Yaldi Dubai GBFS 3.0 (verified, ready) |
| Iraq (`iq-`) | 17 | 1 | 2 | 1 | 13 | EMSC Zagros seismology (the only live channel — most ministries offline) |
| Kuwait (`kw-`) | 14 | 0 | 1 | 3 | 10 | None Kuwait-specific; rely on global aggregators |
| Qatar (`qa-`) | 14 | 0 | 7 | 0 | 7 | EMSC Qatar-Saudi border M4+ sequence (new 2025 cluster) + Open-Meteo dust |
| Oman (`om-`) | 11 | 1 | 2 | 3 | 5 | EMSC Arabian Peninsula (Makran subduction, tsunami threat) |
| Bahrain (`bh-`) | 10 | 1 | 2 | 0 | 7 | OBBI METAR (NOAA Aviation Weather, no auth) |
| **Total** | **114** | **5** | **36** | **14** | **59** | |

### Cross-Gulf findings worth repeating

- **GCCIA pan-Gulf grid is the regional holy grail.** Six-nation
  interconnect (200 GW, 3,000+ km), no public API, no transparency
  platform. If lobbied open, single bridge covers all six states.
- **OpenAQ, AISstream/AISHub, USGS, NOAA Aviation Weather, NASA FIRMS, GDACS**
  are the universal aggregators that already provide Gulf coverage as a
  side effect of being global. Per-country bridges are the wrong shape.
- **Gulf state digital maturity is uneven.** UAE (Dubai/Abu Dhabi) > Saudi
  Vision-2030 portals > Qatar (FIFA-2022 sensor legacy is sealed) > Oman/
  Bahrain (websites only) > Kuwait/Iraq (most ministry portals unreachable).
- **Qatar's FIFA-2022 smart-city build-out produced zero public GTFS-RT, zero
  TASMU sensor APIs, zero Kahramaa grid feeds.** A documented gap.
- **EMSC over USGS for Arabian Peninsula seismology.** EMSC is faster
  (2–5 min) for regional M2.5–4.5 events that USGS thresholds miss. Add as
  a regional sibling to the existing USGS bridge.

---

## Fleet 2 — Satellite Earth observation (6 agents)

**Scope**: NASA, ESA/Copernicus/Sentinel, NOAA satellite-derived products,
EUMETSAT + SAFs, JAXA+ISRO+KARI+CNSA+TASA, and the "other Western + open"
basket (USGS Landsat, CNES, DLR, ASI, UKSA, CSA, INPE, CONAE, SANSA,
Planetary Computer, NICFI, Maxar Open). **Russia explicitly excluded.**

| Agency basket | Prefix | Files | Top pick(s) |
|---|---|---|---|
| NASA | `nasa-` | 12 | EONET (16/18 ✅), TEMPO N-America hourly air quality (14/18 ✅) |
| ESA + Copernicus | `esa-` | 33 | CEMS Rapid Mapping (15/18 ✅), EFFIS Fire Weather (13/18 ✅), TROPOMI NO₂/SO₂/CO |
| NOAA satellite | `noaasat-` | 15 | SWPC Propagated Solar Wind (**18/18**), GOES X-ray + Proton flux (17/18 each) |
| EUMETSAT + SAFs | `eumetsat-` | 24 | LSA SAF Fire Radiative Power (15/18), OSI SAF ASCAT winds (14/18), H SAF precip (14/18), MTG Lightning Imager (16/18, pending API access verification) |
| Asia (excl. Russia) | `jaxa-` `isro-` `kari-` `cnsa-` `tasa-` | 11 | Himawari-9 on AWS (no auth, 10-min full disk + SST) is the runaway winner |
| Other Western + open | `spaceother-` | ~20 | Copernicus Data Space STAC (17/18), Element84 Earth Search (16/18), Microsoft Planetary Computer (16/18), INPE DETER + Queimadas (15-16/18) |
| **Total** | | **~115** | |

### Cross-fleet satellite findings

- **STAC-on-cloud is the new substrate.** Copernicus Data Space, Element84
  Earth Search (AWS), Microsoft Planetary Computer (Azure) — all serve
  multi-mission imagery with a single STAC interface. Build one STAC poller,
  cover dozens of missions. This is the highest leverage architecture
  change for the satellite-EO domain in this repo.
- **SWPC JSON APIs are exceptional.** No-auth, 1-minute cadence,
  clean JSON, perfect Kafka fit. The propagated solar wind (DSCOVR L1)
  scored a perfect 18/18 — first time any candidate has.
- **JAXA's Himawari-on-AWS is the gold standard for open access.** Korean,
  Indian, and Chinese geostationary equivalents (GK-2A, INSAT-3D, FY-4)
  have similar science quality but registration walls + language barriers
  collapse their effective openness.
- **File-based satellite products (NetCDF/HDF5/GRIB) are a poor fit for
  this repo's per-event Kafka model** unless wrapped in the
  notification-only pattern (emit one event per new granule with an S3 URL,
  not per-pixel events). This pattern is already used by the DMI radar
  feeder being built in worktree.
- **Event-driven satellite services (CEMS rapid mapping, EONET, INPE
  Queimadas, FIRMS, lightning imagers) are the natural fit.** Per-pixel
  imagery products are not, except via the notification pattern.
- **MTG Lightning Imager (16/18) is pending API access verification.**
  Worth a follow-up — if EUMETSAT Data Store carries it via HTTP (not just
  EUMETCast DVB-S broadcast), this is a top-tier addition.

---

## Build backlog impact

Combining both fleets, the ✅-Build set this round is small (~7 candidates
across both fleets, plus the existing 22-candidate pre-existing build
backlog documented in the May 2026 stocktake). Most agents converged on
the same pattern: **build the global/regional aggregator once, the
per-country/per-mission slice comes for free.**

Concrete ✅-Build adds queued by this round (not yet built):

| Candidate | Score | Topic | Why first |
|---|---|---|---|
| NOAA SWPC Propagated Solar Wind | 18/18 | space-weather | Perfect score, clean JSON, no auth |
| NASA EONET | 16/18 | wildfire | Multi-domain event aggregator |
| EMSC FDSN regional (Arabian Pen.) | 16/18 | seismology | Fills USGS sub-M4.5 gap |
| MS Planetary Computer STAC | 16/18 | imagery | Cloud-native multi-mission |
| Copernicus Data Space STAC | 17/18 | imagery | Official ESA, 1–2h NRT |
| CEMS Rapid Mapping | 15/18 | emergencies | RSS event feed of disaster activations |
| NASA TEMPO | 14/18 | air-quality | First hourly air-quality from space (N. America) |
| Careem BIKE Dubai GBFS | 13/18 | bikeshare-gbfs | Verified working, GBFS 3.0 |
| Yaldi Dubai GBFS | 13/18 | bikeshare-gbfs | Verified working, GBFS 3.0 |

The full pending-build backlog (these + the 22 from previous rounds) is
the orchestrator's input queue for the next build sprint.

---

## Hygiene notes

- All 233 candidate files match the required `<topic>/<prefix>-<slug>.md`
  layout. None of the agents touched existing INDEX.md files — that was
  done by the orchestrator (`tools/update_indexes.py`) after consolidation.
- 9 brand-new topic folders were created (`climate`, `emergencies`,
  `floods`, `ice`, `imagery`, `infrastructure`, `land`, `oceans`,
  `space-weather`). Each got a fresh INDEX.md from the same updater.
- Four free-form summary reports the agents wrote at the candidates root
  (Asian survey, NOAA summary, spaceother summary, UAE discovery) were
  moved under `_research-rounds/` with a `2026-05-` date prefix so they
  don't clutter the topic catalog.
- The script `tools/update_indexes.py` is idempotent — re-running it
  replaces any prior "## Round 2026-05" section it finds rather than
  duplicating it.
