# Xceed Nightlife Events — Container Deployment

## Overview

This container polls the [Xceed Open Event API](https://docs.xceed.me/) and forwards
European nightlife and live-entertainment event data as CloudEvents to Apache Kafka or
Azure Event Hubs.

Two event types are emitted:

- **`xceed.Event`** — Event reference data including schedule, venue, and metadata. Emitted
  at startup and refreshed periodically (default: every hour).
- **`xceed.EventAdmission`** — Ticket-availability telemetry per admission tier, including
  `is_sold_out`, `is_sales_closed`, `price`, and `remaining` count. Polled on every cycle.

All events conform to the CloudEvents 1.0 specification in structured JSON mode and are
described in [EVENTS.md](EVENTS.md).

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `CONNECTION_STRING` | **Yes** | — | Kafka or Event Hubs connection string. See formats below. |
| `KAFKA_TOPIC` | No | EntityPath from connection string | Kafka topic name override. |
| `KAFKA_ENABLE_TLS` | No | `true` | Set to `false` for plaintext local Kafka. |
| `POLLING_INTERVAL` | No | `300` | Admission polling interval in seconds. |
| `EVENT_REFRESH_INTERVAL` | No | `3600` | Event list refresh interval in seconds. |

## Connection String Formats

**Plain Kafka (local / development):**

```
BootstrapServer=localhost:9092;EntityPath=xceed
```

**Azure Event Hubs:**

```
Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy>;SharedAccessKey=<key>;EntityPath=xceed
```

**Microsoft Fabric Event Streams:**

Use the Kafka-compatible endpoint provided by your Fabric workspace.

## Docker Pull

```bash
docker pull ghcr.io/clemensv/real-time-sources-xceed:latest
```

## Running with Plain Kafka

```bash
docker run --rm \
  -e CONNECTION_STRING="BootstrapServer=localhost:9092;EntityPath=xceed" \
  -e KAFKA_ENABLE_TLS=false \
  ghcr.io/clemensv/real-time-sources-xceed:latest
```

## Running with Azure Event Hubs

```bash
docker run --rm \
  -e CONNECTION_STRING="Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=<key>;EntityPath=xceed" \
  ghcr.io/clemensv/real-time-sources-xceed:latest
```

## Customising Poll Intervals

```bash
docker run --rm \
  -e CONNECTION_STRING="BootstrapServer=localhost:9092;EntityPath=xceed" \
  -e KAFKA_ENABLE_TLS=false \
  -e POLLING_INTERVAL=120 \
  -e EVENT_REFRESH_INTERVAL=1800 \
  ghcr.io/clemensv/real-time-sources-xceed:latest
```

## Kafka Topics

| Topic | Key template | Event types |
|-------|-------------|-------------|
| `xceed` | `{event_id}` | `xceed.Event` |
| `xceed` | `{event_id}/{admission_id}` | `xceed.EventAdmission` |

Both event types are forwarded to the same Kafka topic (default: `xceed`). Consumers
can filter by CloudEvents `type` attribute to separate reference data from telemetry.

## Azure Container Instances

Deploy with the Azure CLI using the environment variables described above:

```bash
az container create \
  --resource-group <rg> \
  --name xceed-bridge \
  --image ghcr.io/clemensv/real-time-sources-xceed:latest \
  --environment-variables \
    CONNECTION_STRING="<event-hubs-connection-string>" \
  --restart-policy Always
```

## Upstream API

- Public base URL: `https://events.xceed.me/v1`
- No authentication required for the Open Event API
- Rate limits: use responsibly; no published limit
- Staging / sandbox: `https://events.staging.xceed.me/v1`
