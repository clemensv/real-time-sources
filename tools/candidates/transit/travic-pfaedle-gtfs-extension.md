# TRAVIC / trajserv + pfaedle — GTFS Shape Enrichment & Worldwide Feed Discovery

> ⏭ **SKIP** · Offline GTFS shape-generation toolchain (pfaedle/TRAVIC), not a real-time feed.

**Country/Region**: Global
**Publisher**: Patrick Brosi / University of Freiburg, Chair of Algorithms & Data Structures (TRAVIC, trajserv, pfaedle). TRAVIC was originally a geOps project; geOps still ships the matching client libraries and the commercial tracker API.
**API Endpoint**: https://travic.app/ (frontend) · backend `https://travic.cs.uni-freiburg.de/trajserv` (proxied as `/trajserv`) · geOps tracker API `https://api.geops.io/tracker/v1`
**Documentation**: https://travic.app · https://github.com/ad-freiburg/pfaedle · [SIGSPATIAL 2018 "Sparse map matching" paper](http://ad-publications.informatik.uni-freiburg.de/SIGSPATIAL_Sparse%20map%20matching%202018.pdf)
**Protocol**: N/A — a visualization/discovery platform **plus** an offline GTFS shape-matching toolchain. Neither is itself a new real-time feed; this note documents an **extension to the existing `gtfs/` bridge**.
**Auth**: TRAVIC frontend open · geOps tracker API requires a key (developer.geops.io) · pfaedle is a local CLI (no auth)
**Data Format**: GTFS (static) + GTFS-RT (realtime) **in**; GTFS `shapes.txt` (OSM-accurate polylines) **out**
**Update Frequency**: TRAVIC visualization polls ~every 3 s · pfaedle is an **offline batch** enrichment step
**License**: pfaedle is open source (see repo); **generated shapes are derived from OpenStreetMap → ODbL 1.0, attribution required**. The trajserv *server* is closed source; the surrounding parsing/harvesting toolchain is open.

## What It Provides

This is **not a new pollable source** — it is an *extension to GTFS* with two parts that complement the repo's existing generic `gtfs/` (GTFS-RT) bridge:

1. **pfaedle — a GTFS geometry extension.** GTFS trips reference their geographic path through the optional `shapes.txt` file. Many agencies omit it or ship crude straight-line shapes, so a map renderer draws vehicles teleporting between stops. pfaedle synthesizes high-quality `shapes.txt` by **map-matching each trip's ordered stop sequence onto OpenStreetMap, per transport mode** (rail on rails, tram on tram tracks, subway on subway, bus on roads, ferry on water). This is the direct "extension to GTFS": it enriches a feed the repo already ingests with accurate route geometry.
2. **TRAVIC / trajserv — worldwide feed discovery + a reference architecture.** TRAVIC ("Transit Visualization Client") renders schedule-interpolated and GTFS-RT vehicle movements for agencies worldwide. Its backend (`trajserv`) maintains a directory of every feed it tracks — a discovery surface comparable to the MobilityData and Transitland catalogs already noted in this folder.

## pfaedle — the GTFS shape extension (primary value)

- **What it does**: `pfaedle -x <OSM FILE> <GTFS FEED>` → writes a shape'd copy of the feed to `./gtfs-out` with a proper `shapes.txt` (and `shape_dist_traveled`). By default it only fills trips that lack a shape; `-D` recomputes all.
- **Algorithm**: sparse / HMM-style map-matching (Viterbi over an OSM-derived routing graph), first described in the ad-freiburg **SIGSPATIAL 2018** paper. It balances closeness-to-stops against routing cost, so noisy stop coordinates still match sensibly.
- **Mode awareness (`-m`)**: `tram`, `bus`, `coach`, `rail`, `subway`, `ferry`, `funicular`, `gondola`, `all`, or GTFS `route_type` codes incl. extended types (e.g. `-m 101` = high-speed rail). The mode picks the correct OSM network layer.
- **OSM pre-filter (`-X`)**: emits a minimal OSM file containing only what a given feed needs, so you don't re-parse `planet.osm` every run.
- **Packaging**: C++ (CMake; `gcc ≥ 5` / `clang ≥ 3.9`), official Docker image `ghcr.io/ad-freiburg/pfaedle`, config via `pfaedle.cfg`.
- **Debug**: `-T <tripId>` dumps one trip as GeoJSON; `--write-graph` / `--write-trgraph` export the routing/network graphs.

**How it extends this repo's `gtfs/` bridge**: the bridge emits GTFS-RT (`TripUpdate` / `VehiclePosition` / `Alert`) as CloudEvents. pfaedle is an *offline companion* that produces OSM-accurate trip geometry, useful if we ever (a) attach route polylines to emitted events, (b) render the feed on a map/KQL geospatial layer, or (c) improve interpolated positions for agencies that publish schedule-only data. It is an enrichment/extension, **not** a real-time feed in its own right.

## TRAVIC & the trajserv backend (discovery + reference architecture)

- The frontend config (`cfg.js`) sets `BACKENDURL = "/trajserv"`; the basemap (`l=osm_standard` in the permalink) is just OSM/HERE/Bing/Thunderforest tiles, independent of the transit data.
- **Source model**: GTFS **static** schedules drive interpolated movement; GTFS-**RT** overrides with live positions/delays where the agency publishes it. Route shapes are pfaedle/OSM-matched (the same OSM is used twice: basemap *and* geometry).
- **Feed directory**: the machine-readable list is `GET https://travic.app/trajserv/feeds` (returns a feed registry — name, bbox, publisher, realtime flag). The in-app **"Overview"** button lists every feed, and each **vehicle popup links to the publisher's website and license**. *(As of June 2026 the backend was temporarily in maintenance and the endpoint returned empty.)*
- **trajserv HTTP API** (documented by the open geOps client `geops/react-transit` → `src/layers/TrajservLayer.js`, base `https://api.geops.io/tracker/v1`):
  - `…/trajectory_collection?bbox=&btime=&etime=&date=&z=&key=` — all vehicle trajectories in a bbox/time window (polled ~3 s)
  - `…/trajstations?id=<trajId>&time=` — stops/timetable of one trajectory (delays, cancellations, wheelchair flags)
  - `…/trajectorybyid?id=<journeyId>&time=` — full shape geometry of one journey
  - filters: `publishedlinename`, `tripnumber`, `operator`
- **Successor**: geOps has since replaced trajserv with a WebSocket realtime backend, **Tralis** (`TralisLayer.js` in `geops/trafimage-maps`). Also closed source.

## Open toolchain (how to "build your own" trajserv)

The live-position server is proprietary, but the rest of the pipeline is open:

| Component | Repo | Role |
|-----------|------|------|
| **pfaedle** | `ad-freiburg/pfaedle` | GTFS → OSM-matched `shapes.txt` (the extension) |
| cppgtfs | `ad-freiburg/cppgtfs` | C++ GTFS parser pfaedle builds on |
| gtfsparser | `geops/gtfsparser` | Go GTFS parser |
| **gtfsman** | `geops/gtfsman` | manage & continuously update a large number of GTFS feeds (feed harvester) |
| loom | `ad-freiburg/loom` | automated transit-map generation |
| lossyrob/TRAVIC | `lossyrob/TRAVIC` | original (2014) open-source TRAVIC web client |

## Feasibility Rating

| Criterion      | Score | Notes                                                                 |
|----------------|-------|-----------------------------------------------------------------------|
| Freshness      | 1     | pfaedle is offline batch; TRAVIC is visualization/discovery, not a feed |
| Openness       | 2     | pfaedle + toolchain open (ODbL output); trajserv/Tralis server closed   |
| Stability      | 3     | Maintained by Uni Freiburg AD chair + geOps; pfaedle actively built     |
| Structure      | 3     | Standard GTFS `shapes.txt`; clean, well-defined                         |
| Identifiers    | 2     | GTFS `trip_id` / `shape_id`; trajserv journey IDs                       |
| Additive Value | 3     | Shape enrichment for the `gtfs/` bridge + worldwide feed discovery      |
| **Total**      | **14/18** |                                                                     |

## Notes

- **Primary takeaway**: pfaedle is an *extension to GTFS* — an OSM map-matching step that gives any GTFS feed (including those the `gtfs/` bridge consumes) accurate route geometry. It is enrichment tooling, not a real-time source.
- **Discovery angle** overlaps and complements [`mobilitydata-catalog.md`](mobilitydata-catalog.md) and [`transitland.md`](transitland.md): TRAVIC's `/trajserv/feeds` is another worldwide directory of GTFS / GTFS-RT endpoints that could seed automated `gtfs/` bridge deployment.
- The trajserv **server** itself has no public source (checked `ad-freiburg`, `geops`, and a global GitHub code search); only client libraries (`react-transit`, `mobility-toolbox-js`) and the 2014 `lossyrob/TRAVIC` client are open.
- **Attribution**: any redistributed pfaedle output must credit OpenStreetMap contributors (ODbL 1.0).
- **Not a candidate for a new bridge** — logged here as a GTFS extension/enrichment + discovery reference so the option isn't lost.
