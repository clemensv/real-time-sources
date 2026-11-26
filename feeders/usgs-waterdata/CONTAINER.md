# USGS Water Data containers: Kafka, MQTT and AMQP

[Overview](README.md) · [Event schemas](EVENTS.md) · [KQL schema](kql/usgs-waterdata.kql)

## Upstream

- API and documentation: <https://api.waterdata.usgs.gov/ogcapi/v1>
- Provider: U.S. Geological Survey; see [licence and data caveats](README.md#documentation-licence-and-rate-limits).

## Why this container

Flood-warning teams and water operators need current conditions and enough
metadata to interpret a reading. These images publish continuous USGS
observations together with location, parameter and series references.
They retain exact observation value strings, separate provisional approval
from sensor qualifiers, and emit changed observations after confirmed delivery.
The default query is runnable without a private upstream credential.

## What ships in the box

| Image | Transport | Default behavior |
|---|---|---|
| `ghcr.io/clemensv/real-time-sources-usgs-waterdata:latest` | Kafka | Structured JSON CloudEvents; topic `usgs-waterdata`, key `{time_series_id}` |
| `ghcr.io/clemensv/real-time-sources-usgs-waterdata-mqtt:latest` | MQTT 5 | Binary CloudEvents, QoS 1; retained references and non-retained observations |
| `ghcr.io/clemensv/real-time-sources-usgs-waterdata-amqp:latest` | AMQP 1.0 | Binary CloudEvents, address `usgs-waterdata`, native series partition identity |

## Database schemas and handling

[Generated KQL](kql/usgs-waterdata.kql) defines dispatch ingestion and typed
tables for non-schematized consumers. For schematized Fabric ingestion,
register the event schemas and use Eventstream-managed typed tables.
KQL stores `data_gap_interval` as its original ISO-8601 string rather than
a Kusto timespan; calendar durations cannot be reduced to fixed seconds.
Kusto datetime columns are UTC analytical values with 100-nanosecond
resolution. They normalize source offsets and cannot preserve timestamp
spelling or precision finer than seven fractional digits. Native JSON
events preserve the original RFC3339 text; retain those events when the
original spelling matters. Threshold arrays remain dynamic rather than being flattened into datetime
columns. Dynamic JSON also converts timestamp-looking strings: offsets become
UTC, fractional digits are padded to seven, and timezone-free metadata is
interpreted as UTC by Kusto. That interpretation does not establish the
upstream timezone. Keep the original custom-output events when timestamp
spelling or timezone-free metadata must be preserved.
The upstream threshold schema mismatch remains in the migration backlog.
Qualifier coverage is incomplete, and no authoritative legacy TS_ID crosswalk
is available. Native series identities are not inferred from legacy IDs.
See [scope and interpretation](README.md#upstream-scope-and-interpretation).
See [database integration](../../DATABASE.md).

## Image contract

| Tag | Dockerfile | Entry point | State share |
|---|---|---|---|
| `:latest` | `Dockerfile` | `python -m usgs_waterdata feed` | Local volume or managed-identity HTTPS |
| `-mqtt:latest` | `Dockerfile.mqtt` | `python -m usgs_waterdata_mqtt feed` | Local volume or managed-identity HTTPS |
| `-amqp:latest` | `Dockerfile.amqp` | `python -m usgs_waterdata_amqp feed` | Local volume or managed-identity HTTPS |

All variants use Python 3.10 slim, run as UID 10001, expose no inbound ports,
and have no HTTP health endpoint. `/state` is writable in the image.
On SIGTERM the process cancels polling and flushes/closes its transport;
an interrupted batch remains eligible after restart. Each process owns
exactly one transport. Use separate state files for different destinations.
State keeps one scientific-content fingerprint per delivered observation
instant; it grows with the monitored history and is not automatically pruned.

```powershell
docker pull ghcr.io/clemensv/real-time-sources-usgs-waterdata:latest
docker pull ghcr.io/clemensv/real-time-sources-usgs-waterdata-mqtt:latest
docker pull ghcr.io/clemensv/real-time-sources-usgs-waterdata-amqp:latest
```

## Configuration shared by all transports

| Variable | Default | Description |
|---|---|---|
| `USGS_WATERDATA_SITES` | `USGS-01646500` | Comma-separated monitoring-location IDs; numeric USGS site numbers are prefixed with `USGS-`. |
| `USGS_WATERDATA_PARAMETERS` | `00010,00060` | Five-digit parameter codes; empty selects all continuous parameters at the sites. |
| `USGS_WATERDATA_LOOKBACK_HOURS` | `2` | Recent observation-time window. First run starts here; subsequent runs also query corrections without an observation-time limit. |
| `USGS_WATERDATA_REFERENCE_INTERVAL` | `86400` | Seconds between acknowledged full reference refreshes. The series endpoint updates at most daily. |
| `USGS_WATERDATA_OVERLAP_SECONDS` | `300` | Overlap on incremental `last_modified` correction windows. |
| `USGS_API_KEY` | unset | Optional USGS API gateway key, sent only to the allowed API host. Secret. |
| `USER_AGENT` | `real-time-sources-usgs-waterdata/0.1.0` | HTTP User-Agent; supply an operations contact when appropriate. |
| `POLLING_INTERVAL` | `300` | Seconds between cycles; must be positive. |
| `STATE_FILE` | unset | Atomic delivery checkpoint path; unset means memory only. Do not share across concurrent writers/destinations. |
| `STATE_BACKEND` | `local` | `azure-files-rest` uses the dedicated state identity over HTTPS. See [backend bindings](../../tools/aci_files_identity.md#runtime-configuration-and-persistence). No storage key fallback. |
| `ONCE_MODE` | `false` | One cycle then exit; any failed site causes a visible nonzero exit. |
| `LOG_LEVEL` | `INFO` | Python logging level; broker secrets are never logged. |

Reference data is sent before observations for every native time series.
Transient reference-refresh failures retain the previous acknowledged catalog.
Failed site slices retain their correction cursor while other sites continue.
Kafka state requires every delivery callback to succeed and flush remainder
zero. MQTT state requires QoS-1 acknowledgements. AMQP sends require remote
accepted settlement.
Password links explicitly select SASL PLAIN and pass the decoded username
and password to Proton. Insecure SASL mechanisms are allowed only when
the effective TLS setting is false (`AMQP_USE_TLS` takes precedence over
`AMQP_TLS`, or an explicit `amqp://` URL selects the default).
TLS links keep Proton's insecure-mechanism allowance disabled. The AMQP
image includes the Cyrus SASL PLAIN module; Entra/SAS CBS paths are unchanged.

## Kafka variant

| Variable | Default | Description |
|---|---|---|
| `CONNECTION_STRING` | unset | `BootstrapServer=host:port;EntityPath=topic` or Event Hubs connection string. EntityPath overrides `KAFKA_TOPIC`. Secret for SAS formats. |
| `KAFKA_BOOTSTRAP_SERVERS` | `localhost:9092` | Bootstrap servers when no connection string is supplied. |
| `KAFKA_TOPIC` | `usgs-waterdata` | Topic without a connection-string EntityPath. |
| `KAFKA_ENABLE_TLS` | `true` | Use TLS for direct bootstrap configuration; cloud connection strings select their required protocol. |
| `SASL_USERNAME` | unset | SASL username; must be paired with `SASL_PASSWORD`. |
| `SASL_PASSWORD` | unset | SASL password for the explicit broker username; required with `SASL_USERNAME` and supplied as a secret. |
| `SASL_MECHANISM` | `PLAIN` | SASL mechanism for explicit credentials. |
| `KAFKA_AUTH_MODE` | unset | `azure-entra` uses an explicit managed identity for Event Hubs Kafka; `fabric-entra` uses NotebookUtils namespace-audience tokens in notebooks. Both require TLS and one namespace on port 9093, refresh tokens and reject passwords. Unset preserves existing broker authentication. |
| `KAFKA_ENTRA_CLIENT_ID` | required with `azure-entra` | User-assigned managed identity client ID. The Event Hubs template grants this identity Data Sender and disables broker local authentication; there is no key fallback. |

```powershell
docker run --rm -v "${PWD}\state:/state" -e STATE_FILE=/state/native-kafka.json -e KAFKA_BOOTSTRAP_SERVERS=kafka.example:9093 -e SASL_USERNAME=publisher -e SASL_PASSWORD="<password>" ghcr.io/clemensv/real-time-sources-usgs-waterdata:latest
docker run --rm -v "${PWD}\state:/state" -e STATE_FILE=/state/native-eventhub.json -e KAFKA_BOOTSTRAP_SERVERS="<namespace>.servicebus.windows.net:9093" -e KAFKA_TOPIC="<hub>" -e KAFKA_AUTH_MODE=azure-entra -e KAFKA_ENTRA_CLIENT_ID="<assigned-identity-client-id>" ghcr.io/clemensv/real-time-sources-usgs-waterdata:latest
```

The managed-identity example requires an Azure host with the selected identity
assigned and its identity endpoint reachable from the container.

## MQTT 5 variant

| Variable | Default | Description |
|---|---|---|
| `MQTT_BROKER_URL` | required | Broker `host:port` or URI; single broker-host configuration. |
| `MQTT_ENABLE_TLS` | `true`, or `false` for explicit `mqtt://` URI | TLS; defaults port to 8883, otherwise 1883. Required for Entra/certificate authentication. |
| `MQTT_AUTH_MODE` | `anonymous` | `anonymous`, `userpass` (`password` alias), `tls-cert`, or `entra`. |
| `MQTT_USERNAME` | unset | Required with userpass; optional client resource username with Entra. |
| `MQTT_PASSWORD` | unset | Required with userpass. Secret. |
| `MQTT_CLIENT_ID` | `usgs-waterdata` | Unique client ID per concurrent publisher. |
| `MQTT_CLIENT_CERT` | unset | PEM client certificate path for tls-cert mode. |
| `MQTT_CLIENT_KEY` | unset | PEM private-key path for tls-cert mode. |
| `MQTT_CA_FILE` | system trust | Optional broker CA bundle. TLS verification remains enabled. |
| `MQTT_ENTRA_CLIENT_ID` | unset | User-assigned managed identity client ID; otherwise DefaultAzureCredential. |
| `MQTT_ENTRA_AUDIENCE` | `https://eventgrid.azure.net/` | Entra resource audience. Tokens refresh before expiry with enhanced-auth reconnect. |

Topic prefix, QoS and retain are contract-defined rather than runtime
overrides: `hydro/us/usgs/waterdata/{time_series_id}/`, QoS 1, retained reference
leaves, non-retained observations. MQTT 5 binary CloudEvents carry the bare
context attribute names in user properties, per the MQTT binding.

```powershell
docker run --rm -e MQTT_BROKER_URL=mqtt.example:8883 -e MQTT_AUTH_MODE=userpass -e MQTT_USERNAME=publisher -e MQTT_PASSWORD="<password>" ghcr.io/clemensv/real-time-sources-usgs-waterdata-mqtt:latest
docker run --rm -e MQTT_BROKER_URL="<namespace-hostname>:8883" -e MQTT_AUTH_MODE=entra -e MQTT_ENTRA_CLIENT_ID="<managed-identity-client-id>" ghcr.io/clemensv/real-time-sources-usgs-waterdata-mqtt:latest
docker run --rm -v "${PWD}\certs:/certs:ro" -e MQTT_BROKER_URL=mqtt.example:8883 -e MQTT_AUTH_MODE=tls-cert -e MQTT_CLIENT_CERT=/certs/client.crt -e MQTT_CLIENT_KEY=/certs/client.key -e MQTT_CA_FILE=/certs/ca.crt ghcr.io/clemensv/real-time-sources-usgs-waterdata-mqtt:latest
```

## AMQP 1.0 variant

| Variable | Default | Description |
|---|---|---|
| `AMQP_BROKER_URL` | unset | Optional broker URI; host, port, address and URL-encoded credentials override individual values. |
| `AMQP_HOST` | `localhost` | AMQP hostname when no URL hostname is supplied. |
| `AMQP_PORT` | `5671` with TLS, otherwise `5672` | AMQP broker port. |
| `AMQP_ADDRESS` | `usgs-waterdata` | Queue/topic address; never a shared legacy-source address. |
| `AMQP_TLS` | `true`, or `false` for explicit `amqp://` URI | TLS; required with Entra, disabled for local Artemis/emulator examples. |
| `AMQP_USE_TLS` | unset | Explicit TLS override, including generated SAS CBS connections; takes precedence over `AMQP_TLS`. Set `false` only for an intentional plaintext broker/emulator. Entra rejects `false`. |
| `AMQP_AUTH_MODE` | `password` | `password` (SASL PLAIN), `entra` (CBS), or `sas` (CBS). |
| `AMQP_USERNAME` | unset | SASL PLAIN username in password mode. |
| `AMQP_PASSWORD` | unset | SASL PLAIN password. Secret. |
| `AMQP_CONTENT_MODE` | `binary` | Binary CloudEvents by default; `structured` also supported. |
| `AMQP_ENTRA_CLIENT_ID` | unset | User-assigned managed identity client ID; otherwise DefaultAzureCredential. |
| `AMQP_ENTRA_AUDIENCE` | `https://servicebus.azure.net/.default` | CBS token audience; Event Hubs uses `https://eventhubs.azure.net/.default`. |
| `AMQP_SAS_KEY_NAME` | required in sas mode | Existing SAS policy/key name passed to the generated CBS provider. |
| `AMQP_SAS_KEY` | required in sas mode | Existing SAS key passed to generated code. Secret; no bridge-side token minting. |

```powershell
docker run --rm -e AMQP_HOST=artemis -e AMQP_PORT=5672 -e AMQP_TLS=false -e AMQP_USERNAME=artemis -e AMQP_PASSWORD=artemis ghcr.io/clemensv/real-time-sources-usgs-waterdata-amqp:latest
docker run --rm -e AMQP_HOST="<namespace>.servicebus.windows.net" -e AMQP_ADDRESS=usgs-waterdata -e AMQP_AUTH_MODE=entra -e AMQP_ENTRA_CLIENT_ID="<managed-identity-client-id>" ghcr.io/clemensv/real-time-sources-usgs-waterdata-amqp:latest
docker run --rm -e AMQP_HOST=servicebus-emulator -e AMQP_PORT=5672 -e AMQP_USE_TLS=false -e AMQP_AUTH_MODE=sas -e AMQP_SAS_KEY_NAME=RootManageSharedAccessKey -e AMQP_SAS_KEY="<emulator-key>" ghcr.io/clemensv/real-time-sources-usgs-waterdata-amqp:latest
```

## Deployment

### Microsoft Fabric

> Plain-Python Kafka publication has been verified with namespace-scoped
> Entra tokens. The principal was a delegated user, not workspace managed
> identity. Verify scheduling and the actual target principal separately.

[Deploy notebook](https://clemensv.github.io/real-time-sources#usgs-waterdata/fabric-notebook)
or [container](https://clemensv.github.io/real-time-sources#usgs-waterdata/fabric-aci).
The notebook uses the same Kafka bridge, a OneLake wheel bundle, OneLake
state/logs and a worker thread. Connection lookup stays in the canonical
Topology API cell. Do not paste a connection string into notebook parameters.
The notebook uses the canonical pure-Python kernel without an Environment
binding. It requires exactly one wheel each for the bridge, shared core and
both Kafka producer packages. The shared deployer uploads them under
`/lakehouse/default/Files/wheels/usgs-waterdata/`; the run cell installs them
and their public dependencies before connection lookup. Installation requires
access to the configured Python package index and fails explicitly on error.
Each install has a 300-second timeout. The OneLake log records active package
versions. Verify the wheel bundle and Lakehouse binding in a fresh scheduled
run. The public connection response bundles access keys, but the notebook
immediately discards them. Namespace and entity metadata form a credentialless
binding; refreshed NotebookUtils tokens authenticate Kafka through OAUTHBEARER.
The token audience is the service-issued namespace URI, not the global Event
Hubs resource. No access-key fallback is implemented.
For a scoped run, set notebook parameters `USGS_WATERDATA_SITES` to
`USGS-01646500` and `USGS_WATERDATA_PARAMETERS` to `00010,00060`.
The run cell writes these values into their same-named environment variables,
so notebook parameters take precedence over deployer `EnvVar` settings.
It likewise sets `STATE_FILE`, `POLLING_INTERVAL` and `ONCE_MODE`; the latter
must remain `True`. `RUN_DURATION` bounds the worker join and defaults to 900
seconds. `STATE_BACKEND=local` keeps the OneLake checkpoint independent of
ACI REST bindings. `EVENTSTREAM_NAME`, `EVENTSTREAM_SOURCE_NAME` and
`WORKSPACE_ID` select the exact named public-Topology-API endpoint.

### Azure

All six templates configure delivery state through Azure Files HTTPS with
`allowSharedKeyAccess=false`. A dedicated user-assigned state identity receives
**Storage File Data Privileged Contributor** on the
dedicated storage account; broker identities and permissions remain unchanged.
OAuth backup intent bypasses file ACLs. Do not store unrelated data there.
ACI supplies the explicit state identity without a storage key or host SMB
mount. See the [shared template contract](../../tools/aci_files_identity.md)
for bindings, atomic writes, single-writer semantics and old-role removal.

[Kafka BYO](azure-template.json) deploys ACI against an existing connection;
[Kafka + Event Hubs](azure-template-with-eventhub.json) adds a namespace.
[MQTT BYO](azure-template-mqtt.json) deploys the MQTT container;
[MQTT + Event Grid](azure-template-with-eventgrid-mqtt.json) provisions a
namespace/topic space plus managed identity and topic-space publisher role.
[AMQP default](azure-template-amqp.json) is a canonical alias of the
Service Bus provisioning template, not a bring-your-own-broker template;
[AMQP + Service Bus](azure-template-with-servicebus.json) provisions a namespace,
queue, managed identity and sender role. Service Bus sessions are not enabled.
All six templates provision an Azure Files share and preserve the logical
`STATE_FILE` path `/mnt/bridge-state/usgs-waterdata.json`. The runtime derives
the same share-relative file name; `/mnt/bridge-state` is not mounted.
Run `pwsh feeders\usgs-waterdata\generate-template.ps1` from the repository root
to regenerate them, including the shared managed-identity transformation.
The shared core includes Azure Identity and Azure Files SDK dependencies.

All templates expose the shared source controls and generic `STATE_FILE`,
`USER_AGENT`, `ONCE_MODE`, `LOG_LEVEL` and `POLLING_INTERVAL` parameters.
For long-running ACI deployment leave `onceMode=false`.

Kafka BYO accepts either `connectionString` or direct `kafkaBootstrapServers`,
`kafkaTopic`, `kafkaEnableTls` and `saslUsername`/`saslPassword`/
`saslMechanism` settings. Leave `connectionString` empty for direct settings.
The provision-new Event Hubs template disables local authentication and supplies
its namespace endpoint, hub name and a dedicated Kafka publisher identity.
That identity has namespace-scoped Azure Event Hubs Data Sender, separate from
the state identity. The OAuth callback refreshes Event Hubs tokens; no broker
key or password fallback is configured. Separate bootstrap/SASL controls are not
applicable there.

MQTT BYO infers `userpass` when `brokerUsername` is supplied and `anonymous`
otherwise; `mqttAuthMode` can select an explicit mode. `mqttEnableTls` defaults
to `true`; set it to `false` only for an intentionally unencrypted broker.
Certificate-mode paths (`mqttCaFile`, `mqttClientCert`, `mqttClientKey`) must
refer to separately supplied local readable files. HTTPS checkpoints do not
mount a certificate directory, and the template does not upload certificates.
The Event Grid template supplies the managed identity, client ID, TLS broker
endpoint and Entra audience. Alternate password/certificate modes are not
applicable to that provisioned target.

Both Service Bus templates fix AMQP host/address, TLS, binary content mode
and Entra credentials to their provisioned queue and managed identity.
They expose no separate `AMQP_USE_TLS` override because TLS is required
for that target; the override is available for direct Docker deployment.
Generic SASL-PLAIN and emulator SAS deployments use the Docker examples
above; those modes are not alternate authentication settings for these
provision-new Service Bus templates.

[Deploy Kafka BYO](https://clemensv.github.io/real-time-sources#usgs-waterdata/azure-byoeh) ·
[Deploy Event Hubs](https://clemensv.github.io/real-time-sources#usgs-waterdata/azure) ·
[Deploy MQTT](https://clemensv.github.io/real-time-sources#usgs-waterdata/azure-mqtt) ·
[Deploy Event Grid MQTT](https://clemensv.github.io/real-time-sources#usgs-waterdata/azure-mqtt-eg) ·
[Deploy Service Bus](https://clemensv.github.io/real-time-sources#usgs-waterdata/azure-amqp-sb)
