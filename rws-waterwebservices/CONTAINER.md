# Container Deployment

## Build

```bash
docker build -t rws-waterwebservices .
```

## Run

```bash
docker run -e CONNECTION_STRING="Endpoint=sb://..." rws-waterwebservices
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `CONNECTION_STRING` | Yes* | Azure Event Hubs connection string |
| `KAFKA_BOOTSTRAP_SERVERS` | Yes* | Kafka bootstrap servers |
| `KAFKA_TOPIC` | Yes* | Kafka topic name |
| `SASL_USERNAME` | Yes* | SASL username |
| `SASL_PASSWORD` | Yes* | SASL password |
| `POLLING_INTERVAL` | No | Polling interval in seconds (default: 600) |

*Either `CONNECTION_STRING` or the combination of `KAFKA_BOOTSTRAP_SERVERS`, `KAFKA_TOPIC`, `SASL_USERNAME`, and `SASL_PASSWORD` must be provided.

## Azure Deployment

Deploy using the Azure Resource Manager template:

```bash
az deployment group create \
    --resource-group <resource-group> \
    --template-file azure-template.json \
    --parameters eventHubConnectionString="<connection-string>"
```
