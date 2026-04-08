# UBA Germany Air Quality Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container bridges the Umweltbundesamt (UBA) Germany national air quality
API into Apache Kafka compatible endpoints. It emits structured JSON
[CloudEvents](https://cloudevents.io/) for station metadata, pollutant
components, and hourly measurements. The event contract is documented in
[EVENTS.md](EVENTS.md).

## Upstream Source

The UBA `air_data/v3` API publishes Germany-wide air quality data from the
federal and state monitoring networks. The bridge consumes the station catalog,
component catalog, and hourly one-hour-average measurements.

## What the Bridge Emits

- `Station` reference events keyed by `station_id`
- `Component` reference events keyed by `component_id`
- `Measure` telemetry events keyed by `station_id`

Reference data is emitted first at startup and periodically refreshed so
downstream consumers can keep telemetry aligned with the right station and
component context over time.

## Database Schemas and Handling

If you want to build a full downstream analytics pipeline, the general guidance
for Eventhouse or Azure Data Explorer is in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

```shell
docker pull ghcr.io/clemensv/real-time-sources-uba-airdata:latest
```

## Running the Container

### With a Kafka Broker

```shell
docker run --rm \
  -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
  -e KAFKA_TOPIC='uba-airdata' \
  -e SASL_USERNAME='<sasl-username>' \
  -e SASL_PASSWORD='<sasl-password>' \
  ghcr.io/clemensv/real-time-sources-uba-airdata:latest
```

### With Azure Event Hubs or Fabric Event Streams

```shell
docker run --rm \
  -e CONNECTION_STRING='Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy>;SharedAccessKey=<key>;EntityPath=uba-airdata' \
  ghcr.io/clemensv/real-time-sources-uba-airdata:latest
```

### With Plain Kafka for Local Testing

The repo-wide Docker Kafka E2E harness uses this connection convention:

```shell
docker run --rm \
  -e CONNECTION_STRING='BootstrapServer=<host:port>;EntityPath=uba-airdata' \
  -e KAFKA_ENABLE_TLS=false \
  ghcr.io/clemensv/real-time-sources-uba-airdata:latest
```

## Environment Variables

### Required

- `CONNECTION_STRING` or `KAFKA_BOOTSTRAP_SERVERS`
- `KAFKA_TOPIC` when not supplied through `EntityPath` in `CONNECTION_STRING`

### Optional

- `SASL_USERNAME` — SASL PLAIN username
- `SASL_PASSWORD` — SASL PLAIN password
- `KAFKA_ENABLE_TLS` — `true` by default. Set `false` for plain Kafka
  listeners.
- `POLLING_INTERVAL` — polling interval in seconds. Default: `3600`
- `STATE_FILE` — JSON file used for local dedup state. Default:
  `~/.uba_airdata_state.json`

## Azure Container Instances

You can deploy the container into Azure Container Instances with the same
environment variables shown above. Use an Event Hubs or Fabric connection string
if you want the most compact deployment contract.
