# Event Schema Set definition

Back to [schema-first authoring](./index.md).

The following original example defines two signals with separate Avro payload schemas.
It is the content of `EventSchemaSetDefinition.json`, not the complete Fabric item-creation request.
Its arrays, field casing and schema-text representation follow the public [EventSchemaSet definition contract](https://learn.microsoft.com/en-us/rest/api/fabric/articles/item-management/definitions/eventschemaset-definition).

```json
{
  "eventTypes": [
    {
      "id": "example.device.reading",
      "format": "CloudEvents/1.0",
      "envelopeMetadata": {
        "id": { "type": "string", "required": true },
        "type": {
          "type": "string",
          "required": true,
          "value": "example.device.reading"
        },
        "source": { "type": "string", "required": true },
        "specversion": {
          "type": "string",
          "required": true,
          "value": "1.0"
        }
      },
      "schemaUrl": "#/schemas/example.device.reading",
      "schemaFormat": "Avro/1.12.0"
    },
    {
      "id": "example.device.alarm",
      "format": "CloudEvents/1.0",
      "envelopeMetadata": {
        "id": { "type": "string", "required": true },
        "type": {
          "type": "string",
          "required": true,
          "value": "example.device.alarm"
        },
        "source": { "type": "string", "required": true },
        "specversion": {
          "type": "string",
          "required": true,
          "value": "1.0"
        }
      },
      "schemaUrl": "#/schemas/example.device.alarm",
      "schemaFormat": "Avro/1.12.0"
    }
  ],
  "schemas": [
    {
      "id": "example.device.reading",
      "format": "Avro/1.12.0",
      "versions": [
        {
          "id": "v1",
          "format": "Avro/1.12.0",
          "schema": "{\"type\":\"record\",\"name\":\"DeviceReading\",\"namespace\":\"example.device\",\"fields\":[{\"name\":\"deviceId\",\"type\":\"string\"},{\"name\":\"temperatureC\",\"type\":\"double\"}]}"
        }
      ]
    },
    {
      "id": "example.device.alarm",
      "format": "Avro/1.12.0",
      "versions": [
        {
          "id": "v1",
          "format": "Avro/1.12.0",
          "schema": "{\"type\":\"record\",\"name\":\"DeviceAlarm\",\"namespace\":\"example.device\",\"fields\":[{\"name\":\"deviceId\",\"type\":\"string\"},{\"name\":\"code\",\"type\":\"string\"}]}"
        }
      ]
    }
  ]
}
```

`versions[].schema` contains JSON text, not an embedded object.
Serialize an object schema once; preserve an already textual schema without double encoding.
An event type can use `schemaUrl` or an inline `schema`, not both.
The local references above follow the documented schema-resource form.
For multiple versions, resolve the intended version using the supported reference/default-version behavior and retain that choice; do not invent a version-pointer syntax.
Use the schema formats and versions supported by the target.
An Avro schema does not select Avro binary transport encoding.

This example uses matching event-type and schema-resource IDs; Avro record names remain separate.
A native Fabric picker was observed requesting versions by event-type ID, but that does not make differing IDs invalid xRegistry.
If the target picker requires an alias, retain the original schema, version and declared reference; add a byte-identical alias under the event-type ID with the same pinned version and record the mapping.
An alias or an accepted definition does not prove recognition or storage.
Complete the [registered-schema ingestion check](./verification.md); do not change identifiers or version references as an unverified fix.

Package this document with the required definition-part path using [the REST request example](./schema-set-request.md).
