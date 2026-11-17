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
- [Projection provenance](./projection-provenance.json) records conversion
  version, source identity, projected versions, schema digests and limits.
  These are contract identities, not deployed resource identities.

The older canonical Avro measurement schema uses a long timestamp, while the
JSON serializer emits an ISO-8601 string. Station nullability also differs
from the JSON Structure contract. The projection derives both records from
the authoritative JSON Structure schemas and inlines named dependencies.
Both event families are preserved.

Regenerate from the repository root:

```powershell
python -m pip install -r feeders\pegelonline\fabric\requirements-authoring.txt
python feeders\pegelonline\fabric\project_schemas.py
python -m pytest feeders\pegelonline\fabric\tests\test_projection.py --no-cov -q
```

These commands author local files only. They do not provision resources or
publish events.

## Wire and storage requirements

Use the existing AMQP 1.0 binary CloudEvents contract with JSON payload bytes,
`application/json`, `cloudEvents:` application properties and the exact
service-issued registered schema-version URI.

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
This is a compatibility projection, not a generator fix. Use
`todatetime(timestamp)` explicitly in downstream analytics. Generic Avro
validation does not enforce the original datetime, enum or numeric-range
constraints; retain JSON Structure validation.

## Runtime schema URI discovery

The [notebook](../../notebook/pegelonline-feed.ipynb) passes
`dataschema_overrides` to the generated producer constructor.
[xregistry/codegen#696](https://github.com/xregistry/codegen/pull/696) adds
this API. The Kafka, MQTT and AMQP clients are generated with xrcg 0.11.1
and expose this constructor argument. The Kafka and MQTT `feed` functions
and the AMQP producer factory also accept the optional map. Without a map,
clients emit their original file-backed schema identities.

For a local generator checkout, install it in a dedicated environment outside
the repository. Activate that environment, then run the source's enforced
generator script:

```powershell
python -m pip install -e <local-xrcg-checkout> tomli-w
Push-Location feeders\pegelonline
try { .\generate_producer.ps1 } finally { Pop-Location }
```

The local checkout must report version 0.11.1 and satisfy its declared
dependencies, including Avrotize >=3.9.5. This generator environment is
separate from the pinned projection-authoring environment above. Do not
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

At startup, [the resolver](../../pegelonline_core/pegelonline_core/fabric.py)
reads the selected source's event types and versions, resolves canonical
schema IDs, and obtains service-issued version `selfUrl` values. The map is
keyed by original generated `xreg://./` URIs, not event types. Station source
version `1` maps to projection version `1`; Measurement source version `1`
maps to projection version `2`. Do not infer catalog hosts or schema-set IDs.

Expected versions and SHA-256 fingerprints come from projection provenance.
Missing or duplicate selections, conflicting mappings, schema drift and
unexpected routing hosts fail startup. The read-only resolver currently
supports schema sets in the Eventstream's workspace only. Schema lookup uses
provider metadata APIs and scoped token exchange, not source connection keys.
Connection-string lookup uses the public Topology API.

Override tables exist only in memory. An unmapped URI retains its original
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
5. Bind the Spark kernel to the Environment, Lakehouse and paired KQL database.
   Preserve existing bindings and state; do not use the legacy deployer if
   it clears them.
6. Supply `EVENTSTREAM_NAME`, `WORKSPACE_ID` and `SOURCE_NAME` at deployment.
   Refresh generated `SCHEMA_BINDINGS` with
   [project_schemas.py](../project_schemas.py). Target URIs are discovered,
   not checked in.
7. Use bounded one-shot polling with `ONCE_MODE=True` and a finite
   `RUN_DURATION`. Preserve the configured dedupe file. A new state path
   requires an explicit replay decision.
8. Read the OneLake runtime log and match fresh events from both families
   between custom output and typed KQL history, including IDs, payloads,
   envelopes and registered `dataschema`. Store evidence outside the repo.
   Enable scheduling only after approval for interval and expiry; read back
   and verify an actual scheduled run. Startup time counts toward job duration.

## Validation and remaining work

Run source and authoring tests with the local split-package roots on
`PYTHONPATH`:

```powershell
python -m pytest feeders\pegelonline\tests feeders\pegelonline\fabric\tests -x -q --no-cov
python -m mypy feeders\pegelonline\fabric\project_schemas.py feeders\pegelonline\pegelonline_core\pegelonline_core\fabric.py --config-file mypy.ini
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
