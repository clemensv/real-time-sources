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
- **Use a retrying HTTP session for pollers.** For `requests`-based pollers, mount an `HTTPAdapter` with bounded `urllib3.Retry` handling for transient connect, read, 429, and 5xx failures. A plain `requests.Session()` with no retry policy is too brittle for long-running bridges.
- Normalize upstream payloads into generated data classes.
- **Map upstream field names to schema field names in the bridge.** If the xreg schema uses `station_id` but the upstream JSON returns `id`, the bridge must remap: `s['station_id'] = s.pop('id', '')`. The same applies to non-English upstream names (e.g. `id_stacji` → `station_id`).
- Pass subject or key placeholder values explicitly as positional arguments to the generated producer's send method. **Never use custom `key_mapper` lambdas** — they bypass contract validation and cause E2E key-format failures.
- **Parse datetime strings properly.** Use `datetime.datetime.fromisoformat()` for ISO timestamps. Do not pass raw strings to fields typed as `datetime.datetime` in the generated data classes — the Avro serializer will reject them.
- Handle state and dedupe where the source is polled or replayable.
- **Isolate upstream failures to the smallest practical unit.** One failed dataset, endpoint, station batch, or reference-detail call must not abort the whole poll cycle if other work can continue. Skip the failing slice, log it, and continue with the rest of the cycle.
- **Preserve cached reference metadata when refresh fails.** Do not clear station, community, site, route, or timeseries catalogs before the new refresh succeeds. Build a fresh snapshot separately, swap it in only after a successful refresh, and keep using the previous cache if the refresh fails.
- **Defer state advancement until delivery is durable.** When batching producer calls with `flush_producer=False`, collect pending dedupe updates, resume cursors, and `last_seen` timestamps separately. Flush Kafka with an explicit timeout, check that `producer.flush(timeout=...)` returns `0`, and only then commit state in memory or on disk.
- Make failures obvious and recoverable.
- **Flush at sensible boundaries, and treat non-zero flush remainders as failure.** An unchecked `flush()` can leave messages queued while the bridge believes they were sent, which turns dedupe state into data loss on the next poll.
- **After any schema field rename, cascade the change end-to-end.** Regenerate producers with `generate_producer.ps1`, then update bridge code (constructor args, field mappings), and update unit tests (mock objects, assertions). A field rename touches xreg → generated data classes → generated producer methods → bridge → tests.

## Testing Checklist

- Unit tests for parsing, normalization, timestamp logic, state handling, connection string parsing, and URL construction.
- **For any bridge that batches `send_*` calls with `flush_producer=False`, add a flush-failure unit test.** Mock `producer.flush(timeout=...)` or `producer.producer.flush(timeout=...)` to return a non-zero remainder and assert that `seen_ids`, `previous_digests`, `last_seen`, resume cursors, and persisted state remain unchanged. If the runtime is supposed to retry on the next poll, assert the same records are still eligible to emit.
- Integration tests with mocked upstream responses and mocked or fake producers.
- **For HTTP pollers, add two explicit transient-failure tests.** One test must fail the reference refresh path and assert the bridge keeps using the prior cached metadata instead of clearing it. A second test must fail one dataset, endpoint, or station batch inside a multi-slice poll and assert the bridge skips only that slice while unaffected slices still emit.
- **For sources with multiple generated `*EventProducer` classes, add a one-cycle runtime wiring test.** Feed one mocked record into every emitted family, use fake producer classes per message group, and assert the bridge successfully routes each family to its corresponding producer surface. This is the test that catches `AttributeError` failures caused by importing or instantiating only the first producer class.
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
- **Marking records as seen before Kafka delivery is durable.** If the bridge calls `send_*` with `flush_producer=False`, then updates `seen_ids`, `previous_digests`, `last_seen`, or persisted state before checking the result of `producer.flush(timeout=...)`, a Kafka outage can silently drop updates forever. Stage those state changes, flush with a timeout, require a zero remainder, then commit state.
- **Emitting only telemetry when the source has reference data endpoints.** If the upstream provides station lists, sensor catalogs, or entity metadata, the bridge must fetch and emit those as reference events. Telemetry without co-streamed reference data forces consumers to fetch context out-of-band, breaking temporal consistency.
- **Not re-fetching reference data periodically.** Reference data changes over time (stations are added/moved, sensors are recalibrated, routes change). A one-time startup fetch is the minimum; periodic refresh is the correct pattern.
- **Using a plain `requests.Session()` for a long-running poller with no retry policy.** Transient connection resets and read timeouts are normal on public HTTP infrastructure. Mount bounded retries for GET-based pollers so a single upstream wobble does not fail a whole cycle immediately.
- **Clearing cached reference metadata before refresh succeeds.** If the new station or timeseries refresh fails after the old cache has been discarded, the bridge loses the ability to emit telemetry against still-valid cached entities and turns one transient failure into a full outage.
- **Letting one failing endpoint or dataset abort the rest of the poll cycle.** Multi-endpoint pollers must isolate failures per dataset, station batch, or family whenever the other slices can still emit valid events.
- Hiding required placeholder args inside ad hoc key mappers.
- **Using custom `key_mapper` lambdas to format Kafka keys.** The generated producer already accepts key template values as positional arguments. A custom `key_mapper` overrides the xreg-derived key format and will cause Docker E2E key-format validation failures (e.g. key prefix `b'<source>.'` instead of the expected template expansion). Remove all `key_mapper` code and pass key values through the generated method signature.
- **Passing raw strings to datetime-typed fields.** Generated data classes declare timestamps as `datetime.datetime`. Passing a raw ISO string causes `TypeError` or Avro serialization failure. Always parse with `datetime.datetime.fromisoformat()`.
- **Not updating bridge code after schema field renames.** If a field is renamed in the xreg (e.g. `uuid` → `station_id`) and producers are regenerated, the bridge must also be updated to use the new field name in constructors and `send_*` calls. Missing this causes `TypeError: unexpected keyword argument` at runtime.
- **Not verifying generated method names after regeneration.** Generated producer method names derive from xreg message names (e.g. `send_water_level_observation`). If the message name changes, the bridge must call the new method name. A stale method name causes `AttributeError` at runtime.
- **Assuming one generated producer class covers all message groups.** Multi-group manifests generate multiple `*EventProducer` classes, typically one per message group. If the bridge only imports or instantiates the first class and then calls `send_*` methods that belong to other classes, the runtime fails with `AttributeError` even though the methods exist in the generated package. Audit `producer.py`, import every generated producer class the runtime needs, and instantiate each against the shared Kafka client and topic.
- **Skipping a full-family wiring test on multi-group sources.** Parsing tests can all pass while the runtime still wires travel times, weather, tolls, or other families through the wrong producer instance. Add a one-cycle feed test with fake producer classes per message group so producer-surface mismatches fail in CI instead of in production logs.
