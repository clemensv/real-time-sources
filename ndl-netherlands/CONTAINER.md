# NDW Netherlands Road Traffic bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image bridges the NDW (Nationaal Dataportaal Wegverkeer)
open data feeds at `https://opendata.ndw.nu` to Apache Kafka, Azure Event Hubs,
and Fabric Event Streams. It downloads gzip-compressed DATEX II XML files
containing traffic speed measurements, travel times, and current traffic
situations from the entire Dutch road network, and emits them as CloudEvents.

Events are emitted in CloudEvents structured JSON format. See [EVENTS.md](EVENTS.md)
for the full event catalog.

## Topics

| Topic | Key | Content |
|---|---|---|
| `ndl-traffic` | `{site_id}` | Speed and travel time per measurement site |
| `ndl-traffic-situations` | `{situation_id}` | Road works, closures, incidents |

## Environment variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `CONNECTION_STRING` | **Yes** | — | Kafka or Event Hubs connection string |
| `KAFKA_ENABLE_TLS` | No | `true` | Set to `false` for plain Kafka |
| `KAFKA_TOPIC` | No | `ndl-traffic` | Override measurements topic |
| `MEASUREMENTS_TOPIC` | No | `ndl-traffic` | Override measurements topic |
| `SITUATIONS_TOPIC` | No | `ndl-traffic-situations` | Override situations topic |
| `POLLING_INTERVAL` | No | `60` | Seconds between poll cycles |
| `STATE_FILE` | No | `~/.ndl_netherlands_state.json` | Dedup state persistence |

## Docker

```bash
docker pull ghcr.io/clemensv/real-time-sources/ndl-netherlands:latest
```

### Plain Kafka

```bash
docker run --rm \
  -e CONNECTION_STRING="BootstrapServer=localhost:9092;EntityPath=ndl-traffic" \
  -e KAFKA_ENABLE_TLS=false \
  ghcr.io/clemensv/real-time-sources/ndl-netherlands:latest
```

### Azure Event Hubs

```bash
docker run --rm \
  -e CONNECTION_STRING="Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy>;SharedAccessKey=<key>;EntityPath=ndl-traffic" \
  ghcr.io/clemensv/real-time-sources/ndl-netherlands:latest
```

### Azure Container Instance

```bash
az container create \
  --resource-group myRG \
  --name ndl-netherlands \
  --image ghcr.io/clemensv/real-time-sources/ndl-netherlands:latest \
  --restart-policy Always \
  --environment-variables \
    CONNECTION_STRING="Endpoint=sb://..." \
    POLLING_INTERVAL=60
```
