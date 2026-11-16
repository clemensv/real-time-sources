# Create an Event Schema Set by REST

Back to [Event Schema Set definition](./schema-set-definition.md).

The required `definition.parts[].path` is `EventSchemaSetDefinition.json`, with that exact spelling and casing.
Do not substitute `EventSchemaSetV1.json`.
The [Create Event Schema Set sample](https://learn.microsoft.com/en-us/rest/api/fabric/eventschemaset/items/create-event-schema-set) uses that conflicting name; the [definition contract's required-part table](https://learn.microsoft.com/en-us/rest/api/fabric/articles/item-management/definitions/eventschemaset-definition) specifies `EventSchemaSetDefinition.json`.
A local filename does not determine the provider's definition-part path.

Save your scenario's projected definition as `EventSchemaSetDefinition.json`, then prepare the request:

```javascript
import { readFile, writeFile } from 'node:fs/promises';

const definition = JSON.parse(
  await readFile('EventSchemaSetDefinition.json', 'utf8')
);
const request = {
  displayName: 'Device events',
  definition: {
    parts: [
      {
        path: 'EventSchemaSetDefinition.json',
        payload: Buffer.from(JSON.stringify(definition), 'utf8').toString(
          'base64'
        ),
        payloadType: 'InlineBase64',
      },
    ],
  },
};
await writeFile(
  'schema-set-request.json',
  JSON.stringify(request, null, 2),
  'utf8'
);
```

Submit the request through the approved REST transport or the authenticated Fabric CLI:

```shell
fab api "workspaces/<workspaceId>/eventSchemaSets" -X post -i schema-set-request.json --show_headers
```

Complete any long-running operation and read back the definition before using the item.
An HTTP 500 does not establish that nothing was created; preserve the error and request ID and reconcile the mutation before retrying.
