# EURDEP Radiation

Bridge for the **EURDEP (European Radiological Data Exchange Platform)**
pan-European ambient gamma dose rate monitoring network.

EURDEP aggregates near-real-time radiological monitoring data from
approximately 5,500 stations across 39 European countries. Each station
reports hourly averaged ambient gamma dose rate in microsieverts per hour
(µSv/h).

## Quick Start

```bash
pip install -e .
pip install -e eurdep_radiation_producer/eurdep_radiation_producer_data
pip install -e eurdep_radiation_producer/eurdep_radiation_producer_kafka_producer
python -m eurdep_radiation feed --connection-string "BootstrapServer=localhost:9092;EntityPath=eurdep-radiation"
```

## Events

See [EVENTS.md](EVENTS.md) for the full event catalog.

## Container

See [CONTAINER.md](CONTAINER.md) for Docker deployment instructions.

## Upstream Source

- EURDEP: https://eurdep.jrc.ec.europa.eu/
- WFS endpoint: https://www.imis.bfs.de/ogc/opendata/ows
- Protocol: WFS 1.1.0 with GeoJSON output
- Auth: None (EU open data)
- Update frequency: Hourly

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Feurdep-radiation%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Feurdep-radiation%2Fazure-template-with-eventhub.json)
