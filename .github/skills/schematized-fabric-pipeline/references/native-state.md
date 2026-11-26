# Commit and verify native schema-set mode

Back to the [native API contract](./native-api.md).

Use this version-specific lifecycle only for a newly owned Eventstream created with schema support selected.
It is not a migration procedure for an existing ordinary Eventstream.
Use approved REST access, never browser automation.

## Commit the actual artifact state

The current provider client selects `EnableSchemaAssociation: 2` when a source uses a registered schema set.
It conditionally updates artifact metadata when the current value is `1`.
It preserves the separate dynamic-schema value `5`; do not reinterpret every non-`2` value as disabled or overwrite an unrelated mode.

Re-read metadata after graph publication or a public definition update.
A newly created stream returned to `1` despite initial `2` and saved selections.
For that schema-set path, complete the conditional metadata commit:

1. Read `GET <backendOrigin>/metadata/artifacts/<ownedObjectId>`.
   Verify the exact workspace, capacity, type, name and `provisionState: "Active"`.
   Retain the current response `ETag` as an opaque version.
2. If the freshly read mode is `1`, send the following request with normal Power BI authentication, not an artifact MWC token:

   ```http
   PATCH <backendOrigin>/metadata/artifacts/<ownedObjectId>
   If-Match: <current-ETag>
   Content-Type: application/json

   {"extendedProperties":{"EnableSchemaAssociation":2}}
   ```

3. Read metadata again and require the committed `2`.
   Accepted writes do not prove persistence.
   Reconcile further publication changes before sending events.

Do not use a wildcard ETag or combine this request with other artifact edits.
Construct a new body containing only `extendedProperties.EnableSchemaAssociation`.
Do not spread GET metadata or its `extendedProperties` into the PATCH; retention, throughput and other settings are outside this commit.
If a wrapper advertises flat `response.etag` and top-level `ifMatch`, use them, not an invented `headers` parameter.
For HTTP `412`, refresh metadata and reconcile the concurrent update before a bounded retry with its current ETag.
For an access denial, uncertain mutation or different mode, stop that operation and report the evidence; do not force a transition or switch authoring tools.

Resolve the [actual registered versions](./native-catalog.md) and verify current mode `2` immediately before each native graph save, not only after it.
If a public definition update occurs between a commit and graph save, re-read metadata and reconcile again.
A final metadata PATCH after a failed graph does not prove the consumer recompiled under the corrected mode.

## Check component updates before acceptance

Artifact `Active` state and completed public operations do not establish component readiness.
Poll the current native model with a finite deadline while nodes are `Creating` or `Updating`, before editing.
Retry `DataSourcesValidationError` only when it explicitly names an owned node in those transient states; refresh the model and schema mode first.
Do not retry access denials, unrelated validation errors or uncertain mutation outcomes as transient states.

Re-read the [native graph](./native-topology.md) and its source and Kusto update errors after publishing.
`Running` does not establish readiness while `ESComponentUpdateFailure` or another unresolved component error is present.
Saved four-field selections and an exported schema alias do not establish that the consumer resolved the registered version.
If resolution still fails, record the exact artifact/type/version and current component error; do not repeatedly add aliases or substitute an untyped destination.

Only publish final acceptance probes after those checks pass.
Require [physical schema-qualified storage](./verification.md), not generic table rows, acknowledgements or metadata flags.
