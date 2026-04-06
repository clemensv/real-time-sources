---
name: stream-bridge-implementation
description: Use this skill when implementing the runtime bridge for a source in this repo. Covers API pollers, websocket clients, MQTT consumers, raw TCP decoders, state and dedupe logic, CLI and environment configuration, generated producer wiring, CloudEvents emission order, and source-local test strategy.
argument-hint: Describe the transport, auth, polling or reconnect behavior, resume state needs, and the event families the runtime must emit.
user-invocable: true
---

Implement the runtime only after the xreg contract and generated producer surface are clear. The bridge exists to turn upstream data into the checked-in event contract, not the other way around.

Pick the correct runtime pattern:

- Poller: Periodic HTTP or file fetch, delta detection, reference data at startup or refresh intervals, telemetry on each cycle.
- Websocket or MQTT client: Long-lived connection, reconnect loop, backoff, optional resume cursor or subscription filter.
- Raw TCP decoder: Socket management, framing or sentence reassembly, decode pipeline, reconnect and backpressure handling.

Common runtime structure in this repo:

- Core logic usually lives in `<source>/<source>.py`, `<source>/bridge.py`, or a similarly named module under the source package.
- Generated producer code is checked in under `<source>_producer/`, `<source>_producer_tmp/`, or a paired runtime wrapper like `producer_client.py`.
- Source-specific auth comes from source env vars such as API keys or tokens.
- Kafka output must work with either explicit SASL credentials or a single `CONNECTION_STRING`.

Implementation expectations:

1. Parse configuration from CLI args and environment variables.
   Source-specific credentials should have source-specific env var names. Kafka connection settings should follow repo conventions.

2. Normalize upstream payloads into generated data classes.
   Keep transformation logic explicit. Avoid leaking raw upstream dicts deep into the producer path when a typed generated model exists.

3. Pass subject or key placeholder values explicitly.
   If the generated producer method requires `_station_id`, `_agencyid`, `_mmsi`, or similar placeholder arguments, derive them once from the normalized record and pass them directly.

4. Handle state and dedupe where the source is polled or replayable.
   Persist checkpoints in `STATE_FILE` or a source-local equivalent. Advance state only after successful emission. Follow the NOAA and water-level bridge patterns for delta-oriented polling.

5. Emit reference data intentionally.
   If the source has station, site, zone, or vessel metadata, send that data at startup or on a predictable cadence before telemetry, because the repo-wide container tests often validate both reference and telemetry behavior.

6. Make failures obvious and recoverable.
   Use timeouts, retries, reconnect loops, and logging that makes upstream and Kafka failures diagnosable without exposing secrets.

7. Flush at sensible boundaries.
   Pollers usually flush at the end of a cycle or after a batch. Continuous streams may flush on batch boundaries or leave delivery to the producer configuration, but the behavior should be deliberate.

Transport-specific guidance:

- Pollers should separate fetch, parse, dedupe, and emit stages.
- Websocket and MQTT clients should separate frame handling from event normalization.
- TCP pipelines should isolate framing or sentence assembly from message decoding and event emission.
- Sources with upstream cursors or offsets should persist that resume state distinctly from entity-level dedupe state.

Testing expectations:

- Unit tests for parsing, normalization, timestamp logic, state handling, connection string parsing, and URL construction.
- Integration tests with mocked upstream responses and mocked or fake producers.
- Optional real-upstream e2e tests when credentials are practical. Mark them clearly.
- Container-ready sources should also behave under the repo-wide Docker tests in `tests/docker_e2e/`.

For Docker flow compatibility, the container should be able to run against plain Kafka with:

- `CONNECTION_STRING=BootstrapServer=host:port;EntityPath=topic`
- `KAFKA_ENABLE_TLS=false`

Use nearby sources as runtime examples:

- Delta-state pollers: `noaa`, `rws-waterwebservices`, `waterinfo-vmm`, `hubeau-hydrometrie`
- Websocket or MQTT bridges: `aisstream`, `bluesky`, `digitraffic-maritime`
- Raw TCP decode: `kystverket-ais`
- Large multi-family pollers: `dwd`, `gtfs`, `entsoe`

Avoid these mistakes:

- Deriving Kafka keys differently in runtime code and generated producer wrappers.
- Advancing state before messages are emitted successfully.
- Emitting telemetry only when the source is supposed to publish reference data too.
- Hiding required placeholder args inside ad hoc key mappers.