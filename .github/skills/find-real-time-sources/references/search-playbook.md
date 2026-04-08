# Search Playbook

## Query Construction Strategy

Build web searches that combine three dimensions: **domain keywords**, **data-access indicators**, and **geographic scope**. The goal is to surface official open-data portals, API documentation pages, and developer guides — not news articles or Wikipedia overviews.

For country-specific discovery, translate all three dimensions into the target country's primary administrative/search language and run those queries first. Do not start national-source discovery with English-only searches unless the source is clearly supranational.

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
| Radiation | gamma dose rate, radiation monitoring, ODL, dosimetry | nuclear, Sievert, nSv/h, ambient dose |
| Wildfire | fire detection, hotspot, thermal anomaly, active fire | FIRMS, VIIRS, MODIS, fire radiative power, FRP |
| Lightning | lightning detection, stroke, flash, thunderstorm | Blitzortung, sferic, peak current, CG/IC |
| Tidal/sea level | tide gauge, sea level, tidal prediction, storm surge | IOC, GLOSS, residual, harmonic |
| Bikeshare | GBFS, bikeshare, bike availability, micromobility | docking station, e-scooter, free-floating |
| EV charging | charging station, OCPI, EV charger, connector status | EVSE, availability, CCS, CHAdeMO |
| Reservoir/dam | reservoir storage, dam level, pool elevation, inflow | acre-feet, capacity, Bureau of Reclamation, CDEC |
| Water quality | dissolved oxygen, turbidity, conductance, pH, water quality | continuous monitoring, WFD, NWIS, probe |
| Wikimedia | Wikipedia edits, Wikidata, EventStreams, recent changes | SSE, revision, page create, bot edit |
| OSM | OpenStreetMap, changeset, minutely diff, map edit | node, way, relation, replication |
| Parking | parking availability, garage occupancy, parking guidance | DATEX II, free spaces, parking lot |
| Road traffic | traffic flow, speed sensor, road weather, RWIS | DATEX II, incident, travel time, road surface |
| Volcano | volcanic eruption, ash advisory, VAAC, alert level | VONA, thermal anomaly, SO2, Smithsonian GVP |
| Snow/avalanche | snow depth, SWE, avalanche danger, SNOTEL | snow water equivalent, avalanche bulletin, danger level |
| Geomagnetic | geomagnetic, INTERMAGNET, Kp index, magnetic field | observatory, H/D/Z components, storm, aurora |
| Radio propagation | PSKReporter, WSPR, HF propagation, DX cluster | amateur radio, SNR, gridsquare, ionospheric |
| Coral/marine bio | coral bleaching, sea surface temperature, reef monitoring | degree heating weeks, Coral Reef Watch, chlorophyll |
| Citizen sensors | Sensor.Community, PurpleAir, Safecast, citizen science | crowdsourced, low-cost sensor, personal weather station |
| Noise | noise monitoring, LAeq, decibel, environmental noise | airport noise, traffic noise, sound level |
| Border crossing | border wait time, customs, checkpoint, crossing delay | CBP, lane, pedestrian, commercial |
| Power outage | power outage, utility, service disruption, restoration | customers affected, outage map, electric |
| Disaster alert | CAP, early warning, tsunami, flood forecast | GDACS, EFAS, Meteoalarm, alert level |
| Space/orbital | TLE, satellite tracking, conjunction, space debris | CelesTrak, two-line element, orbit, NEO |

### Data-Access Indicators

Append terms that signal a machine-readable API exists:

- `API`, `REST API`, `JSON`, `open data`, `developer`, `data portal`
- `real-time`, `live data`, `streaming`, `WebSocket`, `MQTT`, `SSE`
- `free`, `public`, `no authentication`, `open government data`
- `documentation`, `endpoint`, `swagger`, `OpenAPI`

Translate these indicators into the target country's primary language before searching national portals or agency sites.

### Geographic Patterns

For country-level searches, default to the primary language used by the target
country's agencies and open-data portals:

- **Translate domain and access terms fully**: use the country's primary-language wording for the phenomenon, API, freshness, and openness terms
- **Use the local script and spelling**: keep accents, umlauts, Cyrillic, Hangul, kana, etc.
- **Try the national open data portal first** using local-language terms: data.gov, data.gouv.fr, govdata.de, data.gov.uk, opendata.swiss
- **Search for the agency name directly** when you know it, in the language the agency uses publicly
- **For multilingual countries**, start with the responsible agency's primary working language; add other official languages only if needed
- **Use English only after local-language queries** for that country, or immediately for EU/international standards bodies, global aggregators, and cross-border programs

### Example Queries

```
# Hydrology
"water level" OR "discharge" API real-time JSON site:*.gov.au
KNMI API "open data" weather observations

# Air quality
OpenAQ API "air quality" real-time
"Sensor.Community" OR "Luftdaten" API JSON "open data"
EPA AirNow API documentation

# Radiation
"gamma dose rate" API real-time open data
EURDEP "radiological" data download API
BfS ODL Messnetz Schnittstelle API
"radiation monitoring" JSON API site:*.go.jp

# Wildfire
NASA FIRMS API "active fire" near-real-time
EFFIS "fire" API "open data" Copernicus
"wildfire" "hotspot" API JSON real-time

# Lightning
Blitzortung API WebSocket lightning real-time
"lightning" "detection" open data API JSON

# Tidal / sea level
IOC "sea level" monitoring API real-time
"tide gauge" API JSON open data -NOAA
UHSLC "fast delivery" tide data

# Bikeshare / GBFS
GBFS "gbfs.json" auto-discovery bikeshare
"bike share" OR "bikeshare" GBFS feed URL
MobilityData GBFS catalog

# EV charging
"open charge map" API documentation
OCPI "charging station" availability API
NOBIL "ladestasjoner" API
"borne de recharge" disponibilité API temps réel France
"punto de recarga" disponibilidad API tiempo real España
"estação de carregamento" disponibilidade API tempo real Portugal
"Ladesäule" Verfügbarkeit API Deutschland

# Reservoir
"reservoir storage" API real-time "Bureau of Reclamation"
CDEC "reservoir" California data API

# Geomagnetic
INTERMAGNET real-time data API download
"geomagnetic" "observatory" real-time data format

# Snow / avalanche
SNOTEL API "snow depth" real-time NRCS
SLF "avalanche" bulletin API Schweiz
avalanche.org API data

# Wiki
stream.wikimedia.org EventStreams documentation
"recent changes" stream API Wikimedia

# Miscellaneous
"datos abiertos" calidad aire API tiempo real España
"Wasserstand" API Echtzeit Deutschland
"qualité de l'air" API temps réel France
"stazione di ricarica" disponibilità API tempo reale Italia
"open data" earthquake API real-time -USGS
AIS vessel tracking open data API -MarineTraffic -VesselFinder
국가수자원관리 종합정보시스템 API
GTFS-RT feed URL transit real-time
"electricity generation" API real-time open data
"border wait time" API CBP JSON
"parking" "availability" API real-time open data DATEX
"power outage" API real-time utility
PSKReporter API "propagation" amateur radio
"coral reef watch" API "sea surface temperature"
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

- **EU Open Data Portal**: data.europa.eu — aggregates member state portals (see detailed querying guide below)
- **Copernicus services**: land, marine, atmosphere, climate, emergency — all have APIs
- **EEA**: European Environment Agency — air quality, water, noise
- **ENTSO-E / ENTSO-G**: pan-European electricity and gas transparency platforms
- **National portals**: data.gouv.fr, govdata.de, dati.gov.it, datos.gob.es, data.overheid.nl, opendata.swiss

#### data.europa.eu — Programmatic Discovery

The EU Open Data Portal at `data.europa.eu` harvests DCAT-AP metadata from
all EU/EEA national portals plus institutional catalogs. It exposes two
machine-readable endpoints that are invaluable for systematic cross-country
source discovery.

**REST Search API** — `https://data.europa.eu/api/hub/search/`

Best for: faceted discovery, country/format breakdowns, initial scoping.

```
# Basic search — returns dataset count, facets, and result pages
GET /search?q="water+level"&filters=dataset&limit=50

# Country-scoped (national data only, excludes EU institutional)
GET /search?q="air+quality"&filters=dataset&countryData=true&limit=50

# Filter by category (DCAT theme codes: TRAN, ENER, ENVI, TECH, etc.)
GET /search?q="charging+station"&filters=dataset&facets={"categories":["TRAN","ENER"]}&limit=50
```

Key parameters:
- `q` — full-text query; use exact phrases with `"quotes"` and language-
  specific terms (e.g. `"IRVE"`, `"Ladesäule"`, `"laadpaal"`)
- `filters=dataset` — restrict to datasets (not catalogs, distributions, etc.)
- `limit` — up to 1000 results per page; use `0` for facet-only queries
- `countryData=true` — filter to national-level catalogs only
- `facets` — JSON object to filter by category, country, format, etc.

Response includes `result.count`, `result.facets` (country, catalog, format,
keywords breakdowns), and `result.results[]` with full dataset metadata
including `distributions[].access_url` and `distributions[].format`.

**SPARQL Endpoint** — `https://data.europa.eu/sparql`

Best for: drilling into distributions of known datasets, finding download URLs,
joining dataset metadata with distribution format/access info.

```sparql
PREFIX dcat: <http://www.w3.org/ns/dcat#>
PREFIX dct:  <http://purl.org/dc/terms/>

SELECT ?dataset ?title ?access_url
WHERE {
  ?dataset a dcat:Dataset ;
           dct:title ?title ;
           dcat:distribution ?dist .
  ?dist dcat:accessURL ?access_url .
  FILTER(CONTAINS(LCASE(STR(?title)), "water level"))
  FILTER(CONTAINS(LCASE(STR(?access_url)), "json") ||
         CONTAINS(LCASE(STR(?access_url)), "api"))
  FILTER(LANG(?title) = "en" || LANG(?title) = "")
}
LIMIT 100
```

POST to `https://data.europa.eu/sparql` with
`Content-Type: application/x-www-form-urlencoded` and `Accept:
application/sparql-results+json`. Complex GROUP BY queries may time out
(HTTP 500); keep queries simple with FILTER + LIMIT.

**Effective querying strategy:**

1. Run REST `limit=0` queries per language-specific term to get faceted
   counts by country — this reveals which countries have data for a domain.
2. Use SPARQL to find actual download/API URLs by filtering on `access_url`
   containing `json`, `csv`, or `api`.
3. Always search in **multiple languages** — French `"borne de recharge"`,
   German `"Ladestation"`, Dutch `"laadpaal"`, etc. — because the portal
   indexes titles in their original language.

**Limitations**: Many key real-time sources operate outside the harvested
DCAT ecosystem (dedicated national platforms like Norway's NOBIL, Netherlands
NDW, Poland's EIPA, Lithuania's EV portal). The portal is strongest for France
(data.gouv.fr is well-indexed with ~74K datasets) and Germany (GovData).
Always supplement data.europa.eu queries with direct probing of national
agency websites.

### North America

- **data.gov**: US federal open data catalog (CKAN API — see below)
- **USGS**, **NOAA**, **EPA**, **FAA**, **EIA**: major US data agencies
- **open.canada.ca**: Canadian open data portal (also CKAN-based, same API pattern)
- **datos.gob.mx**: Mexican open data

#### Querying data.gov Programmatically

data.gov runs CKAN and exposes the full **CKAN Action API v3**. No
authentication is required.

**Base URL:** `https://catalog.data.gov/api/3/action/`

**Key Endpoints:**

| Action | Purpose | Example |
|--------|---------|---------|
| `package_search` | Full-text search with Solr filter queries | `?q="water level"&rows=20` |
| `package_show` | Single dataset by name or ID | `?id=toxics-release-inventory-tri` |
| `organization_list` | List publishing agencies | `?all_fields=true` |
| `group_list` | List topic groups | `?all_fields=true` |
| `tag_list` | List all tags | `?query=real-time` |

**Search Parameters:**

- `q` — full-text query; use `"quoted phrases"` for exact match
- `fq` — Solr filter query for faceted filtering:
  `fq=organization:noaa-gov`, `fq=res_format:API`,
  `fq=tags:real-time AND res_format:JSON`
- `rows` — results per page (max ~1000), default 10
- `start` — offset for pagination
- `sort` — `views_recent desc` (default), `metadata_modified desc`, `name asc`
- `facet=true&facet.field=["organization","res_format","tags"]` — get count
  breakdowns

**Response Shape:**
```json
{"success": true, "result": {"count": 24556, "results": [...]}}
```

Each result includes `organization.name` (e.g. `noaa-gov`, `epa-gov`),
`resources[]` with `format` and `url`, and `tags[]` with keyword names.

**Effective Strategy:**
1. Start broad: `package_search?q="water level"&facet=true&facet.field=["organization","res_format"]&rows=0`
   to get facet counts without retrieving full results.
2. Filter by format: `fq=res_format:API` or `fq=res_format:JSON` to find
   machine-readable endpoints.
3. Filter by agency: `fq=organization:noaa-gov` to scope to a known publisher.
4. Combine filters with AND: `fq=organization:epa-gov AND res_format:API`
5. Inspect `resources[].url` in results — these are the actual data endpoints.

**Example Discovery Queries:**
```
# Real-time APIs across all agencies
package_search?q="real-time"&fq=res_format:API&rows=20

# NOAA datasets with JSON resources
package_search?q=&fq=organization:noaa-gov AND res_format:JSON&rows=50

# Water/hydrology monitoring APIs
package_search?q="water level" OR "stream gauge"&fq=res_format:API&rows=20

# EV charging data
package_search?q="charging station" OR "electric vehicle"&fq=res_format:JSON&rows=20
```

**Limitations:**
- No SPARQL endpoint — CKAN only, no RDF graph queries.
- Many datasets are static file dumps (CSV, ZIP) rather than live APIs.
  Filter on `res_format:API` or `res_format:JSON` to find live endpoints.
- The catalog is a metadata index — the actual data lives at the agency's
  own URL. Always follow `resources[].url` to verify the endpoint works.
- Coverage skews federal; state/local open-data portals (e.g.
  `data.ny.gov`, `data.ca.gov`) run separate CKAN or Socrata instances
  and are not fully indexed here.

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
- **Don't start in English for national-source discovery** — the best government data portals are often only documented in the national language, and English-first searches will systematically miss them.
- **Don't over-index on one country** — spread coverage across regions for a diverse, resilient catalog.
- **Don't skip the license check** — open doesn't always mean free to redistribute. Verify the license explicitly.
