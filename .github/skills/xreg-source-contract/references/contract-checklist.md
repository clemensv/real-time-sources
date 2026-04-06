# Contract Checklist

## Hard Rules

- Every CloudEvents message must declare a `subject` metadata entry with `type: "uritemplate"`.
- Every Kafka producer endpoint must declare `protocoloptions.options.key`.
- The endpoint key template must match the CloudEvents subject template exactly.
- Choose keys from stable domain identifiers only.
- If event families use different identity shapes, split them into separate message groups or endpoints.
- JsonStructure schema `$id` values must be globally unique.
- Regenerate with `xrcg` `0.10.1` after changing subject or key modeling.
- **Enumerate all upstream data channels before deciding which families to model.** Walk the full API index, MQTT topic namespace, or OpenAPI tag list. Missing event families because the audit stopped too early is a contract failure.
- **Model reference data as event types when upstream provides metadata endpoints.** If the upstream exposes station lists, sensor catalogs, zone definitions, route tables, vessel registries, or task type catalogs, model those as named reference event types in the same message group as the telemetry they contextualize. Reference and telemetry events share the same key model and Kafka topic. Do not omit reference data just because it updates slowly.

## Good Key And Subject Examples

- `{station_id}`
- `{code_station}`
- `{agencyid}`
- `{mmsi}`
- `{agency_cd}/{site_no}`
- `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}`

## Bad Key Choices

- Station names
- Provider display labels
- Alert headlines
- Mutable route descriptions
- Any field that changes without changing the real-world entity identity

## Validation Points

- `subject` exists on every emitted event definition.
- `protocoloptions.options.key` exists on every Kafka endpoint.
- Subject and key templates match exactly.
- Generated producer method signatures expose the placeholder values the runtime needs.
- Generated producer tests assert the expected Kafka key behavior.
- Sample code passes placeholder arguments instead of hiding them.
- Runtime code still composes the same identity when calling the producer.
- **Reference event types exist for every telemetry family that has upstream metadata endpoints.** If the upstream provides station metadata, sensor catalogs, or entity registries, the manifest must include corresponding reference event types.

## Useful Repo Analogs

- Station-keyed hydrology sources: `chmi-hydro`, `imgw-hydro`, `hubeau-hydrometrie`, `waterinfo-vmm`
- Vessel-keyed streaming sources: `aisstream`, `digitraffic-maritime`, `kystverket-ais`
- Agency-keyed transit sources: `gtfs`
- Mixed-family sources that may need multiple message groups: `dwd`, `entsoe`

## Common Mistakes

- Treating `subject` as optional decoration.
- Reusing one schema `$id` across multiple event types.
- Hand-editing generated producer code instead of fixing the manifest and regenerating.
- Leaving the runtime wrapper on an older producer contract after a key change.
- **Omitting reference data event types.** If the upstream has station lists, sensor catalogs, or entity metadata, those must be modeled as events. Omitting them forces consumers to fetch context out-of-band, breaking temporal consistency.
- **Stopping the upstream audit after the first few obvious families.** Walk every API doc subsection, every MQTT topic tree, every REST collection. Missing families is a contract failure.