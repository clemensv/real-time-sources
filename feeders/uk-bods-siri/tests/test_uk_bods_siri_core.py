from __future__ import annotations

from uk_bods_siri_core.acquisition import BodsSiriClient, iter_vehicle_positions


def test_iter_vehicle_positions_parses_sample_xml():
    client = BodsSiriClient(api_key="", sample_mode=True)
    snapshot = client.load_snapshot()

    assert snapshot.operators == ("A2BR", "ABCD")
    assert len(snapshot.vehicle_positions) == 2

    first = snapshot.vehicle_positions[0]
    assert first.operator_ref == "A2BR"
    assert first.vehicle_ref == "3312"
    assert first.line_ref == "T12"
    assert first.longitude == 0.054376
    assert first.latitude == 52.29166
    assert first.bearing == 73
    assert first.item_identifier == "9e8f75df-84fb-460d-9aa0-6245bd881a15"


def test_operator_filter_limits_snapshot():
    client = BodsSiriClient(api_key="", operators={"ABCD"}, sample_mode=True)
    snapshot = client.load_snapshot()

    assert snapshot.operators == ("ABCD",)
    assert [item.vehicle_ref for item in snapshot.vehicle_positions] == ["AB12"]


def test_iter_vehicle_positions_handles_raw_bytes():
    xml_bytes = (BodsSiriClient(api_key="", sample_mode=True)._load_xml_bytes())
    positions = list(iter_vehicle_positions(xml_bytes))

    assert {position.identity for position in positions} == {"A2BR/3312", "ABCD/AB12"}
