---
name: find-real-time-sources
description: "Use when searching for new real-time or near-real-time open data sources worldwide that could be added to this repo. Covers domain taxonomy, search strategies, protocol fitness, freshness probing, and candidate ranking."
argument-hint: "Describe the domain of interest (e.g. hydrology, maritime, aviation, seismic), the geographic region or 'global', and any constraints on protocol, auth, or update frequency."
---

# Find Real-Time Sources

## When to Use

- Search for new data sources to add to this repo.
- Survey a geographic region or domain for open real-time feeds.
- Evaluate whether a candidate source is worth building a bridge for.
- Compare alternatives within a domain (e.g. multiple national AIS providers).

## Inputs

- **Domain** — one or more from the taxonomy below, or "any"
- **Region** — a country, continent, "global", or a list of target countries
- **Constraints** — max acceptable latency, auth preferences, protocol preferences, volume bounds

## Procedure

1. **Scope the search** using the domain taxonomy and region.
2. **Generate search queries** following the strategy in [search playbook](references/search-playbook.md).
3. **Probe each candidate** for freshness, protocol, auth, and volume.
4. **Score candidates** against the fitness criteria.
5. **Check for overlap** with sources already in this repo.
6. **Produce a ranked shortlist** with a one-paragraph assessment per candidate.

## What Makes a Good Source

A source is a strong candidate when it satisfies most of these:

- **Fresh** — data updates at least every few minutes; sub-minute is ideal.
- **Open** — no auth, or free API key with generous limits. Paid or restrictive OAuth is a red flag.
- **Stable endpoint** — a documented, versioned API or well-known protocol (REST, WebSocket, MQTT, SSE, TCP). Screen-scraping or undocumented endpoints are fragile.
- **Structured payload** — JSON, XML, Protobuf, or a binary wire format with a public spec. HTML or PDF-only outputs are not viable.
- **Stable identifiers** — entities in the stream have durable IDs (station codes, MMSI, flight ICAO hex, gauge numbers) that work as Kafka keys and CloudEvents subjects.
- **Meaningful volume** — enough events to be interesting for analytics, but not so many that a single bridge instance can't keep up without sharding.
- **Additive to the repo** — covers a new region, domain, or protocol pattern. Duplicating an existing source's exact coverage is low value unless it adds resilience.

## What Disqualifies a Source

- Data refreshes daily or less frequently (batch, not streaming).
- Requires paid commercial license or per-query billing.
- No machine-readable format (PDF reports, image-only dashboards).
- Unstable or undocumented endpoints likely to break without notice.
- Legal restrictions that prohibit redistribution or derived event streams.
- Payload lacks stable entity identifiers — no way to key events.

## Domain Taxonomy

Use these as search anchors. Each domain lists the kinds of entities and measurements that are typical, plus the government or institutional bodies that tend to publish the data.

### Hydrology and Water Monitoring

**Entities**: river gauges, reservoirs, groundwater wells, water quality stations
**Measurements**: water level, discharge/flow, temperature, conductivity, turbidity
**Typical publishers**: national hydrological services, environment agencies, water authorities
**Protocols**: REST polling (dominant), OData, WISKI/KIWIS
**Existing coverage**: Germany, Netherlands, France, Switzerland, Czech Republic, Poland, Norway, Sweden, Finland, UK, USA, Belgium
**White spots**: Spain, Italy, Austria, Portugal, Japan, South Korea, Australia, Canada, Brazil, India, China, African nations

### Maritime / AIS Vessel Tracking

**Entities**: vessels (keyed by MMSI), aids to navigation
**Measurements**: position (lat/lon), speed, course, heading, destination, ship type
**Typical publishers**: national maritime authorities, coast guards, port authorities
**Protocols**: MQTT, WebSocket, raw TCP/NMEA, REST
**Existing coverage**: Norway (Kystverket), Finland/Baltic (Digitraffic), global terrestrial (AISstream — currently broken)
**White spots**: Denmark (DMA), USA (MarineCadastre — historical only), Canada, Baltic states individually, Mediterranean nations, Asian maritime nations

### Aviation / ADS-B

**Entities**: aircraft (keyed by ICAO hex address), flights
**Measurements**: position, altitude, speed, heading, squawk, callsign
**Typical publishers**: national aviation authorities, community networks (ADSBx, OpenSky), local receivers
**Protocols**: BEAST binary (TCP), SBS BaseStation, REST, WebSocket
**Existing coverage**: local Mode-S receiver bridge
**White spots**: OpenSky Network API, ADS-B Exchange, FlightRadar24 (commercial), EUROCONTROL, FAA SWIM

### Weather and Atmospheric

**Entities**: weather stations, radar grids, forecast zones, warning areas
**Measurements**: temperature, pressure, wind, precipitation, humidity, visibility, alerts/warnings
**Typical publishers**: national meteorological services (WMO members), space agencies
**Protocols**: REST, file-server polling (GRIB, CAP XML, GeoJSON), WebSocket, LDM/IDD
**Existing coverage**: Germany (DWD), USA (NOAA NWS, NOAA NDBC, NOAA GOES)
**White spots**: UK Met Office (DataPoint), Météo-France, SMHI (weather, not just hydro), KNMI, JMA (Japan), KMA (South Korea), BOM (Australia), ECMWF (open data), Environment Canada

### Seismology and Geophysics

**Entities**: earthquakes, seismic events, volcanoes
**Measurements**: magnitude, depth, location, felt reports, tsunami alerts
**Typical publishers**: geological surveys, seismological institutes
**Protocols**: REST (GeoJSON, QuakeML), WebSocket, Atom/RSS
**Existing coverage**: USGS (global)
**White spots**: EMSC (European-Mediterranean), GeoNet (New Zealand), Geoscience Australia, JMA (Japan seismic), INGV (Italy), BGS (UK)

### Public Transit / GTFS

**Entities**: vehicles, trips, routes, stops, service alerts
**Measurements**: real-time position, arrival/departure predictions, occupancy, alerts
**Typical publishers**: transit agencies, mobility platforms, regional aggregators
**Protocols**: GTFS-RT Protobuf over HTTP, SIRI XML/JSON, REST
**Existing coverage**: generic GTFS bridge (multi-agency)
**White spots**: specific high-value agencies not yet configured; SIRI-native European systems

### Energy and Grid

**Entities**: generation units, bidding zones, interconnectors, balancing areas
**Measurements**: generation by fuel type, load, cross-border flows, day-ahead prices, imbalance
**Typical publishers**: TSOs, energy market operators, regulatory bodies
**Protocols**: REST (XML dominant for ENTSO-E), SOAP, CSV downloads
**Existing coverage**: ENTSO-E (pan-European — planned)
**White spots**: EIA (US), AEMO (Australia), IESO (Ontario), Elexon (UK), REE (Spain), RTE (France — éCO2mix), CAISO/ERCOT/PJM (US ISOs), Nordpool

### Social and News

**Entities**: posts, feeds, articles
**Measurements**: content, author, timestamp, engagement
**Typical publishers**: social networks, news organizations, blogs
**Protocols**: WebSocket (firehose), RSS/Atom, REST
**Existing coverage**: Bluesky (AT Protocol firehose), RSS/Atom (generic)
**White spots**: Mastodon/ActivityPub firehose, Reddit (pushshift alternatives), Hacker News (Firebase API)

### Air Quality and Environment

**Entities**: monitoring stations, sensors
**Measurements**: PM2.5, PM10, O3, NO2, SO2, CO, AQI
**Typical publishers**: environment agencies, city governments, EU/EEA
**Protocols**: REST, SOAP, CSV
**Existing coverage**: none
**White spots**: EEA (European), EPA AirNow (US), OpenAQ (global aggregator), AQICN, Defra (UK), UBA (Germany — Luftdaten)

### Astronomy and Space

**Entities**: satellites, solar events, NEOs, ISS
**Measurements**: TLE orbital elements, solar flare class, CME speed, NEO approach distance
**Typical publishers**: NASA, ESA, NOAA SWPC, CelesTrak
**Protocols**: REST (JSON, XML, TLE text), SSE
**Existing coverage**: NOAA GOES/SWPC (space weather)
**White spots**: NASA NEO API, CelesTrak TLE feeds, ESA Discos, NASA DONKI

### Earthquake Early Warning and Disaster Alerts

**Entities**: alert zones, warning bulletins, tsunami watches
**Measurements**: alert level, affected area, expected intensity, ETA
**Typical publishers**: USGS ShakeAlert, JMA EEW, PTWC, national emergency agencies
**Protocols**: CAP XML, REST, WebSocket, dedicated alert protocols
**Existing coverage**: none (USGS earthquakes are event catalogs, not EEW)
**White spots**: FEMA IPAWS, EU EFAS (flood alerts), Copernicus EMS, JMA tsunami/EEW

## Outputs

- A ranked candidate list with: name, URL, domain, region, protocol, auth, freshness estimate, volume estimate, and a one-paragraph feasibility note.
- For the top candidates, a concrete next step: either "ready for bootstrap" or "needs deeper probing of X."

## References

- [Search playbook](references/search-playbook.md)
