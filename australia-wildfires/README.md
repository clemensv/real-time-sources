# Australian State Wildfires Bridge

This bridge aggregates live bushfire incident data from three Australian state
emergency services and emits normalized `FireIncident` CloudEvents to a Kafka
topic.

## Sources

| State | Agency | Endpoint |
|-------|--------|----------|
| NSW | Rural Fire Service | `https://www.rfs.nsw.gov.au/feeds/majorIncidents.json` |
| VIC | VicEmergency | `https://www.emergency.vic.gov.au/public/osom-geojson.json` |
| QLD | Queensland Fire Department | `https://publiccontent-gis-psba-qld-gov-au.s3.amazonaws.com/content/Feeds/BushfireCurrentIncidents/bushfireAlert.json` |

All three endpoints are public GeoJSON feeds requiring no authentication.

## How It Works

1. The bridge polls all three GeoJSON endpoints every 5 minutes (configurable).
2. NSW features are parsed directly; VIC features are filtered for
   `category2 == "Fire"` or CAP category containing "Fire"; QLD features are
   included as-is (the feed is bushfire-only).
3. Each feature is normalized into a unified `FireIncident` schema with
   coordinates extracted from the GeoJSON geometry.
4. Deduplication is performed by `{state}/{incident_id}` + `updated` timestamp.
5. New or updated incidents are emitted as structured CloudEvents to Kafka.

## Event Types

See [EVENTS.md](EVENTS.md) for the full event catalog.

## Fabric notebook hosting

This source ships a Fabric notebook (`notebook/australia-wildfires-feed.ipynb`) deployable via [`tools/deploy-fabric/deploy-feeder-notebook.ps1`](../tools/deploy-fabric/deploy-feeder-notebook.ps1) for serverless polling inside a Fabric workspace.

## Running

```bash
# Install
pip install -e .

# List current incidents
python -m australia_wildfires list

# Feed to Kafka
python -m australia_wildfires --connection-string "BootstrapServer=localhost:9092;EntityPath=australia-wildfires" feed

# Feed to MQTT/UNS
MQTT_BROKER_URL=mqtt://localhost:1883 python -m australia_wildfires_mqtt feed
```

## Container

See [CONTAINER.md](CONTAINER.md) for Docker deployment instructions.

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faustralia-wildfires%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faustralia-wildfires%2Fazure-template-with-eventhub.json)


## AMQP 1.0 feeder

This source also ships an AMQP 1.0 companion container (`Dockerfile.amqp`, image `ghcr.io/clemensv/real-time-sources-australia-wildfires-amqp:latest`). It publishes the same CloudEvents contract documented in [EVENTS.md](EVENTS.md) to a single AMQP address named `australia-wildfires` by default. Use it for enterprise queue/topic consumers on ActiveMQ Artemis, RabbitMQ AMQP 1.0, Qpid Dispatch, or Azure Service Bus.

```bash
docker run --rm   -e AMQP_BROKER_URL=amqp://user:password@broker:5672/australia-wildfires   -e AUSTRALIA_WILDFIRES_SAMPLE_MODE=true ONCE_MODE=true   ghcr.io/clemensv/real-time-sources-australia-wildfires-amqp:latest
```

Azure Service Bus deployment (new namespace, queue, managed identity, and ACI):

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faustralia-wildfires%2Finfra%2Fazure-template-amqp.json)
