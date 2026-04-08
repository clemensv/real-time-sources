# Nepal BIPAD Portal — Real-Time River Monitoring Bridge

This project provides a bridge between the [Nepal BIPAD Portal](https://bipadportal.gov.np/)
river monitoring API and Apache Kafka, Azure Event Hubs, and Fabric Event Streams.

## Source

The BIPAD Portal (Building Information Platform Against Disaster) is operated by
the Government of Nepal. The river-stations API provides real-time water level
data from monitoring stations across Nepal's major Himalayan river basins:
Bagmati, Narayani, Koshi, Karnali, Mahakali, Babai, and others.

- **API**: `https://bipadportal.gov.np/api/v1/river-stations/?format=json`
- **Auth**: None (open government data)
- **Update frequency**: Every 15–30 minutes
- **Data source**: Nepal Department of Hydrology and Meteorology (hydrology.gov.np)

## Events

The bridge emits two CloudEvents types:

| Type | Description |
|------|-------------|
| `np.gov.bipad.hydrology.RiverStation` | Reference data: station metadata, location, basin, thresholds |
| `np.gov.bipad.hydrology.WaterLevelReading` | Telemetry: current water level, status, trend |

See [EVENTS.md](EVENTS.md) for full schema documentation.

## Running

```shell
# Using connection string
docker run --rm \
    -e CONNECTION_STRING='BootstrapServer=localhost:9092;EntityPath=nepal-bipad-hydrology' \
    ghcr.io/clemensv/real-time-sources-nepal-bipad-hydrology:latest

# Using explicit Kafka config
docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='localhost:9092' \
    -e KAFKA_TOPIC='nepal-bipad-hydrology' \
    ghcr.io/clemensv/real-time-sources-nepal-bipad-hydrology:latest
```

See [CONTAINER.md](CONTAINER.md) for full deployment documentation.

## Development

```shell
cd nepal-bipad-hydrology
pip install -e .
pip install -e nepal_bipad_hydrology_producer/nepal_bipad_hydrology_producer_data
pip install -e nepal_bipad_hydrology_producer/nepal_bipad_hydrology_producer_kafka_producer
python -m pytest tests -m "unit or integration" --no-header -q
```
