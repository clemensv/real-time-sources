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
This command supports JSON and raw Avro payloads. Existing content-type metadata
is preserved unless `--payload-encoding json|avro` is supplied. That option
changes metadata, not the selected Avro schema or its fingerprint. Raw Avro uses
`application/vnd.apache.avro+avro`, without OCF or Confluent framing.
An Avro schema declaration alone does not prove that a producer's JSON payload
matches it. Compare nullable fields, timestamps and enums with the actual serializer.

## Generate dual-encoding Python data classes

Add `--python-data-output <package-directory> --python-package <package_name>`
to generate data classes from the selected Avro records through Avrotize with
both JSON and Avro binary encoders enabled. This writes an installable generated
package; it does not change message producers or choose a runtime encoding.
Do not combine this option with `--include-history`: one schema version per
record must define the runtime type. Both encoders use the same selected schema,
including its timestamp representation and nullability.

The pinned Avrotize revision includes the 3.9.7 packaging fix for
[clemensv/avrotize#585](https://github.com/clemensv/avrotize/issues/585), so
generated packages declare their Avro runtime dependency without a local patch.
Regenerate packages rather than editing their generated manifests.
It also includes the nullable-zero correction in
[clemensv/avrotize#592](https://github.com/clemensv/avrotize/pull/592).
The official 3.9.7 release still corrupts nullable zeros; use the exact
Git revisions in the dependency manifest until corrected releases are available.
The pinned xrcg revision reports `0.11.2.dev6` and includes
[xregistry/codegen#712](https://github.com/xregistry/codegen/pull/712).

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
Avrotize `s2a --no-custom-logical-types` converter and adds
`<base-message-group>.avro` messages and
`<base-message-group>.avro.json` schemas. Each variant inherits its base message,
pins the new schema version and uses the selected payload content type. The
historical `.avro.json` schema-group name does not select the wire encoding. Original collections,
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
that option automatically for Fabric-compatible Avro schema representations.
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

## Bind a deployed notebook

Schema generation does not bind physical schema URLs. After registration and
association with the exact Eventstream source, the deployment operator resolves
the selected versions, verifies their fingerprints and obtains exact
service-issued version URLs. The shared
[resolve_schema_bindings.py](./resolve_schema_bindings.py) performs the
read-only check with the explicitly selected `az_m` or `az_b` operator profile.
Its Python API also accepts the caller's approved token callback. It verifies
registered content type, matching history serialization, identical source/history
schema-set/version selections and per-schema typed storage for every family.
If the named profile shim is absent, the command invokes Azure CLI with the
corresponding process-local `AZURE_CONFIG_DIR`; it never switches accounts.
The original pilot resolver remains available for its existing callers; fleet
deployment uses the shared tool without a Pegelonline runtime dependency.

Write the event-type-keyed `SCHEMA_BINDINGS` selection as external JSON. Each
entry contains the original `source_uri`, explicit `projected_version` and
compact-schema `schema_sha256`. Then resolve against the associated source:

```powershell
python -m pip install -r tools\deploy-fabric\requirements-migration.txt
python tools\deploy-fabric\resolve_schema_bindings.py `
  --workspace-id <workspace-id> --eventstream-id <eventstream-id> `
  --source-id <source-node-id> `
  --expected-bindings <operator-directory>\expected-bindings.json `
  --payload-encoding <json-or-avro> --azure-profile <az_m-or-az_b> `
  --output <operator-directory>\resolved-map.json
```

Provider-specific metadata access must already be approved. A denial is a
blocker; this tool does not change identities, fetch broker keys, register
schemas or mutate the pipeline. Cross-workspace schema sets remain unsupported.

Write the resulting original-URI-keyed map to an external operator file, then:

```powershell
python tools\deploy-fabric\bind_notebook_schemas.py `
  --notebook feeders\pegelonline\notebook\pegelonline-feed.ipynb `
  --resolved-map <operator-directory>\resolved-map.json `
  --payload-encoding <json-or-avro> `
  --output <operator-directory>\deployed-notebook.ipynb
```

For an existing complete Notebook definition, use
[bind_notebook_definition.py](./bind_notebook_definition.py) instead. Supply its
`parts` object exported through the Fabric definition API, not just the notebook
content. It retains unknown fields and every other part and rejects a missing
Spark kernel, the wrong Environment or absent Lakehouse/database dependencies:

```powershell
python tools\deploy-fabric\bind_notebook_definition.py `
  --definition <operator-directory>\notebook-definition.json `
  --resolved-map <operator-directory>\resolved-map.json `
  --payload-encoding <json-or-avro> --environment-id <environment-id> `
  --output <operator-directory>\bound-notebook-definition.json
```

This is a preparation tool, not a deployer. Upload through the approved API
path, complete asynchronous publication, and read back all parts and bindings.
It does not qualify the legacy deployment scripts or apply KQL ingestion DDL.

The binder validates exact source-URI coverage and HTTPS version-URL shape,
replaces the single `deployment-dataschema-overrides` code cell and compiles
all code cells. It does not resolve service metadata or verify fingerprints
itself; those checks must succeed before supplying the map. Redeployment
replaces rather than duplicates the cell. Never edit the checked-in notebook
with physical URLs or put credentials in the mapping file. Before binding,
read back the registered `datacontenttype` and every selected history destination's
`inputSerialization.type`: JSON requires `Json`; raw Avro requires `Avro`.
The binder records the qualified encoding but does not perform those service checks.

The portable notebook has an unbound placeholder and fails explicitly if
executed without deployment injection. The deployed run cell uses the literal
map without a schema catalog lookup. Connection credentials still come from
the public Topology API at runtime. Refresh and read back the cell when the
target source, schema set or selected versions change.
The run cell rejects a payload encoding that differs from the injected binding
and requires `ONCE_MODE=True`. Changing encoding requires receiver qualification
and a newly bound notebook; changing the notebook parameter alone is insufficient.

This helper does not make the legacy shared deployer schematized-safe; preserve
the registered pipeline and Spark Environment bindings when uploading the
external deployment copy.

## Tests

```powershell
python -m pytest tools\tests\test_generate_schema_set.py --no-cov -q
```
