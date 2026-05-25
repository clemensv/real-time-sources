# Entur Norway Container

## Overview

This container bridges the [Entur Norway](https://developer.entur.org/) SIRI
real-time feeds to Apache Kafka endpoints. It polls the SIRI 2.0 REST API for
Estimated Timetable (ET), Vehicle Monitoring (VM), and Situation Exchange (SX)
data, emitting events as CloudEvents.

The Entur API provides real-time information about Norwegian public transport
across all operators and modes (bus, tram, rail, metro, ferry). Data is sourced
from the national journey planner and covers the entire Norwegian network.

For the full event catalog, see [EVENTS.md](EVENTS.md).

## Container Image

```bash
docker pull ghcr.io/clemensv/real-time-sources/entur-norway:latest
```

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `CONNECTION_STRING` | Yes | — | Kafka connection string (see below) |
| `POLLING_INTERVAL` | No | `30` | Polling interval in seconds |
| `MAX_SIZE` | No | `1000` | Maximum records per SIRI request |
| `KAFKA_ENABLE_TLS` | No | `true` | Set to `false` for plain Kafka without TLS |

## Running with Plain Kafka

```bash
docker run -d \
  -e CONNECTION_STRING="BootstrapServer=localhost:9092;EntityPath=entur-norway" \
  -e KAFKA_ENABLE_TLS=false \
  ghcr.io/clemensv/real-time-sources/entur-norway:latest
```

## Running with Azure Event Hubs

```bash
docker run -d \
  -e CONNECTION_STRING="Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy>;SharedAccessKey=<key>;EntityPath=entur-norway" \
  ghcr.io/clemensv/real-time-sources/entur-norway:latest
```

## Running with Fabric Event Streams

Use the Kafka connection string from your Fabric Event Stream custom
endpoint. The format is the same as Azure Event Hubs.

## Behavior

1. At startup, fetches all three SIRI feeds (ET, VM, SX) without a `requestorId`
   to obtain the complete current dataset.
2. From the initial ET snapshot, emits `no.entur.DatedServiceJourney` reference
   events for each unique service journey, providing timetable context for
   downstream consumers.
3. Emits `no.entur.EstimatedVehicleJourney` events for all stop-level
   predictions from the ET feed.
4. Emits `no.entur.MonitoredVehicleJourney` events for all live vehicle
   positions from the VM feed.
5. Emits `no.entur.PtSituationElement` events for all active service disruptions
   from the SX feed.
6. Subsequent polling cycles use a persistent `requestorId` per feed to receive
   only changed data since the last request (incremental delivery).
7. Handles SIRI `MoreData: true` responses by paginating until all data is
   received.

## Kafka Topic

All events are produced to a single Kafka topic (default: `entur-norway`).

- `journeys` events use the key format `journeys/{operating_day}/{service_journey_id}`
- `situations` events use the key format `situations/{situation_number}`

## Data Source

- API: <https://api.entur.io/realtime/v1/rest/>
- Documentation: <https://developer.entur.org/pages-real-time-intro>
- License: [NLOD (Norwegian Licence for Open Government Data)](https://data.norge.no/nlod/en/2.0)
- Coverage: All Norwegian public transport operators and modes

## MQTT/Unified Namespace image

A sibling MQTT container image, `ghcr.io/clemensv/real-time-sources-entur-norway-mqtt:latest`, publishes the same source events as MQTT 5.0 binary-mode CloudEvents. It uses the xRegistry MQTT messagegroup `no.entur.mqtt` and the source-specific Unified Namespace topic tree described in [EVENTS.md](EVENTS.md).

### Run against a generic MQTT 5 broker

```shell
docker run --rm \
    -e MQTT_BROKER_URL='mqtts://broker.example.com:8883' \
    -e MQTT_USERNAME='<username>' \
    -e MQTT_PASSWORD='<password>' \
    ghcr.io/clemensv/real-time-sources-entur-norway-mqtt:latest
```

### MQTT environment variables

| Variable | Description |
|---|---|
| `MQTT_BROKER_URL` | Broker URL including host, port, and TLS scheme, for example `mqtt://host:1883` or `mqtts://host:8883`. |
| `MQTT_USERNAME` / `MQTT_PASSWORD` | Optional username/password credentials for brokers that require user authentication. Leave unset for anonymous brokers. |
| `MQTT_CLIENT_ID` | Optional MQTT client identifier. Set it explicitly on shared brokers and Event Grid namespaces. |
| `MQTT_CONTENT_MODE` | CloudEvents content mode, `binary` by default. Keep `binary` for MQTT 5 user-property metadata. |
| `POLLING_INTERVAL` | Source polling interval in seconds, when supported by the feeder. |
| `STATE_FILE` | Optional path for source dedupe/checkpoint state, when the feeder maintains local state. |
| topic prefix | Fixed by the xRegistry contract, not an environment variable. Root: `transit/no/entur/entur-norway/et`. |
| retain default | Per message in xRegistry; see the topic table below. |
| QoS default | Per message in xRegistry; MQTT messages in this source use QoS 1 unless noted otherwise. |

### MQTT topic patterns

| Topic pattern | Message type | Retained | QoS | Expiry seconds |
|---|---|---|---|---|
| `transit/no/entur/entur-norway/et/{operator_ref}/{line_ref}/{service_journey_id}/estimated-vehicle-journey` | `no.entur.EstimatedVehicleJourney` | `false` | `1` | `` |
| `transit/no/entur/entur-norway/vm/{operator_ref}/{line_ref}/{service_journey_id}/monitored-vehicle-journey` | `no.entur.MonitoredVehicleJourney` | `false` | `1` | `` |
| `transit/no/entur/entur-norway/sx/{severity}/{situation_number}/situation` | `no.entur.PtSituationElement` | `false` | `1` | `` |

### Subscription patterns

```text
# Everything from this source
transit/no/entur/entur-norway/et/#
```

### MQTT Azure deployment

Deploy the MQTT container against an existing MQTT 5 broker:

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fentur-norway%2Fazure-template-mqtt.json)

Deploy the MQTT container with a new Azure Event Grid namespace MQTT broker:

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fentur-norway%2Fazure-template-with-eventgrid-mqtt.json)

## AMQP 1.0 companion

This source also ships an AMQP 1.0 companion feeder (`Dockerfile.amqp`) alongside the Kafka and MQTT variants. It publishes the same CloudEvents to a single AMQP address named after the source, with CloudEvent `subject` and AMQP application properties mirroring the Kafka key/MQTT topic axes for broker-side filtering. Use `azure-template-with-servicebus.json` to deploy the AMQP feeder to Azure Service Bus with Entra ID/CBS authentication, or set `AMQP_BROKER_URL` for a generic AMQP 1.0 broker.
