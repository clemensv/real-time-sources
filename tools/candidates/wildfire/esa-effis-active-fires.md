# ESA EFFIS Active Fire Detection (VIIRS/MODIS)

- **Country/Region**: Europe, Middle East, North Africa (EMENA)
- **Endpoint**: `https://maps.effis.emergency.copernicus.eu/effis?service=WFS&request=GetFeature&typename=ms:modis.firepts&outputformat=geojson`
- **Protocol**: OGC WFS 1.1.0 (GeoJSON output)
- **Auth**: None
- **Format**: GeoJSON
- **Freshness**: Daily (MODIS Terra/Aqua 4× daily, VIIRS S-NPP/NOAA-20 twice daily)
- **Docs**: https://effis.jrc.ec.europa.eu/, https://forest-fire.emergency.copernicus.eu/applications/data-and-services/
- **Score**: 13/18

## Overview

EFFIS (European Forest Fire Information System) is the Copernicus Emergency Management
Service component for wildfire monitoring across Europe, the Middle East, and North Africa.
It processes thermal anomaly detections from NASA's MODIS (Moderate Resolution Imaging
Spectroradiometer) and VIIRS (Visible Infrared Imaging Radiometer Suite) satellites to
identify active fires and map burnt areas.

Active fire points are detected from:
- **MODIS** (Terra at ~10:30/22:30 local, Aqua at ~13:30/01:30 local) — 1km spatial resolution
- **VIIRS** (S-NPP and NOAA-20 at ~13:30/01:30 local) — 375m spatial resolution

The EFFIS WFS service publishes fire hotspots updated **daily** with attributes including:
- Fire detection timestamp (UTC)
- Satellite source (MODIS Terra, MODIS Aqua, VIIRS S-NPP, VIIRS NOAA-20)
- Fire radiative power (FRP in MW)
- Brightness temperature (K)
- Confidence level (low/nominal/high)
- Country code

EFFIS complements the global NASA FIRMS service but focuses on the EMENA region with
European institutional backing and integration with national fire services.

## Endpoint Analysis

The EFFIS WFS service provides several queryable layers. The most relevant for near-real-time
fire detection are:

1. **Active fire points** (`ms:modis.firepts`) — all MODIS/VIIRS hotspots
2. **Active fire polygons** (`ms:modis.ba.poly`) — burnt area perimeters (updated less frequently)

**Live probe** of the active fire points layer:

```bash
curl -s "https://maps.effis.emergency.copernicus.eu/effis?service=WFS&request=GetFeature&typename=ms:modis.firepts&outputformat=geojson&time=2026-01-01/2026-01-15" | jq '.features | length'
```

The WFS endpoint is operational and returns GeoJSON FeatureCollections. Time filtering is
supported via the `time` parameter (ISO 8601 date range).

Additional WFS capabilities:
- `GetCapabilities` — service metadata
- Spatial filter via `bbox` parameter
- Property filter via `cql_filter` (Common Query Language)
- Multiple output formats: GeoJSON, Shapefile, GML, KML, CSV

Example CQL filter for high-confidence fires in the last 24 hours:
```
confidence='h' AND time >= '2026-01-14T00:00:00Z'
```

## Schema / Sample Payload

GeoJSON feature from the `modis.firepts` layer:

```json
{
  "type": "Feature",
  "id": "modis.firepts.12345",
  "geometry": {
    "type": "Point",
    "coordinates": [23.456, 41.789]
  },
  "properties": {
    "fireDate": "2026-01-15",
    "fireTime": "1234",
    "satellite": "VIIRS_SNPP",
    "confidence": "h",
    "frp": 45.3,
    "brightness": 345.6,
    "bright_t31": 298.1,
    "country": "GR",
    "region": "Attica",
    "x": 23.456,
    "y": 41.789
  }
}
```

Field descriptions:
- **fireDate** — detection date (YYYY-MM-DD)
- **fireTime** — detection time (HHMM UTC)
- **satellite** — `MODIS_TERRA`, `MODIS_AQUA`, `VIIRS_SNPP`, `VIIRS_NOAA20`
- **confidence** — `l` (low), `n` (nominal), `h` (high)
- **frp** — Fire Radiative Power in megawatts (MW) — proxy for fire intensity
- **brightness** — brightness temperature in Kelvin at ~4μm
- **bright_t31** — brightness temperature at 11μm (channel 31)
- **country** — ISO 3166-1 alpha-2 code
- **region** — NUTS-1 or country-specific administrative region

The **FRP** (Fire Radiative Power) is the key intensity metric. High FRP (>100 MW) indicates
large, intense fires. Agricultural burns typically show <10 MW.

## Why Strong

| Criterion | Score | Rationale |
|-----------|-------|-----------|
| **Value** | 3 | Wildfire monitoring is critical for emergency response, air quality, climate policy. EFFIS is the authoritative European source. |
| **Freshness** | 2 | Daily updates, 4–6 satellite overpasses per day for Europe. Not sub-hourly but operationally useful. MODIS/VIIRS data latency is ~3 hours from overpass to EFFIS publication. |
| **Openness** | 3 | No authentication, no API key, no rate limits. Fully open WFS service. |
| **Schema clarity** | 2 | WFS/GeoJSON with clear field names and units. Not as formally typed as OData or Protobuf, but well-documented. |
| **Machine-readability** | 2 | GeoJSON output is standard and parseable. WFS 1.1.0 is mature but not as developer-friendly as modern REST/STAC. |
| **Repo fit** | 1 | Fire hotspots lack stable entity IDs. Each detection is a new point event (lat/lon + timestamp). Kafka keying is problematic — fires are transient phenomena, not persistent entities like gauges or vessels. Could key by grid cell or country+date, but neither is ideal for deduplication. |

**Total: 13/18** — Promising but challenging keying model.

## Integration Notes

### Event Model

Fire hotspots are **ephemeral point events**, not persistent entities. The CloudEvents model
must accommodate this:

- **Subject**: `fire/hotspot/{country}/{grid_cell}` where `grid_cell` is a geohash-5 or H3-5 spatial index
- **Kafka key**: `{country}:{grid_cell}` (e.g., `GR:ezs42`) — allows regional partitioning
- **Payload**: GeoJSON feature properties + computed fields (geohash, H3 index, NUTS region)
- **Type**: `eu.copernicus.effis.fire.detected`
- **Source**: `satellite/{satellite}` (e.g., `satellite/VIIRS_SNPP`)

Alternatively, use **country+date** as the Kafka key and emit all detections for that
country/day in a single event payload. This reduces event count but increases message size.

### Deduplication Strategy

MODIS/VIIRS satellites can detect the same fire on multiple overpasses (morning/afternoon,
different satellites). EFFIS does **not** deduplicate detections across satellites or days.

The bridge must implement deduplication:
1. Compute spatial hash (geohash-6 or H3-8 ~1 km precision)
2. Create composite key: `{spatial_hash}:{fireDate}:{satellite}`
3. Store in bridge state (Redis or local SQLite)
4. Skip if seen within 24 hours

This ensures each fire pixel+date+satellite combination is emitted once, even if WFS is
polled multiple times per day.

### Poll Strategy

Poll the WFS endpoint every **2 hours** with a rolling 48-hour time window:

```bash
time=2026-01-13T00:00:00Z/2026-01-15T23:59:59Z
```

The 48-hour overlap ensures late-arriving detections (sometimes delayed by cloud processing)
are captured. Deduplication prevents re-emission.

Filter for high-confidence fires only (`confidence='h'`) to reduce false positives from
reflective surfaces, gas flares, and agricultural burns.

### Regional Scoping

EFFIS covers **55+ countries** in EMENA. For focused monitoring, filter by country via CQL:

```
country IN ('GR', 'IT', 'ES', 'PT', 'FR', 'TR')
```

This reduces payload volume and focuses on high-risk Mediterranean fire zones.

### VIIRS vs MODIS

**VIIRS** (375m) detects smaller fires than MODIS (1km) and provides better spatial precision.
Prioritize VIIRS detections when both sensors observe the same fire:

```python
if detection['satellite'].startswith('VIIRS'):
    priority = 1
elif detection['satellite'].startswith('MODIS'):
    priority = 2
```

Emit the highest-priority detection per spatial cell per day.

## Limitations

- **No stable fire IDs** — each detection is a new point, no fire perimeter tracking across days
- **Cloud gaps** — fires under persistent cloud cover are missed
- **Agricultural burns** — false positives from crop residue burning, especially in Eastern Europe and North Africa during harvest seasons
- **Commission errors** — reflective roofs, flares, and industrial facilities can trigger detections
- **Omission errors** — small fires (<100m²) under forest canopy are often missed
- **Daily latency** — not real-time; MODIS/VIIRS data reaches EFFIS ~3–6 hours after overpass
- **No historical archive via WFS** — the WFS serves rolling 30-day window; historical data must be requested separately

## Cross-Reference with NASA FIRMS

NASA FIRMS (`https://firms.modaps.eosdis.nasa.gov/api/`) provides **global** MODIS/VIIRS fire
data with similar attributes but:
- Requires free API key
- Covers worldwide (EFFIS is EMENA only)
- Lower administrative overhead (no WFS complexity)

**Trade-off**: EFFIS integrates with European fire services and includes NUTS regions;
FIRMS is global but less European-focused. Consider bridging **both** or choosing based on
geographic scope.

## Why It Matters

Wildfires are intensifying across Mediterranean Europe due to climate change. The 2023
Greek fires, 2022 France/Spain fires, and 2021 Turkey/Algeria fires all caused mass
evacuations, deaths, and billions in damages.

EFFIS fire data enables:
- **Early warning systems** — detect ignition within hours
- **Evacuation planning** — fire perimeters inform road closures
- **Air quality forecasting** — smoke plume modeling (combine with CAMS)
- **Agricultural insurance** — verify fire damage claims
- **Carbon accounting** — biomass burning emissions for climate inventories

Bridging EFFIS into Kafka allows **cross-domain correlation**:
- Fire FRP + CAMS PM2.5 → smoke exposure risk
- Fire hotspots + EFFIS FWI (Fire Weather Index) → fire spread prediction
- Fire location + Copernicus Land Cover → fuel type classification

## Verdict

⚠️ **Maybe** — High value for emergency management and environmental monitoring, but the
lack of stable fire IDs and ephemeral point-event nature makes keying and deduplication
complex. **Build** if the repo expands to cover transient phenomena (fires, floods, earthquakes)
as first-class event types. Alternatively, treat this as a **data-available notification**
service: poll EFFIS daily, emit one event per country with GeoJSON attachment of all detections.
