# WSDOT Traveler Information Events

This document describes the events emitted by the WSDOT Traveler Information bridge.

- [us.wa.wsdot.traffic](#message-group-uswawsdottraffic)
  - [us.wa.wsdot.traffic.TrafficFlowStation](#message-uswawsdottraffictrafficflowstation)
  - [us.wa.wsdot.traffic.TrafficFlowReading](#message-uswawsdottraffictrafficflowreading)
- [us.wa.wsdot.traveltimes](#message-group-uswawsdottraveltimes)
  - [us.wa.wsdot.traveltimes.TravelTimeRoute](#message-uswawsdottraveltimestraveltimeroute)
- [us.wa.wsdot.mountainpass](#message-group-uswawsdotmountainpass)
  - [us.wa.wsdot.mountainpass.MountainPassCondition](#message-uswawsdotmountainpassmountainpasscondition)
- [us.wa.wsdot.weather](#message-group-uswawsdotweather)
  - [us.wa.wsdot.weather.WeatherStation](#message-uswawsdotweatherweatherstation)
  - [us.wa.wsdot.weather.WeatherReading](#message-uswawsdotweatherweatherreading)
- [us.wa.wsdot.tolls](#message-group-uswawsdottolls)
  - [us.wa.wsdot.tolls.TollRate](#message-uswawsdottollstollrate)
- [us.wa.wsdot.cvrestrictions](#message-group-uswawsdotcvrestrictions)
  - [us.wa.wsdot.cvrestrictions.CommercialVehicleRestriction](#message-uswawsdotcvrestrictionscommercialvehiclerestriction)
- [us.wa.wsdot.border](#message-group-uswawsdotborder)
  - [us.wa.wsdot.border.BorderCrossing](#message-uswawsdotborderbordercrossing)
- [us.wa.wsdot.ferries](#message-group-uswawsdotferries)
  - [us.wa.wsdot.ferries.VesselLocation](#message-uswawsdotferriesvessellocation)

---

## Message Group: us.wa.wsdot.traffic

---

### Message: us.wa.wsdot.traffic.TrafficFlowStation

*Metadata for a traffic flow sensor station in the Washington State DOT network. WSDOT deploys approximately 1,400 inductive loop sensors embedded in highway pavement across four geographic regions.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `us.wa.wsdot.traffic.TrafficFlowStation` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{flow_data_id}` |

#### Schema:

##### Record: TrafficFlowStation

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
---

### Message: us.wa.wsdot.traffic.TrafficFlowReading

*A traffic flow reading from a WSDOT sensor station. Updated approximately every 90 seconds, each reading reports the current Level of Service.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `us.wa.wsdot.traffic.TrafficFlowReading` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{flow_data_id}` |

#### Schema:

##### Record: TrafficFlowReading

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
## Message Group: us.wa.wsdot.traveltimes

---

### Message: us.wa.wsdot.traveltimes.TravelTimeRoute

*A named travel time route monitored by WSDOT. Each route has fixed start and end points on Washington State highways with historical average and current real-time travel times.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `us.wa.wsdot.traveltimes.TravelTimeRoute` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{travel_time_id}` |

#### Schema:

##### Record: TravelTimeRoute

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
## Message Group: us.wa.wsdot.mountainpass

---

### Message: us.wa.wsdot.mountainpass.MountainPassCondition

*Current conditions at a Washington State mountain pass including temperature, weather, road conditions, travel advisories, and directional restrictions.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `us.wa.wsdot.mountainpass.MountainPassCondition` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{mountain_pass_id}` |

#### Schema:

##### Record: MountainPassCondition

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
## Message Group: us.wa.wsdot.weather

---

### Message: us.wa.wsdot.weather.WeatherStation

*Metadata for a WSDOT road weather information system (RWIS) station. WSDOT operates approximately 134 stations across Washington State highways.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `us.wa.wsdot.weather.WeatherStation` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:

##### Record: WeatherStation

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
---

### Message: us.wa.wsdot.weather.WeatherReading

*A current weather reading from a WSDOT road weather station including temperature, wind, precipitation, pressure, humidity, visibility, and sky coverage.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `us.wa.wsdot.weather.WeatherReading` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:

##### Record: WeatherReading

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
## Message Group: us.wa.wsdot.tolls

---

### Message: us.wa.wsdot.tolls.TollRate

*Current toll rate for a WSDOT tolled route segment. WSDOT operates dynamic tolling on SR 99, I-405, and SR 167.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `us.wa.wsdot.tolls.TollRate` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{trip_name}` |

#### Schema:

##### Record: TollRate

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
## Message Group: us.wa.wsdot.cvrestrictions

---

### Message: us.wa.wsdot.cvrestrictions.CommercialVehicleRestriction

*A commercial vehicle restriction on a Washington State highway bridge or road segment. Restrictions limit vehicle weight, height, length, or width.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `us.wa.wsdot.cvrestrictions.CommercialVehicleRestriction` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{state_route_id}/{bridge_number}` |

#### Schema:

##### Record: CommercialVehicleRestriction

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
## Message Group: us.wa.wsdot.border

---

### Message: us.wa.wsdot.border.BorderCrossing

*Current wait time at a US-Canada border crossing lane in Washington State. Wait times are in minutes, updated approximately every 5 minutes.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `us.wa.wsdot.border.BorderCrossing` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{crossing_name}` |

#### Schema:

##### Record: BorderCrossing

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
## Message Group: us.wa.wsdot.ferries

---

### Message: us.wa.wsdot.ferries.VesselLocation

*Real-time location and status of a Washington State Ferries vessel. WSF operates approximately 21 vessels across Puget Sound routes.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `us.wa.wsdot.ferries.VesselLocation` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{vessel_id}` |

#### Schema:

##### Record: VesselLocation

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
