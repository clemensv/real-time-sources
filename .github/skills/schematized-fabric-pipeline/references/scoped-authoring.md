# Qualify a scoped pipeline-authoring gateway

Back to the [pipeline-building skill](../SKILL.md).

These notes describe requirements for an optional isolated pipeline-authoring adapter.
They do not grant access or imply that an adapter is installed.
Keep adapter qualification separate from application acceptance.

Source provisioning consent is separate from managed application deployment.
The source-authoring admission permits only the named workspace, approved item types, attempt-owned resources, and an unexpired execution window.
It does not permit changes to existing items, consumer groups, or capacity.

The trusted controller must start the source-authoring gateway before the isolated authoring process.
Its capability must bind the attempt, workspace, expiry, item-name prefix, and loopback gateway origin.
Pass the gateway URL and scoped capability through the adapter's documented configuration; do not forward the operator's Fabric token.
The adapter must redact the capability from retained output and CLI logs, and keep the gateway alive through the authoring operation.
Keep operator credentials unavailable to the isolated process and expose only the admitted scoped capability.
Mark admission started before launching the unprivileged process.

Source capability descriptions must match the admitted action fields and response metadata.
An adapter that exposes the response ETag as `etag` and accepts a top-level `ifMatch` parameter must advertise both fields and the mapping to HTTP `If-Match`; documenting only `method`, `path` and `body` prevents the agent from performing required conditional updates.
Qualify that round trip on a disposable, attempt-owned item before starting the coding model.
Do not qualify it by repairing an application's pipeline.
Advertise the exact admitted body as well as the header mapping.
For that adapter, a conditional mode action is:

```json
{
  "command": "source",
  "method": "PATCH",
  "path": "/metadata/artifacts/<owned-eventstream-id>",
  "ifMatch": "<preceding-response.etag>",
  "body": {
    "extendedProperties": {
      "EnableSchemaAssociation": 2
    }
  }
}
```

Construct this body independently; do not copy other properties from the metadata GET.
Validate the action before dispatch so a malformed body is not confused with an upstream authorization failure.

The native Kusto model can contain a service-managed `dataConnectionId`, including an all-zero placeholder.
A scoped adapter may preserve it only after reading that exact owned stream, native node, logical identity and owned database binding.
An observed value does not authorize moving the connection to another node, changing it or supplying a foreign connection.
Do not reject the entire writable Kusto graph solely because a verified service-returned property is present.
Preserve an unchanged provider-returned serialized topology; separately validate changed topology and all writable node properties.

Return bounded, non-sensitive validation codes and identify gateway-generated errors.
Do not replace an ownership-validation exception with a generic response that looks like a Fabric rejection, or expose arbitrary exception text.
For an owned runtime-log route, invalid timestamps or filters are input errors, not an authorization denial.
Continue to reject foreign workspaces, capacities, artifacts and nodes.

Before using the adapter for schema-qualified ingestion, qualify the complete authoring path with an unrelated disposable contract.
Verify native source and Kusto selections, graph save, schema-derived physical tables and correlated typed rows through the same scoped adapter used by the coding agent.
Keep this neutral qualification separate from application acceptance evidence, and confirm its resources are absent afterward.
A successful conditional metadata PATCH does not qualify Kusto authoring or physical ingestion.

Fabric source authoring must use verified CLI or REST contracts.
Do not launch a browser or expose portal actions for resource creation, schema association, destination configuration, metadata discovery, or cleanup.
A missing schema-aware API contract blocks that operation; record its method/path, checked reference, observed response, and missing contract instead of guessing fields or using a UI fallback.
Browser verification of a consuming application remains a separate acceptance check.
The gateway admits public source and destination metadata reads only beneath an attempt-owned Eventstream; node mutation routes and baseline-item access remain denied.

For asynchronous Fabric responses, the gateway records a valid `x-ms-operation-id` or a same-origin operation `Location`, then returns its own loopback polling URL.
Operation-state and result requests stay on the pinned public Fabric API; a regional `Location` does not redirect the operator's token to another host.
An accepted create is not a completed item.
If its result is uncertain, reconcile the original operation and exact attempt-owned resources before retrying or claiming cleanup.

A configured gateway is not evidence that a source was provisioned.
Permission preflights, deployed schema readback, bounded data publication, and application acceptance need separate receipts.
Schema-aware Eventstream support and schema-selected KQL integration must be verified independently of Event Schema Set creation.
