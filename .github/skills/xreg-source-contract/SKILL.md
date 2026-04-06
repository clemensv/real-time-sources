---
name: xreg-source-contract
description: Use this skill when designing or changing event contracts for this repo. Covers CloudEvents modeling, xreg message groups and schema groups, stable subject and Kafka key selection, JSON Schema and Avro details, xrcg 0.10.1 regeneration, generated producer sync, and EVENTS.md generation for new or updated sources.
argument-hint: Describe the source, the event families, the stable identifier shape, and whether multiple event families share one identity or need separate message groups.
user-invocable: true
---

This repo treats the checked-in xreg manifest as the contract source of truth. Write or update the manifest first, then regenerate the producer artifacts from it.

Hard rules for this repo:

- Every CloudEvents message must declare a `subject` metadata entry with `type: "uritemplate"`.
- Every Kafka producer endpoint must declare `protocoloptions.options.key`.
- The endpoint key template must match the CloudEvents subject template exactly.
- Choose keys from stable domain identifiers only.
- If event families use different identity shapes, split them into separate message groups or endpoints.
- JsonStructure schema `$id` values must be globally unique.
- Regenerate with `xrcg` `0.10.1` after changing subject or key modeling.

Good key and subject examples:

- `{station_id}`
- `{code_station}`
- `{agencyid}`
- `{mmsi}`
- `{agency_cd}/{site_no}`
- `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`

Bad key choices:

- Station names
- Provider display labels
- Alert headlines
- Mutable route descriptions
- Any field that changes without changing the real-world entity identity

Recommended workflow:

1. Identify the real entity or timeseries identity for each event family.
   Reference data, telemetry, and alerts often do not share the same identifier shape. Decide that before you write schema fields.

2. Decide whether one endpoint can support all event families.
   If one family keys by station and another keys by alert ID, do not force them into the same key model. Split the model cleanly.

3. Write the xreg manifest under `xreg/`.
   Define endpoints, message groups, message metadata, and schema groups in the checked-in file. Keep the manifest readable and intentional.

4. Model CloudEvents metadata deliberately.
   `type` should be stable and descriptive. `source` should identify the upstream system or transport root. `subject` should reflect the stable entity identity that the Kafka key also uses.

5. Write schemas to match the source semantics, not the current parser convenience.
   Preserve domain names where they matter. Keep required fields tight. Avoid flattening away important upstream distinctions if they matter for consumers.

6. Regenerate producer output with the source-local `generate_producer.ps1` script.
   That script should validate `xrcg` version and refresh the generated producer package from the checked-in manifest.

7. Sync runtime wrappers after generation.
   In this repo, generated output and runtime wrappers can drift. After regenerating, update any in-app `producer_client.py` or top-level runtime producer module so CloudEvents subject and default Kafka key behavior stay aligned with the manifest.

8. Refresh event documentation.
   `EVENTS.md` should be generated from the manifest, usually via `tools/printdoc.py` or `tools/generate-events-md.ps1`.

Validation checklist:

- `subject` exists on every emitted event definition.
- `protocoloptions.options.key` exists on every Kafka endpoint.
- Subject and key templates match exactly.
- Generated producer method signatures expose the placeholder values the runtime needs.
- Generated producer tests assert the expected Kafka key behavior.
- Sample code passes placeholder arguments instead of hiding them.
- Runtime code still composes the same identity when calling the producer.

Use a nearby source with the same identity pattern as a reference:

- Station-keyed hydrology sources: `chmi-hydro`, `imgw-hydro`, `hubeau-hydrometrie`, `waterinfo-vmm`
- Vessel-keyed streaming sources: `aisstream`, `digitraffic-maritime`, `kystverket-ais`
- Agency-keyed transit sources: `gtfs`
- Mixed-family sources that may need multiple message groups: `dwd`, `entsoe`

Avoid these mistakes:

- Treating `subject` as optional decoration.
- Reusing one schema `$id` across multiple event types.
- Hand-editing generated producer code instead of fixing the manifest and regenerating.
- Leaving the runtime wrapper on an older producer contract after a key change.