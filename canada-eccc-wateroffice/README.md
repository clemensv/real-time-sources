# Canada ECCC Water Office Hydrometric Bridge

Real-time hydrometric data from [Environment and Climate Change Canada (ECCC) Water Survey of Canada](https://wateroffice.ec.gc.ca/) bridged to Apache Kafka as CloudEvents.

## Data

- **~2100 active hydrometric monitoring stations** across all Canadian provinces and territories
- **Real-time water level and discharge** updated approximately every 5 minutes
- **Station reference metadata** including drainage area, province/territory, contributor, and RHBN membership

## Upstream API

| | |
|---|---|
| Station reference | `https://api.weather.gc.ca/collections/hydrometric-stations/items` |
| Real-time observations | `https://api.weather.gc.ca/collections/hydrometric-realtime/items` |
| Protocol | REST (OGC API Features), GeoJSON |
| Auth | None |
| License | Open Government Licence — Canada |
| Update frequency | ~5 minutes |

## Events

| CloudEvents type | Description |
|---|---|
| `CA.Gov.ECCC.Hydro.Station` | Station reference data (emitted at startup and every 24 h) |
| `CA.Gov.ECCC.Hydro.Observation` | Real-time water level / discharge observation |

Kafka key and CloudEvents subject: `stations/{station_number}` (e.g. `stations/05BJ004`)

## Usage

See [CONTAINER.md](CONTAINER.md) for Docker deployment details.


## MQTT and AMQP companion feeders

This source now ships transport-split Kafka, MQTT, and AMQP containers. The MQTT image (`ghcr.io/clemensv/real-time-sources-canada-eccc-wateroffice-mqtt:latest`) publishes retained MQTT 5 binary-mode CloudEvents on `hydro/ca/eccc/canada-eccc-wateroffice/...`. The AMQP image (`ghcr.io/clemensv/real-time-sources-canada-eccc-wateroffice-amqp:latest`) publishes the same CloudEvents to a broker address or Azure Service Bus queue.

Deployment templates: `azure-template-mqtt.json`, `azure-template-with-eventgrid-mqtt.json`, and `azure-template-with-servicebus.json`.
