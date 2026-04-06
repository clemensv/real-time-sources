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
- **The bridge must emit reference data as events, not just telemetry.** If the xreg contract defines reference event types (station metadata, sensor catalogs, zone definitions, route tables, task type catalogs), the bridge must fetch that data via REST at startup and emit it as CloudEvents before or alongside the telemetry stream. Reference data should be re-fetched periodically (typically every few hours or daily, depending on the source) so downstream consumers can maintain temporally consistent views. Reference data goes to the same Kafka topic as the telemetry it contextualizes, using the same key model. Repo analogs: `pegelonline` (stations at startup), `usgs-iv` (sites refreshed weekly), `chmi-hydro` (stations before observations), `noaa-ndbc` (buoy stations). See: https://vasters.com/clemens/2024/10/30/streamifying-reference-data-for-temporal-consistency-with-telemetry-events
- Runtime work for a new source is not complete until the relevant repo-level Docker E2E test passes when the source is meant to participate in the shared container test suite.
- If Docker E2E reports key, subject, or JsonStructure schema failures, treat that as contract or runtime drift and fix the source instead of weakening the test.
- When Docker E2E evidence is needed for manual verification or debugging, the harness must support an explicit opt-in parameter that writes consumed Kafka messages and container logs to disk.

## Procedure

1. Choose the runtime pattern that matches the source: poller, websocket, MQTT, or raw TCP.
2. Structure the bridge using the runtime patterns in [runtime checklist](references/runtime-checklist.md).
3. Parse source configuration and Kafka configuration from CLI args and environment variables.
4. **Emit reference data first.** If the contract defines reference event types, fetch the metadata via REST at startup and emit it as CloudEvents before entering the telemetry loop. Track when reference data was last emitted and re-fetch periodically (interval depends on the source's metadata volatility). Reference events use the same producer topic and key model as the related telemetry.
5. Normalize upstream payloads into the correct generated data classes per family and pass subject or key placeholders explicitly, matching the xreg-declared shape and nullability rules, while consuming the generated producer packages unchanged.
6. Add state, dedupe, reconnect, and emit-order behavior where the source requires it without erasing family-specific meaning.
7. Add unit and integration tests, and keep Docker compatibility in mind if the source should join the repo-wide container tests.
8. **Update Docker E2E test to validate both reference and telemetry event types.** Use `reference_types` and `telemetry_types` parameters in `_run_kafka_flow_test` to verify both categories are emitted.
9. Run the relevant Docker E2E test and treat failures there as unfinished implementation work, not optional follow-up.

## Outputs

- a runtime bridge aligned with the xreg contract
- reference data emission at startup (and periodic refresh) for sources that define reference types
- consistent producer calls with explicit placeholder values
- source-local tests that cover parsing, state, and emission behavior
- a passing repo-level Docker E2E test when the source participates in the shared container suite

## References

- [Runtime checklist](references/runtime-checklist.md)