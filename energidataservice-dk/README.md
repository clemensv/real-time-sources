# Energi Data Service (Energinet) Denmark Bridge

A real-time data bridge that polls the [Energi Data Service](https://www.energidataservice.dk/) API operated by Energinet (the Danish TSO) and streams Danish power system data to Apache Kafka, Azure Event Hubs, or Fabric Event Streams as CloudEvents.

## Data Sources

| Dataset | Update Frequency | Description |
|---------|-----------------|-------------|
| PowerSystemRightNow | ~1 minute | System-wide snapshot: CO2, solar, wind, exchange flows, balancing, imbalance |
| ElspotPrices | Hourly | Day-ahead spot prices per bidding zone (DK1, DK2) in DKK and EUR |

## Events

See [EVENTS.md](EVENTS.md) for the full event schema documentation.

## Container

See [CONTAINER.md](CONTAINER.md) for container deployment instructions.

## Fabric notebook hosting

This source ships a Fabric notebook feeder at [`notebook/energidataservice-dk-feed.ipynb`](notebook/energidataservice-dk-feed.ipynb); deploy it with [`tools/deploy-fabric/deploy-feeder-notebook.ps1`](../tools/deploy-fabric/deploy-feeder-notebook.ps1) to run scheduled single-cycle polls inside a Microsoft Fabric workspace.

## Quick Start

```shell
docker run --rm \
    -e CONNECTION_STRING='BootstrapServer=localhost:9092;EntityPath=energidataservice-dk' \
    -e KAFKA_ENABLE_TLS=false \
    ghcr.io/clemensv/real-time-sources-energidataservice-dk:latest
```

## Development

```shell
cd energidataservice-dk
pip install energidataservice_dk_producer/energidataservice_dk_producer_data
pip install energidataservice_dk_producer/energidataservice_dk_producer_kafka_producer
pip install -e .
pytest
```

## Regenerating the Producer

```shell
cd energidataservice-dk
pwsh generate_producer.ps1
```

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fenergidataservice-dk%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fenergidataservice-dk%2Fazure-template-with-eventhub.json)


## Transports

This source now ships Kafka plus MQTT and AMQP companion feeders. MQTT publishes binary-mode CloudEvents into the documented topic tree for wildcard subscribers and retained last-known-value use cases. AMQP publishes the same CloudEvents to a broker address for queue/topic consumers. Deployment templates include `azure-template.json`, `azure-template-with-eventhub.json`, `azure-template-mqtt.json`, `azure-template-with-eventgrid-mqtt.json`, `azure-template-amqp.json`, and `azure-template-with-servicebus.json`. Dockerfiles: `Dockerfile`, `Dockerfile.mqtt`, `Dockerfile.amqp`.
