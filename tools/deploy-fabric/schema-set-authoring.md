# Generate a Fabric Event Schema Set

[generate_schema_set.py](./generate_schema_set.py) assembles portable Event
Schema Set definitions from local xRegistry manifests. It does not create
Fabric resources, fetch remote schemas, or record deployment identities.

Install the authoring dependencies in a dedicated Python environment:

```powershell
python -m pip install -r tools\deploy-fabric\requirements-schema-set.txt
```

## Select existing Avro variants

```powershell
python tools\deploy-fabric\generate_schema_set.py `
  --registry <registry.xreg.json> `
  --messagegroup <avro-message-group> `
  --definition <EventSchemaSetDefinition.json>
```

Repeat `--messagegroup` for additional event families. The command resolves
`basemessageuri` inheritance, including metadata overrides, and preserves the
inherited CloudEvents wire type. It resolves local `#/`, `/`, and `xreg://./`
references. Unresolved references, inheritance cycles, duplicate wire types and
conflicting schema IDs are errors.

Schema references select their explicit version, or the schema resource's
`defaultversionid`. Override a selection with
`--schema-version "#/schemagroups/<group>/schemas/<schema>=<version>"`.
There is no "highest version" heuristic. Only the selected schema version is
included by default. Add `--include-history` to retain other Avro versions of
selected resources. Version selection for Eventstream association and runtime
URI bindings remains a separate deployment step.

Avro roots must be records. A bundle of named records needs
`--root-record "#/schemagroups/<group>/schemas/<schema>=<qualified-record-name>"`.
Avrotize inlines named dependencies and fastavro validates each resulting record.
Schema strings use deterministic compact JSON. Resource and version order follow
the input; repeated runs with the same input produce identical output.

CloudEvents envelope templates are not fixed values on the wire. The tool removes
template-valued attributes and converts source/dataschema to URI types and subject
to string. Literal metadata values and descriptions remain intact.
This command targets JSON payloads; a declared non-JSON content type is rejected.
An Avro schema declaration alone does not prove that a producer's JSON payload
matches it. Compare nullable fields, timestamps and enums with the actual serializer.

## Construct missing variants

For JSON Structure contracts without suitable Avro variants:

```powershell
python tools\deploy-fabric\generate_schema_set.py `
  --registry <canonical.xreg.json> `
  --messagegroup <base-message-group> `
  --schema-version "#/schemagroups/<group>/schemas/<schema>=<source-version>" `
  --projected-version "#/schemagroups/<group>/schemas/<schema>=<new-projection-version>" `
  --create-avro-variants `
  --output-registry <derived.xreg.json> `
  --definition <EventSchemaSetDefinition.json>
```

Supply a projected version for every converted schema. Versions are explicit
contract decisions, never inferred from event names. The tool runs the pinned
Avrotize 3.9.6 `s2a --no-custom-logical-types` converter and adds
`<base-message-group>.avro` messages and
`<base-message-group>.avro.json` schemas. Each variant inherits its base message,
pins the new schema version and retains JSON content type. Original collections,
endpoints, key templates and subjects are unchanged. Existing target groups are
never overwritten; select them directly instead.

Use the base schema's `name`, or `--root-record` for ambiguous conversion bundles.
The upstream option moves custom logical-type annotations to
`x-original-logical-type` without changing the underlying Avro types. Standard
logical types remain intact. No local datatype, enum, nullability or datetime
transformations run here.
JSON Structure remains authoritative for constraints not enforced by Avro readers.
There is no provenance sidecar.

## Converter and Fabric limitations

For existing Avro inputs, nonstandard logical types remain unchanged and produce
an explicit warning for the selected version. Avro requires readers to ignore unknown logical types,
but Fabric has rejected `rfc3339-timestamp-millis`. A successful generation command
is not proof of Fabric ingestion.

[clemensv/avrotize#571](https://github.com/clemensv/avrotize/issues/571) is resolved
in Avrotize 3.9.6 by `--no-custom-logical-types`. JSON Structure conversion uses
that option automatically because this command targets Fabric JSON-wire schemas.
[clemensv/avrotize#581](https://github.com/clemensv/avrotize/issues/581) was closed:
xRegistry selection and Fabric definition assembly are implemented here instead.

For the retained Pegelonline pilot, use the existing
[derived registry](../../feeders/pegelonline/fabric/schematized/pegelonline.fabric.xreg.json).
The shared command reproduces its schema strings without altering fingerprints.
The same schema strings can now also be regenerated directly from the canonical
JSON Structure schemas, including the datetime annotation, without local patches.
Use projected versions `1` for Station and `2` for CurrentMeasurement as documented
in the [pilot guide](../../feeders/pegelonline/fabric/schematized/README.md).

Review generated contracts and verify genuine events at the registered receiver,
paired KQL database and custom output before accepting a new projection. Keep
workspace IDs, schema URLs, schedules and acceptance evidence outside the checkout.

## Tests

```powershell
python -m pytest tools\tests\test_generate_schema_set.py --no-cov -q
```
