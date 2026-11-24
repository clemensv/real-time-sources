# USGS Water Data

United States — native continuous water observations · Kafka · MQTT 5 · AMQP 1.0

[Container deployment](CONTAINER.md) · [Event schemas](EVENTS.md) ·
[KQL schema](kql/usgs-waterdata.kql) · [Upstream API](https://api.waterdata.usgs.gov/ogcapi/v1)

## At a glance

Flood-warning teams, water utilities and environmental analysts use river
discharge, water level and continuous water-quality observations to assess
conditions and investigate changes. This feeder publishes USGS observations
with their monitoring-location, time-series and parameter metadata. Consumers
can interpret units, provisional status, sensor qualifiers and threshold
history without maintaining separate reference-data polling jobs.

| Aspect | Contract |
|---|---|
| Region / authority | United States / U.S. Geological Survey |
| Acquisition | Public USGS Water Data OGC API, paginated HTTPS |
| Default selection | `USGS-01646500`; parameters `00010,00060` |
| Cadence | Poll every 300 seconds; two-hour recent window; daily reference refresh |
| Identity | Native opaque `time_series_id`; never legacy NWIS numeric TS_ID |
| Types | `USGS.WaterData.ContinuousObservation`, `.MonitoringLocation`, `.TimeSeries`, `.Parameter` |
| Upstream authentication | Optional `USGS_API_KEY`; anonymous access also supported |

> This is a new native contract. It does not replace the identity, types or
> topics of [usgs-iv](../usgs-iv/README.md) or
> [usgs-nwis-wq](../usgs-nwis-wq/README.md).

## 60-second quick start

```powershell
docker run --rm -e CONNECTION_STRING="BootstrapServer=broker:9092;EntityPath=usgs-waterdata" -e KAFKA_ENABLE_TLS=false -e ONCE_MODE=true ghcr.io/clemensv/real-time-sources-usgs-waterdata:latest
docker run --rm -e MQTT_BROKER_URL=broker:1883 -e MQTT_ENABLE_TLS=false -e ONCE_MODE=true ghcr.io/clemensv/real-time-sources-usgs-waterdata-mqtt:latest
docker run --rm -e AMQP_HOST=broker -e AMQP_PORT=5672 -e AMQP_TLS=false -e AMQP_USERNAME=artemis -e AMQP_PASSWORD=artemis -e ONCE_MODE=true ghcr.io/clemensv/real-time-sources-usgs-waterdata-amqp:latest
```

Set `USGS_WATERDATA_SITES` and `USGS_WATERDATA_PARAMETERS` for the deployment
scope. Mount a writable state volume and set `STATE_FILE` for repeated runs.
The complete configuration reference is [CONTAINER.md](CONTAINER.md).

## Architecture

Every process publishes to exactly one transport. A shared native poller uses
`usgs_waterdata_core.WaterDataClient` for bounded HTTP retries and complete
pagination. It publishes three reference types before observations for each
series. Monitoring-location and parameter resources are attached to the series
that references them; the original resource IDs remain in their nested objects.

Each successful poll combines a recent observation-time window with a
`last_modified` window after the previous acknowledged checkpoint. The latter
has **no observation-time limit**, so older corrections remain eligible.
Scientific-content fingerprints distinguish corrections from database-only
refreshes. State advances after successful broker acknowledgements, not enqueue.
Failed sites retain their checkpoints while unaffected sites can complete.
An unsuccessful reference refresh keeps the last acknowledged catalog.

### Transports

| Image suffix | Application | Delivery shape / use |
|---|---|---|
| `:latest` | `usgs_waterdata` | Structured JSON CloudEvents on Kafka; replayable history; key `{time_series_id}` |
| `-mqtt:latest` | `usgs_waterdata_mqtt` | Binary MQTT 5 CloudEvents; retained QoS-1 reference leaves, non-retained observations |
| `-amqp:latest` | `usgs_waterdata_amqp` | Binary AMQP 1.0 CloudEvents; queue/topic consumers, native series partition identity |

MQTT topics are `hydro/us/usgs/waterdata/{time_series_id}/` followed by
`monitoring-location`, `parameter`, `time-series` or `observation`. Subscribe
to `hydro/us/usgs/waterdata/+/observation` for telemetry.
Observations are not retained: an old corrected observation must not overwrite
a latest-value retained slot.
The handwritten AMQP adapter requires remote acceptance and honors TLS on
SASL-PLAIN links. It compensates for
[codegen#699](https://github.com/xregistry/codegen/issues/699) without
editing generated producers.

## Deployment

### Microsoft Fabric

> The notebook uses the shared plain-Python hosting path. Live manual and
> scheduled acceptance remains required. Workspace-identity Kafka publication
> has not been verified; access-key fallback stays disabled pending explicit
> identity approval.

- [Fabric notebook](https://clemensv.github.io/real-time-sources#usgs-waterdata/fabric-notebook):
  runs the same Kafka bridge in a worker thread with OneLake state and logs.
  The shared deployer uploads its wheel bundle to OneLake. The notebook installs
  those wheels and public dependencies without a Fabric Environment binding.
  Missing or ambiguous source wheels and installation failures fail the run
  and are recorded in the OneLake log. Verify the Lakehouse binding, active
  package versions and a fresh scheduled run before production use.
  The generated Kafka source connection requires access keys, so the notebook
  fails closed unless an operator explicitly approves that fallback after
  identity review. It does not expose broker secrets as parameters.
- [Fabric container](https://clemensv.github.io/real-time-sources#usgs-waterdata/fabric-aci):
  an independently hosted Kafka container publishes to an Eventstream.
- [Generated KQL](kql/usgs-waterdata.kql) supports non-schematized structured
  CloudEvents ingestion. Schematized Fabric pipelines must use registered
  event schemas and Eventstream-managed tables instead of dispatch DDL.

### Azure

> These ACI templates use account-key-backed Azure Files mounts for delivery
> checkpoints. Deployment is blocked in subscriptions whose storage policy
> denies Shared Key access. Disabling Shared Key while retaining the mount
> does not fix that dependency. An approved state-storage design is required;
> removing persistent dedupe or weakening policy is not a supported workaround.

| Template | Provisioned resources |
|---|---|
| [Kafka BYO](azure-template.json) | ACI using an existing Kafka/Event Hubs connection |
| [Kafka + Event Hubs](azure-template-with-eventhub.json) | Event Hubs namespace and ACI |
| [MQTT BYO](azure-template-mqtt.json) | ACI connected to an existing MQTT broker |
| [MQTT + Event Grid](azure-template-with-eventgrid-mqtt.json) | MQTT-enabled namespace, topic space, managed identity, publisher role, ACI |
| [AMQP default](azure-template-amqp.json) | Canonical alias: provisions Service Bus, managed identity, sender role and ACI |
| [AMQP + Service Bus](azure-template-with-servicebus.json) | Namespace, queue, managed identity, sender role, ACI |

[Deploy Kafka BYO](https://clemensv.github.io/real-time-sources#usgs-waterdata/azure-byoeh) ·
[Deploy Event Hubs](https://clemensv.github.io/real-time-sources#usgs-waterdata/azure) ·
[Deploy MQTT](https://clemensv.github.io/real-time-sources#usgs-waterdata/azure-mqtt) ·
[Deploy Event Grid MQTT](https://clemensv.github.io/real-time-sources#usgs-waterdata/azure-mqtt-eg) ·
[Deploy Service Bus](https://clemensv.github.io/real-time-sources#usgs-waterdata/azure-amqp-sb)

## Upstream scope and interpretation

The selected scope is `continuous`, `monitoring-locations`,
`time-series-metadata` for instantaneous Points series, and `parameter-codes`.
`latest-continuous` is a duplicate presentation. Daily values, field visits,
peaks, method histories and additional lookup catalogs are outside the
user-selected scope. The complete keep/drop audit is in the
[migration ledger](../USGS-WATERSERVICES-MIGRATION-LEDGER.md).

- No authoritative legacy NWIS TS_ID-to-native-series crosswalk is available.
  Native IDs must not be inferred from legacy numbers or parameter/site matches.
- Observation values remain strings to preserve upstream precision and status
  encodings. Units vary by parameter and are carried in `unit_of_measure`.
  Unit labels remain resource-specific: parameter catalogs can report `ft3/s`
  or `deg C` where time-series metadata reports `ft^3/s` or `degC`.
  A parameter catalog's `Mean`/`1Day` metadata does not override the selected
  series' authoritative `00011`/`Instantaneous` statistic.
- `approval_status` and `qualifier` retain distinct meanings. Provisional data
  can be revised; consumers must not treat it as approved data.
  Upstream qualifier coverage remains incomplete; an absent qualifier does not
  prove that an observation has no qualification.
- Published GeoJSON coordinates are WGS84 longitude/latitude. Survey datum,
  position accuracy, vertical datum and units remain in location metadata.
- The published series schema describes `thresholds` as a string, but live
  data contains structured arrays. This upstream schema mismatch remains in
  the migration backlog; the feeder does not claim it has been resolved.
  The contract models the threshold fields documented in the migration audit.
  Threshold datetimes preserve seven
  fractional digits and open-ended sentinel dates in JSON. The parallel Avro
  contract uses string-backed datetimes with avrotize's custom
  `logicalType: rfc3339-timestamp-millis`, not Avro `long/timestamp-micros`.
  The underlying strings retain the original RFC3339 timestamp text.
  Consumers that interpret this custom logical type must verify their
  fractional-precision handling; consumers that ignore it receive strings.
  These images publish JSON, not Avro binary. Unreported label
  vocabularies remain open strings rather than invented enums.
- `data_gap_interval` retains its original ISO-8601 duration text, including
  live `PT1H15M` values. A handwritten serialization boundary avoids the
  generated Python duration encoder defect tracked in
  [avrotize#572](https://github.com/clemensv/avrotize/issues/572); generated
  files remain unchanged.
- Metadata `last_modified` can omit timezone information; its original text
  is retained. Observation `time` remains an offset-aware datetime.

### Documentation, licence and rate limits

- [OGC API documentation / collections](https://api.waterdata.usgs.gov/ogcapi/v1/collections)
- [USGS Water Data APIs](https://api.waterdata.usgs.gov/)
- [API keys and request limits](https://api.waterdata.usgs.gov/docs/ogcapi/keys/)
- [USGS copyright and credits](https://www.usgs.gov/information-policies-and-instructions/copyrights-and-credits)
- [USGS provisional data disclaimer](https://waterdata.usgs.gov/provisional-data-statement/)

USGS-produced data are generally U.S. public-domain works; attribution to
**U.S. Geological Survey** is requested. Third-party material can have separate
terms. No commercial-use restriction is introduced by this feeder.
An API key raises the hourly request limit. No `X-RateLimit` headers were
present in the reviewed anonymous response, so this feeder assumes no fixed
numerical quota. USGS documents `X-RateLimit-Limit` and
`X-RateLimit-Remaining` as the per-endpoint authority when present; its
illustrative header values are not a fixed quota for every query.
API gateways can return HTTP 429; this implementation
honors `Retry-After` with bounded retries. The reviewed collection schemas do
not specify a numerical request quota. The default 300-second poll is scoped
to one site and two parameters, not a national scan. Operators must size wider
selections against current USGS guidance and their API-key limits.

## Repository layout

`usgs_waterdata_core/` contains acquisition, delivery checkpoints and the
separate legacy-enrollment helpers. `usgs_waterdata/` contains the native
poller and Kafka entrypoint; `usgs_waterdata_mqtt/` and
`usgs_waterdata_amqp/` are separate transport packages.
`usgs_waterdata_producer/`, `usgs_waterdata_mqtt_producer/` and
`usgs_waterdata_amqp_producer/` are generated and must not be edited.
The authoritative contract is `xreg/usgs-waterdata.xreg.json`; regenerate via
`generate_producer.ps1` with enforced xrcg 0.11.0.
Public schema definitions and synthetic domain fixtures live under
`tests/fixtures/`. Raw upstream captures and audit receipts stay outside Git.
