---
name: amqp-feeder
description: "Use when adding AMQP 1.0 transport to a feeder in this repo — either alongside an existing Kafka/MQTT feeder or for a brand-new source. Covers generic AMQP brokers (RabbitMQ AMQP 1.0 plugin, ActiveMQ Artemis, Qpid Dispatch) via SASL PLAIN, Azure Service Bus / Event Hubs via Entra ID (AMQP CBS put-token, no SAS-key minting), xRegistry AMQP endpoint and messagegroup pattern, the `--azure_cbs_target` xrcg generator switch, two-app folder layout sharing a core acquisition module, Dockerfile.amqp, ARM template for Service Bus, and CI matrix integration. Pegelonline is the reference implementation."
argument-hint: "Describe the source id, what data families it will emit, whether it already has a Kafka/MQTT feeder (transport addition) or this is greenfield AMQP-only, and whether the deployment targets generic brokers, Azure Service Bus, Azure Event Hubs, or all of the above."
---

# AMQP 1.0 Feeder

This skill describes how to add AMQP 1.0 transport to a feeder so that
its events are published as CloudEvents to:

- **Generic AMQP 1.0 brokers** — RabbitMQ AMQP 1.0 plugin, ActiveMQ
  Artemis, Qpid Dispatch — via SASL PLAIN.
- **Azure Service Bus** queues/topics via Entra ID (AMQP CBS put-token).
- **Azure Event Hubs** via Entra ID (same CBS path, different audience).

The `pegelonline` source is the reference implementation; read its
`pegelonline_amqp/`, `Dockerfile.amqp`, and
`azure-template-with-servicebus.json` alongside this document.

The skill applies in two shapes:

1. **Transport addition** — a source already ships Kafka and/or MQTT
   feeders, and you are adding an AMQP sibling. Typical when consumers
   prefer AMQP 1.0 message semantics (transactions, pull-mode
   consumption, broker-side filters) or want Service Bus's per-message
   TTL, dead-lettering, and scheduled delivery.
2. **AMQP-first** — a brand-new source whose primary deployment target
   is Azure Service Bus or Event Hubs and where Kafka is not yet planned.

Either way, the runtime never publishes to multiple transports from the
same process. AMQP is its own container, its own pyproject, its own
generated producer, and (when targeting Azure) its own ARM template.

## When to Use

- Add AMQP/Service Bus publication to an existing Kafka or MQTT source.
- Greenfield source where consumers want Service Bus features (queues
  with sessions, topics with subscriptions and SQL filters, per-message
  TTL, scheduled delivery, dead-lettering).
- Greenfield source where consumers want Event Hubs at competitive
  cost, paying for ingestion units rather than a full Kafka cluster.
- Bridging a feeder to a non-Microsoft AMQP 1.0 broker that the consumer
  side already operates (RabbitMQ + AMQP 1.0 plugin in a regulated
  environment, ActiveMQ Artemis on-prem, etc.).

## When **not** to Use

- Sources whose downstream needs a true partition-ordered log with
  consumer-driven seek to historical offsets — use Kafka. AMQP 1.0
  brokers are message-oriented; Event Hubs comes closest but is
  consumed via the EH SDK, not generic AMQP, for replay.
- Sources whose payload model is "last known value per topic with
  retention" — use MQTT/UNS. AMQP 1.0 has no retained-message concept.
- Sources whose volume is so low that even Service Bus' minimum SKU is
  overkill — webhooks or a poller-into-storage may be cheaper.

## Mandatory Expert Reviews

Three subagents must review the AMQP design **before** generation runs:

| Aspect | Reviewer | What to ask |
|--------|----------|-------------|
| xreg contract & subject keying | **xRegistry Expert** | "Review the AMQP messagegroup, endpoint, subject template, and address. Is the address a sensible queue/topic name? Are the subject placeholders the right per-event stable identifiers? Does the schema reuse pattern via `basemessageurl` correctly inherit the base messagegroup's payload schemas?" |
| JsonStructure data shape | **JSON Structure Expert** | "Review every payload schema. Are field descriptions exhaustive? Are units/symbols, altnames, ranges, and enum descriptions present and grounded in the upstream API docs? Any `anyOf`, conditional composition, or other unsupported patterns?" |
| Cloud target sanity | **azure-messaging** (skill) | "Is the chosen Service Bus / Event Hubs SKU appropriate for the projected throughput? Is the queue vs. topic-and-subscription choice right? Is dead-lettering configured? Should we use sessions?" |

If any review surfaces a redesign request, do it **before** running
xrcg, not after.

## Folder Layout

For a source with Kafka + MQTT + AMQP transports, the source folder
contains four side-by-side subpackages and three Dockerfiles:

```
pegelonline/
  pegelonline_core/                          # shared acquisition + state helpers
    pegelonline_core/__init__.py             # exposes PegelOnlineAPI, FEED_URL_ROOT, load_state, save_state
    pyproject.toml

  pegelonline_kafka/                         # Kafka entrypoint
    pegelonline_kafka/app.py
    pyproject.toml

  pegelonline_mqtt/                          # MQTT entrypoint
    pegelonline_mqtt/app.py
    pyproject.toml

  pegelonline_amqp/                          # AMQP 1.0 entrypoint  ◀── this skill
    pegelonline_amqp/__init__.py
    pegelonline_amqp/__main__.py
    pegelonline_amqp/app.py
    pyproject.toml

  pegelonline_producer/                      # generated, xrcg style=kafkaproducer
  pegelonline_mqtt_producer/                 # generated, xrcg style=mqttclient
  pegelonline_amqp_producer/                 # generated, xrcg style=amqpproducer + azure_cbs_target

  Dockerfile.kafka
  Dockerfile.mqtt
  Dockerfile.amqp                            # ◀── this skill

  xreg/pegelonline.xreg.json                 # one manifest, three endpoints + three messagegroups
  generate_producer.ps1                      # three xrcg generate calls

  azure-template.json                        # Kafka/Event Hubs ACI
  azure-template-with-eventgrid-mqtt.json    # MQTT/Event Grid ACI
  azure-template-with-servicebus.json        # ◀── this skill: Service Bus ACI
```

## xRegistry Contract

The AMQP transport gets its own **endpoint** and **messagegroup** in the
same xreg manifest. Like MQTT, it uses `basemessageurl` to inherit the
payload schemas from the base messagegroup, so all transports speak the
same data shape:

```jsonc
{
  "endpoints": {
    "de.wsv.pegelonline.Amqp": {
      "usage": "producer",
      "protocol": "AMQP/1.0",
      "deployed": false,
      "messagegroups": ["#/messagegroups/de.wsv.pegelonline.amqp"],
      "config": {
        "protocol": "AMQP/1.0",
        "endpoints": [{ "uri": "amqp://example.invalid:5672/pegelonline" }]
      },
      "protocoloptions": {
        "options": {
          "content_mode": "binary",
          "address": "pegelonline"
        }
      }
    }
  },
  "messagegroups": {
    "de.wsv.pegelonline.amqp": {
      "messages": {
        "de.wsv.pegelonline.amqp.Station": {
          "basemessageurl": "#/messagegroups/de.wsv.pegelonline/messages/de.wsv.pegelonline.Station",
          "protocoloptions": {
            "properties": {
              "subject": {
                "type": "uritemplate",
                "value": "{station_id}",
                "description": "AMQP message subject — stable per-station identifier from PegelOnline."
              }
            },
            "application_properties": {
              "water_shortname": {
                "type": "string",
                "description": "Short name of the water body (e.g. 'rhein'). Lets brokers like Service Bus topics filter or route by water body without cracking the payload."
              }
            },
            "message_annotations": {
              "x-opt-partition-key": {
                "type": "uritemplate",
                "value": "{station_id}",
                "description": "Service Bus / Event Hubs partition key. UTF-8 string, max 128 characters. Mirrors the CloudEvent subject and the Kafka key so all events for the same station hash to the same partition and ordering is preserved end-to-end across transports."
              }
            }
          }
        }
      }
    }
  }
}
```

### Address vs. subject

Unlike MQTT (one topic template per message), AMQP 1.0 has one
**address** per producer link — the queue or topic name. Routing
within that address is done via:

- The CloudEvent `subject` (mapped to AMQP `properties.subject`),
- AMQP `application_properties`, which subscribers and SQL filters can
  read, and
- AMQP `message-annotations`, which brokers consume for transport-level
  behavior (partition keys, session IDs, scheduled enqueue time, etc.).

For Service Bus topics with subscriptions, the natural pattern is **one
address per source**, with consumers using subscription SQL filters on
`application_properties` and the CE `type` attribute.

For Event Hubs, the address is the event hub name; there are no
sub-addresses or filters — consumers read the whole partition stream.

### Partition keys are required for Service Bus and Event Hubs

Every AMQP message group **must** declare a
`protocoloptions.message_annotations["x-opt-partition-key"]` entry
whose `uritemplate` value matches the CloudEvent subject and the
Kafka key. Source: the Microsoft Python SDKs treat this annotation as
the canonical partition-routing signal for both products.

**Event Hubs** (`azure-eventhub`,
`azure/eventhub/_constants.py:10`, `_pyamqp_transport.py:393`,
`_utils.py:116`): the sender writes the annotation
`b"x-opt-partition-key"` into the message annotations section; the
broker hashes it to pick a partition. Without it, the sender uses
round-robin and event ordering for the same logical entity is lost
across partitions.

**Service Bus** (`azure-servicebus`,
`azure/servicebus/_common/constants.py:119`,
`_common/message.py:331`, `_common/message.py:688`): same annotation
key `b"x-opt-partition-key"`; the broker uses it for partitioned
queues/topics. If `session_id` is also set, the two values **must be
equal** (`_common/message.py:329`).

Data type and constraints (verified against the SDK code):

| Field        | Value                                                                          |
|--------------|--------------------------------------------------------------------------------|
| Annotation   | `b"x-opt-partition-key"` (AMQP symbol)                                          |
| Value type   | UTF-8 string (`str` in Python; the EH SDK also accepts the symbol in bytes)     |
| Max length   | 128 characters (`MESSAGE_PROPERTY_MAX_LENGTH` in `azure/servicebus/_common/constants.py:140`) |
| Encoding     | AMQP `message-annotations` section, **not** `application_properties`            |
| SB constraint| If `session_id` is set, `partition_key` must equal it                           |

Choose the partition-key template from the same stable domain identity
that backs the CloudEvent subject and the Kafka key — never use mutable
names, descriptive labels, timestamps, or surrogate UUIDs. For
multi-part identities (`{agency_cd}/{site_no}`), keep the template
identical across all three (subject, Kafka key, partition key).

> **xrcg support status.** As of xrcg 0.10.6 the Python AMQP producer
> template reads `properties` and `application_properties` but does
> **not** yet emit `message_annotations`. Tracked in
> [xregistry/codegen#294](https://github.com/xregistry/codegen/issues/294).
> Until annotation codegen lands, bridges declare the annotation in the
> manifest (so the contract is authoritative and EVENTS.md / KQL
> generators see it) **and** apply it in the bridge as a thin
> post-build hook on the generated sender — see the *Partition Key
> Bridge Workaround* section in
> [`stream-bridge-implementation`](../stream-bridge-implementation/SKILL.md#partition-key-bridge-workaround-amqp--pending-xrcg-support).

## Producer Generation

Add a third `xrcg generate` invocation to `generate_producer.ps1`:

```powershell
xrcg generate `
    --style amqpproducer `
    --language py `
    --definitions xreg\<source>.xreg.json `
    --endpoint <source>.Amqp `
    --projectname <source>_amqp_producer `
    --template-args azure_cbs_target=servicebus `
    --output <source>_amqp_producer
```

Key flags:

| Flag | Effect |
|------|--------|
| `--style amqpproducer` | Selects the AMQP 1.0 producer template. |
| `--template-args azure_cbs_target=servicebus` | Wires in the AMQP CBS `put-token` flow with the Service Bus audience (`https://servicebus.azure.net/.default`). Use `eventhubs` to target Event Hubs (`https://eventhubs.azure.net/.default`). Omit for **generic-broker-only** builds. |
| `--template-args azure_cbs_audience=<scope>` | Override the audience (only when cross-targeting or in a sovereign cloud). |

**Same binary, two auth modes.** The generated producer class accepts
**both** `username`/`password` (SASL PLAIN, generic brokers) and
`credential` (Entra ID, Azure). They are mutually exclusive at runtime,
not at compile time. One image can be deployed against RabbitMQ in dev
and Service Bus in prod by toggling environment variables only.

## Runtime Bridge Patterns

The app skeleton mirrors the Kafka/MQTT siblings:

```python
from pegelonline_core import FEED_URL_ROOT, PegelOnlineAPI, load_state, save_state
from pegelonline_amqp_producer_data.de.wsv.pegelonline.station import Station
from pegelonline_amqp_producer_amqp_producer.producer import DeWsvPegelonlineAmqpProducer

if auth_mode == "entra":
    from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
    credential = (ManagedIdentityCredential(client_id=entra_client_id)
                  if entra_client_id else DefaultAzureCredential())
    producer = DeWsvPegelonlineAmqpProducer(
        host="ns.servicebus.windows.net", address="pegelonline",
        credential=credential,
        entra_audience="https://servicebus.azure.net/.default",
        use_tls=True,
    )
else:
    producer = DeWsvPegelonlineAmqpProducer(
        host=host, address=address, port=port,
        username=username, password=password,
        use_tls=tls,
    )

producer.send_station(data=_build_station(s),
                      _feedurl=f"{FEED_URL_ROOT}/stations/{s['shortname']}",
                      _station_id=s["uuid"])
```

Subject and source placeholders are passed **explicitly** as kwargs
(`_feedurl`, `_station_id`), exactly as the generated method signature
declares them. Do not hide them in an ad-hoc key/subject mapper.

### Auth mode CLI/env contract

| Flag | Env var | Purpose |
|------|---------|---------|
| `--broker-url` | `AMQP_BROKER_URL` | Convenience URL (`amqp://user:pwd@host:port/address`) — splits into host/port/tls/user/pwd/address. |
| `--host` | `AMQP_HOST` | Broker hostname (alternative to `--broker-url`). |
| `--port` | `AMQP_PORT` | Defaults to 5672, or 5671 when `--tls` is set. |
| `--address` | `AMQP_ADDRESS` | Queue/topic name. Default: source name. |
| `--tls` | `AMQP_TLS` | Force `amqps://`. Auto-enabled when `auth-mode=entra`. |
| `--username` / `--password` | `AMQP_USERNAME` / `AMQP_PASSWORD` | SASL PLAIN credentials. |
| `--auth-mode {password,entra}` | `AMQP_AUTH_MODE` | Auth strategy. Default: `password`. |
| `--entra-audience` | `AMQP_ENTRA_AUDIENCE` | AAD scope. Default: `https://servicebus.azure.net/.default`. Use `https://eventhubs.azure.net/.default` for Event Hubs. |
| `--entra-client-id` | `AMQP_ENTRA_CLIENT_ID` | Optional user-assigned MI client id. |
| `--content-mode {binary,structured}` | `AMQP_CONTENT_MODE` | CloudEvents content mode. Default: `binary` (CE attributes → AMQP message properties). |
| `-i` / `--polling-interval` | `POLLING_INTERVAL` | Seconds between upstream polls. |
| `--state-file` | `STATE_FILE` | Dedupe state JSON path. |
| `--once` | `ONCE_MODE` | Exit after one cycle (useful for Docker E2E and validation). |

### Token refresh — do nothing

Unlike the MQTT Entra path, the AMQP bridge **does not run its own
refresh loop**. The generated `_CbsAzureHandler` owns the proton
reactor, the CBS link, and the connection. The runtime concern reduces
to: pass a `TokenCredential` once, then call `send_*`. CBS token expiry
and renewal happen inside the handler.

(Background-refresh details vary by xrcg release; if the producer's
`__init__` documents a "no automatic refresh" caveat, the bridge can
rely on container-orchestrator restarts. For pegelonline-class cadences
— minutes per poll — token lifetime is irrelevant.)

## Dockerfile.amqp

Boilerplate parallel to `Dockerfile.mqtt`:

```Dockerfile
FROM python:3.10-slim

LABEL org.opencontainers.image.source="..."
LABEL org.opencontainers.image.title="<Source> → AMQP 1.0 bridge"
LABEL org.opencontainers.image.documentation="...CONTAINER.md"
LABEL org.opencontainers.image.license="MIT"

ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY . /app

# Sequential, to avoid Poetry path-dep resolution races.
RUN pip install --no-cache-dir ./<source>_amqp_producer/<source>_amqp_producer_data \
 && pip install --no-cache-dir ./<source>_amqp_producer/<source>_amqp_producer_amqp_producer \
 && pip install --no-cache-dir ./<source>_core \
 && pip install --no-cache-dir ./<source>_amqp

ENV AMQP_BROKER_URL=""
ENV AMQP_ADDRESS="<source>"

CMD ["python", "-m", "<source>_amqp", "feed"]
```

Linux containers use the OpenSSL-linked `python-qpid-proton` wheels from
PyPI and have no TLS 1.3 issues. The Windows wheel index
(`https://xregistry.github.io/codegen/wheels/simple/`) applies only to
local dev on Windows; container builds do not need it.

## Azure Template

`azure-template-with-servicebus.json` provisions, in one ARM pass:

1. A **Service Bus namespace** (Standard SKU for queues, Premium if the
   workload needs topics with SQL filters at scale).
2. A **queue** named after the source (`pegelonline`, `usgs-iv`, etc.),
   or one **topic** + subscriptions when the consumer side already
   wants filtered subscriptions.
3. An **ACI** with a **user-assigned managed identity**.
4. An **RBAC role assignment** of `Azure Service Bus Data Sender` to
   the MI, scoped to the queue or topic. Use
   `extensionResourceId(...)` in `dependsOn` to ensure provisioning
   order.

Environment variables passed to the ACI:

```jsonc
{
  "AMQP_HOST":            "<namespace>.servicebus.windows.net",
  "AMQP_ADDRESS":         "[parameters('queueName')]",
  "AMQP_AUTH_MODE":       "entra",
  "AMQP_ENTRA_AUDIENCE":  "https://servicebus.azure.net/.default",
  "AMQP_ENTRA_CLIENT_ID": "<managed-identity-clientId>",
  "AMQP_TLS":             "true",
  "POLLING_INTERVAL":     "60"
}
```

**Do not** include `imageRegistryServer` / `imageRegistryUsername` /
`imageRegistryPassword` parameters — images are pulled from the public
GHCR registry built by this repo's CI. (Same lesson learned in the MQTT
template — keep the parameter surface minimal.)

The ghpages portal gets a fourth button on the source's page wired to
the new template.

## Event Hubs Variant

If the target is Event Hubs instead of Service Bus, the only delta is:

- `AMQP_ENTRA_AUDIENCE = https://eventhubs.azure.net/.default`
- `AMQP_HOST = <namespace>.servicebus.windows.net` (yes, same suffix)
- `AMQP_ADDRESS = <eventhub_name>`
- RBAC role: `Azure Event Hubs Data Sender`

The same Docker image works against both — only environment changes.
Provide a separate `azure-template-with-eventhubs.json` only if the
consumer-side topology differs materially (capture enabled, schema
registry attached, partitions ≠ 1).

## CI Matrix

Add a build entry to `tests/docker_e2e/matrix.json`:

```json
{ "dir": "pegelonline", "image": "pegelonline-amqp", "file": "Dockerfile.amqp", "module": "pegelonline_amqp" }
```

The Docker E2E **flow** test for AMQP needs an in-test broker. Two
options:

- **ActiveMQ Artemis** — spin up `apache/activemq-artemis:latest` next
  to the bridge container, use the default `artemis`/`artemis` SASL
  PLAIN credentials, and consume via a proton client in the test
  harness. This is the recommended path: closest to the Service Bus
  message shape, supports queues and topics, ships AMQP 1.0 by default.
- **RabbitMQ + AMQP 1.0 plugin** — works but the plugin is a separate
  install step.

Without an E2E flow test, the matrix still builds the image as part of
the standard CI build matrix. Add the flow test as a follow-up.

## Documentation

- `CONTAINER.md` — add a top-level section "AMQP 1.0 variant" with env
  vars and example `docker run` commands for both Service Bus and a
  generic broker.
- `EVENTS.md` — regenerate so it lists the new AMQP messagegroup.
- `README.md` — add a "Transports" section linking the three
  Dockerfiles and the three ARM templates.
- Root `README.md` — annotate the source's row with an AMQP badge.

## Common Pitfalls

- **Don't add SAS-key minting code to the bridge.** The whole point of
  `azure_cbs_target` is to avoid it. If you find yourself writing
  `hmac.new(...)` to build a SAS token, stop — the `credential` path is
  already wired.
- **Don't use `pyamqp` or the Azure Service Bus SDK** as the producer
  runtime when xrcg has already generated a proton-based producer. Two
  AMQP stacks in one process are a hard-debug session waiting to happen.
- **Don't share an address across sources.** One AMQP address per
  source folder — exactly the same rule as Kafka topics.
- **Don't omit `use_tls=True`** for Azure. The producer auto-flips port
  5672 → 5671 when `credential` is set, but the TLS context is gated by
  `use_tls`.
- **Don't try to publish from multiple processes against a
  session-enabled Service Bus queue without setting per-message
  `sessionId`.** AMQP 1.0 has no native session concept; if the queue
  has sessions enabled, set
  `application_properties["x-opt-session-id"]` (Service Bus
  convention). For pegelonline-class ingestion, leave sessions off.
- **Don't ship a Windows-only path for the wheel index in the
  container.** The TLS 1.3 fix is for local Windows dev only. Linux
  containers use PyPI's stock `python-qpid-proton` wheel.

## Reference Implementation

| File | Purpose |
|------|---------|
| `pegelonline/xreg/pegelonline.xreg.json` | `de.wsv.pegelonline.Amqp` endpoint + `de.wsv.pegelonline.amqp` messagegroup |
| `pegelonline/generate_producer.ps1` | Three `xrcg generate` calls (kafka, mqtt, amqp) |
| `pegelonline/pegelonline_amqp/` | The AMQP entrypoint application |
| `pegelonline/Dockerfile.amqp` | Container image |
| `pegelonline/azure-template-with-servicebus.json` | One-click Service Bus ACI deployment |
| `tests/docker_e2e/matrix.json` | CI build entry `pegelonline-amqp` |
