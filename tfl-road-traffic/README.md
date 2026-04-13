# TfL Road Traffic

This bridge polls the [Transport for London (TfL) Unified API](https://api.tfl.gov.uk/) for road corridor status and disruption data, emitting CloudEvents to Apache Kafka.

## Data Model

The bridge emits three event types:

| Event Type | Source Endpoint | Description |
|---|---|---|
| `uk.gov.tfl.road.RoadCorridor` | `GET /Road` | Road corridor reference data (startup + hourly refresh) |
| `uk.gov.tfl.road.RoadStatus` | `GET /Road/all/Status` | Current traffic status per corridor (every poll cycle) |
| `uk.gov.tfl.road.RoadDisruption` | `GET /Road/all/Disruption` | Active disruptions (new/changed only, deduped by `id`+`lastModifiedTime`) |

All events share a single Kafka topic (`tfl-road-traffic`). Corridor events use the key `roads/{road_id}` and disruption events use `disruptions/{disruption_id}`.

## Upstream

- [TfL Unified API](https://api.tfl.gov.uk/)
- [Road API documentation](https://api.tfl.gov.uk/swagger/ui/index.html#!/Road)
- [TfL Open Data](https://tfl.gov.uk/info-for/open-data-users/)

## Deployment

See [CONTAINER.md](CONTAINER.md) for Docker deployment instructions.

## Event Schemas

See [EVENTS.md](EVENTS.md) for full event schema documentation.
