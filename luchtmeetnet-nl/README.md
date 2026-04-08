# Luchtmeetnet Netherlands Air Quality Bridge

This source bridges the public Dutch **Luchtmeetnet** API into Apache Kafka
compatible brokers as structured JSON CloudEvents. It emits both slowly changing
reference data and hourly telemetry so downstream consumers can reconstruct air
quality context and measurements over time without making their own side calls.

## Upstream

- API base URL: `https://api.luchtmeetnet.nl/open_api`
- Documentation: <https://api-docs.luchtmeetnet.nl/>
- Open data information: <https://www.luchtmeetnet.nl/informatie/download-data/open-data>

The upstream data updates hourly and is publicly accessible without
authentication.

## Event Families

- `nl.rivm.luchtmeetnet.Station` — station reference metadata keyed by
  `station_number`
- `nl.rivm.luchtmeetnet.Measurement` — hourly station measurements keyed by
  `station_number`
- `nl.rivm.luchtmeetnet.LKI` — hourly Dutch air-quality-index values keyed by
  `station_number`
- `nl.rivm.luchtmeetnet.components.Component` — component catalog records keyed
  by `formula`

See [EVENTS.md](EVENTS.md) for the event contract.

## Upstream Channel Audit

| Family | Endpoint | Identity | Cadence | Decision |
|---|---|---|---|---|
| Station metadata list | `GET /stations?page={n}` | `station_number` | Rarely changes | KEEP — used to discover all stations. |
| Station metadata detail | `GET /stations/{number}` | `station_number` | Rarely changes | KEEP — authoritative reference data for station events. |
| Component catalog list | `GET /components` | `formula` | Rarely changes | KEEP — component reference data. |
| Component detail | `GET /components/{formula}` | `formula` | Rarely changes | DROP — richer prose and limits metadata exists, but the bridge contract only needs stable catalog names for reference events. |
| Station-scoped measurements | `GET /stations/{number}/measurements` | `station_number` + `formula` | Hourly | DROP — duplicate presentation of the measurement family already available from `/measurements`. |
| Measurements | `GET /measurements?station_number={n}&formula={f}` | `station_number` + `formula` | Hourly | KEEP — core telemetry family. |
| LKI | `GET /lki?station_number={n}` | `station_number` | Hourly | KEEP — derived air-quality-index telemetry. |
| Organisations | `GET /organisations` | `organisation_id` | Rarely changes | DROP — useful catalog, but not required by the requested event model because station events already carry organisation names. |
| Concentrations (ASCII) | `GET /concentrations?...` | coordinate + formula | Hourly | DROP — alternate presentation for map-style concentration lookup, not station-keyed telemetry and outside the requested source scope. |

## Runtime Behavior

The bridge is a poller.

1. At startup it fetches all stations and all components.
2. It emits station reference events first, then component reference events.
3. Every poll cycle it fetches the latest page of measurements for each
   station/formula combination and the latest page of LKI values for each
   station.
4. It deduplicates by remembered timestamp and only emits new records.
5. It refreshes station metadata periodically so downstream consumers can see
   reference-data drift over time.

## Usage

Install locally:

```powershell
pip install luchtmeetnet_nl_producer\luchtmeetnet_nl_producer_data
pip install luchtmeetnet_nl_producer\luchtmeetnet_nl_producer_kafka_producer
pip install -e .
```

Run the bridge:

```powershell
python -m luchtmeetnet_nl feed --kafka-bootstrap-servers localhost:9092 --kafka-topic luchtmeetnet-nl
```

Or with an Event Hubs / Fabric connection string:

```powershell
python -m luchtmeetnet_nl feed --connection-string "Endpoint=sb://namespace.servicebus.windows.net/;SharedAccessKeyName=policy;SharedAccessKey=...;EntityPath=luchtmeetnet-nl"
```

## License

This project is licensed under the MIT License. See [LICENSE.md](../LICENSE.md).
