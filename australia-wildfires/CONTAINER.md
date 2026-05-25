# Australian State Wildfires Bridge — Container

This container bridges live bushfire incident data from three Australian state
emergency services — NSW Rural Fire Service, VicEmergency, and Queensland Fire
Department — into Kafka endpoints as CloudEvents.

All events are emitted as [CloudEvents](https://cloudevents.io/) in structured
JSON content mode. See [EVENTS.md](EVENTS.md) for the full event catalog.

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `CONNECTION_STRING` | Yes | Kafka or Event Hubs connection string |
| `KAFKA_TOPIC` | No | Override the default topic (`australia-wildfires`) |
| `POLLING_INTERVAL` | No | Polling interval in seconds (default: `300`) |
| `STATE_FILE` | No | Path for dedup state persistence (default: `~/.australia_wildfires_state.json`) |
| `KAFKA_ENABLE_TLS` | No | Enable TLS for Kafka connections (default: `true`) |
| `MQTT_BROKER_URL` | MQTT only | MQTT broker URL such as `mqtt://broker:1883` or `mqtts://broker:8883` |
| `MQTT_USERNAME` / `MQTT_PASSWORD` | MQTT only | Optional MQTT credentials |
| `MQTT_CONTENT_MODE` | MQTT only | CloudEvents MQTT content mode (`binary`, default, or `structured`) |
| `AUSTRALIA_WILDFIRES_SAMPLE_MODE` | MQTT test only | Publish one deterministic sample incident instead of polling live feeds |

## Connection Strings

### Plain Kafka

```
BootstrapServer=myhost:9092;EntityPath=australia-wildfires
```

### Azure Event Hubs

```
Endpoint=sb://mynamespace.servicebus.windows.net/;SharedAccessKeyName=send;SharedAccessKey=...;EntityPath=australia-wildfires
```

### Microsoft Fabric Event Streams

Use the Event Hubs–compatible connection string from your Fabric workspace.

## Docker

### Pull

```bash
docker pull ghcr.io/clemensv/real-time-sources/australia-wildfires:latest
```

### Run

```bash
docker run --rm \
  -e CONNECTION_STRING="BootstrapServer=host.docker.internal:9092;EntityPath=australia-wildfires" \
  ghcr.io/clemensv/real-time-sources/australia-wildfires:latest
```

### MQTT/UNS image

```bash
docker build -f Dockerfile.mqtt -t australia-wildfires-mqtt .
docker run --rm \
  -e MQTT_BROKER_URL="mqtt://host.docker.internal:1883" \
  ghcr.io/clemensv/real-time-sources/australia-wildfires-mqtt:latest
```

The MQTT image publishes QoS 1, non-retained binary CloudEvents under
`wildfire/au/{state}/{status}/{incident_id}/incident`.

## Azure Container Instance

Deploy with the Azure CLI:

```bash
az container create \
  --resource-group myRG \
  --name australia-wildfires \
  --image ghcr.io/clemensv/real-time-sources/australia-wildfires:latest \
  --environment-variables CONNECTION_STRING="<your-connection-string>" \
  --restart-policy Always
```

## Database Follow-On

Ingest the Kafka topic into Azure Data Explorer or Fabric KQL Database and
query incidents with KQL:

```kql
['australia-wildfires']
| extend data = parse_json(tostring(data))
| project
    incident_id = tostring(data.incident_id),
    state = tostring(data.state),
    title = tostring(data.title),
    alert_level = tostring(data.alert_level),
    latitude = todouble(data.latitude),
    longitude = todouble(data.longitude),
    size_hectares = todouble(data.size_hectares),
    type = tostring(data.type),
    updated = todatetime(data.updated)
| order by updated desc
```

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faustralia-wildfires%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faustralia-wildfires%2Fazure-template-with-eventhub.json)


## AMQP 1.0 container

The AMQP companion image publishes Australian Wildfires CloudEvents to a single broker address. It supports SASL PLAIN for generic AMQP 1.0 brokers and CBS token authentication for Azure Service Bus (`AMQP_AUTH_MODE=entra` for managed identity, `AMQP_AUTH_MODE=sas` for emulator/SAS-key scenarios).

```bash
docker pull ghcr.io/clemensv/real-time-sources-australia-wildfires-amqp:latest

docker run --rm   -e AMQP_BROKER_URL=amqp://user:password@broker:5672/australia-wildfires   -e AUSTRALIA_WILDFIRES_SAMPLE_MODE=true ONCE_MODE=true   ghcr.io/clemensv/real-time-sources-australia-wildfires-amqp:latest
```

### AMQP environment variables

| Variable | Description | Default |
|---|---|---|
| `AMQP_BROKER_URL` | Full `amqp://` or `amqps://` URL. Path overrides `AMQP_ADDRESS`. | empty |
| `AMQP_HOST` / `AMQP_PORT` | Broker host and port when no URL is supplied. | `localhost` / 5672 or 5671 |
| `AMQP_ADDRESS` | Queue, topic, or link target address. | `australia-wildfires` |
| `AMQP_USERNAME` / `AMQP_PASSWORD` | SASL PLAIN credentials for generic brokers. | empty |
| `AMQP_TLS` | Force TLS for generic brokers. | `false` |
| `AMQP_CONTENT_MODE` | CloudEvents AMQP binding mode: `binary` or `structured`. | `binary` |
| `AMQP_AUTH_MODE` | `password`, `entra`, or `sas`. | `password` |
| `AMQP_ENTRA_AUDIENCE` | Token scope for CBS/Entra authentication. | `https://servicebus.azure.net/.default` |
| `AMQP_ENTRA_CLIENT_ID` | User-assigned managed identity client id. | empty |
| `AMQP_SAS_KEY_NAME` / `AMQP_SAS_KEY` | SAS key credentials for Service Bus emulator/SAS CBS. | empty |

### Deploy to Azure Service Bus

This template creates a Service Bus namespace and queue, user-assigned managed identity, role assignment for Azure Service Bus Data Sender, Log Analytics workspace, storage file share for state, and an Azure Container Instance running the AMQP image.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faustralia-wildfires%2Finfra%2Fazure-template-amqp.json)
