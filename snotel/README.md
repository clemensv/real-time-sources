# USDA NRCS SNOTEL Snow and Weather Bridge

A real-time data bridge that fetches hourly snow and weather observations from the USDA Natural Resources Conservation Service (NRCS) SNOTEL (SNOwpack TELemetry) network and produces them as CloudEvents to Apache Kafka, Azure Event Hubs, or Fabric Event Streams.

## Overview

SNOTEL is an automated system of over 900 snowpack monitoring sites in the western United States and Alaska operated by the NRCS. Each station reports:

- **Snow Water Equivalent (SWE)** — the primary measurement for water supply forecasting
- **Snow Depth** — total snow depth from ultrasonic sensors
- **Precipitation** — water-year accumulated precipitation
- **Air Temperature** — instantaneous readings (known bias, see NRCS docs)

Data is transmitted hourly via satellite telemetry and is publicly available through the [NRCS Report Generator](https://wcc.sc.egov.usda.gov/reportGenerator/). No API key or authentication is required (US Government public domain data).

## Event Types

See [EVENTS.md](EVENTS.md) for the full event schema documentation.

- **Station** — Reference data emitted at startup for each configured station
- **SnowObservation** — Hourly telemetry readings from SNOTEL stations

## Quick Start

```shell
# With a plain Kafka broker
docker run --rm \
    -e CONNECTION_STRING='BootstrapServer=localhost:9092;EntityPath=snotel' \
    ghcr.io/clemensv/real-time-sources-snotel:latest

# With Azure Event Hubs
docker run --rm \
    -e CONNECTION_STRING='Endpoint=sb://mynamespace.servicebus.windows.net/;SharedAccessKeyName=send;SharedAccessKey=...;EntityPath=snotel' \
    ghcr.io/clemensv/real-time-sources-snotel:latest
```

## Configuration

See [CONTAINER.md](CONTAINER.md) for full deployment documentation including environment variables and Azure Container Instance templates.

## Development

```shell
cd snotel
pip install -e .
pip install -e snotel_producer/snotel_producer_data
pip install -e snotel_producer/snotel_producer_kafka_producer
python -m pytest tests -m "unit or integration" -v
```

### Regenerate Producer

```powershell
.\generate_producer.ps1
```

Requires `xrcg` 0.10.1.

## Data Source

- **Provider**: USDA Natural Resources Conservation Service (NRCS)
- **API**: https://wcc.sc.egov.usda.gov/reportGenerator/
- **Update frequency**: Hourly via satellite telemetry
- **Coverage**: 900+ stations across western US and Alaska
- **License**: US Government Public Domain
