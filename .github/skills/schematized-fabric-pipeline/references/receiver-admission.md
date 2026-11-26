# Match wire types to registered event types

Back to [native schema selection](./native-topology.md).

The current native receiver looks up messages by the transmitted CloudEvents `type`.
This provider-specific behavior was checked on 2026-11-11.

## Project the wire identity explicitly

Use the endpoint contract's declared CloudEvents type, with exact casing, as the Fabric `eventTypes[].id`.
Select that deployed ID and its registered version on both the source and Kusto destination.
If an xRegistry message key differs, retain its group, key and version in projection provenance and record the mapping to the Fabric ID.
Do not change the feeder's wire type or an Avro record name to match a registry key.
If the wire type is not fixed in envelope metadata, inspect the selected producer contract before choosing an ID; do not invent one.

Schema resource IDs, Avro record names, version IDs and content URIs remain separate identities.
Preserve the resolved original schema and its pinned version.
A schema-picker alias does not establish a CloudEvents type alias.

## Metadata does not prove receiver admission

Setting `envelopeMetadata.type.value` to a different wire type did not create an ingestion alias.
An observed stream accepted its topology and reported both components Running, and the broker accepted a binary JSON event.
The Kusto runtime log then reported `MessageNotSupportedException` for that transmitted type and dropped the event.
The same neutral contract produced typed physical rows after its registered event-type ID and transmitted type matched.

Read [supported runtime logs](./native-diagnostics.md) when accepted events do not reach storage.
Require [fresh correlated typed rows](./verification.md); successful creation, declared envelope metadata and broker acceptance are insufficient.
