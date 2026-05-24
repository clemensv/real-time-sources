# PTWC/NTWC Tsunami Bulletins Bridge

This bridge polls NOAA's tsunami warning Atom feeds for seismic event bulletins
and forwards them to Apache Kafka, Azure Event Hubs, or Microsoft Fabric Event
Streams as CloudEvents.

## Data Source

- PAAQ feed: `https://www.tsunami.gov/events/xml/PAAQAtom.xml` (Alaska/Pacific)
- PHEB feed: `https://www.tsunami.gov/events/xml/PHEBAtom.xml` (Pacific/Atlantic)
- Format: Atom XML with embedded XHTML summaries
- Authentication: none
- Coverage: Global (Pacific, Atlantic, and Caribbean)

## Events

See [EVENTS.md](EVENTS.md) for the CloudEvents contract.

## Usage

```bash
python -m ptwc_tsunami --bootstrap-servers "localhost:9092" --poll-interval 300
```

Or use a connection string:

```bash
python -m ptwc_tsunami --connection-string "<connection-string>"
```

Limit to specific feeds:

```bash
python -m ptwc_tsunami --connection-string "<cs>" --feeds "PAAQ"
```

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `CONNECTION_STRING` | Event Hubs connection string | none |
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka bootstrap servers | none |
| `KAFKA_TOPIC` | Kafka topic | `ptwc-tsunami` |
| `SASL_USERNAME` | SASL username | none |
| `SASL_PASSWORD` | SASL password | none |
| `PTWC_TSUNAMI_STATE_FILE` | State file path | `~/.ptwc_tsunami_state.json` |
| `PTWC_TSUNAMI_POLL_INTERVAL` | Poll interval (seconds) | `300` |
| `LOG_LEVEL` | Logging level | `INFO` |

## Testing

```bash
pytest tests/test_ptwc_tsunami.py
```

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fptwc-tsunami%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fptwc-tsunami%2Fazure-template-with-eventhub.json)

## Transports

This source now ships separate Kafka and MQTT containers over the same xRegistry contract. The Kafka image is the best fit when consumers need replay, batch catch-up, or a single ordered stream. The MQTT image (`ghcr.io/clemensv/real-time-sources-ptwc-tsunami-mqtt:latest`) is the better fit for operational dashboards and Unified Namespace subscribers that want to subscribe directly to the current state or live event slice for this source.

The MQTT contract is source-specific: MQTT/5.0 transport variant for tsunami.gov PTWC/NTWC tsunami bulletins. Non-retained QoS-1 bulletin events route by basin, tsunami bulletin level, and bulletin id under alerts/intl/ptwc/ptwc-tsunami/... Basin is derived from the NOAA feed (PHEB=pacific, PAAQ=alaska); ptwc_level is the native bulletin category normalized to lowercase.

MQTT publishes binary-mode CloudEvents with JSON payloads and CloudEvent attributes in MQTT 5 user properties. Topic patterns from `xreg/ptwc_tsunami.xreg.json`:

| Topic pattern | Message type | Delivery |
|---|---|---|
| `alerts/intl/ptwc/ptwc-tsunami/{basin}/{ptwc_level}/{bulletin_id}/bulletin` | `PTWC.TsunamiBulletin` | QoS 1, retain=false |

Four Azure Container Instance deployment shapes are documented for this source:

| Transport | Template |
|---|---|
| Kafka, bring your own Event Hub or compatible broker | `azure-template.json` |
| Kafka, create an Event Hubs namespace and hub | `azure-template-with-eventhub.json` |
| MQTT, bring your own MQTT 5 broker | `azure-template-mqtt.json` |
| MQTT, create an Azure Event Grid namespace MQTT broker | `azure-template-with-eventgrid-mqtt.json` |

See [CONTAINER.md](CONTAINER.md) for runtime environment variables and deployment badges, and [EVENTS.md](EVENTS.md) for the full CloudEvents and MQTT topic contract.
