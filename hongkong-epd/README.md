# Hong Kong EPD AQHI Bridge

This bridge fetches the Hong Kong Environmental Protection Department's
[Air Quality Health Index (AQHI)](https://www.aqhi.gov.hk/) feed and emits
CloudEvents into Apache Kafka or Azure Event Hubs.

## Data Model

The bridge emits two event types into the `hongkong-epd-aqhi` topic, keyed by
`{station_id}`:

| Event Type | Description |
|---|---|
| `HK.Gov.EPD.AQHI.Station` | Reference data for the 18 AQHI monitoring stations |
| `HK.Gov.EPD.AQHI.AQHIReading` | Latest AQHI reading per station, derived from the 24-hour XML feed |

## Upstream Feed Review

- **Feed**: `https://www.aqhi.gov.hk/epd/ddata/html/out/24aqhi_Eng.xml`
- **Transport**: HTTP polling of a public XML file
- **Auth**: None
- **Cadence**: Hourly
- **Identity**: Stable station IDs derived from the published station names
- **Feed coverage reviewed**:

| Family | Transport | Identity | Cadence | Decision |
|---|---|---|---|---|
| AQHI 24-hour history feed | XML file over HTTP | `station_id` | Hourly | Keep — bridge emits the latest reading per station |
| Station metadata | Hard-coded from EPD station map and feed station roster | `station_id` | Rarely changes | Keep — emitted as reference events |

The public feed is a single XML channel. It contains 24 hours of AQHI history
for 18 stations. The bridge keeps the latest record per station and publishes
reference data first so downstream consumers can build a temporally consistent
view.

## Source Files

| File | Description |
|---|---|
| [xreg/hongkong_epd.xreg.json](xreg/hongkong_epd.xreg.json) | xRegistry manifest |
| [hongkong_epd/hongkong_epd.py](hongkong_epd/hongkong_epd.py) | Runtime bridge |
| [hongkong_epd_producer/](hongkong_epd_producer/) | Generated producer (xrcg 0.10.1) |
| [tests/](tests/) | Unit tests |
| [Dockerfile](Dockerfile) | Container image |
| [CONTAINER.md](CONTAINER.md) | Deployment contract |
| [EVENTS.md](EVENTS.md) | Event catalog |
