---
name: schematized-fabric-pipeline
description: "Build, migrate and verify schematized Microsoft Fabric Eventstream pipelines for existing or new feeders. Covers reusable Avro variants, pinned schema registration, notebook/runtime bindings, typed history, analytics and Maps, fresh output/history acceptance, staged cutover/rollback and low-disk fleet execution. Use for feeder migration, pipeline creation, schema association or registered-ingestion diagnosis."
---

# Build a schematized Fabric Eventstream pipeline

This skill owns upstream pipeline construction.
Consuming applications start from an existing Fabric Eventstream custom output endpoint with associated Event Schema Set information AND a paired KQL database.
Neither input alone is a complete handoff.

## Establish scope before authoring

Ask for the approved workspace, producer or feeder, authoritative event contracts, intended custom output protocol and historical database requirements.
Identify existing items and obtain explicit permission for resource creation or changes.
Do not replace an existing pipeline, change capacity or reuse a consumer group without approval.
Keep credentials in operator/server-owned configuration and preserve unrelated resources.
Prefer the workspace managed identity wherever the selected API, service and transport support it.
Verify the effective runtime principal, token audiences and least-privilege roles; delegated user credentials are not workspace-identity proof.
Do not fetch SAS keys by default. Document any identity-support limitation and obtain approval for a fallback, with a supported Entra flow preferred over SAS.
Never enable key authentication or broaden permissions silently.
Keep concrete deployment coordinates outside Git, including non-secret
workspace/item names and IDs, registered URLs, schedules and run receipts.
Use portable contracts and placeholders in repository files; retain operator
configuration and acceptance evidence externally.

## Build and verify

Read [schema-first authoring](./references/index.md), then only the references needed for the selected path.
For an existing feeder or a fleet migration, start with the
[migration execution runbook](./references/migration.md). It defines preparation
gates, per-feeder changes, acceptance, cutover/rollback and worktree reuse.
It is a guided workflow, not a claim that the legacy deployer is migration-safe.

1. Inventory the actual producer contracts and supported wire representation.
   [Reuse an existing feeder](./references/external-feeders.md) and resolve [xRegistry references](./references/xregistry-projection.md), including inherited Avro message-group variants.
   Reuse matching Avro variants; when missing, [construct and validate them with Avrotize](./references/avrotize.md#construct-missing-xregistry-avro-variants) before Fabric registration.
   Keep Avro schema representation, payload encoding and CloudEvents envelope mode separate; an Avro schema does not require Avro binary events.
   Use shared repository tooling for registry/Fabric assembly and Avrotize
   for datatype conversion; do not introduce a source-local converter.
2. Create and read back the Event Schema Set and its pinned versions.
   Use [CLI or approved REST](./references/programmatic.md), not browser automation or guessed fields.
3. Create the schema-aware Eventstream and associate registered versions with its exact source node.
   For explicitly approved provider-specific APIs, follow the versioned [native contract](./references/native-api.md); revalidate its availability and never use it to bypass denied public access.
   When deploying the notebook, discover exact registered version URLs, verify
   versions/fingerprints and inject an original-schema-URI-keyed override map
   in a generated cell. The deployed run cell passes it to the producer.
   Concrete URLs and generated deployment copies stay outside Git; regenerate
   the cell when the target binding or selected schemas change.
4. Establish [source readiness](./references/source-readiness.md) and verify [wire admission](./references/ingestion.md).
   Setup probes do not count as final destination acceptance.
5. Configure the [paired KQL destination](./references/destination.md), including explicit registered schema/version selection.
   Let Eventstream create the schematized base tables; do not apply feeder base-table DDL, ingestion mappings or dispatch-to-base update policies.
   Read back actual names and types before adding downstream analytics or Maps.
   Complete [fresh-event storage verification](./references/verification.md).
6. Publish a custom output endpoint on the intended event path.
   Read back its actual listen binding, protocol, consumer group and routed contracts.
   Verify received events against the same events in the paired database.
7. Deliver the [non-secret application handoff](./references/handoff.md).
   Missing output/schema information or missing paired history blocks handoff.

Keep schema registration, broker acceptance, source recognition, physical storage and output consumption as separate results.
Use bounded genuine events and finite deadlines.
Record exact blockers instead of substituting synthetic data or untyped ingestion.

For notebook-hosted sources, also follow the [notebook skill](../fabric-notebook-deployment/SKILL.md).
Preserve Spark Environment bindings, verify native TLS support, select the exact named source and retain dedupe state.
A notebook job marked `Completed` does not prove runtime success or downstream ingestion.
Require its OneLake log and fresh output/history correlation; when scheduling is requested, approve/read back cadence and expiry and observe an actual scheduled invocation.
Do not invoke a legacy deployer that overwrites these bindings or applies base-ingestion KQL.

## Related skills

- [Existing-feeder and fleet migration](./references/migration.md), including
  disk-budgeted worktree reuse and an explicit completion checklist.
- [Scoped authoring gateway qualification](./references/scoped-authoring.md) for an approved isolated pipeline-building adapter.
- [Source contracts](../xreg-source-contract/SKILL.md) for feeder contract authoring.
- [Fabric notebook deployment](../fabric-notebook-deployment/SKILL.md) for notebook-hosted pollers.
- [Container and delivery](../container-and-delivery/SKILL.md) for feeder packaging.
