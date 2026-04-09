# SMHI Hydrological Data Bridge

This bridge fetches real-time hydrological discharge data from the Swedish
Meteorological and Hydrological Institute (SMHI) open data portal and forwards
it to Apache Kafka or Microsoft Azure Event Hubs as CloudEvents.

SMHI provides real-time 15-minute discharge (flow rate) data for hundreds of
hydrological stations across Sweden via a bulk API endpoint, updated every 15
minutes.

## Data Source

- **API Endpoint**: https://opendata-download-hydroobs.smhi.se/api/version/1.0/
- **Data Format**: JSON (bulk endpoint for all stations)
- **Update Frequency**: Every 15 minutes
- **Authentication**: None required (open data)
- **License**: Open data from SMHI (Sveriges meteorologiska och hydrologiska institut)

## Data Attribution

Data is provided by SMHI (Sveriges meteorologiska och hydrologiska institut).
The data is available under SMHI's open data license.

## Events

See [EVENTS.md](EVENTS.md) for details on the CloudEvents produced by this
bridge.

## Deployment

See [CONTAINER.md](CONTAINER.md) for container deployment instructions.

## Usage

### List all stations

```bash
python -m smhi_hydro list
```

### Get discharge for a specific station

```bash
python -m smhi_hydro observation 1583
```

### Feed data to Kafka

```bash
python -m smhi_hydro feed --connection-string "<connection_string>" --topic smhi-hydro
```

Or using environment variables:

```bash
export KAFKA_BROKER=localhost:9092
export KAFKA_TOPIC=smhi-hydro
python -m smhi_hydro feed
```

## Configuration

| Environment Variable | Description | Default |
|---|---|---|
| `KAFKA_CONNECTION_STRING` or `CONNECTION_STRING` | Kafka/Event Hubs connection string | None |
| `KAFKA_BROKER` | Kafka bootstrap server | None |
| `KAFKA_TOPIC` | Kafka topic name | `smhi-hydro` |
| `POLLING_INTERVAL` | Polling interval in seconds | `900` |

## Setup

```bash
pip install -r requirements.txt
pip install -e .
```

## Testing

```bash
pytest tests/test_smhi_hydro_unit.py      # Unit tests (no network)
pytest tests/test_smhi_hydro_e2e.py        # End-to-end tests (hits real API)
pytest tests/test_smhi_hydro_container.py  # Container tests (requires Docker)
```

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsmhi-hydro%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fsmhi-hydro%2Fazure-template-with-eventhub.json)
