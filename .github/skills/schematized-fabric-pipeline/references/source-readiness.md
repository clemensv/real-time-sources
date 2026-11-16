# Start data supply before downstream discovery

Back to [schema-first authoring](./index.md).

An eventing application needs an active producer.
Creating an Eventstream, schema or publisher file does not supply data.
Configure and start the supplied feeder, or implement and run the scenario's producer.
Keep the start command, endpoint configuration and credential acquisition in the application's setup runbook.

## Establish source readiness

1. Publish the schema-aware Eventstream and verify its source is running.
   For native authoring, [resolve each registered version before first publishing its selection](./native-catalog.md).
   Read the source node's actual schema association and selected event types; an Event Schema Set elsewhere in the workspace is insufficient.
   For native authoring, [verify the committed artifact mode and component updates](./native-state.md); `Running` with an unresolved update error is insufficient.
   Repeat these reads after every definition publication, including a successful retry.
   If a newly owned, explicitly schema-aware artifact reports `EnableSchemaAssociation: 1`, execute the documented current-ETag reconciliation and verify committed `2` before saving registered selections.
   Preserve an existing mode `5`; this repair does not authorize converting or replacing an unrelated legacy stream.
2. Start a small, bounded stream of genuine scenario events that conform to the registered contracts.
   Verify the actual transport binding and packet through the [wire-admission checks](./ingestion.md).
   Record the probe IDs and publication times.
3. Check native source runtime logs and the schematized-event preview for the intended event type.
   This establishes source recognition, not destination acceptance.

Do not wait for a final destination before starting all data supply.
When downstream discovery needs live input, publish a small readiness batch after the source association is ready, then inspect or reopen the destination configuration.
If **Input schema** is disabled, empty or only offers untyped events, inspect the published association, source recognition and discovery state.
Do not substitute an untyped input or invent a schema reference.
If registered input remains unavailable, record the observed blocker rather than sending an unbounded series of probes.

## Keep acceptance probes fresh

Reserve at least two fresh acceptance events for after the registered-schema destination is published and ready.
The initial probes do not count as destination acceptance.
With a finite publication budget, account for both phases before sending.
Do not exhaust the budget during upstream preview checks.

Continue with the [Eventhouse destination](./destination.md), then verify [registered-schema storage](./verification.md).
For a supplied external feeder, reuse its real data rather than building a replacement or assuming it is running.
