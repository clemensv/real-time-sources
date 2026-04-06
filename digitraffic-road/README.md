# Digitraffic Road — Finnish Road Traffic Sensor Data

Real-time TMS (Traffic Measurement System) and road weather sensor data from the
Finnish national road network operated by Fintraffic. Data is streamed via the
Digitraffic MQTT service at `wss://tie.digitraffic.fi/mqtt`.

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

See [EVENTS.md](EVENTS.md) for full payload documentation.

## Running

```shell
python -m digitraffic_road stream \
    --kafka-bootstrap-servers localhost:9092 \
    --kafka-topic digitraffic-road
```

Or with a connection string:

```shell
python -m digitraffic_road stream \
    -c "BootstrapServer=localhost:9092;EntityPath=digitraffic-road"
```

Use `python -m digitraffic_road probe` to inspect live MQTT messages.

See [CONTAINER.md](CONTAINER.md) for Docker deployment.
