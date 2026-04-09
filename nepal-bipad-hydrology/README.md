# Nepal BIPAD Portal — Real-Time River Monitoring Bridge

This project provides a bridge between the [Nepal BIPAD Portal](https://bipadportal.gov.np/)
river monitoring API and Apache Kafka, Azure Event Hubs, and Fabric Event Streams.

## Source

The BIPAD Portal (Building Information Platform Against Disaster) is operated by
the Government of Nepal. The river-stations API provides real-time water level
data from monitoring stations across Nepal's major Himalayan river basins:
Bagmati, Narayani, Koshi, Karnali, Mahakali, Babai, and others.

- **API**: `https://bipadportal.gov.np/api/v1/river-stations/?format=json`
- **Auth**: None (open government data)
- **Update frequency**: Every 15–30 minutes
- **Data source**: Nepal Department of Hydrology and Meteorology (hydrology.gov.np)

## Events

The bridge emits two CloudEvents types:

| Type | Description |
|------|-------------|
| `np.gov.bipad.hydrology.RiverStation` | Reference data: station metadata, location, basin, thresholds |
| `np.gov.bipad.hydrology.WaterLevelReading` | Telemetry: current water level, status, trend |

See [EVENTS.md](EVENTS.md) for full schema documentation.

## Running

```shell
# Using connection string
docker run --rm \
    -e CONNECTION_STRING='BootstrapServer=localhost:9092;EntityPath=nepal-bipad-hydrology' \
    ghcr.io/clemensv/real-time-sources-nepal-bipad-hydrology:latest

# Using explicit Kafka config
docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='localhost:9092' \
    -e KAFKA_TOPIC='nepal-bipad-hydrology' \
    ghcr.io/clemensv/real-time-sources-nepal-bipad-hydrology:latest
```

See [CONTAINER.md](CONTAINER.md) for full deployment documentation.

## Development

```shell
cd nepal-bipad-hydrology
pip install -e .
pip install -e nepal_bipad_hydrology_producer/nepal_bipad_hydrology_producer_data
pip install -e nepal_bipad_hydrology_producer/nepal_bipad_hydrology_producer_kafka_producer
python -m pytest tests -m "unit or integration" --no-header -q
```

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnepal-bipad-hydrology%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnepal-bipad-hydrology%2Fazure-template-with-eventhub.json)
