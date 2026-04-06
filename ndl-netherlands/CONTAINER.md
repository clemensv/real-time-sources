# Netherlands NDL EV Charging Infrastructure bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image bridges the Nationale Databank Laadinfrastructuur (NDL)
open data feed at `https://opendata.ndw.nu` to Apache Kafka, Azure Event Hubs,
and Fabric Event Streams. It polls OCPI v2.2 charging location and tariff data
and emits CloudEvents documented in [EVENTS.md](EVENTS.md).

## Functionality

The upstream publishes gzip-compressed JSON snapshots of all Dutch EV charging
locations and tariffs. The bridge downloads these files, decompresses them, and
applies change detection against a local state file to emit EVSE status change
events. Location reference data and tariff reference data are emitted on the
first poll.

The data uses the OCPI (Open Charge Point Interface) v2.2 standard with a
three-level hierarchy: Location → EVSE → Connector.

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a
database, the integration with Fabric Eventhouse and Azure Data Explorer is
described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-ndl-netherlands:latest
```

## Using the Container Image

Run the bridge against a Kafka broker:

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='broker:9092' \
    -e NDL_CHARGING_TOPIC='ndl-charging' \
    -e NDL_TARIFFS_TOPIC='ndl-charging-tariffs' \
    ghcr.io/clemensv/real-time-sources-ndl-netherlands:latest
```

Or use an Event Hubs or Fabric Event Streams connection string:

```shell
$ docker run --rm \
    -e NDL_CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-ndl-netherlands:latest
```

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `NDL_CONNECTION_STRING` | No | Event Hubs/Fabric connection string. |
| `KAFKA_BOOTSTRAP_SERVERS` | No | Kafka bootstrap servers (alternative to connection string). |
| `KAFKA_SASL_USERNAME` | No | SASL username when using bootstrap servers with auth. |
| `KAFKA_SASL_PASSWORD` | No | SASL password when using bootstrap servers with auth. |
| `NDL_CHARGING_TOPIC` | No | Kafka topic for charging location and EVSE status events (default: `ndl-charging`). |
| `NDL_TARIFFS_TOPIC` | No | Kafka topic for tariff reference events (default: `ndl-charging-tariffs`). |
| `NDL_STATE_FILE` | No | Path to the state file for change detection (default: `~/.ndl_netherlands_state.json`). |
| `NDL_POLL_INTERVAL` | No | Polling interval in seconds (default: `300`). |
