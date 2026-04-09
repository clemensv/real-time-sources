# US CBP Border Wait Times Bridge Events

This document describes the events emitted by the US CBP Border Wait Times Bridge.

- [gov.cbp.borderwait](#message-group-govcbpborderwait)
  - [gov.cbp.borderwait.Port](#message-govcbpborderwaitport)
  - [gov.cbp.borderwait.WaitTime](#message-govcbpborderwaitwaittime)

---

## Message Group: gov.cbp.borderwait

---

### Message: gov.cbp.borderwait.Port

*Reference data — sent once at startup before telemetry polling begins.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` | CloudEvent type | `string` | `True` | `gov.cbp.borderwait.Port` |
| `source` | CloudEvent source | `string` | `True` | `https://bwt.cbp.gov` |
| `subject` | Port number | `uritemplate` | `True` | `{port_number}` |

#### Schema: Port

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `port_number` | *string* | Six-digit CBP port number that uniquely identifies this crossing |
| `port_name` | *string* | Name of the city or locality where the port is located |
| `border` | *string* | Which international border this port serves ('Canadian Border' or 'Mexican Border') |
| `crossing_name` | *string* | Name of the specific border crossing facility |
| `hours` | *string* | Operating hours of the port as a human-readable string |
| `passenger_vehicle_max_lanes` | *integer / null* | Maximum number of passenger vehicle inspection lanes |
| `commercial_vehicle_max_lanes` | *integer / null* | Maximum number of commercial vehicle inspection lanes |
| `pedestrian_max_lanes` | *integer / null* | Maximum number of pedestrian inspection lanes |

---

### Message: gov.cbp.borderwait.WaitTime

*Telemetry — current wait times per port, polled approximately hourly.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` | CloudEvent type | `string` | `True` | `gov.cbp.borderwait.WaitTime` |
| `source` | CloudEvent source | `string` | `True` | `https://bwt.cbp.gov` |
| `subject` | Port number | `uritemplate` | `True` | `{port_number}` |

#### Schema: WaitTime

| **Field Name** | **Type** | **Unit** | **Description** |
|----------------|----------|----------|-----------------|
| `port_number` | *string* | — | Six-digit CBP port number |
| `port_name` | *string* | — | City or locality name |
| `border` | *string* | — | International border |
| `crossing_name` | *string* | — | Crossing facility name |
| `port_status` | *string* | — | Overall port operational status |
| `date` | *string* | — | Report date in US format (M/D/YYYY) |
| `time` | *string* | — | Report time in HH:MM:SS local time |
| `passenger_vehicle_standard_delay` | *integer / null* | min | Standard passenger vehicle delay |
| `passenger_vehicle_standard_lanes_open` | *integer / null* | — | Standard passenger vehicle lanes open |
| `passenger_vehicle_standard_operational_status` | *string / null* | — | Standard passenger vehicle status |
| `passenger_vehicle_nexus_sentri_delay` | *integer / null* | min | NEXUS/SENTRI passenger vehicle delay |
| `passenger_vehicle_nexus_sentri_lanes_open` | *integer / null* | — | NEXUS/SENTRI passenger vehicle lanes open |
| `passenger_vehicle_nexus_sentri_operational_status` | *string / null* | — | NEXUS/SENTRI passenger vehicle status |
| `passenger_vehicle_ready_delay` | *integer / null* | min | Ready Lane passenger vehicle delay |
| `passenger_vehicle_ready_lanes_open` | *integer / null* | — | Ready Lane passenger vehicle lanes open |
| `passenger_vehicle_ready_operational_status` | *string / null* | — | Ready Lane passenger vehicle status |
| `pedestrian_standard_delay` | *integer / null* | min | Standard pedestrian delay |
| `pedestrian_standard_lanes_open` | *integer / null* | — | Standard pedestrian lanes open |
| `pedestrian_standard_operational_status` | *string / null* | — | Standard pedestrian status |
| `pedestrian_ready_delay` | *integer / null* | min | Ready Lane pedestrian delay |
| `pedestrian_ready_lanes_open` | *integer / null* | — | Ready Lane pedestrian lanes open |
| `pedestrian_ready_operational_status` | *string / null* | — | Ready Lane pedestrian status |
| `commercial_vehicle_standard_delay` | *integer / null* | min | Standard commercial vehicle delay |
| `commercial_vehicle_standard_lanes_open` | *integer / null* | — | Standard commercial vehicle lanes open |
| `commercial_vehicle_standard_operational_status` | *string / null* | — | Standard commercial vehicle status |
| `commercial_vehicle_fast_delay` | *integer / null* | min | FAST commercial vehicle delay |
| `commercial_vehicle_fast_lanes_open` | *integer / null* | — | FAST commercial vehicle lanes open |
| `commercial_vehicle_fast_operational_status` | *string / null* | — | FAST commercial vehicle status |
| `construction_notice` | *string / null* | — | Construction or closure notice text |
