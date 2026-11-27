"""Synthetic decoded AIS records for bounded feeder checks."""

from datetime import datetime, timezone

from .nmea_decoder import DecodedAIS


def mock_ais_corpus() -> tuple[DecodedAIS, ...]:
    """Return one record per family, with static data before its position."""
    now = datetime.now(timezone.utc).isoformat()
    static = DecodedAIS(
        msg_type=5,
        event_type="static_voyage_data",
        mmsi=257_555_001,
        station_id="MOCK-NO",
        receive_time=datetime.now(timezone.utc),
        fields={
            "mmsi": 257_555_001,
            "imo_number": 9_111_222,
            "callsign": "LXXX",
            "ship_name": "MOCK FJORD CARGO",
            "ship_type": 70,
            "dimension_to_bow": 100,
            "dimension_to_stern": 50,
            "dimension_to_port": 10,
            "dimension_to_starboard": 22,
            "draught": 8.5,
            "destination": "NOOSL",
            "eta_month": 5, "eta_day": 23, "eta_hour": 12, "eta_minute": 0,
            "timestamp": now, "station_id": "MOCK-NO",
        },
    )
    position = DecodedAIS(
        msg_type=1,
        event_type="position_report_class_a",
        mmsi=257_555_001,
        station_id="MOCK-NO",
        receive_time=datetime.now(timezone.utc),
        fields={
            "mmsi": 257_555_001,
            "navigation_status": 0,
            "rate_of_turn": 0.0,
            "speed_over_ground": 12.3,
            "position_accuracy": 1,
            "longitude": 10.7522,
            "latitude": 59.9139,
            "course_over_ground": 95.1,
            "true_heading": 95,
            "timestamp": now,
            "station_id": "MOCK-NO",
            "msg_type": 1,
        },
    )
    aton = DecodedAIS(
        msg_type=21,
        event_type="aid_to_navigation",
        mmsi=992_257_001,
        station_id="MOCK-NO",
        receive_time=datetime.now(timezone.utc),
        fields={
            "mmsi": 992_257_001,
            "aid_type": 1,
            "name": "OSLOFJORD BUOY 7",
            "position_accuracy": 1,
            "longitude": 10.74,
            "latitude": 59.40,
            "timestamp": now,
            "station_id": "MOCK-NO",
        },
    )
    return static, position, aton
