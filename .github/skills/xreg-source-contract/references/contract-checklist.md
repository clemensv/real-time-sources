# Contract Checklist

## Hard Rules

- Every CloudEvents message must declare a `subject` metadata entry with `type: "uritemplate"`.
- Every Kafka producer endpoint must declare `protocoloptions.options.key`.
- The endpoint key template must match the CloudEvents subject template exactly.
- Choose keys from stable domain identifiers only.
- If event families use different identity shapes, split them into separate message groups or endpoints.
- JsonStructure schema `$id` values must be globally unique.
- Regenerate with `xrcg` `0.10.1` after changing subject or key modeling.

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