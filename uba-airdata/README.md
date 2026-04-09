# UBA Germany Air Quality Bridge

This source bridges the Umweltbundesamt (UBA) `air_data/v3` API into Apache
Kafka compatible brokers as structured JSON CloudEvents.

It emits:

- `Station` reference events for air quality monitoring stations
- `Component` reference events for pollutant components such as NO₂, O₃, PM10,
  and PM2.5
- `Measure` telemetry events for hourly measurements

The bridge follows the repo-standard poller pattern: it emits reference data at
startup, refreshes it periodically, and then polls hourly measurements on a
cadence you control.

## Upstream API

- Base URL: `https://www.umweltbundesamt.de/api/air_data/v3/`
- Stations: `/stations/json?lang=en`
- Components: `/components/json?lang=en`
- Networks: `/networks/json?lang=en` (reviewed during source design; station
  payloads already carry denormalized network metadata, so no separate network
  event type is emitted)
- Scopes: `/scopes/json?lang=en` (reviewed during source design; not emitted as
  separate events)
- Measures: `/measures/json?component={id}&scope={id}&date_from={date}&date_to={date}&lang=en`

## Event Model

Two message groups share the same Kafka topic:

- `de.uba.airdata`
  - key / subject: `{station_id}`
  - messages: `Station`, `Measure`
- `de.uba.airdata.components`
  - key / subject: `{component_id}`
  - messages: `Component`

See [EVENTS.md](EVENTS.md) for the contract details.

## Installation

From this directory:

```powershell
pip install uba_airdata_producer/uba_airdata_producer_data
pip install uba_airdata_producer/uba_airdata_producer_kafka_producer
pip install -e .
```

## Usage

Run the bridge:

```powershell
uba_airdata feed --connection-string "<connection-string>"
```

or:

```powershell
uba_airdata feed --kafka-bootstrap-servers "<host:port>" --kafka-topic "uba-airdata"
```

## Configuration

- `CONNECTION_STRING`
- `KAFKA_BOOTSTRAP_SERVERS`
- `KAFKA_TOPIC`
- `SASL_USERNAME`
- `SASL_PASSWORD`
- `KAFKA_ENABLE_TLS`
- `POLLING_INTERVAL`
- `STATE_FILE`

For container usage, see [CONTAINER.md](CONTAINER.md).

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fuba-airdata%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fuba-airdata%2Fazure-template-with-eventhub.json)
