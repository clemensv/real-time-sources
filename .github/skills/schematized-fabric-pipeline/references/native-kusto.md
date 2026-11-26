# Provision schema-qualified Kusto ingestion

Back to [native registered selections](./native-topology.md).
Use CLI or approved REST authoring, never browser automation.

## Create the destination in the intended mode

Discover the actual KQL database and its parent as described in [destination setup](./destination.md).
The public Eventhouse destination uses the following properties:

```json
{
  "workspaceId": "<verified-workspace-id>",
  "itemId": "<verified-kql-database-id>",
  "databaseName": "<verified-database-name>",
  "dataIngestionMode": "ProcessedIngestion",
  "tableName": "<table-prefix>",
  "inputSerialization": {
    "type": "Json",
    "properties": { "encoding": "UTF8" }
  }
}
```

Attach that destination to the intended upstream node in the complete public definition.
See the [public processed-ingestion properties](https://learn.microsoft.com/en-us/rest/api/fabric/eventstream/topology/get-eventstream-topology#eventhouseprocessedingestionmodedestinationproperties).
This creates a native Kusto `Push` node.
Public `DirectIngestion` creates a different native `Pull` node with its own [table and mapping setup](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/api-kusto-pull-destination).
Adding a schema-qualified table mode to a `Pull` node is insufficient.

The provider rejects changing an existing node from `KustoPullMode` to `KustoPushMode`.
Create the destination in the correct mode from the start.
If an authoring attempt created the wrong destination, remove and replace only that owned destination through supported graph authoring.
Preserve the other nodes; never migrate an unrelated destination or copy its service-managed connection ID.

## Apply registered selections

After public publication, [recheck committed schema mode](./native-state.md) and read the actual native model.
Wait for transient component updates before editing.
Use its existing node IDs and logical IDs.
`saveTopology` updates provisioned nodes; it does not create missing nodes from invented IDs.

Require native `dataIngestionMode: "Push"` and the verified KQL database `artifactId`.
Set the destination's registered `eventTypes` independently of the source.
Use `tableCreationMode: "PerCloudEventSchemaVersion"` and a table-name template such as `Telemetry_{CloudEventType}_{CloudEventSchemaVersion}`.
Retain JSON/UTF8 input serialization when the wire payload is JSON; an Avro contract does not select Avro binary encoding.
Save the [complete writable graph](./native-topology.md#save-the-complete-writable-graph).

Read back both effective modes and the exact registered selections.
Then require [physical typed storage and correlated fresh rows](./verification.md).
An accepted save or a table-name template alone does not establish ingestion.

## Preserve owned state

Treat a returned Kusto `dataConnectionId`, including an all-zero placeholder, as service-managed state on that exact native node.
Do not invent it, replace it or copy it to another node or database.
When using a scoped adapter, read the current owned native model before round-tripping those properties so the adapter can verify their provenance.
