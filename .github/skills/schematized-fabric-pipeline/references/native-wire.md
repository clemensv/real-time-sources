# Bind native wire metadata to the original schema

Back to [registered-version resolution](./native-catalog.md) and [AMQP binding](./amqp-binding.md).

## Resolve the wire identity before sending

The verified native custom-endpoint receiver requires `dataschema`, even when the registered envelope metadata does not mark it required.
Treat `CloudEventPropertyMissingException` for `dataschema` as a missing wire attribute, not a missing schema-set association.
Resolve this attribute together with the other required CloudEvents attributes before spending a bounded publication probe.

Read the registered event type and the pinned original schema version through the [approved catalog reads](./native-catalog.md).
The event type's actual `schemaUrl` identifies its canonical schema resource.
An event-type-ID schema alias can satisfy the provider's picker lookup without changing that declared reference.
Byte-identical schemas do not make those resource URIs interchangeable.
Using the alias as `dataschema` can produce `CloudEventPropertyValidationException` even though both versions exist.

Preserve the original schema ID and pinned version when resolving the canonical version resource URI.
A version `selfUrl` ending in `$details` identifies metadata, not the schema content resource.
Resolve the content URI from actual returned metadata and the [xRegistry resource-URI contract](https://github.com/xregistry/spec/blob/main/core/spec.md).
Do not copy an alias or metadata-document URL blindly, invent a Catalog hostname, or follow returned URLs with borrowed credentials.

## Keep content mode separate from payload encoding

For AMQP binary CloudEvents with JSON payloads, the message body is only the payload's UTF-8 JSON bytes.
Set the actual AMQP message content type to `application/json`.
Put attributes such as `specversion`, `id`, `type`, `source`, `subject`, `time` and the canonical `dataschema` in `cloudEvents:` application properties.
If an SDK also supplies a `datacontenttype` application property, it must agree with the message's content type.
This mode does not require Avro binary serialization merely because the registered schema language is Avro.

Use this representation only when the producer contract permits binary CloudEvents.
An explicitly required structured JSON body must remain a full envelope with `application/cloudevents+json`.
Do not nest that envelope where a binary receiver expects payload fields.
Use [actual SDK inner-message inspection](./amqp-binding.md), then collect [runtime logs](./native-diagnostics.md) and [physical storage evidence](./verification.md).
`InputDeserializerError.InvalidData` after metadata recognition is still a failure; neither a valid header nor a broker acknowledgement proves payload admission.
