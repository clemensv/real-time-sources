[![Build Containers](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg)](https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml)
[![Bluesky Firehose Tests](https://github.com/clemensv/real-time-sources/actions/workflows/test-bluesky.yml/badge.svg)](https://github.com/clemensv/real-time-sources/actions/workflows/test-bluesky.yml)
[![GTFS Bridge Tests](https://github.com/clemensv/real-time-sources/actions/workflows/test-gtfs.yml/badge.svg)](https://github.com/clemensv/real-time-sources/actions/workflows/test-gtfs.yml)
[![NOAA Producer Tests](https://github.com/clemensv/real-time-sources/actions/workflows/test-noaa.yml/badge.svg)](https://github.com/clemensv/real-time-sources/actions/workflows/test-noaa.yml)
[![PegelOnline Producer Tests](https://github.com/clemensv/real-time-sources/actions/workflows/test-pegelonline.yml/badge.svg)](https://github.com/clemensv/real-time-sources/actions/workflows/test-pegelonline.yml)
[![RSS Bridge Tests](https://github.com/clemensv/real-time-sources/actions/workflows/test-rss.yml/badge.svg)](https://github.com/clemensv/real-time-sources/actions/workflows/test-rss.yml)
[![USGS-IV Producer Tests](https://github.com/clemensv/real-time-sources/actions/workflows/test-usgs-iv.yml/badge.svg)](https://github.com/clemensv/real-time-sources/actions/workflows/test-usgs-iv.yml)

# Real Time Sources for Apache Kafka, Azure Event Hubs, and Fabric Event Streams

Learning how to build event streaming solutions with Microsoft Azure Event Hubs,
Microsoft Fabric Event Streams, and any Apache Kafka compatible server and
service is more interesting when you have real time data sources to work with.

This repo contains command line tools, written in Python, that can be used to
retrieve real-time streaming data and related reference data from various APIs,
and then routing the data to Apache Kafka compatible endpoints.

For each tool, there is a corresponding, pre-built (Docker-) container image
that you can pull and use instantly from this repo's container registry. There
are also pre-built templates for easily deploying the containers as an Azure
Container Instance (ACI), either feeding data into an Azure Event Hub or an
Fabric Event Stream custom endpoint. The container images will work with any
Apache Kafka compatible server or service, as long as you provide required
information. The supported authentication scheme for the Kafka endpoint is
`SASL/PLAIN`.

The sources are organized by domain below. Each entry links to the container
documentation, and the README in each project directory has full details.

### Hydrology and Water Monitoring

| Source | Coverage | Link |
|---|---|---|
| BAFU Hydro | Switzerland (~300 stations, FOEN) | [README](bafu-hydro/README.md) |
| CHMI Hydro | Czech Republic (CHMU) | [Container](chmi-hydro/CONTAINER.md) |
| German Waters | Germany (12 state portals, ~2,724 stations) | [README](german-waters/README.md) |
| Hub'Eau Hydrometrie | France (~6,300 stations) | [Container](hubeau-hydrometrie/CONTAINER.md) |
| IMGW Hydro | Poland (IMGW-PIB) | [Container](imgw-hydro/CONTAINER.md) |
| NOAA Tides and Currents | United States (~3,000 stations) | [Container](noaa/CONTAINER.md) |
| NOAA NDBC | United States (buoy observations) | [Container](noaa-ndbc/CONTAINER.md) |
| NVE Hydro | Norway (NVE) | [README](nve-hydro/README.md) |
| Pegelonline | Germany (federal waterways, ~3,000 stations) | [Container](pegelonline/CONTAINER.md) |
| RWS Waterwebservices | Netherlands (~785 stations) | [Container](rws-waterwebservices/CONTAINER.md) |
| SMHI Hydro | Sweden (SMHI) | [Container](smhi-hydro/CONTAINER.md) |
| SYKE Hydro | Finland (SYKE) | [README](syke-hydro/README.md) |
| UK EA Flood Monitoring | England (~4,000 stations) | [Container](uk-ea-flood-monitoring/CONTAINER.md) |
| USGS Instantaneous Values | United States (~1.5M stations) | [Container](usgs-iv/CONTAINER.md) |
| Waterinfo VMM | Belgium / Flanders (~1,785 stations) | [Container](waterinfo-vmm/CONTAINER.md) |

### Weather and Meteorology

| Source | Coverage | Link |
|---|---|---|
| BOM Australia | Australia (~8 capital city airports, half-hourly obs) | [Container](bom-australia/CONTAINER.md) |
| DWD | Germany (~1,450 stations, observations and CAP alerts) | [Container](dwd/CONTAINER.md) |
| Environment Canada | Canada (~963 SWOB stations, hourly obs) | [Container](environment-canada/CONTAINER.md) |
| HKO Hong Kong | Hong Kong (27 temp stations, 18 rainfall districts) | [Container](hko-hong-kong/CONTAINER.md) |
| Meteoalarm | Europe (37 countries, severe weather warnings) | [Container](meteoalarm/CONTAINER.md) |
| NOAA NWS | United States (weather alerts, CAP) | [Container](noaa-nws/CONTAINER.md) |
| NWS CAP Alerts | United States (active alerts via api.weather.gov) | [Container](nws-alerts/CONTAINER.md) |
| NOAA GOES / SWPC | Global (space weather, solar wind, K-index) | [Container](noaa-goes/CONTAINER.md) |
| Singapore NEA | Singapore (62 stations, temp/rainfall/wind/forecast) | [Container](singapore-nea/CONTAINER.md) |
| SMHI Weather | Sweden (~232 stations, hourly obs) | [Container](smhi-weather/CONTAINER.md) |

### Disaster Alerts and Civil Protection

| Source | Coverage | Link |
|---|---|---|
| GDACS | Global (earthquakes, floods, cyclones, volcanoes, droughts) | [Container](gdacs/CONTAINER.md) |
| NINA/BBK | Germany (MOWAS, KATWARN, BIWAPP, DWD, LHP, Police) | [Container](nina-bbk/CONTAINER.md) |
| PTWC Tsunami | Pacific and Atlantic (NOAA tsunami bulletins) | [Container](ptwc-tsunami/CONTAINER.md) |
| USGS Earthquakes | Global (seismic events) | [Container](usgs-earthquakes/CONTAINER.md) |

### Radiation Monitoring

| Source | Coverage | Link |
|---|---|---|
| BfS ODL | Germany (~1,700 stations, hourly gamma dose rate) | [Container](bfs-odl/CONTAINER.md) |

### Maritime and Vessel Tracking

| Source | Coverage | Link |
|---|---|---|
| AISStream | Global (AIS via WebSocket, ~200 km from shore) | [Container](aisstream/CONTAINER.md) |
| Digitraffic Maritime | Finland / Baltic Sea (AIS via MQTT) | [Container](digitraffic-maritime/CONTAINER.md) |
| Kystverket AIS | Norway / Svalbard (raw TCP AIS, ~34 msg/s) | [Container](kystverket-ais/CONTAINER.md) |

### Aviation

| Source | Coverage | Link |
|---|---|---|
| Mode-S | Local (ADS-B via dump1090 receivers) | [Container](mode-s/CONTAINER.md) |

### Road Transport

| Source | Coverage | Link |
|---|---|---|
| Autobahn | Germany (roadworks, warnings, closures, webcams) | [Container](autobahn/CONTAINER.md) |
| Digitraffic Road | Finland (TMS sensors, road weather, traffic messages) | [Container](digitraffic-road/CONTAINER.md) |
| GTFS Realtime | Global (1,000+ transit agencies, vehicles, trips, alerts) | [Container](gtfs/CONTAINER.md) |
| Nextbus | North America (public transit arrivals) | [README](nextbus/README.md) |
| WSDOT | Washington State (~1,000 traffic flow sensors, LOS readings) | [Container](wsdot/CONTAINER.md) |

### Railway

| Source | Coverage | Link |
|---|---|---|
| iRail | Belgium (~600 NMBS/SNCB stations, departures, delays) | [Container](irail/CONTAINER.md) |

### Energy and Infrastructure

| Source | Coverage | Link |
|---|---|---|
| ENTSO-E | Europe (electricity generation, prices, load, flows) | [Container](entsoe/CONTAINER.md) |
| NDL Netherlands | Netherlands (EV charging stations, EVSE status, tariffs) | [Container](ndl-netherlands/CONTAINER.md) |

### Social Media and News

| Source | Coverage | Link |
|---|---|---|
| Bluesky Firehose | Global (posts, likes, reposts, follows) | [Container](bluesky/CONTAINER.md) |
| RSS Feeds | Any (configurable RSS/Atom feed URLs or OPML files) | [Container](rss/CONTAINER.md) |
| Wikimedia EventStreams | Global (Wikipedia, Wikidata, Commons recent changes) | [Container](wikimedia-eventstreams/CONTAINER.md) |

## Code Generation

Projects with checked-in `xreg` manifests regenerate their producer clients with
`xrcg generate`. Use `xrcg` `0.10.1`; the checked-in producer output and the
key-aware Kafka producer behavior now relied on by the repo are generated with
that version. Each project's `generate_producer.ps1` script uses the checked-in
manifest as the source of truth, validates the `xrcg` version up front, and
refreshes the generated client package from that definition.

## Command Line Tools

Detailed descriptions of each data source, its API, update frequency, and
configuration options are in the per-project README files linked in the tables
above.

### Hydrology and Water Monitoring

**[BAFU Hydro](bafu-hydro/README.md)** -- Swiss Federal Office for the
Environment (BAFU/FOEN) hydrological monitoring network. Forwards water level,
discharge, and temperature observations from approximately 300 stations.

**[CHMI Hydro](chmi-hydro/README.md)** -- Czech Hydrometeorological Institute.
Real-time water level, discharge, and temperature. Polled every 10 minutes.

**[German Waters](german-waters/README.md)** -- Aggregates water level and
discharge data from 12 German state open data portals (~2,724 stations). Polled
every 15 minutes.

**[Hub'Eau Hydrometrie](hubeau-hydrometrie/README.md)** -- French Hub'Eau
Hydrométrie API, covering ~6,300 stations across France.

**[IMGW Hydro](imgw-hydro/README.md)** -- Polish Institute of Meteorology and
Water Management (IMGW-PIB). Polled every 10 minutes.

**[NOAA Tides and Currents](noaa/README.md)** -- NOAA NOS water level and
current data for over 3,000 US stations. Updated every 6 minutes.

**[NOAA NDBC](noaa-ndbc/README.md)** -- National Data Buoy Center buoy
observations across the United States. Polled every 5 minutes.

**[NVE Hydro](nve-hydro/README.md)** -- Norwegian Water Resources and Energy
Directorate (NVE). Water level and discharge observations. Requires a free API
key.

**[Pegelonline](pegelonline/README.md)** -- German Federal Waterways and
Shipping Administration (WSV). Over 3,000 stations, updated every 15 minutes.

**[RWS Waterwebservices](rws-waterwebservices/README.md)** -- Dutch
Rijkswaterstaat water level data from ~785 stations. Polled every 10 minutes.

**[SMHI Hydro](smhi-hydro/README.md)** -- Swedish Meteorological and
Hydrological Institute (SMHI). Discharge data for hundreds of stations. Polled
every 15 minutes.

**[SYKE Hydro](syke-hydro/README.md)** -- Finnish Environment Institute (SYKE).
Water level and discharge observations.

**[UK EA Flood Monitoring](uk-ea-flood-monitoring/README.md)** -- UK Environment
Agency. ~4,000 stations across England. Polled every 15 minutes.

**[USGS Instantaneous Values](usgs-iv/README.md)** -- USGS water quality and
quantity data for over 1.5 million US stations. Updated every 15 minutes.

**[Waterinfo VMM](waterinfo-vmm/README.md)** -- Belgian Waterinfo.be KIWIS API,
~1,785 stations across Flanders. Polled every 15 minutes.

### Weather and Meteorology

**[BOM Australia](bom-australia/README.md)** -- Australian Bureau of Meteorology.
Half-hourly weather observations from capital city airports: temperature, wind,
pressure, humidity, rainfall, cloud cover, visibility.

**[DWD](dwd/README.md)** -- German Weather Service. ~1,450 stations with
10-minute observations (temperature, precipitation, wind) plus CAP weather
alerts.

**[Environment Canada](environment-canada/README.md)** -- Environment and
Climate Change Canada (ECCC). ~963 SWOB stations via OGC API with hourly
temperature, humidity, dew point, pressure, wind, and precipitation.

**[HKO Hong Kong](hko-hong-kong/README.md)** -- Hong Kong Observatory. 27
temperature stations, 18 rainfall districts, humidity, and UV index. Updated
hourly.

**[Meteoalarm](meteoalarm/README.md)** -- EUMETNET Meteoalarm. Severe weather
warnings aggregated from 37 European national meteorological services.

**[NOAA NWS](noaa-nws/README.md)** -- National Weather Service active weather
alerts across the United States. Polled every 60 seconds.

**[NWS CAP Alerts](nws-alerts/README.md)** -- US National Weather Service
active alerts via the api.weather.gov GeoJSON endpoint with SAME/UGC geocodes
and VTEC codes.

**[NOAA GOES / SWPC](noaa-goes/README.md)** -- NOAA Space Weather Prediction
Center. Space weather alerts, planetary K-index, and solar wind data. Polled
every 60 seconds.

**[Singapore NEA](singapore-nea/README.md)** -- National Environment Agency of
Singapore. 62 weather stations with temperature, rainfall, wind speed, wind
direction, and 2-hour area forecasts.

**[SMHI Weather](smhi-weather/README.md)** -- Swedish Meteorological and
Hydrological Institute (SMHI). ~232 stations with hourly temperature, wind gust,
dew point, pressure, humidity, and precipitation.

### Disaster Alerts and Civil Protection

**[GDACS](gdacs/README.md)** -- Global Disaster Alert and Coordination System.
Earthquake, tropical cyclone, flood, volcano, flash flood, and drought alerts
from the GDACS RSS feed.

**[NINA/BBK](nina-bbk/README.md)** -- German Federal Office of Civil Protection
(BBK) NINA warning system. Aggregates warnings from six providers: MOWAS
(federal), KATWARN, BIWAPP, DWD, LHP (flood centers), and Police.

**[PTWC Tsunami](ptwc-tsunami/README.md)** -- NOAA National Tsunami Warning
Center (NTWC) and Pacific Tsunami Warning Center (PTWC). Tsunami bulletins from
two Atom XML feeds covering the Pacific, Atlantic, and Caribbean.

**[USGS Earthquakes](usgs-earthquakes/README.md)** -- Real-time earthquake
events from the USGS GeoJSON feeds with deduplication. Polled every 60 seconds.

### Radiation Monitoring

**[BfS ODL](bfs-odl/README.md)** -- German Federal Office for Radiation
Protection (BfS) ODL ambient gamma dose rate monitoring network. Approximately
1,700 stationary probes measuring hourly averaged gamma dose rates in µSv/h,
with cosmic and terrestrial decomposition. Open WFS data interface, no auth.
Polled hourly.

### Maritime and Vessel Tracking

**[AISStream](aisstream/README.md)** -- AISStream.io WebSocket API. Real-time
AIS vessel tracking from ships worldwide (~200 km from shore). Publishes 23 AIS
message types. Requires API key. The free service can be unreliable.

**[Digitraffic Maritime](digitraffic-maritime/README.md)** -- Finland's
Digitraffic Marine MQTT stream. AIS vessel positions and metadata from the
Finnish coastal zone and Baltic Sea. ~35 messages/second. Open data (CC 4.0 BY).

**[Kystverket AIS](kystverket-ais/README.md)** -- Norwegian Coastal
Administration raw TCP AIS stream. NMEA sentences from 50+ stations covering the
Norwegian economic zone, Svalbard, and Jan Mayen. ~34 messages/second (~2.9M/day).

### Aviation

**[Mode-S](mode-s/README.md)** -- ADS-B aircraft position and telemetry data
from dump1090 receivers. Polled every 60 seconds.

### Road Transport

**[Autobahn](autobahn/README.md)** -- German Autobahn API. Roadworks, warnings,
closures, parking areas, charging stations, and webcams. Uses ETags and local
state to detect changes.

**[Digitraffic Road](digitraffic-road/README.md)** -- Finland's Digitraffic Road
MQTT stream. TMS sensor readings (vehicle counts and speeds from 500+ stations),
road weather measurements (350+ stations), traffic messages, and maintenance
vehicle tracking. Open data (CC 4.0 BY).

**[GTFS Realtime](gtfs/README.md)** -- GTFS and GTFS-RT data from 1,000+ public
transport agencies worldwide. Vehicle positions, trip updates, and alerts. MTA
feeds alone produce over 50 GB/day.

**[Nextbus](nextbus/README.md)** -- Public transit arrivals from the Nextbus
service.

**[WSDOT](wsdot/README.md)** -- Washington State DOT traffic flow data from
approximately 1,000 inductive loop sensors across five regions. Level of Service
readings updated every 90 seconds. Requires a free API access code.

### Railway

**[iRail](irail/README.md)** -- Belgian railway real-time data from the iRail
API. Station metadata and departure boards for approximately 600 NMBS/SNCB
stations, including delays, platform assignments, cancellations, and occupancy.
No authentication. Rate-limited to 3 requests/second; full cycle ~3–4 minutes.

### Energy and Infrastructure

**[ENTSO-E](entsoe/README.md)** -- European electricity market data from the
ENTSO-E Transparency Platform. Generation output, day-ahead prices, load,
forecasts, installed capacity, reservoir filling, and cross-border flows.

**[NDL Netherlands](ndl-netherlands/README.md)** -- Dutch Nationale Databank
Laadinfrastructuur. EV charging station locations, EVSE connector status changes,
and tariff data via OCPI.

### Social Media and News

**[Bluesky Firehose](bluesky/README.md)** -- Bluesky AT Protocol firehose.
Posts, likes, reposts, follows, blocks, and profile updates. Supports selective
filtering and cursor management for resumable streaming.

**[RSS Feeds](rss/README.md)** -- Configurable RSS/Atom feed poller. Supports
feed URLs or OPML files. Only forwards new items.

**[Wikimedia EventStreams](wikimedia-eventstreams/README.md)** -- Wikimedia's
public recentchange stream for edits, page creations, and log actions across
Wikipedia, Wikidata, Commons, and sister projects.

### External

**[Forza Motorsport PC](https://github.com/clemensv/forza-telemetry-bridge)** --
Racing game telemetry bridge (separate repository). Captures UDP telemetry from
Forza Motorsport games and forwards to Event Hubs or Fabric Event Streams.
Binary release available.
