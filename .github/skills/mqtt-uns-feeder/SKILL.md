---
name: mqtt-uns-feeder
description: "Use when adding MQTT/Unified-Namespace transport to a feeder in this repo — either alongside an existing Kafka feeder (transport split) or for a brand-new source where MQTT is the primary fit. Covers UNS topic-tree design, xRegistry MQTT messagegroup pattern, paho-mqtt v5 binary-mode CloudEvent emission, Entra JWT enhanced auth for Event Grid namespace brokers, two-app folder layout sharing a core acquisition module, Dockerfile.mqtt + dedicated pyproject, two MQTT ARM templates (BYO broker + Event Grid namespace), the read-only test-client registration helper, MQTT Docker E2E, and the four-button portal/README update."
argument-hint: "Describe the source id, what data families it emits, the upstream identifiers that will form the UNS topic hierarchy, and whether the source already has a Kafka feeder (transport split) or this is greenfield MQTT-only."
---

# MQTT / Unified Namespace Feeder

This skill describes how to add MQTT transport to a feeder so that its
events are published into a **Unified Namespace** topic tree carrying
binary-mode MQTT 5.0 CloudEvents with JSON payloads. The pegelonline
source is the reference implementation — read its files alongside this
document.

The skill applies in two shapes:

1. **Transport split** — an existing source already ships a Kafka feeder
   and you are adding an MQTT sibling (the pegelonline pattern).
2. **MQTT-first** — a brand-new source whose data shape is so well-suited
   to LKV-on-retained-topics that Kafka may not even be added later.

Either way, the runtime never publishes to both transports from the same
process. There are always two independent containers, two independent
pyproject.toml files, two independent images, and two independent ARM
templates.

## When to Use

- Add MQTT/UNS publication to an existing Kafka source.
- Greenfield source where the upstream data is naturally a hierarchical
  catalog of stable identifiers (stations, vessels, zones, sensors) each
  emitting periodic measurements.
- Refactor a feeder so the acquisition logic is shared between Kafka and
  MQTT apps.

## When **not** to Use

- High-volume firehose telemetry without stable per-object identity
  (raw lightning strokes, raw AIS sentences, raw firehoses): UNS LKV
  semantics do not fit.
- Sources whose payloads exceed MQTT broker per-message limits.
- Sources that need consumer-side replay/seek to historical offsets.
  MQTT retained slots only hold the **last** value per topic.

## Mandatory Expert Reviews

Three subagents must review the MQTT design **before** generation runs:

| Aspect | Reviewer | What to ask |
|--------|----------|-------------|
| Topic tree | `Antwerp City Intelligence` is **not** the right one. Use the **MQTT Unified Namespace expert** if a user-provided UNS agent is listed in `<available_skills>`; otherwise consult the `xRegistry Expert` who knows the UNS-on-xRegistry mapping. | Validate the hierarchy depth, segment naming, wildcard fitness, retained vs non-retained per event type, QoS, single-vs-multi-topic-per-object decisions. |
| xRegistry MQTT contract | `xRegistry Expert` | Validate the `MQTT/5.0` endpoint, the dedicated `<source>.mqtt` messagegroup with `basemessageurl` references back into the transport-neutral group, and the `protocoloptions.properties` (topic / qos / retain). |
| Schemas | `JSON Structure Expert` | Re-confirm that JsonStructure schemas (shared with Kafka) still cover every field; add no MQTT-specific schema drift. |

Do not skip these reviews. Even when the same human contract author
also wrote the Kafka contract, MQTT-specific decisions (retained slots,
wildcards, key/topic alignment) require an independent expert pass.

## Inputs

- source id (e.g. `pegelonline`)
- list of event types and their identity tuple (e.g. `Station` keyed on
  `water_shortname/station_id`, `CurrentMeasurement` keyed on the same)
- decision: which events are **retained** (LKV) and which are not
- the UNS domain prefix the source belongs to
  (e.g. `hydro/de/wsv/pegelonline/...`)
- whether a Kafka feeder already exists in the folder

## Non-Negotiables

- One process, one transport. Never emit MQTT and Kafka from the same
  Python process or container.
- The MQTT and Kafka messagegroups **share schemas** (single
  `schemagroups.<source>.jstruct` block). MQTT messages declare
  `basemessageurl` back to the transport-neutral message definitions.
- The MQTT topic uritemplate **must use the same identity tuple** as the
  Kafka subject and key. The placeholder names match across all three.
- All MQTT payloads use **binary-mode CloudEvents** (CloudEvents
  metadata in MQTT v5 user properties / system properties; payload is
  the raw JSON body). Never use structured-mode JSON envelopes.
- Reference events (catalog data) are emitted with `retain: true` once
  at startup and re-emitted on periodic refresh.
- Telemetry events whose latest value is meaningful in isolation are
  also retained (LKV). Telemetry that is only meaningful as a stream
  (e.g. discrete alerts, event streams) is **not** retained.
- The MQTT app is generated through `xrcg 0.10.1` exactly as Kafka is.
  The generated producer is never hand-edited.
- Authentication is configurable at runtime (anonymous / username-password
  / TLS-cert / Entra JWT). The contract does not pin the auth mode.

## Recommended UNS Topic-Tree Shape

```
<domain>/<country>/<authority>/<source>/<sub-group>/<object-id>/<event-type>
```

- `<domain>` is the broad data domain (`hydro`, `air`, `traffic`,
  `maritime`, `energy`, `seismic`, `weather`, ...).
- `<country>` is the ISO 3166-1 alpha-2 code (lower-case) where the
  upstream authority operates.
- `<authority>` is the issuing body (`wsv`, `noaa`, `dwd`, `bom`).
- `<source>` is the canonical source id (matches the repo folder name).
- `<sub-group>` is a stable upstream grouping that aids wildcard
  subscriptions (basin, region, agency, vessel-class). Skip this level
  only if no such grouping exists.
- `<object-id>` is the stable per-object identifier (station UUID,
  MMSI, gauge number, sensor id).
- `<event-type>` is a kebab-cased noun describing what the topic carries
  (`info`, `water-level`, `metar`, `alert`, ...).

Rules:

- Lower-case kebab-case everywhere. No human names. No display labels.
- Use the same identity placeholders as the Kafka key/subject template
  (verbatim placeholder names).
- One **retained, QoS-1** topic per (object, event-type) pair. Subscribers
  joining the broker mid-stream see the latest state immediately.
- Subscribers consuming a sub-tree wildcard (e.g. `hydro/de/wsv/+/+/+/water-level`)
  must get a coherent slice of state without needing replay.

Worked example (pegelonline):

```
hydro/de/wsv/pegelonline/<water_shortname>/<station_id>/info          (retained, QoS-1)
hydro/de/wsv/pegelonline/<water_shortname>/<station_id>/water-level   (retained, QoS-1)
```

## xRegistry Contract Pattern

Add two siblings to the existing transport-neutral content:

1. **A new endpoint** `<rev-dns>.<Source>.Mqtt` with `protocol: "MQTT/5.0"`
   that points at `#/messagegroups/<rev-dns>.<source>.mqtt`.
2. **A new messagegroup** `<rev-dns>.<source>.mqtt` whose messages each
   carry:
   - `basemessageurl` referencing the transport-neutral message in
     `<rev-dns>.<source>` (so the schema is shared);
   - `protocol: "MQTT/5.0"`;
   - `protocoloptions.properties.topic` of type `uritemplate` with a
     value matching the Kafka subject/key shape;
   - `protocoloptions.properties.qos` (integer, typically `1`);
   - `protocoloptions.properties.retain` (boolean, per event-type
     retention decision).

Look at
`pegelonline/xreg/pegelonline.xreg.json` lines 23–41 (endpoint) and
119–167 (messagegroup) for the canonical shape.

Do **not** create a second `schemagroups` block. The MQTT messagegroup
references the same JsonStructure schemas the Kafka messagegroup uses
via `basemessageurl`.

After editing the manifest:

```powershell
./generate_producer.ps1   # already exists; regenerates both Kafka and MQTT
```

`xrcg 0.10.1` produces a generated MQTT producer sub-package alongside
the Kafka one. Treat it as installable but never editable.

## Repository Folder Layout (transport split)

```
<source>/
  README.md
  CONTAINER.md
  EVENTS.md
  Dockerfile.kafka                 # CMD: python -m <source>_kafka feed
  Dockerfile.mqtt                  # CMD: python -m <source>_mqtt  feed
  generate_producer.ps1
  xreg/<source>.xreg.json
  <source>/                        # shared core acquisition + config
    __init__.py
    acquisition.py
    config.py
    state.py
  <source>_kafka/
    pyproject.toml                 # depends on the generated Kafka producer
    <source>_kafka/
      __init__.py
      __main__.py
      app.py                       # owns the Kafka producer lifecycle
  <source>_mqtt/
    pyproject.toml                 # depends on the generated MQTT producer
    <source>_mqtt/
      __init__.py
      __main__.py
      app.py                       # owns the MQTT producer lifecycle
  <source>_producer/               # xrcg output — never edited
  azure-template.json              # Kafka, BYO Event Hub
  azure-template-with-eventhub.json
  azure-template-mqtt.json         # MQTT, BYO broker
  azure-template-with-eventgrid-mqtt.json
  tests/
    test_<source>_kafka_app.py
    test_<source>_mqtt_app.py
```

The shared core package (`<source>/`) owns everything that is identical
between transports: HTTP/MQTT/WS acquisition of the upstream, config
parsing, state/dedupe, normalization into the generated data classes.
Both `<source>_kafka/app.py` and `<source>_mqtt/app.py` import from it.

## Runtime Bridge Pattern (MQTT app)

Use `paho-mqtt >= 2.1` as the only MQTT client. The generated producer
already wraps it.

- Parse source + MQTT configuration from env vars and CLI args
  (see [MQTT environment variables](#mqtt-environment-variables)).
- Pick the auth mode at runtime: `anonymous` | `userpass` | `tls-cert`
  | `entra`.
- Connect (see auth-specific notes below), then start the paho loop.
- Emit **reference events first** (catalog) as retained QoS-1, then
  enter the telemetry loop.
- Re-emit reference events on a periodic refresh (same cadence as the
  Kafka feeder).
- Pass topic placeholders **explicitly** to the generated producer's
  `send_*` methods — never hide them inside a key/topic mapper.

### MQTT environment variables

The contract:

| Variable | Required | Default | Description |
|---|---|---|---|
| `MQTT_BROKER_URL` | yes | — | `host:port` of the broker. TLS implied at 8883 / configurable. |
| `MQTT_ENABLE_TLS` | no | `true` | Enable TLS. Always `true` for cloud brokers. |
| `MQTT_AUTH_MODE` | no | `anonymous` | `anonymous` / `userpass` / `tls-cert` / `entra`. |
| `MQTT_USERNAME` | conditional | — | For `userpass`. Also used as MQTT username in `entra` (the Client resource name on Event Grid). |
| `MQTT_PASSWORD` | conditional | — | For `userpass`. |
| `MQTT_CLIENT_CERT` | conditional | — | PEM path for `tls-cert`. |
| `MQTT_CLIENT_KEY` | conditional | — | PEM path for `tls-cert`. |
| `MQTT_CA_FILE` | no | system trust | Path to the broker CA chain. |
| `MQTT_CLIENT_ID` | no | source-derived | MQTT client identifier. |
| `MQTT_ENTRA_CLIENT_ID` | conditional | — | User-assigned MI client id (used as `ManagedIdentityCredential(client_id=…)`). |
| `MQTT_ENTRA_AUDIENCE` | no | `https://eventgrid.azure.net/` | JWT audience. **Must include the trailing slash for EG namespace MQTT.** |

Always make MQTT_BROKER_URL the single point where the broker hostname
is configured. Never hard-code it.

### Auth: Entra JWT enhanced authentication (Event Grid namespace)

This is the only complicated path. Steps:

1. Acquire a token via `azure.identity.ManagedIdentityCredential(client_id=MQTT_ENTRA_CLIENT_ID)`
   (or `DefaultAzureCredential` as fallback) for resource
   `MQTT_ENTRA_AUDIENCE`.
2. Build `paho.mqtt.properties.Properties(PacketTypes.CONNECT)` with:
   - `AuthenticationMethod = "OAUTH2-JWT"`
   - `AuthenticationData = <jwt bytes>`
3. The generated `MqttClient.connect(broker, port, keepalive)` signature
   does **not** accept properties, so bypass it: call
   `paho_client.connect(host, port, keepalive=60, clean_start=True, properties=props)`
   then `paho_client.loop_start()` directly. Take the underlying paho
   client off the generated wrapper's `.client` attribute.
4. Start a background asyncio task that refreshes the token ~5 minutes
   before expiry. paho-mqtt 2.1 has no `reauth()`, so refresh = call
   `paho_client.disconnect()` and reconnect with new CONNECT properties.
5. Apply Azure RBAC at **topic-space scope**, role
   `EventGrid TopicSpaces Publisher` (`a12b0b94-b317-4dcd-84a8-502ce99884c6`).
   No `clients` / `clientGroups` / `permissionBindings` are needed when
   using RBAC.

`pegelonline/pegelonline_mqtt/pegelonline_mqtt/app.py` is the reference
implementation — copy its `_acquire_entra_token` helper and the
`_entra_token_refresh_loop` shape verbatim.

### Auth: X.509 client certificate

Used by the legacy `clients` model (and by the testing tool):

- Configure paho via `tls_set(ca_certs=..., certfile=..., keyfile=...)`.
- The broker matches a `Client` resource by thumbprint or subject CN.
- Authorization is granted via permission bindings on `ClientGroup`s
  selected by `attributes.<name> = '<value>'` queries.

## pyproject.toml — MQTT sibling

```toml
[build-system]
requires = ["poetry-core>=1.1.0"]
build-backend = "poetry.core.masonry.api"

[tool.poetry]
name = "<source>-mqtt"
version = "0.1.0"
packages = [{include = "<source>_mqtt"}]

[tool.poetry.dependencies]
python = ">=3.10,<4.0"
requests = ">=2.32.3"
paho-mqtt = ">=2.1.0"
cloudevents = ">=1.11.0,<2.0.0"
dataclasses_json = ">=0.6.7"
azure-identity = ">=1.17.0"     # only when MQTT_AUTH_MODE=entra is supported
<source>_producer_data         = {path = "../<source>_producer/<source>_producer_data"}
<source>_producer_mqtt_producer = {path = "../<source>_producer/<source>_producer_mqtt_producer"}
```

Install order in containers: `producer_data` → `producer_mqtt_producer`
→ `<source>-mqtt`.

## Dockerfile.mqtt convention

```dockerfile
FROM python:3.10-slim
LABEL source="<source>" \
      title="<Source> MQTT feeder" \
      description="<one-liner>" \
      documentation="https://github.com/clemensv/real-time-sources/blob/main/<source>/CONTAINER.md" \
      license="MIT"
# … install order: producer_data → producer_mqtt_producer → <source>_mqtt
CMD ["python", "-m", "<source>_mqtt", "feed"]
```

GHCR image name convention: `ghcr.io/clemensv/real-time-sources-<source>-mqtt:latest`
(distinct from the Kafka image which is `…-<source>-kafka:latest`).

## Azure Deployment Templates

Two MQTT-specific templates must ship alongside the existing two Kafka
ones:

### `azure-template-mqtt.json` — BYO MQTT broker

- Parameters: `mqttBrokerUrl`, optional `mqttUsername`/`mqttPassword`,
  `imageName`, image registry creds.
- Provisions: an ACI running the `…-<source>-mqtt:latest` image.
- Env: `MQTT_BROKER_URL`, `MQTT_AUTH_MODE` (defaults to `userpass` or
  `anonymous` based on inputs).

### `azure-template-with-eventgrid-mqtt.json` — full Event Grid namespace

Provisions, in order:

1. `Microsoft.EventGrid/namespaces` with `topicSpacesConfiguration.state = 'Enabled'`.
2. A `topicSpaces` child with template `<topicRoot>` (default `<domain>/#`).
3. A user-assigned managed identity.
4. A role assignment of `EventGrid TopicSpaces Publisher`
   (`a12b0b94-b317-4dcd-84a8-502ce99884c6`) **scoped to the topic space**.
5. An ACI with the user-assigned MI attached and env vars:
   - `MQTT_AUTH_MODE=entra`
   - `MQTT_ENTRA_CLIENT_ID = <MI.clientId>`
   - `MQTT_BROKER_URL = reference(<ns>, '2025-07-15-preview').topicSpacesConfiguration.hostname:8883`

### ARM gotchas (do not repeat these mistakes)

- The role assignment is scoped to the *topic space*, not the resource
  group. In the ACI `dependsOn`, reference it via
  `extensionResourceId(<topicSpaceResourceId>, 'Microsoft.Authorization/roleAssignments', <name>)`.
  Plain `resourceId('Microsoft.Authorization/roleAssignments', name)`
  resolves to the RG scope and the template will fail validation.
- The broker hostname **must be live-sourced** with
  `reference(<namespaceResourceId>, '2025-07-15-preview').topicSpacesConfiguration.hostname`.
  Do not assemble it from the region — the Event Grid team has reserved
  the right to change the suffix.
- The container image defaults to the public ghcr.io image published by
  the repo build; no `imageRegistryCredentials` are needed. Add them back
  only if you fork and host the image in a private registry.

Use `pegelonline/azure-template-with-eventgrid-mqtt.json` as the
template — copy and adapt the namePrefix / topicRoot / imageName.

## Testing Helper

`tools/Register-EventGridMqttTestClient.ps1` registers a read-only
client on any Event Grid namespace, generates a self-signed cert,
fetches the broker's CA chain live, and drops `.crt` / `.key` /
`-ca.crt` files into the current directory. Use it for MQTTX inspection
during development. The script grants only the `Subscriber` permission
on the chosen topic space (publishing is denied).

## Docker E2E

Ship a sibling test class in `tests/docker_e2e/test_docker_mqtt_flow.py`
that:

1. Boots `eclipse-mosquitto:2` alongside the `<source>_mqtt` image in
   the same compose-style topology used by the Kafka E2E.
2. Subscribes a paho client to the source's UNS root wildcard.
3. Asserts:
   - At least one **retained** message for every reference topic.
   - At least one telemetry message under each declared event type.
   - Topic strings match the uritemplate from the xreg manifest.
   - Binary-mode CloudEvent properties (`ce_specversion`, `ce_type`,
     `ce_source`, `ce_subject`, `ce_id`, `ce_time`, `content_type`) are
     present in the MQTT v5 user properties.
   - Payload validates against the JsonStructure schema in the manifest.

A source is not done until this passes.

## Documentation Surface

- **CONTAINER.md** — split env-var tables (Kafka section + MQTT section),
  four Deploy-to-Azure badges (Kafka container, Kafka container + Event
  Hubs, MQTT container, MQTT container + Event Grid namespace), MS-Learn
  link to the EG namespace MQTT broker docs.
- **EVENTS.md** — regenerate so it includes the MQTT messagegroup with
  topic patterns.
- **README.md** — add a "Transports" section that explains the
  Kafka-vs-MQTT choice and lists the four deployment templates.
- **Root README.md** — append the MQTT image and the two MQTT deploy
  badges to the source's row.
- **Portal hooks** — set `mqtt: true` on the source entry in both
  `app.js` and `catalog.json` on `main`. Two extra buttons
  (`btn-container-mqtt`, `btn-container-mqtt-eg`) already exist in the
  `ghpages` branch's `index.html`; they auto-show for any source whose
  catalog entry carries `mqtt: true`. Two hash deep-links also work:
  `#<id>/azure-mqtt` and `#<id>/azure-mqtt-eg`.

## Implementation Sequence

1. **Topic-tree review** with the UNS expert (or the xRegistry Expert if
   the UNS agent is not available).
2. **xRegistry edit** — add the Mqtt endpoint + the `<source>.mqtt`
   messagegroup. Run xRegistry Expert review.
3. **Regenerate** producers via `./generate_producer.ps1`.
4. **Folder split** — move the existing Kafka app into `<source>_kafka/`
   if it isn't already split. Create the `<source>_mqtt/` sibling.
5. **MQTT runtime bridge** in `<source>_mqtt/<source>_mqtt/app.py`,
   sharing the core acquisition module with the Kafka app.
6. **Unit + integration tests** for the MQTT app under
   `tests/test_<source>_mqtt_app.py`.
7. **Dockerfile.mqtt** and the MQTT pyproject.
8. **Two ARM templates** (BYO broker + Event Grid namespace).
9. **MQTT Docker E2E** in `tests/docker_e2e/test_docker_mqtt_flow.py`.
10. **Doc refresh**: CONTAINER.md, EVENTS.md, README.md, root README.md.
11. **Portal hooks**: `mqtt: true` in `app.js` + `catalog.json`.
12. **Live smoke test** with `Register-EventGridMqttTestClient.ps1` +
    MQTTX (recommended even outside CI).

## Common Failure Modes

| Symptom | Cause | Fix |
|---|---|---|
| Connect succeeds, no events flow | Forgot to override the generated `MqttClient.connect()` for `entra` auth | Bypass the generated wrapper; call `paho.connect(..., properties=connect_props)` directly. |
| Connect rejected with NOT_AUTHORIZED | Wrong RBAC scope or missing role assignment | Assign `EventGrid TopicSpaces Publisher` (`a12b0b94-…`) at the topic-space scope, not the namespace or RG. |
| Connect rejected after ~24 h | Entra token expired, no refresh loop | Add the disconnect+reconnect refresh task. paho 2.1 has no `reauth()`. |
| Subscriber sees no retained reference data | Telemetry was emitted before reference data, or `retain: true` was missing in the contract | Emit reference data first; verify `retain: true` is present in `protocoloptions.properties.retain`. |
| Template validation error on the role assignment | `dependsOn` uses `resourceId('Microsoft.Authorization/roleAssignments', name)` | Use `extensionResourceId(<topicSpaceResourceId>, 'Microsoft.Authorization/roleAssignments', name)`. |
| Hostname looks wrong (region suffix changed) | Hardcoded `<ns>.<region>-1.ts.eventgrid.azure.net` | Use `reference(<ns>, '2025-07-15-preview').topicSpacesConfiguration.hostname`. |
| `ConvertFrom-Json` fails in tooling | `az` CLI emits SyntaxWarnings to stderr that get mixed into stdout | Capture stdout only (no `2>&1`); let stderr pass through. |
| Test client cannot validate broker cert | Self-signed client cert was used as the "CA file" | Fetch the broker's server-cert chain at runtime (see `Register-EventGridMqttTestClient.ps1`). |
| MQTTX shows "publish failed" but no error code | Broker is silently denying the publish | The client only holds Subscriber permission; this is correct. Add a Publisher binding for a different identity to test publishing. |

## References

- Reference implementation: `pegelonline/pegelonline_mqtt/pegelonline_mqtt/app.py`
- Reference xreg: `pegelonline/xreg/pegelonline.xreg.json`
- Reference ARM (EG namespace): `pegelonline/azure-template-with-eventgrid-mqtt.json`
- Reference Dockerfile: `pegelonline/Dockerfile.mqtt`
- Reference Docker E2E: `tests/docker_e2e/test_docker_mqtt_flow.py`
- Testing helper: `tools/Register-EventGridMqttTestClient.ps1`
- xrcg generator: <https://github.com/clemensv/xrcg> (pinned at 0.10.1)
- Event Grid namespace MQTT broker docs:
  <https://learn.microsoft.com/azure/event-grid/mqtt-overview>
- MQTT v5 Enhanced Authentication for OAuth/JWT (Event Grid namespace):
  <https://learn.microsoft.com/azure/event-grid/mqtt-client-microsoft-entra-token-authentication>
