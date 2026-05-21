# JMA Bosai Volcanic Warnings and Eruptions

This source bridges the Japan Meteorological Agency (JMA) Bosai volcano feeds to Kafka-compatible endpoints as structured CloudEvents. It polls public, unauthenticated JMA endpoints for active volcanic warnings, eruption observations, and the volcano reference catalog.

## Upstream coverage

| Family | Endpoint | Transport | Cadence | Decision |
| --- | --- | --- | --- | --- |
| Volcano catalog | `https://www.jma.go.jp/bosai/volcano/const/volcano_list.json` | REST JSON | refreshed monthly | Keep as `Volcano` reference data |
| Active volcanic warnings | `https://www.jma.go.jp/bosai/volcano/data/warning.json` | REST JSON | as issued; poll about every 60 seconds | Keep as `VolcanicWarning` telemetry |
| Eruption observations | `https://www.jma.go.jp/bosai/volcano/data/eruption.json` | REST JSON | as issued; poll about every 60 seconds | Keep as `VolcanicEruption` telemetry |

The source uses no authentication. Warning records are keyed by the stable three-digit JMA volcano code, not by mutable volcano names.

## Event model

All events use the Kafka key and CloudEvents subject template `jp.jma.volcano/{volcano_code}`.

- `JP.JMA.Volcano.Volcano` — volcano reference data with Japanese/English names, coordinates, elevation when available, and JMA `levelOperation` status.
- `JP.JMA.Volcano.VolcanicWarning` — target-volcano alert level and condition changes from `warning.json`.
- `JP.JMA.Volcano.VolcanicEruption` — discrete eruption observations from `eruption.json` when published.

See [EVENTS.md](EVENTS.md) for field details.

## Running

```powershell
cd jma-bosai-volcano
pip install jma_bosai_volcano_producer/jma_bosai_volcano_producer_data
pip install jma_bosai_volcano_producer/jma_bosai_volcano_producer_kafka_producer
pip install .
jma-bosai-volcano feed --kafka-bootstrap-servers localhost:9092 --kafka-topic jma-bosai-volcano --once
```

Configuration is also available through environment variables: `CONNECTION_STRING`, `KAFKA_BOOTSTRAP_SERVERS`, `KAFKA_TOPIC`, `SASL_USERNAME`, `SASL_PASSWORD`, `POLLING_INTERVAL`, `VOLCANO_METADATA_REFRESH_HOURS`, `STATE_FILE`, `ONCE_MODE`, and `KAFKA_ENABLE_TLS`.

- Fabric notebook hosting: deploy `notebook/jma-bosai-volcano-feed.ipynb` with [`tools/deploy-fabric/deploy-feeder-notebook.ps1`](../tools/deploy-fabric/deploy-feeder-notebook.ps1).
