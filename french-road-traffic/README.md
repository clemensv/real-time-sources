# French Road Traffic

Real-time traffic data from the French national non-conceded road network,
published by [Bison Futé](https://www.bison-fute.gouv.fr/) via the
[transport.data.gouv.fr](https://transport.data.gouv.fr/) open data portal.

## Data Sources

Two DATEX II XML feeds are polled:

1. **Traffic flow measurements** — vehicle counts and average speeds from ~1000
   measurement sites across the national road network, updated every 6 minutes.
2. **Road events** — incidents, accidents, construction works, lane closures,
   speed restrictions, and other events affecting road conditions, with ~300+
   active situations at any time.

## Upstream

- **Portal**: <https://transport.data.gouv.fr/datasets?type=road-data>
- **Protocol**: DATEX II XML (HTTP polling)
- **Auth**: None (Licence Ouverte 2.0)
- **Coverage**: French national non-conceded road network

## Events

See [EVENTS.md](EVENTS.md) for detailed event schemas.

| Event Type | Description |
|-----------|-------------|
| `fr.gouv.transport.bison_fute.TrafficFlowMeasurement` | Vehicle flow rate and average speed per measurement site |
| `fr.gouv.transport.bison_fute.RoadEvent` | Road incidents, works, closures, and other situations |

## Container

See [CONTAINER.md](CONTAINER.md) for deployment instructions.

```bash
docker pull ghcr.io/clemensv/real-time-sources-french-road-traffic:latest
```

## Development

```bash
cd french-road-traffic
pip install -e .
python -m french_road_traffic feed -c "BootstrapServer=localhost:9092;EntityPath=french-road-traffic"
```

### Run tests

```bash
cd french-road-traffic
pip install pytest
pytest tests/ -v
```

### Regenerate producer

```bash
cd french-road-traffic
pwsh generate_producer.ps1
```
