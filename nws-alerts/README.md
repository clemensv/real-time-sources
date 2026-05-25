# NWS CAP Weather Alerts Bridge

This bridge polls the US National Weather Service (NWS) alerts API for active
weather and non-weather alerts and forwards them to Apache Kafka, Azure Event
Hubs, Microsoft Fabric Event Streams, or MQTT 5.0 Unified Namespace brokers as
CloudEvents.

## Data Source

- API: `https://api.weather.gov/alerts/active`
- Format: GeoJSON (CAP-structured)
- Authentication: none
- Coverage: United States and territories

## Events

See [EVENTS.md](EVENTS.md) for the CloudEvents contract.

## Usage

Kafka/Event Hubs:

```bash
python -m nws_alerts --bootstrap-servers "localhost:9092" --poll-interval 120
```

Or use a connection string:

```bash
python -m nws_alerts --connection-string "<connection-string>"
```

MQTT/UNS:

```bash
python -m nws_alerts_mqtt feed --mqtt-broker-url "mqtt://localhost:1883" --once
```

MQTT topics use `alerts/us/noaa/nws-alerts/{state}/<severity>/{event_type}/{alert_id}/alert` with CAP severity baked as `minor`, `moderate`, `severe`, `extreme`, or `unknown`. Alerts are QoS 1, non-retained, binary-mode CloudEvents.

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
| `MQTT_BROKER_URL` | MQTT broker URL for `nws-alerts-mqtt` | `mqtt://localhost:1883` |
| `MQTT_AUTH_MODE` | MQTT auth mode (`anonymous`, `userpass`, `tls-cert`, `entra`) | `anonymous` |
| `MQTT_USERNAME` / `MQTT_PASSWORD` | MQTT username/password | none |
| `NWS_ALERTS_MQTT_EMIT_MOCK_CORPUS` | Emit one synthetic alert per severity for tests | `false` |

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

## MQTT and AMQP companion transports

NWS CAP alerts now ship as three isolated container images: Kafka/Event Hubs (`nws-alerts`), MQTT 5 (`nws-alerts-mqtt`), and AMQP 1.0 (`nws-alerts-amqp`). Emergency-management dashboards and notification routers can use MQTT topic filters such as `alerts/us/noaa/nws-alerts/+/severe/+/+/alert`; queue-oriented consumers can use AMQP with a broker address named `nws-alerts` by default.

| Transport | Image | Routing shape |
|---|---|---|
| Kafka/Event Hubs | `ghcr.io/clemensv/real-time-sources-nws-alerts:latest` | topic `nws-alerts`, key `{alert_id}` |
| MQTT 5 | `ghcr.io/clemensv/real-time-sources-nws-alerts-mqtt:latest` | `alerts/us/noaa/nws-alerts/{state}/{severity}/{event_type}/{alert_id}/alert` |
| AMQP 1.0 | `ghcr.io/clemensv/real-time-sources-nws-alerts-amqp:latest` | address `nws-alerts`, subject `{alert_id}` |

Deployment templates: `azure-template.json`, `azure-template-with-eventhub.json`, `azure-template-mqtt.json`, `azure-template-with-eventgrid-mqtt.json`, and `azure-template-with-servicebus.json`.

AMQP local example:

```bash
docker run --rm \
  -e AMQP_HOST=broker \
  -e AMQP_PORT=5672 \
  -e AMQP_ADDRESS=nws-alerts \
  -e AMQP_USERNAME=admin \
  -e AMQP_PASSWORD=admin \
  -e AMQP_AUTH_MODE=password \
  ghcr.io/clemensv/real-time-sources-nws-alerts-amqp:latest
```
