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
- **Search language** — for country-specific web research, build and run queries in the target country's primary administrative/search language first; use English only for supranational sources, standards material, or after local-language searches fail

## Procedure

1. **Scope the search** using the domain taxonomy and region.
2. **Generate search queries** in the primary language of each target country, following the strategy in [search playbook](references/search-playbook.md). Do not start country-specific discovery with English-only queries.
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

Use these as search anchors. Each domain lists the kinds of entities and measurements that are typical, plus the government or institutional bodies that tend to publish the data. Domains are grouped into tiers by current repo coverage.

---

### Tier 1 — Domains with Existing Bridges

These domains already have at least one bridge in the repo. Search within them to expand geographic or thematic coverage.

#### Hydrology and Water Monitoring

**Entities**: river gauges, reservoirs, groundwater wells, water quality stations
**Measurements**: water level, discharge/flow, temperature, conductivity, turbidity
**Typical publishers**: national hydrological services, environment agencies, water authorities
**Protocols**: REST polling (dominant), OData, WISKI/KIWIS
**Existing coverage**: Germany, Netherlands, France, Switzerland, Czech Republic, Poland, Norway, Sweden, Finland, UK, USA, Belgium
**White spots**: Spain (SAIH/CHE), Italy (ISPRA), Austria (eHYD), Portugal (SNIRH), Japan (MLIT water info), South Korea (WAMIS), Australia (BOM Water Data Online), Canada (ECCC Hydrometric), Brazil (ANA HidroWeb), India (CWC/WRIS), China (MWR), South Africa (DWS), Kenya, Nigeria, and most of Africa and Southeast Asia

#### Maritime / AIS Vessel Tracking

**Entities**: vessels (keyed by MMSI), aids to navigation
**Measurements**: position (lat/lon), speed, course, heading, destination, ship type
**Typical publishers**: national maritime authorities, coast guards, port authorities
**Protocols**: MQTT, WebSocket, raw TCP/NMEA, REST
**Existing coverage**: Norway (Kystverket), Finland/Baltic (Digitraffic), global terrestrial (AISstream — currently broken)
**White spots**: Denmark (DMA), USA (MarineCadastre — historical only; USCG NAIS — restricted), Canada (CCG), Baltic states individually, Mediterranean nations (Italy, Greece, Turkey), Asian maritime nations (Singapore MPA, Japan Coast Guard), Australia (AMSA)

#### Aviation / ADS-B

**Entities**: aircraft (keyed by ICAO hex address), flights
**Measurements**: position, altitude, speed, heading, squawk, callsign
**Typical publishers**: national aviation authorities, community networks (ADSBx, OpenSky), local receivers
**Protocols**: BEAST binary (TCP), SBS BaseStation, REST, WebSocket
**Existing coverage**: local Mode-S receiver bridge
**White spots**: OpenSky Network API (REST, free academic use), ADS-B Exchange (community, API), EUROCONTROL (B2B services — registration required), FAA SWIM (US — TBFM, STDDS feeds), Flightradar24 (commercial — skip)

#### Weather and Atmospheric

**Entities**: weather stations, radar grids, forecast zones, warning areas
**Measurements**: temperature, pressure, wind, precipitation, humidity, visibility, alerts/warnings
**Typical publishers**: national meteorological services (WMO members), space agencies
**Protocols**: REST, file-server polling (GRIB, CAP XML, GeoJSON), WebSocket, LDM/IDD
**Existing coverage**: Germany (DWD), USA (NOAA NWS, NOAA NDBC, NOAA GOES)
**White spots**: UK Met Office (DataPoint API), Météo-France (open data portal), SMHI (weather, not just hydro), KNMI (Data Platform), JMA (Japan — XML feeds), KMA (South Korea — open API), BOM (Australia — extensive), ECMWF (open data subset), Environment Canada (MSC Datamart — Geomet), MeteoSwiss, AEMET (Spain), IPMA (Portugal), DMI (Denmark — open data)

#### Seismology and Geophysics

**Entities**: earthquakes, seismic events, volcanoes
**Measurements**: magnitude, depth, location, felt reports, tsunami alerts
**Typical publishers**: geological surveys, seismological institutes
**Protocols**: REST (GeoJSON, QuakeML), WebSocket, Atom/RSS
**Existing coverage**: USGS (global)
**White spots**: EMSC (European-Mediterranean — real-time WebSocket available), GeoNet (New Zealand — GeoJSON API), Geoscience Australia, JMA (Japan seismic), INGV (Italy — FDSN), BGS (UK — felt reports), IRIS DMC (global seismic data)

#### Public Transit / GTFS

**Entities**: vehicles, trips, routes, stops, service alerts
**Measurements**: real-time position, arrival/departure predictions, occupancy, alerts
**Typical publishers**: transit agencies, mobility platforms, regional aggregators
**Protocols**: GTFS-RT Protobuf over HTTP, SIRI XML/JSON, REST
**Existing coverage**: generic GTFS bridge (multi-agency)
**White spots**: specific high-value agencies not yet configured; SIRI-native European systems (UK Bus Open Data, Samtrafiken/Trafiklab Sweden); MobilityData catalog lists 1,400+ RT feeds

#### Energy and Grid

**Entities**: generation units, bidding zones, interconnectors, balancing areas
**Measurements**: generation by fuel type, load, cross-border flows, day-ahead prices, imbalance
**Typical publishers**: TSOs, energy market operators, regulatory bodies
**Protocols**: REST (XML dominant for ENTSO-E), SOAP, CSV downloads
**Existing coverage**: ENTSO-E (pan-European — planned)
**White spots**: EIA (US — hourly grid monitor), AEMO (Australia — 5-min dispatch), IESO (Ontario), Elexon/BMRS (UK), REE (Spain — real-time demand), RTE éCO2mix (France), CAISO/ERCOT/PJM/MISO/SPP/NYISO (US ISOs — each has own API), Nordpool (day-ahead prices), Electricity Map (aggregator API)

#### Social and News

**Entities**: posts, feeds, articles, edits
**Measurements**: content, author, timestamp, engagement
**Typical publishers**: social networks, news organizations, blogs, wikis
**Protocols**: WebSocket (firehose), SSE, RSS/Atom, REST
**Existing coverage**: Bluesky (AT Protocol firehose), RSS/Atom (generic)
**White spots**: Mastodon/ActivityPub relay firehose, Wikimedia EventStreams (SSE — all Wikipedia/Wikidata edits, real-time, no auth, beautifully documented at stream.wikimedia.org), Hacker News Firebase API (real-time), OpenStreetMap minutely diffs (replication feed of all map edits worldwide)

---

### Tier 2 — Domains Identified but No Bridge Yet

These domains appeared in planning or assessment but have no runtime bridge in the repo.

#### Air Quality and Atmospheric Composition

**Entities**: monitoring stations, sensors, grid cells
**Measurements**: PM2.5, PM10, O3, NO2, SO2, CO, AQI, pollen counts
**Typical publishers**: environment agencies, city governments, EU/EEA, citizen sensor networks
**Protocols**: REST (JSON, CSV), SOAP
**Known sources**: OpenAQ (global aggregator — open API, no auth, 100+ countries), EEA (European — Up-to-Date Air Quality data, hourly), US EPA AirNow (REST, free key), Defra (UK — AURN network), UBA/Luftdaten (Germany), Sensor.Community/Luftdaten.info (crowdsourced — 15,000+ sensors, open API), PurpleAir (commercial API — limited free tier), AQICN (aggregator)
**Why it matters**: politically relevant, spatially dense, well-structured, many open APIs

#### Astronomy, Space Weather, and Orbital Mechanics

**Entities**: satellites, solar events, NEOs, ISS, TLE catalog objects, astronomical transients
**Measurements**: TLE orbital elements, solar flare class/flux, CME speed, NEO approach distance, transient coordinates/magnitude
**Typical publishers**: NASA, ESA, NOAA SWPC, CelesTrak, IAU
**Protocols**: REST (JSON, XML, TLE text), SSE, Kafka (ZTF)
**Known sources**: NOAA GOES/SWPC (existing bridge), NASA NEO API (free key), CelesTrak TLE feeds (no auth, text), NASA DONKI (space weather events), GCN/TAN (gamma-ray burst and gravitational wave alerts — VOEvent XML), ZTF transient alert stream (Kafka-native!)
**Why ZTF is notable**: The Zwicky Transient Facility publishes astronomical transient alerts natively through Apache Kafka. This is a rare case of an upstream source that already speaks our transport protocol. Schema is Avro.

#### Disaster Alerts and Early Warning

**Entities**: alert zones, warning bulletins, tsunami watches, flood forecasts
**Measurements**: alert level, affected area, expected intensity, ETA
**Typical publishers**: national emergency agencies, WMO, tsunami centers
**Protocols**: CAP XML, REST, WebSocket, dedicated alert protocols
**Known sources**: FEMA IPAWS (US — CAP), EU EFAS/EFAS (flood alerts), Copernicus EMS, JMA (Japan — tsunami and earthquake EEW), GDACS (Global Disaster Alert and Coordination System — RSS + API), Pacific Tsunami Warning Center, Meteoalarm (European weather warnings aggregator)

#### Road Traffic and Conditions

**Entities**: traffic sensors, road segments, incidents, roadworks, variable message signs
**Measurements**: flow, speed, occupancy, travel time, incident type, road surface condition
**Typical publishers**: national road administrations, city traffic management centers
**Protocols**: REST, DATEX II (XML), MQTT, OCIT-C
**Known sources**: Autobahn API (Germany — planned), Trafikverket (Sweden — open API, real-time), Statens vegvesen (Norway), Highways England (NTIS — DATEX II), Rijkswaterstaat NDW (Netherlands — DATEX II), FHWA (US — various state DOT feeds), HERE/TomTom (commercial — skip)

---

### Tier 3 — New Domains Not Previously Considered

These are entirely new domains. Many have mature, open, well-structured APIs that are ripe for bridge implementation.

#### Radiation Monitoring

**Entities**: gamma dose rate stations (keyed by station code or EURDEP ID)
**Measurements**: ambient gamma dose rate (nSv/h or µSv/h), sometimes nuclide-specific readings
**Typical publishers**: nuclear safety authorities, radiation protection agencies
**Protocols**: REST (JSON, XML), CSV, SOAP
**Known sources**: EURDEP (European Radiological Data Exchange Platform — aggregates 5,500+ stations across 39 countries, near-real-time, open data viewer + download), German BfS ODL network (REST API, ~1,800 stations, sub-hourly, no auth), Japan NRA monitoring (post-Fukushima network, JSON), Safecast (global citizen radiation network — open API, 200M+ measurements)
**Why it's strong**: structurally identical to hydrology (station-keyed numeric time series), politically significant, clean entity model, multiple open APIs

#### Wildfire and Thermal Anomaly Detection

**Entities**: fire detections / hotspots (keyed by satellite + pixel), active fire perimeters
**Measurements**: latitude, longitude, brightness temperature, fire radiative power (FRP), confidence, scan/track
**Typical publishers**: NASA, ESA, national forestry/fire services
**Protocols**: REST (JSON, CSV, GeoJSON, KML), WMS/WFS
**Known sources**: NASA FIRMS (Fire Information for Resource Management System — global, MODIS + VIIRS, updates every few hours per satellite pass, free API key), EFFIS (European Forest Fire Information System — Copernicus), CAL FIRE (California — incidents API), CWFIS (Canada — Canadian Wildland Fire Information System), Sentinel-3 SLSTR (ESA — active fire detection)
**Why it's strong**: global coverage, high public interest, each fire pixel has coordinates and timestamp, growing importance with climate change

#### Lightning Detection

**Entities**: lightning strokes/flashes (keyed by timestamp + coordinates)
**Measurements**: latitude, longitude, timestamp (microsecond precision), polarity, peak current (kA), stroke type (CG/IC)
**Typical publishers**: community networks, national met services, commercial networks
**Protocols**: WebSocket, REST, proprietary binary
**Known sources**: Blitzortung.org (global community network — real-time WebSocket feed, very high volume during storms, free for non-commercial), national met services sometimes publish aggregated strike data (DWD, Met Office, BOM)
**Why it's strong**: true real-time streaming (WebSocket), extremely high event rate during storms (thousands/minute), clean point-event model, dramatic visualization potential

#### Tidal and Sea Level Monitoring

**Entities**: tide gauges (keyed by station code — GLOSS, IOC, or national ID)
**Measurements**: water level, predicted tide, residual (surge), water temperature at some stations
**Typical publishers**: national hydrographic offices, oceanographic agencies, IOC/UNESCO
**Protocols**: REST (JSON, CSV, XML), ERDDAP, THREDDS
**Known sources**: IOC Sea Level Station Monitoring Facility (SLSMF — ~1,000 stations worldwide, near-real-time, open), UHSLC (University of Hawaii — fast-delivery tide gauge data), SHOM (France — Refmar), BODC (UK), BOM (Australia), JMA (Japan), NOAA CO-OPS (already covered for US)
**Why it's strong**: complements NOAA tides for the rest of the world, station-keyed, numerical, open, critical for tsunami and storm surge monitoring

#### Bikeshare and Micromobility (GBFS)

**Entities**: stations, docking points, free-floating vehicles (keyed by station_id or vehicle_id)
**Measurements**: available bikes, available docks, vehicle battery level, vehicle type, pricing
**Typical publishers**: bikeshare operators, city transportation departments
**Protocols**: GBFS (General Bikeshare Feed Specification) — REST JSON with auto-discovery
**Known sources**: hundreds of cities worldwide publish GBFS feeds; MobilityData maintains a catalog. Major systems include Citi Bike (NYC), Santander Cycles (London), Vélib' (Paris), Bay Wheels (SF), Capital Bikeshare (DC), nextbike (pan-European), Lime/TIER/Voi (e-scooters — some publish GBFS)
**Why it's strong**: standardized spec (like GTFS for transit), auto-discoverable, hundreds of deployments, clean entity model, no auth for most, natural sibling to the existing GTFS bridge

#### EV Charging Station Status

**Entities**: charging stations, connectors/ports (keyed by station ID + connector ID)
**Measurements**: availability status (available/occupied/faulted/unknown), connector type, power output (kW), pricing
**Typical publishers**: charging networks, national registries, aggregators
**Protocols**: OCPI (Open Charge Point Interface), REST, OCPP (backend)
**Known sources**: Open Charge Map (global aggregator — open API, 300,000+ locations), NOBIL (Norway — government registry, API), Bundesnetzagentur (Germany — Ladesäulenregister), nationale Databank Laadinfrastructuur (Netherlands — NDL), ChargePlace Scotland
**Why it's strong**: fast-growing domain, real-time status changes are event-driven by nature, clean entity model, several open APIs, politically relevant (EV transition)

#### Reservoir and Dam Storage

**Entities**: dams, reservoirs (keyed by dam/reservoir ID)
**Measurements**: storage volume (acre-feet or cubic meters), pool elevation, inflow, outflow, percent of capacity
**Typical publishers**: water resource agencies, power authorities
**Protocols**: REST, CSV
**Known sources**: US Bureau of Reclamation (Hydromet — REST, ~500 sites), California CDEC (real-time reservoir data), BOM Water Storage (Australia — daily), Spanish SAIH (basin authorities — real-time), India CWC reservoir bulletin
**Why it's strong**: complements river gauge hydrology, distinct entity model (reservoir vs. gauge), public interest during droughts, relatively small number of entities with high informational value

#### Water Quality (Continuous Monitoring)

**Entities**: water quality stations (keyed by station code, often co-located with hydro gauges)
**Measurements**: dissolved oxygen, pH, specific conductance, turbidity, chlorophyll-a, water temperature, nitrate
**Typical publishers**: environment agencies, water utilities, research institutions
**Protocols**: REST, WISKI/KIWIS, SOS (Sensor Observation Service)
**Known sources**: USGS NWIS (water quality parameters alongside flow — same API as USGS IV), EEA Waterbase, UK EA Water Quality Archive, Irish EPA hydronet, German state environment agencies (varies by Bundesland)
**Why it's strong**: structurally similar to hydrology (same stations, same polling model), adds a new measurement dimension, increasing regulatory importance (EU Water Framework Directive, US Clean Water Act)

#### Wikimedia and Knowledge Graph Edits

**Entities**: wiki pages, Wikidata items (keyed by page title or Q-ID)
**Measurements**: edit diffs, editor, timestamp, change size, edit type (human/bot), wiki project
**Typical publishers**: Wikimedia Foundation
**Protocols**: SSE (Server-Sent Events)
**Known sources**: Wikimedia EventStreams (stream.wikimedia.org — documented, no auth, real-time SSE, covers all Wikipedia languages + Wikidata + Commons + Wiktionary etc.)
**Why it's notable**: this is one of the most well-engineered public event streams on the internet. Proper SSE, JSON payloads, documented schema, multiple topic streams (recentchange, revision-create, page-create, page-delete, etc.). High volume (~50–200 edits/sec across all projects). Perfect protocol fit. Would be a new SSE bridge pattern for the repo.

#### OpenStreetMap Edits

**Entities**: changesets, nodes, ways, relations (keyed by element ID and changeset ID)
**Measurements**: geometry changes, tags, editor used, comment, bounding box
**Typical publishers**: OpenStreetMap Foundation
**Protocols**: XML replication diffs (minutely, available over HTTP)
**Known sources**: planet.openstreetmap.org replication (minutely diffs — sequence-numbered OsmChange XML), Overpass Augmented Diffs, OSMCha (changeset analysis API)
**Why it matters**: global collaborative map with ~10M contributors, minutely diff cadence is good for polling, each changeset has metadata and bounding box, useful for monitoring geographic edit activity

#### Noise Monitoring

**Entities**: noise monitoring stations, airports, construction sites (keyed by station ID)
**Measurements**: equivalent continuous sound level (LAeq), peak level (LAmax), percentile levels (L10, L90)
**Typical publishers**: city environmental departments, airport authorities
**Protocols**: REST, CSV
**Known sources**: Dublin City Noise Monitoring (open data), Barcelona noise monitoring, Heathrow/Schiphol airport noise (some publish APIs), EU Environmental Noise Directive data
**Why it's niche but interesting**: clean numeric time series, station-keyed, growing regulatory importance, unique domain that no other open data bridge project covers

#### Parking Availability

**Entities**: parking garages, lots, zones (keyed by facility ID)
**Measurements**: total spaces, available spaces, occupancy percentage, status (open/full/closed)
**Typical publishers**: city parking operators, smart city platforms
**Protocols**: REST, DATEX II, MQTT
**Known sources**: many European cities publish real-time parking data (Cologne, Munich, Zurich, Amsterdam, Ghent, etc.), UK NaPTAN/APDS, ParkAPI (German aggregator), Open.NRW parking data
**Why it's interesting**: high-frequency state changes, clean entity model, direct practical utility, DATEX II would be a new protocol pattern

#### Power Outages

**Entities**: outage areas, utility service territories (keyed by outage ID or utility + area)
**Measurements**: customers affected, outage cause, start time, estimated restoration, geographic extent
**Typical publishers**: electric utilities, aggregators
**Protocols**: REST (JSON, GeoJSON), web scraping (unfortunately common)
**Known sources**: PowerOutage.us (US aggregator — scrapes utility sites), UK Power Networks (documented API), individual utility outage maps (inconsistent, often scrape-only)
**Why it's tricky**: most utility outage data is published for human dashboards, not APIs. PowerOutage.us is an aggregator but may have terms issues. UK Power Networks is cleaner. This domain has high value but low API maturity.

#### Border Crossing and Wait Times

**Entities**: border crossing points, checkpoint lanes (keyed by port code)
**Measurements**: wait time (minutes), lane count, delay level, crossing type (pedestrian/vehicle/commercial)
**Typical publishers**: customs and border agencies
**Protocols**: REST (JSON, XML)
**Known sources**: US CBP Border Wait Times (REST API — all US land borders, updated frequently, no auth), Canada CBSA (less structured), EU border wait time projects (fragmented)
**Why it's interesting**: US CBP API is well-documented and free, clean entity model, practical utility, very niche domain nobody else bridges

#### Snow, Avalanche, and Mountain Conditions

**Entities**: snow measurement stations, avalanche zones, ski areas (keyed by station or zone ID)
**Measurements**: snow depth, snow water equivalent, avalanche danger level (1–5 European scale), wind, temperature
**Typical publishers**: avalanche warning services, mountain weather services, water supply agencies
**Protocols**: REST, XML, CSV
**Known sources**: SLF (Switzerland — avalanche bulletins and station data), AINEVA (Italy — regional avalanche services), BERA (France — Météo-France), Avalanche.org (US — aggregator), SNOTEL (US NRCS — 900+ automated snow stations, sub-hourly, REST), NVE snow/avalanche (Norway — possibly already adjacent to hydro bridge)
**Why it's strong**: SNOTEL in particular is a mature, high-quality, station-keyed network with REST API. Alpine avalanche services have structured danger level data. Clean fit for polling bridge.

#### Volcanic Activity

**Entities**: volcanoes (keyed by GVP number or VNUM), eruptions, ash advisories
**Measurements**: alert level, eruption type, ash cloud height/extent, SO2 flux, thermal anomaly
**Typical publishers**: volcano observatories, VAACs (Volcanic Ash Advisory Centers), GVP/Smithsonian
**Protocols**: REST, CAP XML, RSS, VONA (text)
**Known sources**: Smithsonian GVP (weekly activity reports — RSS), USGS/CVO Volcano Notification Service (email/RSS), VAAC advisories (9 centers worldwide — XML/graphic), MIROVA (satellite thermal monitoring — near-real-time), VolcanoDiscovery (aggregator)
**Why it matters**: low frequency but high consequence, global interest, the VONA message format is semi-structured, complements seismology nicely

#### Geomagnetic and Ionospheric

**Entities**: geomagnetic observatories (keyed by IAGA code), ionospheric measurement points
**Measurements**: magnetic field components (H, D, Z, F), Kp/Ap indices, TEC (total electron content), scintillation indices
**Typical publishers**: INTERMAGNET, WDC, NOAA SWPC, national geophysical institutes
**Protocols**: REST, IAGA-2002 format (text), CDF
**Known sources**: INTERMAGNET (real-time geomagnetic data from ~150 observatories worldwide, 1-second cadence, open data), GFZ Potsdam (Kp index — near-real-time), NOAA SWPC (partially covered), GNSS ionospheric data (various)
**Why it's interesting**: INTERMAGNET is a high-quality, global, real-time scientific network with 1-second data. The observatory codes are perfect Kafka keys. Volume is modest (150 stations × 1 Hz = manageable). Scientifically fascinating — captures geomagnetic storms, solar wind effects, aurora activity.

#### Amateur Radio Propagation

**Entities**: reception reports (keyed by transmitter callsign + receiver callsign + band)
**Measurements**: frequency, mode, SNR (signal-to-noise ratio), distance, transmitter/receiver gridsquare
**Protocols**: WebSocket, REST
**Known sources**: PSKReporter (real-time HF/VHF propagation reports — WebSocket, very high volume, essentially a global ionospheric sensor network), WSPRnet (Weak Signal Propagation Reporter — automated beacon network), DX cluster (real-time amateur radio contact spots)
**Why it's unique**: amateur radio propagation reports are, in effect, a real-time distributed sensor network for ionospheric conditions. PSKReporter processes millions of reports per day. The data reveals solar cycle effects, geomagnetic storm impacts, and atmospheric phenomena. No other bridge project covers this domain.

#### Coral Reef and Marine Biology

**Entities**: reef sites, monitoring buoys, satellite grid cells (keyed by site/station ID or lat/lon grid)
**Measurements**: sea surface temperature anomaly, bleaching alert level, degree heating weeks, chlorophyll-a
**Typical publishers**: NOAA Coral Reef Watch, GBRMPA (Great Barrier Reef), reef monitoring networks
**Protocols**: REST, NetCDF, GeoTIFF, CSV
**Known sources**: NOAA Coral Reef Watch (global 5km satellite products — daily, REST/ERDDAP, open), AIMS (Australian Institute of Marine Science — reef monitoring data), GCRMN
**Why it matters**: climate indicator, global coverage from satellite, clean grid-based model, daily update cadence is on the slow side but scientifically significant

#### Citizen Science Sensor Networks

**Entities**: sensors/stations (keyed by sensor ID, typically crowdsourced)
**Measurements**: varies — PM2.5, temperature, humidity, radiation, noise, soil moisture
**Typical publishers**: community platforms, NGOs, maker communities
**Protocols**: REST (JSON)
**Known sources**: Sensor.Community (formerly Luftdaten.info — ~15,000 active sensors, open API, global, air quality + weather + noise), PurpleAir (PM2.5 — 30,000+ sensors, API available), Safecast (radiation — 200M+ datapoints, open API), Weather Underground PWS (personal weather stations — API available but commercial terms), CWOP/MADIS (citizen weather)
**Why it matters**: dramatically better spatial resolution than official networks, especially in developing countries. Sensor.Community is the standout — open API, global, structured JSON, active development.

---

### Tier 4 — Horizon Domains

These are emerging, speculative, or restricted-access domains worth monitoring but not yet ready for bridge implementation.

#### Drone / UAS Traffic (Remote ID)
Emerging standard — FAA Remote ID broadcasts, EASA U-Space. Currently fragmented, few open aggregators. Watch for standardization.

#### Wastewater Epidemiology
Post-COVID wastewater monitoring for pathogen surveillance. Some cities publish dashboards, but few have APIs. Growing fast — could mature into a bridgeable domain within 1–2 years.

#### Satellite Conjunction and Space Debris
Space-Track.org (free account required) and LeoLabs publish conjunction warnings. CelesTrak has open TLE data. ESA's Space Debris Office publishes risk assessments. Niche but growing with the Starlink/megaconstellation era.

#### Agricultural Crop Monitoring
USDA CropScape, EU MARS crop bulletins, FAO GIEWS. Mostly weekly-to-monthly cadence — too slow for real-time bridging. But SMAP soil moisture and NDVI vegetation indices from satellites are getting closer to daily updates.

#### Undersea Cable and Internet Routing
RIPE RIS (Routing Information Service) and RouteViews publish real-time BGP route announcements. These are legitimate real-time streams, but the data is complex (BGP UPDATE messages) and the audience is narrow. IODA (Internet Outage Detection and Analysis) aggregates this into a more consumable form.

#### Whale and Marine Mammal Acoustic Detection
NOAA and academic networks operate hydrophone arrays that detect whale calls. Some data reaches near-real-time through platforms like Whale Alert. Very niche, limited API availability, but scientifically compelling.

#### Nuclear Plant Operational Status
US NRC publishes daily plant status reports. IAEA PRIS has a global reactor database. But update cadence is daily at best — borderline for real-time bridging. More of a reference data enrichment source.

## Outputs

- A ranked candidate list with: name, URL, domain, region, protocol, auth, freshness estimate, volume estimate, and a one-paragraph feasibility note.
- For the top candidates, a concrete next step: either "ready for bootstrap" or "needs deeper probing of X."

## References

- [Search playbook](references/search-playbook.md)
