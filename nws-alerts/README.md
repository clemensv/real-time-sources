# NWS CAP Weather Alerts Bridge

This bridge polls the US National Weather Service (NWS) alerts API for active
weather and non-weather alerts and forwards them to Apache Kafka, Azure Event
Hubs, or Microsoft Fabric Event Streams as CloudEvents.

## Data Source

- API: `https://api.weather.gov/alerts/active`
- Format: GeoJSON (CAP-structured)
- Authentication: none
- Coverage: United States and territories

## Events

See [EVENTS.md](EVENTS.md) for the CloudEvents contract.

## Usage

```bash
python -m nws_alerts --bootstrap-servers "localhost:9092" --poll-interval 120
```

Or use a connection string:

```bash
python -m nws_alerts --connection-string "<connection-string>"
```

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `CONNECTION_STRING` | Event Hubs connection string | none |
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka bootstrap servers | none |
| `KAFKA_TOPIC` | Kafka topic | `nws-alerts` |
| `SASL_USERNAME` | SASL username | none |
| `SASL_PASSWORD` | SASL password | none |
| `NWS_ALERTS_STATE_FILE` | State file path | `~/.nws_alerts_state.json` |
| `NWS_ALERTS_POLL_INTERVAL` | Poll interval (seconds) | `120` |
| `LOG_LEVEL` | Logging level | `INFO` |

## Testing

```bash
pytest tests/test_nws_alerts.py
```

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnws-alerts%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnws-alerts%2Fazure-template-with-eventhub.json)
