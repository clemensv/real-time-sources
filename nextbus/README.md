# Nextbus CLI tool

The Nextbus tool is a command line tool that can be used to retrieve real time data from the [Nextbus](https://www.nextbus.com/) service and feed that data into Azure Evnt Hubs and Microsft Fabric Event Streams.

The tool can also be used to query the Nextbus service interactively.

You must accept the [Nextbus Terms of Use](https://www.nextbus.com/xmlFeedDocs/NextBusXMLFeed.pdf) to use this tool. 

## Prerequisites

The Nextbus tool is written in Python and requires Python 3.10 or later. You can download Python from [here](https://www.python.org/downloads/). You also need to install the `git` command line tool. You can download `git` from [here](https://git-scm.com/downloads).

## Installation

Install the tool from the command line as follows:

```bash
git clone https://github.com/clemensv/real-time-sources.git
cd real-time-sources/nextbus
pip install .
```

A package install will be available later.

## Usage

```bash
options:
  -h, --help            show this help message and exit

subcommands:
  {agencies,routes,feed,vehicle-locations,predictions,route-config}
    agencies            get the list of transit agencies
    routes              get the list of routes for an agency
    feed                poll vehicle locations and submit to an Event Hub
    vehicle-locations   get the vehicle locations for a route
    predictions         get the predictions for a stop
    route-config        get the configuration for a route
```

### Agencies

This command returns the list of transit agencies that are supported by the Nextbus service.

```bash
nextbus agencies
```

### Routes

This command returns the list of routes for a given agency. Use the agency tag returned as 
the first value in every line from the `agencies` command to specify the agency, for example
`ttc` for the Toronto Transit Commission.


```bash
nextbus routes --agency <agency>
```

### Route Config

This command returns the configuration for a given route. You must specify the agency tag
and the route tag returned by the `agencies` and `routes` commands.

```bash
nextbus route-config --agency <agency> --route <route>
```

The output is a list of route stops, one per line. Each line contains the following information:

* the stop tag
* the stop title
* the stop location as a latitude/longitude pair
* a link to a map showing the stop location

### Vehicle Locations

This command returns the vehicle locations for a given route. You must specify the agency tag 
and the route tag returned by the `agencies` and `routes` commands.

```bash
nextbus vehicle-locations --agency <agency> --route <route>
```

The output is a list of vehicle locations, one per line. Each line contains the following information:

* the vehicle id
* the vehicle location as a latitude/longitude pair
* the vehicle heading in degrees
* the vehicle speed in km/h
* a link to a map showing the vehicle location

### Predictions

This command returns the predictions for a given stop. You must specify the agency tag
and the stop tag returned by the `agencies` and `route-config` commands.

```bash
nextbus predictions --agency <agency> --stop <stop>
``` 

The output is a list of predictions, one per line. Each line contains the following information:

### Feed

This command polls the Nextbus service for vehicle locations and submits them to an Azure Event Hub
instance or to a Microsoft Fabric Event Stream. The command requires the following parameters:

* `--agency`: the agency tag returned by the `agencies` command (required)
* `--route`: the route tag returned by the `routes` command. If the value is omitted or set to `*` then
  the command will poll all routes for the agency. (optional)
* `--feed-connection-string`: the connection string for the Azure Event Hub instance that receives the
    vehicle locations. The connection string must include the `Send` policy. (required)
* `--feed-event-hub-name`: the name of the Event Hub instance that receives the vehicle locations (required)
* `--reference-connection-string`: If and only if this connection string is set, the command will also periodically 
    retrieve the routes and stops and schedules and messages for the agency and submit them to a "reference"
    Event Hub instance. The connection string must include the `Send` policy. The Event Hub may be configured
    with a "Compaction" retention policy to only keep the latest version of each entity. (optional)
* `--reference-event-hub-name`: the name of the Event Hub instance that receives the reference data (optional)

 event_detail = {
            "agency": agency_tag,
            "routeTag": vehicle.get("routeTag"),
            "dirTag": vehicle.get("dirTag"),
            "id": vehicle.get("id"),
            "lat": vehicle.get("lat"),
            "lon": vehicle.get("lon"),
            "predictable": vehicle.get("predictable"),
            "heading": vehicle.get("heading"),
            "speedKmHr": vehicle.get("speedKmHr"),
            "timestamp": last_report_time
        }
        last_report_time_iso = datetime.utcfromtimestamp(last_report_time).isoformat()
            
        event = CloudEvent({
            "specversion": "1.0",
            "type": "nextbus.vehiclePosition",
            "source": "https://retro.umoiq.com/service/publicXMLFeed",
            "subject": f"{agency_tag}/{vehicle.get('id')}",
            "datacontenttype": "application/json",
            "time": last_report_time_iso
        })

The output into the "feed" Event Hub are CloudEvent messages with the `type` attribute 
set to `nextbus.vehiclePosition`. The `subject` attribute is set to `{agency_tag}/{vehicle_id}`.

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

The output into the "reference" Event Hub are CloudEvent messages with the `type` attribute
set to `nextbus.routeConfig`, `nextbus.schedule`, and `nextbus.messages`.

#### nextbus.routeConfig

The `data` of the CloudEvent message is a JSON object with the following attributes:

* `agency`: the agency tag
* `routeTag`: the route tag
* `routeConfig`: the route configuration as a JSON object

#### nextbus.schedule

The `data` of the CloudEvent message is a JSON object with the following attributes:

* `agency`: the agency tag
* `routeTag`: the route tag
* `schedule`: the route schedule as a JSON object

#### nextbus.messages

The `data` of the CloudEvent message is a JSON object with the following attributes:

* `agency`: the agency tag
* `routeTag`: the route tag
* `messages`: the route messages as a JSON object





