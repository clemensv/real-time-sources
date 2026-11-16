# Reuse an external feeder

Back to [schema-first authoring](./index.md).

If the developer supplies an external feeder, configure and reuse it instead of building another producer.
The [AIS feeder](https://github.com/clemensv/real-time-sources/tree/main/feeders/aisstream) is one example, not a required application dependency.
Read its configuration, schema variants, supported protocols, CloudEvents mode, routing/subject semantics, authentication and runtime prerequisites.
Verify the selected mode and actual received bytes; a registry description and a feeder README can describe different configurations.
Register/project the contracts it actually emits and associate them with the selected source.
Create a producer only for signals the supplied feeder does not provide.

Pin the generator version and any custom-template revision when regenerating a supplied producer.
Verify that generated publishing code preserves configured envelope constants, especially a required canonical `dataschema`, and inspect the actual encoded packet.
A value in the registry is insufficient if the generator discards it.
For a qualified template correction, use the generator's supported custom-template option and regenerate; do not hand-edit generated serializers or assume that rerunning an unchanged faulty template repairs the output.

Keep feeder credentials and upstream connections in operator/server-owned configuration, never browser code or generated event bindings.
Configure the application's output consumer separately from the feeder's producer input.
When pipeline qualification is requested and authorized, verify real delivery through the source, processing, output, storage and consuming application as applicable.
A connected socket, schema registration, stale receipt or fixture output is not evidence of current end-to-end delivery.
Report an upstream dry period or missing feed instead of manufacturing fallback telemetry.

Next, [prepare the application handoff](./handoff.md).
