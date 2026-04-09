---
name: stream-bridge-implementation
description: "Use when implementing the runtime bridge for a source in this repo. Covers pollers, websocket or MQTT clients, raw TCP decoders, family-aware normalization, generated producer wiring, state and dedupe logic, and source-local testing."
argument-hint: "Describe the transport, auth, polling or reconnect behavior, resume state needs, and the event families the runtime must emit."
---

# Stream Bridge Implementation

## When to Use

- Implement a new runtime bridge after the xreg contract is clear.
- Refactor a runtime to align with regenerated producer output.
- Add state, dedupe, reconnect, or emit-order logic.

## Inputs

- transport type and auth model
- poll or reconnect behavior
- state and dedupe requirements
- generated producer methods and placeholder arguments
- reference data endpoints and refresh cadence

## Non-Negotiables

- The runtime is not allowed to paper over a sloppy contract.
- If generated producer methods or upstream subtype signals imply more event families than the bridge emits, stop and fix the contract first.
- Do not normalize semantically different upstream shapes into one generic dict or class just because the transport loop is shared.
- Preserve the family-specific fields and discriminators that justified the contract split in the first place.
- Do not patch, rewrite, or vendor modified copies of `xrcg`-generated producer or data-class code to make the runtime work; import and use the generated packages as emitted.
- The bridge must emit Kafka keys, CloudEvent subjects, and payload shapes that satisfy the checked-in xreg contract, including nullability behavior.
- **HTTP pollers must use bounded retry handling for transient upstream failures.** A long-running `requests` poller is not allowed to rely on a bare `requests.Session()` with no `HTTPAdapter`/`Retry` policy for connect resets, read timeouts, 429s, and 5xx responses.
- **State and dedupe must advance only after Kafka delivery succeeds.** If the bridge batches `send_*` calls with `flush_producer=False`, it must treat `producer.flush(timeout=...)` returning a non-zero remainder as a failed poll and leave dedupe state, resume cursors, `last_seen` timestamps, and persisted checkpoints untouched. Do not mark rows, incidents, or event IDs as seen before delivery is durable.
- **The bridge must emit reference data as events, not just telemetry.** If the xreg contract defines reference event types (station metadata, sensor catalogs, zone definitions, route tables, task type catalogs), the bridge must fetch that data via REST at startup and emit it as CloudEvents before or alongside the telemetry stream. Reference data should be re-fetched periodically (typically every few hours or daily, depending on the source) so downstream consumers can maintain temporally consistent views. Reference data goes to the same Kafka topic as the telemetry it contextualizes, using the same key model. Repo analogs: `pegelonline` (stations at startup), `usgs-iv` (sites refreshed weekly), `chmi-hydro` (stations before observations), `noaa-ndbc` (buoy stations). See: https://vasters.com/clemens/2024/10/30/streamifying-reference-data-for-temporal-consistency-with-telemetry-events
- **A failed reference refresh must not discard a still-usable cached catalog.** Station, site, community, route, and timeseries metadata should be refreshed into a new snapshot and swapped in only after success. If refresh fails and a prior cache exists, keep polling with the cached reference data instead of turning a transient metadata outage into a full bridge outage.
- **Multi-endpoint pollers must isolate failures to the failing slice whenever possible.** One bad dataset, station batch, endpoint, or reference-detail lookup should not abort the rest of the cycle if the remaining slices can still emit valid events.
- Runtime work for a new source is not complete until the relevant repo-level Docker E2E test passes when the source is meant to participate in the shared container test suite.
- If Docker E2E reports key, subject, or JsonStructure schema failures, treat that as contract or runtime drift and fix the source instead of weakening the test.
- When Docker E2E evidence is needed for manual verification or debugging, the harness must support an explicit opt-in parameter that writes consumed Kafka messages and container logs to disk.

## Procedure

1. Choose the runtime pattern that matches the source: poller, websocket, MQTT, or raw TCP.
2. Structure the bridge using the runtime patterns in [runtime checklist](references/runtime-checklist.md).
3. Parse source configuration and Kafka configuration from CLI args and environment variables.
4. **Emit reference data first.** If the contract defines reference event types, fetch the metadata via REST at startup and emit it as CloudEvents before entering the telemetry loop. Track when reference data was last emitted and re-fetch periodically (interval depends on the source's metadata volatility). Reference events use the same producer topic and key model as the related telemetry.
5. **For HTTP pollers, create a retrying session and design partial-failure behavior up front.** Mount bounded retries for transient GET failures, decide what constitutes one isolated slice of work (dataset, station batch, endpoint, family), and define the cached reference snapshot that can survive a failed refresh.
6. Normalize upstream payloads into the correct generated data classes per family and pass subject or key placeholders explicitly, matching the xreg-declared shape and nullability rules, while consuming the generated producer packages unchanged.
    - **Map upstream field names to English schema field names.** If the upstream JSON uses `id`, `uuid`, or non-English names (e.g. `id_stacji`), remap to the schema name (e.g. `station_id`) before constructing data classes.
    - **Parse datetime strings with `datetime.datetime.fromisoformat()`.** Do not pass raw strings to datetime-typed fields.
    - **Never use `key_mapper` lambdas.** Pass key template values as positional arguments to the generated producer send methods. Custom key mappers bypass contract validation and cause E2E key-format failures.
    - **When xrcg emits multiple `*EventProducer` classes, instantiate all of them.** Message groups generate separate producer classes. A bridge that imports or constructs only the first producer class and then calls `send_*` methods owned by other message groups will fail with `AttributeError` at runtime. Repo analogs: `dwd`, `entsoe`, `vatsim`, `wsdot`.
7. Add state, dedupe, reconnect, and emit-order behavior where the source requires it without erasing family-specific meaning.
    - **Do not mutate dedupe or resume state before a successful flush.** Collect candidate state updates during the batch, flush Kafka with an explicit timeout, verify the flush remainder is zero, and only then commit in-memory and persisted state.
    - **Build refreshed reference catalogs separately and swap them in only after success.** If the refresh fails and an older cache exists, keep using the older cache and continue polling unaffected telemetry slices.
    - **Catch upstream failures at the smallest practical boundary.** Skip the failing dataset, endpoint, or batch, log it, and continue with the rest of the cycle whenever the remaining work is still valid.
8. Add unit and integration tests, and keep Docker compatibility in mind if the source should join the repo-wide container tests.
    - **When the bridge batches sends with `flush_producer=False`, add a flush-failure unit test.** Mock `producer.flush(timeout=...)` (or `producer.producer.flush(timeout=...)`) to return a non-zero remainder and assert that dedupe state, `last_seen` markers, resume cursors, and persisted checkpoints do not advance. If the bridge retries on the next poll, assert the same records are still eligible to send.
    - **For HTTP pollers, add two resilience tests, not one vague one.** First, simulate a timeout or connection reset during reference refresh and assert that the old cached station, community, site, route, or timeseries catalog remains in use instead of being cleared. Second, simulate one failed dataset, endpoint, or station batch inside a multi-slice poll and assert that only the failing slice is skipped while unaffected slices still emit.
    - **For multi-group sources, add a one-cycle feed test that exercises every emitted family.** Mock upstream responses for each family, use fake producer classes per generated message group, and assert the runtime emits at least one event through each expected `send_*` path. This catches bridges that import or instantiate only one generated producer class and then call methods owned by another class.
9. **Update Docker E2E test to validate both reference and telemetry event types.** Use `reference_types` and `telemetry_types` parameters in `_run_kafka_flow_test` to verify both categories are emitted.
10. Run the relevant Docker E2E test and treat failures there as unfinished implementation work, not optional follow-up.

## Outputs

- a runtime bridge aligned with the xreg contract
- reference data emission at startup (and periodic refresh) for sources that define reference types
- consistent producer calls with explicit placeholder values
- source-local tests that cover parsing, state, and emission behavior
- a passing repo-level Docker E2E test when the source participates in the shared container suite

## References

- [Runtime checklist](references/runtime-checklist.md)
