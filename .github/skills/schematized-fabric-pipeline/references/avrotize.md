# Reuse or derive Avro schemas with Avrotize

Back to [schema-first authoring](./index.md).

Fabric currently documents Avro schema support.
First reuse a suitable supplied Avro schema, including an existing generated or exported representation.
Do not convert another representation merely because it was the first one inspected.

When conversion is needed, use Avrotize as an authoring-time Python dependency.
Do not write a replacement schema converter or add it to the browser runtime.
For this repository, install the pinned shared authoring dependencies in an
external tooling environment and record their resolved revisions:

```powershell
python -m pip install -r tools\deploy-fabric\requirements-schema-set.txt
python -m pip show avrotize
```

Avrotize 3.9.6 introduced `--no-custom-logical-types`; it is not the qualified
dual-encoding runtime generator. The official 3.9.7 release fixes the generated
Avro dependency but lacks the nullable-zero correction in
[clemensv/avrotize#592](https://github.com/clemensv/avrotize/pull/592).
The requirements also pin the structured JSON/generated-test corrections in
[xregistry/codegen#712](https://github.com/xregistry/codegen/pull/712).
Both correction PRs were still open when the pilot was merged. Use the pinned
revisions until replacement releases pass the same regressions; a version string
alone does not prove that a correction is installed.

For JSON Structure, convert the resolved payload schema, not the whole xRegistry document:

```sh
python -m avrotize s2a DeviceReading.jstruct.json --out DeviceReading.avsc --no-custom-logical-types
```

For JSON Schema, use the alternative command:

```sh
python -m avrotize j2a DeviceReading.schema.json --out DeviceReading.avsc
```

Check the installed command's `--help` for other supported inputs and options.
Validate representative payloads against the generated schema, for example:

```sh
python -m avrotize validate reading.json --schema DeviceReading.avsc --schema-type avro
```

Also validate against the original contract and compare required fields, nullability, unions, numeric ranges, logical types and defaults.
Some conversions use Avrotize logical-type extensions or metadata that a generic Avro consumer does not enforce.
Verify compatibility with Fabric and the consuming application's codecs; retain source constraints and report unsupported or lossy conversions explicitly.
Never relabel JSON Structure or JSON Schema as Avro without conversion, or silently change the producer's payload to fit the result.
Store the validated Avro schema text in the definition and keep the original contract and conversion provenance.

### Verified compatibility limits

The 2026-11-16 pilot found existing Avro timestamps represented as longs while
the actual generated JSON serializer emitted strings; nullability also differed.
An existing variant is reusable only after comparison with actual serialized
payloads, not because its resource name contains `avro`.

Fabric rejected Avrotize 3.9.1's `rfc3339-timestamp-millis` logical-type
extension. Avro explicitly requires readers to ignore unknown logical types and
use the underlying Avro type. Registration and broker acceptance did not expose
this Fabric runtime compatibility defect; the emitted Avro was not invalid merely
because Fabric rejected it.

Avrotize 3.9.6 resolves
[clemensv/avrotize#571](https://github.com/clemensv/avrotize/issues/571) with
`s2a --no-custom-logical-types`. Use that explicit option for Fabric JSON-wire
projections. It retains string payloads and moves custom RFC3339 annotations to
`x-original-logical-type`; standard logical types such as UUID remain intact.
Do not implement that transformation locally or rewrite existing Avro inputs
silently. Both selected Pegelonline schemas reproduce the retained schema strings
byte for byte through this upstream option.
Record the loss of datetime validation and downstream `todatetime` requirements.
Generic Avro validation also does not enforce every original enum or numeric
constraint. Keep authoritative validation and retest provider compatibility
before removing any workaround.

## Construct missing xRegistry Avro variants

Use the shared `tools/deploy-fabric/generate_schema_set.py` command and its
[authoring guide](../../../../tools/deploy-fabric/schema-set-authoring.md)
when available on the target branch (introduced with #1747). It owns local
xRegistry selection/inheritance, missing parallel variants and Fabric definition
assembly; Avrotize owns datatype conversion and named-record inlining. Do not
reintroduce a source-specific converter if integrating that shared tool is needed.
The tool does not fetch remote references or deploy resources; resolve unsupported
references through the approved path before invoking it.

Pin source versions and require explicit projected versions. Never infer a
version bump from an event-name suffix or select the highest map entry.
Preserve canonical resources, endpoints, key templates, subjects and inherited
wire types. No separate projection-provenance sidecar is required: contract
identities and versions are in the registry, schema text is in the definition,
and notebook selections pin fingerprints. Keep operational evidence external.

Missing Avro variants are authoring work for this skill, not a reason to stop at an untyped Fabric route.
Use the [Bluesky variant pattern](./xregistry-projection.md#select-the-avro-message-group-variant).
Reuse existing matching schemas and messages; add only missing resources.
For repository contract edits, load the [source-contract skill](../../xreg-source-contract/SKILL.md) and follow its instructions, regeneration requirements and expert-review gates.
If the upstream registry is read-only, save a derived registry in the approved pipeline authoring location with its original revision and conversion provenance; do not claim to have updated the upstream.

1. Inventory every selected base message, including reference-data events, and resolve its authoritative payload schema and version.
   Convert each missing representation with Avrotize's `s2a` or `j2a`, as appropriate.
   Do not infer schemas from samples when an authoritative contract exists.
2. Let the shared command add `<base-group>.avro.json` schema resources and
   `<base-group>.avro` messages with explicit schema/version IDs.
   The `.avro.json` suffix is a historical resource name, not an encoding switch.
   For registries outside this repository, follow their established group naming
   and inheritance vocabulary instead of renaming existing resources.
   Require explicit projected version IDs and record the source-to-derived mapping.
   Keep nested named-type dependencies resolvable in the schema registered with Fabric.
   Do not replace the original JSON Structure or JSON Schema resources.
3. Add a sibling `<base-group>.avro` message group with one variant per selected base message.
   Preserve each message ID and inherit the original message using the reference attribute supported by that registry revision.
   Override `dataschemaformat` to `Avro` and `dataschemauri` to the corresponding Avro resource.
   Preserve the inherited CloudEvents wire type, source, subject/key identity and
   protocol metadata. Select `datacontenttype` explicitly for the qualified
   payload encoding; retain JSON when no encoding change is authorized.
   Do not copy the full base message into each variant.
4. If Avro binary payloads are also in scope and supported by the producer and target, add `<base-group>.avro.binary`.
   Reference the same Avro schema resources and override only the payload `datacontenttype` to the producer's verified Avro media type.
   The qualified pilot uses `application/vnd.apache.avro+avro`.
   Do not copy another feeder's media type without receiver qualification.
   Do not infer CloudEvents envelope mode from this suffix or advertise unsupported encodings.
5. Add variant references to the applicable existing endpoint's `messagegroups` list only for representations that endpoint/producer supports.
   Preserve existing references and transport bindings; an added reference does not implement a serializer.
6. Resolve the derived registry again.
   Check message coverage, inheritance, schema references, pinned versions and exact wire identities.
   Validate representative real payloads against both contracts, including nulls, optional fields, nested records, arrays, enums and timestamps.
   Parse the Avro records with an Avro implementation and check named-type and default validity.
   Report conversion losses or producer incompatibilities rather than weakening the contract to obtain acceptance.
7. Project the selected Avro variant into the [Fabric definition](./schema-set-definition.md).
   Map the registry's `Avro` format to a versioned format supported by the target, such as `Avro/1.12.0` where verified.
   Store each version's schema as JSON text serialized exactly once.
   Retain the source registry revision, base/variant identities, resolved schema versions, conversion tool version and schema digests.
   Complete registered source/destination readback and [fresh-event storage verification](./verification.md); local schema validation alone does not establish Fabric compatibility.

For a JSON-emitting source, the required result is a reusable `.avro` message group and its Avro schema resources, plus a pinned Fabric projection.
An `.avsc` file alone omits the message identity and envelope metadata needed for that projection.
Constructing these variants must not change the feeder's existing default encoding or replace a deployed pipeline.
If shared generation finds an existing target group, it refuses to overwrite it.
Select and validate that group directly, or authorize a distinct derived
projection; do not bypass the guard with local rewrites.

## Infer a draft from JSON samples

When no authoritative schema is available, Avrotize's `json2a` command can infer a draft Avro schema from JSON samples.
Use representative **payload** samples for one event type at a time; do not merge unrelated signals or infer the payload schema from the entire CloudEvents envelope.
For example:

```sh
python -m avrotize json2a reading-1.json reading-2.json --out DeviceReading.avsc --type-name DeviceReading --namespace example.device --sample-size 0
```

`--sample-size 0` examines all records in the supplied inputs.
Include examples of optional fields, null values, alternate shapes and boundary values where available.
Review required fields, numeric precision/ranges, unions, enum domains, defaults and timestamp/logical-type semantics before accepting the draft.
Samples cannot reveal fields or variants that never appear, or prove the intended constraints and evolution policy.
Validate the reviewed schema with held-out payloads and negative cases before registering it in the Event Schema Set.
Record the sample provenance and Avrotize version.
Inference does not replace an existing authoritative schema or establish compatibility with the actual producer and target runtime.
