# Select registered schemas in native topology

Back to the [native REST contract](./native-api.md).

This version-specific provider model differs from the public Eventstream definition.
Use approved API access, never browser automation.
Read the provisioned native model before editing registered selections; it contains `topology` and `properties`.

## Bind the source

In `properties.dataSources`, select `type: "CustomApp"` and `direction: "Source"`.
The association is `properties.eventTypes` on that source node, not merely a schema-set item elsewhere in the graph.
Each selection carries four registered identities:

```json
{
  "eventSetWorkspaceId": "<schema-set-workspace-id>",
  "eventSetArtifactId": "<schema-set-item-id>",
  "eventTypeId": "<deployed-event-type-id>",
  "schemaVersionId": "<deployed-version-id>"
}
```

Use deployed identities and exact casing; check [wire-type admission](./receiver-admission.md), not metadata alone.
Resolve deployed schema versions and preserve [wire identity](./ingestion.md).

## Select the KQL input separately

Find the intended native `type: "Kusto"` destination.
Its `properties.workspaceId` is the target workspace and `properties.artifactId` is the actual KQL database ID, not its parent Eventhouse ID.
Discover and verify that database as described in [destination setup](./destination.md).
Set that destination's `properties.eventTypes` to the required registered type/version identities.
Generic `inputSchemas` columns are separate and do not establish this selection.

Provision [schema-qualified Kusto ingestion](./native-kusto.md) as public `ProcessedIngestion`, which creates native `Push`, not `Pull`.
Preserve the schema-qualified `tableCreationMode`; the current provider model uses `PerCloudEventSchemaVersion`.
Read back the actual database, table and ingestion configuration.
Require both effective native `Push` mode and the schema-qualified table mode.
A literal `tableName` is not proof of the generated physical table or its payload mapping.

## Save the complete writable graph

Use `POST <workload-base>/saveTopology` with `topology` and `properties`.
This updates provisioned nodes; use the [creation workflow](./native-kusto.md) before reading their actual identities.
Preserve the returned serialized frontend `topology` when present; do not invent a frontend state model.
Retain writable `dataSources`, `streams`, `operators`, `eventLinks` and the service-returned `compatibilityLevel`.
Do not replay root readonly fields such as `embeddedEventHub`, capacity status or artifact idle status as authoring settings.
Preserve node IDs, logical IDs and names on updates.
Let the service generate managed-broker endpoint, hub and consumer-group names; preserve their verified values rather than inventing connection settings.
[Preserve Kusto `dataConnectionId` state on its original node](./native-kusto.md#preserve-owned-state).
Connect `inputNodes` by the upstream names required by the current model.
Where present, preserve registered `inputNodes[].eventType` references as well.
Do not discard other nodes or replace the graph with just the selected source.

Read `GET <workload-base>/model` after saving.
Verify both the exact source's `properties.eventTypes` and the connected Kusto destination's `properties.eventTypes`.
An accepted save, empty public source properties or exported `schemaMode: "None"` does not settle those checks.
Public `creationPayload`, definition and native model fields are not interchangeable.
After publishing, [commit the artifact mode and check component errors](./native-state.md) before acceptance.

## Prove ingestion

Establish [source readiness](./source-readiness.md), then reserve fresh events for destination acceptance.
Require the [physical schema-qualified storage check](./verification.md), including exact registered version, typed payload mapping and correlated fresh rows.
Native metadata alone proves neither wire recognition nor schema-qualified storage.
