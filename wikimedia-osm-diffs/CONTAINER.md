# OpenStreetMap Minutely Diffs bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image bridges the OpenStreetMap minutely replication diff
feed into Apache Kafka, Azure Event Hubs, and Microsoft Fabric Event
Streams as CloudEvents.

## OpenStreetMap Minutely Diffs

OpenStreetMap publishes minutely replication diff files that capture every
edit to the global map database. Each diff is a gzip-compressed OsmChange
XML document containing create, modify, and delete operations on nodes,
ways, and relations. The bridge polls the state file to detect new
sequences, downloads and parses the diffs, and emits individual element
changes as CloudEvents.

- **State endpoint**: `https://planet.openstreetmap.org/replication/minute/state.txt`
- **Diff files**: `https://planet.openstreetmap.org/replication/minute/NNN/NNN/NNN.osc.gz`
- **Protocol**: HTTP polling, gzip-compressed OsmChange XML
- **Authentication**: None
- **License**: ODbL 1.0

## Functionality

The bridge polls the replication state file every 60 seconds, detects new
sequence numbers, downloads the corresponding diff files, decompresses and
parses the OsmChange XML, and emits events as documented in
[EVENTS.md](EVENTS.md).

## Installing the Container Image

Pull the image from GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-wikimedia-osm-diffs:latest
```

## Using the Container Image

### With Azure Event Hubs or Fabric Event Streams

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-wikimedia-osm-diffs:latest
```

### With a Kafka Broker

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-wikimedia-osm-diffs:latest
```

### With Plain Kafka for Docker E2E

```shell
$ docker run --rm \
    -e CONNECTION_STRING='BootstrapServer=host:9092;EntityPath=wikimedia-osm-diffs' \
    -e KAFKA_ENABLE_TLS='false' \
    ghcr.io/clemensv/real-time-sources-wikimedia-osm-diffs:latest
```

## Environment Variables

### `CONNECTION_STRING`

Event Hubs / Fabric style connection string. If set, it overrides the
explicit Kafka arguments.

### `KAFKA_BOOTSTRAP_SERVERS`

Comma-separated Kafka bootstrap servers.

### `KAFKA_TOPIC`

Kafka topic name. Default in the manifest is `wikimedia-osm-diffs`.

### `SASL_USERNAME`

SASL PLAIN username for Kafka authentication.

### `SASL_PASSWORD`

SASL PLAIN password for Kafka authentication.

### `KAFKA_ENABLE_TLS`

Set to `false` for plain Kafka. Default: `true`.

### `OSM_DIFFS_STATE_FILE`

Path to the local state file used for tracking the last processed
sequence number. Default: `~/.wikimedia_osm_diffs_state.json`.

### `OSM_DIFFS_POLL_INTERVAL`

Polling interval in seconds. Default: `60`.

### `OSM_DIFFS_MAX_RETRY_DELAY`

Maximum retry backoff in seconds. Default: `120`.

### `OSM_DIFFS_USER_AGENT`

HTTP `User-Agent` header sent to the OSM server.

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwikimedia-osm-diffs%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwikimedia-osm-diffs%2Fazure-template-with-eventhub.json)


---

## MQTT/UNS variant (`Dockerfile.mqtt`)

The `wikimedia-osm-diffs-mqtt` image (built from `Dockerfile.mqtt`) is a
separate firehose variant of the bridge that publishes MQTT 5.0
binary-mode CloudEvents into a Unified-Namespace topic tree on a broker
of your choice. The minutely diff stream is split into three
non-retained QoS-0 families (one per OSM element type) plus a single
retained side-channel snapshot for the OSM replication state.

### Topic tree

```
osm/intl/wikimedia/wikimedia-osm-diffs/node/{geohash5}/{element_id}/change            # firehose, retain=false, QoS 0
osm/intl/wikimedia/wikimedia-osm-diffs/way/{geohash5}/{element_id}/change             # firehose, retain=false, QoS 0
osm/intl/wikimedia/wikimedia-osm-diffs/relation/{geohash5}/{element_id}/change        # firehose, retain=false, QoS 0
osm/intl/wikimedia/wikimedia-osm-diffs/replication-state/replication-state            # retained, QoS 0
```

The `{geohash5}` placeholder is the lowercase 5-character base32 geohash
of the element's coordinates. OSM ways and relations do not carry inline
coordinates in OsmChange, so `{geohash5}` is the fixed sentinel
`nogeo` for those families. `{element_id}` is the stringified OSM
element id.

### Example wildcard subscriptions

```
# all map changes in a 5-char geohash cell (e.g. `u281`)
osm/intl/wikimedia/wikimedia-osm-diffs/+/u281+/+/change

# all way edits anywhere
osm/intl/wikimedia/wikimedia-osm-diffs/way/+/+/change

# all relation deletes/modifies/creates anywhere (no coords -> nogeo)
osm/intl/wikimedia/wikimedia-osm-diffs/relation/nogeo/+/change

# every change for a known node id 1234567890
osm/intl/wikimedia/wikimedia-osm-diffs/node/+/1234567890/change

# replication-state snapshot (retained)
osm/intl/wikimedia/wikimedia-osm-diffs/replication-state/#
```

### Environment variables

| Variable | Default | Notes |
| --- | --- | --- |
| `MQTT_BROKER_URL` | `mqtt://localhost:1883` | `mqtt://` or `mqtts://`. |
| `MQTT_ENABLE_TLS` | `false` | Forces TLS even when `mqtt://` is used. |
| `MQTT_USERNAME` | _(unset)_ | Optional MQTT username. |
| `MQTT_PASSWORD` | _(unset)_ | Optional MQTT password. |
| `MQTT_CLIENT_ID` | _(auto)_ | Optional MQTT client id. |
| `OSM_DIFFS_STATE_URL` | `https://planet.openstreetmap.org/replication/minute/state.txt` | OSM replication state endpoint. |
| `OSM_DIFFS_BASE_URL` | `https://planet.openstreetmap.org/replication/minute` | OSM replication diff base URL. |
| `OSM_DIFFS_STATE_FILE` | `~/.wikimedia_osm_diffs_mqtt_state.json` | Local state file to remember the last processed sequence. |
| `OSM_DIFFS_POLL_INTERVAL` | `60` | Seconds between polls. |
| `OSM_DIFFS_ONCE` | `false` | Process a single polling cycle and exit. |
| `OSM_DIFFS_MOCK` | `false` | Skip OSM polling, emit one synthetic change per family + replication-state, then exit (used by Docker E2E). |

### Run

```bash
docker run --rm \
  -e MQTT_BROKER_URL=mqtt://broker:1883 \
  ghcr.io/clemensv/real-time-sources/wikimedia-osm-diffs-mqtt:latest
```

CloudEvents ride as MQTT 5.0 binary-mode user properties (`id`,
`source`, `type`, `subject`, `time`, `specversion`); the payload is the
JSON-serialized `MapChange` / `ReplicationState` dataclass and the MQTT
`Content-Type` is set to `application/json`.
