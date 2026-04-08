---
name: xreg-source-contract
description: "Use when designing or changing event contracts for this repo. Covers mandatory upstream schema review, required JSON Structure Core and extension-spec study, exhaustive field descriptions from upstream docs, CloudEvents modeling, xreg message groups, stable subject and Kafka key selection, JsonStructure extension usage, regeneration with xrcg 0.10.1, and EVENTS.md refresh."
argument-hint: "Describe the source, event families, stable identifier shape, and whether multiple families share one identity or need separate message groups."
---

# Xreg Source Contract

## When to Use

- Add a new xreg manifest for a source.
- Change CloudEvents subject or Kafka key modeling.
- Split one source into multiple message groups or endpoints.
- Refresh generated producers after contract changes.

## Inputs

- source name and upstream system
- event families and their stable identifiers
- desired CloudEvents types, source values, and schema formats

## Non-Negotiables

- The contract must follow upstream semantics, not the first convenient normalization.
- Do the tedious review work: read the docs or OpenAPI and inspect representative live detail payloads for every family you intend to emit.
- **Enumerate all upstream data channels before deciding which families to model.** Walk the full API index, MQTT topic namespace, or OpenAPI tag list. For each channel, probe a live payload. Produce an explicit hit list with keep/drop decisions. Missing event families because the upstream audit stopped too early is a contract failure.
- **API surface coverage must be exhaustive for all qualifying real-time and near-real-time data.** Do not stop after modeling the first obvious endpoint. If the upstream API exposes 20 data products and you model 3, that is a failure. Every data product, measurement type, observation parameter, and structured field that the upstream publishes as real-time or regularly-updated data **must** be represented in the contract — either as a distinct event type or as fields within an appropriate schema. The only acceptable reasons to drop an upstream data channel are: (1) the data is static reference material that never updates, (2) the data requires authentication credentials that are not freely available, or (3) the data is a duplicate presentation of something already modeled. "We ran out of time," "it seemed like enough," or "the first few endpoints were working" are not valid reasons to ship a partial contract. When in doubt, model it. A contract that covers 30% of the upstream API surface is not a contract — it is a demo.
- JSON Structure Core and the extension specifications are part of this skill's required curriculum, not optional background reading.
- Before authoring or revising any JsonStructure schema, read JSON Structure Core first, then read the relevant extension specs for every non-core keyword or construct you plan to use.
- Treat JSON Structure Core as the authoritative source for type-system rules, unions, `choice`, identifier constraints, `$ref`, and document-structure rules.
- Treat the Alternate Names, Units, Validation, Import, and Conditional Composition specs as the authoritative source for extension keywords and enabling rules, even where repo policy bans a feature in practice.
- Every schema and every field must carry exhaustive descriptions grounded in the upstream API docs, not placeholder prose or restatements of the field name.
- Do not collapse resource-specific shapes into one generic schema unless the upstream contract and payloads prove they are the same entity with the same lifecycle.
- If subtype signals such as enums or `display_type` values change meaning, lifecycle, or field shape, they must survive as separate event families or be explicitly justified in the design.
- If live payloads are richer than the published schema, model the stable union and document the discrepancy.
- The JsonStructure schema must match the payloads the bridge will actually emit, including whether optional fields are omitted or emitted as explicit `null` values.
- If the upstream docs provide units, aliases, enum labels, formats, bounds, or other validation rules, carry that information into the schema instead of leaving it implicit.
- Use the JSON Structure units, alternate-names, and validation extensions where they add real fidelity, such as `unit` and `symbol` for measured values, `altnames` for upstream JSON keys, `descriptions` or `altenums` for documented labels, and validation keywords for ranges, formats, patterns, or cardinality.
- Conditional composition extensions are not allowed in this repo for routine schema authoring.
- Never use `anyOf`; express nullable or alternative fields with type unions or `choice` instead.
- **`$ref` must be nested inside the `type` attribute.** Write `"type": {"$ref": "#/..."}`, never a bare `"$ref"` at the property level. json-structure 0.6.1+ enforces `SCHEMA_REF_NOT_IN_TYPE`; bare `$ref` silently passes authoring but fails Docker E2E schema validation.
- **Nullable types must exactly mirror Avro's nullability.** If the generated Avro has `["null", "double"]`, the JsonStructure schema must use `"type": ["double", "null"]`. A bare `"type": "double"` will fail the E2E test the first time the upstream sends a `null` for that field. Audit every field the upstream can reasonably emit as `null` and make it nullable in both schemas.
- **Key/subject template variables must be literal schema field names.** The template `{station_id}` requires a field named `station_id` in the data payload. If the upstream JSON uses `id`, `uuid`, or a non-English name, rename the schema field to match the template and map the upstream name in the bridge. The E2E harness resolves templates from `dict(event) | dict(data)` — mismatched names cause "Could not resolve template" failures.
- **Schema field names must be English.** When the upstream API uses non-English names (e.g. Polish `id_stacji`, Czech `vodní_tok`, French `code_station`), the xreg schema must use English equivalents. The bridge maps upstream to English names.
- **Model reference data as first-class event types.** If the upstream provides metadata about the entities telemetry describes (stations, sensors, zones, routes, vessel registries, task catalogs), those must be modeled as named event types in the manifest, not omitted because they update slowly. Reference data and telemetry differ only in update frequency. Place reference types in the same message group as the telemetry they contextualize so they share the same key model and Kafka topic, enabling temporally consistent downstream analytics. See: https://vasters.com/clemens/2024/10/30/streamifying-reference-data-for-temporal-consistency-with-telemetry-events
- Producer artifacts generated by `xrcg` must be treated as generated code, not as source files to patch. Do not hand-edit them, rewrite their imports, or vendor modified copies to make the source work.
- If the upstream docs do not describe a live field well enough to write an exhaustive field description, stop and document the docs gap rather than inventing vague text.
- Missing event types or family-specific fields because they were not reviewed is a contract failure.
- Missing field-level descriptions, missing units where the docs specify them, or missing documented validation constraints is a contract failure.

## Procedure

1. Read the authoritative upstream docs or OpenAPI, then read JSON Structure Core and the relevant extension specs, and inspect representative live list and detail payloads for each family you plan to model, extracting field descriptions, units, aliases, enums, and validation constraints as you go.
2. **Enumerate all upstream data channels** (MQTT topics, REST endpoints, WS channels, file feeds) and produce an explicit hit list with keep/drop decisions before modeling any families.
3. Identify the real entity or time-series identity for each event family.
4. **Identify reference data for each telemetry family.** If the upstream provides metadata REST endpoints for the entities telemetry describes (station lists, sensor catalogs, zone definitions, route tables, task type enums), model those as reference event types in the same message group as the telemetry they contextualize.
5. Decide whether the families can share one endpoint, key model, or schema, and require proof before introducing a shared catch-all shape.
6. Update the checked-in manifest under `xreg/` and model `type`, `source`, and `subject` deliberately.
7. Apply the repo keying rules and validation points in [contract checklist](references/contract-checklist.md).
8. Author each JsonStructure schema with exhaustive schema-level and field-level descriptions, and apply units, alternate names, and validation annotations wherever the upstream contract supports them.
9. Model nullability and alternatives with type unions or `choice`, not `anyOf` or other conditional composition features.
10. Validate any extended JsonStructure features and nullability assumptions before regeneration, because the shared Docker Kafka E2E suite will enforce them against emitted events. Specifically:
    - Confirm every `$ref` is nested inside `"type"`, not bare at the property level.
    - Confirm every field that can be `null` upstream uses a type union like `["double", "null"]`.
    - Confirm every key/subject template variable matches a literal field name in the corresponding schema.
11. Regenerate producer output with the source-local `generate_producer.ps1` script.
12. Keep runtime wiring aligned with the regenerated producer without modifying generated files; if the output cannot be consumed directly, fix the package layout or runtime integration around it instead.
13. Refresh `EVENTS.md` from the manifest and call out any docs-versus-live discrepancies that affected the model.

## Outputs

- an updated xreg manifest
- regenerated producer artifacts
- refreshed runtime wiring and event documentation

## References

- [Contract checklist](references/contract-checklist.md)
- JSON Structure Core: https://json-structure.github.io/core/draft-vasters-json-structure-core.html
- JSON Structure Alternate Names and Descriptions: https://json-structure.github.io/alternate-names/draft-vasters-json-structure-alternate-names.html
- JSON Structure Symbols, Scientific Units, and Currencies: https://json-structure.github.io/units/draft-vasters-json-structure-units.html
- JSON Structure Validation Extensions: https://json-structure.github.io/validation/draft-vasters-json-structure-validation.html
- JSON Structure Conditional Composition: https://json-structure.github.io/conditional-composition/draft-vasters-json-structure-cond-composition.html
- JSON Structure Import: https://json-structure.github.io/import/draft-vasters-json-structure-import.html