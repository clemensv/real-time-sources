# Nextbus Bridge to Azure Event Hubs and Fabric Event Streams

This container polls the [Nextbus/UMOIQ](https://retro.umoiq.com/) public XML feed and emits real-time transit vehicle positions, route configurations, schedules, and service messages to Azure Event Hubs or Fabric Event Streams as CloudEvents JSON.

You must accept the [Nextbus Terms of Use](https://www.nextbus.com/xmlFeedDocs/NextBusXMLFeed.pdf) to use this container.

## Upstream

- **Publisher:** Nextbus / UMOIQ
- **API endpoint:** `https://retro.umoiq.com/service/publicXMLFeed`
- **Products:** Real-time vehicle positions, route configs, schedules, service messages
- **Auth:** None (public feed)
- **License:** See [Nextbus Terms of Use](https://www.nextbus.com/xmlFeedDocs/NextBusXMLFeed.pdf)

## Events

Events emitted by this bridge are described in [EVENTS.md](EVENTS.md).

## Behavior

The bridge runs a continuous polling loop for vehicle positions (default every 10 seconds) and optionally emits reference data (route configurations, schedules, and service messages) to a separate Event Hub every hour. The bridge deduplicates vehicle positions by last-report timestamp per vehicle and checksums reference payloads to skip unchanged data.

## Installing the Container Image

```bash
docker pull ghcr.io/clemensv/real-time-sources-nextbus:latest
```

## Running the Container

### Azure Event Hubs (feed only)

```bash
docker run --rm \
  -e FEED_CONNECTION_STRING="Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy>;SharedAccessKey=<key>;EntityPath=<feed-hub>" \
  -e FEED_EVENT_HUB_NAME="<feed-hub>" \
  -e AGENCY="ttc" \
  ghcr.io/clemensv/real-time-sources-nextbus:latest
```

### Azure Event Hubs (feed + reference data)

```bash
docker run --rm \
  -e FEED_CONNECTION_STRING="Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy>;SharedAccessKey=<key>;EntityPath=<feed-hub>" \
  -e FEED_EVENT_HUB_NAME="<feed-hub>" \
  -e REFERENCE_CONNECTION_STRING="Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy>;SharedAccessKey=<key>;EntityPath=<reference-hub>" \
  -e REFERENCE_EVENT_HUB_NAME="<reference-hub>" \
  -e AGENCY="ttc" \
  ghcr.io/clemensv/real-time-sources-nextbus:latest
```

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `FEED_CONNECTION_STRING` | Yes | — | Azure Event Hubs connection string for vehicle position events. Format: `Endpoint=sb://<ns>.servicebus.windows.net/;SharedAccessKeyName=<policy>;SharedAccessKey=<key>;EntityPath=<hub>` |
| `FEED_EVENT_HUB_NAME` | Yes | — | Name of the Event Hub receiving vehicle position events |
| `REFERENCE_CONNECTION_STRING` | No | — | Connection string for the reference Event Hub. When set, route configs, schedules, and messages are also emitted. May be identical to `FEED_CONNECTION_STRING` |
| `REFERENCE_EVENT_HUB_NAME` | No | — | Name of the Event Hub receiving reference data events |
| `AGENCY` | Yes | — | Nextbus agency tag (e.g. `ttc` for Toronto Transit Commission). Use `docker run ... nextbus agencies` to list available tags |
| `ROUTE` | No | `*` | Route tag to poll. Defaults to `*` (all routes) |
| `POLL_INTERVAL` | No | `10` | Polling interval in seconds for vehicle positions |
| `BACKOFF_INTERVAL` | No | `0` | Seconds to wait between requests when fetching reference data per route |

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnextbus%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnextbus%2Fazure-template-with-eventhub.json)
