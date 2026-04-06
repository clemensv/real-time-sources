# Runtime Checklist

## Runtime Patterns

- Poller: Periodic HTTP or file fetch, delta detection, reference data at startup or refresh intervals, telemetry on each cycle.
- Websocket or MQTT client: Long-lived connection, reconnect loop, backoff, optional resume cursor or subscription filter.
- Raw TCP decoder: Socket management, framing or sentence reassembly, decode pipeline, reconnect and backpressure handling.

## Common Runtime Structure

- Core logic usually lives in `<source>/<source>.py`, `<source>/bridge.py`, or a similarly named module under the source package.
- Generated producer code is checked in under `<source>_producer/`, `<source>_producer_tmp/`, or a paired runtime wrapper like `producer_client.py`.
- Source-specific auth comes from source env vars such as API keys or tokens.
- Kafka output must work with either explicit SASL credentials or a single `CONNECTION_STRING`.

## Implementation Checklist

- Parse source configuration and Kafka configuration from CLI args and environment variables.
- Normalize upstream payloads into generated data classes.
- Pass subject or key placeholder values explicitly.
- Handle state and dedupe where the source is polled or replayable.
- Emit reference data intentionally when the source has station, site, zone, or vessel metadata.
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

## Common Mistakes

- Deriving Kafka keys differently in runtime code and generated producer wrappers.
- Advancing state before messages are emitted successfully.
- Emitting telemetry only when the source is supposed to publish reference data too.
- Hiding required placeholder args inside ad hoc key mappers.