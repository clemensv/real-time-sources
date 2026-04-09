# EAWS ALBINA Avalanche Bulletin Bridge

A real-time bridge that fetches daily avalanche danger bulletins from the EAWS ALBINA system ([avalanche.report](https://avalanche.report)) and publishes them as CloudEvents to Apache Kafka, Azure Event Hubs, or Fabric Event Streams.

## Source

The European Avalanche Warning Services (EAWS) ALBINA system publishes daily avalanche bulletins in the CAAMLv6 standard for European Alps regions:

- **Tirol** (AT-07)
- **South Tyrol** (IT-32-BZ)
- **Trentino** (IT-32-TN)
- **Salzburg** (AT-02)

Bulletins are published twice daily during winter season and include:
- Danger ratings on the 5-level EAWS scale (low → very_high)
- Avalanche problem types (wet snow, persistent weak layers, wind slab, etc.)
- Tendency forecasts (decreasing, steady, increasing)
- Danger patterns (LWD Tyrol classification)
- Snowpack structure analysis

Data is freely available under CC BY license at `https://avalanche.report/albina_files/`.

## Events

See [EVENTS.md](EVENTS.md) for the full event schema documentation.

## Container

See [CONTAINER.md](CONTAINER.md) for Docker deployment instructions and environment variable reference.

## Local Development

```bash
pip install -e .
pip install -e eaws_albina_producer/eaws_albina_producer_data
pip install -e eaws_albina_producer/eaws_albina_producer_kafka_producer
python -m pytest tests -m "unit or integration" --no-header -q
```

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Feaws-albina%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Feaws-albina%2Fazure-template-with-eventhub.json)
