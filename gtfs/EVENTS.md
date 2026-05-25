# GTFS and GTFS-RT API Bridge Usage Guide Events

**GTFS and GTFS-RT API Bridge** is a tool that fetches GTFS (General Transit Feed Specification) Realtime and Static data from various transit agency sources, processes the data, and publishes it to Kafka topics using SASL PLAIN authentication. This tool can be integrated with systems like Microsoft Event Hubs or Microsoft Fabric Event Streams.

## Table of Contents

- [Registry](#registry)
- [Endpoints](#endpoints)
- [Messagegroups](#messagegroups)
- [Schemagroups](#schemagroups)

---

## Registry

| Field | Value |
| --- | --- |
| Endpoints | 1 |
| Messagegroups | 2 |
| Schemagroups | 4 |

## Endpoints

### Endpoint `GeneralTransitFeed.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`GeneralTransitFeedRealTime`](#messagegroup-generaltransitfeedrealtime), [`GeneralTransitFeedStatic`](#messagegroup-generaltransitfeedstatic) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `gtfs` |
| Kafka key | `{agencyid}` |
| Deployed | False |

## Messagegroups

### Messagegroup `GeneralTransitFeedRealTime`
<a id="messagegroup-generaltransitfeedrealtime"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `GeneralTransitFeed.Kafka` (KAFKA) |
| Messages | 3 |

#### Message `GeneralTransitFeedRealTime.Vehicle.VehiclePosition`
<a id="message-generaltransitfeedrealtimevehiclevehicleposition"></a>

| Field | Value |
| --- | --- |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/GeneralTransitFeedRealTime.jstruct/schemas/GeneralTransitFeedRealTime.Vehicle.VehiclePosition`](#schema-generaltransitfeedrealtimevehiclevehicleposition) |
| Transport override | `None` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedRealTime.Vehicle.VehiclePosition` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `True` | `{agencyid}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `GeneralTransitFeed.Kafka` | `KAFKA` | topic `gtfs`; key `{agencyid}` |

#### Message `GeneralTransitFeedRealTime.Trip.TripUpdate`
<a id="message-generaltransitfeedrealtimetriptripupdate"></a>

| Field | Value |
| --- | --- |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/GeneralTransitFeedRealTime.jstruct/schemas/GeneralTransitFeedRealTime.Trip.TripUpdate`](#schema-generaltransitfeedrealtimetriptripupdate) |
| Transport override | `None` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedRealTime.Trip.TripUpdate` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `True` | `{agencyid}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `GeneralTransitFeed.Kafka` | `KAFKA` | topic `gtfs`; key `{agencyid}` |

#### Message `GeneralTransitFeedRealTime.Alert.Alert`
<a id="message-generaltransitfeedrealtimealertalert"></a>

| Field | Value |
| --- | --- |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/GeneralTransitFeedRealTime.jstruct/schemas/GeneralTransitFeedRealTime.Alert.Alert`](#schema-generaltransitfeedrealtimealertalert) |
| Transport override | `None` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedRealTime.Alert.Alert` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `True` | `{agencyid}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `GeneralTransitFeed.Kafka` | `KAFKA` | topic `gtfs`; key `{agencyid}` |

### Messagegroup `GeneralTransitFeedStatic`
<a id="messagegroup-generaltransitfeedstatic"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `GeneralTransitFeed.Kafka` (KAFKA) |
| Messages | 28 |

#### Message `GeneralTransitFeedStatic.Agency`
<a id="message-generaltransitfeedstaticagency"></a>

| Field | Value |
| --- | --- |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/GeneralTransitFeedStatic.jstruct/schemas/GeneralTransitFeedStatic.Agency`](#schema-generaltransitfeedstaticagency) |
| Transport override | `None` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.Agency` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `True` | `{agencyid}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `GeneralTransitFeed.Kafka` | `KAFKA` | topic `gtfs`; key `{agencyid}` |

#### Message `GeneralTransitFeedStatic.Areas`
<a id="message-generaltransitfeedstaticareas"></a>

| Field | Value |
| --- | --- |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/GeneralTransitFeedStatic.jstruct/schemas/GeneralTransitFeedStatic.Areas`](#schema-generaltransitfeedstaticareas) |
| Transport override | `None` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.Areas` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `True` | `{agencyid}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `GeneralTransitFeed.Kafka` | `KAFKA` | topic `gtfs`; key `{agencyid}` |

#### Message `GeneralTransitFeedStatic.Attributions`
<a id="message-generaltransitfeedstaticattributions"></a>

| Field | Value |
| --- | --- |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/GeneralTransitFeedStatic.jstruct/schemas/GeneralTransitFeedStatic.Attributions`](#schema-generaltransitfeedstaticattributions) |
| Transport override | `None` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.Attributions` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `True` | `{agencyid}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `GeneralTransitFeed.Kafka` | `KAFKA` | topic `gtfs`; key `{agencyid}` |

#### Message `GeneralTransitFeed.BookingRules`
<a id="message-generaltransitfeedbookingrules"></a>

| Field | Value |
| --- | --- |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/GeneralTransitFeedStatic.jstruct/schemas/GeneralTransitFeed.BookingRules`](#schema-generaltransitfeedbookingrules) |
| Transport override | `None` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeed.BookingRules` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `True` | `{agencyid}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `GeneralTransitFeed.Kafka` | `KAFKA` | topic `gtfs`; key `{agencyid}` |

#### Message `GeneralTransitFeedStatic.FareAttributes`
<a id="message-generaltransitfeedstaticfareattributes"></a>

| Field | Value |
| --- | --- |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/GeneralTransitFeedStatic.jstruct/schemas/GeneralTransitFeedStatic.FareAttributes`](#schema-generaltransitfeedstaticfareattributes) |
| Transport override | `None` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.FareAttributes` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `True` | `{agencyid}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `GeneralTransitFeed.Kafka` | `KAFKA` | topic `gtfs`; key `{agencyid}` |

#### Message `GeneralTransitFeedStatic.FareLegRules`
<a id="message-generaltransitfeedstaticfarelegrules"></a>

| Field | Value |
| --- | --- |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/GeneralTransitFeedStatic.jstruct/schemas/GeneralTransitFeedStatic.FareLegRules`](#schema-generaltransitfeedstaticfarelegrules) |
| Transport override | `None` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.FareLegRules` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `True` | `{agencyid}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `GeneralTransitFeed.Kafka` | `KAFKA` | topic `gtfs`; key `{agencyid}` |

#### Message `GeneralTransitFeedStatic.FareMedia`
<a id="message-generaltransitfeedstaticfaremedia"></a>

| Field | Value |
| --- | --- |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/GeneralTransitFeedStatic.jstruct/schemas/GeneralTransitFeedStatic.FareMedia`](#schema-generaltransitfeedstaticfaremedia) |
| Transport override | `None` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.FareMedia` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `True` | `{agencyid}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `GeneralTransitFeed.Kafka` | `KAFKA` | topic `gtfs`; key `{agencyid}` |

#### Message `GeneralTransitFeedStatic.FareProducts`
<a id="message-generaltransitfeedstaticfareproducts"></a>

| Field | Value |
| --- | --- |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/GeneralTransitFeedStatic.jstruct/schemas/GeneralTransitFeedStatic.FareProducts`](#schema-generaltransitfeedstaticfareproducts) |
| Transport override | `None` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.FareProducts` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `True` | `{agencyid}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `GeneralTransitFeed.Kafka` | `KAFKA` | topic `gtfs`; key `{agencyid}` |

#### Message `GeneralTransitFeedStatic.FareRules`
<a id="message-generaltransitfeedstaticfarerules"></a>

| Field | Value |
| --- | --- |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/GeneralTransitFeedStatic.jstruct/schemas/GeneralTransitFeedStatic.FareRules`](#schema-generaltransitfeedstaticfarerules) |
| Transport override | `None` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.FareRules` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `True` | `{agencyid}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `GeneralTransitFeed.Kafka` | `KAFKA` | topic `gtfs`; key `{agencyid}` |

#### Message `GeneralTransitFeedStatic.FareTransferRules`
<a id="message-generaltransitfeedstaticfaretransferrules"></a>

| Field | Value |
| --- | --- |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/GeneralTransitFeedStatic.jstruct/schemas/GeneralTransitFeedStatic.FareTransferRules`](#schema-generaltransitfeedstaticfaretransferrules) |
| Transport override | `None` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.FareTransferRules` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `True` | `{agencyid}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `GeneralTransitFeed.Kafka` | `KAFKA` | topic `gtfs`; key `{agencyid}` |

#### Message `GeneralTransitFeedStatic.FeedInfo`
<a id="message-generaltransitfeedstaticfeedinfo"></a>

| Field | Value |
| --- | --- |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/GeneralTransitFeedStatic.jstruct/schemas/GeneralTransitFeedStatic.FeedInfo`](#schema-generaltransitfeedstaticfeedinfo) |
| Transport override | `None` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.FeedInfo` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `True` | `{agencyid}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `GeneralTransitFeed.Kafka` | `KAFKA` | topic `gtfs`; key `{agencyid}` |

#### Message `GeneralTransitFeedStatic.Frequencies`
<a id="message-generaltransitfeedstaticfrequencies"></a>

| Field | Value |
| --- | --- |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/GeneralTransitFeedStatic.jstruct/schemas/GeneralTransitFeedStatic.Frequencies`](#schema-generaltransitfeedstaticfrequencies) |
| Transport override | `None` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.Frequencies` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `True` | `{agencyid}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `GeneralTransitFeed.Kafka` | `KAFKA` | topic `gtfs`; key `{agencyid}` |

#### Message `GeneralTransitFeedStatic.Levels`
<a id="message-generaltransitfeedstaticlevels"></a>

| Field | Value |
| --- | --- |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/GeneralTransitFeedStatic.jstruct/schemas/GeneralTransitFeedStatic.Levels`](#schema-generaltransitfeedstaticlevels) |
| Transport override | `None` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.Levels` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `True` | `{agencyid}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `GeneralTransitFeed.Kafka` | `KAFKA` | topic `gtfs`; key `{agencyid}` |

#### Message `GeneralTransitFeedStatic.LocationGeoJson`
<a id="message-generaltransitfeedstaticlocationgeojson"></a>

| Field | Value |
| --- | --- |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/GeneralTransitFeedStatic.jstruct/schemas/GeneralTransitFeedStatic.LocationGeoJson`](#schema-generaltransitfeedstaticlocationgeojson) |
| Transport override | `None` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.LocationGeoJson` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `True` | `{agencyid}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `GeneralTransitFeed.Kafka` | `KAFKA` | topic `gtfs`; key `{agencyid}` |

#### Message `GeneralTransitFeedStatic.LocationGroups`
<a id="message-generaltransitfeedstaticlocationgroups"></a>

| Field | Value |
| --- | --- |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/GeneralTransitFeedStatic.jstruct/schemas/GeneralTransitFeedStatic.LocationGroups`](#schema-generaltransitfeedstaticlocationgroups) |
| Transport override | `None` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.LocationGroups` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `True` | `{agencyid}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `GeneralTransitFeed.Kafka` | `KAFKA` | topic `gtfs`; key `{agencyid}` |

#### Message `GeneralTransitFeedStatic.LocationGroupStores`
<a id="message-generaltransitfeedstaticlocationgroupstores"></a>

| Field | Value |
| --- | --- |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/GeneralTransitFeedStatic.jstruct/schemas/GeneralTransitFeedStatic.LocationGroupStores`](#schema-generaltransitfeedstaticlocationgroupstores) |
| Transport override | `None` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.LocationGroupStores` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `True` | `{agencyid}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `GeneralTransitFeed.Kafka` | `KAFKA` | topic `gtfs`; key `{agencyid}` |

#### Message `GeneralTransitFeedStatic.Networks`
<a id="message-generaltransitfeedstaticnetworks"></a>

| Field | Value |
| --- | --- |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/GeneralTransitFeedStatic.jstruct/schemas/GeneralTransitFeedStatic.Networks`](#schema-generaltransitfeedstaticnetworks) |
| Transport override | `None` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.Networks` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `True` | `{agencyid}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `GeneralTransitFeed.Kafka` | `KAFKA` | topic `gtfs`; key `{agencyid}` |

#### Message `GeneralTransitFeedStatic.Pathways`
<a id="message-generaltransitfeedstaticpathways"></a>

| Field | Value |
| --- | --- |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/GeneralTransitFeedStatic.jstruct/schemas/GeneralTransitFeedStatic.Pathways`](#schema-generaltransitfeedstaticpathways) |
| Transport override | `None` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.Pathways` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `True` | `{agencyid}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `GeneralTransitFeed.Kafka` | `KAFKA` | topic `gtfs`; key `{agencyid}` |

#### Message `GeneralTransitFeedStatic.RouteNetworks`
<a id="message-generaltransitfeedstaticroutenetworks"></a>

| Field | Value |
| --- | --- |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/GeneralTransitFeedStatic.jstruct/schemas/GeneralTransitFeedStatic.RouteNetworks`](#schema-generaltransitfeedstaticroutenetworks) |
| Transport override | `None` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.RouteNetworks` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `True` | `{agencyid}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `GeneralTransitFeed.Kafka` | `KAFKA` | topic `gtfs`; key `{agencyid}` |

#### Message `GeneralTransitFeedStatic.Routes`
<a id="message-generaltransitfeedstaticroutes"></a>

| Field | Value |
| --- | --- |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/GeneralTransitFeedStatic.jstruct/schemas/GeneralTransitFeedStatic.Routes`](#schema-generaltransitfeedstaticroutes) |
| Transport override | `None` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.Routes` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `True` | `{agencyid}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `GeneralTransitFeed.Kafka` | `KAFKA` | topic `gtfs`; key `{agencyid}` |

#### Message `GeneralTransitFeedStatic.Shapes`
<a id="message-generaltransitfeedstaticshapes"></a>

| Field | Value |
| --- | --- |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/GeneralTransitFeedStatic.jstruct/schemas/GeneralTransitFeedStatic.Shapes`](#schema-generaltransitfeedstaticshapes) |
| Transport override | `None` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.Shapes` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `True` | `{agencyid}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `GeneralTransitFeed.Kafka` | `KAFKA` | topic `gtfs`; key `{agencyid}` |

#### Message `GeneralTransitFeedStatic.StopAreas`
<a id="message-generaltransitfeedstaticstopareas"></a>

| Field | Value |
| --- | --- |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/GeneralTransitFeedStatic.jstruct/schemas/GeneralTransitFeedStatic.StopAreas`](#schema-generaltransitfeedstaticstopareas) |
| Transport override | `None` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.StopAreas` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `True` | `{agencyid}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `GeneralTransitFeed.Kafka` | `KAFKA` | topic `gtfs`; key `{agencyid}` |

#### Message `GeneralTransitFeedStatic.Stops`
<a id="message-generaltransitfeedstaticstops"></a>

| Field | Value |
| --- | --- |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/GeneralTransitFeedStatic.jstruct/schemas/GeneralTransitFeedStatic.Stops`](#schema-generaltransitfeedstaticstops) |
| Transport override | `None` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.Stops` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `True` | `{agencyid}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `GeneralTransitFeed.Kafka` | `KAFKA` | topic `gtfs`; key `{agencyid}` |

#### Message `GeneralTransitFeedStatic.StopTimes`
<a id="message-generaltransitfeedstaticstoptimes"></a>

| Field | Value |
| --- | --- |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/GeneralTransitFeedStatic.jstruct/schemas/GeneralTransitFeedStatic.StopTimes`](#schema-generaltransitfeedstaticstoptimes) |
| Transport override | `None` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.StopTimes` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `True` | `{agencyid}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `GeneralTransitFeed.Kafka` | `KAFKA` | topic `gtfs`; key `{agencyid}` |

#### Message `GeneralTransitFeedStatic.Timeframes`
<a id="message-generaltransitfeedstatictimeframes"></a>

| Field | Value |
| --- | --- |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/GeneralTransitFeedStatic.jstruct/schemas/GeneralTransitFeedStatic.Timeframes`](#schema-generaltransitfeedstatictimeframes) |
| Transport override | `None` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.Timeframes` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `True` | `{agencyid}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `GeneralTransitFeed.Kafka` | `KAFKA` | topic `gtfs`; key `{agencyid}` |

#### Message `GeneralTransitFeedStatic.Transfers`
<a id="message-generaltransitfeedstatictransfers"></a>

| Field | Value |
| --- | --- |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/GeneralTransitFeedStatic.jstruct/schemas/GeneralTransitFeedStatic.Transfers`](#schema-generaltransitfeedstatictransfers) |
| Transport override | `None` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.Transfers` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `True` | `{agencyid}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `GeneralTransitFeed.Kafka` | `KAFKA` | topic `gtfs`; key `{agencyid}` |

#### Message `GeneralTransitFeedStatic.Translations`
<a id="message-generaltransitfeedstatictranslations"></a>

| Field | Value |
| --- | --- |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/GeneralTransitFeedStatic.jstruct/schemas/GeneralTransitFeedStatic.Translations`](#schema-generaltransitfeedstatictranslations) |
| Transport override | `None` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.Translations` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `True` | `{agencyid}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `GeneralTransitFeed.Kafka` | `KAFKA` | topic `gtfs`; key `{agencyid}` |

#### Message `GeneralTransitFeedStatic.Trips`
<a id="message-generaltransitfeedstatictrips"></a>

| Field | Value |
| --- | --- |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/GeneralTransitFeedStatic.jstruct/schemas/GeneralTransitFeedStatic.Trips`](#schema-generaltransitfeedstatictrips) |
| Transport override | `None` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `GeneralTransitFeedStatic.Trips` |
| `source` | Source Feed URL | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Provider name | `uritemplate` | `True` | `{agencyid}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `GeneralTransitFeed.Kafka` | `KAFKA` | topic `gtfs`; key `{agencyid}` |

## Schemagroups

### Schemagroup `GeneralTransitFeedRealTime.jstruct`
<a id="schemagroup-generaltransitfeedrealtimejstruct"></a>

#### Schema `GeneralTransitFeedRealTime.Vehicle.VehiclePosition`
<a id="schema-generaltransitfeedrealtimevehiclevehicleposition"></a>

| Field | Value |
| --- | --- |
| Name | VehiclePosition |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/GeneralTransitFeedRealTime/Vehicle/VehiclePosition` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/GeneralTransitFeedRealTime/Vehicle/VehiclePosition` |
| Type | `object` |

###### Object `VehiclePosition`
<a id="schema-node-vehicleposition"></a>

Realtime positioning information for a given vehicle.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `trip` | `schema` | `False` | The Trip that this vehicle is serving. Can be empty or partial if the vehicle can not be identified with a given trip instance. | - | - | - |
| `vehicle` | `schema` | `False` | Additional information on the vehicle that is serving this trip. | - | - | - |
| `position` | `schema` | `False` | Current position of this vehicle. The stop sequence index of the current stop. The meaning of | - | - | - |
| `current_stop_sequence` | `int32` | `False` | current_stop_sequence (i.e., the stop that it refers to) is determined by current_status. If current_status is missing IN_TRANSIT_TO is assumed. Identifies the current stop. The value must be the same as in stops.txt in | - | - | - |
| `stop_id` | `string` | `False` | the corresponding GTFS feed. | - | - | - |
| `current_status` | `schema` | `False` | The exact status of the vehicle with respect to the current stop. Ignored if current_stop_sequence is missing. Moment at which the vehicle's position was measured. In POSIX time | - | - | - |
| `timestamp` | `int64` | `False` | (i.e., number of seconds since January 1st 1970 00:00:00 UTC). | - | - | - |
| `congestion_level` | `schema` | `False` |  | - | - | - |
| `occupancy_status` | `schema` | `False` |  | - | - | - |

#### Schema `GeneralTransitFeedRealTime.Trip.TripUpdate`
<a id="schema-generaltransitfeedrealtimetriptripupdate"></a>

| Field | Value |
| --- | --- |
| Name | TripUpdate |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/GeneralTransitFeedRealTime/Trip/TripUpdate` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/GeneralTransitFeedRealTime/Trip/TripUpdate` |
| Type | `object` |

###### Object `TripUpdate`
<a id="schema-node-tripupdate"></a>

Entities used in the feed. Realtime update of the progress of a vehicle along a trip. Depending on the value of ScheduleRelationship, a TripUpdate can specify: - A trip that proceeds along the schedule. - A trip that proceeds along a route but has no fixed schedule. - A trip that have been added or removed with regard to schedule. The updates can be for future, predicted arrival/departure events, or for past events that already occurred. Normally, updates should get more precise and more certain (see uncertainty below) as the events gets closer to current time. Even if that is not possible, the information for past events should be precise and certain. In particular, if an update points to time in the past but its update's uncertainty is not 0, the client should conclude that the update is a (wrong) prediction and that the trip has not completed yet. Note that the update can describe a trip that is already completed. To this end, it is enough to provide an update for the last stop of the trip. If the time of that is in the past, the client will conclude from that that the whole trip is in the past (it is possible, although inconsequential, to also provide updates for preceding stops). This option is most relevant for a trip that has completed ahead of schedule, but according to the schedule, the trip is still proceeding at the current time. Removing the updates for this trip could make the client assume that the trip is still proceeding. Note that the feed provider is allowed, but not required, to purge past updates - this is one case where this would be practically useful.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `trip` | `schema` | `True` | The Trip that this message applies to. There can be at most one TripUpdate entity for each actual trip instance. If there is none, that means there is no prediction information available. It does *not* mean that the trip is progressing according to schedule. | - | - | - |
| `vehicle` | `schema` | `False` | Additional information on the vehicle that is serving this trip. | - | - | - |
| `stop_time_update` | array of [`StopTimeUpdate`](#schema-node-stoptimeupdate) | `True` | Updates to StopTimes for the trip (both future, i.e., predictions, and in some cases, past ones, i.e., those that already happened). The updates must be sorted by stop_sequence, and apply for all the following stops of the trip up to the next specified one. Example 1: For a trip with 20 stops, a StopTimeUpdate with arrival delay and departure delay of 0 for stop_sequence of the current stop means that the trip is exactly on time. Example 2: For the same trip instance, 3 StopTimeUpdates are provided: - delay of 5 min for stop_sequence 3 - delay of 1 min for stop_sequence 8 - delay of unspecified duration for stop_sequence 10 This will be interpreted as: - stop_sequences 3,4,5,6,7 have delay of 5 min. - stop_sequences 8,9 have delay of 1 min. - stop_sequences 10,... have unknown delay. Moment at which the vehicle's real-time progress was measured. In POSIX | - | - | - |
| `timestamp` | `int64` | `False` | time (i.e., the number of seconds since January 1st 1970 00:00:00 UTC). The current schedule deviation for the trip.  Delay should only be | - | - | - |
| `delay` | `int32` | `False` | specified when the prediction is given relative to some existing schedule in GTFS. Delay (in seconds) can be positive (meaning that the vehicle is late) or negative (meaning that the vehicle is ahead of schedule). Delay of 0 means that the vehicle is exactly on time. Delay information in StopTimeUpdates take precedent of trip-level delay information, such that trip-level delay is only propagated until the next stop along the trip with a StopTimeUpdate delay value specified. Feed providers are strongly encouraged to provide a TripUpdate.timestamp value indicating when the delay value was last updated, in order to evaluate the freshness of the data. NOTE: This field is still experimental, and subject to change. It may be formally adopted in the future. | - | - | - |

###### Object `StopTimeUpdate`
<a id="schema-node-stoptimeupdate"></a>

Realtime update for arrival and/or departure events for a given stop on a trip. Updates can be supplied for both past and future events. The producer is allowed, although not required, to drop past events.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `stop_sequence` | `int32` | `False` | The update is linked to a specific stop either through stop_sequence or stop_id, so one of the fields below must necessarily be set. See the documentation in TripDescriptor for more information. Must be the same as in stop_times.txt in the corresponding GTFS feed. | - | - | - |
| `stop_id` | `string` | `False` | Must be the same as in stops.txt in the corresponding GTFS feed. | - | - | - |
| `arrival` | `schema` | `False` |  | - | - | - |
| `departure` | `schema` | `False` |  | - | - | - |
| `schedule_relationship` | `schema` | `False` |  | - | - | - |

#### Schema `GeneralTransitFeedRealTime.Alert.Alert`
<a id="schema-generaltransitfeedrealtimealertalert"></a>

| Field | Value |
| --- | --- |
| Name | Alert |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/GeneralTransitFeedRealTime/Alert/Alert` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/GeneralTransitFeedRealTime/Alert/Alert` |
| Type | `object` |

###### Object `Alert`
<a id="schema-node-alert"></a>

An alert, indicating some sort of incident in the public transit network.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `active_period` | array of [`TimeRange`](#schema-node-timerange) | `True` | Time when the alert should be shown to the user. If missing, the alert will be shown as long as it appears in the feed. If multiple ranges are given, the alert will be shown during all of them. | - | - | - |
| `informed_entity` | array of [`EntitySelector`](#schema-node-entityselector) | `True` | Entities whose users we should notify of this alert. | - | - | - |
| `cause` | `schema` | `False` |  | - | - | - |
| `effect` | `schema` | `False` |  | - | - | - |
| `url` | `schema` | `False` | The URL which provides additional information about the alert. | - | - | - |
| `header_text` | `schema` | `False` | Alert header. Contains a short summary of the alert text as plain-text. Full description for the alert as plain-text. The information in the | - | - | - |
| `description_text` | `schema` | `False` | description should add to the information of the header. | - | - | - |

###### Object `TimeRange`
<a id="schema-node-timerange"></a>

Low level data structures used above. A time interval. The interval is considered active at time 't' if 't' is greater than or equal to the start time and less than the end time.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `start` | `int64` | `False` | Start time, in POSIX time (i.e., number of seconds since January 1st 1970 00:00:00 UTC). If missing, the interval starts at minus infinity. | - | - | - |
| `end` | `int64` | `False` | End time, in POSIX time (i.e., number of seconds since January 1st 1970 00:00:00 UTC). If missing, the interval ends at plus infinity. | - | - | - |

###### Object `EntitySelector`
<a id="schema-node-entityselector"></a>

A selector for an entity in a GTFS feed.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `agency_id` | `string` | `False` | The values of the fields should correspond to the appropriate fields in the GTFS feed. At least one specifier must be given. If several are given, then the matching has to apply to all the given specifiers. | - | - | - |
| `route_id` | `string` | `False` |  | - | - | - |
| `route_type` | `int32` | `False` | corresponds to route_type in GTFS. | - | - | - |
| `trip` | `schema` | `False` |  | - | - | - |
| `stop_id` | `string` | `False` |  | - | - | - |

### Schemagroup `GeneralTransitFeedRealTime.avro`
<a id="schemagroup-generaltransitfeedrealtimeavro"></a>

#### Schema `GeneralTransitFeedRealTime.Vehicle.VehiclePosition`
<a id="schema-generaltransitfeedrealtimevehiclevehicleposition"></a>

| Field | Value |
| --- | --- |
| Format | Avro |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro |

###### Avro

| Field | Value |
| --- | --- |
| Name | VehiclePosition |
| Namespace | GeneralTransitFeedRealTime.Vehicle |
| Type | `record` |
| Doc | Realtime positioning information for a given vehicle. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `trip` | `null` \| record `TripDescriptor` | The Trip that this vehicle is serving. Can be empty or partial if the vehicle can not be identified with a given trip instance. | `-` |
| `vehicle` | `null` \| record `VehicleDescriptor` | Additional information on the vehicle that is serving this trip. | `-` |
| `position` | `null` \| record `Position` | Current position of this vehicle. The stop sequence index of the current stop. The meaning of | `-` |
| `current_stop_sequence` | `null` \| `int` | current_stop_sequence (i.e., the stop that it refers to) is determined by current_status. If current_status is missing IN_TRANSIT_TO is assumed. Identifies the current stop. The value must be the same as in stops.txt in | `-` |
| `stop_id` | `null` \| `string` | the corresponding GTFS feed. | `-` |
| `current_status` | `null` \| enum `VehicleStopStatus` | The exact status of the vehicle with respect to the current stop. Ignored if current_stop_sequence is missing. Moment at which the vehicle's position was measured. In POSIX time | `-` |
| `timestamp` | `null` \| `long` | (i.e., number of seconds since January 1st 1970 00:00:00 UTC). | `-` |
| `congestion_level` | `null` \| enum `CongestionLevel` |  | `-` |
| `occupancy_status` | `null` \| enum `OccupancyStatus` |  | `-` |

#### Schema `GeneralTransitFeedRealTime.Trip.TripUpdate`
<a id="schema-generaltransitfeedrealtimetriptripupdate"></a>

| Field | Value |
| --- | --- |
| Format | Avro |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro |

###### Avro

| Field | Value |
| --- | --- |
| Name | TripUpdate |
| Namespace | GeneralTransitFeedRealTime.Trip |
| Type | `record` |
| Doc | Entities used in the feed. Realtime update of the progress of a vehicle along a trip. Depending on the value of ScheduleRelationship, a TripUpdate can specify: - A trip that proceeds along the schedule. - A trip that proceeds along a route but has no fixed schedule. - A trip that have been added or removed with regard to schedule. The updates can be for future, predicted arrival/departure events, or for past events that already occurred. Normally, updates should get more precise and more certain (see uncertainty below) as the events gets closer to current time. Even if that is not possible, the information for past events should be precise and certain. In particular, if an update points to time in the past but its update's uncertainty is not 0, the client should conclude that the update is a (wrong) prediction and that the trip has not completed yet. Note that the update can describe a trip that is already completed. To this end, it is enough to provide an update for the last stop of the trip. If the time of that is in the past, the client will conclude from that that the whole trip is in the past (it is possible, although inconsequential, to also provide updates for preceding stops). This option is most relevant for a trip that has completed ahead of schedule, but according to the schedule, the trip is still proceeding at the current time. Removing the updates for this trip could make the client assume that the trip is still proceeding. Note that the feed provider is allowed, but not required, to purge past updates - this is one case where this would be practically useful. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `trip` | record `TripDescriptor` | The Trip that this message applies to. There can be at most one TripUpdate entity for each actual trip instance. If there is none, that means there is no prediction information available. It does *not* mean that the trip is progressing according to schedule. | `-` |
| `vehicle` | `null` \| record `VehicleDescriptor` | Additional information on the vehicle that is serving this trip. | `-` |
| `stop_time_update` | array of record `StopTimeUpdate` | Updates to StopTimes for the trip (both future, i.e., predictions, and in some cases, past ones, i.e., those that already happened). The updates must be sorted by stop_sequence, and apply for all the following stops of the trip up to the next specified one. Example 1: For a trip with 20 stops, a StopTimeUpdate with arrival delay and departure delay of 0 for stop_sequence of the current stop means that the trip is exactly on time. Example 2: For the same trip instance, 3 StopTimeUpdates are provided: - delay of 5 min for stop_sequence 3 - delay of 1 min for stop_sequence 8 - delay of unspecified duration for stop_sequence 10 This will be interpreted as: - stop_sequences 3,4,5,6,7 have delay of 5 min. - stop_sequences 8,9 have delay of 1 min. - stop_sequences 10,... have unknown delay. Moment at which the vehicle's real-time progress was measured. In POSIX | `-` |
| `timestamp` | `null` \| `long` | time (i.e., the number of seconds since January 1st 1970 00:00:00 UTC). The current schedule deviation for the trip.  Delay should only be | `-` |
| `delay` | `null` \| `int` | specified when the prediction is given relative to some existing schedule in GTFS. Delay (in seconds) can be positive (meaning that the vehicle is late) or negative (meaning that the vehicle is ahead of schedule). Delay of 0 means that the vehicle is exactly on time. Delay information in StopTimeUpdates take precedent of trip-level delay information, such that trip-level delay is only propagated until the next stop along the trip with a StopTimeUpdate delay value specified. Feed providers are strongly encouraged to provide a TripUpdate.timestamp value indicating when the delay value was last updated, in order to evaluate the freshness of the data. NOTE: This field is still experimental, and subject to change. It may be formally adopted in the future. | `-` |

#### Schema `GeneralTransitFeedRealTime.Alert.Alert`
<a id="schema-generaltransitfeedrealtimealertalert"></a>

| Field | Value |
| --- | --- |
| Format | Avro |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro |

###### Avro

| Field | Value |
| --- | --- |
| Name | Alert |
| Namespace | GeneralTransitFeedRealTime.Alert |
| Type | `record` |
| Doc | An alert, indicating some sort of incident in the public transit network. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `active_period` | array of record `TimeRange` | Time when the alert should be shown to the user. If missing, the alert will be shown as long as it appears in the feed. If multiple ranges are given, the alert will be shown during all of them. | `-` |
| `informed_entity` | array of record `EntitySelector` | Entities whose users we should notify of this alert. | `-` |
| `cause` | `null` \| enum `Cause` |  | `-` |
| `effect` | `null` \| enum `Effect` |  | `-` |
| `url` | `null` \| record `TranslatedString` | The URL which provides additional information about the alert. | `-` |
| `header_text` | `null` \| `GeneralTransitFeedRealTime.Alert.TranslatedString` | Alert header. Contains a short summary of the alert text as plain-text. Full description for the alert as plain-text. The information in the | `-` |
| `description_text` | `null` \| `GeneralTransitFeedRealTime.Alert.TranslatedString` | description should add to the information of the header. | `-` |

### Schemagroup `GeneralTransitFeedStatic.jstruct`
<a id="schemagroup-generaltransitfeedstaticjstruct"></a>

#### Schema `GeneralTransitFeedStatic.Agency`
<a id="schema-generaltransitfeedstaticagency"></a>

| Field | Value |
| --- | --- |
| Name | Agency |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/GeneralTransitFeedStatic/Agency` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/GeneralTransitFeedStatic/Agency` |
| Type | `object` |

###### Object `Agency`
<a id="schema-node-agency"></a>

Information about the transit agencies.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `agencyId` | `string` | `True` | Identifies a transit brand which is often synonymous with a transit agency. | - | - | - |
| `agencyName` | `string` | `True` | Full name of the transit agency. | - | - | - |
| `agencyUrl` | `string` | `True` | URL of the transit agency. | - | - | - |
| `agencyTimezone` | `string` | `True` | Timezone where the transit agency is located. | - | - | - |
| `agencyLang` | `string` | `False` | Primary language used by this transit agency. | - | default=`-` | default=`-` |
| `agencyPhone` | `string` | `False` | A voice telephone number for the specified agency. | - | default=`-` | default=`-` |
| `agencyFareUrl` | `string` | `False` | URL of a web page that allows a rider to purchase tickets or other fare instruments for that agency online. | - | default=`-` | default=`-` |
| `agencyEmail` | `string` | `False` | Email address actively monitored by the agency’s customer service department. | - | default=`-` | default=`-` |

#### Schema `GeneralTransitFeedStatic.Areas`
<a id="schema-generaltransitfeedstaticareas"></a>

| Field | Value |
| --- | --- |
| Name | Areas |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/GeneralTransitFeedStatic/Areas` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/GeneralTransitFeedStatic/Areas` |
| Type | `object` |

###### Object `Areas`
<a id="schema-node-areas"></a>

Defines areas.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `areaId` | `string` | `True` | Identifies an area. | - | - | - |
| `areaName` | `string` | `True` | Name of the area. | - | - | - |
| `areaDesc` | `string` | `False` | Description of the area. | - | default=`-` | default=`-` |
| `areaUrl` | `string` | `False` | URL of a web page about the area. | - | default=`-` | default=`-` |

#### Schema `GeneralTransitFeedStatic.Attributions`
<a id="schema-generaltransitfeedstaticattributions"></a>

| Field | Value |
| --- | --- |
| Name | Attributions |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/GeneralTransitFeedStatic/Attributions` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/GeneralTransitFeedStatic/Attributions` |
| Type | `object` |

###### Object `Attributions`
<a id="schema-node-attributions"></a>

Provides information about the attributions.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `attributionId` | `string` | `False` | Identifies an attribution for the dataset. | - | default=`-` | default=`-` |
| `agencyId` | `string` | `False` | Identifies the agency associated with the attribution. | - | default=`-` | default=`-` |
| `routeId` | `string` | `False` | Identifies the route associated with the attribution. | - | default=`-` | default=`-` |
| `tripId` | `string` | `False` | Identifies the trip associated with the attribution. | - | default=`-` | default=`-` |
| `organizationName` | `string` | `True` | Name of the organization associated with the attribution. | - | - | - |
| `isProducer` | `int32` | `False` | Indicates if the organization is a producer. | - | default=`-` | default=`-` |
| `isOperator` | `int32` | `False` | Indicates if the organization is an operator. | - | default=`-` | default=`-` |
| `isAuthority` | `int32` | `False` | Indicates if the organization is an authority. | - | default=`-` | default=`-` |
| `attributionUrl` | `string` | `False` | URL of a web page about the attribution. | - | default=`-` | default=`-` |
| `attributionEmail` | `string` | `False` | Email address associated with the attribution. | - | default=`-` | default=`-` |
| `attributionPhone` | `string` | `False` | Phone number associated with the attribution. | - | default=`-` | default=`-` |

#### Schema `GeneralTransitFeed.BookingRules`
<a id="schema-generaltransitfeedbookingrules"></a>

| Field | Value |
| --- | --- |
| Name | BookingRules |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/GeneralTransitFeedStatic/BookingRules` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/GeneralTransitFeedStatic/BookingRules` |
| Type | `object` |

###### Object `BookingRules`
<a id="schema-node-bookingrules"></a>

Defines booking rules.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `bookingRuleId` | `string` | `True` | Identifies a booking rule. | - | - | - |
| `bookingRuleName` | `string` | `True` | Name of the booking rule. | - | - | - |
| `bookingRuleDesc` | `string` | `False` | Description of the booking rule. | - | default=`-` | default=`-` |
| `bookingRuleUrl` | `string` | `False` | URL of a web page about the booking rule. | - | default=`-` | default=`-` |

#### Schema `GeneralTransitFeedStatic.FareAttributes`
<a id="schema-generaltransitfeedstaticfareattributes"></a>

| Field | Value |
| --- | --- |
| Name | FareAttributes |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/GeneralTransitFeedStatic/FareAttributes` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/GeneralTransitFeedStatic/FareAttributes` |
| Type | `object` |

###### Object `FareAttributes`
<a id="schema-node-fareattributes"></a>

Defines fare attributes.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `fareId` | `string` | `True` | Identifies a fare class. | - | - | - |
| `price` | `double` | `True` | Fare price, in the unit specified by currency_type. | - | - | - |
| `currencyType` | `string` | `True` | Currency type used to pay the fare. | - | - | - |
| `paymentMethod` | `int32` | `True` | When 0, fare must be paid on board. When 1, fare must be paid before boarding. | - | - | - |
| `transfers` | `int32` | `False` | Specifies the number of transfers permitted on this fare. | - | default=`-` | default=`-` |
| `agencyId` | `string` | `False` | Identifies the agency for the specified fare. | - | default=`-` | default=`-` |
| `transferDuration` | `int64` | `False` | Length of time in seconds before a transfer expires. | - | default=`-` | default=`-` |

#### Schema `GeneralTransitFeedStatic.FareLegRules`
<a id="schema-generaltransitfeedstaticfarelegrules"></a>

| Field | Value |
| --- | --- |
| Name | FareLegRules |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/GeneralTransitFeedStatic/FareLegRules` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/GeneralTransitFeedStatic/FareLegRules` |
| Type | `object` |

###### Object `FareLegRules`
<a id="schema-node-farelegrules"></a>

Defines fare leg rules.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `fareLegRuleId` | `string` | `True` | Identifies a fare leg rule. | - | - | - |
| `fareProductId` | `string` | `True` | Identifies a fare product. | - | - | - |
| `legGroupId` | `string` | `False` | Identifies a group of legs. | - | default=`-` | default=`-` |
| `networkId` | `string` | `False` | Identifies a network. | - | default=`-` | default=`-` |
| `fromAreaId` | `string` | `False` | Identifies the origin area. | - | default=`-` | default=`-` |
| `toAreaId` | `string` | `False` | Identifies the destination area. | - | default=`-` | default=`-` |

#### Schema `GeneralTransitFeedStatic.FareMedia`
<a id="schema-generaltransitfeedstaticfaremedia"></a>

| Field | Value |
| --- | --- |
| Name | FareMedia |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/GeneralTransitFeedStatic/FareMedia` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/GeneralTransitFeedStatic/FareMedia` |
| Type | `object` |

###### Object `FareMedia`
<a id="schema-node-faremedia"></a>

Defines fare media.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `fareMediaId` | `string` | `True` | Identifies a fare media. | - | - | - |
| `fareMediaName` | `string` | `True` | Name of the fare media. | - | - | - |
| `fareMediaDesc` | `string` | `False` | Description of the fare media. | - | default=`-` | default=`-` |
| `fareMediaUrl` | `string` | `False` | URL of a web page about the fare media. | - | default=`-` | default=`-` |

#### Schema `GeneralTransitFeedStatic.FareProducts`
<a id="schema-generaltransitfeedstaticfareproducts"></a>

| Field | Value |
| --- | --- |
| Name | FareProducts |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/GeneralTransitFeedStatic/FareProducts` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/GeneralTransitFeedStatic/FareProducts` |
| Type | `object` |

###### Object `FareProducts`
<a id="schema-node-fareproducts"></a>

Defines fare products.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `fareProductId` | `string` | `True` | Identifies a fare product. | - | - | - |
| `fareProductName` | `string` | `True` | Name of the fare product. | - | - | - |
| `fareProductDesc` | `string` | `False` | Description of the fare product. | - | default=`-` | default=`-` |
| `fareProductUrl` | `string` | `False` | URL of a web page about the fare product. | - | default=`-` | default=`-` |

#### Schema `GeneralTransitFeedStatic.FareRules`
<a id="schema-generaltransitfeedstaticfarerules"></a>

| Field | Value |
| --- | --- |
| Name | FareRules |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/GeneralTransitFeedStatic/FareRules` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/GeneralTransitFeedStatic/FareRules` |
| Type | `object` |

###### Object `FareRules`
<a id="schema-node-farerules"></a>

Defines fare rules.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `fareId` | `string` | `True` | Identifies a fare class. | - | - | - |
| `routeId` | `string` | `False` | Identifies a route associated with the fare. | - | default=`-` | default=`-` |
| `originId` | `string` | `False` | Identifies the fare zone of the origin. | - | default=`-` | default=`-` |
| `destinationId` | `string` | `False` | Identifies the fare zone of the destination. | - | default=`-` | default=`-` |
| `containsId` | `string` | `False` | Identifies the fare zone that a rider will enter or leave. | - | default=`-` | default=`-` |

#### Schema `GeneralTransitFeedStatic.FareTransferRules`
<a id="schema-generaltransitfeedstaticfaretransferrules"></a>

| Field | Value |
| --- | --- |
| Name | FareTransferRules |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/GeneralTransitFeedStatic/FareTransferRules` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/GeneralTransitFeedStatic/FareTransferRules` |
| Type | `object` |

###### Object `FareTransferRules`
<a id="schema-node-faretransferrules"></a>

Defines fare transfer rules.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `fareTransferRuleId` | `string` | `True` | Identifies a fare transfer rule. | - | - | - |
| `fareProductId` | `string` | `True` | Identifies a fare product. | - | - | - |
| `transferCount` | `int32` | `False` | Number of transfers permitted. | - | default=`-` | default=`-` |
| `fromLegGroupId` | `string` | `False` | Identifies the leg group from which the transfer starts. | - | default=`-` | default=`-` |
| `toLegGroupId` | `string` | `False` | Identifies the leg group to which the transfer applies. | - | default=`-` | default=`-` |
| `duration` | `int64` | `False` | Length of time in seconds before a transfer expires. | - | default=`-` | default=`-` |
| `durationType` | `string` | `False` | Type of duration for the transfer. | - | default=`-` | default=`-` |

#### Schema `GeneralTransitFeedStatic.FeedInfo`
<a id="schema-generaltransitfeedstaticfeedinfo"></a>

| Field | Value |
| --- | --- |
| Name | FeedInfo |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/GeneralTransitFeedStatic/FeedInfo` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/GeneralTransitFeedStatic/FeedInfo` |
| Type | `object` |

###### Object `FeedInfo`
<a id="schema-node-feedinfo"></a>

Provides information about the GTFS feed itself.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `feedPublisherName` | `string` | `True` | Full name of the organization that publishes the feed. | - | - | - |
| `feedPublisherUrl` | `string` | `True` | URL of the feed publishing organization's website. | - | - | - |
| `feedLang` | `string` | `True` | Default language for the text in this feed. | - | - | - |
| `defaultLang` | `string` | `False` | Specifies the language used when the data consumer doesn’t know the language of the user. | - | default=`-` | default=`-` |
| `feedStartDate` | `string` | `False` | The start date for the dataset. | - | default=`-` | default=`-` |
| `feedEndDate` | `string` | `False` | The end date for the dataset. | - | default=`-` | default=`-` |
| `feedVersion` | `string` | `False` | Version string that indicates the current version of their GTFS dataset. | - | default=`-` | default=`-` |
| `feedContactEmail` | `string` | `False` | Email address for communication with the data publisher. | - | default=`-` | default=`-` |
| `feedContactUrl` | `string` | `False` | URL for a web page that allows a feed consumer to contact the data publisher. | - | default=`-` | default=`-` |

#### Schema `GeneralTransitFeedStatic.Frequencies`
<a id="schema-generaltransitfeedstaticfrequencies"></a>

| Field | Value |
| --- | --- |
| Name | Frequencies |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/GeneralTransitFeedStatic/Frequencies` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/GeneralTransitFeedStatic/Frequencies` |
| Type | `object` |

###### Object `Frequencies`
<a id="schema-node-frequencies"></a>

Defines frequencies.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `tripId` | `string` | `True` | Identifies a trip. | - | - | - |
| `startTime` | `string` | `True` | Time at which service begins with the specified frequency. | - | - | - |
| `endTime` | `string` | `True` | Time at which service ends with the specified frequency. | - | - | - |
| `headwaySecs` | `int32` | `True` | Time between departures from the same stop (headway) for this trip, in seconds. | - | - | - |
| `exactTimes` | `int32` | `False` | When 1, frequency-based trips should be exactly scheduled. When 0 (or empty), frequency-based trips are not exactly scheduled. | - | default=`-` | default=`-` |

#### Schema `GeneralTransitFeedStatic.Levels`
<a id="schema-generaltransitfeedstaticlevels"></a>

| Field | Value |
| --- | --- |
| Name | Levels |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/GeneralTransitFeedStatic/Levels` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/GeneralTransitFeedStatic/Levels` |
| Type | `object` |

###### Object `Levels`
<a id="schema-node-levels"></a>

Defines levels.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `levelId` | `string` | `True` | Identifies a level. | - | - | - |
| `levelIndex` | `double` | `True` | Numeric index of the level that indicates relative position of the level in relation to other levels. | - | - | - |
| `levelName` | `string` | `False` | Name of the level. | - | default=`-` | default=`-` |

#### Schema `GeneralTransitFeedStatic.LocationGeoJson`
<a id="schema-generaltransitfeedstaticlocationgeojson"></a>

| Field | Value |
| --- | --- |
| Name | LocationGeoJson |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/GeneralTransitFeedStatic/LocationGeoJson` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/GeneralTransitFeedStatic/LocationGeoJson` |
| Type | `object` |

###### Object `LocationGeoJson`
<a id="schema-node-locationgeojson"></a>

Defines location GeoJSON data.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `locationGeoJsonId` | `string` | `True` | Identifies a location GeoJSON. | - | - | - |
| `locationGeoJsonType` | `string` | `True` | Type of the GeoJSON. | - | - | - |
| `locationGeoJsonData` | `string` | `True` | GeoJSON data. | - | - | - |

#### Schema `GeneralTransitFeedStatic.LocationGroups`
<a id="schema-generaltransitfeedstaticlocationgroups"></a>

| Field | Value |
| --- | --- |
| Name | LocationGroups |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/GeneralTransitFeedStatic/LocationGroups` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/GeneralTransitFeedStatic/LocationGroups` |
| Type | `object` |

###### Object `LocationGroups`
<a id="schema-node-locationgroups"></a>

Defines location groups.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `locationGroupId` | `string` | `True` | Identifies a location group. | - | - | - |
| `locationGroupName` | `string` | `True` | Name of the location group. | - | - | - |
| `locationGroupDesc` | `string` | `False` | Description of the location group. | - | default=`-` | default=`-` |
| `locationGroupUrl` | `string` | `False` | URL of a web page about the location group. | - | default=`-` | default=`-` |

#### Schema `GeneralTransitFeedStatic.LocationGroupStores`
<a id="schema-generaltransitfeedstaticlocationgroupstores"></a>

| Field | Value |
| --- | --- |
| Name | LocationGroupStores |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/GeneralTransitFeedStatic/LocationGroupStores` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/GeneralTransitFeedStatic/LocationGroupStores` |
| Type | `object` |

###### Object `LocationGroupStores`
<a id="schema-node-locationgroupstores"></a>

Defines location group stores.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `locationGroupStoreId` | `string` | `True` | Identifies a location group store. | - | - | - |
| `locationGroupId` | `string` | `True` | Identifies a location group. | - | - | - |
| `storeId` | `string` | `True` | Identifies a store. | - | - | - |

#### Schema `GeneralTransitFeedStatic.Networks`
<a id="schema-generaltransitfeedstaticnetworks"></a>

| Field | Value |
| --- | --- |
| Name | Networks |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/GeneralTransitFeedStatic/Networks` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/GeneralTransitFeedStatic/Networks` |
| Type | `object` |

###### Object `Networks`
<a id="schema-node-networks"></a>

Defines networks.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `networkId` | `string` | `True` | Identifies a network. | - | - | - |
| `networkName` | `string` | `True` | Name of the network. | - | - | - |
| `networkDesc` | `string` | `False` | Description of the network. | - | default=`-` | default=`-` |
| `networkUrl` | `string` | `False` | URL of a web page about the network. | - | default=`-` | default=`-` |

#### Schema `GeneralTransitFeedStatic.Pathways`
<a id="schema-generaltransitfeedstaticpathways"></a>

| Field | Value |
| --- | --- |
| Name | Pathways |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/GeneralTransitFeedStatic/Pathways` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/GeneralTransitFeedStatic/Pathways` |
| Type | `object` |

###### Object `Pathways`
<a id="schema-node-pathways"></a>

Defines pathways.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `pathwayId` | `string` | `True` | Identifies a pathway. | - | - | - |
| `fromStopId` | `string` | `True` | Identifies a stop or station where the pathway begins. | - | - | - |
| `toStopId` | `string` | `True` | Identifies a stop or station where the pathway ends. | - | - | - |
| `pathwayMode` | `int32` | `True` | Type of pathway between the specified (from_stop_id, to_stop_id) pair. | - | - | - |
| `isBidirectional` | `int32` | `True` | When 1, the pathway can be used in both directions. When 0, the pathway can only be used from (from_stop_id) to (to_stop_id). | - | - | - |
| `length` | `double` | `False` | Length of the pathway, in meters. | - | default=`-` | default=`-` |
| `traversalTime` | `int32` | `False` | Average time, in seconds, needed to walk through the pathway. | - | default=`-` | default=`-` |
| `stairCount` | `int32` | `False` | Number of stairs of the pathway. | - | default=`-` | default=`-` |
| `maxSlope` | `double` | `False` | Maximum slope of the pathway, in percent. | - | default=`-` | default=`-` |
| `minWidth` | `double` | `False` | Minimum width of the pathway, in meters. | - | default=`-` | default=`-` |
| `signpostedAs` | `string` | `False` | Signposting information for the pathway. | - | default=`-` | default=`-` |
| `reversedSignpostedAs` | `string` | `False` | Reversed signposting information for the pathway. | - | default=`-` | default=`-` |

#### Schema `GeneralTransitFeedStatic.RouteNetworks`
<a id="schema-generaltransitfeedstaticroutenetworks"></a>

| Field | Value |
| --- | --- |
| Name | RouteNetworks |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/GeneralTransitFeedStatic/RouteNetworks` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/GeneralTransitFeedStatic/RouteNetworks` |
| Type | `object` |

###### Object `RouteNetworks`
<a id="schema-node-routenetworks"></a>

Defines route networks.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `routeNetworkId` | `string` | `True` | Identifies a route network. | - | - | - |
| `routeId` | `string` | `True` | Identifies a route. | - | - | - |
| `networkId` | `string` | `True` | Identifies a network. | - | - | - |

#### Schema `GeneralTransitFeedStatic.Routes`
<a id="schema-generaltransitfeedstaticroutes"></a>

| Field | Value |
| --- | --- |
| Name | Routes |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/GeneralTransitFeedStatic/Routes` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/GeneralTransitFeedStatic/Routes` |
| Type | `object` |

###### Object `Routes`
<a id="schema-node-routes"></a>

Identifies a route.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `routeId` | `string` | `True` | Identifies a route. | - | - | - |
| `agencyId` | `string` | `False` | Agency for the specified route. | - | default=`-` | default=`-` |
| `routeShortName` | `string` | `False` | Short name of a route. | - | default=`-` | default=`-` |
| `routeLongName` | `string` | `False` | Full name of a route. | - | default=`-` | default=`-` |
| `routeDesc` | `string` | `False` | Description of a route that provides useful, quality information. | - | default=`-` | default=`-` |
| `routeType` | `schema` | `True` | Indicates the type of transportation used on a route. | - | - | - |
| `routeUrl` | `string` | `False` | URL of a web page about the particular route. | - | default=`-` | default=`-` |
| `routeColor` | `string` | `False` | Route color designation that matches public facing material. | - | default=`-` | default=`-` |
| `routeTextColor` | `string` | `False` | Legible color to use for text drawn against a background of route_color. | - | default=`-` | default=`-` |
| `routeSortOrder` | `int32` | `False` | Orders the routes in a way which is ideal for presentation to customers. | - | default=`-` | default=`-` |
| `continuousPickup` | `schema` | `True` | Indicates that the rider can board the transit vehicle at any point along the vehicle’s travel path. | - | - | - |
| `continuousDropOff` | `schema` | `True` | Indicates that the rider can alight from the transit vehicle at any point along the vehicle’s travel path. | - | - | - |
| `networkId` | `string` | `False` | Identifies a group of routes. | - | default=`-` | default=`-` |

#### Schema `GeneralTransitFeedStatic.Shapes`
<a id="schema-generaltransitfeedstaticshapes"></a>

| Field | Value |
| --- | --- |
| Name | Shapes |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/GeneralTransitFeedStatic/Shapes` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/GeneralTransitFeedStatic/Shapes` |
| Type | `object` |

###### Object `Shapes`
<a id="schema-node-shapes"></a>

Defines shapes.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `shapeId` | `string` | `True` | Identifies a shape. | - | - | - |
| `shapePtLat` | `double` | `True` | Latitude of a shape point. | - | - | - |
| `shapePtLon` | `double` | `True` | Longitude of a shape point. | - | - | - |
| `shapePtSequence` | `int32` | `True` | Sequence in which the shape points connect to form the shape. | - | - | - |
| `shapeDistTraveled` | `double` | `False` | Actual distance traveled along the shape from the first shape point to the specified shape point. | - | default=`-` | default=`-` |

#### Schema `GeneralTransitFeedStatic.StopAreas`
<a id="schema-generaltransitfeedstaticstopareas"></a>

| Field | Value |
| --- | --- |
| Name | StopAreas |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/GeneralTransitFeedStatic/StopAreas` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/GeneralTransitFeedStatic/StopAreas` |
| Type | `object` |

###### Object `StopAreas`
<a id="schema-node-stopareas"></a>

Defines stop areas.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `stopAreaId` | `string` | `True` | Identifies a stop area. | - | - | - |
| `stopId` | `string` | `True` | Identifies a stop. | - | - | - |
| `areaId` | `string` | `True` | Identifies an area. | - | - | - |

#### Schema `GeneralTransitFeedStatic.Stops`
<a id="schema-generaltransitfeedstaticstops"></a>

| Field | Value |
| --- | --- |
| Name | Stops |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/GeneralTransitFeedStatic/Stops` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/GeneralTransitFeedStatic/Stops` |
| Type | `object` |

###### Object `Stops`
<a id="schema-node-stops"></a>

Identifies locations such as stop/platform, station, entrance/exit, generic node or boarding area.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `stopId` | `string` | `True` | Identifies a location: stop/platform, station, entrance/exit, generic node or boarding area. | - | - | - |
| `stopCode` | `string` | `False` | Short text or a number that identifies the location for riders. | - | default=`-` | default=`-` |
| `stopName` | `string` | `False` | Name of the location. | - | default=`-` | default=`-` |
| `ttsStopName` | `string` | `False` | Readable version of the stop_name. | - | default=`-` | default=`-` |
| `stopDesc` | `string` | `False` | Description of the location that provides useful, quality information. | - | default=`-` | default=`-` |
| `stopLat` | `double` | `False` | Latitude of the location. | - | default=`-` | default=`-` |
| `stopLon` | `double` | `False` | Longitude of the location. | - | default=`-` | default=`-` |
| `zoneId` | `string` | `False` | Identifies the fare zone for a stop. | - | default=`-` | default=`-` |
| `stopUrl` | `string` | `False` | URL of a web page about the location. | - | default=`-` | default=`-` |
| `locationType` | `schema` | `True` | Location type. | - | - | - |
| `parentStation` | `string` | `False` | Defines hierarchy between the different locations. | - | default=`-` | default=`-` |
| `stopTimezone` | `string` | `False` | Timezone of the location. | - | default=`-` | default=`-` |
| `wheelchairBoarding` | `schema` | `True` | Indicates whether wheelchair boardings are possible from the location. | - | - | - |
| `levelId` | `string` | `False` | Level of the location. | - | default=`-` | default=`-` |
| `platformCode` | `string` | `False` | Platform identifier for a platform stop. | - | default=`-` | default=`-` |

#### Schema `GeneralTransitFeedStatic.StopTimes`
<a id="schema-generaltransitfeedstaticstoptimes"></a>

| Field | Value |
| --- | --- |
| Name | StopTimes |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/GeneralTransitFeedStatic/StopTimes` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/GeneralTransitFeedStatic/StopTimes` |
| Type | `object` |

###### Object `StopTimes`
<a id="schema-node-stoptimes"></a>

Represents times that a vehicle arrives at and departs from individual stops for each trip.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `tripId` | `string` | `True` | Identifies a trip. | - | - | - |
| `arrivalTime` | `string` | `False` | Arrival time at the stop for a specific trip. | - | default=`-` | default=`-` |
| `departureTime` | `string` | `False` | Departure time from the stop for a specific trip. | - | default=`-` | default=`-` |
| `stopId` | `string` | `False` | Identifies the serviced stop. | - | default=`-` | default=`-` |
| `stopSequence` | `int32` | `True` | Order of stops for a particular trip. | - | - | - |
| `stopHeadsign` | `string` | `False` | Text that appears on signage identifying the trip's destination to riders. | - | default=`-` | default=`-` |
| `pickupType` | `schema` | `True` | Indicates pickup method. | - | - | - |
| `dropOffType` | `schema` | `True` | Indicates drop off method. | - | - | - |
| `continuousPickup` | `schema` | `False` | Indicates continuous stopping pickup. | - | default=`-` | default=`-` |
| `continuousDropOff` | `schema` | `False` | Indicates continuous stopping drop off. | - | default=`-` | default=`-` |
| `shapeDistTraveled` | `double` | `False` | Actual distance traveled along the shape from the first stop to the stop specified in this record. | - | default=`-` | default=`-` |
| `timepoint` | `schema` | `True` | Indicates if arrival and departure times for a stop are strictly adhered to by the vehicle or if they are instead approximate and/or interpolated times. | - | - | - |

#### Schema `GeneralTransitFeedStatic.Timeframes`
<a id="schema-generaltransitfeedstatictimeframes"></a>

| Field | Value |
| --- | --- |
| Name | Timeframes |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/GeneralTransitFeedStatic/Timeframes` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/GeneralTransitFeedStatic/Timeframes` |
| Type | `object` |

###### Object `Timeframes`
<a id="schema-node-timeframes"></a>

Used to describe fares that can vary based on the time of day, the day of the week, or a particular day in the year.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `timeframeGroupId` | `string` | `True` | Identifies a timeframe or set of timeframes. | - | - | - |
| `startTime` | `string` | `False` | Defines the beginning of a timeframe. | - | default=`-` | default=`-` |
| `endTime` | `string` | `False` | Defines the end of a timeframe. | - | default=`-` | default=`-` |
| `serviceDates` | `choice` | `True` | Identifies a set of dates when service is available for one or more routes. | - | - | - |

#### Schema `GeneralTransitFeedStatic.Transfers`
<a id="schema-generaltransitfeedstatictransfers"></a>

| Field | Value |
| --- | --- |
| Name | Transfers |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/GeneralTransitFeedStatic/Transfers` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/GeneralTransitFeedStatic/Transfers` |
| Type | `object` |

###### Object `Transfers`
<a id="schema-node-transfers"></a>

Defines transfers.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `fromStopId` | `string` | `True` | Identifies a stop or station where a connection between routes begins. | - | - | - |
| `toStopId` | `string` | `True` | Identifies a stop or station where a connection between routes ends. | - | - | - |
| `transferType` | `int32` | `True` | Type of connection for the specified (from_stop_id, to_stop_id) pair. | - | - | - |
| `minTransferTime` | `int32` | `False` | Amount of time, in seconds, needed to transfer from the specified (from_stop_id) to the specified (to_stop_id). | - | default=`-` | default=`-` |

#### Schema `GeneralTransitFeedStatic.Translations`
<a id="schema-generaltransitfeedstatictranslations"></a>

| Field | Value |
| --- | --- |
| Name | Translations |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/GeneralTransitFeedStatic/Translations` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/GeneralTransitFeedStatic/Translations` |
| Type | `object` |

###### Object `Translations`
<a id="schema-node-translations"></a>

Defines translations.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `tableName` | `string` | `True` | Name of the table containing the field to be translated. | - | - | - |
| `fieldName` | `string` | `True` | Name of the field to be translated. | - | - | - |
| `language` | `string` | `True` | Language of the translation. | - | - | - |
| `translation` | `string` | `True` | Translated value. | - | - | - |

#### Schema `GeneralTransitFeedStatic.Trips`
<a id="schema-generaltransitfeedstatictrips"></a>

| Field | Value |
| --- | --- |
| Name | Trips |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/GeneralTransitFeedStatic/Trips` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/GeneralTransitFeedStatic/Trips` |
| Type | `object` |

###### Object `Trips`
<a id="schema-node-trips"></a>

Identifies a trip.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `routeId` | `string` | `True` | Identifies a route. | - | - | - |
| `serviceDates` | `schema` | `True` |  | - | - | - |
| `serviceExceptions` | array of [`CalendarDates`](#schema-node-calendardates) | `True` |  | - | - | - |
| `tripId` | `string` | `True` | Identifies a trip. | - | - | - |
| `tripHeadsign` | `string` | `False` | Text that appears on signage identifying the trip's destination to riders. | - | default=`-` | default=`-` |
| `tripShortName` | `string` | `False` | Public facing text used to identify the trip to riders. | - | default=`-` | default=`-` |
| `directionId` | `schema` | `True` | Indicates the direction of travel for a trip. | - | - | - |
| `blockId` | `string` | `False` | Identifies the block to which the trip belongs. | - | default=`-` | default=`-` |
| `shapeId` | `string` | `False` | Identifies a geospatial shape describing the vehicle travel path for a trip. | - | default=`-` | default=`-` |
| `wheelchairAccessible` | `schema` | `True` | Indicates wheelchair accessibility. | - | - | - |
| `bikesAllowed` | `schema` | `True` | Indicates whether bikes are allowed. | - | - | - |

###### Object `CalendarDates`
<a id="schema-node-calendardates"></a>

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `serviceId` | `string` | `True` | Identifies a set of dates when a service exception occurs for one or more routes. | - | - | - |
| `date` | `string` | `True` | Date when service exception occurs. | - | - | - |
| `exceptionType` | `schema` | `True` | Indicates whether service is available on the date specified. | - | - | - |

### Schemagroup `GeneralTransitFeedStatic.avro`
<a id="schemagroup-generaltransitfeedstaticavro"></a>

#### Schema `GeneralTransitFeedStatic.Agency`
<a id="schema-generaltransitfeedstaticagency"></a>

| Field | Value |
| --- | --- |
| Format | Avro |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro |

###### Avro

| Field | Value |
| --- | --- |
| Name | Agency |
| Namespace | GeneralTransitFeedStatic |
| Type | `record` |
| Doc | Information about the transit agencies. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `agencyId` | `string` | Identifies a transit brand which is often synonymous with a transit agency. | `-` |
| `agencyName` | `string` | Full name of the transit agency. | `-` |
| `agencyUrl` | `string` | URL of the transit agency. | `-` |
| `agencyTimezone` | `string` | Timezone where the transit agency is located. | `-` |
| `agencyLang` | `null` \| `string` | Primary language used by this transit agency. | `-` |
| `agencyPhone` | `null` \| `string` | A voice telephone number for the specified agency. | `-` |
| `agencyFareUrl` | `null` \| `string` | URL of a web page that allows a rider to purchase tickets or other fare instruments for that agency online. | `-` |
| `agencyEmail` | `null` \| `string` | Email address actively monitored by the agency’s customer service department. | `-` |

#### Schema `GeneralTransitFeedStatic.Areas`
<a id="schema-generaltransitfeedstaticareas"></a>

| Field | Value |
| --- | --- |
| Format | Avro |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro |

###### Avro

| Field | Value |
| --- | --- |
| Name | Areas |
| Namespace | GeneralTransitFeedStatic |
| Type | `record` |
| Doc | Defines areas. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `areaId` | `string` | Identifies an area. | `-` |
| `areaName` | `string` | Name of the area. | `-` |
| `areaDesc` | `null` \| `string` | Description of the area. | `-` |
| `areaUrl` | `null` \| `string` | URL of a web page about the area. | `-` |

#### Schema `GeneralTransitFeedStatic.Attributions`
<a id="schema-generaltransitfeedstaticattributions"></a>

| Field | Value |
| --- | --- |
| Format | Avro |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro |

###### Avro

| Field | Value |
| --- | --- |
| Name | Attributions |
| Namespace | GeneralTransitFeedStatic |
| Type | `record` |
| Doc | Provides information about the attributions. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `attributionId` | `null` \| `string` | Identifies an attribution for the dataset. | `-` |
| `agencyId` | `null` \| `string` | Identifies the agency associated with the attribution. | `-` |
| `routeId` | `null` \| `string` | Identifies the route associated with the attribution. | `-` |
| `tripId` | `null` \| `string` | Identifies the trip associated with the attribution. | `-` |
| `organizationName` | `string` | Name of the organization associated with the attribution. | `-` |
| `isProducer` | `null` \| `int` | Indicates if the organization is a producer. | `-` |
| `isOperator` | `null` \| `int` | Indicates if the organization is an operator. | `-` |
| `isAuthority` | `null` \| `int` | Indicates if the organization is an authority. | `-` |
| `attributionUrl` | `null` \| `string` | URL of a web page about the attribution. | `-` |
| `attributionEmail` | `null` \| `string` | Email address associated with the attribution. | `-` |
| `attributionPhone` | `null` \| `string` | Phone number associated with the attribution. | `-` |

#### Schema `GeneralTransitFeed.BookingRules`
<a id="schema-generaltransitfeedbookingrules"></a>

| Field | Value |
| --- | --- |
| Format | Avro |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro |

###### Avro

| Field | Value |
| --- | --- |
| Name | BookingRules |
| Namespace | GeneralTransitFeedStatic |
| Type | `record` |
| Doc | Defines booking rules. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `bookingRuleId` | `string` | Identifies a booking rule. | `-` |
| `bookingRuleName` | `string` | Name of the booking rule. | `-` |
| `bookingRuleDesc` | `null` \| `string` | Description of the booking rule. | `-` |
| `bookingRuleUrl` | `null` \| `string` | URL of a web page about the booking rule. | `-` |

#### Schema `GeneralTransitFeedStatic.FareAttributes`
<a id="schema-generaltransitfeedstaticfareattributes"></a>

| Field | Value |
| --- | --- |
| Format | Avro |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro |

###### Avro

| Field | Value |
| --- | --- |
| Name | FareAttributes |
| Namespace | GeneralTransitFeedStatic |
| Type | `record` |
| Doc | Defines fare attributes. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `fareId` | `string` | Identifies a fare class. | `-` |
| `price` | `double` | Fare price, in the unit specified by currency_type. | `-` |
| `currencyType` | `string` | Currency type used to pay the fare. | `-` |
| `paymentMethod` | `int` | When 0, fare must be paid on board. When 1, fare must be paid before boarding. | `-` |
| `transfers` | `null` \| `int` | Specifies the number of transfers permitted on this fare. | `-` |
| `agencyId` | `null` \| `string` | Identifies the agency for the specified fare. | `-` |
| `transferDuration` | `null` \| `long` | Length of time in seconds before a transfer expires. | `-` |

#### Schema `GeneralTransitFeedStatic.FareLegRules`
<a id="schema-generaltransitfeedstaticfarelegrules"></a>

| Field | Value |
| --- | --- |
| Format | Avro |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro |

###### Avro

| Field | Value |
| --- | --- |
| Name | FareLegRules |
| Namespace | GeneralTransitFeedStatic |
| Type | `record` |
| Doc | Defines fare leg rules. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `fareLegRuleId` | `string` | Identifies a fare leg rule. | `-` |
| `fareProductId` | `string` | Identifies a fare product. | `-` |
| `legGroupId` | `null` \| `string` | Identifies a group of legs. | `-` |
| `networkId` | `null` \| `string` | Identifies a network. | `-` |
| `fromAreaId` | `null` \| `string` | Identifies the origin area. | `-` |
| `toAreaId` | `null` \| `string` | Identifies the destination area. | `-` |

#### Schema `GeneralTransitFeedStatic.FareMedia`
<a id="schema-generaltransitfeedstaticfaremedia"></a>

| Field | Value |
| --- | --- |
| Format | Avro |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro |

###### Avro

| Field | Value |
| --- | --- |
| Name | FareMedia |
| Namespace | GeneralTransitFeedStatic |
| Type | `record` |
| Doc | Defines fare media. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `fareMediaId` | `string` | Identifies a fare media. | `-` |
| `fareMediaName` | `string` | Name of the fare media. | `-` |
| `fareMediaDesc` | `null` \| `string` | Description of the fare media. | `-` |
| `fareMediaUrl` | `null` \| `string` | URL of a web page about the fare media. | `-` |

#### Schema `GeneralTransitFeedStatic.FareProducts`
<a id="schema-generaltransitfeedstaticfareproducts"></a>

| Field | Value |
| --- | --- |
| Format | Avro |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro |

###### Avro

| Field | Value |
| --- | --- |
| Name | FareProducts |
| Namespace | GeneralTransitFeedStatic |
| Type | `record` |
| Doc | Defines fare products. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `fareProductId` | `string` | Identifies a fare product. | `-` |
| `fareProductName` | `string` | Name of the fare product. | `-` |
| `fareProductDesc` | `null` \| `string` | Description of the fare product. | `-` |
| `fareProductUrl` | `null` \| `string` | URL of a web page about the fare product. | `-` |

#### Schema `GeneralTransitFeedStatic.FareRules`
<a id="schema-generaltransitfeedstaticfarerules"></a>

| Field | Value |
| --- | --- |
| Format | Avro |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro |

###### Avro

| Field | Value |
| --- | --- |
| Name | FareRules |
| Namespace | GeneralTransitFeedStatic |
| Type | `record` |
| Doc | Defines fare rules. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `fareId` | `string` | Identifies a fare class. | `-` |
| `routeId` | `null` \| `string` | Identifies a route associated with the fare. | `-` |
| `originId` | `null` \| `string` | Identifies the fare zone of the origin. | `-` |
| `destinationId` | `null` \| `string` | Identifies the fare zone of the destination. | `-` |
| `containsId` | `null` \| `string` | Identifies the fare zone that a rider will enter or leave. | `-` |

#### Schema `GeneralTransitFeedStatic.FareTransferRules`
<a id="schema-generaltransitfeedstaticfaretransferrules"></a>

| Field | Value |
| --- | --- |
| Format | Avro |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro |

###### Avro

| Field | Value |
| --- | --- |
| Name | FareTransferRules |
| Namespace | GeneralTransitFeedStatic |
| Type | `record` |
| Doc | Defines fare transfer rules. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `fareTransferRuleId` | `string` | Identifies a fare transfer rule. | `-` |
| `fareProductId` | `string` | Identifies a fare product. | `-` |
| `transferCount` | `null` \| `int` | Number of transfers permitted. | `-` |
| `fromLegGroupId` | `null` \| `string` | Identifies the leg group from which the transfer starts. | `-` |
| `toLegGroupId` | `null` \| `string` | Identifies the leg group to which the transfer applies. | `-` |
| `duration` | `null` \| `long` | Length of time in seconds before a transfer expires. | `-` |
| `durationType` | `null` \| `string` | Type of duration for the transfer. | `-` |

#### Schema `GeneralTransitFeedStatic.FeedInfo`
<a id="schema-generaltransitfeedstaticfeedinfo"></a>

| Field | Value |
| --- | --- |
| Format | Avro |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro |

###### Avro

| Field | Value |
| --- | --- |
| Name | FeedInfo |
| Namespace | GeneralTransitFeedStatic |
| Type | `record` |
| Doc | Provides information about the GTFS feed itself. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `feedPublisherName` | `string` | Full name of the organization that publishes the feed. | `-` |
| `feedPublisherUrl` | `string` | URL of the feed publishing organization's website. | `-` |
| `feedLang` | `string` | Default language for the text in this feed. | `-` |
| `defaultLang` | `null` \| `string` | Specifies the language used when the data consumer doesn’t know the language of the user. | `-` |
| `feedStartDate` | `null` \| `string` | The start date for the dataset. | `-` |
| `feedEndDate` | `null` \| `string` | The end date for the dataset. | `-` |
| `feedVersion` | `null` \| `string` | Version string that indicates the current version of their GTFS dataset. | `-` |
| `feedContactEmail` | `null` \| `string` | Email address for communication with the data publisher. | `-` |
| `feedContactUrl` | `null` \| `string` | URL for a web page that allows a feed consumer to contact the data publisher. | `-` |

#### Schema `GeneralTransitFeedStatic.Frequencies`
<a id="schema-generaltransitfeedstaticfrequencies"></a>

| Field | Value |
| --- | --- |
| Format | Avro |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro |

###### Avro

| Field | Value |
| --- | --- |
| Name | Frequencies |
| Namespace | GeneralTransitFeedStatic |
| Type | `record` |
| Doc | Defines frequencies. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `tripId` | `string` | Identifies a trip. | `-` |
| `startTime` | `string` | Time at which service begins with the specified frequency. | `-` |
| `endTime` | `string` | Time at which service ends with the specified frequency. | `-` |
| `headwaySecs` | `int` | Time between departures from the same stop (headway) for this trip, in seconds. | `-` |
| `exactTimes` | `null` \| `int` | When 1, frequency-based trips should be exactly scheduled. When 0 (or empty), frequency-based trips are not exactly scheduled. | `-` |

#### Schema `GeneralTransitFeedStatic.Levels`
<a id="schema-generaltransitfeedstaticlevels"></a>

| Field | Value |
| --- | --- |
| Format | Avro |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro |

###### Avro

| Field | Value |
| --- | --- |
| Name | Levels |
| Namespace | GeneralTransitFeedStatic |
| Type | `record` |
| Doc | Defines levels. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `levelId` | `string` | Identifies a level. | `-` |
| `levelIndex` | `double` | Numeric index of the level that indicates relative position of the level in relation to other levels. | `-` |
| `levelName` | `null` \| `string` | Name of the level. | `-` |

#### Schema `GeneralTransitFeedStatic.LocationGeoJson`
<a id="schema-generaltransitfeedstaticlocationgeojson"></a>

| Field | Value |
| --- | --- |
| Format | Avro |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro |

###### Avro

| Field | Value |
| --- | --- |
| Name | LocationGeoJson |
| Namespace | GeneralTransitFeedStatic |
| Type | `record` |
| Doc | Defines location GeoJSON data. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `locationGeoJsonId` | `string` | Identifies a location GeoJSON. | `-` |
| `locationGeoJsonType` | `string` | Type of the GeoJSON. | `-` |
| `locationGeoJsonData` | `string` | GeoJSON data. | `-` |

#### Schema `GeneralTransitFeedStatic.LocationGroups`
<a id="schema-generaltransitfeedstaticlocationgroups"></a>

| Field | Value |
| --- | --- |
| Format | Avro |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro |

###### Avro

| Field | Value |
| --- | --- |
| Name | LocationGroups |
| Namespace | GeneralTransitFeedStatic |
| Type | `record` |
| Doc | Defines location groups. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `locationGroupId` | `string` | Identifies a location group. | `-` |
| `locationGroupName` | `string` | Name of the location group. | `-` |
| `locationGroupDesc` | `null` \| `string` | Description of the location group. | `-` |
| `locationGroupUrl` | `null` \| `string` | URL of a web page about the location group. | `-` |

#### Schema `GeneralTransitFeedStatic.LocationGroupStores`
<a id="schema-generaltransitfeedstaticlocationgroupstores"></a>

| Field | Value |
| --- | --- |
| Format | Avro |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro |

###### Avro

| Field | Value |
| --- | --- |
| Name | LocationGroupStores |
| Namespace | GeneralTransitFeedStatic |
| Type | `record` |
| Doc | Defines location group stores. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `locationGroupStoreId` | `string` | Identifies a location group store. | `-` |
| `locationGroupId` | `string` | Identifies a location group. | `-` |
| `storeId` | `string` | Identifies a store. | `-` |

#### Schema `GeneralTransitFeedStatic.Networks`
<a id="schema-generaltransitfeedstaticnetworks"></a>

| Field | Value |
| --- | --- |
| Format | Avro |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro |

###### Avro

| Field | Value |
| --- | --- |
| Name | Networks |
| Namespace | GeneralTransitFeedStatic |
| Type | `record` |
| Doc | Defines networks. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `networkId` | `string` | Identifies a network. | `-` |
| `networkName` | `string` | Name of the network. | `-` |
| `networkDesc` | `null` \| `string` | Description of the network. | `-` |
| `networkUrl` | `null` \| `string` | URL of a web page about the network. | `-` |

#### Schema `GeneralTransitFeedStatic.Pathways`
<a id="schema-generaltransitfeedstaticpathways"></a>

| Field | Value |
| --- | --- |
| Format | Avro |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro |

###### Avro

| Field | Value |
| --- | --- |
| Name | Pathways |
| Namespace | GeneralTransitFeedStatic |
| Type | `record` |
| Doc | Defines pathways. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `pathwayId` | `string` | Identifies a pathway. | `-` |
| `fromStopId` | `string` | Identifies a stop or station where the pathway begins. | `-` |
| `toStopId` | `string` | Identifies a stop or station where the pathway ends. | `-` |
| `pathwayMode` | `int` | Type of pathway between the specified (from_stop_id, to_stop_id) pair. | `-` |
| `isBidirectional` | `int` | When 1, the pathway can be used in both directions. When 0, the pathway can only be used from (from_stop_id) to (to_stop_id). | `-` |
| `length` | `null` \| `double` | Length of the pathway, in meters. | `-` |
| `traversalTime` | `null` \| `int` | Average time, in seconds, needed to walk through the pathway. | `-` |
| `stairCount` | `null` \| `int` | Number of stairs of the pathway. | `-` |
| `maxSlope` | `null` \| `double` | Maximum slope of the pathway, in percent. | `-` |
| `minWidth` | `null` \| `double` | Minimum width of the pathway, in meters. | `-` |
| `signpostedAs` | `null` \| `string` | Signposting information for the pathway. | `-` |
| `reversedSignpostedAs` | `null` \| `string` | Reversed signposting information for the pathway. | `-` |

#### Schema `GeneralTransitFeedStatic.RouteNetworks`
<a id="schema-generaltransitfeedstaticroutenetworks"></a>

| Field | Value |
| --- | --- |
| Format | Avro |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro |

###### Avro

| Field | Value |
| --- | --- |
| Name | RouteNetworks |
| Namespace | GeneralTransitFeedStatic |
| Type | `record` |
| Doc | Defines route networks. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `routeNetworkId` | `string` | Identifies a route network. | `-` |
| `routeId` | `string` | Identifies a route. | `-` |
| `networkId` | `string` | Identifies a network. | `-` |

#### Schema `GeneralTransitFeedStatic.Routes`
<a id="schema-generaltransitfeedstaticroutes"></a>

| Field | Value |
| --- | --- |
| Format | Avro |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro |

###### Avro

| Field | Value |
| --- | --- |
| Name | Routes |
| Namespace | GeneralTransitFeedStatic |
| Type | `record` |
| Doc | Identifies a route. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `routeId` | `string` | Identifies a route. | `-` |
| `agencyId` | `null` \| `string` | Agency for the specified route. | `-` |
| `routeShortName` | `null` \| `string` | Short name of a route. | `-` |
| `routeLongName` | `null` \| `string` | Full name of a route. | `-` |
| `routeDesc` | `null` \| `string` | Description of a route that provides useful, quality information. | `-` |
| `routeType` | enum `RouteType` | Indicates the type of transportation used on a route. | `-` |
| `routeUrl` | `null` \| `string` | URL of a web page about the particular route. | `-` |
| `routeColor` | `null` \| `string` | Route color designation that matches public facing material. | `-` |
| `routeTextColor` | `null` \| `string` | Legible color to use for text drawn against a background of route_color. | `-` |
| `routeSortOrder` | `null` \| `int` | Orders the routes in a way which is ideal for presentation to customers. | `-` |
| `continuousPickup` | enum `ContinuousPickup` | Indicates that the rider can board the transit vehicle at any point along the vehicle’s travel path. | `-` |
| `continuousDropOff` | enum `ContinuousDropOff` | Indicates that the rider can alight from the transit vehicle at any point along the vehicle’s travel path. | `-` |
| `networkId` | `null` \| `string` | Identifies a group of routes. | `-` |

#### Schema `GeneralTransitFeedStatic.Shapes`
<a id="schema-generaltransitfeedstaticshapes"></a>

| Field | Value |
| --- | --- |
| Format | Avro |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro |

###### Avro

| Field | Value |
| --- | --- |
| Name | Shapes |
| Namespace | GeneralTransitFeedStatic |
| Type | `record` |
| Doc | Defines shapes. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `shapeId` | `string` | Identifies a shape. | `-` |
| `shapePtLat` | `double` | Latitude of a shape point. | `-` |
| `shapePtLon` | `double` | Longitude of a shape point. | `-` |
| `shapePtSequence` | `int` | Sequence in which the shape points connect to form the shape. | `-` |
| `shapeDistTraveled` | `null` \| `double` | Actual distance traveled along the shape from the first shape point to the specified shape point. | `-` |

#### Schema `GeneralTransitFeedStatic.StopAreas`
<a id="schema-generaltransitfeedstaticstopareas"></a>

| Field | Value |
| --- | --- |
| Format | Avro |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro |

###### Avro

| Field | Value |
| --- | --- |
| Name | StopAreas |
| Namespace | GeneralTransitFeedStatic |
| Type | `record` |
| Doc | Defines stop areas. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `stopAreaId` | `string` | Identifies a stop area. | `-` |
| `stopId` | `string` | Identifies a stop. | `-` |
| `areaId` | `string` | Identifies an area. | `-` |

#### Schema `GeneralTransitFeedStatic.Stops`
<a id="schema-generaltransitfeedstaticstops"></a>

| Field | Value |
| --- | --- |
| Format | Avro |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro |

###### Avro

| Field | Value |
| --- | --- |
| Name | Stops |
| Namespace | GeneralTransitFeedStatic |
| Type | `record` |
| Doc | Identifies locations such as stop/platform, station, entrance/exit, generic node or boarding area. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `stopId` | `string` | Identifies a location: stop/platform, station, entrance/exit, generic node or boarding area. | `-` |
| `stopCode` | `null` \| `string` | Short text or a number that identifies the location for riders. | `-` |
| `stopName` | `null` \| `string` | Name of the location. | `-` |
| `ttsStopName` | `null` \| `string` | Readable version of the stop_name. | `-` |
| `stopDesc` | `null` \| `string` | Description of the location that provides useful, quality information. | `-` |
| `stopLat` | `null` \| `double` | Latitude of the location. | `-` |
| `stopLon` | `null` \| `double` | Longitude of the location. | `-` |
| `zoneId` | `null` \| `string` | Identifies the fare zone for a stop. | `-` |
| `stopUrl` | `null` \| `string` | URL of a web page about the location. | `-` |
| `locationType` | enum `LocationType` | Location type. | `-` |
| `parentStation` | `null` \| `string` | Defines hierarchy between the different locations. | `-` |
| `stopTimezone` | `null` \| `string` | Timezone of the location. | `-` |
| `wheelchairBoarding` | enum `WheelchairBoarding` | Indicates whether wheelchair boardings are possible from the location. | `-` |
| `levelId` | `null` \| `string` | Level of the location. | `-` |
| `platformCode` | `null` \| `string` | Platform identifier for a platform stop. | `-` |

#### Schema `GeneralTransitFeedStatic.StopTimes`
<a id="schema-generaltransitfeedstaticstoptimes"></a>

| Field | Value |
| --- | --- |
| Format | Avro |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro |

###### Avro

| Field | Value |
| --- | --- |
| Name | StopTimes |
| Namespace | GeneralTransitFeedStatic |
| Type | `record` |
| Doc | Represents times that a vehicle arrives at and departs from individual stops for each trip. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `tripId` | `string` | Identifies a trip. | `-` |
| `arrivalTime` | `null` \| `string` | Arrival time at the stop for a specific trip. | `-` |
| `departureTime` | `null` \| `string` | Departure time from the stop for a specific trip. | `-` |
| `stopId` | `null` \| `string` | Identifies the serviced stop. | `-` |
| `stopSequence` | `int` | Order of stops for a particular trip. | `-` |
| `stopHeadsign` | `null` \| `string` | Text that appears on signage identifying the trip's destination to riders. | `-` |
| `pickupType` | enum `PickupType` | Indicates pickup method. | `-` |
| `dropOffType` | enum `DropOffType` | Indicates drop off method. | `-` |
| `continuousPickup` | `null` \| enum `ContinuousPickup` | Indicates continuous stopping pickup. | `-` |
| `continuousDropOff` | `null` \| enum `ContinuousDropOff` | Indicates continuous stopping drop off. | `-` |
| `shapeDistTraveled` | `null` \| `double` | Actual distance traveled along the shape from the first stop to the stop specified in this record. | `-` |
| `timepoint` | enum `Timepoint` | Indicates if arrival and departure times for a stop are strictly adhered to by the vehicle or if they are instead approximate and/or interpolated times. | `-` |

#### Schema `GeneralTransitFeedStatic.Timeframes`
<a id="schema-generaltransitfeedstatictimeframes"></a>

| Field | Value |
| --- | --- |
| Format | Avro |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro |

###### Avro

| Field | Value |
| --- | --- |
| Name | Timeframes |
| Namespace | GeneralTransitFeedStatic |
| Type | `record` |
| Doc | Used to describe fares that can vary based on the time of day, the day of the week, or a particular day in the year. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `timeframeGroupId` | `string` | Identifies a timeframe or set of timeframes. | `-` |
| `startTime` | `null` \| `string` | Defines the beginning of a timeframe. | `-` |
| `endTime` | `null` \| `string` | Defines the end of a timeframe. | `-` |
| `serviceDates` | record `Calendar` \| record `CalendarDates` | Identifies a set of dates when service is available for one or more routes. | `-` |

#### Schema `GeneralTransitFeedStatic.Transfers`
<a id="schema-generaltransitfeedstatictransfers"></a>

| Field | Value |
| --- | --- |
| Format | Avro |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro |

###### Avro

| Field | Value |
| --- | --- |
| Name | Transfers |
| Namespace | GeneralTransitFeedStatic |
| Type | `record` |
| Doc | Defines transfers. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `fromStopId` | `string` | Identifies a stop or station where a connection between routes begins. | `-` |
| `toStopId` | `string` | Identifies a stop or station where a connection between routes ends. | `-` |
| `transferType` | `int` | Type of connection for the specified (from_stop_id, to_stop_id) pair. | `-` |
| `minTransferTime` | `null` \| `int` | Amount of time, in seconds, needed to transfer from the specified (from_stop_id) to the specified (to_stop_id). | `-` |

#### Schema `GeneralTransitFeedStatic.Translations`
<a id="schema-generaltransitfeedstatictranslations"></a>

| Field | Value |
| --- | --- |
| Format | Avro |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro |

###### Avro

| Field | Value |
| --- | --- |
| Name | Translations |
| Namespace | GeneralTransitFeedStatic |
| Type | `record` |
| Doc | Defines translations. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `tableName` | `string` | Name of the table containing the field to be translated. | `-` |
| `fieldName` | `string` | Name of the field to be translated. | `-` |
| `language` | `string` | Language of the translation. | `-` |
| `translation` | `string` | Translated value. | `-` |

#### Schema `GeneralTransitFeedStatic.Trips`
<a id="schema-generaltransitfeedstatictrips"></a>

| Field | Value |
| --- | --- |
| Format | Avro |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro |

###### Avro

| Field | Value |
| --- | --- |
| Name | Trips |
| Namespace | GeneralTransitFeedStatic |
| Type | `record` |
| Doc | Identifies a trip. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `routeId` | `string` | Identifies a route. | `-` |
| `serviceDates` | record `Calendar` |  | `-` |
| `serviceExceptions` | array of record `CalendarDates` |  | `-` |
| `tripId` | `string` | Identifies a trip. | `-` |
| `tripHeadsign` | `null` \| `string` | Text that appears on signage identifying the trip's destination to riders. | `-` |
| `tripShortName` | `null` \| `string` | Public facing text used to identify the trip to riders. | `-` |
| `directionId` | enum `DirectionId` | Indicates the direction of travel for a trip. | `-` |
| `blockId` | `null` \| `string` | Identifies the block to which the trip belongs. | `-` |
| `shapeId` | `null` \| `string` | Identifies a geospatial shape describing the vehicle travel path for a trip. | `-` |
| `wheelchairAccessible` | enum `WheelchairAccessible` | Indicates wheelchair accessibility. | `-` |
| `bikesAllowed` | enum `BikesAllowed` | Indicates whether bikes are allowed. | `-` |
