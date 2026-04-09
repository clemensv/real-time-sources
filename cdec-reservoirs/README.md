# CDEC California Reservoirs Bridge

This source bridges real-time reservoir data from the California Data Exchange
Center (CDEC) to Apache Kafka, Azure Event Hubs, or Fabric Event Streams.

## Data Source

The [California Data Exchange Center (CDEC)](https://cdec.water.ca.gov/) is
operated by the California Department of Water Resources. It provides real-time
hydrologic data for over 2,600 stations, including all major California
reservoirs.

The bridge polls the CDEC JSON Data Servlet for hourly readings of:
- **Storage** (acre-feet) — sensor 15
- **Reservoir Elevation** (feet) — sensor 6
- **Inflow** (cubic feet per second) — sensor 76
- **Outflow** (cubic feet per second) — sensor 23

Default monitored stations include Shasta (SHA), Oroville (ORO), Folsom (FOL),
New Melones (NML), Don Pedro (DNP), Hetch Hetchy (HTC), Sonoma (SON),
Millerton (MIL), and Pine Flat (PNF).

## Events

See [EVENTS.md](EVENTS.md) for the event schema documentation.

## Container

See [CONTAINER.md](CONTAINER.md) for Docker deployment instructions.

## Development

```shell
cd cdec-reservoirs
pip install -e .
pip install -e cdec_reservoirs_producer/cdec_reservoirs_producer_data
pip install -e cdec_reservoirs_producer/cdec_reservoirs_producer_kafka_producer
python -m pytest tests -m "unit or integration" --no-header -q
```

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcdec-reservoirs%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fcdec-reservoirs%2Fazure-template-with-eventhub.json)
