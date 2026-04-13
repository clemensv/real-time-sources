# Fienta Public Events Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between the [Fienta](https://fienta.com) public events API and Apache Kafka, Azure Event Hubs, and Fabric Event Streams. The bridge polls public ticketed events across Europe and forwards event metadata and sale-status changes to the configured Kafka topic.

## Fienta API

[Fienta](https://fienta.com) is a European event ticketing platform primarily serving Estonia, Latvia, Lithuania, and other European markets. The public events API at `https://fienta.com/api/v1/public/events` returns all publicly listed events without requiring authentication. Events include sale-status signals such as `onSale`, `soldOut`, `notOnSale`, and `saleEnded`, making the feed useful for downstream analytics on event popularity and demand.

## Functionality

The bridge polls the Fienta public events API every 5 minutes and writes events to a Kafka topic as [CloudEvents](https://cloudevents.io/) in JSON format, documented in [EVENTS.md](EVENTS.md).

At startup, the bridge emits full `Event` reference data for all currently listed public events, then enters the polling loop. On each poll:

1. **Reference data refresh** — Every hour, all `Event` records are re-emitted so consumers can maintain a current view of event metadata (name, location, organizer, schedule).
2. **Sale-status telemetry** — `EventSaleStatus` events are emitted whenever the `sale_status` of an event changes since the last poll. Previously seen statuses are tracked in a state file to prevent duplicate emission.

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-fienta:latest
```

To use it as a base image in a Dockerfile:

```dockerfile
FROM ghcr.io/clemensv/real-time-sources-fienta:latest
```

## Using the Container Image

The container starts the bridge, polling the Fienta API and writing events to Kafka, Azure Event Hubs, or Fabric Event Streams.

### With a Kafka Broker

```shell
$ docker run --rm \
    -e CONNECTION_STRING="BootstrapServer=mybroker:9092;EntityPath=fienta" \
    -e KAFKA_ENABLE_TLS=false \
    ghcr.io/clemensv/real-time-sources-fienta:latest
```

### With Azure Event Hubs

```shell
$ docker run --rm \
    -e CONNECTION_STRING="Endpoint=sb://mynamespace.servicebus.windows.net/;SharedAccessKeyName=send;SharedAccessKey=<key>;EntityPath=fienta" \
    ghcr.io/clemensv/real-time-sources-fienta:latest
```

### With Microsoft Fabric Event Streams

```shell
$ docker run --rm \
    -e CONNECTION_STRING="<Fabric Event Stream connection string>" \
    ghcr.io/clemensv/real-time-sources-fienta:latest
```

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `CONNECTION_STRING` | Yes | Kafka/Event Hubs/Fabric connection string |
| `KAFKA_ENABLE_TLS` | No | Set to `false` to disable TLS (default: `true`) |
| `FIENTA_STATE_FILE` | No | Path to state file for sale-status deduplication (default: `/mnt/fileshare/fienta_state.json`) |

## Azure Container Instance Deployment

```shell
$ az container create \
    --resource-group myResourceGroup \
    --name fienta-bridge \
    --image ghcr.io/clemensv/real-time-sources-fienta:latest \
    --environment-variables \
        CONNECTION_STRING="<connection-string>" \
    --restart-policy Always
```
