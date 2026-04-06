---
name: bootstrap-real-time-source
description: "Use when planning or adding a new real-time source in this repo. Covers mandatory upstream docs and field review, required JSON Structure Core and extension-spec study for schema work, repo fit, transport choice, event-family scoping, folder layout, and sequencing xreg, runtime, container, and documentation work."
argument-hint: "Describe the upstream source, transport, auth model, cadence, stable identifiers, and expected event families."
---

# Bootstrap Real-Time Source

## When to Use

- Add a brand-new source folder to this repo.
- Turn a rough source idea into an ordered implementation plan.
- Choose the right repo analog before writing xreg or runtime code.

## Inputs

- Upstream source name and endpoint
- transport, auth, refresh cadence, replay behavior, and expected volume
- stable identifiers and expected reference, telemetry, or alert families

## Non-Negotiables

- Do not infer the contract from one convenient list payload and call it done.
- Read the upstream docs or OpenAPI and inspect representative live payloads before you name event families or schemas.
- **Enumerate every available data channel exhaustively.** List every MQTT topic tree, every REST collection endpoint, every WebSocket channel, and every file feed the upstream exposes. Do not stop at the first two obvious families. Walk the full upstream API index page, topic namespace, or OpenAPI tag list and confirm each channel was reviewed. If the upstream docs have a "Data" or "MQTT" section, read every subsection, not just the ones that sound familiar. Probe topics you are unsure about with live requests. Produce an explicit hit list of every data family the source offers, then justify keeping or dropping each one before proceeding to contract authoring.
- If the source will require JsonStructure schema work, read JSON Structure Core and the relevant extension specs during planning; they are part of the required curriculum for this workflow.
- Collect the upstream field descriptions, units, aliases, enums, and validation rules before you hand off schema work; payload shape alone is not enough.
- If the source exposes detail endpoints, subtype enums, or `display_type`-style discriminators, review them before deciding anything about family boundaries.
- Flattening semantically different upstream entities into one generic catch-all item is a modeling error, not an acceptable simplification.
- **Every source that exposes reference data must emit it as events.** Reference data (station metadata, sensor catalogs, route definitions, zone lists, vessel registries, task type catalogs) is not fundamentally different from telemetry; it differs only in update frequency. Treating reference data as out-of-band context that consumers must fetch themselves breaks temporal consistency in downstream analytics. Model reference data as named event types in the xreg manifest, fetch it via REST at bridge startup (and periodically thereafter), and emit it as CloudEvents into the same Kafka topic(s) as the telemetry it contextualizes. The reference article for this pattern is: https://vasters.com/clemens/2024/10/30/streamifying-reference-data-for-temporal-consistency-with-telemetry-events
- Plan to consume `xrcg` output as generated. Do not design a source around post-generation Python edits, vendored rewrites, or import-fixup scripts as a normal integration step.
- If the upstream review is not strong enough to support exhaustive field descriptions in the eventual schemas, the source is not ready for contract authoring.
- A new source is not done when the manifest generates or the unit tests pass; it is done when the source's repo-level Docker E2E test is passing if the source is expected to ship as a containerized bridge.

## Procedure

1. Study the authoritative upstream docs, read JSON Structure Core and the relevant extension specs if the source will need schema work, and inspect representative live list and detail payloads, then identify the stable domain identity and extract the field descriptions, units, aliases, enums, and validation rules the schema will need.
2. **Enumerate all available data channels.** Walk the full upstream API index, MQTT topic namespace, WebSocket message types, or OpenAPI tag list. For each channel, probe a live payload to confirm its shape and volume. Produce an explicit table of every data family with columns: family name, transport (MQTT topic / REST endpoint / WS channel), identity shape, update cadence, and keep/drop decision with justification. This table is a gate: do not proceed to contract authoring until it is complete.
3. **Identify reference data.** For every telemetry family, determine whether the upstream provides metadata about the entities that telemetry describes (stations, sensors, vehicles, zones, routes, task types). If so, plan a reference data event type that will be fetched via REST at startup and periodically refreshed. Reference data and telemetry share the same key model and go to the same Kafka topic so consumers can build temporally consistent views. If the upstream provides no useful metadata endpoint, document that explicitly.
4. Choose the closest repo pattern from [bootstrap checklist](references/bootstrap-checklist.md).
5. Decide whether the source should be a poller, websocket client, MQTT consumer, or raw TCP bridge.
6. Split the source into event families (including reference types) and determine whether their identities can share one message group, preserving meaningful upstream schema and subtype distinctions unless you can prove they are semantically identical.
7. Lay out the source folder using the scaffold in [bootstrap checklist](references/bootstrap-checklist.md).
8. Use `xreg-source-contract` for contract work, `stream-bridge-implementation` for runtime work, and `container-and-delivery` for packaging and documentation.
9. Treat the source as incomplete until its expected repo-level Docker E2E coverage is passing.

## Outputs

- a scoped source plan
- a chosen analog source
- a project layout
- a stable identity model
- an ordered work breakdown

## References

- [Bootstrap checklist](references/bootstrap-checklist.md)
- JSON Structure Core: https://json-structure.github.io/core/draft-vasters-json-structure-core.html
- JSON Structure Alternate Names and Descriptions: https://json-structure.github.io/alternate-names/draft-vasters-json-structure-alternate-names.html
- JSON Structure Symbols, Scientific Units, and Currencies: https://json-structure.github.io/units/draft-vasters-json-structure-units.html
- JSON Structure Validation Extensions: https://json-structure.github.io/validation/draft-vasters-json-structure-validation.html
- JSON Structure Conditional Composition: https://json-structure.github.io/conditional-composition/draft-vasters-json-structure-cond-composition.html
- JSON Structure Import: https://json-structure.github.io/import/draft-vasters-json-structure-import.html