# Read native Eventstream runtime logs

Back to [native API authoring](./native-api.md).

Use only explicitly approved readonly routes with the same normal artifact-scoped `ES`/`EventStream` authentication as [native model reads](./native-api.md#read-and-save-the-native-model).
This provider-specific contract was checked on 2026-11-09; it is not a public GA REST guarantee.
Keep tokens operator-side.

## Request an owned node's logs

Read the current owned `/model` first.
Resolve the node's native `id` in `properties.dataSources` or `properties.streams`, not its public `logicalId`.
Under the approved native artifact workload base, the provider uses:

```text
GET <base>/datasources/<nativeDataSourceId>/logs
GET <base>/streams/<nativeStreamId>/logs
```

Supply these query parameters:

| Parameter        | Value                                  |
| ---------------- | -------------------------------------- |
| `startTimeInUTC` | UTC ISO timestamp                      |
| `endTimeInUTC`   | Later UTC ISO timestamp                |
| `eventChannels`  | `Admin,Operation`                      |
| `levels`         | `Critical,Error,Warning,Informational` |

Percent-encode the query values, not the path identifiers.
Use UTC ISO timestamps such as `2026-11-11T00:50:47.040Z` or `2026-11-11T00:50:47.040599+00:00`.
The scoped adapter accepts `Z` or an explicit `+00:00` offset and up to nine fractional-second digits; other offsets are not UTC input for this contract.
JavaScript's `Date.toISOString()` supplies the simpler millisecond form.
Use a finite recent window covering the actual publication; a scoped adapter can restrict it to at most one hour within the last day.
Do not add unadmitted filters or query another artifact.

The JSON response has `logs` and `continuationToken`.
Read each log's message, severity and timestamp; correlate it with the post-readiness probe.
Record a nonempty continuation token as incomplete evidence.
Narrow the time window or use separately approved paging rather than assuming the first response is complete.

## Distinguish unsupported nodes from empty results

The native CustomApp source can return HTTP 400 `WorkloadUserException` stating that activity logs are unsupported for `SourceCustomApp`.
That is not an empty successful log response.
The connected native Kusto destination's logs can expose upstream Event Hub receiver/schema-validation failures, including dropped events.
Read that owned node through its verified route; do not invent a source-preview endpoint.

An HTTP 401/403 is an access denial: stop that route without trying another identity or endpoint.
An adapter-generated HTTP 400 `source-authoring-native-log-query-invalid` instead identifies invalid query parameters before provider access.
Check the timestamp format, finite interval, required parameter names and exact channel/level values rather than requesting broader permissions.
An empty successful log response also does not prove ingestion.
Keep [wire admission](./amqp-binding.md) separate from [schema-qualified physical storage](./verification.md).
