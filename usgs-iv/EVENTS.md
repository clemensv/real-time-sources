# USGS Water Services - Instantaneous Value Service Usage Guide Events

MQTT/5.0 transport variants for USGS site metadata. Topics are retained QoS-1 site info leaves under hydro/us/usgs/usgs-iv/{site_no}/info. The manifest intentionally uses existing schema field names site_no and parameter_cd rather than adding aliases.

## Table of Contents

- [Registry](#registry)
- [Endpoints](#endpoints)
- [Messagegroups](#messagegroups)
- [Schemagroups](#schemagroups)

---

## Registry

| Field | Value |
| --- | --- |
| Endpoints | 3 |
| Messagegroups | 6 |
| Schemagroups | 4 |

## Endpoints

### Endpoint `USGS.Sites.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`USGS.Sites`](#messagegroup-usgssites) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `usgs-iv` |
| Kafka key | `{agency_cd}/{site_no}` |
| Deployed | False |

### Endpoint `USGS.Timeseries.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`USGS.SiteTimeseries`](#messagegroup-usgssitetimeseries), [`USGS.InstantaneousValues`](#messagegroup-usgsinstantaneousvalues) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `usgs-iv` |
| Kafka key | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| Deployed | False |

### Endpoint `USGS.IV.Mqtt`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `MQTT/5.0` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"mode": "binary"}` |
| Messagegroups | [`USGS.Sites.mqtt`](#messagegroup-usgssitesmqtt), [`USGS.SiteTimeseries.mqtt`](#messagegroup-usgssitetimeseriesmqtt), [`USGS.InstantaneousValues.mqtt`](#messagegroup-usgsinstantaneousvaluesmqtt) |

#### Transport options

| Option | Value |
| --- | --- |
| Deployed | False |
| Broker endpoints | `[{"uri": "mqtt://localhost:1883"}]` |

## Messagegroups

### Messagegroup `USGS.Sites`
<a id="messagegroup-usgssites"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `USGS.Sites.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `USGS.Sites.Site`
<a id="message-usgssitessite"></a>

USGS site metadata.

| Field | Value |
| --- | --- |
| Name | Site |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.Sites.jstruct/schemas/USGS.Sites.Site`](#schema-usgssitessite) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.Sites.Site` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.Sites.Kafka` | `KAFKA` | topic `usgs-iv`; key `{agency_cd}/{site_no}` |

### Messagegroup `USGS.SiteTimeseries`
<a id="messagegroup-usgssitetimeseries"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `USGS.Timeseries.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `USGS.Sites.SiteTimeseries`
<a id="message-usgssitessitetimeseries"></a>

USGS site timeseries metadata.

| Field | Value |
| --- | --- |
| Name | SiteTimeseries |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.Sites.jstruct/schemas/USGS.Sites.SiteTimeseries`](#schema-usgssitessitetimeseries) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.Sites.SiteTimeseries` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.Timeseries.Kafka` | `KAFKA` | topic `usgs-iv`; key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

### Messagegroup `USGS.InstantaneousValues`
<a id="messagegroup-usgsinstantaneousvalues"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `USGS.Timeseries.Kafka` (KAFKA) |
| Messages | 26 |

#### Message `USGS.InstantaneousValues.OtherParameter`
<a id="message-usgsinstantaneousvaluesotherparameter"></a>

USGS other parameter data.

| Field | Value |
| --- | --- |
| Name | OtherParameter |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.OtherParameter`](#schema-usgsinstantaneousvaluesotherparameter) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.OtherParameter` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.Timeseries.Kafka` | `KAFKA` | topic `usgs-iv`; key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Message `USGS.InstantaneousValues.Precipitation`
<a id="message-usgsinstantaneousvaluesprecipitation"></a>

USGS precipitation data. Parameter code 00045.

| Field | Value |
| --- | --- |
| Name | Precipitation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.Precipitation`](#schema-usgsinstantaneousvaluesprecipitation) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.Precipitation` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.Timeseries.Kafka` | `KAFKA` | topic `usgs-iv`; key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Message `USGS.InstantaneousValues.Streamflow`
<a id="message-usgsinstantaneousvaluesstreamflow"></a>

USGS streamflow data. Parameter code 00060.

| Field | Value |
| --- | --- |
| Name | Streamflow |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.Streamflow`](#schema-usgsinstantaneousvaluesstreamflow) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.Streamflow` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.Timeseries.Kafka` | `KAFKA` | topic `usgs-iv`; key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Message `USGS.InstantaneousValues.GageHeight`
<a id="message-usgsinstantaneousvaluesgageheight"></a>

USGS gage height data. Parameter code 00065.

| Field | Value |
| --- | --- |
| Name | GageHeight |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.GageHeight`](#schema-usgsinstantaneousvaluesgageheight) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.GageHeight` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.Timeseries.Kafka` | `KAFKA` | topic `usgs-iv`; key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Message `USGS.InstantaneousValues.WaterTemperature`
<a id="message-usgsinstantaneousvalueswatertemperature"></a>

USGS water temperature data. Parameter code 00010.

| Field | Value |
| --- | --- |
| Name | WaterTemperature |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.WaterTemperature`](#schema-usgsinstantaneousvalueswatertemperature) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.WaterTemperature` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.Timeseries.Kafka` | `KAFKA` | topic `usgs-iv`; key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Message `USGS.InstantaneousValues.DissolvedOxygen`
<a id="message-usgsinstantaneousvaluesdissolvedoxygen"></a>

USGS dissolved oxygen data. Parameter code 00300.

| Field | Value |
| --- | --- |
| Name | DissolvedOxygen |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.DissolvedOxygen`](#schema-usgsinstantaneousvaluesdissolvedoxygen) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.DissolvedOxygen` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.Timeseries.Kafka` | `KAFKA` | topic `usgs-iv`; key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Message `USGS.InstantaneousValues.pH`
<a id="message-usgsinstantaneousvaluesph"></a>

USGS pH data. Parameter code 00400.

| Field | Value |
| --- | --- |
| Name | pH |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.pH`](#schema-usgsinstantaneousvaluesph) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.pH` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.Timeseries.Kafka` | `KAFKA` | topic `usgs-iv`; key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Message `USGS.InstantaneousValues.SpecificConductance`
<a id="message-usgsinstantaneousvaluesspecificconductance"></a>

USGS specific conductance data. Parameter code 00095.

| Field | Value |
| --- | --- |
| Name | SpecificConductance |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.SpecificConductance`](#schema-usgsinstantaneousvaluesspecificconductance) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.SpecificConductance` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.Timeseries.Kafka` | `KAFKA` | topic `usgs-iv`; key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Message `USGS.InstantaneousValues.Turbidity`
<a id="message-usgsinstantaneousvaluesturbidity"></a>

USGS turbidity data. Parameter code 00076.

| Field | Value |
| --- | --- |
| Name | Turbidity |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.Turbidity`](#schema-usgsinstantaneousvaluesturbidity) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.Turbidity` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.Timeseries.Kafka` | `KAFKA` | topic `usgs-iv`; key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Message `USGS.InstantaneousValues.AirTemperature`
<a id="message-usgsinstantaneousvaluesairtemperature"></a>

USGS air temperature data. Parameter code 00020.

| Field | Value |
| --- | --- |
| Name | AirTemperature |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.AirTemperature`](#schema-usgsinstantaneousvaluesairtemperature) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.AirTemperature` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.Timeseries.Kafka` | `KAFKA` | topic `usgs-iv`; key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Message `USGS.InstantaneousValues.WindSpeed`
<a id="message-usgsinstantaneousvalueswindspeed"></a>

USGS wind speed data. Parameter code 00035.

| Field | Value |
| --- | --- |
| Name | WindSpeed |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.WindSpeed`](#schema-usgsinstantaneousvalueswindspeed) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.WindSpeed` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.Timeseries.Kafka` | `KAFKA` | topic `usgs-iv`; key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Message `USGS.InstantaneousValues.WindDirection`
<a id="message-usgsinstantaneousvalueswinddirection"></a>

USGS wind direction data. Parameter codes 00036 and 163695.

| Field | Value |
| --- | --- |
| Name | WindDirection |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.WindDirection`](#schema-usgsinstantaneousvalueswinddirection) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.WindDirection` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.Timeseries.Kafka` | `KAFKA` | topic `usgs-iv`; key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Message `USGS.InstantaneousValues.RelativeHumidity`
<a id="message-usgsinstantaneousvaluesrelativehumidity"></a>

USGS relative humidity data. Parameter code 00052.

| Field | Value |
| --- | --- |
| Name | RelativeHumidity |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.RelativeHumidity`](#schema-usgsinstantaneousvaluesrelativehumidity) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.RelativeHumidity` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.Timeseries.Kafka` | `KAFKA` | topic `usgs-iv`; key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Message `USGS.InstantaneousValues.BarometricPressure`
<a id="message-usgsinstantaneousvaluesbarometricpressure"></a>

USGS barometric pressure data. Parameter codes 62605 and 75969.

| Field | Value |
| --- | --- |
| Name | BarometricPressure |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.BarometricPressure`](#schema-usgsinstantaneousvaluesbarometricpressure) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.BarometricPressure` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.Timeseries.Kafka` | `KAFKA` | topic `usgs-iv`; key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Message `USGS.InstantaneousValues.TurbidityFNU`
<a id="message-usgsinstantaneousvaluesturbidityfnu"></a>

USGS turbidity data (FNU). Parameter code 63680.

| Field | Value |
| --- | --- |
| Name | TurbidityFNU |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.TurbidityFNU`](#schema-usgsinstantaneousvaluesturbidityfnu) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.TurbidityFNU` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.Timeseries.Kafka` | `KAFKA` | topic `usgs-iv`; key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Message `USGS.InstantaneousValues.fDOM`
<a id="message-usgsinstantaneousvaluesfdom"></a>

USGS dissolved organic matter fluorescence data (fDOM). Parameter codes 32295 and 32322.

| Field | Value |
| --- | --- |
| Name | fDOM |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.fDOM`](#schema-usgsinstantaneousvaluesfdom) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.fDOM` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.Timeseries.Kafka` | `KAFKA` | topic `usgs-iv`; key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Message `USGS.InstantaneousValues.ReservoirStorage`
<a id="message-usgsinstantaneousvaluesreservoirstorage"></a>

USGS reservoir storage data. Parameter code 00054.

| Field | Value |
| --- | --- |
| Name | ReservoirStorage |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.ReservoirStorage`](#schema-usgsinstantaneousvaluesreservoirstorage) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.ReservoirStorage` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.Timeseries.Kafka` | `KAFKA` | topic `usgs-iv`; key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Message `USGS.InstantaneousValues.LakeElevationNGVD29`
<a id="message-usgsinstantaneousvalueslakeelevationngvd29"></a>

USGS lake or reservoir water surface elevation above NGVD 1929, feet. Parameter code 62614.

| Field | Value |
| --- | --- |
| Name | LakeElevationNGVD29 |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.LakeElevationNGVD29`](#schema-usgsinstantaneousvalueslakeelevationngvd29) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.LakeElevationNGVD29` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.Timeseries.Kafka` | `KAFKA` | topic `usgs-iv`; key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Message `USGS.InstantaneousValues.WaterDepth`
<a id="message-usgsinstantaneousvalueswaterdepth"></a>

USGS water depth data. Parameter code 72199.

| Field | Value |
| --- | --- |
| Name | WaterDepth |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.WaterDepth`](#schema-usgsinstantaneousvalueswaterdepth) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.WaterDepth` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.Timeseries.Kafka` | `KAFKA` | topic `usgs-iv`; key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Message `USGS.InstantaneousValues.EquipmentStatus`
<a id="message-usgsinstantaneousvaluesequipmentstatus"></a>

USGS equipment alarm status data. Parameter code 99235.

| Field | Value |
| --- | --- |
| Name | EquipmentStatus |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.EquipmentStatus`](#schema-usgsinstantaneousvaluesequipmentstatus) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.EquipmentStatus` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.Timeseries.Kafka` | `KAFKA` | topic `usgs-iv`; key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Message `USGS.InstantaneousValues.TidallyFilteredDischarge`
<a id="message-usgsinstantaneousvaluestidallyfiltereddischarge"></a>

USGS tidally filtered discharge data. Parameter code 72137.

| Field | Value |
| --- | --- |
| Name | TidallyFilteredDischarge |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.TidallyFilteredDischarge`](#schema-usgsinstantaneousvaluestidallyfiltereddischarge) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.TidallyFilteredDischarge` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.Timeseries.Kafka` | `KAFKA` | topic `usgs-iv`; key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Message `USGS.InstantaneousValues.WaterVelocity`
<a id="message-usgsinstantaneousvalueswatervelocity"></a>

USGS water velocity data. Parameter code 72254.

| Field | Value |
| --- | --- |
| Name | WaterVelocity |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.WaterVelocity`](#schema-usgsinstantaneousvalueswatervelocity) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.WaterVelocity` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.Timeseries.Kafka` | `KAFKA` | topic `usgs-iv`; key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Message `USGS.InstantaneousValues.EstuaryElevationNGVD29`
<a id="message-usgsinstantaneousvaluesestuaryelevationngvd29"></a>

USGS estuary or ocean water surface elevation above NGVD 1929, feet. Parameter code 62619.

| Field | Value |
| --- | --- |
| Name | EstuaryElevationNGVD29 |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.EstuaryElevationNGVD29`](#schema-usgsinstantaneousvaluesestuaryelevationngvd29) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.EstuaryElevationNGVD29` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.Timeseries.Kafka` | `KAFKA` | topic `usgs-iv`; key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Message `USGS.InstantaneousValues.LakeElevationNAVD88`
<a id="message-usgsinstantaneousvalueslakeelevationnavd88"></a>

USGS lake or reservoir water surface elevation above NAVD 1988, feet. Parameter code 62615.

| Field | Value |
| --- | --- |
| Name | LakeElevationNAVD88 |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.LakeElevationNAVD88`](#schema-usgsinstantaneousvalueslakeelevationnavd88) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.LakeElevationNAVD88` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.Timeseries.Kafka` | `KAFKA` | topic `usgs-iv`; key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Message `USGS.InstantaneousValues.Salinity`
<a id="message-usgsinstantaneousvaluessalinity"></a>

USGS salinity data. Parameter code 00480.

| Field | Value |
| --- | --- |
| Name | Salinity |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.Salinity`](#schema-usgsinstantaneousvaluessalinity) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.Salinity` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.Timeseries.Kafka` | `KAFKA` | topic `usgs-iv`; key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

#### Message `USGS.InstantaneousValues.GateOpening`
<a id="message-usgsinstantaneousvaluesgateopening"></a>

USGS gate opening data. Parameter code 45592.

| Field | Value |
| --- | --- |
| Name | GateOpening |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.GateOpening`](#schema-usgsinstantaneousvaluesgateopening) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.GateOpening` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.Timeseries.Kafka` | `KAFKA` | topic `usgs-iv`; key `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

### Messagegroup `USGS.Sites.mqtt`
<a id="messagegroup-usgssitesmqtt"></a>

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 transport variants for USGS site metadata. Topics are retained QoS-1 site info leaves under hydro/us/usgs/usgs-iv/{site_no}/info. The manifest intentionally uses existing schema field names site_no and parameter_cd rather than adding aliases. |
| Transport bindings | `USGS.IV.Mqtt` (MQTT/5.0) |
| Messages | 1 |

#### Message `USGS.Sites.mqtt.Site`
<a id="message-usgssitesmqttsite"></a>

USGS site metadata.

| Field | Value |
| --- | --- |
| Name | Site |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.Sites.jstruct/schemas/USGS.Sites.Site`](#schema-usgssitessite) |
| Base message chain | `/messagegroups/USGS.Sites/messages/USGS.Sites.Site` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.Sites.Site` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.IV.Mqtt` | `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/info` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `hydro/us/usgs/usgs-iv/{site_no}/info` |
| QoS | 1 |
| Retain | True |
| Additional protocol metadata | `{"message_expiry_interval": 2592000}` |

### Messagegroup `USGS.SiteTimeseries.mqtt`
<a id="messagegroup-usgssitetimeseriesmqtt"></a>

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 transport variants for USGS site timeseries metadata. Retained QoS-1 leaves use existing schema fields site_no, parameter_cd, and timeseries_cd to preserve the Kafka identity axes. |
| Transport bindings | `USGS.IV.Mqtt` (MQTT/5.0) |
| Messages | 1 |

#### Message `USGS.SiteTimeseries.mqtt.SiteTimeseries`
<a id="message-usgssitetimeseriesmqttsitetimeseries"></a>

USGS site timeseries metadata.

| Field | Value |
| --- | --- |
| Name | SiteTimeseries |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.Sites.jstruct/schemas/USGS.Sites.SiteTimeseries`](#schema-usgssitessitetimeseries) |
| Base message chain | `/messagegroups/USGS.SiteTimeseries/messages/USGS.Sites.SiteTimeseries` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.Sites.SiteTimeseries` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.IV.Mqtt` | `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/timeseries` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/timeseries` |
| QoS | 1 |
| Retain | True |
| Additional protocol metadata | `{"message_expiry_interval": 2592000}` |

### Messagegroup `USGS.InstantaneousValues.mqtt`
<a id="messagegroup-usgsinstantaneousvaluesmqtt"></a>

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 transport variants for USGS instantaneous values. Retained QoS-1 latest-observation leaves use existing schema fields site_no, parameter_cd, and timeseries_cd to avoid collapsing independent USGS time series; message expiry limits stale latest values. |
| Transport bindings | `USGS.IV.Mqtt` (MQTT/5.0) |
| Messages | 26 |

#### Message `USGS.InstantaneousValues.mqtt.OtherParameter`
<a id="message-usgsinstantaneousvaluesmqttotherparameter"></a>

USGS other parameter data.

| Field | Value |
| --- | --- |
| Name | OtherParameter |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.OtherParameter`](#schema-usgsinstantaneousvaluesotherparameter) |
| Base message chain | `/messagegroups/USGS.InstantaneousValues/messages/USGS.InstantaneousValues.OtherParameter` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.OtherParameter` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.IV.Mqtt` | `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |
| QoS | 1 |
| Retain | True |
| Additional protocol metadata | `{"message_expiry_interval": 86400}` |

#### Message `USGS.InstantaneousValues.mqtt.Precipitation`
<a id="message-usgsinstantaneousvaluesmqttprecipitation"></a>

USGS precipitation data. Parameter code 00045.

| Field | Value |
| --- | --- |
| Name | Precipitation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.Precipitation`](#schema-usgsinstantaneousvaluesprecipitation) |
| Base message chain | `/messagegroups/USGS.InstantaneousValues/messages/USGS.InstantaneousValues.Precipitation` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.Precipitation` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.IV.Mqtt` | `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |
| QoS | 1 |
| Retain | True |
| Additional protocol metadata | `{"message_expiry_interval": 86400}` |

#### Message `USGS.InstantaneousValues.mqtt.Streamflow`
<a id="message-usgsinstantaneousvaluesmqttstreamflow"></a>

USGS streamflow data. Parameter code 00060.

| Field | Value |
| --- | --- |
| Name | Streamflow |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.Streamflow`](#schema-usgsinstantaneousvaluesstreamflow) |
| Base message chain | `/messagegroups/USGS.InstantaneousValues/messages/USGS.InstantaneousValues.Streamflow` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.Streamflow` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.IV.Mqtt` | `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |
| QoS | 1 |
| Retain | True |
| Additional protocol metadata | `{"message_expiry_interval": 86400}` |

#### Message `USGS.InstantaneousValues.mqtt.GageHeight`
<a id="message-usgsinstantaneousvaluesmqttgageheight"></a>

USGS gage height data. Parameter code 00065.

| Field | Value |
| --- | --- |
| Name | GageHeight |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.GageHeight`](#schema-usgsinstantaneousvaluesgageheight) |
| Base message chain | `/messagegroups/USGS.InstantaneousValues/messages/USGS.InstantaneousValues.GageHeight` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.GageHeight` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.IV.Mqtt` | `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |
| QoS | 1 |
| Retain | True |
| Additional protocol metadata | `{"message_expiry_interval": 86400}` |

#### Message `USGS.InstantaneousValues.mqtt.WaterTemperature`
<a id="message-usgsinstantaneousvaluesmqttwatertemperature"></a>

USGS water temperature data. Parameter code 00010.

| Field | Value |
| --- | --- |
| Name | WaterTemperature |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.WaterTemperature`](#schema-usgsinstantaneousvalueswatertemperature) |
| Base message chain | `/messagegroups/USGS.InstantaneousValues/messages/USGS.InstantaneousValues.WaterTemperature` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.WaterTemperature` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.IV.Mqtt` | `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |
| QoS | 1 |
| Retain | True |
| Additional protocol metadata | `{"message_expiry_interval": 86400}` |

#### Message `USGS.InstantaneousValues.mqtt.DissolvedOxygen`
<a id="message-usgsinstantaneousvaluesmqttdissolvedoxygen"></a>

USGS dissolved oxygen data. Parameter code 00300.

| Field | Value |
| --- | --- |
| Name | DissolvedOxygen |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.DissolvedOxygen`](#schema-usgsinstantaneousvaluesdissolvedoxygen) |
| Base message chain | `/messagegroups/USGS.InstantaneousValues/messages/USGS.InstantaneousValues.DissolvedOxygen` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.DissolvedOxygen` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.IV.Mqtt` | `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |
| QoS | 1 |
| Retain | True |
| Additional protocol metadata | `{"message_expiry_interval": 86400}` |

#### Message `USGS.InstantaneousValues.mqtt.pH`
<a id="message-usgsinstantaneousvaluesmqttph"></a>

USGS pH data. Parameter code 00400.

| Field | Value |
| --- | --- |
| Name | pH |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.pH`](#schema-usgsinstantaneousvaluesph) |
| Base message chain | `/messagegroups/USGS.InstantaneousValues/messages/USGS.InstantaneousValues.pH` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.pH` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.IV.Mqtt` | `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |
| QoS | 1 |
| Retain | True |
| Additional protocol metadata | `{"message_expiry_interval": 86400}` |

#### Message `USGS.InstantaneousValues.mqtt.SpecificConductance`
<a id="message-usgsinstantaneousvaluesmqttspecificconductance"></a>

USGS specific conductance data. Parameter code 00095.

| Field | Value |
| --- | --- |
| Name | SpecificConductance |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.SpecificConductance`](#schema-usgsinstantaneousvaluesspecificconductance) |
| Base message chain | `/messagegroups/USGS.InstantaneousValues/messages/USGS.InstantaneousValues.SpecificConductance` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.SpecificConductance` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.IV.Mqtt` | `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |
| QoS | 1 |
| Retain | True |
| Additional protocol metadata | `{"message_expiry_interval": 86400}` |

#### Message `USGS.InstantaneousValues.mqtt.Turbidity`
<a id="message-usgsinstantaneousvaluesmqttturbidity"></a>

USGS turbidity data. Parameter code 00076.

| Field | Value |
| --- | --- |
| Name | Turbidity |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.Turbidity`](#schema-usgsinstantaneousvaluesturbidity) |
| Base message chain | `/messagegroups/USGS.InstantaneousValues/messages/USGS.InstantaneousValues.Turbidity` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.Turbidity` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.IV.Mqtt` | `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |
| QoS | 1 |
| Retain | True |
| Additional protocol metadata | `{"message_expiry_interval": 86400}` |

#### Message `USGS.InstantaneousValues.mqtt.AirTemperature`
<a id="message-usgsinstantaneousvaluesmqttairtemperature"></a>

USGS air temperature data. Parameter code 00020.

| Field | Value |
| --- | --- |
| Name | AirTemperature |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.AirTemperature`](#schema-usgsinstantaneousvaluesairtemperature) |
| Base message chain | `/messagegroups/USGS.InstantaneousValues/messages/USGS.InstantaneousValues.AirTemperature` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.AirTemperature` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.IV.Mqtt` | `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |
| QoS | 1 |
| Retain | True |
| Additional protocol metadata | `{"message_expiry_interval": 86400}` |

#### Message `USGS.InstantaneousValues.mqtt.WindSpeed`
<a id="message-usgsinstantaneousvaluesmqttwindspeed"></a>

USGS wind speed data. Parameter code 00035.

| Field | Value |
| --- | --- |
| Name | WindSpeed |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.WindSpeed`](#schema-usgsinstantaneousvalueswindspeed) |
| Base message chain | `/messagegroups/USGS.InstantaneousValues/messages/USGS.InstantaneousValues.WindSpeed` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.WindSpeed` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.IV.Mqtt` | `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |
| QoS | 1 |
| Retain | True |
| Additional protocol metadata | `{"message_expiry_interval": 86400}` |

#### Message `USGS.InstantaneousValues.mqtt.WindDirection`
<a id="message-usgsinstantaneousvaluesmqttwinddirection"></a>

USGS wind direction data. Parameter codes 00036 and 163695.

| Field | Value |
| --- | --- |
| Name | WindDirection |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.WindDirection`](#schema-usgsinstantaneousvalueswinddirection) |
| Base message chain | `/messagegroups/USGS.InstantaneousValues/messages/USGS.InstantaneousValues.WindDirection` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.WindDirection` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.IV.Mqtt` | `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |
| QoS | 1 |
| Retain | True |
| Additional protocol metadata | `{"message_expiry_interval": 86400}` |

#### Message `USGS.InstantaneousValues.mqtt.RelativeHumidity`
<a id="message-usgsinstantaneousvaluesmqttrelativehumidity"></a>

USGS relative humidity data. Parameter code 00052.

| Field | Value |
| --- | --- |
| Name | RelativeHumidity |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.RelativeHumidity`](#schema-usgsinstantaneousvaluesrelativehumidity) |
| Base message chain | `/messagegroups/USGS.InstantaneousValues/messages/USGS.InstantaneousValues.RelativeHumidity` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.RelativeHumidity` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.IV.Mqtt` | `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |
| QoS | 1 |
| Retain | True |
| Additional protocol metadata | `{"message_expiry_interval": 86400}` |

#### Message `USGS.InstantaneousValues.mqtt.BarometricPressure`
<a id="message-usgsinstantaneousvaluesmqttbarometricpressure"></a>

USGS barometric pressure data. Parameter codes 62605 and 75969.

| Field | Value |
| --- | --- |
| Name | BarometricPressure |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.BarometricPressure`](#schema-usgsinstantaneousvaluesbarometricpressure) |
| Base message chain | `/messagegroups/USGS.InstantaneousValues/messages/USGS.InstantaneousValues.BarometricPressure` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.BarometricPressure` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.IV.Mqtt` | `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |
| QoS | 1 |
| Retain | True |
| Additional protocol metadata | `{"message_expiry_interval": 86400}` |

#### Message `USGS.InstantaneousValues.mqtt.TurbidityFNU`
<a id="message-usgsinstantaneousvaluesmqttturbidityfnu"></a>

USGS turbidity data (FNU). Parameter code 63680.

| Field | Value |
| --- | --- |
| Name | TurbidityFNU |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.TurbidityFNU`](#schema-usgsinstantaneousvaluesturbidityfnu) |
| Base message chain | `/messagegroups/USGS.InstantaneousValues/messages/USGS.InstantaneousValues.TurbidityFNU` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.TurbidityFNU` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.IV.Mqtt` | `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |
| QoS | 1 |
| Retain | True |
| Additional protocol metadata | `{"message_expiry_interval": 86400}` |

#### Message `USGS.InstantaneousValues.mqtt.fDOM`
<a id="message-usgsinstantaneousvaluesmqttfdom"></a>

USGS dissolved organic matter fluorescence data (fDOM). Parameter codes 32295 and 32322.

| Field | Value |
| --- | --- |
| Name | fDOM |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.fDOM`](#schema-usgsinstantaneousvaluesfdom) |
| Base message chain | `/messagegroups/USGS.InstantaneousValues/messages/USGS.InstantaneousValues.fDOM` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.fDOM` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.IV.Mqtt` | `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |
| QoS | 1 |
| Retain | True |
| Additional protocol metadata | `{"message_expiry_interval": 86400}` |

#### Message `USGS.InstantaneousValues.mqtt.ReservoirStorage`
<a id="message-usgsinstantaneousvaluesmqttreservoirstorage"></a>

USGS reservoir storage data. Parameter code 00054.

| Field | Value |
| --- | --- |
| Name | ReservoirStorage |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.ReservoirStorage`](#schema-usgsinstantaneousvaluesreservoirstorage) |
| Base message chain | `/messagegroups/USGS.InstantaneousValues/messages/USGS.InstantaneousValues.ReservoirStorage` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.ReservoirStorage` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.IV.Mqtt` | `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |
| QoS | 1 |
| Retain | True |
| Additional protocol metadata | `{"message_expiry_interval": 86400}` |

#### Message `USGS.InstantaneousValues.mqtt.LakeElevationNGVD29`
<a id="message-usgsinstantaneousvaluesmqttlakeelevationngvd29"></a>

USGS lake or reservoir water surface elevation above NGVD 1929, feet. Parameter code 62614.

| Field | Value |
| --- | --- |
| Name | LakeElevationNGVD29 |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.LakeElevationNGVD29`](#schema-usgsinstantaneousvalueslakeelevationngvd29) |
| Base message chain | `/messagegroups/USGS.InstantaneousValues/messages/USGS.InstantaneousValues.LakeElevationNGVD29` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.LakeElevationNGVD29` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.IV.Mqtt` | `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |
| QoS | 1 |
| Retain | True |
| Additional protocol metadata | `{"message_expiry_interval": 86400}` |

#### Message `USGS.InstantaneousValues.mqtt.WaterDepth`
<a id="message-usgsinstantaneousvaluesmqttwaterdepth"></a>

USGS water depth data. Parameter code 72199.

| Field | Value |
| --- | --- |
| Name | WaterDepth |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.WaterDepth`](#schema-usgsinstantaneousvalueswaterdepth) |
| Base message chain | `/messagegroups/USGS.InstantaneousValues/messages/USGS.InstantaneousValues.WaterDepth` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.WaterDepth` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.IV.Mqtt` | `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |
| QoS | 1 |
| Retain | True |
| Additional protocol metadata | `{"message_expiry_interval": 86400}` |

#### Message `USGS.InstantaneousValues.mqtt.EquipmentStatus`
<a id="message-usgsinstantaneousvaluesmqttequipmentstatus"></a>

USGS equipment alarm status data. Parameter code 99235.

| Field | Value |
| --- | --- |
| Name | EquipmentStatus |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.EquipmentStatus`](#schema-usgsinstantaneousvaluesequipmentstatus) |
| Base message chain | `/messagegroups/USGS.InstantaneousValues/messages/USGS.InstantaneousValues.EquipmentStatus` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.EquipmentStatus` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.IV.Mqtt` | `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |
| QoS | 1 |
| Retain | True |
| Additional protocol metadata | `{"message_expiry_interval": 86400}` |

#### Message `USGS.InstantaneousValues.mqtt.TidallyFilteredDischarge`
<a id="message-usgsinstantaneousvaluesmqtttidallyfiltereddischarge"></a>

USGS tidally filtered discharge data. Parameter code 72137.

| Field | Value |
| --- | --- |
| Name | TidallyFilteredDischarge |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.TidallyFilteredDischarge`](#schema-usgsinstantaneousvaluestidallyfiltereddischarge) |
| Base message chain | `/messagegroups/USGS.InstantaneousValues/messages/USGS.InstantaneousValues.TidallyFilteredDischarge` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.TidallyFilteredDischarge` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.IV.Mqtt` | `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |
| QoS | 1 |
| Retain | True |
| Additional protocol metadata | `{"message_expiry_interval": 86400}` |

#### Message `USGS.InstantaneousValues.mqtt.WaterVelocity`
<a id="message-usgsinstantaneousvaluesmqttwatervelocity"></a>

USGS water velocity data. Parameter code 72254.

| Field | Value |
| --- | --- |
| Name | WaterVelocity |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.WaterVelocity`](#schema-usgsinstantaneousvalueswatervelocity) |
| Base message chain | `/messagegroups/USGS.InstantaneousValues/messages/USGS.InstantaneousValues.WaterVelocity` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.WaterVelocity` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.IV.Mqtt` | `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |
| QoS | 1 |
| Retain | True |
| Additional protocol metadata | `{"message_expiry_interval": 86400}` |

#### Message `USGS.InstantaneousValues.mqtt.EstuaryElevationNGVD29`
<a id="message-usgsinstantaneousvaluesmqttestuaryelevationngvd29"></a>

USGS estuary or ocean water surface elevation above NGVD 1929, feet. Parameter code 62619.

| Field | Value |
| --- | --- |
| Name | EstuaryElevationNGVD29 |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.EstuaryElevationNGVD29`](#schema-usgsinstantaneousvaluesestuaryelevationngvd29) |
| Base message chain | `/messagegroups/USGS.InstantaneousValues/messages/USGS.InstantaneousValues.EstuaryElevationNGVD29` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.EstuaryElevationNGVD29` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.IV.Mqtt` | `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |
| QoS | 1 |
| Retain | True |
| Additional protocol metadata | `{"message_expiry_interval": 86400}` |

#### Message `USGS.InstantaneousValues.mqtt.LakeElevationNAVD88`
<a id="message-usgsinstantaneousvaluesmqttlakeelevationnavd88"></a>

USGS lake or reservoir water surface elevation above NAVD 1988, feet. Parameter code 62615.

| Field | Value |
| --- | --- |
| Name | LakeElevationNAVD88 |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.LakeElevationNAVD88`](#schema-usgsinstantaneousvalueslakeelevationnavd88) |
| Base message chain | `/messagegroups/USGS.InstantaneousValues/messages/USGS.InstantaneousValues.LakeElevationNAVD88` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.LakeElevationNAVD88` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.IV.Mqtt` | `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |
| QoS | 1 |
| Retain | True |
| Additional protocol metadata | `{"message_expiry_interval": 86400}` |

#### Message `USGS.InstantaneousValues.mqtt.Salinity`
<a id="message-usgsinstantaneousvaluesmqttsalinity"></a>

USGS salinity data. Parameter code 00480.

| Field | Value |
| --- | --- |
| Name | Salinity |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.Salinity`](#schema-usgsinstantaneousvaluessalinity) |
| Base message chain | `/messagegroups/USGS.InstantaneousValues/messages/USGS.InstantaneousValues.Salinity` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.Salinity` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.IV.Mqtt` | `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |
| QoS | 1 |
| Retain | True |
| Additional protocol metadata | `{"message_expiry_interval": 86400}` |

#### Message `USGS.InstantaneousValues.mqtt.GateOpening`
<a id="message-usgsinstantaneousvaluesmqttgateopening"></a>

USGS gate opening data. Parameter code 45592.

| Field | Value |
| --- | --- |
| Name | GateOpening |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.InstantaneousValues.jstruct/schemas/USGS.InstantaneousValues.GateOpening`](#schema-usgsinstantaneousvaluesgateopening) |
| Base message chain | `/messagegroups/USGS.InstantaneousValues/messages/USGS.InstantaneousValues.GateOpening` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.InstantaneousValues.GateOpening` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{agency_cd}/{site_no}/{parameter_cd}/{timeseries_cd}` |
| `time` |  | `uritemplate` | `False` | `{datetime}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.IV.Mqtt` | `MQTT/5.0` | topic `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `hydro/us/usgs/usgs-iv/{site_no}/{parameter_cd}/{timeseries_cd}/observation` |
| QoS | 1 |
| Retain | True |
| Additional protocol metadata | `{"message_expiry_interval": 86400}` |

## Schemagroups

### Schemagroup `USGS.Sites.jstruct`
<a id="schemagroup-usgssitesjstruct"></a>

#### Schema `USGS.Sites.Site`
<a id="schema-usgssitessite"></a>

| Field | Value |
| --- | --- |
| Name | Site |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/USGS/Sites/Site` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/USGS/Sites/Site` |
| Type | `object` |

###### Object `Site`
<a id="schema-node-site"></a>

USGS site metadata.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `agency_cd` | `string` | `True` | Agency code. | - | - | - |
| `site_no` | `string` | `True` | USGS site number. | - | - | - |
| `station_nm` | `string` | `True` | Station name. | - | - | - |
| `site_tp_cd` | `string` | `True` | Site type code. | - | - | - |
| `lat_va` | `string` | `True` | DMS latitude. | - | - | - |
| `long_va` | `string` | `True` | DMS longitude. | - | - | - |
| `dec_lat_va` | `float` | `False` | Decimal latitude. | - | default=`-` | default=`-` |
| `dec_long_va` | `float` | `False` | Decimal longitude. | - | default=`-` | default=`-` |
| `coord_meth_cd` | `string` | `True` | Latitude-longitude method code. | - | - | - |
| `coord_acy_cd` | `string` | `True` | Coordinate accuracy code. | - | - | - |
| `coord_datum_cd` | `string` | `True` | Latitude-longitude datum code. | - | - | - |
| `dec_coord_datum_cd` | `string` | `True` | Decimal latitude-longitude datum code. | - | - | - |
| `district_cd` | `string` | `True` | District code. | - | - | - |
| `state_cd` | `string` | `True` | State code. | - | - | - |
| `county_cd` | `string` | `True` | County code. | - | - | - |
| `country_cd` | `string` | `True` | Country code. | - | - | - |
| `land_net_ds` | `string` | `True` | Land net location description. | - | - | - |
| `map_nm` | `string` | `True` | Location map name. | - | - | - |
| `map_scale_fc` | `float` | `False` | Location map scale factor. | - | default=`-` | default=`-` |
| `alt_va` | `float` | `False` | Altitude. | - | default=`-` | default=`-` |
| `alt_meth_cd` | `string` | `True` | Method altitude determined code. | - | - | - |
| `alt_acy_va` | `float` | `False` | Altitude accuracy. | - | default=`-` | default=`-` |
| `alt_datum_cd` | `string` | `True` | Altitude datum code. | - | - | - |
| `huc_cd` | `string` | `True` | Hydrologic unit code. | - | - | - |
| `basin_cd` | `string` | `True` | Drainage basin code. | - | - | - |
| `topo_cd` | `string` | `True` | Topographic setting code. | - | - | - |
| `instruments_cd` | `string` | `True` | Flags for instruments at site. | - | - | - |
| `construction_dt` | `string` | `False` | Date of first construction. | - | default=`-` | default=`-` |
| `inventory_dt` | `string` | `False` | Date site established or inventoried. | - | default=`-` | default=`-` |
| `drain_area_va` | `float` | `False` | Drainage area. | - | default=`-` | default=`-` |
| `contrib_drain_area_va` | `float` | `False` | Contributing drainage area. | - | default=`-` | default=`-` |
| `tz_cd` | `string` | `True` | Time Zone abbreviation. | - | - | - |
| `local_time_fg` | `boolean` | `True` | Site honors Daylight Savings Time flag. | - | - | - |
| `reliability_cd` | `string` | `True` | Data reliability code. | - | - | - |
| `gw_file_cd` | `string` | `True` | Data-other GW files code. | - | - | - |
| `nat_aqfr_cd` | `string` | `True` | National aquifer code. | - | - | - |
| `aqfr_cd` | `string` | `True` | Local aquifer code. | - | - | - |
| `aqfr_type_cd` | `string` | `True` | Local aquifer type code. | - | - | - |
| `well_depth_va` | `float` | `False` | Well depth. | - | default=`-` | default=`-` |
| `hole_depth_va` | `float` | `False` | Hole depth. | - | default=`-` | default=`-` |
| `depth_src_cd` | `string` | `True` | Source of depth data. | - | - | - |
| `project_no` | `string` | `True` | Project number. | - | - | - |

#### Schema `USGS.Sites.SiteTimeseries`
<a id="schema-usgssitessitetimeseries"></a>

| Field | Value |
| --- | --- |
| Name | SiteTimeseries |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/USGS/Sites/SiteTimeseries` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/USGS/Sites/SiteTimeseries` |
| Type | `object` |

###### Object `SiteTimeseries`
<a id="schema-node-sitetimeseries"></a>

USGS site timeseries metadata.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `agency_cd` | `string` | `True` | Agency code. | - | - | - |
| `site_no` | `string` | `True` | USGS site number. | - | - | - |
| `parameter_cd` | `string` | `True` | Parameter code. | - | - | - |
| `timeseries_cd` | `string` | `True` | Timeseries code. | - | - | - |
| `description` | `string` | `True` | Description. | - | - | - |

### Schemagroup `USGS.Sites.avro`
<a id="schemagroup-usgssitesavro"></a>

#### Schema `USGS.Sites.Site`
<a id="schema-usgssitessite"></a>

| Field | Value |
| --- | --- |
| Name | Site |
| Format | Avro/1.11.3 |
| Default version | 1 |
| Description | USGS site metadata. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | Site |
| Namespace | USGS.Sites |
| Type | `record` |
| Doc | USGS site metadata. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `agency_cd` | `string` | Agency code. | `-` |
| `site_no` | `string` | USGS site number. | `-` |
| `station_nm` | `string` | Station name. | `-` |
| `site_tp_cd` | `string` | Site type code. | `-` |
| `lat_va` | `string` | DMS latitude. | `-` |
| `long_va` | `string` | DMS longitude. | `-` |
| `dec_lat_va` | `null` \| `float` | Decimal latitude. | `-` |
| `dec_long_va` | `null` \| `float` | Decimal longitude. | `-` |
| `coord_meth_cd` | `string` | Latitude-longitude method code. | `-` |
| `coord_acy_cd` | `string` | Coordinate accuracy code. | `-` |
| `coord_datum_cd` | `string` | Latitude-longitude datum code. | `-` |
| `dec_coord_datum_cd` | `string` | Decimal latitude-longitude datum code. | `-` |
| `district_cd` | `string` | District code. | `-` |
| `state_cd` | `string` | State code. | `-` |
| `county_cd` | `string` | County code. | `-` |
| `country_cd` | `string` | Country code. | `-` |
| `land_net_ds` | `string` | Land net location description. | `-` |
| `map_nm` | `string` | Location map name. | `-` |
| `map_scale_fc` | `null` \| `float` | Location map scale factor. | `-` |
| `alt_va` | `null` \| `float` | Altitude. | `-` |
| `alt_meth_cd` | `string` | Method altitude determined code. | `-` |
| `alt_acy_va` | `null` \| `float` | Altitude accuracy. | `-` |
| `alt_datum_cd` | `string` | Altitude datum code. | `-` |
| `huc_cd` | `string` | Hydrologic unit code. | `-` |
| `basin_cd` | `string` | Drainage basin code. | `-` |
| `topo_cd` | `string` | Topographic setting code. | `-` |
| `instruments_cd` | `string` | Flags for instruments at site. | `-` |
| `construction_dt` | `null` \| `string` | Date of first construction. | `-` |
| `inventory_dt` | `null` \| `string` | Date site established or inventoried. | `-` |
| `drain_area_va` | `null` \| `float` | Drainage area. | `-` |
| `contrib_drain_area_va` | `null` \| `float` | Contributing drainage area. | `-` |
| `tz_cd` | `string` | Time Zone abbreviation. | `-` |
| `local_time_fg` | `boolean` | Site honors Daylight Savings Time flag. | `-` |
| `reliability_cd` | `string` | Data reliability code. | `-` |
| `gw_file_cd` | `string` | Data-other GW files code. | `-` |
| `nat_aqfr_cd` | `string` | National aquifer code. | `-` |
| `aqfr_cd` | `string` | Local aquifer code. | `-` |
| `aqfr_type_cd` | `string` | Local aquifer type code. | `-` |
| `well_depth_va` | `null` \| `float` | Well depth. | `-` |
| `hole_depth_va` | `null` \| `float` | Hole depth. | `-` |
| `depth_src_cd` | `string` | Source of depth data. | `-` |
| `project_no` | `string` | Project number. | `-` |

#### Schema `USGS.Sites.SiteTimeseries`
<a id="schema-usgssitessitetimeseries"></a>

| Field | Value |
| --- | --- |
| Name | SiteTimeseries |
| Format | Avro/1.11.3 |
| Default version | 1 |
| Description | USGS site timeseries metadata. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | SiteTimeseries |
| Namespace | USGS.Sites |
| Type | `record` |
| Doc | USGS site timeseries metadata. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `agency_cd` | `string` | Agency code. | `-` |
| `site_no` | `string` | USGS site number. | `-` |
| `parameter_cd` | `string` | Parameter code. | `-` |
| `timeseries_cd` | `string` | Timeseries code. | `-` |
| `description` | `string` | Description. | `-` |

### Schemagroup `USGS.InstantaneousValues.jstruct`
<a id="schemagroup-usgsinstantaneousvaluesjstruct"></a>

#### Schema `USGS.InstantaneousValues.OtherParameter`
<a id="schema-usgsinstantaneousvaluesotherparameter"></a>

| Field | Value |
| --- | --- |
| Name | OtherParameter |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/USGS/InstantaneousValues/OtherParameter` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/USGS/InstantaneousValues/OtherParameter` |
| Type | `object` |

###### Object `OtherParameter`
<a id="schema-node-otherparameter"></a>

USGS other parameter data.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `site_no` | `string` | `True` | {"description": "USGS site number."} | - | - | - |
| `datetime` | `string` | `True` | {"description": "Date and time of the measurement in ISO-8601 format."} | - | - | - |
| `value` | `double` | `False` | {"description": "Value."} | - | - | - |
| `exception` | `string` | `False` | {"description": "Exception code when the value is unavailable."} | - | - | - |
| `qualifiers` | array of `string` | `True` | {"description": "Qualifiers for the measurement."} | - | - | - |
| `parameter_cd` | `string` | `True` | {"description": "Parameter code."} | - | - | - |
| `timeseries_cd` | `string` | `True` | {"description": "Timeseries code."} | - | - | - |

#### Schema `USGS.InstantaneousValues.Precipitation`
<a id="schema-usgsinstantaneousvaluesprecipitation"></a>

| Field | Value |
| --- | --- |
| Name | Precipitation |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/USGS/InstantaneousValues/Precipitation` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/USGS/InstantaneousValues/Precipitation` |
| Type | `object` |

###### Object `Precipitation`
<a id="schema-node-precipitation"></a>

USGS precipitation data. Parameter code 00045.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `site_no` | `string` | `True` | {"description": "USGS site number."} | - | - | - |
| `datetime` | `string` | `True` | {"description": "Date and time of the measurement in ISO-8601 format."} | - | - | - |
| `value` | `double` | `False` | {"description": "Precipitation value, inches."} | - | - | - |
| `exception` | `string` | `False` | {"description": "Exception code when the value is unavailable."} | - | - | - |
| `qualifiers` | array of `string` | `True` | {"description": "Qualifiers for the measurement."} | - | - | - |
| `parameter_cd` | `string` | `True` | {"description": "Parameter code."} | - | - | - |
| `timeseries_cd` | `string` | `True` | {"description": "Timeseries code."} | - | - | - |

#### Schema `USGS.InstantaneousValues.Streamflow`
<a id="schema-usgsinstantaneousvaluesstreamflow"></a>

| Field | Value |
| --- | --- |
| Name | Streamflow |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/USGS/InstantaneousValues/Streamflow` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/USGS/InstantaneousValues/Streamflow` |
| Type | `object` |

###### Object `Streamflow`
<a id="schema-node-streamflow"></a>

USGS streamflow data. Parameter code 00060.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `site_no` | `string` | `True` | {"description": "USGS site number."} | - | - | - |
| `datetime` | `string` | `True` | {"description": "Date and time of the measurement in ISO-8601 format."} | - | - | - |
| `value` | `double` | `False` | {"description": "Discharge value."} | - | - | - |
| `exception` | `string` | `False` | {"description": "Exception code when the value is unavailable."} | - | - | - |
| `qualifiers` | array of `string` | `True` | {"description": "Qualifiers for the measurement."} | - | - | - |
| `parameter_cd` | `string` | `True` | {"description": "Parameter code."} | - | - | - |
| `timeseries_cd` | `string` | `True` | {"description": "Timeseries code."} | - | - | - |

#### Schema `USGS.InstantaneousValues.GageHeight`
<a id="schema-usgsinstantaneousvaluesgageheight"></a>

| Field | Value |
| --- | --- |
| Name | GageHeight |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/USGS/InstantaneousValues/GageHeight` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/USGS/InstantaneousValues/GageHeight` |
| Type | `object` |

###### Object `GageHeight`
<a id="schema-node-gageheight"></a>

USGS gage height data. Parameter code 00065.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `site_no` | `string` | `True` | {"description": "USGS site number."} | - | - | - |
| `datetime` | `string` | `True` | {"description": "Date and time of the measurement in ISO-8601 format."} | - | - | - |
| `value` | `double` | `False` | {"description": "Gage height value."} | - | - | - |
| `exception` | `string` | `False` | {"description": "Exception code when the value is unavailable."} | - | - | - |
| `qualifiers` | array of `string` | `True` | {"description": "Qualifiers for the measurement."} | - | - | - |
| `parameter_cd` | `string` | `True` | {"description": "Parameter code."} | - | - | - |
| `timeseries_cd` | `string` | `True` | {"description": "Timeseries code."} | - | - | - |

#### Schema `USGS.InstantaneousValues.WaterTemperature`
<a id="schema-usgsinstantaneousvalueswatertemperature"></a>

| Field | Value |
| --- | --- |
| Name | WaterTemperature |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/USGS/InstantaneousValues/WaterTemperature` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/USGS/InstantaneousValues/WaterTemperature` |
| Type | `object` |

###### Object `WaterTemperature`
<a id="schema-node-watertemperature"></a>

USGS water temperature data. Parameter code 00010.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `site_no` | `string` | `True` | {"description": "USGS site number."} | - | - | - |
| `datetime` | `string` | `True` | {"description": "Date and time of the measurement in ISO-8601 format."} | - | - | - |
| `value` | `double` | `False` | {"description": "Water temperature value."} | - | - | - |
| `exception` | `string` | `False` | {"description": "Exception code when the value is unavailable."} | - | - | - |
| `qualifiers` | array of `string` | `True` | {"description": "Qualifiers for the measurement."} | - | - | - |
| `parameter_cd` | `string` | `True` | {"description": "Parameter code."} | - | - | - |
| `timeseries_cd` | `string` | `True` | {"description": "Timeseries code."} | - | - | - |

#### Schema `USGS.InstantaneousValues.DissolvedOxygen`
<a id="schema-usgsinstantaneousvaluesdissolvedoxygen"></a>

| Field | Value |
| --- | --- |
| Name | DissolvedOxygen |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/USGS/InstantaneousValues/DissolvedOxygen` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/USGS/InstantaneousValues/DissolvedOxygen` |
| Type | `object` |

###### Object `DissolvedOxygen`
<a id="schema-node-dissolvedoxygen"></a>

USGS dissolved oxygen data. Parameter code 00300.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `site_no` | `string` | `True` | {"description": "USGS site number."} | - | - | - |
| `datetime` | `string` | `True` | {"description": "Date and time of the measurement in ISO-8601 format."} | - | - | - |
| `value` | `double` | `False` | {"description": "Dissolved oxygen value."} | - | - | - |
| `exception` | `string` | `False` | {"description": "Exception code when the value is unavailable."} | - | - | - |
| `qualifiers` | array of `string` | `True` | {"description": "Qualifiers for the measurement."} | - | - | - |
| `parameter_cd` | `string` | `True` | {"description": "Parameter code."} | - | - | - |
| `timeseries_cd` | `string` | `True` | {"description": "Timeseries code."} | - | - | - |

#### Schema `USGS.InstantaneousValues.pH`
<a id="schema-usgsinstantaneousvaluesph"></a>

| Field | Value |
| --- | --- |
| Name | pH |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/USGS/InstantaneousValues/pH` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/USGS/InstantaneousValues/pH` |
| Type | `object` |

###### Object `pH`
<a id="schema-node-ph"></a>

USGS pH data. Parameter code 00400.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `site_no` | `string` | `True` | {"description": "USGS site number."} | - | - | - |
| `datetime` | `string` | `True` | {"description": "Date and time of the measurement in ISO-8601 format."} | - | - | - |
| `value` | `double` | `False` | {"description": "pH value."} | - | - | - |
| `exception` | `string` | `False` | {"description": "Exception code when the value is unavailable."} | - | - | - |
| `qualifiers` | array of `string` | `True` | {"description": "Qualifiers for the measurement."} | - | - | - |
| `parameter_cd` | `string` | `True` | {"description": "Parameter code."} | - | - | - |
| `timeseries_cd` | `string` | `True` | {"description": "Timeseries code."} | - | - | - |

#### Schema `USGS.InstantaneousValues.SpecificConductance`
<a id="schema-usgsinstantaneousvaluesspecificconductance"></a>

| Field | Value |
| --- | --- |
| Name | SpecificConductance |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/USGS/InstantaneousValues/SpecificConductance` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/USGS/InstantaneousValues/SpecificConductance` |
| Type | `object` |

###### Object `SpecificConductance`
<a id="schema-node-specificconductance"></a>

USGS specific conductance data. Parameter code 00095.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `site_no` | `string` | `True` | {"description": "USGS site number."} | - | - | - |
| `datetime` | `string` | `True` | {"description": "Date and time of the measurement in ISO-8601 format."} | - | - | - |
| `value` | `double` | `False` | {"description": "Specific conductance value."} | - | - | - |
| `exception` | `string` | `False` | {"description": "Exception code when the value is unavailable."} | - | - | - |
| `qualifiers` | array of `string` | `True` | {"description": "Qualifiers for the measurement."} | - | - | - |
| `parameter_cd` | `string` | `True` | {"description": "Parameter code."} | - | - | - |
| `timeseries_cd` | `string` | `True` | {"description": "Timeseries code."} | - | - | - |

#### Schema `USGS.InstantaneousValues.Turbidity`
<a id="schema-usgsinstantaneousvaluesturbidity"></a>

| Field | Value |
| --- | --- |
| Name | Turbidity |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/USGS/InstantaneousValues/Turbidity` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/USGS/InstantaneousValues/Turbidity` |
| Type | `object` |

###### Object `Turbidity`
<a id="schema-node-turbidity"></a>

USGS turbidity data. Parameter code 00076.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `site_no` | `string` | `True` | {"description": "USGS site number."} | - | - | - |
| `datetime` | `string` | `True` | {"description": "Date and time of the measurement in ISO-8601 format."} | - | - | - |
| `value` | `double` | `False` | {"description": "Turbidity value."} | - | - | - |
| `exception` | `string` | `False` | {"description": "Exception code when the value is unavailable."} | - | - | - |
| `qualifiers` | array of `string` | `True` | {"description": "Qualifiers for the measurement."} | - | - | - |
| `parameter_cd` | `string` | `True` | {"description": "Parameter code."} | - | - | - |
| `timeseries_cd` | `string` | `True` | {"description": "Timeseries code."} | - | - | - |

#### Schema `USGS.InstantaneousValues.WindSpeed`
<a id="schema-usgsinstantaneousvalueswindspeed"></a>

| Field | Value |
| --- | --- |
| Name | WindSpeed |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/USGS/InstantaneousValues/WindSpeed` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/USGS/InstantaneousValues/WindSpeed` |
| Type | `object` |

###### Object `WindSpeed`
<a id="schema-node-windspeed"></a>

USGS wind speed data. Parameter code 00035.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `site_no` | `string` | `True` | {"description": "USGS site number."} | - | - | - |
| `datetime` | `string` | `True` | {"description": "Date and time of the measurement in ISO-8601 format."} | - | - | - |
| `value` | `double` | `False` | {"description": "Wind speed value."} | - | - | - |
| `exception` | `string` | `False` | {"description": "Exception code when the value is unavailable."} | - | - | - |
| `qualifiers` | array of `string` | `True` | {"description": "Qualifiers for the measurement."} | - | - | - |
| `parameter_cd` | `string` | `True` | {"description": "Parameter code."} | - | - | - |
| `timeseries_cd` | `string` | `True` | {"description": "Timeseries code."} | - | - | - |

#### Schema `USGS.InstantaneousValues.WindDirection`
<a id="schema-usgsinstantaneousvalueswinddirection"></a>

| Field | Value |
| --- | --- |
| Name | WindDirection |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/USGS/InstantaneousValues/WindDirection` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/USGS/InstantaneousValues/WindDirection` |
| Type | `object` |

###### Object `WindDirection`
<a id="schema-node-winddirection"></a>

USGS wind direction data. Parameter codes 00036 and 163695.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `site_no` | `string` | `True` | {"description": "USGS site number."} | - | - | - |
| `datetime` | `string` | `True` | {"description": "Date and time of the measurement in ISO-8601 format."} | - | - | - |
| `value` | `double` | `False` | {"description": "Wind direction value."} | - | - | - |
| `exception` | `string` | `False` | {"description": "Exception code when the value is unavailable."} | - | - | - |
| `qualifiers` | array of `string` | `True` | {"description": "Qualifiers for the measurement."} | - | - | - |
| `parameter_cd` | `string` | `True` | {"description": "Parameter code."} | - | - | - |
| `timeseries_cd` | `string` | `True` | {"description": "Timeseries code."} | - | - | - |

#### Schema `USGS.InstantaneousValues.RelativeHumidity`
<a id="schema-usgsinstantaneousvaluesrelativehumidity"></a>

| Field | Value |
| --- | --- |
| Name | RelativeHumidity |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/USGS/InstantaneousValues/RelativeHumidity` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/USGS/InstantaneousValues/RelativeHumidity` |
| Type | `object` |

###### Object `RelativeHumidity`
<a id="schema-node-relativehumidity"></a>

USGS relative humidity data. Parameter code 00052.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `site_no` | `string` | `True` | {"description": "USGS site number."} | - | - | - |
| `datetime` | `string` | `True` | {"description": "Date and time of the measurement in ISO-8601 format."} | - | - | - |
| `value` | `double` | `False` | {"description": "Relative humidity value."} | - | - | - |
| `exception` | `string` | `False` | {"description": "Exception code when the value is unavailable."} | - | - | - |
| `qualifiers` | array of `string` | `True` | {"description": "Qualifiers for the measurement."} | - | - | - |
| `parameter_cd` | `string` | `True` | {"description": "Parameter code."} | - | - | - |
| `timeseries_cd` | `string` | `True` | {"description": "Timeseries code."} | - | - | - |

#### Schema `USGS.InstantaneousValues.BarometricPressure`
<a id="schema-usgsinstantaneousvaluesbarometricpressure"></a>

| Field | Value |
| --- | --- |
| Name | BarometricPressure |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/USGS/InstantaneousValues/BarometricPressure` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/USGS/InstantaneousValues/BarometricPressure` |
| Type | `object` |

###### Object `BarometricPressure`
<a id="schema-node-barometricpressure"></a>

USGS barometric pressure data. Parameter codes 62605 and 75969.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `site_no` | `string` | `True` | {"description": "USGS site number."} | - | - | - |
| `datetime` | `string` | `True` | {"description": "Date and time of the measurement in ISO-8601 format."} | - | - | - |
| `value` | `double` | `False` | {"description": "Barometric pressure value."} | - | - | - |
| `exception` | `string` | `False` | {"description": "Exception code when the value is unavailable."} | - | - | - |
| `qualifiers` | array of `string` | `True` | {"description": "Qualifiers for the measurement."} | - | - | - |
| `parameter_cd` | `string` | `True` | {"description": "Parameter code."} | - | - | - |
| `timeseries_cd` | `string` | `True` | {"description": "Timeseries code."} | - | - | - |

#### Schema `USGS.InstantaneousValues.AirTemperature`
<a id="schema-usgsinstantaneousvaluesairtemperature"></a>

| Field | Value |
| --- | --- |
| Name | AirTemperature |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/USGS/InstantaneousValues/AirTemperature` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/USGS/InstantaneousValues/AirTemperature` |
| Type | `object` |

###### Object `AirTemperature`
<a id="schema-node-airtemperature"></a>

USGS air temperature data. Parameter code 00020.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `site_no` | `string` | `True` | {"description": "USGS site number."} | - | - | - |
| `datetime` | `string` | `True` | {"description": "Date and time of the measurement in ISO-8601 format."} | - | - | - |
| `value` | `double` | `False` | {"description": "Air temperature value."} | - | - | - |
| `exception` | `string` | `False` | {"description": "Exception code when the value is unavailable."} | - | - | - |
| `qualifiers` | array of `string` | `True` | {"description": "Qualifiers for the measurement."} | - | - | - |
| `parameter_cd` | `string` | `True` | {"description": "Parameter code."} | - | - | - |
| `timeseries_cd` | `string` | `True` | {"description": "Timeseries code."} | - | - | - |

#### Schema `USGS.InstantaneousValues.TurbidityFNU`
<a id="schema-usgsinstantaneousvaluesturbidityfnu"></a>

| Field | Value |
| --- | --- |
| Name | TurbidityFNU |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/USGS/InstantaneousValues/TurbidityFNU` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/USGS/InstantaneousValues/TurbidityFNU` |
| Type | `object` |

###### Object `TurbidityFNU`
<a id="schema-node-turbidityfnu"></a>

USGS turbidity data (FNU). Parameter code 63680.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `site_no` | `string` | `True` | {"description": "USGS site number."} | - | - | - |
| `datetime` | `string` | `True` | {"description": "Date and time of the measurement in ISO-8601 format."} | - | - | - |
| `value` | `double` | `False` | {"description": "Turbidity value."} | - | - | - |
| `exception` | `string` | `False` | {"description": "Exception code when the value is unavailable."} | - | - | - |
| `qualifiers` | array of `string` | `True` | {"description": "Qualifiers for the measurement."} | - | - | - |
| `parameter_cd` | `string` | `True` | {"description": "Parameter code."} | - | - | - |
| `timeseries_cd` | `string` | `True` | {"description": "Timeseries code."} | - | - | - |

#### Schema `USGS.InstantaneousValues.fDOM`
<a id="schema-usgsinstantaneousvaluesfdom"></a>

| Field | Value |
| --- | --- |
| Name | fDOM |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/USGS/InstantaneousValues/fDOM` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/USGS/InstantaneousValues/fDOM` |
| Type | `object` |

###### Object `fDOM`
<a id="schema-node-fdom"></a>

USGS dissolved organic matter fluorescence data (fDOM). Parameter codes 32295 and 32322.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `site_no` | `string` | `True` | {"description": "USGS site number."} | - | - | - |
| `datetime` | `string` | `True` | {"description": "Date and time of the measurement in ISO-8601 format."} | - | - | - |
| `value` | `double` | `False` | {"description": "Dissolved organic matter fluorescence value."} | - | - | - |
| `exception` | `string` | `False` | {"description": "Exception code when the value is unavailable."} | - | - | - |
| `qualifiers` | array of `string` | `True` | {"description": "Qualifiers for the measurement."} | - | - | - |
| `parameter_cd` | `string` | `True` | {"description": "Parameter code."} | - | - | - |
| `timeseries_cd` | `string` | `True` | {"description": "Timeseries code."} | - | - | - |

#### Schema `USGS.InstantaneousValues.ReservoirStorage`
<a id="schema-usgsinstantaneousvaluesreservoirstorage"></a>

| Field | Value |
| --- | --- |
| Name | ReservoirStorage |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/USGS/InstantaneousValues/ReservoirStorage` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/USGS/InstantaneousValues/ReservoirStorage` |
| Type | `object` |

###### Object `ReservoirStorage`
<a id="schema-node-reservoirstorage"></a>

USGS reservoir storage data. Parameter code 00054.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `site_no` | `string` | `True` | {"description": "USGS site number."} | - | - | - |
| `datetime` | `string` | `True` | {"description": "Date and time of the measurement in ISO-8601 format."} | - | - | - |
| `value` | `double` | `False` | {"description": "Reservoir storage value."} | - | - | - |
| `exception` | `string` | `False` | {"description": "Exception code when the value is unavailable."} | - | - | - |
| `qualifiers` | array of `string` | `True` | {"description": "Qualifiers for the measurement."} | - | - | - |
| `parameter_cd` | `string` | `True` | {"description": "Parameter code."} | - | - | - |
| `timeseries_cd` | `string` | `True` | {"description": "Timeseries code."} | - | - | - |

#### Schema `USGS.InstantaneousValues.LakeElevationNGVD29`
<a id="schema-usgsinstantaneousvalueslakeelevationngvd29"></a>

| Field | Value |
| --- | --- |
| Name | LakeElevationNGVD29 |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/USGS/InstantaneousValues/LakeElevationNGVD29` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/USGS/InstantaneousValues/LakeElevationNGVD29` |
| Type | `object` |

###### Object `LakeElevationNGVD29`
<a id="schema-node-lakeelevationngvd29"></a>

USGS lake or reservoir water surface elevation above NGVD 1929, feet. Parameter code 62614.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `site_no` | `string` | `True` | {"description": "USGS site number."} | - | - | - |
| `datetime` | `string` | `True` | {"description": "Date and time of the measurement in ISO-8601 format."} | - | - | - |
| `value` | `double` | `False` | {"description": "Lake elevation above NGVD 1929."} | - | - | - |
| `exception` | `string` | `False` | {"description": "Exception code when the value is unavailable."} | - | - | - |
| `qualifiers` | array of `string` | `True` | {"description": "Qualifiers for the measurement."} | - | - | - |
| `parameter_cd` | `string` | `True` | {"description": "Parameter code."} | - | - | - |
| `timeseries_cd` | `string` | `True` | {"description": "Timeseries code."} | - | - | - |

#### Schema `USGS.InstantaneousValues.WaterDepth`
<a id="schema-usgsinstantaneousvalueswaterdepth"></a>

| Field | Value |
| --- | --- |
| Name | WaterDepth |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/USGS/InstantaneousValues/WaterDepth` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/USGS/InstantaneousValues/WaterDepth` |
| Type | `object` |

###### Object `WaterDepth`
<a id="schema-node-waterdepth"></a>

USGS water depth data. Parameter code 72199.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `site_no` | `string` | `True` | {"description": "USGS site number."} | - | - | - |
| `datetime` | `string` | `True` | {"description": "Date and time of the measurement in ISO-8601 format."} | - | - | - |
| `value` | `double` | `False` | {"description": "Water depth value."} | - | - | - |
| `exception` | `string` | `False` | {"description": "Exception code when the value is unavailable."} | - | - | - |
| `qualifiers` | array of `string` | `True` | {"description": "Qualifiers for the measurement."} | - | - | - |
| `parameter_cd` | `string` | `True` | {"description": "Parameter code."} | - | - | - |
| `timeseries_cd` | `string` | `True` | {"description": "Timeseries code."} | - | - | - |

#### Schema `USGS.InstantaneousValues.EquipmentStatus`
<a id="schema-usgsinstantaneousvaluesequipmentstatus"></a>

| Field | Value |
| --- | --- |
| Name | EquipmentStatus |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/USGS/InstantaneousValues/EquipmentStatus` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/USGS/InstantaneousValues/EquipmentStatus` |
| Type | `object` |

###### Object `EquipmentStatus`
<a id="schema-node-equipmentstatus"></a>

USGS equipment alarm status data. Parameter code 99235.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `site_no` | `string` | `True` | {"description": "USGS site number."} | - | - | - |
| `datetime` | `string` | `True` | {"description": "Date and time of the measurement in ISO-8601 format."} | - | - | - |
| `status` | `string` | `False` | {"description": "Status of equipment alarm as codes."} | - | - | - |
| `parameter_cd` | `string` | `True` | {"description": "Parameter code."} | - | - | - |
| `timeseries_cd` | `string` | `True` | {"description": "Timeseries code."} | - | - | - |

#### Schema `USGS.InstantaneousValues.TidallyFilteredDischarge`
<a id="schema-usgsinstantaneousvaluestidallyfiltereddischarge"></a>

| Field | Value |
| --- | --- |
| Name | TidallyFilteredDischarge |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/USGS/InstantaneousValues/TidallyFilteredDischarge` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/USGS/InstantaneousValues/TidallyFilteredDischarge` |
| Type | `object` |

###### Object `TidallyFilteredDischarge`
<a id="schema-node-tidallyfiltereddischarge"></a>

USGS tidally filtered discharge data. Parameter code 72137.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `site_no` | `string` | `True` | {"description": "USGS site number."} | - | - | - |
| `datetime` | `string` | `True` | {"description": "Date and time of the measurement in ISO-8601 format."} | - | - | - |
| `value` | `double` | `False` | {"description": "Tidally filtered discharge value."} | - | - | - |
| `exception` | `string` | `False` | {"description": "Exception code when the value is unavailable."} | - | - | - |
| `qualifiers` | array of `string` | `True` | {"description": "Qualifiers for the measurement."} | - | - | - |
| `parameter_cd` | `string` | `True` | {"description": "Parameter code."} | - | - | - |
| `timeseries_cd` | `string` | `True` | {"description": "Timeseries code."} | - | - | - |

#### Schema `USGS.InstantaneousValues.WaterVelocity`
<a id="schema-usgsinstantaneousvalueswatervelocity"></a>

| Field | Value |
| --- | --- |
| Name | WaterVelocity |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/USGS/InstantaneousValues/WaterVelocity` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/USGS/InstantaneousValues/WaterVelocity` |
| Type | `object` |

###### Object `WaterVelocity`
<a id="schema-node-watervelocity"></a>

USGS water velocity data. Parameter code 72254.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `site_no` | `string` | `True` | {"description": "USGS site number."} | - | - | - |
| `datetime` | `string` | `True` | {"description": "Date and time of the measurement in ISO-8601 format."} | - | - | - |
| `value` | `double` | `False` | {"description": "Water velocity value."} | - | - | - |
| `exception` | `string` | `False` | {"description": "Exception code when the value is unavailable."} | - | - | - |
| `qualifiers` | array of `string` | `True` | {"description": "Qualifiers for the measurement."} | - | - | - |
| `parameter_cd` | `string` | `True` | {"description": "Parameter code."} | - | - | - |
| `timeseries_cd` | `string` | `True` | {"description": "Timeseries code."} | - | - | - |

#### Schema `USGS.InstantaneousValues.EstuaryElevationNGVD29`
<a id="schema-usgsinstantaneousvaluesestuaryelevationngvd29"></a>

| Field | Value |
| --- | --- |
| Name | EstuaryElevationNGVD29 |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/USGS/InstantaneousValues/EstuaryElevationNGVD29` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/USGS/InstantaneousValues/EstuaryElevationNGVD29` |
| Type | `object` |

###### Object `EstuaryElevationNGVD29`
<a id="schema-node-estuaryelevationngvd29"></a>

USGS estuary or ocean water surface elevation above NGVD 1929, feet. Parameter code 62619.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `site_no` | `string` | `True` | {"description": "USGS site number."} | - | - | - |
| `datetime` | `string` | `True` | {"description": "Date and time of the measurement in ISO-8601 format."} | - | - | - |
| `value` | `double` | `False` | {"description": "Estuary or ocean water surface elevation above NGVD 1929."} | - | - | - |
| `exception` | `string` | `False` | {"description": "Exception code when the value is unavailable."} | - | - | - |
| `qualifiers` | array of `string` | `True` | {"description": "Qualifiers for the measurement."} | - | - | - |
| `parameter_cd` | `string` | `True` | {"description": "Parameter code."} | - | - | - |
| `timeseries_cd` | `string` | `True` | {"description": "Timeseries code."} | - | - | - |

#### Schema `USGS.InstantaneousValues.LakeElevationNAVD88`
<a id="schema-usgsinstantaneousvalueslakeelevationnavd88"></a>

| Field | Value |
| --- | --- |
| Name | LakeElevationNAVD88 |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/USGS/InstantaneousValues/LakeElevationNAVD88` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/USGS/InstantaneousValues/LakeElevationNAVD88` |
| Type | `object` |

###### Object `LakeElevationNAVD88`
<a id="schema-node-lakeelevationnavd88"></a>

USGS lake or reservoir water surface elevation above NAVD 1988, feet. Parameter code 62615.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `site_no` | `string` | `True` | {"description": "USGS site number."} | - | - | - |
| `datetime` | `string` | `True` | {"description": "Date and time of the measurement in ISO-8601 format."} | - | - | - |
| `value` | `double` | `False` | {"description": "Lake elevation above NAVD 1988."} | - | - | - |
| `exception` | `string` | `False` | {"description": "Exception code when the value is unavailable."} | - | - | - |
| `qualifiers` | array of `string` | `True` | {"description": "Qualifiers for the measurement."} | - | - | - |
| `parameter_cd` | `string` | `True` | {"description": "Parameter code."} | - | - | - |
| `timeseries_cd` | `string` | `True` | {"description": "Timeseries code."} | - | - | - |

#### Schema `USGS.InstantaneousValues.Salinity`
<a id="schema-usgsinstantaneousvaluessalinity"></a>

| Field | Value |
| --- | --- |
| Name | Salinity |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/USGS/InstantaneousValues/Salinity` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/USGS/InstantaneousValues/Salinity` |
| Type | `object` |

###### Object `Salinity`
<a id="schema-node-salinity"></a>

USGS salinity data. Parameter code 00480.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `site_no` | `string` | `True` | {"description": "USGS site number."} | - | - | - |
| `datetime` | `string` | `True` | {"description": "Date and time of the measurement in ISO-8601 format."} | - | - | - |
| `value` | `double` | `False` | {"description": "Salinity value."} | - | - | - |
| `exception` | `string` | `False` | {"description": "Exception code when the value is unavailable."} | - | - | - |
| `qualifiers` | array of `string` | `True` | {"description": "Qualifiers for the measurement."} | - | - | - |
| `parameter_cd` | `string` | `True` | {"description": "Parameter code."} | - | - | - |
| `timeseries_cd` | `string` | `True` | {"description": "Timeseries code."} | - | - | - |

#### Schema `USGS.InstantaneousValues.GateOpening`
<a id="schema-usgsinstantaneousvaluesgateopening"></a>

| Field | Value |
| --- | --- |
| Name | GateOpening |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/USGS/InstantaneousValues/GateOpening` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/USGS/InstantaneousValues/GateOpening` |
| Type | `object` |

###### Object `GateOpening`
<a id="schema-node-gateopening"></a>

USGS gate opening data. Parameter code 45592.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `site_no` | `string` | `True` | {"description": "USGS site number."} | - | - | - |
| `datetime` | `string` | `True` | {"description": "Date and time of the measurement in ISO-8601 format."} | - | - | - |
| `value` | `double` | `False` | {"description": "Gate opening value."} | - | - | - |
| `exception` | `string` | `False` | {"description": "Exception code when the value is unavailable."} | - | - | - |
| `qualifiers` | array of `string` | `True` | {"description": "Qualifiers for the measurement."} | - | - | - |
| `parameter_cd` | `string` | `True` | {"description": "Parameter code."} | - | - | - |
| `timeseries_cd` | `string` | `True` | {"description": "Timeseries code."} | - | - | - |

### Schemagroup `USGS.InstantaneousValues.avro`
<a id="schemagroup-usgsinstantaneousvaluesavro"></a>

#### Schema `USGS.InstantaneousValues.OtherParameter`
<a id="schema-usgsinstantaneousvaluesotherparameter"></a>

| Field | Value |
| --- | --- |
| Name | OtherParameter |
| Format | Avro/1.11.3 |
| Default version | 1 |
| Description | USGS other parameter data. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | OtherParameter |
| Namespace | USGS.InstantaneousValues |
| Type | `record` |
| Doc | USGS other parameter data. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `site_no` | `string` | {"description": "USGS site number."} | `-` |
| `datetime` | `string` | {"description": "Date and time of the measurement in ISO-8601 format."} | `-` |
| `value` | `double` \| `null` | {"description": "Value."} | `-` |
| `exception` | `string` \| `null` | {"description": "Exception code when the value is unavailable."} | `-` |
| `qualifiers` | array of `string` | {"description": "Qualifiers for the measurement."} | `-` |
| `parameter_cd` | `string` | {"description": "Parameter code."} | `-` |
| `timeseries_cd` | `string` | {"description": "Timeseries code."} | `-` |

#### Schema `USGS.InstantaneousValues.Precipitation`
<a id="schema-usgsinstantaneousvaluesprecipitation"></a>

| Field | Value |
| --- | --- |
| Name | Precipitation |
| Format | Avro/1.11.3 |
| Default version | 1 |
| Description | USGS precipitation data. Parameter code 00045. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | Precipitation |
| Namespace | USGS.InstantaneousValues |
| Type | `record` |
| Doc | USGS precipitation data. Parameter code 00045. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `site_no` | `string` | {"description": "USGS site number."} | `-` |
| `datetime` | `string` | {"description": "Date and time of the measurement in ISO-8601 format."} | `-` |
| `value` | `double` \| `null` | {"description": "Precipitation value, inches."} | `-` |
| `exception` | `string` \| `null` | {"description": "Exception code when the value is unavailable."} | `-` |
| `qualifiers` | array of `string` | {"description": "Qualifiers for the measurement."} | `-` |
| `parameter_cd` | `string` | {"description": "Parameter code."} | `-` |
| `timeseries_cd` | `string` | {"description": "Timeseries code."} | `-` |

#### Schema `USGS.InstantaneousValues.Streamflow`
<a id="schema-usgsinstantaneousvaluesstreamflow"></a>

| Field | Value |
| --- | --- |
| Name | Streamflow |
| Format | Avro/1.11.3 |
| Default version | 1 |
| Description | USGS streamflow data. Parameter code 00060. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | Streamflow |
| Namespace | USGS.InstantaneousValues |
| Type | `record` |
| Doc | USGS streamflow data. Parameter code 00060. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `site_no` | `string` | {"description": "USGS site number."} | `-` |
| `datetime` | `string` | {"description": "Date and time of the measurement in ISO-8601 format."} | `-` |
| `value` | `double` \| `null` | {"description": "Discharge value."} | `-` |
| `exception` | `string` \| `null` | {"description": "Exception code when the value is unavailable."} | `-` |
| `qualifiers` | array of `string` | {"description": "Qualifiers for the measurement."} | `-` |
| `parameter_cd` | `string` | {"description": "Parameter code."} | `-` |
| `timeseries_cd` | `string` | {"description": "Timeseries code."} | `-` |

#### Schema `USGS.InstantaneousValues.GageHeight`
<a id="schema-usgsinstantaneousvaluesgageheight"></a>

| Field | Value |
| --- | --- |
| Name | GageHeight |
| Format | Avro/1.11.3 |
| Default version | 1 |
| Description | USGS gage height data. Parameter code 00065. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | GageHeight |
| Namespace | USGS.InstantaneousValues |
| Type | `record` |
| Doc | USGS gage height data. Parameter code 00065. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `site_no` | `string` | {"description": "USGS site number."} | `-` |
| `datetime` | `string` | {"description": "Date and time of the measurement in ISO-8601 format."} | `-` |
| `value` | `double` \| `null` | {"description": "Gage height value."} | `-` |
| `exception` | `string` \| `null` | {"description": "Exception code when the value is unavailable."} | `-` |
| `qualifiers` | array of `string` | {"description": "Qualifiers for the measurement."} | `-` |
| `parameter_cd` | `string` | {"description": "Parameter code."} | `-` |
| `timeseries_cd` | `string` | {"description": "Timeseries code."} | `-` |

#### Schema `USGS.InstantaneousValues.WaterTemperature`
<a id="schema-usgsinstantaneousvalueswatertemperature"></a>

| Field | Value |
| --- | --- |
| Name | WaterTemperature |
| Format | Avro/1.11.3 |
| Default version | 1 |
| Description | USGS water temperature data. Parameter code 00010. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | WaterTemperature |
| Namespace | USGS.InstantaneousValues |
| Type | `record` |
| Doc | USGS water temperature data. Parameter code 00010. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `site_no` | `string` | {"description": "USGS site number."} | `-` |
| `datetime` | `string` | {"description": "Date and time of the measurement in ISO-8601 format."} | `-` |
| `value` | `double` \| `null` | {"description": "Water temperature value."} | `-` |
| `exception` | `string` \| `null` | {"description": "Exception code when the value is unavailable."} | `-` |
| `qualifiers` | array of `string` | {"description": "Qualifiers for the measurement."} | `-` |
| `parameter_cd` | `string` | {"description": "Parameter code."} | `-` |
| `timeseries_cd` | `string` | {"description": "Timeseries code."} | `-` |

#### Schema `USGS.InstantaneousValues.DissolvedOxygen`
<a id="schema-usgsinstantaneousvaluesdissolvedoxygen"></a>

| Field | Value |
| --- | --- |
| Name | DissolvedOxygen |
| Format | Avro/1.11.3 |
| Default version | 1 |
| Description | USGS dissolved oxygen data. Parameter code 00300. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | DissolvedOxygen |
| Namespace | USGS.InstantaneousValues |
| Type | `record` |
| Doc | USGS dissolved oxygen data. Parameter code 00300. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `site_no` | `string` | {"description": "USGS site number."} | `-` |
| `datetime` | `string` | {"description": "Date and time of the measurement in ISO-8601 format."} | `-` |
| `value` | `double` \| `null` | {"description": "Dissolved oxygen value."} | `-` |
| `exception` | `string` \| `null` | {"description": "Exception code when the value is unavailable."} | `-` |
| `qualifiers` | array of `string` | {"description": "Qualifiers for the measurement."} | `-` |
| `parameter_cd` | `string` | {"description": "Parameter code."} | `-` |
| `timeseries_cd` | `string` | {"description": "Timeseries code."} | `-` |

#### Schema `USGS.InstantaneousValues.pH`
<a id="schema-usgsinstantaneousvaluesph"></a>

| Field | Value |
| --- | --- |
| Name | pH |
| Format | Avro/1.11.3 |
| Default version | 1 |
| Description | USGS pH data. Parameter code 00400. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | pH |
| Namespace | USGS.InstantaneousValues |
| Type | `record` |
| Doc | USGS pH data. Parameter code 00400. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `site_no` | `string` | {"description": "USGS site number."} | `-` |
| `datetime` | `string` | {"description": "Date and time of the measurement in ISO-8601 format."} | `-` |
| `value` | `double` \| `null` | {"description": "pH value."} | `-` |
| `exception` | `string` \| `null` | {"description": "Exception code when the value is unavailable."} | `-` |
| `qualifiers` | array of `string` | {"description": "Qualifiers for the measurement."} | `-` |
| `parameter_cd` | `string` | {"description": "Parameter code."} | `-` |
| `timeseries_cd` | `string` | {"description": "Timeseries code."} | `-` |

#### Schema `USGS.InstantaneousValues.SpecificConductance`
<a id="schema-usgsinstantaneousvaluesspecificconductance"></a>

| Field | Value |
| --- | --- |
| Name | SpecificConductance |
| Format | Avro/1.11.3 |
| Default version | 1 |
| Description | USGS specific conductance data. Parameter code 00095. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | SpecificConductance |
| Namespace | USGS.InstantaneousValues |
| Type | `record` |
| Doc | USGS specific conductance data. Parameter code 00095. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `site_no` | `string` | {"description": "USGS site number."} | `-` |
| `datetime` | `string` | {"description": "Date and time of the measurement in ISO-8601 format."} | `-` |
| `value` | `double` \| `null` | {"description": "Specific conductance value."} | `-` |
| `exception` | `string` \| `null` | {"description": "Exception code when the value is unavailable."} | `-` |
| `qualifiers` | array of `string` | {"description": "Qualifiers for the measurement."} | `-` |
| `parameter_cd` | `string` | {"description": "Parameter code."} | `-` |
| `timeseries_cd` | `string` | {"description": "Timeseries code."} | `-` |

#### Schema `USGS.InstantaneousValues.Turbidity`
<a id="schema-usgsinstantaneousvaluesturbidity"></a>

| Field | Value |
| --- | --- |
| Name | Turbidity |
| Format | Avro/1.11.3 |
| Default version | 1 |
| Description | USGS turbidity data. Parameter code 00076. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | Turbidity |
| Namespace | USGS.InstantaneousValues |
| Type | `record` |
| Doc | USGS turbidity data. Parameter code 00076. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `site_no` | `string` | {"description": "USGS site number."} | `-` |
| `datetime` | `string` | {"description": "Date and time of the measurement in ISO-8601 format."} | `-` |
| `value` | `double` \| `null` | {"description": "Turbidity value."} | `-` |
| `exception` | `string` \| `null` | {"description": "Exception code when the value is unavailable."} | `-` |
| `qualifiers` | array of `string` | {"description": "Qualifiers for the measurement."} | `-` |
| `parameter_cd` | `string` | {"description": "Parameter code."} | `-` |
| `timeseries_cd` | `string` | {"description": "Timeseries code."} | `-` |

#### Schema `USGS.InstantaneousValues.WindSpeed`
<a id="schema-usgsinstantaneousvalueswindspeed"></a>

| Field | Value |
| --- | --- |
| Name | WindSpeed |
| Format | Avro/1.11.3 |
| Default version | 1 |
| Description | USGS wind speed data. Parameter code 00035. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | WindSpeed |
| Namespace | USGS.InstantaneousValues |
| Type | `record` |
| Doc | USGS wind speed data. Parameter code 00035. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `site_no` | `string` | {"description": "USGS site number."} | `-` |
| `datetime` | `string` | {"description": "Date and time of the measurement in ISO-8601 format."} | `-` |
| `value` | `double` \| `null` | {"description": "Wind speed value."} | `-` |
| `exception` | `string` \| `null` | {"description": "Exception code when the value is unavailable."} | `-` |
| `qualifiers` | array of `string` | {"description": "Qualifiers for the measurement."} | `-` |
| `parameter_cd` | `string` | {"description": "Parameter code."} | `-` |
| `timeseries_cd` | `string` | {"description": "Timeseries code."} | `-` |

#### Schema `USGS.InstantaneousValues.WindDirection`
<a id="schema-usgsinstantaneousvalueswinddirection"></a>

| Field | Value |
| --- | --- |
| Name | WindDirection |
| Format | Avro/1.11.3 |
| Default version | 1 |
| Description | USGS wind direction data. Parameter codes 00036 and 163695. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | WindDirection |
| Namespace | USGS.InstantaneousValues |
| Type | `record` |
| Doc | USGS wind direction data. Parameter codes 00036 and 163695. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `site_no` | `string` | {"description": "USGS site number."} | `-` |
| `datetime` | `string` | {"description": "Date and time of the measurement in ISO-8601 format."} | `-` |
| `value` | `double` \| `null` | {"description": "Wind direction value."} | `-` |
| `exception` | `string` \| `null` | {"description": "Exception code when the value is unavailable."} | `-` |
| `qualifiers` | array of `string` | {"description": "Qualifiers for the measurement."} | `-` |
| `parameter_cd` | `string` | {"description": "Parameter code."} | `-` |
| `timeseries_cd` | `string` | {"description": "Timeseries code."} | `-` |

#### Schema `USGS.InstantaneousValues.RelativeHumidity`
<a id="schema-usgsinstantaneousvaluesrelativehumidity"></a>

| Field | Value |
| --- | --- |
| Name | RelativeHumidity |
| Format | Avro/1.11.3 |
| Default version | 1 |
| Description | USGS relative humidity data. Parameter code 00052. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | RelativeHumidity |
| Namespace | USGS.InstantaneousValues |
| Type | `record` |
| Doc | USGS relative humidity data. Parameter code 00052. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `site_no` | `string` | {"description": "USGS site number."} | `-` |
| `datetime` | `string` | {"description": "Date and time of the measurement in ISO-8601 format."} | `-` |
| `value` | `double` \| `null` | {"description": "Relative humidity value."} | `-` |
| `exception` | `string` \| `null` | {"description": "Exception code when the value is unavailable."} | `-` |
| `qualifiers` | array of `string` | {"description": "Qualifiers for the measurement."} | `-` |
| `parameter_cd` | `string` | {"description": "Parameter code."} | `-` |
| `timeseries_cd` | `string` | {"description": "Timeseries code."} | `-` |

#### Schema `USGS.InstantaneousValues.BarometricPressure`
<a id="schema-usgsinstantaneousvaluesbarometricpressure"></a>

| Field | Value |
| --- | --- |
| Name | BarometricPressure |
| Format | Avro/1.11.3 |
| Default version | 1 |
| Description | USGS barometric pressure data. Parameter codes 62605 and 75969. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | BarometricPressure |
| Namespace | USGS.InstantaneousValues |
| Type | `record` |
| Doc | USGS barometric pressure data. Parameter codes 62605 and 75969. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `site_no` | `string` | {"description": "USGS site number."} | `-` |
| `datetime` | `string` | {"description": "Date and time of the measurement in ISO-8601 format."} | `-` |
| `value` | `double` \| `null` | {"description": "Barometric pressure value."} | `-` |
| `exception` | `string` \| `null` | {"description": "Exception code when the value is unavailable."} | `-` |
| `qualifiers` | array of `string` | {"description": "Qualifiers for the measurement."} | `-` |
| `parameter_cd` | `string` | {"description": "Parameter code."} | `-` |
| `timeseries_cd` | `string` | {"description": "Timeseries code."} | `-` |

#### Schema `USGS.InstantaneousValues.AirTemperature`
<a id="schema-usgsinstantaneousvaluesairtemperature"></a>

| Field | Value |
| --- | --- |
| Name | AirTemperature |
| Format | Avro/1.11.3 |
| Default version | 1 |
| Description | USGS air temperature data. Parameter code 00020. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | AirTemperature |
| Namespace | USGS.InstantaneousValues |
| Type | `record` |
| Doc | USGS air temperature data. Parameter code 00020. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `site_no` | `string` | {"description": "USGS site number."} | `-` |
| `datetime` | `string` | {"description": "Date and time of the measurement in ISO-8601 format."} | `-` |
| `value` | `double` \| `null` | {"description": "Air temperature value."} | `-` |
| `exception` | `string` \| `null` | {"description": "Exception code when the value is unavailable."} | `-` |
| `qualifiers` | array of `string` | {"description": "Qualifiers for the measurement."} | `-` |
| `parameter_cd` | `string` | {"description": "Parameter code."} | `-` |
| `timeseries_cd` | `string` | {"description": "Timeseries code."} | `-` |

#### Schema `USGS.InstantaneousValues.TurbidityFNU`
<a id="schema-usgsinstantaneousvaluesturbidityfnu"></a>

| Field | Value |
| --- | --- |
| Name | TurbidityFNU |
| Format | Avro/1.11.3 |
| Default version | 1 |
| Description | USGS turbidity data (FNU). Parameter code 63680. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | TurbidityFNU |
| Namespace | USGS.InstantaneousValues |
| Type | `record` |
| Doc | USGS turbidity data (FNU). Parameter code 63680. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `site_no` | `string` | {"description": "USGS site number."} | `-` |
| `datetime` | `string` | {"description": "Date and time of the measurement in ISO-8601 format."} | `-` |
| `value` | `double` \| `null` | {"description": "Turbidity value."} | `-` |
| `exception` | `string` \| `null` | {"description": "Exception code when the value is unavailable."} | `-` |
| `qualifiers` | array of `string` | {"description": "Qualifiers for the measurement."} | `-` |
| `parameter_cd` | `string` | {"description": "Parameter code."} | `-` |
| `timeseries_cd` | `string` | {"description": "Timeseries code."} | `-` |

#### Schema `USGS.InstantaneousValues.fDOM`
<a id="schema-usgsinstantaneousvaluesfdom"></a>

| Field | Value |
| --- | --- |
| Name | fDOM |
| Format | Avro/1.11.3 |
| Default version | 1 |
| Description | USGS dissolved organic matter fluorescence data (fDOM). Parameter codes 32295 and 32322. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | fDOM |
| Namespace | USGS.InstantaneousValues |
| Type | `record` |
| Doc | USGS dissolved organic matter fluorescence data (fDOM). Parameter codes 32295 and 32322. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `site_no` | `string` | {"description": "USGS site number."} | `-` |
| `datetime` | `string` | {"description": "Date and time of the measurement in ISO-8601 format."} | `-` |
| `value` | `double` \| `null` | {"description": "Dissolved organic matter fluorescence value."} | `-` |
| `exception` | `string` \| `null` | {"description": "Exception code when the value is unavailable."} | `-` |
| `qualifiers` | array of `string` | {"description": "Qualifiers for the measurement."} | `-` |
| `parameter_cd` | `string` | {"description": "Parameter code."} | `-` |
| `timeseries_cd` | `string` | {"description": "Timeseries code."} | `-` |

#### Schema `USGS.InstantaneousValues.ReservoirStorage`
<a id="schema-usgsinstantaneousvaluesreservoirstorage"></a>

| Field | Value |
| --- | --- |
| Name | ReservoirStorage |
| Format | Avro/1.11.3 |
| Default version | 1 |
| Description | USGS reservoir storage data. Parameter code 00054. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | ReservoirStorage |
| Namespace | USGS.InstantaneousValues |
| Type | `record` |
| Doc | USGS reservoir storage data. Parameter code 00054. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `site_no` | `string` | {"description": "USGS site number."} | `-` |
| `datetime` | `string` | {"description": "Date and time of the measurement in ISO-8601 format."} | `-` |
| `value` | `double` \| `null` | {"description": "Reservoir storage value."} | `-` |
| `exception` | `string` \| `null` | {"description": "Exception code when the value is unavailable."} | `-` |
| `qualifiers` | array of `string` | {"description": "Qualifiers for the measurement."} | `-` |
| `parameter_cd` | `string` | {"description": "Parameter code."} | `-` |
| `timeseries_cd` | `string` | {"description": "Timeseries code."} | `-` |

#### Schema `USGS.InstantaneousValues.LakeElevationNGVD29`
<a id="schema-usgsinstantaneousvalueslakeelevationngvd29"></a>

| Field | Value |
| --- | --- |
| Name | LakeElevationNGVD29 |
| Format | Avro/1.11.3 |
| Default version | 1 |
| Description | USGS lake or reservoir water surface elevation above NGVD 1929, feet. Parameter code 62614. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | LakeElevationNGVD29 |
| Namespace | USGS.InstantaneousValues |
| Type | `record` |
| Doc | USGS lake or reservoir water surface elevation above NGVD 1929, feet. Parameter code 62614. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `site_no` | `string` | {"description": "USGS site number."} | `-` |
| `datetime` | `string` | {"description": "Date and time of the measurement in ISO-8601 format."} | `-` |
| `value` | `double` \| `null` | {"description": "Lake elevation above NGVD 1929."} | `-` |
| `exception` | `string` \| `null` | {"description": "Exception code when the value is unavailable."} | `-` |
| `qualifiers` | array of `string` | {"description": "Qualifiers for the measurement."} | `-` |
| `parameter_cd` | `string` | {"description": "Parameter code."} | `-` |
| `timeseries_cd` | `string` | {"description": "Timeseries code."} | `-` |

#### Schema `USGS.InstantaneousValues.WaterDepth`
<a id="schema-usgsinstantaneousvalueswaterdepth"></a>

| Field | Value |
| --- | --- |
| Name | WaterDepth |
| Format | Avro/1.11.3 |
| Default version | 1 |
| Description | USGS water depth data. Parameter code 72199. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | WaterDepth |
| Namespace | USGS.InstantaneousValues |
| Type | `record` |
| Doc | USGS water depth data. Parameter code 72199. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `site_no` | `string` | {"description": "USGS site number."} | `-` |
| `datetime` | `string` | {"description": "Date and time of the measurement in ISO-8601 format."} | `-` |
| `value` | `double` \| `null` | {"description": "Water depth value."} | `-` |
| `exception` | `string` \| `null` | {"description": "Exception code when the value is unavailable."} | `-` |
| `qualifiers` | array of `string` | {"description": "Qualifiers for the measurement."} | `-` |
| `parameter_cd` | `string` | {"description": "Parameter code."} | `-` |
| `timeseries_cd` | `string` | {"description": "Timeseries code."} | `-` |

#### Schema `USGS.InstantaneousValues.EquipmentStatus`
<a id="schema-usgsinstantaneousvaluesequipmentstatus"></a>

| Field | Value |
| --- | --- |
| Name | EquipmentStatus |
| Format | Avro/1.11.3 |
| Default version | 1 |
| Description | USGS equipment alarm status data. Parameter code 99235. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | EquipmentStatus |
| Namespace | USGS.InstantaneousValues |
| Type | `record` |
| Doc | USGS equipment alarm status data. Parameter code 99235. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `site_no` | `string` | {"description": "USGS site number."} | `-` |
| `datetime` | `string` | {"description": "Date and time of the measurement in ISO-8601 format."} | `-` |
| `status` | `string` \| `null` | {"description": "Status of equipment alarm as codes."} | `-` |
| `parameter_cd` | `string` | {"description": "Parameter code."} | `-` |
| `timeseries_cd` | `string` | {"description": "Timeseries code."} | `-` |

#### Schema `USGS.InstantaneousValues.TidallyFilteredDischarge`
<a id="schema-usgsinstantaneousvaluestidallyfiltereddischarge"></a>

| Field | Value |
| --- | --- |
| Name | TidallyFilteredDischarge |
| Format | Avro/1.11.3 |
| Default version | 1 |
| Description | USGS tidally filtered discharge data. Parameter code 72137. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | TidallyFilteredDischarge |
| Namespace | USGS.InstantaneousValues |
| Type | `record` |
| Doc | USGS tidally filtered discharge data. Parameter code 72137. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `site_no` | `string` | {"description": "USGS site number."} | `-` |
| `datetime` | `string` | {"description": "Date and time of the measurement in ISO-8601 format."} | `-` |
| `value` | `double` \| `null` | {"description": "Tidally filtered discharge value."} | `-` |
| `exception` | `string` \| `null` | {"description": "Exception code when the value is unavailable."} | `-` |
| `qualifiers` | array of `string` | {"description": "Qualifiers for the measurement."} | `-` |
| `parameter_cd` | `string` | {"description": "Parameter code."} | `-` |
| `timeseries_cd` | `string` | {"description": "Timeseries code."} | `-` |

#### Schema `USGS.InstantaneousValues.WaterVelocity`
<a id="schema-usgsinstantaneousvalueswatervelocity"></a>

| Field | Value |
| --- | --- |
| Name | WaterVelocity |
| Format | Avro/1.11.3 |
| Default version | 1 |
| Description | USGS water velocity data. Parameter code 72254. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | WaterVelocity |
| Namespace | USGS.InstantaneousValues |
| Type | `record` |
| Doc | USGS water velocity data. Parameter code 72254. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `site_no` | `string` | {"description": "USGS site number."} | `-` |
| `datetime` | `string` | {"description": "Date and time of the measurement in ISO-8601 format."} | `-` |
| `value` | `double` \| `null` | {"description": "Water velocity value."} | `-` |
| `exception` | `string` \| `null` | {"description": "Exception code when the value is unavailable."} | `-` |
| `qualifiers` | array of `string` | {"description": "Qualifiers for the measurement."} | `-` |
| `parameter_cd` | `string` | {"description": "Parameter code."} | `-` |
| `timeseries_cd` | `string` | {"description": "Timeseries code."} | `-` |

#### Schema `USGS.InstantaneousValues.EstuaryElevationNGVD29`
<a id="schema-usgsinstantaneousvaluesestuaryelevationngvd29"></a>

| Field | Value |
| --- | --- |
| Name | EstuaryElevationNGVD29 |
| Format | Avro/1.11.3 |
| Default version | 1 |
| Description | USGS estuary or ocean water surface elevation above NGVD 1929, feet. Parameter code 62619. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | EstuaryElevationNGVD29 |
| Namespace | USGS.InstantaneousValues |
| Type | `record` |
| Doc | USGS estuary or ocean water surface elevation above NGVD 1929, feet. Parameter code 62619. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `site_no` | `string` | {"description": "USGS site number."} | `-` |
| `datetime` | `string` | {"description": "Date and time of the measurement in ISO-8601 format."} | `-` |
| `value` | `double` \| `null` | {"description": "Estuary or ocean water surface elevation above NGVD 1929."} | `-` |
| `exception` | `string` \| `null` | {"description": "Exception code when the value is unavailable."} | `-` |
| `qualifiers` | array of `string` | {"description": "Qualifiers for the measurement."} | `-` |
| `parameter_cd` | `string` | {"description": "Parameter code."} | `-` |
| `timeseries_cd` | `string` | {"description": "Timeseries code."} | `-` |

#### Schema `USGS.InstantaneousValues.LakeElevationNAVD88`
<a id="schema-usgsinstantaneousvalueslakeelevationnavd88"></a>

| Field | Value |
| --- | --- |
| Name | LakeElevationNAVD88 |
| Format | Avro/1.11.3 |
| Default version | 1 |
| Description | USGS lake or reservoir water surface elevation above NAVD 1988, feet. Parameter code 62615. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | LakeElevationNAVD88 |
| Namespace | USGS.InstantaneousValues |
| Type | `record` |
| Doc | USGS lake or reservoir water surface elevation above NAVD 1988, feet. Parameter code 62615. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `site_no` | `string` | {"description": "USGS site number."} | `-` |
| `datetime` | `string` | {"description": "Date and time of the measurement in ISO-8601 format."} | `-` |
| `value` | `double` \| `null` | {"description": "Lake elevation above NAVD 1988."} | `-` |
| `exception` | `string` \| `null` | {"description": "Exception code when the value is unavailable."} | `-` |
| `qualifiers` | array of `string` | {"description": "Qualifiers for the measurement."} | `-` |
| `parameter_cd` | `string` | {"description": "Parameter code."} | `-` |
| `timeseries_cd` | `string` | {"description": "Timeseries code."} | `-` |

#### Schema `USGS.InstantaneousValues.Salinity`
<a id="schema-usgsinstantaneousvaluessalinity"></a>

| Field | Value |
| --- | --- |
| Name | Salinity |
| Format | Avro/1.11.3 |
| Default version | 1 |
| Description | USGS salinity data. Parameter code 00480. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | Salinity |
| Namespace | USGS.InstantaneousValues |
| Type | `record` |
| Doc | USGS salinity data. Parameter code 00480. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `site_no` | `string` | {"description": "USGS site number."} | `-` |
| `datetime` | `string` | {"description": "Date and time of the measurement in ISO-8601 format."} | `-` |
| `value` | `double` \| `null` | {"description": "Salinity value."} | `-` |
| `exception` | `string` \| `null` | {"description": "Exception code when the value is unavailable."} | `-` |
| `qualifiers` | array of `string` | {"description": "Qualifiers for the measurement."} | `-` |
| `parameter_cd` | `string` | {"description": "Parameter code."} | `-` |
| `timeseries_cd` | `string` | {"description": "Timeseries code."} | `-` |

#### Schema `USGS.InstantaneousValues.GateOpening`
<a id="schema-usgsinstantaneousvaluesgateopening"></a>

| Field | Value |
| --- | --- |
| Name | GateOpening |
| Format | Avro/1.11.3 |
| Default version | 1 |
| Description | USGS gate opening data. Parameter code 45592. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | GateOpening |
| Namespace | USGS.InstantaneousValues |
| Type | `record` |
| Doc | USGS gate opening data. Parameter code 45592. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `site_no` | `string` | {"description": "USGS site number."} | `-` |
| `datetime` | `string` | {"description": "Date and time of the measurement in ISO-8601 format."} | `-` |
| `value` | `double` \| `null` | {"description": "Gate opening value."} | `-` |
| `exception` | `string` \| `null` | {"description": "Exception code when the value is unavailable."} | `-` |
| `qualifiers` | array of `string` | {"description": "Qualifiers for the measurement."} | `-` |
| `parameter_cd` | `string` | {"description": "Parameter code."} | `-` |
| `timeseries_cd` | `string` | {"description": "Timeseries code."} | `-` |
