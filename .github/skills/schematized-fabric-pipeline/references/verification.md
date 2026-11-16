# Verify registered-schema ingestion

Back to [schema-first authoring](./index.md).

A working source must pass configuration readback and real-event storage checks.
Do not declare success from resource creation, send acknowledgements, `Running`, or an upstream **Schematized events** preview alone.

## Configure the destination deliberately

1. Read back the deployed Event Schema Set.
   Resolve the selected event type to the intended payload schema/version and compare its schema content with the supplied contract.
   Preserve any explicit projection/alias mapping.
2. Verify schema-aware creation and the association on the exact source node.
   Inspect the published association, not only an accepted request or a schema set existing in the workspace.
3. In the [Eventhouse destination](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/add-destination-kql-database#configure-schemas-for-an-eventhouse-destination), select the registered event schema in **Input schema**.
   Verify the intended version; an untyped/default input is not the registered schema.
   Select the required table-creation method and payload-only or metadata-and-payload storage.
   A table-name template does not select a schema.
4. Save, publish and read back the destination's selected input schemas and target database.
   Use verified programmatic metadata to complete the readback; report missing access or contract coverage explicitly.
   Generic envelope columns such as `id`, `type` and a string/dynamic `data` column alone do not prove a registered payload/version was selected.
   If the registered input is unavailable, resolve the association/recognition problem; do not select the untyped input as a fallback.

The preview for an unsaved destination is not proof of upstream failure.
Inspect the actual connected source/default stream separately.
If an API rejects the configuration, report its status and validation errors instead of guessing a definition patch.
Use the verified [programmatic path](./programmatic.md); do not use browser automation or invent schema-selection properties.

## Correlate fresh events through storage

Wait for both the source and destination to be ready before the acceptance probes.
Events sent before destination activation may not be routed into storage.
If preview bootstrap is needed, budget it separately and use new IDs for the final probes.

Publish at least two fresh events within the authorized count and wait with a finite deadline.
Correlate those probes in the exact target database by retained event IDs, or by contract-supported payload correlation for payload-only output.
Read only the query's primary result; statistics and completion tables are not event rows.
Read its actual physical table schema and ingestion configuration, including mappings where the selected ingestion mode uses them.
Trace the selected registered schema/version to that storage; do not infer the binding from a plausible table name.
Check the expected envelope attributes and payload fields, types and values.
Record the destination's actual envelope/payload layout before deriving downstream bindings.

An event found only in `Unschematized_NoSchema`, an untyped/default route, or a manually populated table fails this check.
For structured input, a complete CloudEvent stored inside the payload's `data` is a decoding/layout mismatch to investigate, not proof of successful schema application.
Do not add an application-side unwrap or manually create a matching table to conceal an upstream classification failure.

Keep a small sanitized receipt with owned resource IDs, schema/version identities, published selection, exact probe IDs, physical storage/readback and cleanup outcome.
Exclude tokens, SAS keys, connection strings and machine/user identifiers not needed for correlation.
Only after these checks pass should you [prepare the application handoff](./handoff.md).
