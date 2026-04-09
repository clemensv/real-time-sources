# Ireland OPW waterlevel.ie Bridge

This project provides a bridge that reads real-time water level, temperature,
and voltage data from Ireland's OPW (Office of Public Works) hydrometric
stations via the [waterlevel.ie](https://waterlevel.ie) GeoJSON API and emits
the data as CloudEvents to Apache Kafka, Azure Event Hubs, or Fabric Event
Streams.

## Data Source

The OPW operates a network of hydrometric stations across Irish rivers, lakes,
and canals. The `https://waterlevel.ie/geojson/latest/` endpoint returns a
GeoJSON FeatureCollection updated every 15 minutes. Data is published under
CC BY 4.0.

Each feature contains:
- **station_ref**: 10-digit station code
- **station_name**: human-readable name
- **sensor_ref**: sensor type ('0001' = level, '0002' = temperature, '0003' = voltage, 'OD' = Ordnance Datum)
- **value**: string numeric reading
- **datetime**: ISO 8601 timestamp
- **err_code**: 99 = OK

## Events

See [EVENTS.md](EVENTS.md) for detailed event documentation.

## Container

See [CONTAINER.md](CONTAINER.md) for Docker usage and deployment instructions.

## Development

```bash
pip install -e .
pip install -e ireland_opw_waterlevel_producer/ireland_opw_waterlevel_producer_data
pip install -e ireland_opw_waterlevel_producer/ireland_opw_waterlevel_producer_kafka_producer
python -m pytest tests -m "unit or integration" --no-header -q
```
