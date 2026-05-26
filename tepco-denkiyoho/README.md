# TEPCO Electricity Supply & Demand (Denki Yoho) Bridge

This source polls Tokyo Electric Power Company (TEPCO) Electricity Forecast (でんき予報) open data and emits CloudEvents to Apache Kafka, Azure Event Hubs, or Microsoft Fabric Event Streams.

## Upstream source

- Publisher: Tokyo Electric Power Company (TEPCO / 東京電力)
- Coverage: Tokyo Electric Power Company service area: Tokyo, Kanagawa, Saitama, Chiba, Tochigi, Gunma, Ibaraki, Yamanashi, and Shizuoka east of the Fujikawa River
- Main feed: `https://www.tepco.co.jp/forecast/html/images/juyo-d1-j.csv`
- Encoding: Shift-JIS
- Cadence: about every 5 minutes
- Auth: none

## Channel review

| Data family | Transport | Identity | Cadence | Decision |
| --- | --- | --- | --- | --- |
| Daily same-day CSV `juyo-d1-j.csv` | HTTPS Shift-JIS CSV | date + local time, with `_supply_capacity_` sentinel for daily supply reference | ~5 minutes | Keep: contains supply capacity, hourly forecasts, and five-minute actual demand. |
| Archive CSV `juyo-j.csv` | HTTPS Shift-JIS CSV | date + local time | Archive/reconciliation | Drop for initial bridge: lower-priority duplicate/history view, not needed for live feed. |
| Forecast website HTML | HTTPS HTML | page widgets | ~5 minutes | Drop: presentation layer for values carried by the CSV. |

TEPCO does not expose station, sensor, zone, or entity metadata endpoints for this feed; the only reference event is the daily supply-capacity header from the same CSV.

## Events

The bridge emits three event types in one message group (`JP.TEPCO.Denkiyoho`):

- `SupplyCapacity` daily reference data from the CSV header
- `DemandActual` five-minute actual demand rows with non-zero measured values
- `DemandForecast` hourly forecast rows

Values published by TEPCO in `万kW` are preserved and also converted to MW by multiplying by 10. See [EVENTS.md](EVENTS.md) for the contract.

## Usage

Install locally:

```powershell
cd tepco-denkiyoho
pip install .\tepco_denkiyoho_producer\tepco_denkiyoho_producer_data
pip install .\tepco_denkiyoho_producer\tepco_denkiyoho_producer_kafka_producer
pip install .
```

Run the poller:

```powershell
tepco-denkiyoho feed --connection-string "BootstrapServer=localhost:9092;EntityPath=tepco-denkiyoho" --once
```

Configuration can be supplied by command-line arguments or environment variables: `CONNECTION_STRING`, `KAFKA_TOPIC`, `POLLING_INTERVAL`, `KAFKA_ENABLE_TLS`, and `STATE_FILE`.


## Transports

This source now ships Kafka plus MQTT and AMQP companion feeders. MQTT publishes binary-mode CloudEvents into the documented topic tree for wildcard subscribers and retained last-known-value use cases. AMQP publishes the same CloudEvents to a broker address for queue/topic consumers. Deployment templates include `azure-template.json`, `azure-template-with-eventhub.json`, `azure-template-mqtt.json`, `azure-template-with-eventgrid-mqtt.json`, `azure-template-amqp.json`, and `azure-template-with-servicebus.json`. Dockerfiles: `Dockerfile`, `Dockerfile.mqtt`, `Dockerfile.amqp`.
