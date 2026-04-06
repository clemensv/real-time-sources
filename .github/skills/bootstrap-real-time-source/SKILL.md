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
- If the source will require JsonStructure schema work, read JSON Structure Core and the relevant extension specs during planning; they are part of the required curriculum for this workflow.
- Collect the upstream field descriptions, units, aliases, enums, and validation rules before you hand off schema work; payload shape alone is not enough.
- If the source exposes detail endpoints, subtype enums, or `display_type`-style discriminators, review them before deciding anything about family boundaries.
- Flattening semantically different upstream entities into one generic catch-all item is a modeling error, not an acceptable simplification.
- Plan to consume `xrcg` output as generated. Do not design a source around post-generation Python edits, vendored rewrites, or import-fixup scripts as a normal integration step.
- If the upstream review is not strong enough to support exhaustive field descriptions in the eventual schemas, the source is not ready for contract authoring.
- A new source is not done when the manifest generates or the unit tests pass; it is done when the source's repo-level Docker E2E test is passing if the source is expected to ship as a containerized bridge.

## Procedure

1. Study the authoritative upstream docs, read JSON Structure Core and the relevant extension specs if the source will need schema work, and inspect representative live list and detail payloads, then identify the stable domain identity and extract the field descriptions, units, aliases, enums, and validation rules the schema will need.
2. Choose the closest repo pattern from [bootstrap checklist](references/bootstrap-checklist.md).
3. Decide whether the source should be a poller, websocket client, MQTT consumer, or raw TCP bridge.
4. Split the source into event families and determine whether their identities can share one message group, preserving meaningful upstream schema and subtype distinctions unless you can prove they are semantically identical.
5. Lay out the source folder using the scaffold in [bootstrap checklist](references/bootstrap-checklist.md).
6. Use `xreg-source-contract` for contract work, `stream-bridge-implementation` for runtime work, and `container-and-delivery` for packaging and documentation.
7. Treat the source as incomplete until its expected repo-level Docker E2E coverage is passing.

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