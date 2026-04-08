# Madrid Real-Time Traffic (Informo) Container

This container is a bridge between Madrid's Informo real-time traffic sensor system and Apache Kafka endpoints. It polls the Informo pm.xml feed and emits traffic sensor reference data and telemetry readings as CloudEvents.

All events are structured CloudEvents. See [EVENTS.md](EVENTS.md) for the event schemas.

## Docker

Pull the container image:

```bash
docker pull ghcr.io/clemensv/real-time-sources/madrid-traffic:latest
```

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `CONNECTION_STRING` | Yes | Kafka or Azure Event Hubs connection string |
| `KAFKA_ENABLE_TLS` | No | Set to `false` to disable TLS (default: `true`) |

### Connection String Formats

**Plain Kafka:**
```
BootstrapServer=mybroker:9092;EntityPath=madrid-traffic
```

**Azure Event Hubs:**
```
Endpoint=sb://mynamespace.servicebus.windows.net/;SharedAccessKeyName=send;SharedAccessKey=...;EntityPath=madrid-traffic
```

**Microsoft Fabric Event Stream:**
Use the Fabric-provided connection string.

## Running

### Plain Kafka (no TLS)

```bash
docker run --rm \
  -e CONNECTION_STRING="BootstrapServer=mybroker:9092;EntityPath=madrid-traffic" \
  -e KAFKA_ENABLE_TLS=false \
  ghcr.io/clemensv/real-time-sources/madrid-traffic:latest
```

### Azure Event Hubs

```bash
docker run --rm \
  -e CONNECTION_STRING="Endpoint=sb://mynamespace.servicebus.windows.net/;SharedAccessKeyName=send;SharedAccessKey=XXXX;EntityPath=madrid-traffic" \
  ghcr.io/clemensv/real-time-sources/madrid-traffic:latest
```

## Azure Container Instance

Deploy with the Azure CLI:

```bash
az container create \
  --resource-group mygroup \
  --name madrid-traffic-bridge \
  --image ghcr.io/clemensv/real-time-sources/madrid-traffic:latest \
  --environment-variables \
    CONNECTION_STRING="Endpoint=sb://..." \
  --restart-policy Always
```
