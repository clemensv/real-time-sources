# Digitraffic Road — Finnish Road Traffic Data

Real-time road traffic data from the Finnish national road network operated by
Fintraffic. Data is streamed via the Digitraffic MQTT service at
`wss://tie.digitraffic.fi/mqtt` and includes TMS sensor readings, road weather
sensor readings, traffic messages (incidents, road works, weight restrictions,
exempted transports), and maintenance vehicle tracking.

## Data Source

- **Publisher**: Fintraffic
- **Documentation**: https://www.digitraffic.fi/en/road-traffic/
- **Protocol**: MQTT over WebSocket
- **Auth**: None
- **License**: Creative Commons 4.0 BY
- **Update Frequency**: Real-time (sub-second via MQTT)

## Event Types

| Type | Description |
|---|---|
| `fi.digitraffic.road.sensors.TmsSensorData` | Traffic measurement (speed, vehicle count) from a TMS station |
| `fi.digitraffic.road.sensors.WeatherSensorData` | Road weather measurement (temperature, wind, humidity) from a weather station |
| `fi.digitraffic.road.messages.TrafficAnnouncement` | Traffic incident or lane closure announcement |
| `fi.digitraffic.road.messages.RoadWork` | Active or planned road work with phases and restrictions |
| `fi.digitraffic.road.messages.WeightRestriction` | Weight restriction on a road or bridge |
| `fi.digitraffic.road.messages.ExemptedTransport` | Oversize or heavy transport advance notice |
| `fi.digitraffic.road.maintenance.MaintenanceTracking` | Maintenance vehicle position and task report |

See [EVENTS.md](EVENTS.md) for full payload documentation.

## Running

```shell
python -m digitraffic_road stream \
    --kafka-bootstrap-servers localhost:9092 \
    --kafka-topic-sensors digitraffic-road-sensors \
    --kafka-topic-messages digitraffic-road-messages \
    --kafka-topic-maintenance digitraffic-road-maintenance
```

Or with a connection string (topics configured via env vars):

```shell
python -m digitraffic_road stream \
    -c "BootstrapServer=localhost:9092"
```

Use `python -m digitraffic_road probe` to inspect live MQTT messages.

See [CONTAINER.md](CONTAINER.md) for Docker deployment.
