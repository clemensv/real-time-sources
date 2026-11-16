# Prepare the Eventhouse destination

Back to [schema-first authoring](./index.md).

## Discover the actual database

[Creating an Eventhouse](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/create-eventhouse) also creates a default child KQL database with the same name.
Use that database when it meets the scenario; do not create an additional database just to obtain a destination.
Discover its ID from the returned Eventhouse metadata or workspace inventory, then read the KQL database and verify its workspace and `parentEventhouseItemId`.
An Eventhouse ID is not a KQL database ID, and a matching display name alone does not establish ownership.
Wait for provisioning to complete before selecting the database in the destination.

Create a separate KQL database only when the scenario requires one.
Preserve existing databases and consumer groups.

## Complete asynchronous operations

A successful HTTP `202` means the request was accepted, not that the item is ready.
For [Fabric long-running operations](https://learn.microsoft.com/en-us/rest/api/fabric/articles/long-running-operation), use the returned `Location` or the documented public operation-state/result APIs with the returned `x-ms-operation-id`.
Honor `Retry-After`, wait with a finite deadline, and read the actual created item and its parent relationship.
Do not copy an Eventhouse ID into a database binding or issue a second create because the accepted response had no item body.

If a mutation's result is unknown, stop further mutations and reconcile the original operation and exact attempt-owned item before retrying.
An access denial requires approved access; changing identities or inventing an endpoint is not a recovery procedure.

## Select registered input

Configure the [Eventhouse destination](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/add-destination-kql-database) through a verified [programmatic path](./programmatic.md).
For approved native access, [select the destination's registered identities](./native-topology.md#select-the-kql-input-separately) separately from its column schemas.
If the registered-selection API contract is unavailable, report that exact blocker; do not switch to browser automation.
Choose the exact target database and registered **Input schema**, including the intended version.
If the picker reports an unknown version, inspect the event-type/schema references and the deployed schema content; use a compatibility alias only when the [observed picker requires it](./schema-set-definition.md).
A database, table-name template or untyped input does not establish schema-qualified ingestion.

Save, publish, and complete the [registered-schema storage verification](./verification.md).

## Let Eventstream create schematized base tables

Eventstream owns base-table creation for this registered-schema path.
Do not apply feeder base-table DDL, ingestion mappings or dispatch-to-base
update policies. Read back the actual created table names, column types and
registered schema/version selections before configuring downstream analytics
or Maps. Preserve generated KQL artifacts required by non-Fabric deployments.
Do not use legacy dispatch-table counts as acceptance for this path.
Record storage normalization observed in the selected destination, including
nullable strings represented as empty strings.

## Keep setup repeatable

Maintain an application-local setup runbook and a progress record of created item IDs, schema associations and outstanding checks.
Write them before time-consuming provisioning work and update them after each provisioning or verification phase.
Include commands to configure, start and stop the actual data supply.
Mark unverified steps explicitly; resource creation alone is not a runnable source.
