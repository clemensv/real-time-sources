# Pegelonline schematized Fabric hosting

[Source overview](../../README.md) | [Container deployment](../../CONTAINER.md) | [Event contracts](../../EVENTS.md)

This directory contains portable schema authoring artifacts and hosting
instructions, not deployment records. Keep workspace and item identities,
service-issued endpoints, run logs, acceptance receipts and schedules outside
the repository. Supply deployment bindings at runtime.

Eventstream owns KQL base-table creation from registered destination schemas.
Do not apply legacy base-table DDL, ingestion mappings, dispatch update
policies or the legacy Map hook to a schematized pipeline. The shared deployer
does not yet preserve the required schema associations and Spark Environment
bindings.

## Contract artifacts

- [Derived registry](./pegelonline.fabric.xreg.json) preserves the canonical
  registry and adds an `.avro` message group with JSON-wire-compatible schemas
  under `.avro.json`. Canonical producer migration remains separate work.
- [Event Schema Set definition](./EventSchemaSetDefinition.json) projects
  CloudEvents wire types and pinned Avro schemas.

The older canonical Avro measurement schema uses a long timestamp, while the
JSON serializer emits an ISO-8601 string. Station nullability also differs
from the JSON Structure contract. The projection derives both records from
the authoritative JSON Structure schemas and inlines named dependencies.
Both event families are preserved.

### Shared generation

Registry selection, inheritance and Fabric definition assembly belong in this
repository's [shared CLI](../../../../tools/deploy-fabric/generate_schema_set.py).
[clemensv/avrotize#581](https://github.com/clemensv/avrotize/issues/581) was closed
because it assigned those tasks to the wrong repository. Avrotize owns schema
conversion; its portable datetime option shipped in Avrotize 3.9.6 and resolves
[clemensv/avrotize#571](https://github.com/clemensv/avrotize/issues/571).

Generate a definition from the retained, validated Avro variants:

```powershell
python -m pip install -r tools\deploy-fabric\requirements-schema-set.txt
python tools\deploy-fabric\generate_schema_set.py `
  --registry feeders\pegelonline\fabric\schematized\pegelonline.fabric.xreg.json `
  --messagegroup de.wsv.pegelonline.avro `
  --include-history `
  --definition <operator-directory>\EventSchemaSetDefinition.json
```

The schema strings reproduce the checked-in definition byte for byte, including
historical versions and the selected Measurement version `2`. Wire types inherit
from the base messages; URI templates become concrete Fabric attribute types,
not fixed template values. The shared tool does not modify the input registry,
publish items, or generate a provenance sidecar.

The [shared authoring guide](../../../../tools/deploy-fabric/schema-set-authoring.md)
also covers creating missing parallel Avro variants through Avrotize. Conversion
uses upstream `s2a --no-custom-logical-types`; no local datetime patch is applied.
Regenerate both selected schemas directly from the canonical JSON Structure:

```powershell
python tools\deploy-fabric\generate_schema_set.py `
  --registry feeders\pegelonline\xreg\pegelonline.xreg.json `
  --messagegroup de.wsv.pegelonline `
  --create-avro-variants `
  --projected-version "#/schemagroups/de.wsv.pegelonline.jstruct/schemas/de.wsv.pegelonline.Station=1" `
  --projected-version "#/schemagroups/de.wsv.pegelonline.jstruct/schemas/de.wsv.pegelonline.CurrentMeasurement=2" `
  --output-registry <operator-directory>\pegelonline.fabric.xreg.json `
  --definition <operator-directory>\EventSchemaSetDefinition.json
```

Tests verify byte-for-byte equality of the selected schema strings with the
retained artifacts. This path creates the selected versions only, not the
historical Measurement version `1`. It does not replace checked-in artifacts
or refresh notebook bindings. New contract output still requires schema review
and live acceptance before replacing validated artifacts.

Validate the retained artifacts from the repository root:

```powershell
python -m pip install -r feeders\pegelonline\fabric\requirements-validation.txt
python -m pytest feeders\pegelonline\fabric\tests\test_projection.py feeders\pegelonline\fabric\tests\test_notebook.py feeders\pegelonline\fabric\tests\test_payload_encoding.py --no-cov -q
```

These checks compare the registry, Fabric definition and notebook bindings
directly. They do not regenerate files, provision resources or publish events.

## Wire and storage requirements

The notebook parameter `PAYLOAD_ENCODING` accepts `json` (the default,
`application/json`) or `avro` (`application/vnd.apache.avro+avro`, raw Avro
binary without an object-container header). CloudEvents remains in AMQP binary
mode for both choices: `cloudEvents:` application properties and the exact
service-issued registered schema-version URI are unchanged. Invalid encoding
values fail before connection lookup.

The AMQP data package is generated from the selected projected Avro schemas
with both Avrotize encoders. Both encodings retain string timestamps and the
selected schemas' nullability; this does not select the older canonical
long-timestamp Avro variant. `generate_producer.ps1` regenerates this package
after xrcg using the shared schema authoring command. Avrotize
3.9.7 fixes the missing Avro runtime dependency tracked in
[clemensv/avrotize#585](https://github.com/clemensv/avrotize/issues/585).
Preserving nullable zeros requires the follow-up correction in
[clemensv/avrotize#592](https://github.com/clemensv/avrotize/pull/592).
The shared requirements pin that commit and the structured-JSON/generated-test
corrections in [xregistry/codegen#712](https://github.com/xregistry/codegen/pull/712).
Use these revisions until corrected releases are available; do not patch
generated artifacts.

Changing the checked-in notebook does not update a deployed notebook or its
Environment. Publish the new AMQP data and bridge wheels before changing the
deployed parameter. JSON is the previously live-validated Fabric path. Avro
binary requires new receiver/output/history acceptance before a live switch;
an Avro schema registered for JSON does not prove that the configured receiver
admits Avro binary.

Structured Kafka input was rejected by the registered receiver with
`CloudEventPropertyMissingException: type is missing`. Do not assume that
the legacy Kafka notebook is compatible or change its required structured
mode to conceal the incompatibility. Kafka custom output can expose AMQP
properties as AMQP-encoded header values; decode them with an AMQP codec
rather than assuming native `ce_` headers.

The portable projection selects Station version `1` and CurrentMeasurement
version `2`. Discover physical table names and column types from the target
database instead of copying names from another deployment. Tables include
typed payload columns and CloudEvents metadata columns. KQL string columns
can represent JSON null as an empty string.

Fabric rejected Avrotize 3.9.1's `rfc3339-timestamp-millis` extension.
Measurement projection version `2` preserves the string payload and moves
the annotation to `x-original-logical-type`. See
[clemensv/avrotize#571](https://github.com/clemensv/avrotize/issues/571).
Avrotize 3.9.6 now produces this compatibility projection through its explicit
upstream option without local patches. Use
`todatetime(timestamp)` explicitly in downstream analytics. Generic Avro
validation does not enforce the original datetime, enum or numeric-range
constraints; retain JSON Structure validation.

The bridge emits the documented `unknown` classification when upstream omits
either water-level state, or supplies no state value. It does not emit `null`
for these optional, non-nullable canonical fields. Other nullable fields,
including zero-valued trends and river kilometres, retain their values.

## Deployment-time schema URI binding

The intended deployment path resolves schema URLs **during notebook deployment**.
After registration and source association, verify versions/fingerprints and
inject a code cell containing the literal `dataschema_overrides` dictionary into
the deployed notebook. Keep that cell's concrete URLs and all generated
deployment copies outside Git. Refresh it when bindings or selected versions
change. Portable `SCHEMA_BINDINGS` remains the contract selection, not a table
of deployed URLs.

The portable notebook now has a dedicated mapping placeholder. During deployment,
the operator resolves and verifies the map with the existing resolver, then uses
the [shared notebook binder](../../../../tools/deploy-fabric/bind_notebook_schemas.py)
to replace that cell in an external deployment copy. The unbound template fails
explicitly before connecting. The legacy deployer is still not schematized-safe.
Connection credential discovery remains separate from schema URL mapping.
The binder also requires the payload encoding qualified against registered
content-type metadata and the history receiver's `Json` or `Avro` serialization.
The run cell rejects a mismatched `PAYLOAD_ENCODING` and continuous mode.
Keep `ONCE_MODE=True`; this notebook has no cooperative worker shutdown.

## Analytics without ingestion plumbing

Eventstream owns the typed Station and CurrentMeasurement tables. Do not apply
the legacy dispatch table, JSON mappings or either dispatch-to-base update policy
to this path. The legacy KQL script remains available for other deployments.

After fresh typed-history acceptance, discover the exact physical table names
and types from the database. The [analytics renderer](../render_analytics.py)
accepts the `Name` and `OrderedColumns` JSON returned by `.show table ... schema
as json`. It rejects missing or incompatible columns and writes a bound copy
outside Git. Its output creates functions only, including explicit datetime
conversion for string measurement timestamps.

Latest-state helpers scan retained history on each refresh so stale stations
remain visible. Measure refresh cost before adding latest-state materialization;
a recent-history cutoff would hide stale stations and is not equivalent.

For Map setup, invoke the [post-deploy hook](../post-deploy.ps1) explicitly with
`-Schematized -StationTable <discovered-station-table>
-MeasurementTable <discovered-measurement-table>`, alongside the workspace, Map,
database and cluster parameters. The hook reads and validates both schemas,
loads static river geometry, installs the [analytics helpers](../analytics.kql)
and wires the Map. It does not create base ingestion tables, mappings or routing
policies. Latest-state enrichment and trends run at query time against the
selected history; no additional update policy is required.

The [notebook](../../notebook/pegelonline-feed.ipynb) passes
`dataschema_overrides` to the generated producer constructor.
[xregistry/codegen#696](https://github.com/xregistry/codegen/pull/696) adds
this API. The Kafka, MQTT and AMQP clients are generated with the pinned xrcg revision
and expose this constructor argument. The Kafka and MQTT `feed` functions
and the AMQP producer factory also accept the optional map. Without a map,
clients emit their original file-backed schema identities.

For a local generator checkout, install it in a dedicated environment outside
the repository. Activate that environment, then run the source's enforced
generator script:

```powershell
python -m pip install -r tools\deploy-fabric\requirements-schema-set.txt tomli-w
Push-Location feeders\pegelonline
try { .\generate_producer.ps1 } finally { Pop-Location }
```

The pinned xrcg revision reports `0.11.2.dev6`. The pinned Avrotize revision
preserves nullable zeros in both encodings; the official 3.9.7 release does not.
Client generation does not generate
the Fabric schema-set definition; use the shared authoring command above. Do not
hand-edit generated clients or relax dependency requirements. Rebuild all
affected wheels before updating a Fabric Environment; regeneration does
not update already deployed libraries.

The local generator also includes the source-template fix for
[xregistry/codegen#701](https://github.com/xregistry/codegen/issues/701).
Unpatched 0.11.1 changes structured Kafka JSON payloads from `data` objects
to `data_base64`. Regeneration must preserve object-valued `data` for JSON,
including `+json` media types, while retaining binary-mode bytes and
structured non-JSON base64 encoding. The source regression tests enforce
this wire shape; a matching version number alone does not establish it.

During deployment, [the resolver](../../pegelonline_core/pegelonline_core/fabric.py)
reads the selected source's event types and versions, resolves canonical
schema IDs, and obtains service-issued version `selfUrl` values. The map is
keyed by original generated `xreg://./` URIs, not event types. Station source
version `1` maps to projection version `1`; Measurement source version `1`
maps to projection version `2`. Do not infer catalog hosts or schema-set IDs.

The notebook's `SCHEMA_BINDINGS` pins expected versions and SHA-256
fingerprints. Tests compare these directly with the canonical source
identities and selected schemas in the registry and Fabric definition;
there is no provenance sidecar.
The shared generator reproduces the selected schema strings byte for byte.
If regeneration changes those bytes, deliberately refresh the expected
fingerprints and repeat contract review and acceptance before deployment;
semantic similarity is not a fingerprint match.
Missing or duplicate selections, conflicting mappings, schema drift and
unexpected routing hosts fail deployment. The read-only resolver currently
supports schema sets in the Eventstream's workspace only. Schema lookup uses
provider metadata APIs and scoped token exchange, not source connection keys.
Connection-string lookup uses the public Topology API.

The verified map is serialized as Python literals in the deployed notebook's
`deployment-dataschema-overrides` cell. It is not resolved anew on each run.
Use the [binding command](../../../../tools/deploy-fabric/schema-set-authoring.md#bind-a-deployed-notebook)
after metadata verification, then read the uploaded cell back before scheduling.
Keep all intermediate files outside the checkout.

At runtime, an unmapped URI retains its original
value; mappings are exact, copied per producer instance, and are not applied
recursively. No target schema URI belongs in a checked-in table.

Prefer workspace managed identity where supported. Verify the executing
principal, roles and token audience. Delegated metadata access and successful
SAS publishing do not prove workspace-identity support. Any unsupported path
requires an explicitly approved fallback.

## Hosting sequence

1. Select the target workspace, registered Eventstream, schema versions and
   paired database through operator configuration. Keep those values outside
   version control.
2. Generate compatible producers, then build wheels with
   `python -m pip wheel --no-deps --wheel-dir <operator-directory>` for:
   - `pegelonline_core`
   - `pegelonline_amqp_producer/pegelonline_amqp_producer_data`
   - `pegelonline_amqp_producer/pegelonline_amqp_producer_amqp_producer`
   - `pegelonline_amqp`
   Run `tools/deploy-fabric/strip-wheel-pathdeps.py` over the wheels.
3. Supply a TLS-capable native Proton wheel matching the Environment's Python
   ABI and Linux platform. Build with OpenSSL development files, repair with
   `auditwheel`, and verify `from proton import SSL; assert SSL.present()` in
   a clean compatible container. Record package hashes outside the repo.
   Never disable certificate verification.
4. Create or update a source-specific Fabric Environment. Upload feeder and
   Proton wheels plus [notebook-environment.yml](./notebook-environment.yml)
   through multipart upload. Publish, wait for `Success`, and read back.
   Verify loaded package versions inside the running notebook against the
   intended wheel set; upload and publication alone do not prove activation.
5. Bind the Spark kernel to the Environment, Lakehouse and paired KQL database.
   Preserve existing bindings and state; do not use the legacy deployer if
   it clears them.
6. Supply `EVENTSTREAM_NAME`, `WORKSPACE_ID` and `SOURCE_NAME` at deployment.
   Keep the validated `SCHEMA_BINDINGS` aligned with the selected contract
   artifacts. Definition assembly and datetime-compatible variant generation
   use the shared CLI and pinned Avrotize option described above.
   Target URIs are discovered, not checked in.
   Resolve and fingerprint-check selected schema URLs, inject the dedicated
   mapping cell with the shared binder and read it back in the deployed
   definition. The template's unbound placeholder must not reach a scheduled run.
7. Use bounded one-shot polling with `ONCE_MODE=True` and a finite
   `RUN_DURATION`. Preserve the configured dedupe file. A new state path
   requires an explicit replay decision.
8. Read the OneLake runtime log and match fresh events from both families
   between custom output and typed KQL history, including IDs, payloads,
   envelopes and registered `dataschema`. Store evidence outside the repo.
   Enable scheduling only after approval for interval and expiry; read back
   and verify an actual scheduled run. Startup time counts toward job duration.

For in-place replacement, retain the existing definition/bindings, state path
and approved schedule in external operator records. Pause scheduling only with
approval and reconcile that notebook's active invocation before replacement.
After readback and manual acceptance, restore the approved interval/expiry and
observe an actual scheduled invocation. Do not interrupt unrelated jobs.

## Validation and remaining work

Run source and artifact-validation tests with the local split-package roots on
`PYTHONPATH`:

```powershell
python -m pytest feeders\pegelonline\tests feeders\pegelonline\fabric\tests -x -q --no-cov
python -m mypy feeders\pegelonline\pegelonline_core\pegelonline_core\fabric.py --config-file mypy.ini
pwsh tools\validate-fabric-deployment.ps1 -FeederSlug pegelonline
```

Spark is intentional for Environment binding even if the static validator
warns that it expects a Python kernel. Runtime acceptance must prove output
and typed history; job completion and broker acknowledgement are insufficient.

Migration remains incomplete until canonical variant integration and expert
reviews, shared deployer integration, Map/query compatibility and production
handoff are complete. A merged codegen change does not update deployed wheels
or notebooks. Keep deployment status and acceptance receipts in an external
operator record, not this runbook.
