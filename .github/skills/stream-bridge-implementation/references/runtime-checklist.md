# Runtime Checklist

## Runtime Patterns

- Poller: Periodic HTTP or file fetch, delta detection, reference data at startup or refresh intervals, telemetry on each cycle.
- Websocket or MQTT client: Long-lived connection, reconnect loop, backoff, optional resume cursor or subscription filter. Reference data fetched via REST at startup and periodically refreshed alongside the live stream.
- Raw TCP decoder: Socket management, framing or sentence reassembly, decode pipeline, reconnect and backpressure handling.

## Common Runtime Structure

- Core logic usually lives in `<source>/<source>.py`, `<source>/bridge.py`, or a similarly named module under the source package.
- Generated producer code is checked in under `<source>_producer/`, `<source>_producer_tmp/`, or a paired runtime wrapper like `producer_client.py`.
- Source-specific auth comes from source env vars such as API keys or tokens.
- Kafka output must work with either explicit SASL credentials or a single `CONNECTION_STRING`.

## Implementation Checklist

- Parse source configuration and Kafka configuration from CLI args and environment variables.
- **Fetch and emit reference data at startup.** If the xreg contract defines reference event types (station metadata, sensor lists, zone definitions, route tables), fetch them via REST before entering the telemetry loop. Emit each reference record as a CloudEvent using the generated producer's send method, with the same key model as the related telemetry. Flush after the reference batch.
- **Re-fetch reference data periodically.** Track when reference data was last emitted and re-fetch at a cadence appropriate to the source (e.g. every few hours for station metadata, weekly for slowly changing catalogs). This ensures downstream consumers can maintain temporally consistent views of the entities telemetry describes.
- Normalize upstream payloads into generated data classes.
- Pass subject or key placeholder values explicitly.
- Handle state and dedupe where the source is polled or replayable.
- Make failures obvious and recoverable.
- Flush at sensible boundaries.

## Testing Checklist

- Unit tests for parsing, normalization, timestamp logic, state handling, connection string parsing, and URL construction.
- Integration tests with mocked upstream responses and mocked or fake producers.
- Optional real-upstream e2e tests when credentials are practical.
- Docker-compatible sources should also behave under `tests/docker_e2e/`.

## Docker Flow Compatibility

- `CONNECTION_STRING=BootstrapServer=host:port;EntityPath=topic`
- `KAFKA_ENABLE_TLS=false`

## Useful Repo Analogs

- Delta-state pollers: `noaa`, `rws-waterwebservices`, `waterinfo-vmm`, `hubeau-hydrometrie`
- Websocket or MQTT bridges: `aisstream`, `bluesky`, `digitraffic-maritime`
- Raw TCP decode: `kystverket-ais`
- Large multi-family pollers: `dwd`, `gtfs`, `entsoe`
- Reference-first emission pattern: `pegelonline` (stations at startup), `chmi-hydro` (stations before observations), `noaa-ndbc` (buoy stations at startup)
- Periodic reference refresh: `usgs-iv` (site metadata refreshed weekly per state)

## Reference Data Emission Pattern

The standard pattern for reference data emission, used across this repo:

1. **At startup**, before the telemetry loop:
   - Fetch all reference records via REST (e.g. station list, sensor catalog)
   - Emit each as a CloudEvent using the generated producer's send method
   - Use the same Kafka topic and key model as telemetry
   - Flush the producer after the reference batch
2. **Periodically** (every N hours or days):
   - Re-fetch and re-emit reference data
   - Track last-emitted timestamp to avoid unnecessary re-fetches
3. **Key principle**: Reference data and telemetry differ only in update frequency, not fundamental nature. Both must be time-stamped events so consumers can reconstruct the state of any entity at any point in time.

See: https://vasters.com/clemens/2024/10/30/streamifying-reference-data-for-temporal-consistency-with-telemetry-events

## Common Mistakes

- Deriving Kafka keys differently in runtime code and generated producer wrappers.
- Advancing state before messages are emitted successfully.
- **Emitting only telemetry when the source has reference data endpoints.** If the upstream provides station lists, sensor catalogs, or entity metadata, the bridge must fetch and emit those as reference events. Telemetry without co-streamed reference data forces consumers to fetch context out-of-band, breaking temporal consistency.
- **Not re-fetching reference data periodically.** Reference data changes over time (stations are added/moved, sensors are recalibrated, routes change). A one-time startup fetch is the minimum; periodic refresh is the correct pattern.
- Hiding required placeholder args inside ad hoc key mappers.