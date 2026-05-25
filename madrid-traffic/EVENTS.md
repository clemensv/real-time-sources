# Madrid Real-Time Traffic (Informo) Events

This bridge polls the Madrid Informo traffic sensor API and sends traffic data to Apache Kafka as CloudEvents.

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
| Messagegroups | 1 |
| Schemagroups | 1 |

## Endpoints

### Endpoint `es.madrid.informo.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`es.madrid.informo`](#messagegroup-esmadridinformo) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `madrid-traffic` |
| Kafka key | `{sensor_id}` |
| Deployed | False |

## Messagegroups

### Messagegroup `es.madrid.informo`
<a id="messagegroup-esmadridinformo"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `es.madrid.informo.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `es.madrid.informo.MeasurementPoint`
<a id="message-esmadridinformomeasurementpoint"></a>

| Field | Value |
| --- | --- |
| Name | MeasurementPoint |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/es.madrid.informo.jstruct/schemas/es.madrid.informo.MeasurementPoint`](#schema-esmadridinformomeasurementpoint) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `es.madrid.informo.MeasurementPoint` |
| `source` |  | `string` | `False` | `https://informo.madrid.es/informo/tmadrid/pm.xml` |
| `subject` |  | `uritemplate` | `False` | `{sensor_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `es.madrid.informo.Kafka` | `KAFKA` | topic `madrid-traffic`; key `{sensor_id}` |

#### Message `es.madrid.informo.TrafficReading`
<a id="message-esmadridinformotrafficreading"></a>

| Field | Value |
| --- | --- |
| Name | TrafficReading |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/es.madrid.informo.jstruct/schemas/es.madrid.informo.TrafficReading`](#schema-esmadridinformotrafficreading) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `es.madrid.informo.TrafficReading` |
| `source` |  | `string` | `False` | `https://informo.madrid.es/informo/tmadrid/pm.xml` |
| `subject` |  | `uritemplate` | `False` | `{sensor_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `es.madrid.informo.Kafka` | `KAFKA` | topic `madrid-traffic`; key `{sensor_id}` |

## Schemagroups

### Schemagroup `es.madrid.informo.jstruct`
<a id="schemagroup-esmadridinformojstruct"></a>

#### Schema `es.madrid.informo.MeasurementPoint`
<a id="schema-esmadridinformomeasurementpoint"></a>

| Field | Value |
| --- | --- |
| Name | MeasurementPoint |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://informo.madrid.es/schemas/es/madrid/informo/MeasurementPoint` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `MeasurementPoint`
<a id="schema-node-measurementpoint"></a>

Reference data for a traffic measurement point (sensor) in Madrid's Informo road traffic monitoring system. Each measurement point is installed on a specific road segment and reports traffic intensity, occupancy, and service level readings. This data is relatively static and describes the sensor installation, not the real-time traffic conditions.

| Field | Value |
| --- | --- |
| $id | `https://informo.madrid.es/schemas/es/madrid/informo/MeasurementPoint` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `sensor_id` | `string` | `True` | Unique sensor identifier from the Madrid Informo system. Corresponds to the 'idelem' field in the upstream XML. Numeric code assigned by the Madrid traffic management center to each measurement point. | altnames=`{"lang:es": "idelem"}` | - | - |
| `description` | `string` | `True` | Human-readable description of the road segment where this sensor is installed. Typically includes the street name, direction, and bounding cross-streets. Corresponds to 'descripcion' in the upstream XML. Text is in Spanish. | altnames=`{"lang:es": "descripcion"}` | - | - |
| `element_type` | `union` | `False` | Classification of the measurement point within Madrid's traffic network. Derived from the 'accesoAsociado' field prefix in the upstream XML. Common values include 'URB' for urban streets and 'M30' for the M-30 ring motorway. | altnames=`{"lang:es": "tipo_elem"}` | - | - |
| `subarea` | `union` | `False` | Traffic management zone code for this sensor. Corresponds to 'subarea' in the upstream XML. Used by Madrid's traffic management center for geographic grouping of sensors. | - | - | - |
| `longitude` | `union` | `False` | Longitude of the sensor in decimal degrees (WGS84, EPSG:4326). Converted from the UTM easting in 'st_x' in the upstream XML, which uses European comma decimal separators. | unit=`deg` symbol=`°` | - | - |
| `latitude` | `union` | `False` | Latitude of the sensor in decimal degrees (WGS84, EPSG:4326). Converted from the UTM northing in 'st_y' in the upstream XML, which uses European comma decimal separators. | unit=`deg` symbol=`°` | - | - |
| `saturation_intensity` | `union` | `False` | Maximum traffic intensity that the road segment can handle, expressed in vehicles per hour. Corresponds to 'intensidadSat' in the upstream XML. Used as the denominator for computing load and saturation ratios. | unit=`1/h` symbol=`veh/h`<br>altnames=`{"lang:es": "intensidadSat"}` | - | - |

#### Schema `es.madrid.informo.TrafficReading`
<a id="schema-esmadridinformotrafficreading"></a>

| Field | Value |
| --- | --- |
| Name | TrafficReading |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://informo.madrid.es/schemas/es/madrid/informo/TrafficReading` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `TrafficReading`
<a id="schema-node-trafficreading"></a>

Real-time traffic reading from a measurement point in Madrid's Informo road traffic monitoring system. Updated approximately every 5 minutes. Each reading provides the current traffic intensity, road occupancy, load, and service level for a specific sensor on Madrid's road network, including the M-30 ring motorway and urban streets.

| Field | Value |
| --- | --- |
| $id | `https://informo.madrid.es/schemas/es/madrid/informo/TrafficReading` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `sensor_id` | `string` | `True` | Unique sensor identifier from the Madrid Informo system. Corresponds to 'idelem' in the upstream XML. Used as the key for correlating readings with measurement point reference data. | altnames=`{"lang:es": "idelem"}` | - | - |
| `intensity` | `union` | `False` | Current traffic intensity measured by the sensor, expressed in vehicles per hour. Corresponds to 'intensidad' in the upstream XML. A value of 0 may indicate no traffic or a sensor in standby mode. | unit=`1/h` symbol=`veh/h`<br>altnames=`{"lang:es": "intensidad"}` | - | - |
| `occupancy` | `union` | `False` | Percentage of time the sensor detects a vehicle presence. Corresponds to 'ocupacion' in the upstream XML. Range is 0 to 100. | unit=`%` symbol=`%`<br>altnames=`{"lang:es": "ocupacion"}` | - | - |
| `load` | `union` | `False` | Load percentage representing the ratio of current intensity to saturation intensity. Corresponds to 'carga' in the upstream XML. Range is typically 0 to 100. | unit=`%` symbol=`%`<br>altnames=`{"lang:es": "carga"}` | - | - |
| `service_level` | `union` | `False` | Traffic service level reported by the sensor. Corresponds to 'nivelServicio' in the upstream XML. Values: 0 = fluid/free flow, 1 = moderate/dense, 2 = congested, 3 = severely congested. | altnames=`{"lang:es": "nivelServicio"}` | - | - |
| `error_flag` | `union` | `False` | Error status flag for this reading. Corresponds to 'error' in the upstream XML. 'N' indicates a normal reading, 'S' or 'Y' indicates the sensor is reporting an error and the data may be unreliable. | - | - | - |
| `timestamp` | `datetime` | `True` | Timestamp of the traffic reading in UTC. Since the upstream XML does not include per-sensor timestamps, this is derived from the poll time rounded to the nearest 5-minute interval, reflecting the upstream update cadence. | - | - | - |
