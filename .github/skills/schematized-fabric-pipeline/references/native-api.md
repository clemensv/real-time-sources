# Native schema-aware Eventstream APIs

Back to [CLI or REST authoring](./programmatic.md).

Use this version-specific provider contract only through explicitly approved access.
It was checked against the Fabric client on 2026-11-09; it is not the public Fabric item API or a stable GA REST guarantee.
Revalidate it after provider changes.
Do not use browser automation.
An approved scoped transport can handle authentication internally; submit the actual relative paths and request bodies, not a scenario-specific setup action.

## Route normal authentication

The operator obtains a normal token for `https://analysis.windows.net/powerbi/api`.
Discover the backend with `GET https://api.powerbi.com/v1.0/myorg/groups/<workspaceId>?preferClientRouting=true`.
`preferClientRouting` is a query parameter, not a header.
Follow only validated HTTPS provider redirects retaining that workspace path and query.
See [normal Power BI routing](https://learn.microsoft.com/en-us/power-bi/developer/embedded/troubleshoot-rest-api).
Do not query capacity metadata, guess a backend or change identities after a denial.

## Create with schema support selected

Send `POST <backendOrigin>/metadata/workspaces/<workspaceId>/artifacts` with normal Bearer authorization:

```json
{
  "artifactType": "EventStream",
  "displayName": "<unique-owned-name>",
  "extendedProperties": {
    "EnableEventStreamApiV2": 1,
    "EnableSchemaAssociation": 2
  }
}
```

Native `EventStream` differs from public item type `Eventstream`.
These native extended properties are not a verified public `creationPayload` mapping.
Journal the create intent and returned `objectId`.
HTTP `202` establishes acceptance and an owned ID, not terminal readiness.
Poll `GET <backendOrigin>/metadata/artifacts/<objectId>` with a finite deadline until `provisionState` is `Active`.
Verify `folderObjectId`, `capacityObjectId`, name, type and `extendedProperties.EnableSchemaAssociation === 2`.
Do not immediately publish a graph merely because metadata is readable.
After graph publication, [recheck and commit the actual schema-set mode](./native-state.md); initial flags can change.

## Read and save the native model

The operator requests an artifact-scoped token with `POST <backendOrigin>/metadata/v201606/generatemwctokenv2`:

```json
{
  "workspaceObjectId": "<workspaceId>",
  "workloadType": "ES",
  "artifacts": [
    { "artifactType": "EventStream", "artifactObjectId": "<objectId>" }
  ]
}
```

Keep the returned `Token` private.
Validate `CapacityObjectId` and the provider-issued `TargetUriHost` against the approved capacity.
Never return token-minting access or raw owner/creator identity metadata to a coding worker.

The workload base is `https://<TargetUriHost>/webapi/capacities/<capacityId>/workloads/ES/ESService/Direct/v2/workspaces/<workspaceId>/artifacts/<objectId>`.
Use `Authorization: MwcToken <Token>` and `x-ms-workload-resource-moniker: <objectId>`, not Bearer authorization, for `GET <base>/model` and `POST <base>/saveTopology`.
An approved transport supplies those headers without exposing credentials.
Continue with [registered source and destination selection](./native-topology.md).
Before the first graph save, [resolve selected versions through the schema-set catalog](./native-catalog.md).

## Delete only owned artifacts

Use `DELETE <backendOrigin>/metadata/artifacts/<objectId>?hardDelete=true` with normal Bearer authorization.
The successful delete body is void; do not require JSON.
Poll both native metadata and public item reads to `404`, then reconcile inventory and capacity.
Preserve all baseline items and consumer groups.
