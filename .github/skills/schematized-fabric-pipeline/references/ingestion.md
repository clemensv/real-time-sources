# Admit events against the registered contract

Back to [schema-first authoring](./index.md).

Keep three choices separate: the registered payload schema, the CloudEvents envelope mode and the transport binding.
An Avro schema can describe JSON payloads.
Registering that schema neither selects binary Avro nor makes an arbitrary JSON message a recognized CloudEvent.
Preserve the producer's required encoding; do not switch a structured-JSON contract to binary mode to make a test pass.

## Match the actual wire representation

1. Read the selected source's supported protocol and schema-association documentation.
   Fabric's [schema-use guidance](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/schema-sets/use-event-schemas) names `ce-type` as the event-type discriminator.
   Map attributes through the selected protocol's binding; an HTTP header name is not automatically an AMQP application-property name.
   For AMQP property names and structured-mode metadata, follow [the AMQP binding details](./amqp-binding.md).
   See the official [CloudEvents bindings](https://github.com/cloudevents/spec/tree/main/cloudevents/bindings), including AMQP, Kafka and HTTP.
2. In structured JSON mode, send the complete CloudEvent as UTF-8 bytes with the structured media type `application/cloudevents+json` on the actual message.
   Its `data` is the payload, not another CloudEvents envelope.
   Envelope `datacontenttype: application/json` describes that payload; it is not the structured message's content type.
   In binary mode, attributes occupy transport metadata and the body contains only the payload.
   Use binary mode only when the producer contract permits it.
3. Keep the exact registered CloudEvents `type`, source, subject and event ID.
   The event type, schema-resource ID and Avro record name are different identifiers.
   If a deployed schema URI is required, obtain it from authorized programmatic service metadata and record its schema/version binding.
   Missing metadata access or an unknown API contract is a blocker, not permission for browser automation.
   A local `#/schemas/...` reference is not a deployed wire URI.
   Never construct a Catalog hostname, group ID or version suffix from examples.
   For the native custom endpoint's required `dataschema` and canonical-versus-alias distinction, follow [native wire metadata](./native-wire.md).
4. Inspect the encoded message, not just the object passed to the SDK.
   With a batch transport, inspect the inner event's content type, attributes and body.
   A successful send acknowledgement proves broker acceptance, not Eventstream recognition.
   Do not add several guessed attribute-prefix variants or replace the serializer without evidence of a binding error.

## Separate observations

In the 2026-11-16 feeder pilot, structured Kafka messages were broker-accepted
but rejected by the registered receiver for missing transport-level `type`.
The source's separately declared AMQP binary binding passed acceptance.
The Kafka custom output retained AMQP-encoded `cloudEvents:` header values;
it did not establish a native Kafka `ce_` binding. These are observations
of that tested provider configuration, not universal transport restrictions.
Inspect the real output with its codec instead of assuming UTF-8 header values.

Generated producers can omit schema metadata despite schema references in the
manifest. Track the fix in
[xregistry/codegen#693](https://github.com/xregistry/codegen/issues/693);
do not assume an issue under development is released. File-backed relative
schema references and API-backed absolute references must retain their intended
resolution semantics. Fabric admission may separately require the actual
service-issued registered version URI. Never invent its base URL.
An approved deployment-boundary adaptation must be explicit, tested and linked
to its removal condition; do not make a temporary producer subclass the fleet
architecture or patch generated source. Remove it only after regeneration and
fresh output/history proof with the supported generator.

Publish a small authorized probe with new IDs after the source is ready.
Use real measurements when the scenario requires them; do not synthesize telemetry.
Inspect the actual upstream source/default stream, not an unsaved destination's test preview.
Record the recognized event type/version and inspect source runtime logs for validation failures.
Use [approved native runtime-log reads](./native-diagnostics.md) when working through the native API.
An associated schema, a preview label and a `Running` status answer different questions.

The public association workflow does not establish a callable native metadata API or its token audience.
An HTTP 401/403 is an access blocker: retain sanitized request/status evidence and stop that diagnostic route.
Do not try another identity, guess private endpoints or treat denied metadata as an empty result.
Metadata access is not a substitute for the [destination and storage check](./verification.md).
