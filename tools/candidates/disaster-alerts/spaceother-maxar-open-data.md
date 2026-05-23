# Maxar Open Data Program

- **Country/Region**: Global (disaster-activated regions)
- **Endpoint**: `https://www.maxar.com/open-data` (event-based index), S3 buckets per event
- **Protocol**: HTTP/S3 (static file hosting), AWS Open Data Registry
- **Auth**: None (public S3 buckets)
- **Format**: GeoTIFF (COG), shapefiles
- **Freshness**: Hours to days after disaster activation (then static archive)
- **Docs**: https://www.maxar.com/open-data, https://github.com/maxar-analytics/open-data
- **Score**: 10/18

## Overview

Maxar Open Data Program releases **commercial satellite imagery** (0.3-0.5m resolution) for **disaster response and humanitarian relief** under Creative Commons BY-NC 4.0 license. When a major disaster occurs (earthquake, hurricane, wildfire, flood, conflict, etc.), Maxar tasking its constellation (WorldView-1/2/3, GeoEye-1) and releases pre/post-event imagery to the public within 24-72 hours.

The program has been active since 2018, with **60+ events** covered (2024 Turkey-Syria earthquake, 2023 Maui wildfire, 2023 Libya floods, 2022 Ukraine conflict, 2021 Haiti earthquake, 2020 Beirut explosion, etc.). Imagery is hosted in **public S3 buckets** (one bucket per event) and indexed on Maxar's website + AWS Open Data Registry.

**Key features**:
- **0.3-0.5m resolution** — Commercial-grade imagery, best-in-class for damage assessment
- **Pre/post-event pairs** — Baseline + post-disaster captures for change detection
- **Disaster-activated** — Not continuous monitoring; only releases imagery after major events
- **Free for humanitarian use** — CC BY-NC 4.0 (attribution required, non-commercial)

**Limitations**:
- **Not real-time** — Imagery is released 24-72 hours after disaster, then becomes a static archive
- **Event-driven** — No standing coverage; only disasters that Maxar chooses to activate
- **Non-commercial license** — Cannot be used in commercial services or paid products

## Endpoint Analysis

**Open Data index verified** — Maxar maintains a list of events at https://www.maxar.com/open-data.

Each event has:
- Event name and date (e.g., "2024 Turkey-Syria Earthquake", "2023 Maui Wildfire")
- S3 bucket URL (e.g., `s3://maxar-opendata/events/turkey-earthquake-23/`)
- HTTP access (e.g., `https://maxar-opendata.s3.amazonaws.com/events/turkey-earthquake-23/`)
- Shapefile index of image footprints
- Pre-event and post-event subdirectories

**Example event structure** (2024 Turkey-Syria Earthquake):
```
s3://maxar-opendata/events/turkey-earthquake-23/
  ├── pre-event/
  │   ├── 10300100C6F18B00/
  │   │   └── 10300100C6F18B00.tif (0.5m GeoTIFF, captured 2023-01-15)
  │   ├── 1030010102D84D00/
  │   │   └── 1030010102D84D00.tif (0.3m GeoTIFF, captured 2023-01-20)
  ├── post-event/
  │   ├── 1030010102E45600/
  │   │   └── 1030010102E45600.tif (0.5m GeoTIFF, captured 2023-02-06)
  │   ├── 1030010102E98E00/
  │   │   └── 1030010102E98E00.tif (0.3m GeoTIFF, captured 2023-02-07)
  ├── index/
  │   └── footprints.shp (shapefile of all image footprints)
```

**Accessing imagery**:
```bash
# HTTP listing (if bucket allows listing)
curl -s https://maxar-opendata.s3.amazonaws.com/events/turkey-earthquake-23/

# Direct download
wget https://maxar-opendata.s3.amazonaws.com/events/turkey-earthquake-23/post-event/1030010102E45600/1030010102E45600.tif

# AWS CLI
aws s3 ls s3://maxar-opendata/events/ --no-sign-request
aws s3 sync s3://maxar-opendata/events/turkey-earthquake-23/post-event/ ./local/ --no-sign-request
```

**No API** — The program is a **static file repository**, not a queryable API. Discovering new events requires:
1. Scraping https://www.maxar.com/open-data (HTML page)
2. Monitoring AWS Open Data Registry changelog (https://registry.opendata.aws/)
3. Subscribing to Maxar blog RSS/Twitter announcements

**Data formats**:
- **GeoTIFF** — 0.3-0.5m resolution, 3-band RGB or 4-band multispectral (some events)
- **Shapefile** — Footprint index (GeoJSON would be preferable but not provided)
- **No STAC** — Metadata is minimal (file naming convention only)

## Schema/Sample

**File naming convention** (Maxar catalog ID):
- `10300100C6F18B00.tif` — 16-character hexadecimal scene ID
- No embedded metadata (acquisition time, sensor, cloud cover)

**Footprint shapefile** (index.shp):
```
OBJECTID | CATALOG_ID        | ACQ_TIME            | SENSOR    | CLOUD_COVER
1        | 10300100C6F18B00  | 2023-01-15T09:23:45 | WV02      | 0.0
2        | 1030010102D84D00  | 2023-01-20T10:15:12 | WV03      | 2.5
3        | 1030010102E45600  | 2023-02-06T08:45:33 | WV02      | 1.2
```

**Stable identifiers**: Catalog IDs are unique and stable. Suitable for Kafka keys: `{event_slug}/{catalog_id}`

## Why Strong

1. **Unmatched resolution** — 0.3-0.5m is **commercial-grade**. 10-15× better than Sentinel-2, 60-100× better than Landsat. Critical for building damage assessment, infrastructure mapping, and humanitarian response.
2. **Pre/post pairs** — Change detection is built-in. Compare baseline vs. post-disaster imagery.
3. **Disaster focus** — Targeted coverage for the events that matter most (earthquakes, hurricanes, wildfires, floods, conflicts).
4. **Free for humanitarian use** — CC BY-NC license is compatible with disaster response, research, and NGO work.
5. **AWS-hosted** — Public S3 buckets, no egress fees for AWS-based processing.

## Limitations

- **Not real-time** — Imagery is released 24-72 hours after disaster, then becomes **static**. No ongoing monitoring.
- **Event-driven only** — No standing coverage. Maxar decides which events to activate (typically major disasters with media attention).
- **Non-commercial license** — CC BY-NC 4.0 prohibits commercial use. Cannot be embedded in paid products or commercial services.
- **No API** — Discovery requires scraping HTML or monitoring AWS Open Data changelog. No queryable catalog.
- **No STAC** — Metadata is minimal (shapefile index only). No standardized CloudEvents-compatible schema.
- **Sparse coverage** — Only 60+ events since 2018. Not a continuous global monitoring system.
- **Unpredictable** — No SLA or commitment to activate for any specific event. Maxar chooses which disasters to cover.

## Integration Notes

**Recommended bridge pattern**: **Event scraper + static archive indexer**

1. **Event discovery** — Poll https://www.maxar.com/open-data (HTML scraping) or AWS Open Data Registry (JSON feed) daily.
2. **New event detection** — Compare discovered events against known list (SQLite or Kafka compacted topic).
3. **Bucket enumeration** — For each new event, list S3 bucket contents (`aws s3 ls`) to discover pre/post subdirectories and image files.
4. **Shapefile parsing** — Download `index.shp` and extract footprint metadata (catalog ID, acquisition time, sensor, cloud cover).
5. **Message groups** — One group for disaster events:
   - `maxar_disaster_events` — keyed by `{event_slug}` (e.g., `turkey-earthquake-23`)
   - Subject: `maxar-opendata/event/{event_slug}`
   - Payload: Event metadata (name, date, bbox, pre/post image count, S3 URLs)
6. **Reference data** — Emit image footprints as reference events:
   - `maxar_disaster_images` — keyed by `{event_slug}/{catalog_id}`
   - Payload: Catalog ID, acquisition time, sensor, cloud cover, S3 download URL, footprint geometry

**Why not emit raw imagery?** GeoTIFFs are **large** (100MB-1GB per scene). Kafka topics should carry **metadata + URLs**, not pixels.

**License compliance**: The bridge must:
- Include CC BY-NC attribution in CloudEvent metadata (`source: "maxar-opendata"`, `license: "CC-BY-NC-4.0"`)
- Document non-commercial restriction in CONTAINER.md and README
- Not redistribute imagery (only metadata + S3 URLs)

**Limitations for repo fit**:
- **Not continuous** — This is a **disaster archive**, not a real-time feed. Events are added sporadically (5-10 per year).
- **No push notifications** — Bridge must poll Maxar website or AWS registry daily.
- **Humanitarian niche** — Only useful for disaster response use cases. Not relevant for general EO monitoring.

## Verdict

**WEAK ACCEPT (niche utility)** — This is a **high-value disaster response source** with **unmatched resolution** (0.3-0.5m), but it has significant limitations:

1. **Not real-time** — Imagery is released 24-72 hours after disaster, then becomes a static archive. No ongoing monitoring.
2. **Event-driven** — Only 5-10 events per year. Not a continuous data stream.
3. **Non-commercial license** — CC BY-NC prohibits commercial use. Incompatible with paid services.
4. **No API** — Discovery requires HTML scraping. No standardized catalog.

**Recommended IF**:
- The repo wants to support **humanitarian disaster response** (earthquake damage, flood extent, wildfire perimeters)
- Users accept **non-commercial license** restrictions
- The repo is willing to build a **custom event scraper** (no API available)

**Skip IF**:
- The repo prioritizes **continuous real-time monitoring** (Maxar releases are sporadic)
- The repo targets **commercial users** (license prohibits this)
- The repo wants **standardized STAC integration** (Maxar data is not STAC-compliant)

Alternative: For **open + continuous disaster monitoring**, use:
- **Sentinel-2 L2A** (10m, 5-day revisit, fully open) for flood/fire extent
- **Sentinel-1 GRD** (10m SAR, all-weather) for flood mapping
- **MODIS/VIIRS** (500m, daily) for rapid fire/flood detection

Maxar's advantage is **resolution** (0.3m vs. 10m) for **building-level damage assessment**. But the **sporadic availability** and **non-commercial license** make it a **supplementary source** rather than a core feed.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 3 | Unmatched 0.3-0.5m resolution for disaster damage assessment |
| Freshness | 1 | 24-72h after disaster, then static (not continuous monitoring) |
| Openness | 1 | CC BY-NC (non-commercial only), requires attribution |
| Schema clarity | 1 | Minimal metadata (shapefile index only, no STAC) |
| Machine-readability | 2 | GeoTIFF (COG-compatible), shapefile, but no API |
| Repo fit | 2 | Event-driven (5-10/year), non-commercial license, niche utility |
