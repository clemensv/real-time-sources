# Author Fabric through CLI or REST

Back to [schema-first authoring](./index.md).

Use the Fabric CLI, Azure CLI REST support or an approved scoped REST transport.
Do not use browser automation for Fabric resource authoring, configuration, metadata discovery or cleanup.
[Fabric CLI](https://microsoft.github.io/fabric-cli/) supports `fab api`.
Check CLI help and authentication first.
For explicitly approved version-specific access, see the [native schema-aware REST contract](./native-api.md).

## Keep access scoped

Use the approved identity, workspace and resource ownership rules for every operation.
A CLI on the host is not automatically installed or authenticated in an agent container.
In a restricted environment, use the supplied scoped REST transport; do not copy operator credentials or present a custom wrapper as the real CLI.
Do not change shared account profiles.
An access denial or uncertain mutation is not permission to switch tools, identities or endpoints.

For example, the documented [schema-set definition read](https://learn.microsoft.com/en-us/rest/api/fabric/eventschemaset/items/get-event-schema-set-definition) can be requested with:

```shell
fab api "workspaces/<workspaceId>/eventSchemaSets/<schemaSetId>/getDefinition" -X post --show_headers
```

For a JSON request body, `fab api -i request.json` takes the file path directly, not Azure CLI-style `@request.json`.
Inspect response headers and complete [asynchronous operations](./destination.md#complete-asynchronous-operations) before treating an accepted request as ready.
Use the [schema-set request packaging](./schema-set-request.md) for its required definition-part path and UTF-8/base64 payload.
Keep the actual HTTP status, provider error code and request ID when an API call fails.
For HTTP 500, another server error or a lost create response, reconcile the mutation before retrying.

## Preserve the complete definition

Read every returned definition part, including `eventstream.json`, `eventstreamProperties.json` and `.platform` when present.
Preserve unknown fields, parts, schema associations and registered input references during updates.
Do not rebuild only the graph from an older minimal template and discard the other metadata.
Read back the published result; request acceptance does not prove that the service retained a field.

The [Eventstream REST overview](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/eventstream-rest-api) and [definition reference](https://learn.microsoft.com/en-us/rest/api/fabric/articles/item-management/definitions/eventstream-definition) are starting points, not proof that every preview field is described.
Check [current REST coverage](https://github.com/microsoft/fabric-rest-api-specs/tree/main/eventstream) and node metadata readback.
Generic `inputSchemas` columns alone do not establish registered event-type/version selection.

## Report an unresolved API contract

Check current API coverage separately for schema-aware creation, source association and registered destination selection.
Missing fields in an older reference or template do not prove an operation is unavailable through APIs.
If an approved API contract cannot be established, stop that operation and report the blocker.
Record the exact operation, HTTP method/path, checked API version/reference, observed response and missing contract.
Do not fall back to a portal, Playwright, a headless browser or private endpoint discovery.
Do not invent definition fields or perform speculative create/update requests.

Helper flags and accepted creates do not prove saved state.
The exported `schemaMode` value or empty source properties alone do not prove whether schema-aware creation or association succeeded.
Verify published associations and registered references; report missing metadata access instead of guessing.
Complete [registered-schema storage verification](./verification.md) regardless of the authoring tool.
