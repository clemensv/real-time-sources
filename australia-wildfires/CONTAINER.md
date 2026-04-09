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
