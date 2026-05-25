# Mode-S/ADS-B Aircraft Telemetry Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between a local [dump1090](https://github.com/flightaware/dump1090) ADS-B receiver and Apache Kafka, Azure Event Hubs, and Fabric Event Streams. The bridge connects to your dump1090 instance via the BEAST protocol, decodes raw Mode-S/ADS-B messages from aircraft broadcasting on 1090 MHz, and forwards structured aircraft telemetry to the configured Kafka endpoint.

## Mode-S/ADS-B Data

ADS-B (Automatic Dependent Surveillance-Broadcast) is a surveillance technology where aircraft broadcast their position, altitude, speed, and identification. You receive these signals with an inexpensive RTL-SDR USB dongle and an antenna, decoded by [dump1090](https://github.com/flightaware/dump1090). The easiest way to get started is [PiAware](https://flightaware.com/adsb/piaware/install) on a Raspberry Pi.

The bridge reads from dump1090's BEAST output (TCP port 30005 by default), decodes the raw messages, and bundles them into batches flushed every second or after 1,000 records.

## Functionality

The bridge connects to a dump1090 instance via the BEAST binary protocol, decodes aircraft telemetry (position, altitude, speed, heading, callsign, vertical rate), and writes batched messages to a Kafka topic as [CloudEvents](https://cloudevents.io/) in JSON format, documented in [EVENTS.md](EVENTS.md).

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a database, the integration with Fabric Eventhouse and Azure Data Explorer is described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-mode-s:latest
```

## Using the Container Image

### With Azure Event Hubs or Fabric Event Streams

```shell
$ docker run --rm \
    -e DUMP1090_HOST='<dump1090-host-ip>' \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-mode-s:latest
```

### With a Kafka Broker

```shell
$ docker run --rm \
    -e DUMP1090_HOST='<dump1090-host-ip>' \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-mode-s:latest
```

### With Antenna Reference Position

Provide your antenna's coordinates for accurate distance and bearing calculations:

```shell
$ docker run --rm \
    -e DUMP1090_HOST='<dump1090-host-ip>' \
    -e REF_LAT='52.3676' \
    -e REF_LON='4.9041' \
    -e STATIONID='amsterdam-01' \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-mode-s:latest
```

## Environment Variables

### `DUMP1090_HOST`

Host or IP address of the dump1090 instance. Default: `localhost`.

### `DUMP1090_PORT`

TCP port for the BEAST binary output of dump1090. Default: `30005`.

### `REF_LAT`

Latitude of the receiving antenna, used for position calculations. Default: `0`.

### `REF_LON`

Longitude of the receiving antenna, used for position calculations. Default: `0`.

### `STATIONID`

Identifier for this receiving station, used as the CloudEvent source. Default: `station1`.

### `CONNECTION_STRING`

An Azure Event Hubs-style connection string used to connect to Azure Event Hubs or Fabric Event Streams.

### `KAFKA_BOOTSTRAP_SERVERS`

The address of the Kafka broker. Provide a comma-separated list of host and port pairs.

### `KAFKA_TOPIC`

The Kafka topic where messages will be produced.

### `SASL_USERNAME`

Username for SASL PLAIN authentication.

### `SASL_PASSWORD`

Password for SASL PLAIN authentication.

### `POLLING_INTERVAL`

Polling interval in seconds. Default: `60`.

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fmode-s%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fmode-s%2Fazure-template-with-eventhub.json)


---

## MQTT 5.0 / Unified-Namespace feeder

A second container image, built from `Dockerfile.mqtt`, publishes each decoded Mode-S record to an MQTT 5.0 broker on a Unified-Namespace (UNS) topic tree. The Kafka image and contract are unchanged.

### Topic template

```
aviation/intl/mode-s/mode-s/{icao24}/{receiver_id}/{msg_type}
```

* `{icao24}` – ICAO 24-bit address (lowercase hex)
* `{receiver_id}` – stable id of the decoding station
* `{msg_type}` – Downlink Format family literal: `df17-adsb`, `df4-altitude`, `df5-identity`, `df11-acquisition`, `df20-comm-b`, `df21-comm-b`

Non-retained firehose: every publish is **QoS 0** with `retain=false`. Subscribers must be attached before the feeder starts. CloudEvents binary mode – CE attributes (`id`, `source`, `type`, `subject`, `time`, `specversion`) ride as MQTT 5 user properties. `ContentType=application/json`. `subject` equals the ICAO 24-bit address.

### Pull & run

```bash
docker pull ghcr.io/clemensv/real-time-sources/mode-s-mqtt:latest

docker run --rm -e MQTT_BROKER_URL=mqtt://broker:1883 \
  ghcr.io/clemensv/real-time-sources/mode-s-mqtt:latest
```

### Environment variables

| Variable | Purpose |
|----------|---------|
| `MQTT_BROKER_URL` | `mqtt://host:port` or `mqtts://host:port` |
| `MQTT_USERNAME` / `MQTT_PASSWORD` | Optional broker credentials |
| `MQTT_ENABLE_TLS` | `true` to force TLS (auto if scheme is `mqtts://`) |
| `MODE_S_DUMP1090_HOST` / `MODE_S_DUMP1090_PORT` | dump1090 Beast TCP endpoint (default `localhost:30005`) |
| `MODE_S_RECEIVER_ID` | Stable receiver identifier baked into the topic axis |
| `MODE_S_REF_LAT` / `MODE_S_REF_LON` | Reference position for local CPR decoding |
| `MODE_S_MOCK` | `true` to emit one canned record per DF family then exit (used by Docker E2E) |

### Subscribe examples

```bash
# All Mode-S traffic
mosquitto_sub -h broker -t 'aviation/intl/mode-s/#'
# All ADS-B from one airframe
mosquitto_sub -h broker -t 'aviation/intl/mode-s/mode-s/4ca7b8/+/df17-adsb'
```


## AMQP 1.0 companion feeder

Pull and run the AMQP image:

```bash
docker pull ghcr.io/clemensv/real-time-sources-mode-s-amqp:latest
docker run --rm \
  -e AMQP_HOST=broker \
  -e AMQP_PORT=5672 \
  -e AMQP_ADDRESS=mode-s \
  -e AMQP_USERNAME=user \
  -e AMQP_PASSWORD=secret \
  -e AMQP_AUTH_MODE=password \
  -e MODE_S_MOCK=true \
  ghcr.io/clemensv/real-time-sources-mode-s-amqp:latest
```

For Azure Service Bus, set `AMQP_AUTH_MODE=entra`, `AMQP_HOST=<namespace>.servicebus.windows.net`, `AMQP_PORT=5671`, `AMQP_TLS=true`, and optionally `AMQP_ENTRA_CLIENT_ID` for a user-assigned managed identity. For the Service Bus emulator or SAS-only namespaces, use `AMQP_AUTH_MODE=sas` with `AMQP_SAS_KEY_NAME` and `AMQP_SAS_KEY`.

| Variable | Description | Default |
|---|---|---|
| `AMQP_BROKER_URL` | Optional full AMQP URL; path overrides `AMQP_ADDRESS`. | empty |
| `AMQP_HOST` / `AMQP_PORT` | Broker host and port. | localhost / 5672 |
| `AMQP_ADDRESS` | Queue/topic/event-hub name. | `mode-s` |
| `AMQP_USERNAME` / `AMQP_PASSWORD` | SASL PLAIN credentials for generic brokers. | empty |
| `AMQP_AUTH_MODE` | `password`, `entra`, or `sas`. | `password` |
| `AMQP_TLS` | Enable TLS for AMQP. | false (`entra` implies TLS) |
| `AMQP_CONTENT_MODE` | CloudEvents content mode. | `binary` |
| `AMQP_ENTRA_AUDIENCE` | Token audience for CBS. | `https://servicebus.azure.net/.default` |
| `AMQP_ENTRA_CLIENT_ID` | User-assigned managed identity client id. | empty |
| `AMQP_SAS_KEY_NAME` / `AMQP_SAS_KEY` | SAS CBS credentials. | empty |

Deploy a new Service Bus queue plus managed identity with [`azure-template-with-servicebus.json`](azure-template-with-servicebus.json) or [`infra/azure-template-amqp.json`](infra/azure-template-amqp.json).
