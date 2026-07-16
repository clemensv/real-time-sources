"""Tests for the ``celestrak_kafka`` feeder.

The Kafka producer is mocked so the full ``feed`` coroutine runs in ``--once``
mode without a live broker, asserting per-message key arguments, flush
semantics and the GP dedup-by-EPOCH watermark. A second block pins the
normalization helpers so the verbatim UPPERCASE CCSDS keys and the integer
``NORAD_CAT_ID`` survive onto the JSON wire.
"""

from __future__ import annotations

import asyncio
import json
from unittest import mock

import pytest

from celestrak_core import FeedConfig

SATCAT_ROW = {
    "OBJECT_NAME": "ISS (ZARYA)",
    "OBJECT_ID": "1998-067A",
    "NORAD_CAT_ID": 25544,
    "OBJECT_TYPE": "PAY",
    "OPS_STATUS_CODE": "+",
    "OWNER": "ISS",
    "LAUNCH_DATE": "1998-11-20",
    "LAUNCH_SITE": "TTMTR",
    "DECAY_DATE": None,
    "PERIOD": 92.9,
    "INCLINATION": 51.64,
    "APOGEE": 419,
    "PERIGEE": 413,
    "RCS": 401.3524,
    "DATA_STATUS_CODE": None,
    "ORBIT_CENTER": "EA",
    "ORBIT_TYPE": "ORB",
}

GP_ROW = {
    "OBJECT_NAME": "ISS (ZARYA)",
    "OBJECT_ID": "1998-067A",
    "EPOCH": "2026-07-16T12:00:00.000000",
    "MEAN_MOTION": 15.50103472,
    "ECCENTRICITY": 0.0007038,
    "INCLINATION": 51.6412,
    "RA_OF_ASC_NODE": 247.4627,
    "ARG_OF_PERICENTER": 130.536,
    "MEAN_ANOMALY": 325.0288,
    "EPHEMERIS_TYPE": 0,
    "CLASSIFICATION_TYPE": "U",
    "NORAD_CAT_ID": 25544,
    "ELEMENT_SET_NO": 999,
    "REV_AT_EPOCH": 45123,
    "BSTAR": 0.00016717,
    "MEAN_MOTION_DOT": 0.00010982,
    "MEAN_MOTION_DDOT": 0,
}


def _mock_api():
    api = mock.Mock()
    api.halted = False
    api.get_satcat.return_value = [SATCAT_ROW]
    api.get_gp.return_value = [GP_ROW]
    return api


def _run_feed(api, tmp_path, state=None):
    from celestrak_kafka import app as kafka_app

    state_file = tmp_path / "state.json"
    if state is not None:
        state_file.write_text(json.dumps(state))
    cfg = FeedConfig(
        groups=["stations"],
        supgp_sources=[],
        polling_interval=1,
        reference_refresh_interval=86400,
        state_file=str(state_file),
        once=True,
    )
    fake_raw_producer = mock.MagicMock()
    fake_event_producer = mock.MagicMock()
    with mock.patch.object(kafka_app, "Producer", return_value=fake_raw_producer), \
         mock.patch.object(kafka_app, "OrgCelestrakKafkaEventProducer",
                           return_value=fake_event_producer):
        asyncio.run(kafka_app.feed(
            api=api,
            kafka_config={"bootstrap.servers": "localhost:9092"},
            kafka_topic="celestrak",
            cfg=cfg,
        ))
    return fake_event_producer, state_file


@pytest.mark.unit
def test_kafka_feed_once_emits_satcat_and_gp(tmp_path):
    api = _mock_api()
    ep, state_file = _run_feed(api, tmp_path)

    assert ep.send_org_celestrak_kafka_satellite_catalog_entry.call_count == 1
    sat_call = ep.send_org_celestrak_kafka_satellite_catalog_entry.call_args
    assert sat_call.kwargs["_norad_cat_id"] == "25544"
    assert sat_call.kwargs["flush_producer"] is False

    assert ep.send_org_celestrak_kafka_orbit_mean_elements.call_count == 1
    gp_call = ep.send_org_celestrak_kafka_orbit_mean_elements.call_args
    assert gp_call.kwargs["_norad_cat_id"] == "25544"
    assert gp_call.kwargs["flush_producer"] is False

    persisted = json.loads(state_file.read_text())
    assert persisted["gp"]["25544"] == "2026-07-16T12:00:00.000000"


@pytest.mark.unit
def test_kafka_feed_gp_dedup_by_epoch_skips_unchanged(tmp_path):
    api = _mock_api()
    ep, _ = _run_feed(
        api, tmp_path,
        state={"gp": {"25544": "2026-07-16T12:00:00.000000"}, "supgp": {}},
    )
    # SATCAT reference is always re-emitted; GP is suppressed by the watermark.
    assert ep.send_org_celestrak_kafka_satellite_catalog_entry.call_count == 1
    assert ep.send_org_celestrak_kafka_orbit_mean_elements.call_count == 0


@pytest.mark.unit
def test_build_gp_preserves_verbatim_keys_and_int_norad():
    from celestrak_kafka.app import _build_gp

    obj = json.loads(_build_gp(GP_ROW).to_byte_array("application/json"))
    assert obj["NORAD_CAT_ID"] == 25544
    assert isinstance(obj["NORAD_CAT_ID"], int)
    assert obj["OBJECT_NAME"] == "ISS (ZARYA)"
    assert obj["CLASSIFICATION_TYPE"] == "U"
    assert obj["EPOCH"].startswith("2026-07-16T12:00:00")


@pytest.mark.unit
def test_build_satcat_dates_are_strings_and_nulls_pass_through():
    from celestrak_kafka.app import _build_satcat

    obj = json.loads(_build_satcat(SATCAT_ROW).to_byte_array("application/json"))
    assert obj["NORAD_CAT_ID"] == 25544
    assert obj["LAUNCH_DATE"] == "1998-11-20"
    assert obj["DECAY_DATE"] is None
    assert obj["OWNER"] == "ISS"
