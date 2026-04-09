# German Autobahn Traffic bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image bridges the German Autobahn API at
`https://verkehr.autobahn.de/o/autobahn` to Apache Kafka, Azure Event Hubs,
and Fabric Event Streams. It polls current roadworks, warnings, closures,
entry and exit closures, weight-limit restrictions, lorry parking metadata,
electric charging station metadata, and webcam metadata and emits CloudEvents
documented in [EVENTS.md](EVENTS.md).

## Functionality

The upstream API serves current-state snapshots, not a change feed. The bridge
uses ETags per road and resource where possible and keeps a local state file to
detect newly appeared, updated, and resolved items. Event families are split by
resource schema and, where relevant, by `display_type` so short-term roadworks,
entry and exit closures, and strong charging stations remain distinguishable in
the output stream.

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a
database, the integration with Fabric Eventhouse and Azure Data Explorer is
described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-autobahn:latest
```

## Using the Container Image

Run the bridge against a Kafka broker:

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='broker:9092' \
    -e KAFKA_TOPIC='autobahn' \
    -e KAFKA_ENABLE_TLS='false' \
    ghcr.io/clemensv/real-time-sources-autobahn:latest
```

Or use an Event Hubs or Fabric Event Streams connection string:

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-autobahn:latest
```

To preserve ETags and last-seen snapshots across restarts, mount a writable
volume and point the bridge at a state file on that volume:

```shell
$ docker run --rm \
    -v /path/to/state:/mnt/fileshare \
    -e AUTOBAHN_STATE_FILE='/mnt/fileshare/autobahn_state.json' \
    ghcr.io/clemensv/real-time-sources-autobahn:latest
```

## Environment Variables

- `CONNECTION_STRING`: Event Hubs or Fabric Event Streams connection string.
- `KAFKA_BOOTSTRAP_SERVERS`: Kafka bootstrap servers.
- `KAFKA_TOPIC`: Kafka topic. Defaults to `autobahn`.
- `SASL_USERNAME`: SASL/PLAIN username.
- `SASL_PASSWORD`: SASL/PLAIN password.
- `KAFKA_ENABLE_TLS`: When no SASL credentials are supplied, use `true` for
  TLS or `false` for plain Kafka.
- `AUTOBAHN_STATE_FILE`: File that stores ETags and the last successful
  snapshots. Defaults to `/mnt/fileshare/autobahn_state.json` in the ACI
  template below.
- `AUTOBAHN_POLL_INTERVAL`: Poll interval in seconds. Defaults to `300`.
- `AUTOBAHN_RESOURCES`: Comma-separated resource list or `*`.
- `AUTOBAHN_ROADS`: Comma-separated road list or `*`.
- `AUTOBAHN_REQUEST_CONCURRENCY`: Maximum concurrent API requests.

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fautobahn%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fautobahn%2Fazure-template-with-eventhub.json)