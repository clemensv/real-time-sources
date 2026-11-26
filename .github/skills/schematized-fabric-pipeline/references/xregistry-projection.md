# Project an existing xRegistry definition

Back to [schema-first authoring](./index.md).

xRegistry uses keyed maps such as `messagegroups.<group>.messages.<message>` and `schemagroups.<group>.schemas.<schema>`, with lowercase standard attributes.
Fabric uses `eventTypes[]`, `schemas[]` and `versions[]` with explicit `id` fields and camelCase attributes; changing casing alone is insufficient.

| xRegistry input                     | Fabric definition                         |
| ----------------------------------- | ----------------------------------------- |
| `messagegroups` message/version     | `eventTypes[]` with explicit `id`         |
| `envelope`                          | `format`                                  |
| `envelopemetadata`                  | `envelopeMetadata`                        |
| `dataschemaformat`                  | `schemaFormat`                            |
| `dataschemauri` or an inline schema | Resolved `schemaUrl` or `schema`          |
| `protocol`, `protocoloptions`       | `protocol`, `protocolOptions`             |
| `schemagroups` schemas              | `schemas[]` with explicit `id`            |
| `versions` map and schema bodies    | `versions[]`: `id`, `format`, schema text |

Select the endpoint, protocol and message group before projecting.
Resolve message inheritance transitively and reject cycles.
Honor the registry revision's reference attribute, including `basemessage` in older manifests and `basemessageuri` in current manifests; reject conflicting references.
Merge inherited metadata by attribute so a variant's `datacontenttype` override does not discard inherited `type`, `source`, `specversion` or `subject`.
Resolve explicit or declared default versions, including `defaultversionid`; never choose the first map entry.
Resolve schema URIs against the original registry before rewriting local references.
Support resource paths, JSON Pointer fragments and absolute references to resource `self` URLs already present in the supplied document.
Absolute in-document references need no network request.
For JSON Pointer fragments, split on `/` before decoding `~1` to `/` and `~0` to `~`; escaped characters belong to resource keys.
Resolve absolute references and escaped resource keys rather than rejecting them.
Reject unresolved references and ambiguous identities.
External references absent from the document require authorized retrieval and pinned provenance, not schema substitution.
Detect ID collisions when flattening different groups and record any explicit identity mapping.
Preserve source identities in provenance; verify [wire-type projection](./receiver-admission.md).
Do not lowercase identifiers, recursively camel-case payload properties, change CloudEvents wire types or replace them with Avro record names.
Preserve envelope/protocol metadata and payload field case, types, defaults and constraints.

## Select the Avro message-group variant

The [Bluesky registry](../../../../feeders/bluesky/xreg/bluesky.xreg.json) provides a concrete pattern:

| Resource | Purpose |
| --- | --- |
| `messagegroups.BlueskyFirehose` | Base event identities and JSON payload metadata, with JSON Structure schemas. |
| `messagegroups.BlueskyFirehose.avro` | Inherits each base message and overrides only its schema format/reference. Payload content type remains `application/json`. |
| `messagegroups.BlueskyFirehose.avro.binary` | Uses the same Avro schemas but overrides payload content type to `application/vnd.apache.org.avro+avro`. |
| `schemagroups.BlueskyFirehose.avro` | Avro payload records with explicit versions; both variant groups reference these resources. |

Both variant groups contain the same six event identities as the base group.
The Kafka, MQTT and AMQP endpoints list the variant groups alongside their existing groups.
These are alternate representations of the same events, not additional signals to flatten into duplicate Fabric event types.
Choose one representation per wire event type for a given source association; retain the selected group and schema version in provenance.

For an existing JSON-emitting feeder, start with the `.avro` variant, resolve its inherited envelope metadata and validate the actual JSON payload against that Avro contract.
The `.avro.binary` suffix describes the payload encoding; it does not select CloudEvents binary envelope mode.
An endpoint's envelope mode is a separate setting.
Endpoint references alone do not prove that the producer implements either encoding.
Do not switch a running feeder to Avro binary to register an Avro schema in Fabric.
If variants are missing, [construct them from the authoritative contracts](./avrotize.md#construct-missing-xregistry-avro-variants) rather than inventing Fabric-only payload schemas.

Follow the [native schema lookup guidance](./schema-set-definition.md) if the target picker needs an alias.
An alias preserves the original resource, pinned version, reference and schema bytes without renaming the event or Avro record.

Projecting the registry structure and converting a payload schema are separate operations.
The [AIS feeder registry](https://github.com/clemensv/real-time-sources/blob/main/feeders/aisstream/xreg/aisstream.xreg.json) illustrates message groups, inherited protocol descriptions and schema references.
Inventory its supplied schema representations, including Avro; one embedded JSON Structure group is not the complete format inventory.
A Fabric definition does not carry the full xRegistry endpoint model or establish the application's output consumer endpoint and historical bindings.

Use the official [xRegistry documentation](https://xregistry.io/), [core specification](https://github.com/xregistry/spec/blob/main/core/spec.md), [message specification](https://github.com/xregistry/spec/blob/main/message/spec.md), [schema specification](https://github.com/xregistry/spec/blob/main/schema/spec.md) and [endpoint specification](https://github.com/xregistry/spec/blob/main/endpoint/spec.md).
Pin the source model/specification version; registries can use different revisions.

If the payload format needs conversion, read the [Avrotize guidance](./avrotize.md).

## Generate the notebook schema URL cell during deployment

Keep authoring, deployment and runtime binding separate:

1. Author portable schema identities, explicit versions and expected fingerprints.
2. Deploy/register the schemas and associate the selected versions with the exact
   Eventstream source. Supply workspace/Eventstream/source bindings externally.
3. During notebook deployment, read that source's associated schema metadata and
   retrieve exact service-issued schema-version URLs. Verify versions and
   fingerprints, then inject the resolved mapping as a literal code cell in
   the deployed notebook before the feeder run cell.

Build an override table keyed by each original generated
`xreg://./.../versions/...` URI. Values are the exact registered version URLs,
not inferred URL templates. Preserve the generated client's behavior for
unmapped URIs; maps are instance-local, exact and nonrecursive. Reject missing
or ambiguous selections, conflicting mappings and schema drift before upload.
Do not guess catalog hosts or internal schema-group names/GUIDs.

Checked-in `SCHEMA_BINDINGS` represents portable contract selections, not the
physical URL map. Persist the resolved table only in the deployed notebook and
external operator artifacts, never Git. The run cell passes it to the producer;
schema catalog discovery need not run on each invocation. Keep credentials
separate. Use safe Python-literal serialization, replace rather than duplicate
the dedicated cell on redeployment, and read it back before scheduling.
Regenerate after source/schema-set/version changes.

The pilot uses `tools/deploy-fabric/bind_notebook_schemas.py` for cell injection
after operator-side resolution and fingerprint verification. Its portable
template fails explicitly when the cell is unbound. The legacy shared deployer
is not yet schematized-safe. Verify resolver scope explicitly; that pilot supports
schema sets in the Eventstream's workspace only.

Serialize schema text deterministically and compare bytes/fingerprints when
regenerating. Identical schema strings retain existing fingerprints. Changed
bytes require deliberate selection/binding updates and renewed acceptance;
semantic similarity alone is not a fingerprint match.
