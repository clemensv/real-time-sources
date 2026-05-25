# WSDOT Traveler Information Events

This source bridges the Washington State Department of Transportation (WSDOT) Traveler Information API and Washington State Ferries API to Apache Kafka, producing real-time data across eight event families: traffic flow, travel times, mountain pass conditions, road weather, toll rates, commercial vehicle restrictions, US-Canada border crossing wait times, and ferry vessel locations.

## Table of Contents

- [Registry](#registry)
- [Endpoints](#endpoints)
- [Messagegroups](#messagegroups)
- [Schemagroups](#schemagroups)

---

## Registry

| Field | Value |
| --- | --- |
| Endpoints | 8 |
| Messagegroups | 8 |
| Schemagroups | 16 |

## Endpoints

### Endpoint `us.wa.wsdot.traffic.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`us.wa.wsdot.traffic`](#messagegroup-uswawsdottraffic) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `wsdot` |
| Kafka key | `{flow_data_id}` |
| Deployed | False |

### Endpoint `us.wa.wsdot.traveltimes.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`us.wa.wsdot.traveltimes`](#messagegroup-uswawsdottraveltimes) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `wsdot` |
| Kafka key | `{travel_time_id}` |
| Deployed | False |

### Endpoint `us.wa.wsdot.mountainpass.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`us.wa.wsdot.mountainpass`](#messagegroup-uswawsdotmountainpass) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `wsdot` |
| Kafka key | `{mountain_pass_id}` |
| Deployed | False |

### Endpoint `us.wa.wsdot.weather.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`us.wa.wsdot.weather`](#messagegroup-uswawsdotweather) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `wsdot` |
| Kafka key | `{station_id}` |
| Deployed | False |

### Endpoint `us.wa.wsdot.tolls.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`us.wa.wsdot.tolls`](#messagegroup-uswawsdottolls) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `wsdot` |
| Kafka key | `{trip_name}` |
| Deployed | False |

### Endpoint `us.wa.wsdot.cvrestrictions.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`us.wa.wsdot.cvrestrictions`](#messagegroup-uswawsdotcvrestrictions) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `wsdot` |
| Kafka key | `{state_route_id}/{bridge_number}` |
| Deployed | False |

### Endpoint `us.wa.wsdot.border.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`us.wa.wsdot.border`](#messagegroup-uswawsdotborder) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `wsdot` |
| Kafka key | `{crossing_name}` |
| Deployed | False |

### Endpoint `us.wa.wsdot.ferries.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`us.wa.wsdot.ferries`](#messagegroup-uswawsdotferries) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `wsdot` |
| Kafka key | `{vessel_id}` |
| Deployed | False |

## Messagegroups

### Messagegroup `us.wa.wsdot.traffic`
<a id="messagegroup-uswawsdottraffic"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `us.wa.wsdot.traffic.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `us.wa.wsdot.traffic.TrafficFlowStation`
<a id="message-uswawsdottraffictrafficflowstation"></a>

Metadata for a traffic flow sensor station in the Washington State DOT network. WSDOT deploys approximately 1,400 inductive loop sensors embedded in highway pavement across four geographic regions.

| Field | Value |
| --- | --- |
| Name | TrafficFlowStation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/us.wa.wsdot.traffic.jstruct/schemas/us.wa.wsdot.traffic.TrafficFlowStation`](#schema-uswawsdottraffictrafficflowstation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `us.wa.wsdot.traffic.TrafficFlowStation` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{flow_data_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `us.wa.wsdot.traffic.Kafka` | `KAFKA` | topic `wsdot`; key `{flow_data_id}` |

#### Message `us.wa.wsdot.traffic.TrafficFlowReading`
<a id="message-uswawsdottraffictrafficflowreading"></a>

A traffic flow reading from a WSDOT sensor station. Updated approximately every 90 seconds, each reading reports the current Level of Service.

| Field | Value |
| --- | --- |
| Name | TrafficFlowReading |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/us.wa.wsdot.traffic.jstruct/schemas/us.wa.wsdot.traffic.TrafficFlowReading`](#schema-uswawsdottraffictrafficflowreading) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `us.wa.wsdot.traffic.TrafficFlowReading` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{flow_data_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `us.wa.wsdot.traffic.Kafka` | `KAFKA` | topic `wsdot`; key `{flow_data_id}` |

### Messagegroup `us.wa.wsdot.traveltimes`
<a id="messagegroup-uswawsdottraveltimes"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `us.wa.wsdot.traveltimes.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `us.wa.wsdot.traveltimes.TravelTimeRoute`
<a id="message-uswawsdottraveltimestraveltimeroute"></a>

A named travel time route monitored by WSDOT. Each route has fixed start and end points on Washington State highways with historical average and current real-time travel times.

| Field | Value |
| --- | --- |
| Name | TravelTimeRoute |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/us.wa.wsdot.traveltimes.jstruct/schemas/us.wa.wsdot.traveltimes.TravelTimeRoute`](#schema-uswawsdottraveltimestraveltimeroute) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `us.wa.wsdot.traveltimes.TravelTimeRoute` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{travel_time_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `us.wa.wsdot.traveltimes.Kafka` | `KAFKA` | topic `wsdot`; key `{travel_time_id}` |

### Messagegroup `us.wa.wsdot.mountainpass`
<a id="messagegroup-uswawsdotmountainpass"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `us.wa.wsdot.mountainpass.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `us.wa.wsdot.mountainpass.MountainPassCondition`
<a id="message-uswawsdotmountainpassmountainpasscondition"></a>

Current conditions at a Washington State mountain pass including temperature, weather, road conditions, travel advisories, and directional restrictions.

| Field | Value |
| --- | --- |
| Name | MountainPassCondition |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/us.wa.wsdot.mountainpass.jstruct/schemas/us.wa.wsdot.mountainpass.MountainPassCondition`](#schema-uswawsdotmountainpassmountainpasscondition) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `us.wa.wsdot.mountainpass.MountainPassCondition` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{mountain_pass_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `us.wa.wsdot.mountainpass.Kafka` | `KAFKA` | topic `wsdot`; key `{mountain_pass_id}` |

### Messagegroup `us.wa.wsdot.weather`
<a id="messagegroup-uswawsdotweather"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `us.wa.wsdot.weather.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `us.wa.wsdot.weather.WeatherStation`
<a id="message-uswawsdotweatherweatherstation"></a>

Metadata for a WSDOT road weather information system (RWIS) station. WSDOT operates approximately 134 stations across Washington State highways.

| Field | Value |
| --- | --- |
| Name | WeatherStation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/us.wa.wsdot.weather.jstruct/schemas/us.wa.wsdot.weather.WeatherStation`](#schema-uswawsdotweatherweatherstation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `us.wa.wsdot.weather.WeatherStation` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `us.wa.wsdot.weather.Kafka` | `KAFKA` | topic `wsdot`; key `{station_id}` |

#### Message `us.wa.wsdot.weather.WeatherReading`
<a id="message-uswawsdotweatherweatherreading"></a>

A current weather reading from a WSDOT road weather station including temperature, wind, precipitation, pressure, humidity, visibility, and sky coverage.

| Field | Value |
| --- | --- |
| Name | WeatherReading |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/us.wa.wsdot.weather.jstruct/schemas/us.wa.wsdot.weather.WeatherReading`](#schema-uswawsdotweatherweatherreading) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `us.wa.wsdot.weather.WeatherReading` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `us.wa.wsdot.weather.Kafka` | `KAFKA` | topic `wsdot`; key `{station_id}` |

### Messagegroup `us.wa.wsdot.tolls`
<a id="messagegroup-uswawsdottolls"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `us.wa.wsdot.tolls.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `us.wa.wsdot.tolls.TollRate`
<a id="message-uswawsdottollstollrate"></a>

Current toll rate for a WSDOT tolled route segment. WSDOT operates dynamic tolling on SR 99, I-405, and SR 167.

| Field | Value |
| --- | --- |
| Name | TollRate |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/us.wa.wsdot.tolls.jstruct/schemas/us.wa.wsdot.tolls.TollRate`](#schema-uswawsdottollstollrate) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `us.wa.wsdot.tolls.TollRate` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{trip_name}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `us.wa.wsdot.tolls.Kafka` | `KAFKA` | topic `wsdot`; key `{trip_name}` |

### Messagegroup `us.wa.wsdot.cvrestrictions`
<a id="messagegroup-uswawsdotcvrestrictions"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `us.wa.wsdot.cvrestrictions.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `us.wa.wsdot.cvrestrictions.CommercialVehicleRestriction`
<a id="message-uswawsdotcvrestrictionscommercialvehiclerestriction"></a>

A commercial vehicle restriction on a Washington State highway bridge or road segment. Restrictions limit vehicle weight, height, length, or width.

| Field | Value |
| --- | --- |
| Name | CommercialVehicleRestriction |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/us.wa.wsdot.cvrestrictions.jstruct/schemas/us.wa.wsdot.cvrestrictions.CommercialVehicleRestriction`](#schema-uswawsdotcvrestrictionscommercialvehiclerestriction) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `us.wa.wsdot.cvrestrictions.CommercialVehicleRestriction` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{state_route_id}/{bridge_number}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `us.wa.wsdot.cvrestrictions.Kafka` | `KAFKA` | topic `wsdot`; key `{state_route_id}/{bridge_number}` |

### Messagegroup `us.wa.wsdot.border`
<a id="messagegroup-uswawsdotborder"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `us.wa.wsdot.border.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `us.wa.wsdot.border.BorderCrossing`
<a id="message-uswawsdotborderbordercrossing"></a>

Current wait time at a US-Canada border crossing lane in Washington State. Wait times are in minutes, updated approximately every 5 minutes.

| Field | Value |
| --- | --- |
| Name | BorderCrossing |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/us.wa.wsdot.border.jstruct/schemas/us.wa.wsdot.border.BorderCrossing`](#schema-uswawsdotborderbordercrossing) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `us.wa.wsdot.border.BorderCrossing` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{crossing_name}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `us.wa.wsdot.border.Kafka` | `KAFKA` | topic `wsdot`; key `{crossing_name}` |

### Messagegroup `us.wa.wsdot.ferries`
<a id="messagegroup-uswawsdotferries"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `us.wa.wsdot.ferries.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `us.wa.wsdot.ferries.VesselLocation`
<a id="message-uswawsdotferriesvessellocation"></a>

Real-time location and status of a Washington State Ferries vessel. WSF operates approximately 21 vessels across Puget Sound routes.

| Field | Value |
| --- | --- |
| Name | VesselLocation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/us.wa.wsdot.ferries.jstruct/schemas/us.wa.wsdot.ferries.VesselLocation`](#schema-uswawsdotferriesvessellocation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `us.wa.wsdot.ferries.VesselLocation` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{vessel_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `us.wa.wsdot.ferries.Kafka` | `KAFKA` | topic `wsdot`; key `{vessel_id}` |

## Schemagroups

### Schemagroup `us.wa.wsdot.traffic.jstruct`
<a id="schemagroup-uswawsdottrafficjstruct"></a>

#### Schema `us.wa.wsdot.traffic.TrafficFlowStation`
<a id="schema-uswawsdottraffictrafficflowstation"></a>

| Field | Value |
| --- | --- |
| Name | TrafficFlowStation |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://real-time-sources.2030.io/schemas/us/wa/wsdot/traffic/TrafficFlowStation` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/us/wa/wsdot/traffic/TrafficFlowStation` |
| Type | `object` |

###### Object `TrafficFlowStation`
<a id="schema-node-trafficflowstation"></a>

Metadata for a traffic flow sensor station in the WSDOT network. Each sensor is identified by a unique FlowDataID integer.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `flow_data_id` | `string` | `True` | Unique numeric identifier for this traffic flow sensor station, stringified from upstream FlowDataID. | altnames=`{"json": "FlowDataID"}` | - | - |
| `station_name` | `string` | `True` | Descriptive name of the flow sensor station. | altnames=`{"json": "StationName"}` | - | - |
| `region` | enum `['Eastern', 'Northwest', 'Olympic', 'Southwest']` | `True` | WSDOT geographic coverage region. | altnames=`{"json": "Region"}` | - | - |
| `description` | `union` | `True` | Location description. Null if not provided. | altnames=`{"json": "Description"}` | - | - |
| `road_name` | `string` | `True` | Road designation where the sensor is installed. | altnames=`{"json": "RoadName"}` | - | - |
| `direction` | `union` | `True` | Direction of travel monitored. Examples: NB, SB, EB, WB. | altnames=`{"json": "Direction"}` | - | - |
| `milepost` | `union` | `True` | Milepost marker along the roadway. | altnames=`{"json": "MilePost"}` | - | - |
| `latitude` | `double` | `True` | Latitude in WGS84 decimal degrees. | unit=`deg` symbol=`°`<br>altnames=`{"json": "Latitude"}` | - | - |
| `longitude` | `double` | `True` | Longitude in WGS84 decimal degrees. | unit=`deg` symbol=`°`<br>altnames=`{"json": "Longitude"}` | - | - |

#### Schema `us.wa.wsdot.traffic.TrafficFlowReading`
<a id="schema-uswawsdottraffictrafficflowreading"></a>

| Field | Value |
| --- | --- |
| Name | TrafficFlowReading |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://real-time-sources.2030.io/schemas/us/wa/wsdot/traffic/TrafficFlowReading` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/us/wa/wsdot/traffic/TrafficFlowReading` |
| Type | `object` |

###### Object `TrafficFlowReading`
<a id="schema-node-trafficflowreading"></a>

A traffic flow reading from a WSDOT sensor station.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `flow_data_id` | `string` | `True` | Sensor station identifier, stringified from upstream FlowDataID. | altnames=`{"json": "FlowDataID"}` | - | - |
| `station_name` | `string` | `True` | Station name. | altnames=`{"json": "StationName"}` | - | - |
| `region` | enum `['Eastern', 'Northwest', 'Olympic', 'Southwest']` | `True` | WSDOT region. | altnames=`{"json": "Region"}` | - | - |
| `flow_reading` | enum `['Unknown', 'WideOpen', 'Moderate', 'Heavy', 'StopAndGo', 'NoData']` | `True` | Current traffic Level of Service. Converted from upstream FlowReadingValue byte. | altenums=`{"upstream_byte": {"Heavy": "3", "Moderate": "2", "NoData": "5", "StopAndGo": "4", "Unknown": "0", "WideOpen": "1"}}` | - | - |
| `reading_time` | `string` | `True` | ISO 8601 UTC timestamp of the reading. | altnames=`{"json": "Time"}` | - | - |

### Schemagroup `us.wa.wsdot.traveltimes.jstruct`
<a id="schemagroup-uswawsdottraveltimesjstruct"></a>

#### Schema `us.wa.wsdot.traveltimes.TravelTimeRoute`
<a id="schema-uswawsdottraveltimestraveltimeroute"></a>

| Field | Value |
| --- | --- |
| Name | TravelTimeRoute |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://real-time-sources.2030.io/schemas/us/wa/wsdot/traveltimes/TravelTimeRoute` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/us/wa/wsdot/traveltimes/TravelTimeRoute` |
| Type | `object` |

###### Object `TravelTimeRoute`
<a id="schema-node-traveltimeroute"></a>

A named travel time route monitored by WSDOT with historical average and current real-time travel times in minutes.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `travel_time_id` | `string` | `True` | Unique route identifier, stringified from upstream TravelTimeID. | altnames=`{"json": "TravelTimeID"}` | - | - |
| `name` | `string` | `True` | Short route segment name. | altnames=`{"json": "Name"}` | - | - |
| `description` | `string` | `True` | Longer description including lane type. | altnames=`{"json": "Description"}` | - | - |
| `distance` | `double` | `True` | Route distance in miles. | unit=`mi` symbol=`mi`<br>altnames=`{"json": "Distance"}` | - | - |
| `average_time` | `int32` | `True` | Historical average travel time in minutes. | unit=`min` symbol=`min`<br>altnames=`{"json": "AverageTime"}` | - | - |
| `current_time` | `int32` | `True` | Current real-time travel time in minutes. | unit=`min` symbol=`min`<br>altnames=`{"json": "CurrentTime"}` | - | - |
| `time_updated` | `string` | `True` | ISO 8601 UTC timestamp of last update. | altnames=`{"json": "TimeUpdated"}` | - | - |
| `start_description` | `union` | `True` | Start point description. | - | - | - |
| `start_road_name` | `union` | `True` | Road at start point. | - | - | - |
| `start_direction` | `union` | `True` | Direction at start point. | - | - | - |
| `start_milepost` | `union` | `True` | Milepost at start. | - | - | - |
| `start_latitude` | `double` | `True` | Start latitude in WGS84. | unit=`deg` symbol=`°` | - | - |
| `start_longitude` | `double` | `True` | Start longitude in WGS84. | unit=`deg` symbol=`°` | - | - |
| `end_description` | `union` | `True` | End point description. | - | - | - |
| `end_road_name` | `union` | `True` | Road at end point. | - | - | - |
| `end_direction` | `union` | `True` | Direction at end point. | - | - | - |
| `end_milepost` | `union` | `True` | Milepost at end. | - | - | - |
| `end_latitude` | `double` | `True` | End latitude in WGS84. | unit=`deg` symbol=`°` | - | - |
| `end_longitude` | `double` | `True` | End longitude in WGS84. | unit=`deg` symbol=`°` | - | - |

### Schemagroup `us.wa.wsdot.mountainpass.jstruct`
<a id="schemagroup-uswawsdotmountainpassjstruct"></a>

#### Schema `us.wa.wsdot.mountainpass.MountainPassCondition`
<a id="schema-uswawsdotmountainpassmountainpasscondition"></a>

| Field | Value |
| --- | --- |
| Name | MountainPassCondition |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://real-time-sources.2030.io/schemas/us/wa/wsdot/mountainpass/MountainPassCondition` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/us/wa/wsdot/mountainpass/MountainPassCondition` |
| Type | `object` |

###### Object `MountainPassCondition`
<a id="schema-node-mountainpasscondition"></a>

Current conditions at a Washington State mountain pass. WSDOT monitors 16 mountain passes reporting temperature, weather, road conditions, travel advisories, and directional restrictions.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `mountain_pass_id` | `string` | `True` | Unique pass identifier, stringified from upstream MountainPassId. | altnames=`{"json": "MountainPassId"}` | - | - |
| `mountain_pass_name` | `string` | `True` | Pass name with highway designation. | altnames=`{"json": "MountainPassName"}` | - | - |
| `elevation_in_feet` | `int32` | `True` | Summit elevation in feet above sea level. | unit=`ft` symbol=`ft`<br>altnames=`{"json": "ElevationInFeet"}` | - | - |
| `latitude` | `double` | `True` | Latitude in WGS84. | unit=`deg` symbol=`°`<br>altnames=`{"json": "Latitude"}` | - | - |
| `longitude` | `double` | `True` | Longitude in WGS84. | unit=`deg` symbol=`°`<br>altnames=`{"json": "Longitude"}` | - | - |
| `temperature_in_fahrenheit` | `union` | `True` | Temperature at the summit in Fahrenheit. Null if not reporting. | unit=`degF` symbol=`°F`<br>altnames=`{"json": "TemperatureInFahrenheit"}` | - | - |
| `weather_condition` | `string` | `True` | Current weather condition text. Examples: Clear, Rain, Snow, Fog. | altnames=`{"json": "WeatherCondition"}` | - | - |
| `road_condition` | `string` | `True` | Road surface condition text. Examples: Dry, Wet, Compact Snow, Ice. | altnames=`{"json": "RoadCondition"}` | - | - |
| `travel_advisory_active` | `boolean` | `True` | True if a travel advisory is in effect. | altnames=`{"json": "TravelAdvisoryActive"}` | - | - |
| `restriction_one_direction` | `union` | `True` | Direction for first restriction. | - | - | - |
| `restriction_one_text` | `union` | `True` | First restriction text. | - | - | - |
| `restriction_two_direction` | `union` | `True` | Direction for second restriction. | - | - | - |
| `restriction_two_text` | `union` | `True` | Second restriction text. | - | - | - |
| `date_updated` | `string` | `True` | ISO 8601 UTC timestamp of last update. | altnames=`{"json": "DateUpdated"}` | - | - |

### Schemagroup `us.wa.wsdot.weather.jstruct`
<a id="schemagroup-uswawsdotweatherjstruct"></a>

#### Schema `us.wa.wsdot.weather.WeatherStation`
<a id="schema-uswawsdotweatherweatherstation"></a>

| Field | Value |
| --- | --- |
| Name | WeatherStation |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://real-time-sources.2030.io/schemas/us/wa/wsdot/weather/WeatherStation` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/us/wa/wsdot/weather/WeatherStation` |
| Type | `object` |

###### Object `WeatherStation`
<a id="schema-node-weatherstation"></a>

Metadata for a WSDOT RWIS station.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | Station identifier from upstream StationCode. | altnames=`{"json": "StationCode"}` | - | - |
| `station_name` | `string` | `True` | Station name with highway and milepost. | altnames=`{"json": "StationName"}` | - | - |
| `latitude` | `double` | `True` | Latitude in WGS84. | unit=`deg` symbol=`°`<br>altnames=`{"json": "Latitude"}` | - | - |
| `longitude` | `double` | `True` | Longitude in WGS84. | unit=`deg` symbol=`°`<br>altnames=`{"json": "Longitude"}` | - | - |

#### Schema `us.wa.wsdot.weather.WeatherReading`
<a id="schema-uswawsdotweatherweatherreading"></a>

| Field | Value |
| --- | --- |
| Name | WeatherReading |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://real-time-sources.2030.io/schemas/us/wa/wsdot/weather/WeatherReading` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/us/wa/wsdot/weather/WeatherReading` |
| Type | `object` |

###### Object `WeatherReading`
<a id="schema-node-weatherreading"></a>

A current weather reading from a WSDOT RWIS station.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | Station identifier from upstream StationID. | altnames=`{"json": "StationID"}` | - | - |
| `station_name` | `string` | `True` | Station name. | altnames=`{"json": "StationName"}` | - | - |
| `reading_time` | `string` | `True` | ISO 8601 UTC timestamp. | altnames=`{"json": "ReadingTime"}` | - | - |
| `temperature_in_fahrenheit` | `union` | `True` | Air temperature in Fahrenheit. | unit=`degF` symbol=`°F`<br>altnames=`{"json": "TemperatureInFahrenheit"}` | - | - |
| `precipitation_in_inches` | `union` | `True` | Precipitation in inches. | unit=`in` symbol=`in`<br>altnames=`{"json": "PrecipitationInInches"}` | - | - |
| `wind_speed_in_mph` | `union` | `True` | Wind speed in mph. | unit=`mi/h` symbol=`mph`<br>altnames=`{"json": "WindSpeedInMPH"}` | - | - |
| `wind_gust_speed_in_mph` | `union` | `True` | Wind gust speed in mph. | unit=`mi/h` symbol=`mph`<br>altnames=`{"json": "WindGustSpeedInMPH"}` | - | - |
| `wind_direction` | `union` | `True` | Wind direction in degrees from true north. | unit=`deg` symbol=`°`<br>altnames=`{"json": "WindDirection"}` | - | - |
| `wind_direction_cardinal` | `union` | `True` | Wind direction as cardinal abbreviation. | altnames=`{"json": "WindDirectionCardinal"}` | - | - |
| `barometric_pressure` | `union` | `True` | Barometric pressure in hPa. | unit=`hPa` symbol=`hPa`<br>altnames=`{"json": "BarometricPressure"}` | - | - |
| `relative_humidity` | `union` | `True` | Relative humidity percentage. | unit=`%` symbol=`%`<br>altnames=`{"json": "RelativeHumidity"}` | - | - |
| `visibility` | `union` | `True` | Visibility distance. | altnames=`{"json": "Visibility"}` | - | - |
| `sky_coverage` | `union` | `True` | Sky coverage description. | altnames=`{"json": "SkyCoverage"}` | - | - |
| `latitude` | `double` | `True` | Latitude in WGS84. | unit=`deg` symbol=`°`<br>altnames=`{"json": "Latitude"}` | - | - |
| `longitude` | `double` | `True` | Longitude in WGS84. | unit=`deg` symbol=`°`<br>altnames=`{"json": "Longitude"}` | - | - |

### Schemagroup `us.wa.wsdot.tolls.jstruct`
<a id="schemagroup-uswawsdottollsjstruct"></a>

#### Schema `us.wa.wsdot.tolls.TollRate`
<a id="schema-uswawsdottollstollrate"></a>

| Field | Value |
| --- | --- |
| Name | TollRate |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://real-time-sources.2030.io/schemas/us/wa/wsdot/tolls/TollRate` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/us/wa/wsdot/tolls/TollRate` |
| Type | `object` |

###### Object `TollRate`
<a id="schema-node-tollrate"></a>

Current toll rate for a WSDOT tolled route segment with dynamic pricing.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `trip_name` | `string` | `True` | Tolled route segment identifier. | altnames=`{"json": "TripName"}` | - | - |
| `state_route` | `string` | `True` | State route number. | altnames=`{"json": "StateRoute"}` | - | - |
| `travel_direction` | `string` | `True` | Travel direction: N, S, E, W. | altnames=`{"json": "TravelDirection"}` | - | - |
| `current_toll` | `int32` | `True` | Current toll in cents. | altnames=`{"json": "CurrentToll"}` | - | - |
| `current_message` | `union` | `True` | Optional status message. | altnames=`{"json": "CurrentMessage"}` | - | - |
| `time_updated` | `string` | `True` | ISO 8601 UTC timestamp. | altnames=`{"json": "TimeUpdated"}` | - | - |
| `start_location_name` | `string` | `True` | Start location name. | altnames=`{"json": "StartLocationName"}` | - | - |
| `start_latitude` | `double` | `True` | Start latitude. | unit=`deg` symbol=`°`<br>altnames=`{"json": "StartLatitude"}` | - | - |
| `start_longitude` | `double` | `True` | Start longitude. | unit=`deg` symbol=`°`<br>altnames=`{"json": "StartLongitude"}` | - | - |
| `start_milepost` | `double` | `True` | Start milepost. | altnames=`{"json": "StartMilepost"}` | - | - |
| `end_location_name` | `string` | `True` | End location name. | altnames=`{"json": "EndLocationName"}` | - | - |
| `end_latitude` | `double` | `True` | End latitude. | unit=`deg` symbol=`°`<br>altnames=`{"json": "EndLatitude"}` | - | - |
| `end_longitude` | `double` | `True` | End longitude. | unit=`deg` symbol=`°`<br>altnames=`{"json": "EndLongitude"}` | - | - |
| `end_milepost` | `double` | `True` | End milepost. | altnames=`{"json": "EndMilepost"}` | - | - |

### Schemagroup `us.wa.wsdot.cvrestrictions.jstruct`
<a id="schemagroup-uswawsdotcvrestrictionsjstruct"></a>

#### Schema `us.wa.wsdot.cvrestrictions.CommercialVehicleRestriction`
<a id="schema-uswawsdotcvrestrictionscommercialvehiclerestriction"></a>

| Field | Value |
| --- | --- |
| Name | CommercialVehicleRestriction |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://real-time-sources.2030.io/schemas/us/wa/wsdot/cvrestrictions/CommercialVehicleRestriction` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/us/wa/wsdot/cvrestrictions/CommercialVehicleRestriction` |
| Type | `object` |

###### Object `CommercialVehicleRestriction`
<a id="schema-node-commercialvehiclerestriction"></a>

A commercial vehicle restriction on a Washington State highway bridge or road segment.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `state_route_id` | `string` | `True` | State route identifier, first part of composite key. | altnames=`{"json": "StateRouteID"}` | - | - |
| `bridge_number` | `string` | `True` | Bridge or structure number, second part of composite key. | altnames=`{"json": "BridgeNumber"}` | - | - |
| `bridge_name` | `union` | `True` | Bridge or structure name. | altnames=`{"json": "BridgeName"}` | - | - |
| `location_name` | `union` | `True` | Location relative to landmarks. | altnames=`{"json": "LocationName"}` | - | - |
| `location_description` | `union` | `True` | Detailed location description. | altnames=`{"json": "LocationDescription"}` | - | - |
| `latitude` | `double` | `True` | Latitude in WGS84. | unit=`deg` symbol=`°`<br>altnames=`{"json": "Latitude"}` | - | - |
| `longitude` | `double` | `True` | Longitude in WGS84. | unit=`deg` symbol=`°`<br>altnames=`{"json": "Longitude"}` | - | - |
| `state` | `union` | `True` | State abbreviation, typically WA. | altnames=`{"json": "State"}` | - | - |
| `restriction_type` | `union` | `True` | Type: BridgeRestriction, RoadRestriction. | altnames=`{"json": "RestrictionType"}` | - | - |
| `vehicle_type` | `union` | `True` | Affected vehicle type. | altnames=`{"json": "VehicleType"}` | - | - |
| `restriction_weight_in_pounds` | `union` | `True` | Axle weight limit in pounds. | unit=`lb` symbol=`lbs`<br>altnames=`{"json": "RestrictionWeightInPounds"}` | - | - |
| `maximum_gross_vehicle_weight_in_pounds` | `union` | `True` | GVW limit in pounds. | unit=`lb` symbol=`lbs`<br>altnames=`{"json": "MaximumGrossVehicleWeightInPounds"}` | - | - |
| `restriction_height_in_inches` | `union` | `True` | Height limit in inches. | unit=`in` symbol=`in`<br>altnames=`{"json": "RestrictionHeightInInches"}` | - | - |
| `restriction_width_in_inches` | `union` | `True` | Width limit in inches. | unit=`in` symbol=`in`<br>altnames=`{"json": "RestrictionWidthInInches"}` | - | - |
| `restriction_length_in_inches` | `union` | `True` | Length limit in inches. | unit=`in` symbol=`in`<br>altnames=`{"json": "RestrictionLengthInInches"}` | - | - |
| `is_permanent_restriction` | `boolean` | `True` | True if permanent. | altnames=`{"json": "IsPermanentRestriction"}` | - | - |
| `is_warning` | `boolean` | `True` | True if warning only. | altnames=`{"json": "IsWarning"}` | - | - |
| `is_detour_available` | `boolean` | `True` | True if detour exists. | altnames=`{"json": "IsDetourAvailable"}` | - | - |
| `is_exceptions_allowed` | `boolean` | `True` | True if permits available. | altnames=`{"json": "IsExceptionsAllowed"}` | - | - |
| `restriction_comment` | `union` | `True` | Additional details. | altnames=`{"json": "RestrictionComment"}` | - | - |
| `date_posted` | `union` | `True` | ISO 8601 UTC date posted. | altnames=`{"json": "DatePosted"}` | - | - |
| `date_effective` | `union` | `True` | ISO 8601 UTC date effective. | altnames=`{"json": "DateEffective"}` | - | - |
| `date_expires` | `union` | `True` | ISO 8601 UTC date expires. | altnames=`{"json": "DateExpires"}` | - | - |

### Schemagroup `us.wa.wsdot.border.jstruct`
<a id="schemagroup-uswawsdotborderjstruct"></a>

#### Schema `us.wa.wsdot.border.BorderCrossing`
<a id="schema-uswawsdotborderbordercrossing"></a>

| Field | Value |
| --- | --- |
| Name | BorderCrossing |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://real-time-sources.2030.io/schemas/us/wa/wsdot/border/BorderCrossing` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/us/wa/wsdot/border/BorderCrossing` |
| Type | `object` |

###### Object `BorderCrossing`
<a id="schema-node-bordercrossing"></a>

US-Canada border crossing wait time in Washington State.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `crossing_name` | `string` | `True` | Crossing lane identifier. | altnames=`{"json": "CrossingName"}` | - | - |
| `wait_time` | `union` | `True` | Wait time in minutes. | unit=`min` symbol=`min`<br>altnames=`{"json": "WaitTime"}` | - | - |
| `time` | `string` | `True` | ISO 8601 UTC measurement timestamp. | altnames=`{"json": "Time"}` | - | - |
| `description` | `union` | `True` | Lane description. | - | - | - |
| `road_name` | `union` | `True` | Road designation. | - | - | - |
| `latitude` | `double` | `True` | Latitude in WGS84. | unit=`deg` symbol=`°` | - | - |
| `longitude` | `double` | `True` | Longitude in WGS84. | unit=`deg` symbol=`°` | - | - |

### Schemagroup `us.wa.wsdot.ferries.jstruct`
<a id="schemagroup-uswawsdotferriesjstruct"></a>

#### Schema `us.wa.wsdot.ferries.VesselLocation`
<a id="schema-uswawsdotferriesvessellocation"></a>

| Field | Value |
| --- | --- |
| Name | VesselLocation |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://real-time-sources.2030.io/schemas/us/wa/wsdot/ferries/VesselLocation` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/us/wa/wsdot/ferries/VesselLocation` |
| Type | `object` |

###### Object `VesselLocation`
<a id="schema-node-vessellocation"></a>

Real-time location and status of a Washington State Ferries vessel.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `vessel_id` | `string` | `True` | Vessel identifier, stringified from upstream VesselID. | altnames=`{"json": "VesselID"}` | - | - |
| `vessel_name` | `string` | `True` | Ferry vessel name. | altnames=`{"json": "VesselName"}` | - | - |
| `mmsi` | `union` | `True` | Maritime Mobile Service Identity for AIS. | altnames=`{"json": "Mmsi"}` | - | - |
| `in_service` | `boolean` | `True` | True if in active service. | altnames=`{"json": "InService"}` | - | - |
| `at_dock` | `boolean` | `True` | True if docked. | altnames=`{"json": "AtDock"}` | - | - |
| `latitude` | `double` | `True` | Latitude in WGS84. | unit=`deg` symbol=`°`<br>altnames=`{"json": "Latitude"}` | - | - |
| `longitude` | `double` | `True` | Longitude in WGS84. | unit=`deg` symbol=`°`<br>altnames=`{"json": "Longitude"}` | - | - |
| `speed` | `union` | `True` | Speed in knots. | unit=`kn` symbol=`kn`<br>altnames=`{"json": "Speed"}` | - | - |
| `heading` | `union` | `True` | Heading in degrees. | unit=`deg` symbol=`°`<br>altnames=`{"json": "Heading"}` | - | - |
| `departing_terminal_id` | `union` | `True` | Departure terminal ID. | altnames=`{"json": "DepartingTerminalID"}` | - | - |
| `departing_terminal_name` | `union` | `True` | Departure terminal name. | altnames=`{"json": "DepartingTerminalName"}` | - | - |
| `departing_terminal_abbrev` | `union` | `True` | Departure terminal abbreviation. | altnames=`{"json": "DepartingTerminalAbbrev"}` | - | - |
| `arriving_terminal_id` | `union` | `True` | Arrival terminal ID. | altnames=`{"json": "ArrivingTerminalID"}` | - | - |
| `arriving_terminal_name` | `union` | `True` | Arrival terminal name. | altnames=`{"json": "ArrivingTerminalName"}` | - | - |
| `arriving_terminal_abbrev` | `union` | `True` | Arrival terminal abbreviation. | altnames=`{"json": "ArrivingTerminalAbbrev"}` | - | - |
| `scheduled_departure` | `union` | `True` | ISO 8601 UTC scheduled departure. | altnames=`{"json": "ScheduledDeparture"}` | - | - |
| `left_dock` | `union` | `True` | ISO 8601 UTC actual departure. | altnames=`{"json": "LeftDock"}` | - | - |
| `eta` | `union` | `True` | ISO 8601 UTC estimated arrival. | altnames=`{"json": "Eta"}` | - | - |
| `eta_basis` | `union` | `True` | ETA calculation description. | altnames=`{"json": "EtaBasis"}` | - | - |
| `route_abbreviation` | `union` | `True` | Current route abbreviation. | - | - | - |
| `timestamp` | `string` | `True` | ISO 8601 UTC position timestamp. | altnames=`{"json": "TimeStamp"}` | - | - |

### Schemagroup `us.wa.wsdot.traffic.avro`
<a id="schemagroup-uswawsdottrafficavro"></a>

#### Schema `us.wa.wsdot.traffic.TrafficFlowStation`
<a id="schema-uswawsdottraffictrafficflowstation"></a>

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
| Name | TrafficFlowStation |
| Namespace | us.wa.wsdot.traffic |
| Type | `record` |
| Doc | Traffic flow sensor station metadata. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `flow_data_id` | `string` |  | `-` |
| `station_name` | `string` |  | `-` |
| `region` | `string` |  | `-` |
| `description` | `null` \| `string` |  | `-` |
| `road_name` | `string` |  | `-` |
| `direction` | `null` \| `string` |  | `-` |
| `milepost` | `null` \| `double` |  | `-` |
| `latitude` | `double` |  | `-` |
| `longitude` | `double` |  | `-` |

#### Schema `us.wa.wsdot.traffic.TrafficFlowReading`
<a id="schema-uswawsdottraffictrafficflowreading"></a>

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
| Name | TrafficFlowReading |
| Namespace | us.wa.wsdot.traffic |
| Type | `record` |
| Doc | Traffic flow reading. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `flow_data_id` | `string` |  | `-` |
| `station_name` | `string` |  | `-` |
| `region` | `string` |  | `-` |
| `flow_reading` | `string` |  | `-` |
| `reading_time` | `string` |  | `-` |

### Schemagroup `us.wa.wsdot.traveltimes.avro`
<a id="schemagroup-uswawsdottraveltimesavro"></a>

#### Schema `us.wa.wsdot.traveltimes.TravelTimeRoute`
<a id="schema-uswawsdottraveltimestraveltimeroute"></a>

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
| Name | TravelTimeRoute |
| Namespace | us.wa.wsdot.traveltimes |
| Type | `record` |
| Doc | Travel time route. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `travel_time_id` | `string` |  | `-` |
| `name` | `string` |  | `-` |
| `description` | `string` |  | `-` |
| `distance` | `double` |  | `-` |
| `average_time` | `int` |  | `-` |
| `current_time` | `int` |  | `-` |
| `time_updated` | `string` |  | `-` |
| `start_description` | `null` \| `string` |  | `-` |
| `start_road_name` | `null` \| `string` |  | `-` |
| `start_direction` | `null` \| `string` |  | `-` |
| `start_milepost` | `null` \| `double` |  | `-` |
| `start_latitude` | `double` |  | `-` |
| `start_longitude` | `double` |  | `-` |
| `end_description` | `null` \| `string` |  | `-` |
| `end_road_name` | `null` \| `string` |  | `-` |
| `end_direction` | `null` \| `string` |  | `-` |
| `end_milepost` | `null` \| `double` |  | `-` |
| `end_latitude` | `double` |  | `-` |
| `end_longitude` | `double` |  | `-` |

### Schemagroup `us.wa.wsdot.mountainpass.avro`
<a id="schemagroup-uswawsdotmountainpassavro"></a>

#### Schema `us.wa.wsdot.mountainpass.MountainPassCondition`
<a id="schema-uswawsdotmountainpassmountainpasscondition"></a>

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
| Name | MountainPassCondition |
| Namespace | us.wa.wsdot.mountainpass |
| Type | `record` |
| Doc | Mountain pass conditions. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `mountain_pass_id` | `string` |  | `-` |
| `mountain_pass_name` | `string` |  | `-` |
| `elevation_in_feet` | `int` |  | `-` |
| `latitude` | `double` |  | `-` |
| `longitude` | `double` |  | `-` |
| `temperature_in_fahrenheit` | `null` \| `int` |  | `-` |
| `weather_condition` | `string` |  | `-` |
| `road_condition` | `string` |  | `-` |
| `travel_advisory_active` | `boolean` |  | `-` |
| `restriction_one_direction` | `null` \| `string` |  | `-` |
| `restriction_one_text` | `null` \| `string` |  | `-` |
| `restriction_two_direction` | `null` \| `string` |  | `-` |
| `restriction_two_text` | `null` \| `string` |  | `-` |
| `date_updated` | `string` |  | `-` |

### Schemagroup `us.wa.wsdot.weather.avro`
<a id="schemagroup-uswawsdotweatheravro"></a>

#### Schema `us.wa.wsdot.weather.WeatherStation`
<a id="schema-uswawsdotweatherweatherstation"></a>

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
| Name | WeatherStation |
| Namespace | us.wa.wsdot.weather |
| Type | `record` |
| Doc | WSDOT weather station metadata. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` |  | `-` |
| `station_name` | `string` |  | `-` |
| `latitude` | `double` |  | `-` |
| `longitude` | `double` |  | `-` |

#### Schema `us.wa.wsdot.weather.WeatherReading`
<a id="schema-uswawsdotweatherweatherreading"></a>

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
| Name | WeatherReading |
| Namespace | us.wa.wsdot.weather |
| Type | `record` |
| Doc | Weather reading. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` |  | `-` |
| `station_name` | `string` |  | `-` |
| `reading_time` | `string` |  | `-` |
| `temperature_in_fahrenheit` | `null` \| `double` |  | `-` |
| `precipitation_in_inches` | `null` \| `double` |  | `-` |
| `wind_speed_in_mph` | `null` \| `double` |  | `-` |
| `wind_gust_speed_in_mph` | `null` \| `double` |  | `-` |
| `wind_direction` | `null` \| `int` |  | `-` |
| `wind_direction_cardinal` | `null` \| `string` |  | `-` |
| `barometric_pressure` | `null` \| `double` |  | `-` |
| `relative_humidity` | `null` \| `int` |  | `-` |
| `visibility` | `null` \| `double` |  | `-` |
| `sky_coverage` | `null` \| `string` |  | `-` |
| `latitude` | `double` |  | `-` |
| `longitude` | `double` |  | `-` |

### Schemagroup `us.wa.wsdot.tolls.avro`
<a id="schemagroup-uswawsdottollsavro"></a>

#### Schema `us.wa.wsdot.tolls.TollRate`
<a id="schema-uswawsdottollstollrate"></a>

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
| Name | TollRate |
| Namespace | us.wa.wsdot.tolls |
| Type | `record` |
| Doc | Toll rate. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `trip_name` | `string` |  | `-` |
| `state_route` | `string` |  | `-` |
| `travel_direction` | `string` |  | `-` |
| `current_toll` | `int` |  | `-` |
| `current_message` | `null` \| `string` |  | `-` |
| `time_updated` | `string` |  | `-` |
| `start_location_name` | `string` |  | `-` |
| `start_latitude` | `double` |  | `-` |
| `start_longitude` | `double` |  | `-` |
| `start_milepost` | `double` |  | `-` |
| `end_location_name` | `string` |  | `-` |
| `end_latitude` | `double` |  | `-` |
| `end_longitude` | `double` |  | `-` |
| `end_milepost` | `double` |  | `-` |

### Schemagroup `us.wa.wsdot.cvrestrictions.avro`
<a id="schemagroup-uswawsdotcvrestrictionsavro"></a>

#### Schema `us.wa.wsdot.cvrestrictions.CommercialVehicleRestriction`
<a id="schema-uswawsdotcvrestrictionscommercialvehiclerestriction"></a>

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
| Name | CommercialVehicleRestriction |
| Namespace | us.wa.wsdot.cvrestrictions |
| Type | `record` |
| Doc | Commercial vehicle restriction. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `state_route_id` | `string` |  | `-` |
| `bridge_number` | `string` |  | `-` |
| `bridge_name` | `null` \| `string` |  | `-` |
| `location_name` | `null` \| `string` |  | `-` |
| `location_description` | `null` \| `string` |  | `-` |
| `latitude` | `double` |  | `-` |
| `longitude` | `double` |  | `-` |
| `state` | `null` \| `string` |  | `-` |
| `restriction_type` | `null` \| `string` |  | `-` |
| `vehicle_type` | `null` \| `string` |  | `-` |
| `restriction_weight_in_pounds` | `null` \| `int` |  | `-` |
| `maximum_gross_vehicle_weight_in_pounds` | `null` \| `int` |  | `-` |
| `restriction_height_in_inches` | `null` \| `int` |  | `-` |
| `restriction_width_in_inches` | `null` \| `int` |  | `-` |
| `restriction_length_in_inches` | `null` \| `int` |  | `-` |
| `is_permanent_restriction` | `boolean` |  | `-` |
| `is_warning` | `boolean` |  | `-` |
| `is_detour_available` | `boolean` |  | `-` |
| `is_exceptions_allowed` | `boolean` |  | `-` |
| `restriction_comment` | `null` \| `string` |  | `-` |
| `date_posted` | `null` \| `string` |  | `-` |
| `date_effective` | `null` \| `string` |  | `-` |
| `date_expires` | `null` \| `string` |  | `-` |

### Schemagroup `us.wa.wsdot.border.avro`
<a id="schemagroup-uswawsdotborderavro"></a>

#### Schema `us.wa.wsdot.border.BorderCrossing`
<a id="schema-uswawsdotborderbordercrossing"></a>

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
| Name | BorderCrossing |
| Namespace | us.wa.wsdot.border |
| Type | `record` |
| Doc | Border crossing wait time. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `crossing_name` | `string` |  | `-` |
| `wait_time` | `null` \| `int` |  | `-` |
| `time` | `string` |  | `-` |
| `description` | `null` \| `string` |  | `-` |
| `road_name` | `null` \| `string` |  | `-` |
| `latitude` | `double` |  | `-` |
| `longitude` | `double` |  | `-` |

### Schemagroup `us.wa.wsdot.ferries.avro`
<a id="schemagroup-uswawsdotferriesavro"></a>

#### Schema `us.wa.wsdot.ferries.VesselLocation`
<a id="schema-uswawsdotferriesvessellocation"></a>

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
| Name | VesselLocation |
| Namespace | us.wa.wsdot.ferries |
| Type | `record` |
| Doc | WSF vessel location. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `vessel_id` | `string` |  | `-` |
| `vessel_name` | `string` |  | `-` |
| `mmsi` | `null` \| `int` |  | `-` |
| `in_service` | `boolean` |  | `-` |
| `at_dock` | `boolean` |  | `-` |
| `latitude` | `double` |  | `-` |
| `longitude` | `double` |  | `-` |
| `speed` | `null` \| `double` |  | `-` |
| `heading` | `null` \| `int` |  | `-` |
| `departing_terminal_id` | `null` \| `int` |  | `-` |
| `departing_terminal_name` | `null` \| `string` |  | `-` |
| `departing_terminal_abbrev` | `null` \| `string` |  | `-` |
| `arriving_terminal_id` | `null` \| `int` |  | `-` |
| `arriving_terminal_name` | `null` \| `string` |  | `-` |
| `arriving_terminal_abbrev` | `null` \| `string` |  | `-` |
| `scheduled_departure` | `null` \| `string` |  | `-` |
| `left_dock` | `null` \| `string` |  | `-` |
| `eta` | `null` \| `string` |  | `-` |
| `eta_basis` | `null` \| `string` |  | `-` |
| `route_abbreviation` | `null` \| `string` |  | `-` |
| `timestamp` | `string` |  | `-` |
