# GTFS Real Time CLI tool

The GTFS real time tool is a command line tool that can be used to retrieve real time data from GTFS Real Time endpoints and feed that data into Azure Evnt Hubs and Microsft Fabric Event Streams.

GTFS Real Time is a standard for exchanging real time data about public transit systems. The standard is maintained by Google and is described [here](https://developers.google.com/transit/gtfs-realtime/).

## Prerequisites

The tool is written in Python and requires Python 3.10 or later. You can download Python from [here](https://www.python.org/downloads/). You also need to install the `git` command line tool. You can download `git` from [here](https://git-scm.com/downloads).

## Installation

Install the tool from the command line as follows:

```bash
git clone https://github.com/clemensv/real-time-sources.git
cd real-time-sources/gtfs
pip install .
```

A package install will be available later.

## Usage

```bash
options:
  -h, --help            show this help message and exit

subcommands:
  {feed,vehicle-locations}
    feed                poll vehicle locations and submit to an Event Hub
    vehicle-locations   get the vehicle locations for a route
    
```


### Vehicle Locations

This command returns the vehicle locations from the feed.

* `--agency <name>`: the name of the agency (required)
* `--gtfs-url <url>`: the URL of the agency's GTFS real-time endpoint (required)`
* `--header <key> <value>`: extra HTTP header to use for the request to the GTFS real-time endpoint. Can be specified multiple times. (optional)

```bash
gtfs-cli vehicle-locations --agency <agency> --gtfs-url <url> [--header <key> <value>]
```

The output is a list of vehicle locations, one per line. Each line contains the following information:

* the vehicle id
* the vehicle location as a latitude/longitude pair
* the vehicle heading in degrees
* the vehicle speed in km/h
* a link to a map showing the vehicle location


### Feed

This command polls the GTFS real-time endpoint for vehicle locations and submits them to an Azure Event Hub
instance or to a Microsoft Fabric Event Stream. The command requires the following parameters:

* `--agency <name>`: the name of the agency (required)
* `--gtfs-url <url>`: the URL of the agency's GTFS real-time endpoint (required)`
* `--header <key> <value>`: extra HTTP header to use for the request to the GTFS real-time endpoint. Can be specified multiple times. (optional)
* `--feed-connection-string <string>`: the connection string for the Azure Event Hub instance that receives the
    vehicle locations. The connection string must include the `Send` policy. (required)
* `--feed-event-hub-name <name>`: the name of the Event Hub instance that receives the vehicle locations (required)
* `--poll-interval <num>`: the interval in seconds between polls of the GTFS feed service. The default is 10 seconds. (optional)

The connection information for the Event Hub instances can be found in the Azure portal. The connection string
is available in the "Shared access policies" section of the Event Hub instance. The Event Hub name is the name
of the Event Hub instance. 

The feed command will run until interrupted with `Ctrl-C`. 

```bash
gtfs-cli feed --agency <agency> --route <route> --feed-connection-string <feed-connection-string> --feed-event-hub-name <feed-event-hub-name>
```

### "Feed" Event Hub output

The output into the "feed" Event Hub are CloudEvent messages with the `type` attribute 
set to `gtfs.vehiclePosition`. The `subject` attribute is set to `{agency_tag}/{vehicle_id}`.

#### gtfs.vehiclePosition

The `data`of the CloudEvent message is a JSON object with the following attributes:

* `agency`: the agency tag 
* `routeTag`: the route tag 
* `dirTag`: the direction tag 
* `id`: the vehicle id
* `lat`: the vehicle location latitude
* `lon`: the vehicle location as a longitude
* `predictable`: whether the vehicle location is predictable
* `heading`: the vehicle heading in degrees
* `speedKmHr`: the vehicle speed in km/h
* `timestamp`: the timestamp of the vehicle location

## Public GTFS Real time feeds with vehicle positions

| Agency | URL | Documentation |
|--------|-----|---------------|
| New York City MTA Bus Time, US | http://gtfsrt.prod.obanyc.com/vehiclePositions?key={key} | https://bustime.mta.info/wiki/Developers/GTFSRt |
| Catalunya FGC, ES |https://fgc.opendatasoft.com/explore/dataset/vehicle-positions-gtfs_realtime/files/d286964db2d107ecdb1344bf02f7b27b/download/ | https://data.europa.eu/data/datasets/https-analisi-transparenciacatalunya-cat-api-views-y6iv-pycv?locale=en |
| Brest métropole, FR | https://www.data.gouv.fr/fr/datasets/r/d5d43e1e-af62-4811-8a4e-ca14ad4209c8 | https://data.europa.eu/data/datasets/55ffbe0888ee387348ccb97d?locale=en |
| ALEOP (regional transport in Pays de la Loire), FR | https://www.data.gouv.fr/fr/datasets/r/b78c6d8a-3145-4deb-b68a-9b6fc9af7a89 | https://data.europa.eu/data/datasets/632b2c56696ec36c7f4811c8?locale=en |
