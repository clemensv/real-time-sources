# Table of Contents

- [Mode_S](#message-group-modes)
  - [Mode_S.Messages](#message-modesmessages)
- [Mode_S.mqtt](#message-group-modesmqtt)
  - [Mode_S.ADSB.mqtt](#message-modesadsbmqtt)
  - [Mode_S.AltitudeReply.mqtt](#message-modesaltitudereplymqtt)
  - [Mode_S.IdentityReply.mqtt](#message-modesidentityreplymqtt)
  - [Mode_S.AcquisitionReply.mqtt](#message-modesacquisitionreplymqtt)
  - [Mode_S.CommBAltitude.mqtt](#message-modescommbaltitudemqtt)
  - [Mode_S.CommBIdentity.mqtt](#message-modescommbidentitymqtt)

---

## Message Group: Mode_S
---
### Message: Mode_S.Messages
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `Mode_S.Messages` |
| `source` | URL of the feed | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Partition key subject | `uritemplate` | `True` | `{stationid}` |

#### Schema:
##### Object: Messages
*A container for multiple Mode-S and ADS-B decoded messages.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `messages` | array of *unknown* | - | `True` | An array of Mode-S and ADS-B decoded message records. |
## Message Group: Mode_S.mqtt
---
### Message: Mode_S.ADSB.mqtt
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` |  | `string` | `True` | `1.0` |
| `type` |  | `string` | `True` | `Mode_S.mqtt.ADSB` |
| `source` |  | `uritemplate` | `True` | `{feedurl}` |
| `subject` |  | `uritemplate` | `True` | `{icao24}` |

#### Schema:
##### Object: Record
*Single Mode-S record published on the MQTT firehose. Carries the topic axes (icao24, receiver_id, msg_type) and the decoded record fields.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `icao24` | *string* | - | `True` | ICAO 24-bit address (lowercase hex). |
| `receiver_id` | *string* | - | `True` | Stable identifier of the receiver/station that decoded this message. |
| `msg_type` | *string* | - | `True` | Kebab-case Mode-S downlink-format family literal (df17-adsb, df4-altitude, df5-identity, df11-acquisition, df20-comm-b, df21-comm-b). |
| `ts` | *int64* | - | `True` | Reception timestamp (epoch millis). |
| `df` | *int32* | - | `True` | Downlink Format value. |
| `tc` | *int32* | - | `False` | Type Code (ADS-B only). |
| `bcode` | *string* | - | `False` | BDS code (Comm-B only). |
| `alt` | *int32* | - | `False` | Barometric altitude (ft). |
| `cs` | *string* | - | `False` | Aircraft callsign. |
| `sq` | *string* | - | `False` | Squawk code. |
| `lat` | *double* | - | `False` | Latitude (deg). |
| `lon` | *double* | - | `False` | Longitude (deg). |
| `spd` | *float* | - | `False` | Speed (kn). |
| `ang` | *float* | - | `False` | Heading angle (deg). |
| `vr` | *int32* | - | `False` | Vertical rate (ft/min). |
| `rssi` | *float* | - | `False` | RSSI (dBFS). |
---
### Message: Mode_S.AltitudeReply.mqtt
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` |  | `string` | `True` | `1.0` |
| `type` |  | `string` | `True` | `Mode_S.mqtt.AltitudeReply` |
| `source` |  | `uritemplate` | `True` | `{feedurl}` |
| `subject` |  | `uritemplate` | `True` | `{icao24}` |

#### Schema:
##### Object: Record
*Single Mode-S record published on the MQTT firehose. Carries the topic axes (icao24, receiver_id, msg_type) and the decoded record fields.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `icao24` | *string* | - | `True` | ICAO 24-bit address (lowercase hex). |
| `receiver_id` | *string* | - | `True` | Stable identifier of the receiver/station that decoded this message. |
| `msg_type` | *string* | - | `True` | Kebab-case Mode-S downlink-format family literal (df17-adsb, df4-altitude, df5-identity, df11-acquisition, df20-comm-b, df21-comm-b). |
| `ts` | *int64* | - | `True` | Reception timestamp (epoch millis). |
| `df` | *int32* | - | `True` | Downlink Format value. |
| `tc` | *int32* | - | `False` | Type Code (ADS-B only). |
| `bcode` | *string* | - | `False` | BDS code (Comm-B only). |
| `alt` | *int32* | - | `False` | Barometric altitude (ft). |
| `cs` | *string* | - | `False` | Aircraft callsign. |
| `sq` | *string* | - | `False` | Squawk code. |
| `lat` | *double* | - | `False` | Latitude (deg). |
| `lon` | *double* | - | `False` | Longitude (deg). |
| `spd` | *float* | - | `False` | Speed (kn). |
| `ang` | *float* | - | `False` | Heading angle (deg). |
| `vr` | *int32* | - | `False` | Vertical rate (ft/min). |
| `rssi` | *float* | - | `False` | RSSI (dBFS). |
---
### Message: Mode_S.IdentityReply.mqtt
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` |  | `string` | `True` | `1.0` |
| `type` |  | `string` | `True` | `Mode_S.mqtt.IdentityReply` |
| `source` |  | `uritemplate` | `True` | `{feedurl}` |
| `subject` |  | `uritemplate` | `True` | `{icao24}` |

#### Schema:
##### Object: Record
*Single Mode-S record published on the MQTT firehose. Carries the topic axes (icao24, receiver_id, msg_type) and the decoded record fields.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `icao24` | *string* | - | `True` | ICAO 24-bit address (lowercase hex). |
| `receiver_id` | *string* | - | `True` | Stable identifier of the receiver/station that decoded this message. |
| `msg_type` | *string* | - | `True` | Kebab-case Mode-S downlink-format family literal (df17-adsb, df4-altitude, df5-identity, df11-acquisition, df20-comm-b, df21-comm-b). |
| `ts` | *int64* | - | `True` | Reception timestamp (epoch millis). |
| `df` | *int32* | - | `True` | Downlink Format value. |
| `tc` | *int32* | - | `False` | Type Code (ADS-B only). |
| `bcode` | *string* | - | `False` | BDS code (Comm-B only). |
| `alt` | *int32* | - | `False` | Barometric altitude (ft). |
| `cs` | *string* | - | `False` | Aircraft callsign. |
| `sq` | *string* | - | `False` | Squawk code. |
| `lat` | *double* | - | `False` | Latitude (deg). |
| `lon` | *double* | - | `False` | Longitude (deg). |
| `spd` | *float* | - | `False` | Speed (kn). |
| `ang` | *float* | - | `False` | Heading angle (deg). |
| `vr` | *int32* | - | `False` | Vertical rate (ft/min). |
| `rssi` | *float* | - | `False` | RSSI (dBFS). |
---
### Message: Mode_S.AcquisitionReply.mqtt
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` |  | `string` | `True` | `1.0` |
| `type` |  | `string` | `True` | `Mode_S.mqtt.AcquisitionReply` |
| `source` |  | `uritemplate` | `True` | `{feedurl}` |
| `subject` |  | `uritemplate` | `True` | `{icao24}` |

#### Schema:
##### Object: Record
*Single Mode-S record published on the MQTT firehose. Carries the topic axes (icao24, receiver_id, msg_type) and the decoded record fields.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `icao24` | *string* | - | `True` | ICAO 24-bit address (lowercase hex). |
| `receiver_id` | *string* | - | `True` | Stable identifier of the receiver/station that decoded this message. |
| `msg_type` | *string* | - | `True` | Kebab-case Mode-S downlink-format family literal (df17-adsb, df4-altitude, df5-identity, df11-acquisition, df20-comm-b, df21-comm-b). |
| `ts` | *int64* | - | `True` | Reception timestamp (epoch millis). |
| `df` | *int32* | - | `True` | Downlink Format value. |
| `tc` | *int32* | - | `False` | Type Code (ADS-B only). |
| `bcode` | *string* | - | `False` | BDS code (Comm-B only). |
| `alt` | *int32* | - | `False` | Barometric altitude (ft). |
| `cs` | *string* | - | `False` | Aircraft callsign. |
| `sq` | *string* | - | `False` | Squawk code. |
| `lat` | *double* | - | `False` | Latitude (deg). |
| `lon` | *double* | - | `False` | Longitude (deg). |
| `spd` | *float* | - | `False` | Speed (kn). |
| `ang` | *float* | - | `False` | Heading angle (deg). |
| `vr` | *int32* | - | `False` | Vertical rate (ft/min). |
| `rssi` | *float* | - | `False` | RSSI (dBFS). |
---
### Message: Mode_S.CommBAltitude.mqtt
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` |  | `string` | `True` | `1.0` |
| `type` |  | `string` | `True` | `Mode_S.mqtt.CommBAltitude` |
| `source` |  | `uritemplate` | `True` | `{feedurl}` |
| `subject` |  | `uritemplate` | `True` | `{icao24}` |

#### Schema:
##### Object: Record
*Single Mode-S record published on the MQTT firehose. Carries the topic axes (icao24, receiver_id, msg_type) and the decoded record fields.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `icao24` | *string* | - | `True` | ICAO 24-bit address (lowercase hex). |
| `receiver_id` | *string* | - | `True` | Stable identifier of the receiver/station that decoded this message. |
| `msg_type` | *string* | - | `True` | Kebab-case Mode-S downlink-format family literal (df17-adsb, df4-altitude, df5-identity, df11-acquisition, df20-comm-b, df21-comm-b). |
| `ts` | *int64* | - | `True` | Reception timestamp (epoch millis). |
| `df` | *int32* | - | `True` | Downlink Format value. |
| `tc` | *int32* | - | `False` | Type Code (ADS-B only). |
| `bcode` | *string* | - | `False` | BDS code (Comm-B only). |
| `alt` | *int32* | - | `False` | Barometric altitude (ft). |
| `cs` | *string* | - | `False` | Aircraft callsign. |
| `sq` | *string* | - | `False` | Squawk code. |
| `lat` | *double* | - | `False` | Latitude (deg). |
| `lon` | *double* | - | `False` | Longitude (deg). |
| `spd` | *float* | - | `False` | Speed (kn). |
| `ang` | *float* | - | `False` | Heading angle (deg). |
| `vr` | *int32* | - | `False` | Vertical rate (ft/min). |
| `rssi` | *float* | - | `False` | RSSI (dBFS). |
---
### Message: Mode_S.CommBIdentity.mqtt
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` |  | `string` | `True` | `1.0` |
| `type` |  | `string` | `True` | `Mode_S.mqtt.CommBIdentity` |
| `source` |  | `uritemplate` | `True` | `{feedurl}` |
| `subject` |  | `uritemplate` | `True` | `{icao24}` |

#### Schema:
##### Object: Record
*Single Mode-S record published on the MQTT firehose. Carries the topic axes (icao24, receiver_id, msg_type) and the decoded record fields.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `icao24` | *string* | - | `True` | ICAO 24-bit address (lowercase hex). |
| `receiver_id` | *string* | - | `True` | Stable identifier of the receiver/station that decoded this message. |
| `msg_type` | *string* | - | `True` | Kebab-case Mode-S downlink-format family literal (df17-adsb, df4-altitude, df5-identity, df11-acquisition, df20-comm-b, df21-comm-b). |
| `ts` | *int64* | - | `True` | Reception timestamp (epoch millis). |
| `df` | *int32* | - | `True` | Downlink Format value. |
| `tc` | *int32* | - | `False` | Type Code (ADS-B only). |
| `bcode` | *string* | - | `False` | BDS code (Comm-B only). |
| `alt` | *int32* | - | `False` | Barometric altitude (ft). |
| `cs` | *string* | - | `False` | Aircraft callsign. |
| `sq` | *string* | - | `False` | Squawk code. |
| `lat` | *double* | - | `False` | Latitude (deg). |
| `lon` | *double* | - | `False` | Longitude (deg). |
| `spd` | *float* | - | `False` | Speed (kn). |
| `ang` | *float* | - | `False` | Heading angle (deg). |
| `vr` | *int32* | - | `False` | Vertical rate (ft/min). |
| `rssi` | *float* | - | `False` | RSSI (dBFS). |
