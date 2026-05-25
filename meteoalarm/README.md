# Meteoalarm European Weather Warnings Bridge

This bridge polls the EUMETNET Meteoalarm API for severe weather warnings from
30+ European national meteorological services and forwards them to Apache
Kafka, Azure Event Hubs, Microsoft Fabric Event Streams, MQTT 5.0, or AMQP 1.0 as CloudEvents.

## Data Source

- API: `https://feeds.meteoalarm.org/api/v1/warnings/feeds-{country}`
- Format: JSON (CAP-structured)
- Authentication: none
- Coverage: 30+ European countries

## Events

See [EVENTS.md](EVENTS.md) for the CloudEvents contract.

## Usage

```bash
python -m meteoalarm --bootstrap-servers "localhost:9092" --poll-interval 300
```

Or use a connection string:

```bash
python -m meteoalarm --connection-string "<connection-string>"
```

Limit to specific countries:

```bash
python -m meteoalarm --connection-string "<cs>" --countries "germany,france,spain"
```

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `CONNECTION_STRING` | Event Hubs connection string | none |
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka bootstrap servers | none |
| `KAFKA_TOPIC` | Kafka topic | `meteoalarm` |
| `SASL_USERNAME` | SASL username | none |
| `SASL_PASSWORD` | SASL password | none |
| `METEOALARM_STATE_FILE` | State file path | `~/.meteoalarm_state.json` |
| `METEOALARM_POLL_INTERVAL` | Poll interval (seconds) | `300` |
| `LOG_LEVEL` | Logging level | `INFO` |

## Testing

```bash
pytest tests/test_meteoalarm.py
```

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fmeteoalarm%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fmeteoalarm%2Fazure-template-with-eventhub.json)

## Transports

This source now ships separate Kafka and MQTT containers over the same xRegistry contract. The Kafka image is the best fit when consumers need replay, batch catch-up, or a single ordered stream. The MQTT image (`ghcr.io/clemensv/real-time-sources-meteoalarm-mqtt:latest`) is the better fit for operational dashboards and Unified Namespace subscribers that want to subscribe directly to the current state or live event slice for this source.

The MQTT contract is source-specific: MQTT/5.0 transport variant for Meteoalarm CAP weather warnings. Non-retained QoS-1 warning events route by country feed slug, native CAP severity, normalized Meteoalarm awareness type, and CAP identifier under alerts/intl/meteoalarm/meteoalarm/... The awareness_type axis is derived from the Meteoalarm awareness_type parameter label and normalized for MQTT topic safety.

MQTT publishes binary-mode CloudEvents with JSON payloads and CloudEvent attributes in MQTT 5 user properties. Topic patterns from `xreg/meteoalarm.xreg.json`:

| Topic pattern | Message type | Delivery |
|---|---|---|
| `alerts/intl/meteoalarm/meteoalarm/{country}/{severity}/{awareness_type}/{identifier}/warning` | `Meteoalarm.WeatherWarning` | QoS 1, retain=false |

Four Azure Container Instance deployment shapes are documented for this source:

| Transport | Template |
|---|---|
| Kafka, bring your own Event Hub or compatible broker | `azure-template.json` |
| Kafka, create an Event Hubs namespace and hub | `azure-template-with-eventhub.json` |
| MQTT, bring your own MQTT 5 broker | `azure-template-mqtt.json` |
| MQTT, create an Azure Event Grid namespace MQTT broker | `azure-template-with-eventgrid-mqtt.json` |

See [CONTAINER.md](CONTAINER.md) for runtime environment variables and deployment badges, and [EVENTS.md](EVENTS.md) for the full CloudEvents and MQTT topic contract.

## AMQP 1.0 companion feeder

This source now ships Kafka, MQTT, and AMQP 1.0 transport variants. The AMQP container (`ghcr.io/clemensv/real-time-sources-meteoalarm-amqp:latest`) publishes the same CloudEvents payloads as the Kafka and MQTT feeders to a single broker address named `meteoalarm` by default, using binary-mode AMQP 1.0 for generic brokers or Azure Service Bus.

Run locally against an AMQP 1.0 broker:

```bash
docker run --rm \
  -e AMQP_HOST=broker \
  -e AMQP_PORT=5672 \
  -e AMQP_ADDRESS=meteoalarm \
  -e AMQP_USERNAME=admin \
  -e AMQP_PASSWORD=admin \
  -e AMQP_AUTH_MODE=password \
  ghcr.io/clemensv/real-time-sources-meteoalarm-amqp:latest
```

Deploy to Azure Service Bus with `azure-template-with-servicebus.json` (also mirrored at `infra/azure-template-amqp.json`). The template provisions a Service Bus queue, storage-backed state share, a user-assigned managed identity, and an Azure Container Instance configured for AMQP CBS / Entra ID authentication.

