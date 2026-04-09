# Madrid Real-Time Traffic (Informo)

This bridge polls the Madrid Informo traffic sensor API and sends traffic data to Apache Kafka as CloudEvents.

## Source

The bridge fetches data from [Madrid Informo](https://informo.madrid.es/informo/tmadrid/pm.xml), which provides real-time traffic sensor readings across Madrid's road network including the M-30 ring motorway and urban streets. Data is updated approximately every 5 minutes and is available under a CC BY 4.0 license.

## Event Types

- **MeasurementPoint** — Reference data describing each traffic sensor: location, road segment description, subarea, and saturation capacity.
- **TrafficReading** — Telemetry: current intensity (vehicles/hour), occupancy (%), load (%), service level (0–3), and error status.

See [EVENTS.md](EVENTS.md) for full schema details.

## How It Works

1. At startup, the bridge polls the XML feed and emits a `MeasurementPoint` reference event for every sensor.
2. Each poll cycle (every 5 minutes), the bridge emits a `TrafficReading` for each sensor without error flags.
3. Reference data is refreshed hourly.
4. Deduplication: readings with the same 5-minute timestamp boundary are not re-emitted.

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fmadrid-traffic%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fmadrid-traffic%2Fazure-template-with-eventhub.json)
