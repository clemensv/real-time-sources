# CloudEvents attributes on AMQP

Back to [registered-contract admission](./ingestion.md).

Read the [official AMQP binding](https://github.com/cloudevents/spec/blob/main/cloudevents/bindings/amqp-protocol-binding.md).
The HTTP header `ce-type` is not its AMQP attribute mapping.
AMQP uses application properties such as `cloudEvents:type`, `cloudEvents:specversion`, `cloudEvents:id` and `cloudEvents:source`.
The binding also permits the `cloudEvents_` separator.
Choose one consistent permitted separator; do not send guessed prefix variants.

## Preserve the selected content mode

In structured JSON mode, keep the full CloudEvent in the body and set the actual AMQP message content type to `application/cloudevents+json`.
The JSON `datacontenttype` still describes `data`.
In binary mode, the body contains only the payload, its media type is the AMQP content type, and the other attributes occupy application properties.
Do not silently change a producer's required structured mode to binary.
If the contract requires JSON payloads but permits either CloudEvents content mode, binary mode can carry those JSON bytes without an envelope in the body.
CloudEvents binary mode does not select Avro binary payload encoding.
For the verified native custom-endpoint path, use the `cloudEvents:` mapping; a separator allowed by the general standard is not proof of receiver support.
Before publishing, bind `dataschema` to the [actual canonical native schema](./native-wire.md).

The binding's section 3.2.3 permits structured messages to carry the same attribute application properties as binary messages.
If a source adapter requires transport attributes as well as a structured body, mirror the event's actual attributes using the AMQP namespace.
Keep every mirrored value equal to its JSON value.
Include the required attributes together, not just `type`; preserve optional attributes that the registered contract uses.
The structured body and its media type remain unchanged.

## Inspect the encoded inner message

For the JavaScript Event Hubs SDK, `EventData.contentType` is the message content type and `EventData.properties` holds application properties.
Check the installed SDK version and encode/decode an actual SDK batch offline.
Inspect each inner message's AMQP `content_type`, application properties and exact UTF-8 body bytes.
Do not infer these from the outer batch envelope or the original JavaScript object.

Use [native runtime diagnostics](./native-diagnostics.md) after a bounded probe.
`CloudEventPropertyMissingException` for `type`, despite a JSON `type` field, requires checking the content type and source's transport-attribute lookup.
It does not prove that the payload schema is missing.
Record the observed property names and apply the documented binding, then publish new measured events.
If the source still cannot admit the required encoding, retain the exact error and report the incompatibility; do not replace the required wire contract or claim ingestion.
