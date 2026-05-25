# TfL Road Traffic

This bridge polls the [Transport for London (TfL) Unified API](https://api.tfl.gov.uk/) for road corridor status and disruption data, emitting CloudEvents to Apache Kafka.

## Data Model

The bridge emits three event types:

| Event Type | Source Endpoint | Description |
|---|---|---|
| `uk.gov.tfl.road.RoadCorridor` | `GET /Road` | Road corridor reference data (startup + hourly refresh) |
| `uk.gov.tfl.road.RoadStatus` | `GET /Road/all/Status` | Current traffic status per corridor (every poll cycle) |
| `uk.gov.tfl.road.RoadDisruption` | `GET /Road/all/Disruption` | Active disruptions (new/changed only, deduped by `id`+`lastModifiedTime`) |

All Kafka events share a single topic (`tfl-road-traffic`). Corridor events use the key `roads/{road_id}` and disruption events use `disruptions/{road_id}/{severity}/{disruption_id}`.

- MQTT/UNS feeder: `tfl_road_traffic_mqtt` publishes binary-mode CloudEvents under retained `traffic/gb/tfl/tfl-road-traffic/roads/{road_id}/corridor` and `traffic/gb/tfl/tfl-road-traffic/roads/{road_id}/status` topics, plus non-retained `traffic/gb/tfl/tfl-road-traffic/disruptions/{road_id}/{severity}/{disruption_id}` topics, all with QoS 1.

## Upstream

- [TfL Unified API](https://api.tfl.gov.uk/)
- [Road API documentation](https://api.tfl.gov.uk/swagger/ui/index.html#!/Road)
- [TfL Open Data](https://tfl.gov.uk/info-for/open-data-users/)

## Deployment

See [CONTAINER.md](CONTAINER.md) for Docker deployment instructions.

## Event Schemas

See [EVENTS.md](EVENTS.md) for full event schema documentation.


## MQTT and AMQP companion feeders

This source now ships separate MQTT and AMQP companion containers in addition to the Kafka/Event Hubs feeder. The MQTT container publishes binary-mode CloudEvents to the UNS topic templates declared in `xreg/`; the AMQP container publishes the same CloudEvents to an AMQP 1.0 address named `tfl-road-traffic` by default.

- MQTT image: `ghcr.io/clemensv/real-time-sources-tfl-road-traffic-mqtt:latest`
- AMQP image: `ghcr.io/clemensv/real-time-sources-tfl-road-traffic-amqp:latest`
- MQTT templates: `azure-template-mqtt.json`, `azure-template-with-eventgrid-mqtt.json`
- AMQP templates: `infra/azure-template-amqp.json`, `infra/azure-template-with-servicebus.json`
