# Create an eventing app schema first

Back to the [pipeline-building skill](../SKILL.md).

Create and associate the Event Schema Set before generating application bindings.
These upstream event contracts are separate from application data models.
Application connector configuration does not provision this infrastructure.
Obtain approval for the target workspace and resource changes.

1. Inventory signals, supplied producers/feeders, schemas and xRegistry definitions.
   Define an event type per distinct contract, such as a reading or alarm.
   Different transports for one signal do not require duplicate event types.
   Keep the exact CloudEvents `type`, catalog message ID and payload schema identity separate.
2. Create the Event Schema Set in the target workspace.
   Add the required event types, envelope metadata, payload schemas and versions.
   Reuse supplied Avro contracts where they match the producer; [project existing xRegistry definitions](./xregistry-projection.md) rather than reauthoring them.
   If the selected event families lack Avro variants, [construct the missing variants](./avrotize.md#construct-missing-xregistry-avro-variants) from their authoritative payload schemas first.
   Register the variant that matches the actual wire encoding, not an Avro-binary variant merely because Fabric uses Avro schema definitions.
3. Enable schema-aware support when creating the Eventstream through a verified API contract.
   Current Fabric guidance says this option cannot be enabled on an existing Eventstream.
   Inspect an existing stream before proposing a separate migration or replacement; do not silently recreate it.
   For schema-aware native creation, [reconcile the owned artifact's committed mode](./native-state.md) before and after each definition publication or retry; creation flags can change.
4. Associate the Event Schema Set with the appropriate Eventstream **source node** and select the event types/schemas that source carries.
   Read back the published source association and its selected registered schemas/versions.
   Creating the registry item alone does not establish this association.
5. Configure and start the producer or [reuse the external feeder](./external-feeders.md), then verify [wire admission](./ingestion.md) against the associated contracts.
   Establish [source readiness](./source-readiness.md) before downstream schema discovery.
   Run setup probes separately from final destination acceptance.
   Nonconforming events from an associated source are dropped; inspect runtime logs.
6. Prepare the [Eventhouse/KQL destination](./destination.md) and explicitly select the registered input schemas and versions required by the app.
   Publish and read back the destination configuration, then verify the actual database, physical tables and mappings against those selections.
   Creating a table or receiving untyped events does not establish schema-aware KQL integration.
   Verify the output consumer endpoint and physical history mappings before generating application bindings.

Read back the committed mode, registered source/destination versions and typed storage before app wiring.
Resolve failed checkpoints, then declare the native backend connector, generate typed bindings and verify authenticated live/history calls.
A frontend build cannot repair a missing connector or unfinished source.

Require the [registered-schema ingestion check](./verification.md) before calling the source runnable; an upstream preview does not prove destination selection.

Follow Fabric's [Event Schema Set guidance](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/schema-sets/create-manage-event-schema-sets) and [schema association workflow](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/schema-sets/use-event-schemas).
Use [CLI or REST authoring](./programmatic.md); unresolved API contracts never authorize browser automation.

## Read the needed detail

- [Event Schema Set definition](./schema-set-definition.md).
- [Project an existing xRegistry definition](./xregistry-projection.md).
- [Avro reuse, conversion and inference](./avrotize.md).
- [Reuse an external feeder](./external-feeders.md).
- [Native REST and registered selections](./native-api.md).

Next, [prepare the application handoff](./handoff.md).
