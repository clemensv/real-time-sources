# USGS NWIS Water Quality - Continuous Water Quality Sensor Data Events

**usgs-nwis-wq** is a bridge that polls the [USGS Water Services](https://waterservices.usgs.gov/) Instantaneous Values Service API for continuous water quality sensor readings from over 3,000 monitoring sites across the United States. The bridge focuses specifically on water quality parameters: dissolved oxygen, pH, water temperature, specific conductance, turbidity, and nitrate.

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

### Endpoint `USGS.WaterQuality.Sites.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`USGS.WaterQuality.Sites`](#messagegroup-usgswaterqualitysites) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `usgs-nwis-wq` |
| Kafka key | `{site_number}` |
| Deployed | False |

### Endpoint `USGS.WaterQuality.Readings.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`USGS.WaterQuality.Readings`](#messagegroup-usgswaterqualityreadings) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `usgs-nwis-wq` |
| Kafka key | `{site_number}/{parameter_code}` |
| Deployed | False |

## Messagegroups

### Messagegroup `USGS.WaterQuality.Sites`
<a id="messagegroup-usgswaterqualitysites"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `USGS.WaterQuality.Sites.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `USGS.WaterQuality.Sites.MonitoringSite`
<a id="message-usgswaterqualitysitesmonitoringsite"></a>

USGS water quality monitoring site reference data. Describes a physical monitoring location equipped with continuous water quality sensors.

| Field | Value |
| --- | --- |
| Name | MonitoringSite |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.WaterQuality.Sites.jstruct/schemas/USGS.WaterQuality.Sites.MonitoringSite`](#schema-usgswaterqualitysitesmonitoringsite) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.WaterQuality.Sites.MonitoringSite` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{site_number}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.WaterQuality.Sites.Kafka` | `KAFKA` | topic `usgs-nwis-wq`; key `{site_number}` |

### Messagegroup `USGS.WaterQuality.Readings`
<a id="messagegroup-usgswaterqualityreadings"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `USGS.WaterQuality.Readings.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `USGS.WaterQuality.Readings.WaterQualityReading`
<a id="message-usgswaterqualityreadingswaterqualityreading"></a>

A single water quality observation from a USGS continuous monitoring sensor, including dissolved oxygen, pH, water temperature, specific conductance, turbidity, and nitrate readings.

| Field | Value |
| --- | --- |
| Name | WaterQualityReading |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/USGS.WaterQuality.Readings.jstruct/schemas/USGS.WaterQuality.Readings.WaterQualityReading`](#schema-usgswaterqualityreadingswaterqualityreading) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `USGS.WaterQuality.Readings.WaterQualityReading` |
| `source` |  | `uritemplate` | `False` | `{source_uri}` |
| `subject` |  | `uritemplate` | `False` | `{site_number}/{parameter_code}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `USGS.WaterQuality.Readings.Kafka` | `KAFKA` | topic `usgs-nwis-wq`; key `{site_number}/{parameter_code}` |

## Schemagroups

### Schemagroup `USGS.WaterQuality.Sites.jstruct`
<a id="schemagroup-usgswaterqualitysitesjstruct"></a>

#### Schema `USGS.WaterQuality.Sites.MonitoringSite`
<a id="schema-usgswaterqualitysitesmonitoringsite"></a>

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |
| Default version | 1.0 |

##### Version `1.0`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### Avro

| Field | Value |
| --- | --- |
| Name | MonitoringSite |
| Namespace | - |
| Type | `record` |
| Doc |  |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `site_number` | `string` |  | `-` |
| `site_name` | `string` |  | `-` |
| `agency_code` | `string` |  | `-` |
| `latitude` | `double` \| `null` |  | `-` |
| `longitude` | `double` \| `null` |  | `-` |
| `site_type` | `string` \| `null` |  | `-` |
| `state_code` | `string` \| `null` |  | `-` |
| `county_code` | `string` \| `null` |  | `-` |
| `huc_code` | `string` \| `null` |  | `-` |

### Schemagroup `USGS.WaterQuality.Readings.jstruct`
<a id="schemagroup-usgswaterqualityreadingsjstruct"></a>

#### Schema `USGS.WaterQuality.Readings.WaterQualityReading`
<a id="schema-usgswaterqualityreadingswaterqualityreading"></a>

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |
| Default version | 1.0 |

##### Version `1.0`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### Avro

| Field | Value |
| --- | --- |
| Name | WaterQualityReading |
| Namespace | - |
| Type | `record` |
| Doc |  |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `site_number` | `string` |  | `-` |
| `site_name` | `string` |  | `-` |
| `parameter_code` | `string` |  | `-` |
| `parameter_name` | `string` |  | `-` |
| `value` | `double` \| `null` |  | `-` |
| `unit` | `string` |  | `-` |
| `qualifier` | `string` \| `null` |  | `-` |
| `date_time` | `string` |  | `-` |
