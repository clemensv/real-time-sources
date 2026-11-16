---
name: schematized-fabric-pipeline
description: "Build and verify a schematized Microsoft Fabric Eventstream pipeline from a producer or feeder and event contracts. Covers Event Schema Sets, xRegistry/Avro projection, schema-aware source association, wire admission, custom output endpoints, paired KQL history, and the application handoff. Use for pipeline creation, schema association, registered KQL ingestion, or upstream pipeline diagnosis."
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

## Build and verify

Read [schema-first authoring](./references/index.md), then only the references needed for the selected path.

1. Inventory the actual producer contracts and supported wire representation.
   [Reuse an existing feeder](./references/external-feeders.md) and resolve [xRegistry references](./references/xregistry-projection.md), including inherited Avro message-group variants.
   Reuse matching Avro variants; when missing, [construct and validate them with Avrotize](./references/avrotize.md#construct-missing-xregistry-avro-variants) before Fabric registration.
   Keep Avro schema representation, payload encoding and CloudEvents envelope mode separate; an Avro schema does not require Avro binary events.
2. Create and read back the Event Schema Set and its pinned versions.
   Use [CLI or approved REST](./references/programmatic.md), not browser automation or guessed fields.
3. Create the schema-aware Eventstream and associate registered versions with its exact source node.
   For explicitly approved provider-specific APIs, follow the versioned [native contract](./references/native-api.md); revalidate its availability and never use it to bypass denied public access.
4. Establish [source readiness](./references/source-readiness.md) and verify [wire admission](./references/ingestion.md).
   Setup probes do not count as final destination acceptance.
5. Configure the [paired KQL destination](./references/destination.md), including explicit registered schema/version selection.
   Complete [fresh-event storage verification](./references/verification.md).
6. Publish a custom output endpoint on the intended event path.
   Read back its actual listen binding, protocol, consumer group and routed contracts.
   Verify received events against the same events in the paired database.
7. Deliver the [non-secret application handoff](./references/handoff.md).
   Missing output/schema information or missing paired history blocks handoff.

Keep schema registration, broker acceptance, source recognition, physical storage and output consumption as separate results.
Use bounded genuine events and finite deadlines.
Record exact blockers instead of substituting synthetic data or untyped ingestion.

## Related skills

- [Scoped authoring gateway qualification](./references/scoped-authoring.md) for an approved isolated pipeline-building adapter.
- [Source contracts](../xreg-source-contract/SKILL.md) for feeder contract authoring.
- [Fabric notebook deployment](../fabric-notebook-deployment/SKILL.md) for notebook-hosted pollers.
- [Container and delivery](../container-and-delivery/SKILL.md) for feeder packaging.
