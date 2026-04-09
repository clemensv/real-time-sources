# IMGW-PIB Hydrological Data Bridge

This bridge fetches real-time hydrological data from the Polish Institute of
Meteorology and Water Management (IMGW-PIB) public API and forwards it to
Apache Kafka or Microsoft Azure Event Hubs as CloudEvents.

The IMGW-PIB provides real-time water level, water temperature, and discharge
data for hundreds of hydrological stations across Poland.

## Data Source

- **API Endpoint**: https://danepubliczne.imgw.pl/api/data/hydro
- **Data Format**: JSON
- **Update Frequency**: Approximately every hour
- **Authentication**: None required (open data)
- **License**: Public data from IMGW-PIB (Instytut Meteorologii i Gospodarki
  Wodnej – Państwowy Instytut Badawczy)

## Data Attribution

Źródłem pochodzenia danych jest Instytut Meteorologii i Gospodarki Wodnej –
Państwowy Instytut Badawczy (IMGW-PIB). The data source is the Institute of
Meteorology and Water Management – National Research Institute.

## Events

See [EVENTS.md](EVENTS.md) for details on the CloudEvents produced by this
bridge.

## Deployment

See [CONTAINER.md](CONTAINER.md) for container deployment instructions.

## Usage

### List all stations

```bash
python -m imgw_hydro list
```

### Get water level for a specific station

```bash
python -m imgw_hydro level <station_id>
```

### Feed data to Kafka

```bash
python -m imgw_hydro feed --connection-string "<connection_string>" --topic imgw-hydro
```

Or using environment variables:

```bash
export KAFKA_BROKER=localhost:9092
export KAFKA_TOPIC=imgw-hydro
python -m imgw_hydro feed
```

## Configuration

| Environment Variable | Description | Default |
|---|---|---|
| `KAFKA_CONNECTION_STRING` or `CONNECTION_STRING` | Kafka/Event Hubs connection string | None |
| `KAFKA_BROKER` | Kafka bootstrap server | None |
| `KAFKA_TOPIC` | Kafka topic name | `imgw-hydro` |
| `POLLING_INTERVAL` | Polling interval in seconds | `600` |

## Setup

```bash
pip install -r requirements.txt
pip install -e .
```

## Testing

```bash
pytest tests/test_imgw_hydro_unit.py      # Unit tests (no network)
pytest tests/test_imgw_hydro_e2e.py        # End-to-end tests (hits real API)
pytest tests/test_imgw_hydro_container.py  # Container tests (requires Docker)
```

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fimgw-hydro%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fimgw-hydro%2Fazure-template-with-eventhub.json)
