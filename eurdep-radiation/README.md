# EURDEP Radiation

Bridge for the **EURDEP (European Radiological Data Exchange Platform)**
pan-European ambient gamma dose rate monitoring network.

EURDEP aggregates near-real-time radiological monitoring data from
approximately 5,500 stations across 39 European countries. Each station
reports hourly averaged ambient gamma dose rate in microsieverts per hour
(µSv/h).

## Quick Start

```bash
pip install -e .
pip install -e eurdep_radiation_producer/eurdep_radiation_producer_data
pip install -e eurdep_radiation_producer/eurdep_radiation_producer_kafka_producer
python -m eurdep_radiation feed --connection-string "BootstrapServer=localhost:9092;EntityPath=eurdep-radiation"
```

## Events

See [EVENTS.md](EVENTS.md) for the full event catalog.

## Container

See [CONTAINER.md](CONTAINER.md) for Docker deployment instructions.

## Upstream Source

- EURDEP: https://eurdep.jrc.ec.europa.eu/
- WFS endpoint: https://www.imis.bfs.de/ogc/opendata/ows
- Protocol: WFS 1.1.0 with GeoJSON output
- Auth: None (EU open data)
- Update frequency: Hourly
