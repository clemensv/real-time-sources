# Sensor.Community Events

Sensor.Community, formerly Luftdaten.info, is a large citizen-science sensor network that publishes near-real-time environmental measurements from thousands of community-operated stations. This source polls the public Airrohr API and republishes selected sensor metadata and readings as CloudEvents into Kafka.

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
| Schemagroups | 2 |

## Endpoints

### Endpoint `io.sensor.community.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`io.sensor.community`](#messagegroup-iosensorcommunity) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `sensor-community` |
| Kafka key | `{sensor_id}` |
| Deployed | False |

## Messagegroups

### Messagegroup `io.sensor.community`
<a id="messagegroup-iosensorcommunity"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `io.sensor.community.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `io.sensor.community.SensorInfo`
<a id="message-iosensorcommunitysensorinfo"></a>

Reference data for a Sensor.Community sensor node including its hardware type and last known location metadata.

| Field | Value |
| --- | --- |
| Name | SensorInfo |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/io.sensor.community.jstruct/schemas/io.sensor.community.SensorInfo`](#schema-iosensorcommunitysensorinfo) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `io.sensor.community.SensorInfo` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{sensor_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `io.sensor.community.Kafka` | `KAFKA` | topic `sensor-community`; key `{sensor_id}` |

#### Message `io.sensor.community.SensorReading`
<a id="message-iosensorcommunitysensorreading"></a>

Latest Sensor.Community telemetry reading for one sensor at a specific timestamp, normalized across particulate, climate, pressure, and noise measurements.

| Field | Value |
| --- | --- |
| Name | SensorReading |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/io.sensor.community.jstruct/schemas/io.sensor.community.SensorReading`](#schema-iosensorcommunitysensorreading) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `io.sensor.community.SensorReading` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{sensor_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `io.sensor.community.Kafka` | `KAFKA` | topic `sensor-community`; key `{sensor_id}` |

## Schemagroups

### Schemagroup `io.sensor.community.jstruct`
<a id="schemagroup-iosensorcommunityjstruct"></a>

#### Schema `io.sensor.community.SensorInfo`
<a id="schema-iosensorcommunitysensorinfo"></a>

| Field | Value |
| --- | --- |
| Name | SensorInfo |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://github.com/clemensv/real-time-sources/schemas/io/sensor/community/SensorInfo` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/io/sensor/community/SensorInfo` |
| Type | `object` |

###### Object `SensorInfo`
<a id="schema-node-sensorinfo"></a>

Schema for Sensor.Community sensor reference data, capturing the stable sensor identifier, hardware type, and latest known location metadata published in the Airrohr API payload.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `sensor_id` | `integer` | `True` | Stable integer identifier of the Sensor.Community sensor device. This value is used as the CloudEvents subject and Kafka key. | - | - | - |
| `sensor_type_id` | `integer` | `True` | Numeric upstream identifier for the sensor hardware type, such as the Sensor.Community type id for SDS011 or BME280. | - | - | - |
| `sensor_type_name` | `string` | `True` | Upstream sensor hardware type name published under sensor.sensor_type.name, for example SDS011, SPS30, BME280, or DHT22. | - | - | - |
| `sensor_type_manufacturer` | `string` | `True` | Manufacturer name published by Sensor.Community for the sensor hardware type, taken from sensor.sensor_type.manufacturer. | - | - | - |
| `pin` | `string` | `True` | Sensor pin designation reported by the upstream payload under sensor.pin. | - | - | - |
| `location_id` | `integer` | `True` | Stable integer identifier of the Sensor.Community location object associated with the reading. | - | - | - |
| `latitude` | `double` | `True` | Latitude of the sensor location in WGS84 decimal degrees. | - | - | - |
| `longitude` | `double` | `True` | Longitude of the sensor location in WGS84 decimal degrees. | - | - | - |
| `altitude` | `union` | `True` | Altitude of the sensor location in meters above sea level when supplied by the upstream payload. | unit=`m` | - | - |
| `country` | `string` | `True` | ISO 3166-1 alpha-2 country code published in the Sensor.Community location record. | - | maxLength=`2`<br>minLength=`2` | - |
| `indoor` | `boolean` | `True` | True when the upstream location.indoor flag marks the sensor as indoor; false when the sensor is marked as outdoor. | - | - | - |

#### Schema `io.sensor.community.SensorReading`
<a id="schema-iosensorcommunitysensorreading"></a>

| Field | Value |
| --- | --- |
| Name | SensorReading |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://github.com/clemensv/real-time-sources/schemas/io/sensor/community/SensorReading` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/io/sensor/community/SensorReading` |
| Type | `object` |

###### Object `SensorReading`
<a id="schema-node-sensorreading"></a>

Schema for the latest normalized Sensor.Community telemetry reading for a single sensor and timestamp, covering particulate matter, temperature, humidity, pressure, and supported noise measurements.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `sensor_id` | `integer` | `True` | Stable integer identifier of the Sensor.Community sensor device. This value is used as the CloudEvents subject and Kafka key. | - | - | - |
| `timestamp` | `string` | `True` | UTC timestamp published by Sensor.Community for the reading in the format YYYY-MM-DD HH:mm:ss. | - | - | - |
| `sensor_type_name` | `string` | `True` | Upstream sensor hardware type name published under sensor.sensor_type.name for the device that emitted the reading. | - | - | - |
| `pm10_ug_m3` | `union` | `True` | Particulate matter mass concentration for PM10 in micrograms per cubic meter when the upstream feed publishes value type P1. | unit=`µg/m³`<br>altnames=`["P1"]` | - | - |
| `pm2_5_ug_m3` | `union` | `True` | Particulate matter mass concentration for PM2.5 in micrograms per cubic meter when the upstream feed publishes value type P2. | unit=`µg/m³`<br>altnames=`["P2"]` | - | - |
| `pm1_0_ug_m3` | `union` | `True` | Particulate matter mass concentration for PM1.0 in micrograms per cubic meter when the upstream feed publishes value type P0, typically for SPS30-family sensors. | unit=`µg/m³`<br>altnames=`["P0"]` | - | - |
| `pm4_0_ug_m3` | `union` | `True` | Particulate matter mass concentration for PM4.0 in micrograms per cubic meter when the upstream feed publishes value type P4, typically for SPS30-family sensors. | unit=`µg/m³`<br>altnames=`["P4"]` | - | - |
| `temperature_celsius` | `union` | `True` | Ambient temperature measurement in degrees Celsius when the upstream feed publishes value type temperature. | unit=`°C`<br>altnames=`["temperature"]` | - | - |
| `humidity_percent` | `union` | `True` | Relative humidity in percent when the upstream feed publishes value type humidity. | unit=`%`<br>altnames=`["humidity"]` | - | - |
| `pressure_pa` | `union` | `True` | Atmospheric pressure in pascals when the upstream feed publishes value type pressure. | unit=`Pa`<br>altnames=`["pressure"]` | - | - |
| `pressure_sealevel_pa` | `union` | `True` | Atmospheric pressure reduced to sea level in pascals when the upstream feed publishes value type pressure_at_sealevel. | unit=`Pa`<br>altnames=`["pressure_at_sealevel"]` | - | - |
| `noise_laeq_db` | `union` | `True` | Equivalent continuous sound level in A-weighted decibels when the upstream feed publishes value type noise_LAeq. | unit=`dB(A)`<br>altnames=`["noise_LAeq"]` | - | - |
| `noise_la_min_db` | `union` | `True` | Minimum A-weighted sound level in decibels when the upstream feed publishes value type noise_LA_min. | unit=`dB(A)`<br>altnames=`["noise_LA_min"]` | - | - |
| `noise_la_max_db` | `union` | `True` | Maximum A-weighted sound level in decibels when the upstream feed publishes value type noise_LA_max. | unit=`dB(A)`<br>altnames=`["noise_LA_max"]` | - | - |

### Schemagroup `io.sensor.community.avro`
<a id="schemagroup-iosensorcommunityavro"></a>

#### Schema `io.sensor.community.SensorInfo`
<a id="schema-iosensorcommunitysensorinfo"></a>

| Field | Value |
| --- | --- |
| Name | SensorInfo |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | SensorInfo |
| Namespace | io.sensor.community |
| Type | `record` |
| Doc | Reference data for a Sensor.Community sensor node including hardware type and latest known location metadata. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `sensor_id` | `int` | Stable integer identifier of the Sensor.Community sensor device. This value is used as the CloudEvents subject and Kafka key. | `-` |
| `sensor_type_id` | `int` | Numeric upstream identifier for the sensor hardware type, such as the Sensor.Community type id for SDS011 or BME280. | `-` |
| `sensor_type_name` | `string` | Upstream sensor hardware type name published under sensor.sensor_type.name, for example SDS011, SPS30, BME280, or DHT22. | `-` |
| `sensor_type_manufacturer` | `string` | Manufacturer name published by Sensor.Community for the sensor hardware type, taken from sensor.sensor_type.manufacturer. | `-` |
| `pin` | `string` | Sensor pin designation reported by the upstream payload under sensor.pin. | `-` |
| `location_id` | `int` | Stable integer identifier of the Sensor.Community location object associated with the reading. | `-` |
| `latitude` | `double` | Latitude of the sensor location in WGS84 decimal degrees. | `-` |
| `longitude` | `double` | Longitude of the sensor location in WGS84 decimal degrees. | `-` |
| `altitude` | `null` \| `double` | Altitude of the sensor location in meters above sea level when supplied by the upstream payload. | `-` |
| `country` | `string` | ISO 3166-1 alpha-2 country code published in the Sensor.Community location record. | `-` |
| `indoor` | `boolean` | True when the upstream location.indoor flag marks the sensor as indoor; false when the sensor is marked as outdoor. | `-` |

#### Schema `io.sensor.community.SensorReading`
<a id="schema-iosensorcommunitysensorreading"></a>

| Field | Value |
| --- | --- |
| Name | SensorReading |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | SensorReading |
| Namespace | io.sensor.community |
| Type | `record` |
| Doc | Latest Sensor.Community telemetry reading for one sensor at a specific timestamp, normalized across particulate, climate, pressure, and noise measurements. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `sensor_id` | `int` | Stable integer identifier of the Sensor.Community sensor device. This value is used as the CloudEvents subject and Kafka key. | `-` |
| `timestamp` | `string` | UTC timestamp published by Sensor.Community for the reading in the format YYYY-MM-DD HH:mm:ss. | `-` |
| `sensor_type_name` | `string` | Upstream sensor hardware type name published under sensor.sensor_type.name for the device that emitted the reading. | `-` |
| `pm10_ug_m3` | `null` \| `double` | Particulate matter mass concentration for PM10 in micrograms per cubic meter when the upstream feed publishes value type P1. | `-` |
| `pm2_5_ug_m3` | `null` \| `double` | Particulate matter mass concentration for PM2.5 in micrograms per cubic meter when the upstream feed publishes value type P2. | `-` |
| `pm1_0_ug_m3` | `null` \| `double` | Particulate matter mass concentration for PM1.0 in micrograms per cubic meter when the upstream feed publishes value type P0. | `-` |
| `pm4_0_ug_m3` | `null` \| `double` | Particulate matter mass concentration for PM4.0 in micrograms per cubic meter when the upstream feed publishes value type P4. | `-` |
| `temperature_celsius` | `null` \| `double` | Ambient temperature measurement in degrees Celsius when the upstream feed publishes value type temperature. | `-` |
| `humidity_percent` | `null` \| `double` | Relative humidity in percent when the upstream feed publishes value type humidity. | `-` |
| `pressure_pa` | `null` \| `double` | Atmospheric pressure in pascals when the upstream feed publishes value type pressure. | `-` |
| `pressure_sealevel_pa` | `null` \| `double` | Atmospheric pressure reduced to sea level in pascals when the upstream feed publishes value type pressure_at_sealevel. | `-` |
| `noise_laeq_db` | `null` \| `double` | Equivalent continuous sound level in A-weighted decibels when the upstream feed publishes value type noise_LAeq. | `-` |
| `noise_la_min_db` | `null` \| `double` | Minimum A-weighted sound level in decibels when the upstream feed publishes value type noise_LA_min. | `-` |
| `noise_la_max_db` | `null` \| `double` | Maximum A-weighted sound level in decibels when the upstream feed publishes value type noise_LA_max. | `-` |
