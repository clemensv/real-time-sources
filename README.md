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

* [GTFS Realtime - Public transport data](gtfs/CONTAINER.md)
* [NOAA Tides ands Currents -  Water level and current data](noaa/CONTAINER.md)
* [RSS Feeds - News and blog posts](rss/CONTAINER.md)
* [Pegelonline - Water level and current data](pegelonline/CONTAINER.md)

Details about the tools and the data sources are provided in the respective
README files.

## Command Line Tools

### GTFS Realtime - Public transport data

The [GTFS Realtime Bridge](gtfs/README.md) is a command line tool that retrieves
to retrieve schedules, real-time vehicle position, real-time trip updates (live
predictions of arrivals/departures), and alerts from practically any GTFS and
GTFS-RT service. Over 1000 public transport agencies worldwide publish their
data in GTFS format, and many of them also provide real-time data in GTFS-RT
format. 

In terms of sheer data volume, the feeds related to the New York City
Metropolitan Transportation Authority (MTA) will produce over 50 Gigabytes of
data each day.

### NOAA Tides ands Currents -  Water level and current data

The [NOAA data poller](noaa/README.md) is a command line tool that can be used
to retrieve real-time water level and current data from NOAA's National Ocean
Service (NOS) Tides and Currents API. The data is available for over 3000
stations in the United States and its territories. The NOAA data is updated
every 6 minutes, and the data volume is relatively low.

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

### Nextbus - Public transport data

The [Nextbus tool](nextbus/README.md) is a command line tool that can be used to
retrieve real-time data from the [Nextbus](https://www.nextbus.com/) service and
feed that data into Azure Event Hubs and Microsft Fabric Event Streams. The tool
can also be used to query the Nextbus service interactively.