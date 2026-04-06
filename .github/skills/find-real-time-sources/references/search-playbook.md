# Search Playbook

## Query Construction Strategy

Build web searches that combine three dimensions: **domain keywords**, **data-access indicators**, and **geographic scope**. The goal is to surface official open-data portals, API documentation pages, and developer guides — not news articles or Wikipedia overviews.

### Domain Keywords

Use the technical vocabulary that data publishers actually put in their docs:

| Domain | Primary terms | Secondary terms |
|--------|--------------|-----------------|
| Hydrology | water level, discharge, streamflow, river gauge, hydrometric | real-time, telemetry, station data, time series |
| Maritime/AIS | AIS, vessel tracking, ship position, maritime traffic | MMSI, VHF, coastal surveillance, port monitoring |
| Aviation | ADS-B, flight tracking, aircraft position, Mode S | transponder, radar, ICAO, airspace |
| Weather | weather observation, METAR, SYNOP, forecast, warning | CAP, GRIB, station data, radar imagery |
| Seismic | earthquake, seismic event, magnitude, epicenter | real-time, QuakeML, shakemap, felt report |
| Transit | GTFS, GTFS-RT, real-time transit, bus/train position | SIRI, vehicle location, arrival prediction |
| Energy | electricity generation, grid load, energy market, balancing | day-ahead, cross-border flow, generation mix |
| Air quality | air quality, PM2.5, ozone, NO2, monitoring station | AQI, pollutant, ambient air, hourly measurement |

### Data-Access Indicators

Append terms that signal a machine-readable API exists:

- `API`, `REST API`, `JSON`, `open data`, `developer`, `data portal`
- `real-time`, `live data`, `streaming`, `WebSocket`, `MQTT`, `SSE`
- `free`, `public`, `no authentication`, `open government data`
- `documentation`, `endpoint`, `swagger`, `OpenAPI`

### Geographic Patterns

For country-level searches, use both English and native-language terms:

- **Prefer native language** for national agencies: "Wasserstand API" beats "water level API Germany"
- **Try the national open data portal** first: data.gov, data.gouv.fr, govdata.de, data.gov.uk, opendata.swiss
- **Search for the agency name directly** when you know it: "BOM API Australia", "KNMI data platform"
- **Use regional aggregators**: EU Open Data Portal, Copernicus, GEOSS

### Example Queries

```
"water level" OR "discharge" API real-time JSON site:*.gov.au
KNMI API "open data" weather observations
"datos abiertos" calidad aire API tiempo real España
"open data" earthquake API real-time -USGS
AIS vessel tracking open data API -MarineTraffic -VesselFinder
국가수자원관리 종합정보시스템 API (Korean water resources)
GTFS-RT feed URL transit real-time
"electricity generation" API real-time open data
```

## Probing a Candidate

Once you find a promising endpoint, probe it systematically:

### 1. Documentation Check

- Is there an API reference with endpoint descriptions, parameters, and response formats?
- Is the data license stated? Look for CC-BY, OGL, public domain, or equivalent.
- Are there rate limits, and are they stated? Unstated limits suggest fragility.
- Is authentication required? If so, is the key free and self-service?

### 2. Freshness Probe

Make a request and check how old the newest data point is:

```
# For a REST endpoint — look at the most recent timestamp in the response
curl -s "https://example.com/api/v1/stations/latest" | jq '.features[0].properties.timestamp'

# Compare to current time
# If the gap is < 5 minutes: excellent (real-time)
# If 5–30 minutes: good (near-real-time)
# If 30–60 minutes: acceptable for polling
# If > 1 hour: borderline — check if this is just a quiet period or the actual cadence
```

For streaming endpoints (WebSocket, MQTT, SSE):

```
# Connect and measure message rate
# > 1 msg/sec: high volume, good for streaming bridge
# 1 msg/min to 1 msg/sec: moderate, still viable
# < 1 msg/min: may need combined polling + push approach
```

### 3. Payload Inspection

Check the response structure for bridge fitness:

- **Stable IDs**: Does each entity have a durable identifier (station code, MMSI, ICAO hex, gauge number)?
- **Timestamps**: Are timestamps present and machine-parseable (ISO 8601, epoch)?
- **Coordinates**: Are lat/lon included for geospatial entities?
- **Structured data**: Is it JSON, XML, Protobuf, or CSV with headers? (Good.) Or HTML, PDF, images? (Bad.)
- **Consistent schema**: Do different entities of the same type share the same field set?

### 4. Volume Estimation

Estimate the message rate to choose the right bridge pattern:

- **< 1 msg/sec**: polling bridge with moderate interval (30s–5min)
- **1–100 msg/sec**: streaming bridge (WebSocket, MQTT, SSE)
- **100–10,000 msg/sec**: streaming bridge, may need batching or partitioning
- **> 10,000 msg/sec**: needs careful design — topic filtering, sampling, or multiple bridge instances

### 5. Overlap Check

Before recommending a candidate, verify it doesn't duplicate existing coverage:

- Same data from the same upstream but through a different aggregator — skip it.
- Same domain but different geography — good, this is additive.
- Same geography but different domain — good.
- Same domain, overlapping geography, but different entity set or resolution — potentially good, note the overlap.

## Scoring Rubric

Rate each candidate 0–3 on each dimension, then sum for a total out of 18:

| Dimension | 0 | 1 | 2 | 3 |
|-----------|---|---|---|---|
| **Freshness** | Daily or worse | Hourly | Every few minutes | Sub-minute / streaming |
| **Openness** | Paid / restrictive | Free key, moderate limits | Free key, generous limits | No auth required |
| **Stability** | Undocumented, scraping | Documented but no versioning | Versioned API | Versioned + status page + SLA |
| **Structure** | HTML / PDF | CSV / untyped JSON | Typed JSON / XML with schema | Protobuf / formal spec |
| **Identifiers** | No stable IDs | IDs exist but unstable | Stable IDs, good key candidates | Hierarchical IDs, perfect for subject + key |
| **Additive value** | Duplicates existing source | Minor extension of existing | New region for existing domain | New domain or unique dataset |

- **15–18**: Strong candidate — proceed to bootstrap.
- **10–14**: Promising — worth a deeper probe or a feasibility write-up.
- **6–9**: Marginal — consider only if the domain or region is high priority.
- **0–5**: Skip.

## Regional Search Shortcuts

### Europe

- **EU Open Data Portal**: data.europa.eu — aggregates member state portals
- **Copernicus services**: land, marine, atmosphere, climate, emergency — all have APIs
- **EEA**: European Environment Agency — air quality, water, noise
- **ENTSO-E / ENTSO-G**: pan-European electricity and gas transparency platforms
- **National portals**: data.gouv.fr, govdata.de, dati.gov.it, datos.gob.es, data.overheid.nl, opendata.swiss

### North America

- **data.gov**: US federal open data catalog
- **USGS**, **NOAA**, **EPA**, **FAA**, **EIA**: major US data agencies
- **open.canada.ca**: Canadian open data portal
- **datos.gob.mx**: Mexican open data

### Asia-Pacific

- **data.go.jp**: Japan open data
- **data.go.kr**: South Korea open data (also KOSIS, Water Resources Management Information System)
- **data.gov.au**: Australia — also BOM (weather), Geoscience Australia
- **data.gov.in**: India open data
- **data.gov.sg**: Singapore open data (LTA for transit, NEA for weather)
- **data.gov.tw**: Taiwan open data

### Other

- **WMO OSCAR**: global catalog of weather observing stations
- **GEO/GEOSS**: Global Earth Observation System of Systems — discovery portal
- **OpenAQ**: global air quality aggregator with API
- **GBIF**: biodiversity (less real-time but worth noting)

## Anti-Patterns

- **Don't chase commercial aggregators** (MarineTraffic, FlightRadar24, Windy) — they sit on top of the same raw sources we want direct access to, and their terms prohibit redistribution.
- **Don't confuse a data viewer with a data API** — many portals have pretty dashboards but no machine-readable endpoint. Check for `/api/` in the URL or a "Developers" section.
- **Don't assume English-only** — the best government data portals are often only documented in the national language. Use translation tools.
- **Don't over-index on one country** — spread coverage across regions for a diverse, resilient catalog.
- **Don't skip the license check** — open doesn't always mean free to redistribute. Verify the license explicitly.
