# NDW Netherlands Road Traffic Bridge

This bridge downloads DATEX II XML data published by the Dutch NDW (Nationaal
Dataportaal Wegverkeer) at `https://opendata.ndw.nu` and forwards traffic
speed, travel time, and situation data to Apache Kafka, Azure Event Hubs,
or Microsoft Fabric Event Streams as CloudEvents.

## Data Sources

| Feed | URL | Update | Content |
|---|---|---|---|
| Traffic Speed | `trafficspeed.xml.gz` | ~1 min | Per-segment speed and flow |
| Travel Time | `traveltime.xml.gz` | ~1 min | Segment travel times |
| Situations | `actueel_beeld.xml.gz` | ~15 min | Road works, closures, incidents |

All files are gzip-compressed DATEX II XML (v2 for speed/travel time, v3 for
situations). No authentication is required.

## Event Types

- **TrafficSpeed** — aggregated speed/flow per measurement site
- **TravelTime** — actual and reference travel time per segment
- **TrafficSituation** — road works, lane closures, diversions

See [EVENTS.md](EVENTS.md) for the full schema documentation and
[CONTAINER.md](CONTAINER.md) for deployment instructions.

## Quick Start

```bash
pip install -e .
CONNECTION_STRING="BootstrapServer=localhost:9092;EntityPath=ndl-traffic" \
  KAFKA_ENABLE_TLS=false \
  python -m ndl_netherlands
```

## Running Tests

```bash
pip install pytest
python -m pytest tests/ -v
```

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fndl-netherlands%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fndl-netherlands%2Fazure-template-with-eventhub.json)
