"""NMEA AIS decoder — wraps pyais, handles multi-sentence reassembly."""

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

from pyais.messages import NMEAMessage

logger = logging.getLogger(__name__)

# AIS message types we care about
POSITION_CLASS_A = {1, 2, 3}
STATIC_VOYAGE = {5}
POSITION_CLASS_B = {18, 19}
STATIC_CLASS_B = {24}
AID_TO_NAV = {21}
SUPPORTED_TYPES = POSITION_CLASS_A | STATIC_VOYAGE | POSITION_CLASS_B | STATIC_CLASS_B | AID_TO_NAV


@dataclass
class DecodedAIS:
    """A fully decoded AIS message with metadata."""
    msg_type: int
    event_type: str
    mmsi: int
    station_id: str
    receive_time: datetime
    fields: Dict[str, Any]


def _safe_int(val: Any, default: int = 0) -> int:
    if val is None:
        return default
    try:
        return int(val)
    except (ValueError, TypeError):
        return default


def _safe_float(val: Any, default: float = 0.0) -> float:
    if val is None:
        return default
    try:
        return float(val)
    except (ValueError, TypeError):
        return default


def _safe_str(val: Any) -> str:
    if val is None:
        return ""
    s = str(val).strip().rstrip('@')
    return s


def _map_position_class_a(decoded: Any, station_id: str, timestamp: str, msg_type: int) -> Dict[str, Any]:
    return {
        "mmsi": _safe_int(decoded.mmsi),
        "navigation_status": _safe_int(decoded.status),
        "rate_of_turn": _safe_float(decoded.turn, -128.0),
        "speed_over_ground": _safe_float(decoded.speed, 102.3),
        "position_accuracy": _safe_int(decoded.accuracy),
        "longitude": _safe_float(decoded.lon, 181.0),
        "latitude": _safe_float(decoded.lat, 91.0),
        "course_over_ground": _safe_float(decoded.course, 360.0),
        "true_heading": _safe_int(decoded.heading, 511),
        "timestamp": timestamp,
        "station_id": station_id,
        "msg_type": msg_type,
    }


def _map_static_voyage(decoded: Any, station_id: str, timestamp: str) -> Dict[str, Any]:
    return {
        "mmsi": _safe_int(decoded.mmsi),
        "imo_number": _safe_int(decoded.imo),
        "callsign": _safe_str(decoded.callsign),
        "ship_name": _safe_str(decoded.shipname),
        "ship_type": _safe_int(decoded.ship_type),
        "dimension_to_bow": _safe_int(decoded.to_bow),
        "dimension_to_stern": _safe_int(decoded.to_stern),
        "dimension_to_port": _safe_int(decoded.to_port),
        "dimension_to_starboard": _safe_int(decoded.to_starboard),
        "draught": _safe_float(decoded.draught),
        "destination": _safe_str(decoded.destination),
        "eta_month": _safe_int(decoded.month),
        "eta_day": _safe_int(decoded.day),
        "eta_hour": _safe_int(decoded.hour),
        "eta_minute": _safe_int(decoded.minute),
        "timestamp": timestamp,
        "station_id": station_id,
    }


def _map_position_class_b(decoded: Any, station_id: str, timestamp: str, msg_type: int) -> Dict[str, Any]:
    return {
        "mmsi": _safe_int(decoded.mmsi),
        "speed_over_ground": _safe_float(decoded.speed, 102.3),
        "position_accuracy": _safe_int(decoded.accuracy),
        "longitude": _safe_float(decoded.lon, 181.0),
        "latitude": _safe_float(decoded.lat, 91.0),
        "course_over_ground": _safe_float(decoded.course, 360.0),
        "true_heading": _safe_int(decoded.heading, 511),
        "timestamp": timestamp,
        "station_id": station_id,
        "msg_type": msg_type,
    }


def _map_static_class_b(decoded: Any, station_id: str, timestamp: str) -> Dict[str, Any]:
    result = {
        "mmsi": _safe_int(decoded.mmsi),
        "part_number": _safe_int(decoded.partnum),
        "timestamp": timestamp,
        "station_id": station_id,
    }
    # Part A has ship name, Part B has callsign, ship type, dimensions
    if hasattr(decoded, 'shipname') and decoded.shipname:
        result["ship_name"] = _safe_str(decoded.shipname)
    else:
        result["ship_name"] = ""
    if hasattr(decoded, 'callsign') and decoded.callsign:
        result["callsign"] = _safe_str(decoded.callsign)
    else:
        result["callsign"] = ""
    result["ship_type"] = _safe_int(getattr(decoded, 'ship_type', 0))
    result["dimension_to_bow"] = _safe_int(getattr(decoded, 'to_bow', 0))
    result["dimension_to_stern"] = _safe_int(getattr(decoded, 'to_stern', 0))
    result["dimension_to_port"] = _safe_int(getattr(decoded, 'to_port', 0))
    result["dimension_to_starboard"] = _safe_int(getattr(decoded, 'to_starboard', 0))
    return result


def _map_aid_to_nav(decoded: Any, station_id: str, timestamp: str) -> Dict[str, Any]:
    return {
        "mmsi": _safe_int(decoded.mmsi),
        "aid_type": _safe_int(decoded.aid_type),
        "name": _safe_str(decoded.name),
        "position_accuracy": _safe_int(decoded.accuracy),
        "longitude": _safe_float(decoded.lon, 181.0),
        "latitude": _safe_float(decoded.lat, 91.0),
        "timestamp": timestamp,
        "station_id": station_id,
    }


class NMEADecoder:
    """Decodes AIS NMEA sentences, handling multi-sentence reassembly."""

    def __init__(self, message_types: Optional[set] = None):
        self._message_types = message_types or SUPPORTED_TYPES
        # Buffer for multi-sentence messages: key = (channel, seq_id)
        self._fragments: Dict[tuple, List[str]] = {}

    def decode_sentence(self, nmea: str, station_id: str,
                        receive_time: datetime) -> Optional[DecodedAIS]:
        """Decode a single NMEA sentence. Returns DecodedAIS if a complete
        message is available, None if still buffering fragments."""
        parts = nmea.split(',')
        if len(parts) < 6:
            return None

        try:
            frag_count = int(parts[1])
            frag_num = int(parts[2])
        except (ValueError, IndexError):
            return None

        if frag_count == 1:
            # Single-sentence message
            return self._try_decode(nmea, station_id, receive_time)

        # Multi-sentence: buffer fragments
        channel = parts[4]
        seq_id = parts[3]
        key = (channel, seq_id)

        if frag_num == 1:
            self._fragments[key] = [nmea]
        elif key in self._fragments:
            self._fragments[key].append(nmea)
        else:
            # Missed the first fragment
            return None

        if len(self._fragments[key]) == frag_count:
            # All fragments received — reassemble
            sentences = self._fragments.pop(key)
            return self._try_decode_multi(sentences, station_id, receive_time)

        return None

    def _try_decode(self, nmea: str, station_id: str,
                    receive_time: datetime) -> Optional[DecodedAIS]:
        """Decode a single-sentence NMEA message."""
        try:
            msg = NMEAMessage(nmea.encode())
            decoded = msg.decode()
            return self._map_decoded(decoded, station_id, receive_time)
        except Exception as e:
            logger.debug("Failed to decode NMEA: %s (%s)", nmea[:60], e)
            return None

    def _try_decode_multi(self, sentences: List[str], station_id: str,
                          receive_time: datetime) -> Optional[DecodedAIS]:
        """Decode a multi-sentence NMEA message."""
        try:
            msgs = [NMEAMessage(s.encode()) for s in sentences]
            assembled = NMEAMessage.assemble_from_iterable(msgs)
            decoded = assembled.decode()
            return self._map_decoded(decoded, station_id, receive_time)
        except Exception as e:
            logger.debug("Failed to decode multi-sentence: %s (%s)", sentences[0][:60], e)
            return None

    def _map_decoded(self, decoded: Any, station_id: str,
                     receive_time: datetime) -> Optional[DecodedAIS]:
        """Map a pyais decoded message to our DecodedAIS structure."""
        msg_type = decoded.msg_type
        if msg_type not in self._message_types:
            return None

        timestamp = receive_time.isoformat()

        if msg_type in POSITION_CLASS_A:
            fields = _map_position_class_a(decoded, station_id, timestamp, msg_type)
            event_type = "position_report_class_a"
        elif msg_type in STATIC_VOYAGE:
            fields = _map_static_voyage(decoded, station_id, timestamp)
            event_type = "static_voyage_data"
        elif msg_type in POSITION_CLASS_B:
            fields = _map_position_class_b(decoded, station_id, timestamp, msg_type)
            event_type = "position_report_class_b"
        elif msg_type in STATIC_CLASS_B:
            fields = _map_static_class_b(decoded, station_id, timestamp)
            event_type = "static_data_class_b"
        elif msg_type in AID_TO_NAV:
            fields = _map_aid_to_nav(decoded, station_id, timestamp)
            event_type = "aid_to_navigation"
        else:
            return None

        return DecodedAIS(
            msg_type=msg_type,
            event_type=event_type,
            mmsi=fields["mmsi"],
            station_id=station_id,
            receive_time=receive_time,
            fields=fields,
        )
