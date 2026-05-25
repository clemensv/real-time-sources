# German Autobahn Traffic Bridge Events

MQTT/5.0 mirror of the DE.Autobahn CloudEvents, published into the Unified-Namespace topic tree 'traffic/de/autobahn/autobahn/{road}/{kind}/{identifier}/{state}'. {kind} (10 values) and {state} (appeared/updated/resolved) are literally baked per-message so xrcg can resolve every placeholder from schema fields. Lifecycle-event families (roadwork, short-term-roadwork, closure, entry-exit-closure, warning) are QoS-1 non-retained — they are state-change notifications, not LKV slots. Stable-object families (weight-limit-3-5, webcam, parking-lorry, electric-charging-station, strong-electric-charging-station) are QoS-1 retained so late subscribers see the current state of every known object; the bridge publishes an empty retained payload on `resolved` to clear the slot.

## Table of Contents

- [Registry](#registry)
- [Endpoints](#endpoints)
- [Messagegroups](#messagegroups)
- [Schemagroups](#schemagroups)

---

## Registry

| Field | Value |
| --- | --- |
| Endpoints | 2 |
| Messagegroups | 2 |
| Schemagroups | 2 |

## Endpoints

### Endpoint `DE.Autobahn.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`DE.Autobahn`](#messagegroup-deautobahn) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `autobahn` |
| Kafka key | `{identifier}` |
| Deployed | False |

### Endpoint `DE.Autobahn.Mqtt`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `MQTT/5.0` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"mode": "binary"}` |
| Messagegroups | [`DE.Autobahn.mqtt`](#messagegroup-deautobahnmqtt) |

#### Transport options

| Option | Value |
| --- | --- |
| Deployed | False |
| Broker endpoints | `[{"uri": "mqtt://localhost:1883"}]` |

## Messagegroups

### Messagegroup `DE.Autobahn`
<a id="messagegroup-deautobahn"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `DE.Autobahn.Kafka` (KAFKA) |
| Messages | 30 |

#### Message `DE.Autobahn.RoadworkAppeared`
<a id="message-deautobahnroadworkappeared"></a>

| Field | Value |
| --- | --- |
| Name | RoadworkAppeared |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.RoadEvent`](#schema-deautobahnroadevent) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.RoadworkAppeared` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Kafka` | `KAFKA` | topic `autobahn`; key `{identifier}` |

#### Message `DE.Autobahn.RoadworkUpdated`
<a id="message-deautobahnroadworkupdated"></a>

| Field | Value |
| --- | --- |
| Name | RoadworkUpdated |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.RoadEvent`](#schema-deautobahnroadevent) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.RoadworkUpdated` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Kafka` | `KAFKA` | topic `autobahn`; key `{identifier}` |

#### Message `DE.Autobahn.RoadworkResolved`
<a id="message-deautobahnroadworkresolved"></a>

| Field | Value |
| --- | --- |
| Name | RoadworkResolved |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.RoadEvent`](#schema-deautobahnroadevent) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.RoadworkResolved` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Kafka` | `KAFKA` | topic `autobahn`; key `{identifier}` |

#### Message `DE.Autobahn.ShortTermRoadworkAppeared`
<a id="message-deautobahnshorttermroadworkappeared"></a>

| Field | Value |
| --- | --- |
| Name | ShortTermRoadworkAppeared |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.RoadEvent`](#schema-deautobahnroadevent) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.ShortTermRoadworkAppeared` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Kafka` | `KAFKA` | topic `autobahn`; key `{identifier}` |

#### Message `DE.Autobahn.ShortTermRoadworkUpdated`
<a id="message-deautobahnshorttermroadworkupdated"></a>

| Field | Value |
| --- | --- |
| Name | ShortTermRoadworkUpdated |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.RoadEvent`](#schema-deautobahnroadevent) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.ShortTermRoadworkUpdated` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Kafka` | `KAFKA` | topic `autobahn`; key `{identifier}` |

#### Message `DE.Autobahn.ShortTermRoadworkResolved`
<a id="message-deautobahnshorttermroadworkresolved"></a>

| Field | Value |
| --- | --- |
| Name | ShortTermRoadworkResolved |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.RoadEvent`](#schema-deautobahnroadevent) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.ShortTermRoadworkResolved` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Kafka` | `KAFKA` | topic `autobahn`; key `{identifier}` |

#### Message `DE.Autobahn.WarningAppeared`
<a id="message-deautobahnwarningappeared"></a>

| Field | Value |
| --- | --- |
| Name | WarningAppeared |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.WarningEvent`](#schema-deautobahnwarningevent) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.WarningAppeared` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Kafka` | `KAFKA` | topic `autobahn`; key `{identifier}` |

#### Message `DE.Autobahn.WarningUpdated`
<a id="message-deautobahnwarningupdated"></a>

| Field | Value |
| --- | --- |
| Name | WarningUpdated |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.WarningEvent`](#schema-deautobahnwarningevent) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.WarningUpdated` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Kafka` | `KAFKA` | topic `autobahn`; key `{identifier}` |

#### Message `DE.Autobahn.WarningResolved`
<a id="message-deautobahnwarningresolved"></a>

| Field | Value |
| --- | --- |
| Name | WarningResolved |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.WarningEvent`](#schema-deautobahnwarningevent) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.WarningResolved` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Kafka` | `KAFKA` | topic `autobahn`; key `{identifier}` |

#### Message `DE.Autobahn.ClosureAppeared`
<a id="message-deautobahnclosureappeared"></a>

| Field | Value |
| --- | --- |
| Name | ClosureAppeared |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.RoadEvent`](#schema-deautobahnroadevent) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.ClosureAppeared` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Kafka` | `KAFKA` | topic `autobahn`; key `{identifier}` |

#### Message `DE.Autobahn.ClosureUpdated`
<a id="message-deautobahnclosureupdated"></a>

| Field | Value |
| --- | --- |
| Name | ClosureUpdated |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.RoadEvent`](#schema-deautobahnroadevent) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.ClosureUpdated` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Kafka` | `KAFKA` | topic `autobahn`; key `{identifier}` |

#### Message `DE.Autobahn.ClosureResolved`
<a id="message-deautobahnclosureresolved"></a>

| Field | Value |
| --- | --- |
| Name | ClosureResolved |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.RoadEvent`](#schema-deautobahnroadevent) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.ClosureResolved` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Kafka` | `KAFKA` | topic `autobahn`; key `{identifier}` |

#### Message `DE.Autobahn.EntryExitClosureAppeared`
<a id="message-deautobahnentryexitclosureappeared"></a>

| Field | Value |
| --- | --- |
| Name | EntryExitClosureAppeared |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.RoadEvent`](#schema-deautobahnroadevent) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.EntryExitClosureAppeared` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Kafka` | `KAFKA` | topic `autobahn`; key `{identifier}` |

#### Message `DE.Autobahn.EntryExitClosureUpdated`
<a id="message-deautobahnentryexitclosureupdated"></a>

| Field | Value |
| --- | --- |
| Name | EntryExitClosureUpdated |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.RoadEvent`](#schema-deautobahnroadevent) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.EntryExitClosureUpdated` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Kafka` | `KAFKA` | topic `autobahn`; key `{identifier}` |

#### Message `DE.Autobahn.EntryExitClosureResolved`
<a id="message-deautobahnentryexitclosureresolved"></a>

| Field | Value |
| --- | --- |
| Name | EntryExitClosureResolved |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.RoadEvent`](#schema-deautobahnroadevent) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.EntryExitClosureResolved` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Kafka` | `KAFKA` | topic `autobahn`; key `{identifier}` |

#### Message `DE.Autobahn.WeightLimit35RestrictionAppeared`
<a id="message-deautobahnweightlimit35restrictionappeared"></a>

| Field | Value |
| --- | --- |
| Name | WeightLimit35RestrictionAppeared |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.RoadEvent`](#schema-deautobahnroadevent) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.WeightLimit35RestrictionAppeared` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Kafka` | `KAFKA` | topic `autobahn`; key `{identifier}` |

#### Message `DE.Autobahn.WeightLimit35RestrictionUpdated`
<a id="message-deautobahnweightlimit35restrictionupdated"></a>

| Field | Value |
| --- | --- |
| Name | WeightLimit35RestrictionUpdated |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.RoadEvent`](#schema-deautobahnroadevent) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.WeightLimit35RestrictionUpdated` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Kafka` | `KAFKA` | topic `autobahn`; key `{identifier}` |

#### Message `DE.Autobahn.WeightLimit35RestrictionResolved`
<a id="message-deautobahnweightlimit35restrictionresolved"></a>

| Field | Value |
| --- | --- |
| Name | WeightLimit35RestrictionResolved |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.RoadEvent`](#schema-deautobahnroadevent) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.WeightLimit35RestrictionResolved` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Kafka` | `KAFKA` | topic `autobahn`; key `{identifier}` |

#### Message `DE.Autobahn.ParkingLorryAppeared`
<a id="message-deautobahnparkinglorryappeared"></a>

| Field | Value |
| --- | --- |
| Name | ParkingLorryAppeared |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.ParkingLorry`](#schema-deautobahnparkinglorry) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.ParkingLorryAppeared` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Kafka` | `KAFKA` | topic `autobahn`; key `{identifier}` |

#### Message `DE.Autobahn.ParkingLorryUpdated`
<a id="message-deautobahnparkinglorryupdated"></a>

| Field | Value |
| --- | --- |
| Name | ParkingLorryUpdated |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.ParkingLorry`](#schema-deautobahnparkinglorry) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.ParkingLorryUpdated` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Kafka` | `KAFKA` | topic `autobahn`; key `{identifier}` |

#### Message `DE.Autobahn.ParkingLorryResolved`
<a id="message-deautobahnparkinglorryresolved"></a>

| Field | Value |
| --- | --- |
| Name | ParkingLorryResolved |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.ParkingLorry`](#schema-deautobahnparkinglorry) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.ParkingLorryResolved` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Kafka` | `KAFKA` | topic `autobahn`; key `{identifier}` |

#### Message `DE.Autobahn.ElectricChargingStationAppeared`
<a id="message-deautobahnelectricchargingstationappeared"></a>

| Field | Value |
| --- | --- |
| Name | ElectricChargingStationAppeared |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.ChargingStation`](#schema-deautobahnchargingstation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.ElectricChargingStationAppeared` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Kafka` | `KAFKA` | topic `autobahn`; key `{identifier}` |

#### Message `DE.Autobahn.ElectricChargingStationUpdated`
<a id="message-deautobahnelectricchargingstationupdated"></a>

| Field | Value |
| --- | --- |
| Name | ElectricChargingStationUpdated |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.ChargingStation`](#schema-deautobahnchargingstation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.ElectricChargingStationUpdated` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Kafka` | `KAFKA` | topic `autobahn`; key `{identifier}` |

#### Message `DE.Autobahn.ElectricChargingStationResolved`
<a id="message-deautobahnelectricchargingstationresolved"></a>

| Field | Value |
| --- | --- |
| Name | ElectricChargingStationResolved |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.ChargingStation`](#schema-deautobahnchargingstation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.ElectricChargingStationResolved` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Kafka` | `KAFKA` | topic `autobahn`; key `{identifier}` |

#### Message `DE.Autobahn.StrongElectricChargingStationAppeared`
<a id="message-deautobahnstrongelectricchargingstationappeared"></a>

| Field | Value |
| --- | --- |
| Name | StrongElectricChargingStationAppeared |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.ChargingStation`](#schema-deautobahnchargingstation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.StrongElectricChargingStationAppeared` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Kafka` | `KAFKA` | topic `autobahn`; key `{identifier}` |

#### Message `DE.Autobahn.StrongElectricChargingStationUpdated`
<a id="message-deautobahnstrongelectricchargingstationupdated"></a>

| Field | Value |
| --- | --- |
| Name | StrongElectricChargingStationUpdated |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.ChargingStation`](#schema-deautobahnchargingstation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.StrongElectricChargingStationUpdated` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Kafka` | `KAFKA` | topic `autobahn`; key `{identifier}` |

#### Message `DE.Autobahn.StrongElectricChargingStationResolved`
<a id="message-deautobahnstrongelectricchargingstationresolved"></a>

| Field | Value |
| --- | --- |
| Name | StrongElectricChargingStationResolved |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.ChargingStation`](#schema-deautobahnchargingstation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.StrongElectricChargingStationResolved` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Kafka` | `KAFKA` | topic `autobahn`; key `{identifier}` |

#### Message `DE.Autobahn.WebcamAppeared`
<a id="message-deautobahnwebcamappeared"></a>

| Field | Value |
| --- | --- |
| Name | WebcamAppeared |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.Webcam`](#schema-deautobahnwebcam) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.WebcamAppeared` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Kafka` | `KAFKA` | topic `autobahn`; key `{identifier}` |

#### Message `DE.Autobahn.WebcamUpdated`
<a id="message-deautobahnwebcamupdated"></a>

| Field | Value |
| --- | --- |
| Name | WebcamUpdated |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.Webcam`](#schema-deautobahnwebcam) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.WebcamUpdated` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Kafka` | `KAFKA` | topic `autobahn`; key `{identifier}` |

#### Message `DE.Autobahn.WebcamResolved`
<a id="message-deautobahnwebcamresolved"></a>

| Field | Value |
| --- | --- |
| Name | WebcamResolved |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.Webcam`](#schema-deautobahnwebcam) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.WebcamResolved` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Kafka` | `KAFKA` | topic `autobahn`; key `{identifier}` |

### Messagegroup `DE.Autobahn.mqtt`
<a id="messagegroup-deautobahnmqtt"></a>

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 mirror of the DE.Autobahn CloudEvents, published into the Unified-Namespace topic tree 'traffic/de/autobahn/autobahn/{road}/{kind}/{identifier}/{state}'. {kind} (10 values) and {state} (appeared/updated/resolved) are literally baked per-message so xrcg can resolve every placeholder from schema fields. Lifecycle-event families (roadwork, short-term-roadwork, closure, entry-exit-closure, warning) are QoS-1 non-retained — they are state-change notifications, not LKV slots. Stable-object families (weight-limit-3-5, webcam, parking-lorry, electric-charging-station, strong-electric-charging-station) are QoS-1 retained so late subscribers see the current state of every known object; the bridge publishes an empty retained payload on `resolved` to clear the slot. |
| Transport bindings | `DE.Autobahn.Mqtt` (MQTT/5.0) |
| Messages | 30 |

#### Message `DE.Autobahn.RoadworkAppeared.mqtt`
<a id="message-deautobahnroadworkappearedmqtt"></a>

| Field | Value |
| --- | --- |
| Name | RoadworkAppeared |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.RoadEvent`](#schema-deautobahnroadevent) |
| Base message chain | `/messagegroups/DE.Autobahn/messages/DE.Autobahn.RoadworkAppeared` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.RoadworkAppeared` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Mqtt` | `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/roadwork/{identifier}/appeared` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `traffic/de/autobahn/autobahn/{road}/roadwork/{identifier}/appeared` |
| QoS | 1 |
| Retain | False |

#### Message `DE.Autobahn.RoadworkUpdated.mqtt`
<a id="message-deautobahnroadworkupdatedmqtt"></a>

| Field | Value |
| --- | --- |
| Name | RoadworkUpdated |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.RoadEvent`](#schema-deautobahnroadevent) |
| Base message chain | `/messagegroups/DE.Autobahn/messages/DE.Autobahn.RoadworkUpdated` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.RoadworkUpdated` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Mqtt` | `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/roadwork/{identifier}/updated` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `traffic/de/autobahn/autobahn/{road}/roadwork/{identifier}/updated` |
| QoS | 1 |
| Retain | False |

#### Message `DE.Autobahn.RoadworkResolved.mqtt`
<a id="message-deautobahnroadworkresolvedmqtt"></a>

| Field | Value |
| --- | --- |
| Name | RoadworkResolved |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.RoadEvent`](#schema-deautobahnroadevent) |
| Base message chain | `/messagegroups/DE.Autobahn/messages/DE.Autobahn.RoadworkResolved` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.RoadworkResolved` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Mqtt` | `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/roadwork/{identifier}/resolved` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `traffic/de/autobahn/autobahn/{road}/roadwork/{identifier}/resolved` |
| QoS | 1 |
| Retain | False |

#### Message `DE.Autobahn.ShortTermRoadworkAppeared.mqtt`
<a id="message-deautobahnshorttermroadworkappearedmqtt"></a>

| Field | Value |
| --- | --- |
| Name | ShortTermRoadworkAppeared |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.RoadEvent`](#schema-deautobahnroadevent) |
| Base message chain | `/messagegroups/DE.Autobahn/messages/DE.Autobahn.ShortTermRoadworkAppeared` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.ShortTermRoadworkAppeared` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Mqtt` | `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/short-term-roadwork/{identifier}/appeared` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `traffic/de/autobahn/autobahn/{road}/short-term-roadwork/{identifier}/appeared` |
| QoS | 1 |
| Retain | False |

#### Message `DE.Autobahn.ShortTermRoadworkUpdated.mqtt`
<a id="message-deautobahnshorttermroadworkupdatedmqtt"></a>

| Field | Value |
| --- | --- |
| Name | ShortTermRoadworkUpdated |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.RoadEvent`](#schema-deautobahnroadevent) |
| Base message chain | `/messagegroups/DE.Autobahn/messages/DE.Autobahn.ShortTermRoadworkUpdated` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.ShortTermRoadworkUpdated` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Mqtt` | `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/short-term-roadwork/{identifier}/updated` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `traffic/de/autobahn/autobahn/{road}/short-term-roadwork/{identifier}/updated` |
| QoS | 1 |
| Retain | False |

#### Message `DE.Autobahn.ShortTermRoadworkResolved.mqtt`
<a id="message-deautobahnshorttermroadworkresolvedmqtt"></a>

| Field | Value |
| --- | --- |
| Name | ShortTermRoadworkResolved |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.RoadEvent`](#schema-deautobahnroadevent) |
| Base message chain | `/messagegroups/DE.Autobahn/messages/DE.Autobahn.ShortTermRoadworkResolved` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.ShortTermRoadworkResolved` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Mqtt` | `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/short-term-roadwork/{identifier}/resolved` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `traffic/de/autobahn/autobahn/{road}/short-term-roadwork/{identifier}/resolved` |
| QoS | 1 |
| Retain | False |

#### Message `DE.Autobahn.ClosureAppeared.mqtt`
<a id="message-deautobahnclosureappearedmqtt"></a>

| Field | Value |
| --- | --- |
| Name | ClosureAppeared |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.RoadEvent`](#schema-deautobahnroadevent) |
| Base message chain | `/messagegroups/DE.Autobahn/messages/DE.Autobahn.ClosureAppeared` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.ClosureAppeared` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Mqtt` | `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/closure/{identifier}/appeared` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `traffic/de/autobahn/autobahn/{road}/closure/{identifier}/appeared` |
| QoS | 1 |
| Retain | False |

#### Message `DE.Autobahn.ClosureUpdated.mqtt`
<a id="message-deautobahnclosureupdatedmqtt"></a>

| Field | Value |
| --- | --- |
| Name | ClosureUpdated |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.RoadEvent`](#schema-deautobahnroadevent) |
| Base message chain | `/messagegroups/DE.Autobahn/messages/DE.Autobahn.ClosureUpdated` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.ClosureUpdated` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Mqtt` | `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/closure/{identifier}/updated` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `traffic/de/autobahn/autobahn/{road}/closure/{identifier}/updated` |
| QoS | 1 |
| Retain | False |

#### Message `DE.Autobahn.ClosureResolved.mqtt`
<a id="message-deautobahnclosureresolvedmqtt"></a>

| Field | Value |
| --- | --- |
| Name | ClosureResolved |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.RoadEvent`](#schema-deautobahnroadevent) |
| Base message chain | `/messagegroups/DE.Autobahn/messages/DE.Autobahn.ClosureResolved` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.ClosureResolved` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Mqtt` | `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/closure/{identifier}/resolved` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `traffic/de/autobahn/autobahn/{road}/closure/{identifier}/resolved` |
| QoS | 1 |
| Retain | False |

#### Message `DE.Autobahn.EntryExitClosureAppeared.mqtt`
<a id="message-deautobahnentryexitclosureappearedmqtt"></a>

| Field | Value |
| --- | --- |
| Name | EntryExitClosureAppeared |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.RoadEvent`](#schema-deautobahnroadevent) |
| Base message chain | `/messagegroups/DE.Autobahn/messages/DE.Autobahn.EntryExitClosureAppeared` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.EntryExitClosureAppeared` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Mqtt` | `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/entry-exit-closure/{identifier}/appeared` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `traffic/de/autobahn/autobahn/{road}/entry-exit-closure/{identifier}/appeared` |
| QoS | 1 |
| Retain | False |

#### Message `DE.Autobahn.EntryExitClosureUpdated.mqtt`
<a id="message-deautobahnentryexitclosureupdatedmqtt"></a>

| Field | Value |
| --- | --- |
| Name | EntryExitClosureUpdated |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.RoadEvent`](#schema-deautobahnroadevent) |
| Base message chain | `/messagegroups/DE.Autobahn/messages/DE.Autobahn.EntryExitClosureUpdated` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.EntryExitClosureUpdated` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Mqtt` | `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/entry-exit-closure/{identifier}/updated` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `traffic/de/autobahn/autobahn/{road}/entry-exit-closure/{identifier}/updated` |
| QoS | 1 |
| Retain | False |

#### Message `DE.Autobahn.EntryExitClosureResolved.mqtt`
<a id="message-deautobahnentryexitclosureresolvedmqtt"></a>

| Field | Value |
| --- | --- |
| Name | EntryExitClosureResolved |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.RoadEvent`](#schema-deautobahnroadevent) |
| Base message chain | `/messagegroups/DE.Autobahn/messages/DE.Autobahn.EntryExitClosureResolved` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.EntryExitClosureResolved` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Mqtt` | `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/entry-exit-closure/{identifier}/resolved` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `traffic/de/autobahn/autobahn/{road}/entry-exit-closure/{identifier}/resolved` |
| QoS | 1 |
| Retain | False |

#### Message `DE.Autobahn.WarningAppeared.mqtt`
<a id="message-deautobahnwarningappearedmqtt"></a>

| Field | Value |
| --- | --- |
| Name | WarningAppeared |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.WarningEvent`](#schema-deautobahnwarningevent) |
| Base message chain | `/messagegroups/DE.Autobahn/messages/DE.Autobahn.WarningAppeared` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.WarningAppeared` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Mqtt` | `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/warning/{identifier}/appeared` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `traffic/de/autobahn/autobahn/{road}/warning/{identifier}/appeared` |
| QoS | 1 |
| Retain | False |

#### Message `DE.Autobahn.WarningUpdated.mqtt`
<a id="message-deautobahnwarningupdatedmqtt"></a>

| Field | Value |
| --- | --- |
| Name | WarningUpdated |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.WarningEvent`](#schema-deautobahnwarningevent) |
| Base message chain | `/messagegroups/DE.Autobahn/messages/DE.Autobahn.WarningUpdated` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.WarningUpdated` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Mqtt` | `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/warning/{identifier}/updated` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `traffic/de/autobahn/autobahn/{road}/warning/{identifier}/updated` |
| QoS | 1 |
| Retain | False |

#### Message `DE.Autobahn.WarningResolved.mqtt`
<a id="message-deautobahnwarningresolvedmqtt"></a>

| Field | Value |
| --- | --- |
| Name | WarningResolved |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.WarningEvent`](#schema-deautobahnwarningevent) |
| Base message chain | `/messagegroups/DE.Autobahn/messages/DE.Autobahn.WarningResolved` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.WarningResolved` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Mqtt` | `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/warning/{identifier}/resolved` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `traffic/de/autobahn/autobahn/{road}/warning/{identifier}/resolved` |
| QoS | 1 |
| Retain | False |

#### Message `DE.Autobahn.WeightLimit35RestrictionAppeared.mqtt`
<a id="message-deautobahnweightlimit35restrictionappearedmqtt"></a>

| Field | Value |
| --- | --- |
| Name | WeightLimit35RestrictionAppeared |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.RoadEvent`](#schema-deautobahnroadevent) |
| Base message chain | `/messagegroups/DE.Autobahn/messages/DE.Autobahn.WeightLimit35RestrictionAppeared` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.WeightLimit35RestrictionAppeared` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Mqtt` | `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/weight-limit-3-5/{identifier}/appeared` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `traffic/de/autobahn/autobahn/{road}/weight-limit-3-5/{identifier}/appeared` |
| QoS | 1 |
| Retain | True |

#### Message `DE.Autobahn.WeightLimit35RestrictionUpdated.mqtt`
<a id="message-deautobahnweightlimit35restrictionupdatedmqtt"></a>

| Field | Value |
| --- | --- |
| Name | WeightLimit35RestrictionUpdated |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.RoadEvent`](#schema-deautobahnroadevent) |
| Base message chain | `/messagegroups/DE.Autobahn/messages/DE.Autobahn.WeightLimit35RestrictionUpdated` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.WeightLimit35RestrictionUpdated` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Mqtt` | `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/weight-limit-3-5/{identifier}/updated` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `traffic/de/autobahn/autobahn/{road}/weight-limit-3-5/{identifier}/updated` |
| QoS | 1 |
| Retain | True |

#### Message `DE.Autobahn.WeightLimit35RestrictionResolved.mqtt`
<a id="message-deautobahnweightlimit35restrictionresolvedmqtt"></a>

| Field | Value |
| --- | --- |
| Name | WeightLimit35RestrictionResolved |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.RoadEvent`](#schema-deautobahnroadevent) |
| Base message chain | `/messagegroups/DE.Autobahn/messages/DE.Autobahn.WeightLimit35RestrictionResolved` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.WeightLimit35RestrictionResolved` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Mqtt` | `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/weight-limit-3-5/{identifier}/resolved` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `traffic/de/autobahn/autobahn/{road}/weight-limit-3-5/{identifier}/resolved` |
| QoS | 1 |
| Retain | True |

#### Message `DE.Autobahn.WebcamAppeared.mqtt`
<a id="message-deautobahnwebcamappearedmqtt"></a>

| Field | Value |
| --- | --- |
| Name | WebcamAppeared |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.Webcam`](#schema-deautobahnwebcam) |
| Base message chain | `/messagegroups/DE.Autobahn/messages/DE.Autobahn.WebcamAppeared` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.WebcamAppeared` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Mqtt` | `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/webcam/{identifier}/appeared` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `traffic/de/autobahn/autobahn/{road}/webcam/{identifier}/appeared` |
| QoS | 1 |
| Retain | True |

#### Message `DE.Autobahn.WebcamUpdated.mqtt`
<a id="message-deautobahnwebcamupdatedmqtt"></a>

| Field | Value |
| --- | --- |
| Name | WebcamUpdated |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.Webcam`](#schema-deautobahnwebcam) |
| Base message chain | `/messagegroups/DE.Autobahn/messages/DE.Autobahn.WebcamUpdated` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.WebcamUpdated` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Mqtt` | `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/webcam/{identifier}/updated` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `traffic/de/autobahn/autobahn/{road}/webcam/{identifier}/updated` |
| QoS | 1 |
| Retain | True |

#### Message `DE.Autobahn.WebcamResolved.mqtt`
<a id="message-deautobahnwebcamresolvedmqtt"></a>

| Field | Value |
| --- | --- |
| Name | WebcamResolved |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.Webcam`](#schema-deautobahnwebcam) |
| Base message chain | `/messagegroups/DE.Autobahn/messages/DE.Autobahn.WebcamResolved` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.WebcamResolved` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Mqtt` | `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/webcam/{identifier}/resolved` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `traffic/de/autobahn/autobahn/{road}/webcam/{identifier}/resolved` |
| QoS | 1 |
| Retain | True |

#### Message `DE.Autobahn.ParkingLorryAppeared.mqtt`
<a id="message-deautobahnparkinglorryappearedmqtt"></a>

| Field | Value |
| --- | --- |
| Name | ParkingLorryAppeared |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.ParkingLorry`](#schema-deautobahnparkinglorry) |
| Base message chain | `/messagegroups/DE.Autobahn/messages/DE.Autobahn.ParkingLorryAppeared` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.ParkingLorryAppeared` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Mqtt` | `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/parking-lorry/{identifier}/appeared` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `traffic/de/autobahn/autobahn/{road}/parking-lorry/{identifier}/appeared` |
| QoS | 1 |
| Retain | True |

#### Message `DE.Autobahn.ParkingLorryUpdated.mqtt`
<a id="message-deautobahnparkinglorryupdatedmqtt"></a>

| Field | Value |
| --- | --- |
| Name | ParkingLorryUpdated |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.ParkingLorry`](#schema-deautobahnparkinglorry) |
| Base message chain | `/messagegroups/DE.Autobahn/messages/DE.Autobahn.ParkingLorryUpdated` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.ParkingLorryUpdated` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Mqtt` | `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/parking-lorry/{identifier}/updated` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `traffic/de/autobahn/autobahn/{road}/parking-lorry/{identifier}/updated` |
| QoS | 1 |
| Retain | True |

#### Message `DE.Autobahn.ParkingLorryResolved.mqtt`
<a id="message-deautobahnparkinglorryresolvedmqtt"></a>

| Field | Value |
| --- | --- |
| Name | ParkingLorryResolved |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.ParkingLorry`](#schema-deautobahnparkinglorry) |
| Base message chain | `/messagegroups/DE.Autobahn/messages/DE.Autobahn.ParkingLorryResolved` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.ParkingLorryResolved` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Mqtt` | `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/parking-lorry/{identifier}/resolved` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `traffic/de/autobahn/autobahn/{road}/parking-lorry/{identifier}/resolved` |
| QoS | 1 |
| Retain | True |

#### Message `DE.Autobahn.ElectricChargingStationAppeared.mqtt`
<a id="message-deautobahnelectricchargingstationappearedmqtt"></a>

| Field | Value |
| --- | --- |
| Name | ElectricChargingStationAppeared |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.ChargingStation`](#schema-deautobahnchargingstation) |
| Base message chain | `/messagegroups/DE.Autobahn/messages/DE.Autobahn.ElectricChargingStationAppeared` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.ElectricChargingStationAppeared` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Mqtt` | `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/electric-charging-station/{identifier}/appeared` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `traffic/de/autobahn/autobahn/{road}/electric-charging-station/{identifier}/appeared` |
| QoS | 1 |
| Retain | True |

#### Message `DE.Autobahn.ElectricChargingStationUpdated.mqtt`
<a id="message-deautobahnelectricchargingstationupdatedmqtt"></a>

| Field | Value |
| --- | --- |
| Name | ElectricChargingStationUpdated |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.ChargingStation`](#schema-deautobahnchargingstation) |
| Base message chain | `/messagegroups/DE.Autobahn/messages/DE.Autobahn.ElectricChargingStationUpdated` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.ElectricChargingStationUpdated` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Mqtt` | `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/electric-charging-station/{identifier}/updated` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `traffic/de/autobahn/autobahn/{road}/electric-charging-station/{identifier}/updated` |
| QoS | 1 |
| Retain | True |

#### Message `DE.Autobahn.ElectricChargingStationResolved.mqtt`
<a id="message-deautobahnelectricchargingstationresolvedmqtt"></a>

| Field | Value |
| --- | --- |
| Name | ElectricChargingStationResolved |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.ChargingStation`](#schema-deautobahnchargingstation) |
| Base message chain | `/messagegroups/DE.Autobahn/messages/DE.Autobahn.ElectricChargingStationResolved` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.ElectricChargingStationResolved` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Mqtt` | `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/electric-charging-station/{identifier}/resolved` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `traffic/de/autobahn/autobahn/{road}/electric-charging-station/{identifier}/resolved` |
| QoS | 1 |
| Retain | True |

#### Message `DE.Autobahn.StrongElectricChargingStationAppeared.mqtt`
<a id="message-deautobahnstrongelectricchargingstationappearedmqtt"></a>

| Field | Value |
| --- | --- |
| Name | StrongElectricChargingStationAppeared |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.ChargingStation`](#schema-deautobahnchargingstation) |
| Base message chain | `/messagegroups/DE.Autobahn/messages/DE.Autobahn.StrongElectricChargingStationAppeared` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.StrongElectricChargingStationAppeared` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Mqtt` | `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/strong-electric-charging-station/{identifier}/appeared` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `traffic/de/autobahn/autobahn/{road}/strong-electric-charging-station/{identifier}/appeared` |
| QoS | 1 |
| Retain | True |

#### Message `DE.Autobahn.StrongElectricChargingStationUpdated.mqtt`
<a id="message-deautobahnstrongelectricchargingstationupdatedmqtt"></a>

| Field | Value |
| --- | --- |
| Name | StrongElectricChargingStationUpdated |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.ChargingStation`](#schema-deautobahnchargingstation) |
| Base message chain | `/messagegroups/DE.Autobahn/messages/DE.Autobahn.StrongElectricChargingStationUpdated` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.StrongElectricChargingStationUpdated` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Mqtt` | `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/strong-electric-charging-station/{identifier}/updated` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `traffic/de/autobahn/autobahn/{road}/strong-electric-charging-station/{identifier}/updated` |
| QoS | 1 |
| Retain | True |

#### Message `DE.Autobahn.StrongElectricChargingStationResolved.mqtt`
<a id="message-deautobahnstrongelectricchargingstationresolvedmqtt"></a>

| Field | Value |
| --- | --- |
| Name | StrongElectricChargingStationResolved |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Autobahn.jstruct/schemas/DE.Autobahn.ChargingStation`](#schema-deautobahnchargingstation) |
| Base message chain | `/messagegroups/DE.Autobahn/messages/DE.Autobahn.StrongElectricChargingStationResolved` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Autobahn.StrongElectricChargingStationResolved` |
| `source` |  | `string` | `False` | `https://verkehr.autobahn.de/o/autobahn` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Autobahn.Mqtt` | `MQTT/5.0` | topic `traffic/de/autobahn/autobahn/{road}/strong-electric-charging-station/{identifier}/resolved` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `traffic/de/autobahn/autobahn/{road}/strong-electric-charging-station/{identifier}/resolved` |
| QoS | 1 |
| Retain | True |

## Schemagroups

### Schemagroup `DE.Autobahn.jstruct`
<a id="schemagroup-deautobahnjstruct"></a>

#### Schema `DE.Autobahn.RoadEvent`
<a id="schema-deautobahnroadevent"></a>

| Field | Value |
| --- | --- |
| Name | RoadEvent |
| Format | JsonStructure/draft-02 |
| Default version | 1 |
| Description | Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/DE/Autobahn/RoadEvent` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |
| Additional properties | `False` |

###### Object `RoadEvent`
<a id="schema-node-roadevent"></a>

Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure.

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/DE/Autobahn/RoadEvent` |
| Additional properties | `False` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `identifier` | `string` | `True` | Stable Autobahn item identifier used for the CloudEvents subject and Kafka key. | altnames=`{"autobahn-api": "identifier"}` | - | - |
| `road` | `string` | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. | - | pattern=`^[a-z0-9-]+$` | - |
| `road_ids` | array of `string` | `True` | Autobahn road identifiers for the road query that yielded this item. The bridge emits the queried road id as a stable array field shared by all Autobahn families. | - | minItems=`1`<br>uniqueItems=`True` | - |
| `event_time` | `datetime` | `True` | CloudEvents event time for the emitted record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp. | - | - | - |
| `display_type` | enum `['ROADWORKS', 'SHORT_TERM_ROADWORKS', 'CLOSURE', 'CLOSURE_ENTRY_EXIT', 'WEIGHT_LIMIT_35']` | `True` | Autobahn API display_type value that identifies the road-event subtype. | altnames=`{"autobahn-api": "display_type"}` | - | - |
| `title` | `union` | `False` | Human-readable title from the Autobahn API item. | - | - | - |
| `subtitle` | `union` | `False` | Human-readable subtitle from the Autobahn API item. | - | - | - |
| `description_lines` | `union` | `False` | Description lines from the Autobahn API description array. | altnames=`{"autobahn-api": "description"}` | - | - |
| `future` | `union` | `False` | Whether the Autobahn API marks the item as a future event. | altnames=`{"autobahn-api": "future"}` | - | - |
| `is_blocked` | `union` | `False` | Whether the Autobahn API marks the affected road segment as blocked. | altnames=`{"autobahn-api": "isBlocked"}` | - | - |
| `icon` | `union` | `False` | Autobahn API icon identifier for the item. | altnames=`{"autobahn-api": "icon"}` | - | - |
| `start_lc_position` | `union` | `False` | Numeric startLcPosition value emitted by the Autobahn API for the beginning of the affected segment. | altnames=`{"autobahn-api": "startLcPosition"}` | - | - |
| `start_timestamp` | `union` | `False` | startTimestamp value from the Autobahn API when the item includes a scheduled or known start time. | altnames=`{"autobahn-api": "startTimestamp"}` | - | - |
| `extent` | `union` | `False` | Autobahn API extent text for the affected road segment. | altnames=`{"autobahn-api": "extent"}` | - | - |
| `point` | `union` | `False` | Autobahn API point text that identifies the affected point on the road segment. | altnames=`{"autobahn-api": "point"}` | - | - |
| `coordinate_lat` | `union` | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. | altnames=`{"autobahn-api": "coordinate.lat"}` | maximum=`90`<br>minimum=`-90` | - |
| `coordinate_lon` | `union` | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. | altnames=`{"autobahn-api": "coordinate.long"}` | maximum=`180`<br>minimum=`-180` | - |
| `geometry_json` | `union` | `False` | Serialized Autobahn API geometry object for the affected road segment. | altnames=`{"autobahn-api": "geometry"}` | - | - |
| `impact_lower` | `union` | `False` | Lower bound from the Autobahn API impact object. | altnames=`{"autobahn-api": "impact.lower"}` | - | - |
| `impact_upper` | `union` | `False` | Upper bound from the Autobahn API impact object. | altnames=`{"autobahn-api": "impact.upper"}` | - | - |
| `impact_symbols` | `union` | `False` | Impact symbols from the Autobahn API impact.symbols array. | altnames=`{"autobahn-api": "impact.symbols"}` | - | - |
| `route_recommendation_json` | `union` | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available. | altnames=`{"autobahn-api": "routeRecommendation"}` | - | - |
| `footer_lines` | `union` | `False` | Footer lines from the Autobahn API footer array. | altnames=`{"autobahn-api": "footer"}` | - | - |

#### Schema `DE.Autobahn.WarningEvent`
<a id="schema-deautobahnwarningevent"></a>

| Field | Value |
| --- | --- |
| Name | WarningEvent |
| Format | JsonStructure/draft-02 |
| Default version | 1 |
| Description | Normalized Autobahn warning payload with delay and traffic source details. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/warning. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/DE/Autobahn/WarningEvent` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |
| Additional properties | `False` |

###### Object `WarningEvent`
<a id="schema-node-warningevent"></a>

Normalized Autobahn warning payload with delay and traffic source details. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/warning.

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/DE/Autobahn/WarningEvent` |
| Additional properties | `False` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `identifier` | `string` | `True` | Stable Autobahn warning identifier used for the CloudEvents subject and Kafka key. | altnames=`{"autobahn-api": "identifier"}` | - | - |
| `road` | `string` | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. | - | pattern=`^[a-z0-9-]+$` | - |
| `road_ids` | array of `string` | `True` | Autobahn road identifiers for the road query that yielded this warning item. | - | minItems=`1`<br>uniqueItems=`True` | - |
| `event_time` | `datetime` | `True` | CloudEvents event time for the emitted warning record. For appeared events the bridge uses startTimestamp when the API supplies it; otherwise it uses the poll timestamp. | - | - | - |
| `display_type` | enum `['WARNING']` | `True` | Autobahn API display_type for warning items. | altnames=`{"autobahn-api": "display_type"}` | - | - |
| `title` | `union` | `False` | Human-readable title from the Autobahn API warning item. | - | - | - |
| `subtitle` | `union` | `False` | Human-readable subtitle from the Autobahn API warning item. | - | - | - |
| `description_lines` | `union` | `False` | Description lines from the Autobahn API description array. | altnames=`{"autobahn-api": "description"}` | - | - |
| `future` | `union` | `False` | Whether the Autobahn API marks the warning as a future event. | altnames=`{"autobahn-api": "future"}` | - | - |
| `is_blocked` | `union` | `False` | Whether the Autobahn API marks the warning segment as blocked. | altnames=`{"autobahn-api": "isBlocked"}` | - | - |
| `icon` | `union` | `False` | Autobahn API icon identifier for the warning item. | altnames=`{"autobahn-api": "icon"}` | - | - |
| `start_lc_position` | `union` | `False` | Numeric startLcPosition value emitted by the Autobahn API for the beginning of the warning segment. | altnames=`{"autobahn-api": "startLcPosition"}` | - | - |
| `start_timestamp` | `union` | `False` | startTimestamp value from the Autobahn API when the warning includes a scheduled or known start time. | altnames=`{"autobahn-api": "startTimestamp"}` | - | - |
| `extent` | `union` | `False` | Autobahn API extent text for the affected road segment. | altnames=`{"autobahn-api": "extent"}` | - | - |
| `point` | `union` | `False` | Autobahn API point text that identifies the affected point on the road segment. | altnames=`{"autobahn-api": "point"}` | - | - |
| `coordinate_lat` | `union` | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. | altnames=`{"autobahn-api": "coordinate.lat"}` | maximum=`90`<br>minimum=`-90` | - |
| `coordinate_lon` | `union` | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. | altnames=`{"autobahn-api": "coordinate.long"}` | maximum=`180`<br>minimum=`-180` | - |
| `geometry_json` | `union` | `False` | Serialized Autobahn API geometry object for the affected road segment. | altnames=`{"autobahn-api": "geometry"}` | - | - |
| `impact_lower` | `union` | `False` | Lower bound from the Autobahn API impact object. | altnames=`{"autobahn-api": "impact.lower"}` | - | - |
| `impact_upper` | `union` | `False` | Upper bound from the Autobahn API impact object. | altnames=`{"autobahn-api": "impact.upper"}` | - | - |
| `impact_symbols` | `union` | `False` | Impact symbols from the Autobahn API impact.symbols array. | altnames=`{"autobahn-api": "impact.symbols"}` | - | - |
| `route_recommendation_json` | `union` | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available. | altnames=`{"autobahn-api": "routeRecommendation"}` | - | - |
| `footer_lines` | `union` | `False` | Footer lines from the Autobahn API footer array. | altnames=`{"autobahn-api": "footer"}` | - | - |
| `delay_minutes` | `union` | `False` | delayTimeValue from the Autobahn warning item, expressed in minutes. | unit=`min`<br>altnames=`{"autobahn-api": "delayTimeValue"}` | minimum=`0` | - |
| `average_speed_kmh` | `union` | `False` | averageSpeed from the Autobahn warning item, expressed in kilometers per hour. | unit=`km/h`<br>altnames=`{"autobahn-api": "averageSpeed"}` | minimum=`0` | - |
| `abnormal_traffic_type` | `union` | `False` | abnormalTrafficType code from the Autobahn warning item. | altnames=`{"autobahn-api": "abnormalTrafficType"}` | - | - |
| `source_name` | `union` | `False` | source value from the Autobahn warning item that identifies the origin of the warning. | altnames=`{"autobahn-api": "source"}` | - | - |

#### Schema `DE.Autobahn.ParkingLorry`
<a id="schema-deautobahnparkinglorry"></a>

| Field | Value |
| --- | --- |
| Name | ParkingLorry |
| Format | JsonStructure/draft-02 |
| Default version | 1 |
| Description | Normalized Autobahn lorry parking payload with parsed amenity and space counts. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/parking_lorry. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/DE/Autobahn/ParkingLorry` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |
| Additional properties | `False` |

###### Object `ParkingLorry`
<a id="schema-node-parkinglorry"></a>

Normalized Autobahn lorry parking payload with parsed amenity and space counts. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/parking_lorry.

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/DE/Autobahn/ParkingLorry` |
| Additional properties | `False` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `identifier` | `string` | `True` | Stable Autobahn parking identifier used for the CloudEvents subject and Kafka key. | altnames=`{"autobahn-api": "identifier"}` | - | - |
| `road` | `string` | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. | - | pattern=`^[a-z0-9-]+$` | - |
| `road_ids` | array of `string` | `True` | Autobahn road identifiers for the road query that yielded this parking item. | - | minItems=`1`<br>uniqueItems=`True` | - |
| `event_time` | `datetime` | `True` | CloudEvents event time for the emitted parking record. The bridge uses the poll timestamp because parking items do not expose startTimestamp in the normalized payload. | - | - | - |
| `display_type` | enum `['PARKING']` | `True` | Autobahn API display_type for lorry parking items. | altnames=`{"autobahn-api": "display_type"}` | - | - |
| `title` | `union` | `False` | Human-readable title from the Autobahn API parking item. | - | - | - |
| `subtitle` | `union` | `False` | Human-readable subtitle from the Autobahn API parking item. | - | - | - |
| `description_lines` | `union` | `False` | Description lines from the Autobahn API description array. | altnames=`{"autobahn-api": "description"}` | - | - |
| `future` | `union` | `False` | Whether the Autobahn API marks the parking item as a future entry. | altnames=`{"autobahn-api": "future"}` | - | - |
| `is_blocked` | `union` | `False` | Whether the Autobahn API marks the parking site as blocked. | altnames=`{"autobahn-api": "isBlocked"}` | - | - |
| `icon` | `union` | `False` | Autobahn API icon identifier for the parking item. | altnames=`{"autobahn-api": "icon"}` | - | - |
| `start_lc_position` | `union` | `False` | Numeric startLcPosition value emitted by the Autobahn API for the parking site location. | altnames=`{"autobahn-api": "startLcPosition"}` | - | - |
| `extent` | `union` | `False` | Autobahn API extent text for the parking site. | altnames=`{"autobahn-api": "extent"}` | - | - |
| `point` | `union` | `False` | Autobahn API point text that identifies the parking site location. | altnames=`{"autobahn-api": "point"}` | - | - |
| `coordinate_lat` | `union` | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. | altnames=`{"autobahn-api": "coordinate.lat"}` | maximum=`90`<br>minimum=`-90` | - |
| `coordinate_lon` | `union` | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. | altnames=`{"autobahn-api": "coordinate.long"}` | maximum=`180`<br>minimum=`-180` | - |
| `route_recommendation_json` | `union` | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available for the parking location. | altnames=`{"autobahn-api": "routeRecommendation"}` | - | - |
| `footer_lines` | `union` | `False` | Footer lines from the Autobahn API footer array. | altnames=`{"autobahn-api": "footer"}` | - | - |
| `amenity_descriptions` | `union` | `False` | Descriptions extracted from lorryParkingFeatureIcons[].description for the parking site amenities. | altnames=`{"autobahn-api": "lorryParkingFeatureIcons[].description"}` | - | - |
| `car_space_count` | `union` | `False` | Number of passenger-car spaces parsed from description lines that contain PKW Stellplätze. | - | minimum=`0` | - |
| `lorry_space_count` | `union` | `False` | Number of lorry spaces parsed from description lines that contain LKW Stellplätze. | - | minimum=`0` | - |

#### Schema `DE.Autobahn.ChargingStation`
<a id="schema-deautobahnchargingstation"></a>

| Field | Value |
| --- | --- |
| Name | ChargingStation |
| Format | JsonStructure/draft-02 |
| Default version | 1 |
| Description | Normalized Autobahn charging-station payload with parsed address and charging point details. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/electric_charging_station. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/DE/Autobahn/ChargingStation` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |
| Additional properties | `False` |

###### Object `ChargingStation`
<a id="schema-node-chargingstation"></a>

Normalized Autobahn charging-station payload with parsed address and charging point details. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/electric_charging_station.

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/DE/Autobahn/ChargingStation` |
| Additional properties | `False` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `identifier` | `string` | `True` | Stable Autobahn charging-station identifier used for the CloudEvents subject and Kafka key. | altnames=`{"autobahn-api": "identifier"}` | - | - |
| `road` | `string` | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. | - | pattern=`^[a-z0-9-]+$` | - |
| `road_ids` | array of `string` | `True` | Autobahn road identifiers for the road query that yielded this charging station item. | - | minItems=`1`<br>uniqueItems=`True` | - |
| `event_time` | `datetime` | `True` | CloudEvents event time for the emitted charging-station record. The bridge uses the poll timestamp because charging station items do not expose startTimestamp in the normalized payload. | - | - | - |
| `display_type` | enum `['ELECTRIC_CHARGING_STATION', 'STRONG_ELECTRIC_CHARGING_STATION']` | `True` | Autobahn API display_type for charging-station items. | altnames=`{"autobahn-api": "display_type"}` | - | - |
| `title` | `union` | `False` | Human-readable title from the Autobahn API charging-station item. | - | - | - |
| `subtitle` | `union` | `False` | Human-readable subtitle from the Autobahn API charging-station item. | - | - | - |
| `description_lines` | `union` | `False` | Description lines from the Autobahn API description array. | altnames=`{"autobahn-api": "description"}` | - | - |
| `future` | `union` | `False` | Whether the Autobahn API marks the charging station item as a future entry. | altnames=`{"autobahn-api": "future"}` | - | - |
| `is_blocked` | `union` | `False` | Whether the Autobahn API marks the charging station site as blocked. | altnames=`{"autobahn-api": "isBlocked"}` | - | - |
| `icon` | `union` | `False` | Autobahn API icon identifier for the charging station item. | altnames=`{"autobahn-api": "icon"}` | - | - |
| `extent` | `union` | `False` | Autobahn API extent text for the charging station site. | altnames=`{"autobahn-api": "extent"}` | - | - |
| `point` | `union` | `False` | Autobahn API point text that identifies the charging station site. | altnames=`{"autobahn-api": "point"}` | - | - |
| `coordinate_lat` | `union` | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. | altnames=`{"autobahn-api": "coordinate.lat"}` | maximum=`90`<br>minimum=`-90` | - |
| `coordinate_lon` | `union` | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. | altnames=`{"autobahn-api": "coordinate.long"}` | maximum=`180`<br>minimum=`-180` | - |
| `address_line` | `union` | `False` | Address line parsed from the first Autobahn API description line for the charging station site. | - | - | - |
| `charging_point_count` | `union` | `False` | Number of parsed charging point entries derived from the Autobahn API description lines. | - | minimum=`0` | - |
| `charging_points_json` | `union` | `False` | Serialized array of normalized charging point entries parsed from the Autobahn API description lines. | - | - | - |
| `route_recommendation_json` | `union` | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available for the charging station site. | altnames=`{"autobahn-api": "routeRecommendation"}` | - | - |
| `footer_lines` | `union` | `False` | Footer lines from the Autobahn API footer array. | altnames=`{"autobahn-api": "footer"}` | - | - |

#### Schema `DE.Autobahn.Webcam`
<a id="schema-deautobahnwebcam"></a>

| Field | Value |
| --- | --- |
| Name | Webcam |
| Format | JsonStructure/draft-02 |
| Default version | 1 |
| Description | Normalized Autobahn webcam payload with operator and media URLs. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/webcam. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/DE/Autobahn/Webcam` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |
| Additional properties | `False` |

###### Object `Webcam`
<a id="schema-node-webcam"></a>

Normalized Autobahn webcam payload with operator and media URLs. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/webcam.

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/DE/Autobahn/Webcam` |
| Additional properties | `False` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `identifier` | `string` | `True` | Stable Autobahn webcam identifier used for the CloudEvents subject and Kafka key. | altnames=`{"autobahn-api": "identifier"}` | - | - |
| `road` | `string` | `True` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. | - | pattern=`^[a-z0-9-]+$` | - |
| `road_ids` | array of `string` | `True` | Autobahn road identifiers for the road query that yielded this webcam item. | - | minItems=`1`<br>uniqueItems=`True` | - |
| `event_time` | `datetime` | `True` | CloudEvents event time for the emitted webcam record. The bridge uses the poll timestamp because webcam items do not expose startTimestamp in the normalized payload. | - | - | - |
| `display_type` | enum `['WEBCAM']` | `True` | Autobahn API display_type for webcam items. | altnames=`{"autobahn-api": "display_type"}` | - | - |
| `title` | `union` | `False` | Human-readable title from the Autobahn API webcam item. | - | - | - |
| `subtitle` | `union` | `False` | Human-readable subtitle from the Autobahn API webcam item. | - | - | - |
| `description_lines` | `union` | `False` | Description lines from the Autobahn API description array. | altnames=`{"autobahn-api": "description"}` | - | - |
| `future` | `union` | `False` | Whether the Autobahn API marks the webcam item as a future entry. | altnames=`{"autobahn-api": "future"}` | - | - |
| `is_blocked` | `union` | `False` | Whether the Autobahn API marks the webcam location as blocked. | altnames=`{"autobahn-api": "isBlocked"}` | - | - |
| `icon` | `union` | `False` | Autobahn API icon identifier for the webcam item. | altnames=`{"autobahn-api": "icon"}` | - | - |
| `extent` | `union` | `False` | Autobahn API extent text for the webcam location. | altnames=`{"autobahn-api": "extent"}` | - | - |
| `point` | `union` | `False` | Autobahn API point text that identifies the webcam location. | altnames=`{"autobahn-api": "point"}` | - | - |
| `coordinate_lat` | `union` | `False` | Latitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. | altnames=`{"autobahn-api": "coordinate.lat"}` | maximum=`90`<br>minimum=`-90` | - |
| `coordinate_lon` | `union` | `False` | Longitude extracted from the Autobahn API coordinate object or coordinate GeoJSON point. | altnames=`{"autobahn-api": "coordinate.long"}` | maximum=`180`<br>minimum=`-180` | - |
| `route_recommendation_json` | `union` | `False` | Serialized Autobahn API routeRecommendation object when rerouting advice is available for the webcam location. | altnames=`{"autobahn-api": "routeRecommendation"}` | - | - |
| `footer_lines` | `union` | `False` | Footer lines from the Autobahn API footer array. | altnames=`{"autobahn-api": "footer"}` | - | - |
| `operator_name` | `union` | `False` | operator value from the Autobahn API webcam item. | altnames=`{"autobahn-api": "operator"}` | - | - |
| `image_url` | `union` | `False` | imageurl value from the Autobahn API webcam item for the still image. | altnames=`{"autobahn-api": "imageurl"}` | - | - |
| `stream_url` | `union` | `False` | linkurl value from the Autobahn API webcam item for the linked stream or detail page. | altnames=`{"autobahn-api": "linkurl"}` | - | - |

### Schemagroup `DE.Autobahn.avro`
<a id="schemagroup-deautobahnavro"></a>

#### Schema `DE.Autobahn.RoadEvent`
<a id="schema-deautobahnroadevent"></a>

| Field | Value |
| --- | --- |
| Name | RoadEvent |
| Format | Avro/1.11.3 |
| Default version | 1 |
| Description | Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | RoadEvent |
| Namespace | DE.Autobahn |
| Type | `record` |
| Doc | Normalized Autobahn road-event payload used for roadworks and closure-like items. Source pages: https://verkehr.autobahn.de/o/autobahn/A1/services/roadworks and https://verkehr.autobahn.de/o/autobahn/A1/services/closure. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `identifier` | `string` |  | `-` |
| `road` | `string` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. | `-` |
| `road_ids` | array of `string` |  | `-` |
| `event_time` | `string` |  | `-` |
| `display_type` | `string` |  | `-` |
| `title` | `null` \| `string` |  | `-` |
| `subtitle` | `null` \| `string` |  | `-` |
| `description_lines` | `null` \| array of `string` |  | `-` |
| `future` | `null` \| `boolean` |  | `-` |
| `is_blocked` | `null` \| `boolean` |  | `-` |
| `icon` | `null` \| `string` |  | `-` |
| `start_lc_position` | `null` \| `int` |  | `-` |
| `start_timestamp` | `null` \| `string` |  | `-` |
| `extent` | `null` \| `string` |  | `-` |
| `point` | `null` \| `string` |  | `-` |
| `coordinate_lat` | `null` \| `double` |  | `-` |
| `coordinate_lon` | `null` \| `double` |  | `-` |
| `geometry_json` | `null` \| `string` |  | `-` |
| `impact_lower` | `null` \| `string` |  | `-` |
| `impact_upper` | `null` \| `string` |  | `-` |
| `impact_symbols` | `null` \| array of `string` |  | `-` |
| `route_recommendation_json` | `null` \| `string` |  | `-` |
| `footer_lines` | `null` \| array of `string` |  | `-` |

#### Schema `DE.Autobahn.WarningEvent`
<a id="schema-deautobahnwarningevent"></a>

| Field | Value |
| --- | --- |
| Name | WarningEvent |
| Format | Avro/1.11.3 |
| Default version | 1 |
| Description | Normalized Autobahn warning payload with delay and traffic source details. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/warning. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | WarningEvent |
| Namespace | DE.Autobahn |
| Type | `record` |
| Doc | Normalized Autobahn warning payload with delay and traffic source details. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/warning. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `identifier` | `string` |  | `-` |
| `road` | `string` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. | `-` |
| `road_ids` | array of `string` |  | `-` |
| `event_time` | `string` |  | `-` |
| `display_type` | `string` |  | `-` |
| `title` | `null` \| `string` |  | `-` |
| `subtitle` | `null` \| `string` |  | `-` |
| `description_lines` | `null` \| array of `string` |  | `-` |
| `future` | `null` \| `boolean` |  | `-` |
| `is_blocked` | `null` \| `boolean` |  | `-` |
| `icon` | `null` \| `string` |  | `-` |
| `start_lc_position` | `null` \| `int` |  | `-` |
| `start_timestamp` | `null` \| `string` |  | `-` |
| `extent` | `null` \| `string` |  | `-` |
| `point` | `null` \| `string` |  | `-` |
| `coordinate_lat` | `null` \| `double` |  | `-` |
| `coordinate_lon` | `null` \| `double` |  | `-` |
| `geometry_json` | `null` \| `string` |  | `-` |
| `impact_lower` | `null` \| `string` |  | `-` |
| `impact_upper` | `null` \| `string` |  | `-` |
| `impact_symbols` | `null` \| array of `string` |  | `-` |
| `route_recommendation_json` | `null` \| `string` |  | `-` |
| `footer_lines` | `null` \| array of `string` |  | `-` |
| `delay_minutes` | `null` \| `int` |  | `-` |
| `average_speed_kmh` | `null` \| `int` |  | `-` |
| `abnormal_traffic_type` | `null` \| `string` |  | `-` |
| `source_name` | `null` \| `string` |  | `-` |

#### Schema `DE.Autobahn.ParkingLorry`
<a id="schema-deautobahnparkinglorry"></a>

| Field | Value |
| --- | --- |
| Name | ParkingLorry |
| Format | Avro/1.11.3 |
| Default version | 1 |
| Description | Normalized Autobahn lorry parking payload with parsed amenity and space counts. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/parking_lorry. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | ParkingLorry |
| Namespace | DE.Autobahn |
| Type | `record` |
| Doc | Normalized Autobahn lorry parking payload with parsed amenity and space counts. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/parking_lorry. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `identifier` | `string` |  | `-` |
| `road` | `string` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. | `-` |
| `road_ids` | array of `string` |  | `-` |
| `event_time` | `string` |  | `-` |
| `display_type` | `string` |  | `-` |
| `title` | `null` \| `string` |  | `-` |
| `subtitle` | `null` \| `string` |  | `-` |
| `description_lines` | `null` \| array of `string` |  | `-` |
| `future` | `null` \| `boolean` |  | `-` |
| `is_blocked` | `null` \| `boolean` |  | `-` |
| `icon` | `null` \| `string` |  | `-` |
| `start_lc_position` | `null` \| `int` |  | `-` |
| `extent` | `null` \| `string` |  | `-` |
| `point` | `null` \| `string` |  | `-` |
| `coordinate_lat` | `null` \| `double` |  | `-` |
| `coordinate_lon` | `null` \| `double` |  | `-` |
| `route_recommendation_json` | `null` \| `string` |  | `-` |
| `footer_lines` | `null` \| array of `string` |  | `-` |
| `amenity_descriptions` | `null` \| array of `string` |  | `-` |
| `car_space_count` | `null` \| `int` |  | `-` |
| `lorry_space_count` | `null` \| `int` |  | `-` |

#### Schema `DE.Autobahn.ChargingStation`
<a id="schema-deautobahnchargingstation"></a>

| Field | Value |
| --- | --- |
| Name | ChargingStation |
| Format | Avro/1.11.3 |
| Default version | 1 |
| Description | Normalized Autobahn charging-station payload with parsed address and charging point details. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/electric_charging_station. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | ChargingStation |
| Namespace | DE.Autobahn |
| Type | `record` |
| Doc | Normalized Autobahn charging-station payload with parsed address and charging point details. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/electric_charging_station. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `identifier` | `string` |  | `-` |
| `road` | `string` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. | `-` |
| `road_ids` | array of `string` |  | `-` |
| `event_time` | `string` |  | `-` |
| `display_type` | `string` |  | `-` |
| `title` | `null` \| `string` |  | `-` |
| `subtitle` | `null` \| `string` |  | `-` |
| `description_lines` | `null` \| array of `string` |  | `-` |
| `future` | `null` \| `boolean` |  | `-` |
| `is_blocked` | `null` \| `boolean` |  | `-` |
| `icon` | `null` \| `string` |  | `-` |
| `extent` | `null` \| `string` |  | `-` |
| `point` | `null` \| `string` |  | `-` |
| `coordinate_lat` | `null` \| `double` |  | `-` |
| `coordinate_lon` | `null` \| `double` |  | `-` |
| `address_line` | `null` \| `string` |  | `-` |
| `charging_point_count` | `null` \| `int` |  | `-` |
| `charging_points_json` | `null` \| `string` |  | `-` |
| `route_recommendation_json` | `null` \| `string` |  | `-` |
| `footer_lines` | `null` \| array of `string` |  | `-` |

#### Schema `DE.Autobahn.Webcam`
<a id="schema-deautobahnwebcam"></a>

| Field | Value |
| --- | --- |
| Name | Webcam |
| Format | Avro/1.11.3 |
| Default version | 1 |
| Description | Normalized Autobahn webcam payload with operator and media URLs. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/webcam. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | Webcam |
| Namespace | DE.Autobahn |
| Type | `record` |
| Doc | Normalized Autobahn webcam payload with operator and media URLs. Source page: https://verkehr.autobahn.de/o/autobahn/A1/services/webcam. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `identifier` | `string` |  | `-` |
| `road` | `string` | Lowercase kebab-case autobahn road designation (e.g. 'a1', 'a2') for the road query that yielded this item. Populated by the bridge from the Autobahn API road id (which is upper-case, e.g. 'A1'). Used as the second-to-last MQTT topic segment so subscribers can wildcard per road (e.g. 'traffic/de/autobahn/autobahn/a1/+/+/+'). The full upstream set is retained on `road_ids` for completeness. | `-` |
| `road_ids` | array of `string` |  | `-` |
| `event_time` | `string` |  | `-` |
| `display_type` | `string` |  | `-` |
| `title` | `null` \| `string` |  | `-` |
| `subtitle` | `null` \| `string` |  | `-` |
| `description_lines` | `null` \| array of `string` |  | `-` |
| `future` | `null` \| `boolean` |  | `-` |
| `is_blocked` | `null` \| `boolean` |  | `-` |
| `icon` | `null` \| `string` |  | `-` |
| `extent` | `null` \| `string` |  | `-` |
| `point` | `null` \| `string` |  | `-` |
| `coordinate_lat` | `null` \| `double` |  | `-` |
| `coordinate_lon` | `null` \| `double` |  | `-` |
| `route_recommendation_json` | `null` \| `string` |  | `-` |
| `footer_lines` | `null` \| array of `string` |  | `-` |
| `operator_name` | `null` \| `string` |  | `-` |
| `image_url` | `null` \| `string` |  | `-` |
| `stream_url` | `null` \| `string` |  | `-` |
