# Energy-Charts (Fraunhofer ISE) — European Electricity Data Bridge

This bridge polls the [Energy-Charts API](https://api.energy-charts.info/) operated by Fraunhofer ISE and forwards European electricity generation, price, and grid carbon signal data to Apache Kafka, Azure Event Hubs, or Fabric Event Streams as CloudEvents.

## Data Source

The Energy-Charts API provides freely available (CC BY 4.0) electricity data for 40+ European countries. Data is sourced from the ENTSO-E transparency platform and national grid operators.

### Endpoints Polled

| Endpoint | Description | Interval |
|----------|-------------|----------|
| `/public_power?country={country}` | Net generation by fuel type (MW) | 15 min |
| `/price?bzn={bidding_zone}` | Day-ahead spot prices (EUR/MWh) | 1 hour |
| `/signal?country={country}` | Grid carbon signal (0/1/2 traffic light) | 15 min |

## Events

See [EVENTS.md](EVENTS.md) for the full event schema documentation.

| Event Type | Description |
|-----------|-------------|
| `info.energy_charts.PublicPower` | Generation mix per country per timestamp |
| `info.energy_charts.SpotPrice` | Day-ahead spot price per bidding zone |
| `info.energy_charts.GridSignal` | Carbon signal + renewable share % |

## Installation

```shell
pip install .
```

## Usage

### With a connection string (Event Hubs / Fabric)

```shell
python -m energy_charts --connection-string '<connection-string>'
```

### With explicit Kafka settings

```shell
python -m energy_charts \
    --kafka-bootstrap-servers 'broker:9092' \
    --kafka-topic 'energy-charts' \
    --country de \
    --bidding-zone DE-LU
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `CONNECTION_STRING` | Azure Event Hubs / Fabric connection string | — |
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka broker addresses | — |
| `KAFKA_TOPIC` | Kafka topic | — |
| `COUNTRY` | ISO country code | `de` |
| `BIDDING_ZONE` | ENTSO-E bidding zone | `DE-LU` |
| `ENERGY_CHARTS_LAST_POLLED_FILE` | State file for deduplication | `~/.energy_charts_last_polled.json` |

## Container

See [CONTAINER.md](CONTAINER.md) for Docker usage.

```shell
docker pull ghcr.io/clemensv/real-time-sources-energy-charts:latest
```
