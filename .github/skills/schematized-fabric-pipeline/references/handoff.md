# Hand off the output and paired history

Back to the [pipeline-building skill](../SKILL.md).

Deliver both inputs together.
Ask the application owner to confirm the intended output and paired database before declaring the handoff complete.

## Custom output and associated schema set

- Tenant/workspace and Eventstream item identity; exact custom output node identity.
- Actual output/listen protocol, namespace/bootstrap addresses, entity/topic and consumer group.
  Keep producer input/send details separate.
- Associated Event Schema Set workspace/item identity, selected event types, pinned schema/message versions and complete schema content.
- Exact CloudEvents wire identities, envelope mode, payload encoding and declared schema URIs.
- Export provenance, timestamps, source revision where applicable and complete-document digests.
- Non-secret authentication mechanism and acquisition instructions; never tokens, keys or connection strings.

Do not infer output association from matching names or a schema set elsewhere in the workspace.
Verify that the actual output carries the selected contracts.
Kafka and AMQP endpoints are distinct protocol bindings.

## Paired KQL database

- Database workspace/item ID, parent Eventhouse identity, query service URI and physical database name.
  An Eventhouse ID is not a database ID.
- Per-event-type physical table names, schema/version bindings, envelope/payload columns and ingestion mappings where used.
- Retention and supported historical interval, plus the runtime reader's access requirements.
- Evidence that the output and history contain the same event identities and payloads.

Read physical names from deployed metadata and queries; never derive them from Avro record names.
For literal dotted table names, quote the entire entity in KQL.

## Verification receipt

Retain the observation interval, at least two fresh genuine event IDs, matched output/storage values, published selections, unresolved checks and ownership/cleanup status.
Keep the pipeline available for authorized application attachment.
The application's authenticated live-stream, historical-query and browser checks follow in the consuming repository; pipeline creation alone does not establish application acceptance.
