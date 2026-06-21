# KiWIS

[Events](EVENTS.md) · [Container deployment](CONTAINER.md) · [xRegistry contract](xreg/kiwis.xreg.json)

KiWIS turns public KISTERS Web Interoperability Solution hydrological databases into streaming CloudEvents. Water agencies, flood-warning teams, researchers, and operations dashboards can subscribe to consistent station catalogs, timeseries metadata, and live values from many KiWIS instances without writing one bespoke integration per authority.

The feeder is generalized by configuration. `KIWIS_ENDPOINTS` accepts CSV lines (`kiwis_id,base_url,datasource,station_filter,timeseries_filter,ts_ids,period,api_key`) or a JSON array, and may also point at `@file`. The shipped default uses the public, key-less SEPA Scotland KiWIS endpoint.

## Upstream API audit

| Request | Family | Decision |
| --- | --- | --- |
| `getRequestInfo` | capability discovery | Used during audit and diagnostics; not emitted because it describes the service surface, not a hydrological entity. |
| `getStationList` | station reference | Kept as `org.kiwis.Station`, keyed `{kiwis_id}/{station_id}`. |
| `getParameterList`, `getParameterTypeList` | parameter reference | Reviewed; parameter labels used from `getTimeseriesList`. Dedicated parameter events are not emitted because timeseries metadata already carries the parameter context needed by values. |
| `getTimeseriesChanges` / `changedSince` filters | delta discovery | Reviewed; not emitted as its own event family because it is a polling optimization/change index for timeseries already modeled by `Timeseries` and `TimeseriesValue`. The bridge uses state-based dedupe and can add `changedSince` later without changing the event contract. |
| Graph, layer, comments, release-state, ensemble requests | presentation or specialized extensions | Dropped for this generalized public default because they are either visualization helpers, optional quality workflow metadata, or specialized products not consistently available on public keyless instances. |
| `getTimeseriesList` | timeseries catalog | Kept as `org.kiwis.Timeseries`, keyed `{kiwis_id}/{ts_id}`. |
| `getTimeseriesValues` | telemetry | Kept as `org.kiwis.TimeseriesValue`, keyed `{kiwis_id}/{ts_id}`. |

Validated public instance: `https://timeseries.sepa.org.uk/KiWIS/KiWIS`. SEPA returned station fields `station_id`, `station_no`, `station_name`, `station_latitude`, `station_longitude`, `river_name`, `catchment_name`; timeseries fields including `ts_id`, station linkage, parameter labels, `ts_unitname`, `ts_unitsymbol`, and coverage; values as `Timestamp,Value,Quality Code` rows.

## Transports

| Variant | Image | Delivery shape |
| --- | --- | --- |
| Kafka | `ghcr.io/clemensv/real-time-sources-kiwis:latest` | Structured CloudEvents to Kafka/Event Hubs/Fabric Eventstream topic `kiwis`. |
| MQTT | `ghcr.io/clemensv/real-time-sources-kiwis-mqtt:latest` | Binary-mode MQTT 5 CloudEvents under `hydro/kiwis/{kiwis_id}/...`, retained QoS 1. |
| AMQP 1.0 | `ghcr.io/clemensv/real-time-sources-kiwis-amqp:latest` | Binary-mode CloudEvents to one AMQP address for Service Bus or generic brokers. |

Fabric notebook hosting is available via `tools/deploy-fabric/deploy-feeder-notebook.ps1`; the notebook runs the Kafka feeder in `--once` mode and looks up the Event Stream connection string at runtime.

## Configuration quick start

```powershell
# Kafka local/Fabric/Event Hubs style
$env:CONNECTION_STRING='BootstrapServer=localhost:9092;EntityPath=kiwis'
$env:KAFKA_ENABLE_TLS='false'
$env:KIWIS_MOCK='true'
python -m kiwis_kafka feed --once
```

Set `KIWIS_ENDPOINTS` to a CSV or JSON list to poll more agencies. API keys are optional and can be supplied through environment expansion such as `${KIWIS_API_KEY}` in the config file. Default polling is 300 seconds, well below the practical rate pressure for a small configured timeseries set; SEPA's public KiWIS endpoint did not publish an explicit rate-limit statement in the audited response.
