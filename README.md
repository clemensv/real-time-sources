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

The container image documentation provides detailed information:

* [AISStream - Global AIS vessel tracking](aisstream/CONTAINER.md)
* [Autobahn - German motorway traffic events](autobahn/CONTAINER.md)
* [Bluesky Firehose - Social media posts and interactions](bluesky/CONTAINER.md)
* [CHMI Hydro - Czech hydrological observations](chmi-hydro/CONTAINER.md)
* [Digitraffic Maritime - Finnish AIS vessel tracking](digitraffic-maritime/CONTAINER.md)
* [Digitraffic Road - Finnish road traffic data (sensors, messages, maintenance)](digitraffic-road/CONTAINER.md)
* [DWD - German weather observations and alerts](dwd/CONTAINER.md)
* [ENTSO-E - European electricity market data](entsoe/CONTAINER.md)
* [German Waters - German state water level observations](german-waters/README.md)
* [GTFS Realtime - Public transport data](gtfs/CONTAINER.md)
* [Hub'Eau Hydrometrie - French hydrometric observations](hubeau-hydrometrie/CONTAINER.md)
* [IMGW Hydro - Polish hydrological observations](imgw-hydro/CONTAINER.md)
* [Kystverket AIS - Norwegian AIS vessel tracking](kystverket-ais/CONTAINER.md)
* [Mode-S - ADS-B and Mode-S aircraft telemetry](mode-s/CONTAINER.md)
* [NOAA Tides and Currents - Water level and current data](noaa/CONTAINER.md)
* [NOAA GOES and SWPC - Space weather and alert feeds](noaa-goes/CONTAINER.md)
* [NOAA NDBC - Buoy observations](noaa-ndbc/CONTAINER.md)
* [NOAA NWS - Weather alerts](noaa-nws/CONTAINER.md)
* [Pegelonline - Water level and current data](pegelonline/CONTAINER.md)
* [RSS Feeds - News and blog posts](rss/CONTAINER.md)
* [RWS Waterwebservices - Dutch water observations](rws-waterwebservices/CONTAINER.md)
* [SMHI Hydro - Swedish hydrological observations](smhi-hydro/CONTAINER.md)
* [UK EA Flood Monitoring - English flood and river data](uk-ea-flood-monitoring/CONTAINER.md)
* [USGS Earthquakes - Seismic event feeds](usgs-earthquakes/CONTAINER.md)
* [USGS Instantaneous Values - Water quality and quantity data](usgs-iv/CONTAINER.md)
* [Waterinfo VMM - Flemish water observations](waterinfo-vmm/CONTAINER.md)

Details about the tools and the data sources are provided in the respective
README files.

## Code Generation

Projects with checked-in `xreg` manifests regenerate their producer clients with
`xrcg generate`. Use `xrcg` `0.10.1`; the checked-in producer output and the
key-aware Kafka producer behavior now relied on by the repo are generated with
that version. Each project's `generate_producer.ps1` script uses the checked-in
manifest as the source of truth, validates the `xrcg` version up front, and
refreshes the generated client package from that definition.

## Command Line Tools

### AISStream - Global AIS vessel tracking

The [AISStream bridge](aisstream/README.md) connects to the AISStream.io
WebSocket API and streams real-time AIS vessel tracking data from ships
worldwide. Coverage extends approximately 200 km from shore. The bridge
publishes 23 AIS message types as CloudEvents to Kafka. Note that the free
AISStream service can be unreliable and may have frequent outages.

### Autobahn - German motorway traffic events

The [Autobahn bridge](autobahn/README.md) polls the German Autobahn API for
current roadworks, warnings, closures, parking areas, charging stations, and
webcams and emits change events as CloudEvents to Kafka. The bridge uses ETags
and local state to detect appeared, updated, and resolved items across the
network.

### Bluesky Firehose - Social media posts and interactions

The [Bluesky Firehose tool](bluesky/README.md) is a command line tool that
connects to the Bluesky AT Protocol firehose and streams real-time events
from the Bluesky social network. The tool captures posts, likes, reposts,
follows, blocks, and profile updates, formatting them as CloudEvents for
standardized event processing. The data can be sent to Kafka topics,
Azure Event Hubs, or Microsoft Fabric Event Streams. The tool supports
selective filtering, cursor management for resuming after restarts, and
is optimized for high-throughput event processing.

### CHMI Hydro - Czech hydrological observations

The [CHMI Hydro bridge](chmi-hydro/README.md) fetches real-time water level,
discharge, and temperature data from the Czech Hydrometeorological Institute
(ČHMÚ) and publishes the observations to Kafka as CloudEvents. The data is
polled every 10 minutes by default.

### Digitraffic Maritime - Finnish AIS vessel tracking

The [Digitraffic Maritime bridge](digitraffic-maritime/README.md) connects to
Finland's Digitraffic Marine MQTT stream and forwards real-time AIS vessel
positions and metadata from the Finnish coastal zone and Baltic Sea. The data is
open (CC 4.0 BY), requires no API key, and produces approximately 35 messages
per second.

### Digitraffic Road - Finnish road traffic data

The [Digitraffic Road bridge](digitraffic-road/README.md) connects to Finland's
Digitraffic Road MQTT stream and forwards real-time data from the Finnish national
road network: TMS sensor readings (vehicle counts and speeds from 500+ stations),
road weather measurements (temperature, wind, humidity from 350+ stations),
traffic messages (incidents, road works, weight restrictions, exempted transports),
and maintenance vehicle tracking. Events are emitted to three Kafka topics with
distinct key models. The data is open (CC 4.0 BY) and requires no API key.

### DWD - German weather observations and alerts

The [DWD bridge](dwd/README.md) fetches real-time weather observations and
alerts from the German Weather Service (Deutscher Wetterdienst). It covers
approximately 1,450 stations reporting 10-minute observations for temperature,
precipitation, wind, and other parameters, plus CAP weather alerts. The data is
published to Kafka as CloudEvents.

### ENTSO-E - European electricity market data

The [ENTSO-E bridge](entsoe/README.md) retrieves European electricity market
data from the ENTSO-E Transparency Platform, including generation output,
day-ahead prices, load data, forecasts, installed capacity, reservoir filling,
and cross-border flows across multiple European bidding zones. The data is
published to Kafka as CloudEvents.

### German Waters - German state water level observations

The [German Waters bridge](german-waters/README.md) aggregates real-time water
level and discharge data from 12 German state open data portals, covering
approximately 2,724 monitoring stations, and publishes the observations to Kafka
as CloudEvents. The data is polled every 15 minutes by default.

### GTFS Realtime - Public transport data

The [GTFS Realtime Bridge](gtfs/README.md) is a command line tool that retrieves
schedules, real-time vehicle positions, real-time trip updates (live
predictions of arrivals/departures), and alerts from practically any GTFS and
GTFS-RT service. Over 1000 public transport agencies worldwide publish their
data in GTFS format, and many of them also provide real-time data in GTFS-RT
format.

In terms of sheer data volume, the feeds related to the New York City
Metropolitan Transportation Authority (MTA) will produce over 50 Gigabytes of
data each day.

### Hub'Eau Hydrometrie - French hydrometric observations

The [Hub'Eau Hydrometrie bridge](hubeau-hydrometrie/README.md) retrieves
real-time water level and flow data from the French Hub'Eau Hydrométrie API,
covering approximately 6,300 monitoring stations across France, and publishes
the observations to Kafka as CloudEvents.

### IMGW Hydro - Polish hydrological observations

The [IMGW Hydro bridge](imgw-hydro/README.md) fetches real-time hydrological
data from the Polish Institute of Meteorology and Water Management (IMGW-PIB)
and forwards the observations to Kafka as CloudEvents. The data is polled every
10 minutes by default.

### Kystverket AIS - Norwegian AIS vessel tracking

The [Kystverket AIS bridge](kystverket-ais/README.md) connects to the Norwegian
Coastal Administration's raw TCP AIS stream and decodes NMEA AIS sentences from
50+ terrestrial and offshore stations covering the Norwegian economic zone,
Svalbard, and Jan Mayen. The stream produces approximately 34 messages per
second (~2.9 million per day) and publishes them to Kafka as CloudEvents.

### Mode-S - ADS-B and Mode-S aircraft telemetry

The [Mode-S data poller](mode-s/README.md) retrieves real-time ADS-B aircraft
position and telemetry data from dump1090 receivers and publishes the data to
Kafka as CloudEvents. The data is polled every 60 seconds by default.

### NOAA Tides and Currents - Water level and current data

The [NOAA data poller](noaa/README.md) is a command line tool that can be used
to retrieve real-time water level and current data from NOAA's National Ocean
Service (NOS) Tides and Currents API. The data is available for over 3000
stations in the United States and its territories. The NOAA data is updated
every 6 minutes, and the data volume is relatively low.

### NOAA GOES and SWPC - Space weather and alert feeds

The [NOAA GOES/SWPC poller](noaa-goes/README.md) polls the NOAA Space Weather
Prediction Center for space weather alerts, planetary K-index, and solar wind
data, publishing the observations to Kafka as CloudEvents. The data is polled
every 60 seconds by default.

### NOAA NDBC - Buoy observations

The [NOAA NDBC poller](noaa-ndbc/README.md) polls the National Data Buoy Center
for the latest buoy observations across the United States and publishes the data
to Kafka as CloudEvents. The data is polled every 5 minutes by default.

### NOAA NWS - Weather alerts

The [NOAA NWS poller](noaa-nws/README.md) polls the National Weather Service for
active weather alerts across the United States and publishes them to Kafka as
CloudEvents. The data is polled every 60 seconds by default.

### RSS Feeds - News and blog posts

The [RSS feed poller](rss/README.md) is a command line tool that can be used to
retrieve real-time news and blog posts from any RSS feed. The tool can be
configured with a list of RSS feed URLs or OPML files, and it will poll the
feeds at a configurable interval. The RSS client will only forward new items
from the feeds.

### Pegelonline - Water level and current data

The [Pegelonline data poller](pegelonline/README.md) is a command line tool that
can be used to retrieve real-time water level and current data from the German
Federal Waterways and Shipping Administration (WSV) Pegelonline API. The data is
available for over 3000 stations in Germany. The Pegelonline data is updated
every 15 minutes, and the data volume is relatively low.

### RWS Waterwebservices - Dutch water observations

The [RWS Waterwebservices bridge](rws-waterwebservices/README.md) retrieves
water level data from the Dutch Rijkswaterstaat Waterwebservices API, covering
approximately 785 water monitoring stations, and publishes the observations to
Kafka as CloudEvents. The data is polled every 10 minutes by default.

### SMHI Hydro - Swedish hydrological observations

The [SMHI Hydro bridge](smhi-hydro/README.md) fetches real-time discharge data
from the Swedish Meteorological and Hydrological Institute (SMHI) for hundreds
of monitoring stations and publishes the observations to Kafka as CloudEvents.
The data is polled every 15 minutes by default.

### UK EA Flood Monitoring - English flood and river data

The [UK EA Flood Monitoring bridge](uk-ea-flood-monitoring/README.md) retrieves
real-time water level and flow data from the UK Environment Agency Flood
Monitoring API, covering approximately 4,000 stations across England, and
publishes the observations to Kafka as CloudEvents. The data is polled every
15 minutes by default.

### USGS Earthquakes - Seismic event feeds

The [USGS Earthquakes tool](usgs-earthquakes/README.md) fetches real-time
earthquake events from the USGS GeoJSON feeds with deduplication and publishes
them to Kafka as CloudEvents. The data is polled every 60 seconds by default.

### USGS Instantaneous Values - Water quality and quantity data

The [USGS Instantaneous Values tool](usgs-iv/README.md) is a command line tool that
can be used to retrieve real-time water quality and quantity data from the
United States Geological Survey (USGS) Instantaneous Values API. The data is
available for over 1.5 million stations in the United States and its territories.
The USGS data is updated every 15 minutes, and the data volume is relatively low.

### Waterinfo VMM - Flemish water observations

The [Waterinfo VMM bridge](waterinfo-vmm/README.md) retrieves real-time water
level data from the Belgian Waterinfo.be KIWIS API, covering approximately
1,785 monitoring stations across Flanders, and publishes the observations to
Kafka as CloudEvents. The data is polled every 15 minutes by default.

### Nextbus - Public transport data

The [Nextbus tool](nextbus/README.md) is a command line tool that can be used to
retrieve real-time data from the [Nextbus](https://www.nextbus.com/) service and
feed that data into Azure Event Hubs and Microsoft Fabric Event Streams. The tool
can also be used to query the Nextbus service interactively.


### Forza Motorsport PC - Racing game telemetry data

The
[Forza Motorsports telemetry bridge](https://github.com/clemensv/forza-telemetry-bridge)
is hosted in a separate repository. The bridge app is designed to capture and
forward Forza Motorsports telemetry data to Microsoft Azure Event Hubs or
Microsoft Fabric Event Streams. It utilizes UDP to listen for telemetry data
sent from Forza Motorsport games and forwards this data after processing and
formatting into cloud event streams. The game is compatible with the XBox and PC
games. For XBox, it requires a separate computer to run the bridge app. While
there is no containerized version, there is a binary release in a ZIP file
[available from the releases page](https://github.com/clemensv/forza-telemetry-bridge/releases).
