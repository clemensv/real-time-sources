# Tokyo Docomo Bikeshare – Kafka Container

## Overview

This container polls the **Tokyo Docomo Bikeshare** GBFS 2.3 feeds published
by the [Open Data Platform for Transportation (ODPT)](https://developer-dc.odpt.org/)
and forwards them as CloudEvents to a Kafka topic.

The bridge emits three event types:

| Event type | Source feed | Update cadence |
|---|---|---|
| `JP.ODPT.DocomoBikeshare.BikeshareSystem` | `system_information.json` | Hourly |
| `JP.ODPT.DocomoBikeshare.BikeshareStation` | `station_information.json` | Hourly |
| `JP.ODPT.DocomoBikeshare.BikeshareStationStatus` | `station_status.json` | 60 s TTL |

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `CONNECTION_STRING` | yes | Kafka connection string. See formats below. |
| `KAFKA_ENABLE_TLS` | no | Set to `false` to disable TLS (default: `true`). |

## Kafka connection string formats

### Plain Kafka (no authentication)

```
CONNECTION_STRING=BootstrapServer=<host>:<port>;EntityPath=<topic>
KAFKA_ENABLE_TLS=false
```

### Azure Event Hubs

```
CONNECTION_STRING=Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<key-name>;SharedAccessKey=<key>;EntityPath=<topic>
```

## Docker pull

```bash
docker pull ghcr.io/clemensv/real-time-sources-tokyo-docomo-bikeshare:latest
```

## Docker run

### Plain Kafka

```bash
docker run --rm \
  -e CONNECTION_STRING="BootstrapServer=localhost:9092;EntityPath=tokyo-docomo-bikeshare" \
  -e KAFKA_ENABLE_TLS=false \
  ghcr.io/clemensv/real-time-sources-tokyo-docomo-bikeshare:latest
```

### Azure Event Hubs

```bash
docker run --rm \
  -e CONNECTION_STRING="Endpoint=sb://myhub.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=<key>;EntityPath=tokyo-docomo-bikeshare" \
  ghcr.io/clemensv/real-time-sources-tokyo-docomo-bikeshare:latest
```

## Kafka topic and keys

All three event types are published to the same Kafka topic specified by
`EntityPath` in the connection string.

| Event type | Kafka key |
|---|---|
| `BikeshareSystem` | `{system_id}` e.g. `docomo-cycle-tokyo` |
| `BikeshareStation` | `{system_id}/{station_id}` e.g. `docomo-cycle-tokyo/00010137` |
| `BikeshareStationStatus` | `{system_id}/{station_id}` e.g. `docomo-cycle-tokyo/00010137` |

## Event schema

See [EVENTS.md](EVENTS.md) for full CloudEvents schema details.

## Data source

- **Publisher**: Docomo Bike Share / ODPT
- **License**: ODPT open data license
- **Autodiscovery**: `https://api-public.odpt.org/api/v4/gbfs/docomo-cycle-tokyo/gbfs.json`
- **Protocol**: GBFS 2.3, no authentication required


## MQTT 5.0 / Unified Namespace

```bash
docker pull ghcr.io/clemensv/real-time-sources-tokyo-docomo-bikeshare-mqtt:latest
docker run --rm -e MQTT_BROKER_URL=mqtt://broker:1883 ghcr.io/clemensv/real-time-sources-tokyo-docomo-bikeshare-mqtt:latest
```

| Variable | Required | Default | Description |
|---|---:|---|---|
| `MQTT_BROKER_URL` | No | `mqtt://localhost:1883` | MQTT broker URL. |
| `MQTT_USERNAME` / `MQTT_PASSWORD` | No | — | Optional username/password auth. |
| `MQTT_TLS` | No | `false` | Enable TLS for broker connections. |

## AMQP 1.0

```bash
docker pull ghcr.io/clemensv/real-time-sources-tokyo-docomo-bikeshare-amqp:latest
docker run --rm -e AMQP_HOST=broker -e AMQP_ADDRESS=tokyo-docomo-bikeshare ghcr.io/clemensv/real-time-sources-tokyo-docomo-bikeshare-amqp:latest
```

| Variable | Required | Default | Description |
|---|---:|---|---|
| `AMQP_HOST` | No | `localhost` | AMQP 1.0 broker host. |
| `AMQP_PORT` | No | `5672` | AMQP 1.0 broker port. |
| `AMQP_ADDRESS` | No | `tokyo-docomo-bikeshare` | Queue/topic/address to send to. |
| `AMQP_USERNAME` / `AMQP_PASSWORD` | No | — | Optional SASL PLAIN credentials. |
