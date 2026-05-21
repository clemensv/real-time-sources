# JMA Bosai Earthquake & Seismic Intensity Information

This source polls the Japan Meteorological Agency (JMA / 気象庁) Bosai earthquake feed and emits new earthquake and seismic intensity reports as CloudEvents to Kafka, Azure Event Hubs, or Microsoft Fabric Event Streams.

## Upstream source

- Publisher: Japan Meteorological Agency (JMA)
- Authentication: none
- License: Japanese government open data
- Cadence: reports appear as earthquakes occur, with updates and corrections; the bridge polls every 60 seconds by default.
- Fabric notebook hosting: deploy the scheduled notebook feeder with [`tools/deploy-fabric/deploy-feeder-notebook.ps1`](../tools/deploy-fabric/deploy-feeder-notebook.ps1).

## Reviewed data channels

| Family | Transport | Identity | Cadence | Decision |
| --- | --- | --- | --- | --- |
| Recent earthquake list | REST `https://www.jma.go.jp/bosai/quake/data/list.json` | `eid` plus `ser` | Near real time | Keep. This is the current/recent earthquake report index and carries the stable event id, serial, report metadata, hypocenter summary, and prefecture/city intensity summaries. |
| Earthquake detail JSON | REST `https://www.jma.go.jp/bosai/quake/data/{json}` | `eid` plus `ser` | Near real time with each list entry | Keep as enrichment. The bridge fetches the referenced detail file to derive tsunami-related comments when available. |
| Tsunami VTSE detail products | REST detail files whose product code starts `VTSE` | Tsunami bulletin ids | Near real time | Drop. Tsunami products are covered by the separate `jma-bosai-warning` source and are not emitted here. |

No separate station or catalog metadata endpoint is required for this event model; JMA supplies the affected prefecture and city codes inline with each report.

## Event model

The source emits one event type, `JP.JMA.Quake.EarthquakeReport`, documented in [EVENTS.md](EVENTS.md). The CloudEvents subject and Kafka key are both:

```text
jp.jma.quake/{event_id}/{serial}
```

The composite key preserves multiple serial reports for the same earthquake, including corrections and cancellations.

## Running locally

```powershell
cd jma-bosai-quake
pip install .\jma_bosai_quake_producer\jma_bosai_quake_producer_data
pip install .\jma_bosai_quake_producer\jma_bosai_quake_producer_kafka_producer
pip install -e .
jma-bosai-quake feed --kafka-bootstrap-servers "localhost:9092" --kafka-topic "jma-bosai-quake" --once
```

Configuration can also be supplied via environment variables: `CONNECTION_STRING`, `KAFKA_BOOTSTRAP_SERVERS`, `KAFKA_TOPIC`, `SASL_USERNAME`, `SASL_PASSWORD`, `KAFKA_ENABLE_TLS`, `POLLING_INTERVAL`, `STATE_FILE`, and `ONCE_MODE`.

## State

The bridge persists a FIFO set of the latest 1000 `(eid, ser)` tuples in `./state/jma-bosai-quake.json` by default. State advances only after Kafka flush succeeds, so failed deliveries are retried on the next poll.
