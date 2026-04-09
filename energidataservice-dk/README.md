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
