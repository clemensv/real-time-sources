# Resolve registered versions before native publication

Back to the [native API contract](./native-api.md).

Use this version-specific read contract through approved REST access.
Resolve every selected version before the first source or Kusto graph publication.
An exported Event Schema Set definition alone does not establish consumer lookup readiness.

## Read the actual schema-set catalog

Read native metadata for the owned schema set and verify its workspace, capacity, name and type.
Public `EventSchemaSet` corresponds to native `EventDefinition`, not `EventStream`.
Use the [normal routed authentication and private scoped-token exchange](./native-api.md), but select `workloadType: "OneRiver"` and `artifactType: "EventDefinition"` for this artifact.
Keep tokens operator-side; set the workload moniker to the schema-set artifact ID.
Do not query capacity metadata or follow catalog URLs with borrowed credentials.

The base is `https://<TargetUriHost>/webapi/capacities/<capacityId>/workloads/OneRiver/OneRiverService/automatic/eventdefinitions/v1/workspaces/<workspaceId>/artifacts/<schemaSetArtifactId>`.
With the same private `MwcToken` header pattern, read:

```http
GET <base>/eventtypes/<eventTypeId>
GET <base>/schemas/<eventTypeId>/versions
```

The first response gives the event type's actual `id`, `envelopeMetadata`, `schemaUrl` and `schemaFormat`.
Validate the intended envelope contract and declared schema reference.
The versions response is a JSON array, not an object containing `data`.
An HTTP-client wrapper's `response.data` is not a property of that JSON body.
Match the intended entry's `id`, `schemaId`, `format` and textual `schema` against the pinned producer contract.
Parse schema JSON explicitly and compare its content; do not blindly select the first or latest version.

## Finish compatibility mapping before connecting consumers

This provider picker requests versions by event-type ID even when `schemaUrl` names a different schema resource.
Differing IDs remain valid xRegistry.
If that required lookup is empty or missing, complete the [verified alias mapping](./schema-set-definition.md) before first publishing a consumer.
Retain the original schema, version and declared reference; any alias must contain identical schema bytes and the same pinned version.
Use documented item-definition operations, then repeat the native versions read and verify the exact returned version and bytes.
Do not invent catalog writes, substitute IDs or alter the schema to suppress a lookup error.
Stop an access-denied operation rather than changing identity or endpoint.

Keep the picker alias separate from the [canonical wire schema URI](./native-wire.md).
Immediately before each native graph save, [verify and commit explicit schema-set mode](./native-state.md).
A public definition update between a metadata commit and graph save invalidates that earlier readiness check.
Publish the [registered selections](./native-topology.md) only after both catalog resolution and current mode checks pass.

A successful versions read proves catalog availability, not ingestion.
An unchanged graph save or a later metadata PATCH does not prove a failed component recompiled.
If `ESComponentUpdateFailure` persists, retain the exact error and report an unresolved consumer; do not dismiss it as stale.
Require [physical schema-qualified storage](./verification.md) after fresh genuine probes.
