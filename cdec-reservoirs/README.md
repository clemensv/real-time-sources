# CDEC California Reservoirs Bridge

This source bridges real-time reservoir data from the California Data Exchange
Center (CDEC) to Apache Kafka, Azure Event Hubs, or Fabric Event Streams.

## Data Source

The [California Data Exchange Center (CDEC)](https://cdec.water.ca.gov/) is
operated by the California Department of Water Resources. It provides real-time
hydrologic data for over 2,600 stations, including all major California
reservoirs.

The bridge polls the CDEC JSON Data Servlet for hourly readings of:
- **Storage** (acre-feet) — sensor 15
- **Reservoir Elevation** (feet) — sensor 6
- **Inflow** (cubic feet per second) — sensor 76
- **Outflow** (cubic feet per second) — sensor 23

Default monitored stations include Shasta (SHA), Oroville (ORO), Folsom (FOL),
New Melones (NML), Don Pedro (DNP), Hetch Hetchy (HTC), Sonoma (SON),
Millerton (MIL), and Pine Flat (PNF).

## Events

See [EVENTS.md](EVENTS.md) for the event schema documentation.

## Container

See [CONTAINER.md](CONTAINER.md) for Docker deployment instructions.

## Development

```shell
cd cdec-reservoirs
pip install -e .
pip install -e cdec_reservoirs_producer/cdec_reservoirs_producer_data
pip install -e cdec_reservoirs_producer/cdec_reservoirs_producer_kafka_producer
python -m pytest tests -m "unit or integration" --no-header -q
```
