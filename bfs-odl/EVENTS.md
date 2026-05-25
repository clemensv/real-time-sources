# BfS ODL — Ambient Gamma Dose Rate Monitoring Events

MQTT/5.0 transport variants of the BfS ODL CloudEvents, mapping each message to a retained, QoS-1 Unified Namespace topic under radiation/de/bfs/bfs-odl/{state}/{station_id}/... The {state} placeholder is derived from the station's AGS-based Kennziffer (first two digits map to a German Bundesland) and normalized to lowercase kebab-case before publishing.

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

### Endpoint `de.bfs.odl.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`de.bfs.odl`](#messagegroup-debfsodl) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `bfs-odl` |
| Kafka key | `{station_id}` |
| Deployed | False |

### Endpoint `de.bfs.odl.Mqtt`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `MQTT/5.0` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"mode": "binary"}` |
| Messagegroups | [`de.bfs.odl.mqtt`](#messagegroup-debfsodlmqtt) |

#### Transport options

| Option | Value |
| --- | --- |
| Deployed | False |
| Broker endpoints | `[{"uri": "mqtt://localhost:1883"}]` |

## Messagegroups

### Messagegroup `de.bfs.odl.mqtt`
<a id="messagegroup-debfsodlmqtt"></a>

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 transport variants of the BfS ODL CloudEvents, mapping each message to a retained, QoS-1 Unified Namespace topic under radiation/de/bfs/bfs-odl/{state}/{station_id}/... The {state} placeholder is derived from the station's AGS-based Kennziffer (first two digits map to a German Bundesland) and normalized to lowercase kebab-case before publishing. |
| Transport bindings | `de.bfs.odl.Mqtt` (MQTT/5.0) |
| Messages | 2 |

#### Message `de.bfs.odl.mqtt.Station`
<a id="message-debfsodlmqttstation"></a>

Metadata for an ODL (Ortsdosisleistung) measuring station in the BfS gamma dose rate monitoring network. The BfS operates approximately 1,700 stationary probes across Germany that continuously measure ambient gamma dose rate. Station metadata includes the geographic position, elevation above sea level, postal code, and operational status of each probe.

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/de.bfs.odl.jstruct/schemas/de.bfs.odl.Station`](#schema-debfsodlstation) |
| Base message chain | `/messagegroups/de.bfs.odl/messages/de.bfs.odl.Station` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `de.bfs.odl.Station` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `de.bfs.odl.Mqtt` | `MQTT/5.0` | topic `radiation/de/bfs/bfs-odl/{state}/{station_id}/info` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `radiation/de/bfs/bfs-odl/{state}/{station_id}/info` |
| QoS | 1 |
| Retain | True |

#### Message `de.bfs.odl.mqtt.DoseRateMeasurement`
<a id="message-debfsodlmqttdoseratemeasurement"></a>

A one-hour averaged ambient gamma dose rate measurement from the BfS ODL monitoring network. Each measurement reports the gross gamma dose rate in microsieverts per hour (µSv/h), optionally split into cosmic and terrestrial components. The cosmic component originates from secondary cosmic radiation and depends primarily on altitude; the terrestrial component originates from naturally occurring radionuclides in the ground and varies with local geology.

| Field | Value |
| --- | --- |
| Name | DoseRateMeasurement |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/de.bfs.odl.jstruct/schemas/de.bfs.odl.DoseRateMeasurement`](#schema-debfsodldoseratemeasurement) |
| Base message chain | `/messagegroups/de.bfs.odl/messages/de.bfs.odl.DoseRateMeasurement` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `de.bfs.odl.DoseRateMeasurement` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `de.bfs.odl.Mqtt` | `MQTT/5.0` | topic `radiation/de/bfs/bfs-odl/{state}/{station_id}/dose-rate` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `radiation/de/bfs/bfs-odl/{state}/{station_id}/dose-rate` |
| QoS | 1 |
| Retain | True |

### Messagegroup `de.bfs.odl`
<a id="messagegroup-debfsodl"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `de.bfs.odl.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `de.bfs.odl.Station`
<a id="message-debfsodlstation"></a>

Metadata for an ODL (Ortsdosisleistung) measuring station in the BfS gamma dose rate monitoring network. The BfS operates approximately 1,700 stationary probes across Germany that continuously measure ambient gamma dose rate. Station metadata includes the geographic position, elevation above sea level, postal code, and operational status of each probe.

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/de.bfs.odl.jstruct/schemas/de.bfs.odl.Station`](#schema-debfsodlstation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `de.bfs.odl.Station` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `de.bfs.odl.Kafka` | `KAFKA` | topic `bfs-odl`; key `{station_id}` |

#### Message `de.bfs.odl.DoseRateMeasurement`
<a id="message-debfsodldoseratemeasurement"></a>

A one-hour averaged ambient gamma dose rate measurement from the BfS ODL monitoring network. Each measurement reports the gross gamma dose rate in microsieverts per hour (µSv/h), optionally split into cosmic and terrestrial components. The cosmic component originates from secondary cosmic radiation and depends primarily on altitude; the terrestrial component originates from naturally occurring radionuclides in the ground and varies with local geology.

| Field | Value |
| --- | --- |
| Name | DoseRateMeasurement |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/de.bfs.odl.jstruct/schemas/de.bfs.odl.DoseRateMeasurement`](#schema-debfsodldoseratemeasurement) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `de.bfs.odl.DoseRateMeasurement` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `de.bfs.odl.Kafka` | `KAFKA` | topic `bfs-odl`; key `{station_id}` |

## Schemagroups

### Schemagroup `de.bfs.odl.jstruct`
<a id="schemagroup-debfsodljstruct"></a>

#### Schema `de.bfs.odl.Station`
<a id="schema-debfsodlstation"></a>

| Field | Value |
| --- | --- |
| Name | Station |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://real-time-sources.2030.io/schemas/de/bfs/odl/Station` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/de/bfs/odl/Station` |
| Type | `object` |

###### Object `Station`
<a id="schema-node-station"></a>

Metadata for a BfS ODL gamma dose rate monitoring station. Each station is a stationary probe in the IMIS (Integrated Measuring and Information System) network operated by the German Federal Office for Radiation Protection (Bundesamt für Strahlenschutz). Stations continuously measure ambient gamma dose rate and report hourly averaged values.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | Nine-digit station identifier (Kennziffer) assigned by BfS in the IMIS network. Composed of the official municipality key (AGS) prefix and a station sequence number. Example: '033510091'. This is the stable key used for timeseries retrieval. | altnames=`{"json": "kenn", "lang:de": "Kennziffer"}` | - | - |
| `state` | `string` | `True` | German federal state (Bundesland) derived from the first two digits of the station Kennziffer (AGS prefix). Normalized to lowercase kebab-case for use as the {state} segment in the MQTT/UNS topic. Example: 'niedersachsen', 'bayern', 'nordrhein-westfalen'. | - | - | - |
| `station_code` | `string` | `True` | Short alphanumeric station code assigned by BfS, consisting of a 'DEZ' prefix followed by a four-digit number. Example: 'DEZ0305'. Used in the BfS web interface and download area. | altnames=`{"json": "id", "lang:de": "Stationscode"}` | - | - |
| `name` | `string` | `True` | Human-readable name of the station location, typically a German municipality or locality name. Example: 'Flensburg'. | - | - | - |
| `postal_code` | `string` | `True` | German postal code (Postleitzahl / PLZ) of the station location. Five digits as a string. | altnames=`{"json": "plz", "lang:de": "Postleitzahl"}` | - | - |
| `site_status` | `int32` | `True` | Numeric operational status code. 1 = in operation (in Betrieb), 0 or other values indicate the station is decommissioned or under maintenance. | altnames=`{"json": "site_status"}` | - | - |
| `site_status_text` | `string` | `True` | Human-readable German text describing the operational status. Example: 'in Betrieb' (in operation). | - | - | - |
| `kid` | `int32` | `True` | Numeric region identifier (Kreis-ID) used internally by BfS to group stations into geographic regions. | - | - | - |
| `height_above_sea` | `union` | `True` | Elevation of the station above mean sea level in meters (Normalhöhennull / NHN). Determines the cosmic radiation component. Null if unknown. | unit=`m` symbol=`m` | - | - |
| `longitude` | `double` | `True` | Longitude of the station in WGS84 decimal degrees. Extracted from the GeoJSON geometry coordinates. | unit=`deg` symbol=`°` | - | - |
| `latitude` | `double` | `True` | Latitude of the station in WGS84 decimal degrees. Extracted from the GeoJSON geometry coordinates. | unit=`deg` symbol=`°` | - | - |

#### Schema `de.bfs.odl.DoseRateMeasurement`
<a id="schema-debfsodldoseratemeasurement"></a>

| Field | Value |
| --- | --- |
| Name | DoseRateMeasurement |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://real-time-sources.2030.io/schemas/de/bfs/odl/DoseRateMeasurement` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/de/bfs/odl/DoseRateMeasurement` |
| Type | `object` |

###### Object `DoseRateMeasurement`
<a id="schema-node-doseratemeasurement"></a>

A one-hour averaged ambient gamma dose rate measurement from a BfS ODL station. The gross dose rate value is the total ambient dose equivalent rate H*(10) at 1 meter above ground, expressed in microsieverts per hour (µSv/h). It may be decomposed into a cosmic component (secondary cosmic radiation, altitude-dependent) and a terrestrial component (naturally occurring radionuclides in soil, geology-dependent). Normal background levels in Germany range from approximately 0.05 to 0.18 µSv/h depending on local geology and altitude.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | Nine-digit station identifier (Kennziffer) of the measuring probe. Matches the station_id in the Station schema. | altnames=`{"json": "kenn", "lang:de": "Kennziffer"}` | - | - |
| `state` | `string` | `True` | German federal state (Bundesland) derived from the station Kennziffer. Propagated from station catalog so subscribers can route by state without a catalog join. Used as the {state} segment of the MQTT/UNS topic. | - | - | - |
| `start_measure` | `string` | `True` | Start of the one-hour measurement period in ISO 8601 UTC format. Example: '2026-04-07T12:00:00Z'. | - | - | - |
| `end_measure` | `string` | `True` | End of the one-hour measurement period in ISO 8601 UTC format. Example: '2026-04-07T13:00:00Z'. | - | - | - |
| `value` | `union` | `True` | Gross ambient gamma dose rate averaged over the measurement period in microsieverts per hour (µSv/h). This is the total dose rate including both cosmic and terrestrial components. Null if the station did not report a valid measurement for this interval. | unit=`uSv/h` symbol=`µSv/h` | - | - |
| `value_cosmic` | `union` | `True` | Cosmic radiation component of the ambient gamma dose rate in microsieverts per hour (µSv/h). Estimated from the station's altitude using a standard model. Null when the BfS system has not yet computed the decomposition for this measurement. | unit=`uSv/h` symbol=`µSv/h` | - | - |
| `value_terrestrial` | `union` | `True` | Terrestrial radiation component of the ambient gamma dose rate in microsieverts per hour (µSv/h). Computed as gross value minus cosmic component. Varies with local geology (granite, basalt, sediment). Null when the cosmic component is not available. | unit=`uSv/h` symbol=`µSv/h` | - | - |
| `validated` | `int32` | `True` | Data validation flag. 1 = the measurement has been validated by BfS quality control. 0 = the measurement is preliminary or unvalidated. | - | - | - |
| `nuclide` | `string` | `True` | Nuclide identifier describing the type of radiation measured. For standard ODL probes this is always 'Gamma-ODL-Brutto' (gross gamma ambient dose rate). | - | - | - |

### Schemagroup `de.bfs.odl.avro`
<a id="schemagroup-debfsodlavro"></a>

#### Schema `de.bfs.odl.Station`
<a id="schema-debfsodlstation"></a>

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | Station |
| Namespace | de.bfs.odl |
| Type | `record` |
| Doc | Metadata for a BfS ODL gamma dose rate monitoring station in the IMIS network. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` | Nine-digit station identifier (Kennziffer) assigned by BfS. | `-` |
| `state` | `string` | German federal state (Bundesland) derived from AGS prefix of Kennziffer. | `-` |
| `station_code` | `string` | Short alphanumeric station code (DEZ prefix + four digits). | `-` |
| `name` | `string` | Human-readable station location name. | `-` |
| `postal_code` | `string` | German postal code (PLZ) of the station location. | `-` |
| `site_status` | `int` | Numeric operational status code. 1 = in operation. | `-` |
| `site_status_text` | `string` | Human-readable German operational status text. | `-` |
| `kid` | `int` | Numeric region identifier (Kreis-ID). | `-` |
| `height_above_sea` | `null` \| `double` | Elevation above sea level in meters. Null if unknown. | `-` |
| `longitude` | `double` | Longitude in WGS84 decimal degrees. | `-` |
| `latitude` | `double` | Latitude in WGS84 decimal degrees. | `-` |

#### Schema `de.bfs.odl.DoseRateMeasurement`
<a id="schema-debfsodldoseratemeasurement"></a>

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | DoseRateMeasurement |
| Namespace | de.bfs.odl |
| Type | `record` |
| Doc | A one-hour averaged ambient gamma dose rate measurement from a BfS ODL station. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` | Nine-digit station identifier (Kennziffer) of the measuring probe. | `-` |
| `state` | `string` | German federal state (Bundesland) derived from station Kennziffer AGS prefix. | `-` |
| `start_measure` | `string` | Start of the measurement period in ISO 8601 UTC. | `-` |
| `end_measure` | `string` | End of the measurement period in ISO 8601 UTC. | `-` |
| `value` | `null` \| `double` | Gross ambient gamma dose rate in µSv/h. Null if not reported. | `-` |
| `value_cosmic` | `null` \| `double` | Cosmic radiation component in µSv/h. Null when not computed. | `-` |
| `value_terrestrial` | `null` \| `double` | Terrestrial radiation component in µSv/h. Null when not computed. | `-` |
| `validated` | `int` | Data validation flag. 1 = validated, 0 = preliminary. | `-` |
| `nuclide` | `string` | Nuclide identifier, typically 'Gamma-ODL-Brutto'. | `-` |
