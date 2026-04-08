# French Road Traffic — Container

## Summary

This container bridges real-time traffic data from the French national
non-conceded road network (published by Bison Futé / TIPI via DATEX II XML
feeds) into Apache Kafka as CloudEvents.

Two DATEX II endpoints are polled:

| Feed | Endpoint | CloudEvents type |
|------|----------|-----------------|
| Traffic flow (vehicle counts & speeds) | `QTV-DIR/qtvDir.xml` | `fr.gouv.transport.bison_fute.TrafficFlowMeasurement` |
| Road events (incidents, works, closures) | `Evenementiel-DIR/grt/RRN/content.xml` | `fr.gouv.transport.bison_fute.RoadEvent` |

Events are emitted as structured CloudEvents in JSON format.
See [EVENTS.md](EVENTS.md) for schema details.

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `CONNECTION_STRING` | Yes (or individual vars) | — | Event Hubs / Fabric / plain Kafka connection string |
| `KAFKA_BOOTSTRAP_SERVERS` | If no `CONNECTION_STRING` | — | Kafka bootstrap servers |
| `KAFKA_TOPIC_FLOW` | No | `french-road-traffic-flow` | Topic for traffic flow measurements |
| `KAFKA_TOPIC_EVENTS` | No | `french-road-traffic-events` | Topic for road events |
| `SASL_USERNAME` | No | — | SASL username |
| `SASL_PASSWORD` | No | — | SASL password |
| `KAFKA_ENABLE_TLS` | No | `true` | Set to `false` to disable TLS |
| `POLLING_INTERVAL` | No | `360` | Polling interval in seconds |

## Docker

```bash
docker pull ghcr.io/clemensv/real-time-sources-french-road-traffic:latest
```

### Plain Kafka

```bash
docker run --rm \
  -e CONNECTION_STRING="BootstrapServer=localhost:9092;EntityPath=french-road-traffic" \
  -e KAFKA_ENABLE_TLS=false \
  ghcr.io/clemensv/real-time-sources-french-road-traffic:latest
```

### Azure Event Hubs

```bash
docker run --rm \
  -e CONNECTION_STRING="Endpoint=sb://myhub.servicebus.windows.net/;SharedAccessKeyName=send;SharedAccessKey=...;EntityPath=french-road-traffic" \
  ghcr.io/clemensv/real-time-sources-french-road-traffic:latest
```

### Microsoft Fabric Event Stream

```bash
docker run --rm \
  -e CONNECTION_STRING="Endpoint=sb://....servicebus.windows.net/;SharedAccessKeyName=...;SharedAccessKey=...;EntityPath=..." \
  ghcr.io/clemensv/real-time-sources-french-road-traffic:latest
```

## Azure Container Instance

Deploy via the Azure template in `azure-template.json` or using the Azure CLI:

```bash
az container create \
  --resource-group mygroup \
  --name french-road-traffic \
  --image ghcr.io/clemensv/real-time-sources-french-road-traffic:latest \
  --environment-variables \
    CONNECTION_STRING="..." \
  --restart-policy Always
```

## Data Source

- **Portal**: <https://transport.data.gouv.fr/datasets?type=road-data>
- **Licence**: Licence Ouverte 2.0 (French Open Data licence)
- **Update frequency**: Snapshots every ~6 minutes
- **Coverage**: French national non-conceded road network
