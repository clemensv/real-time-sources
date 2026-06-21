from __future__ import annotations

from pathlib import Path

from erddap_core import ErddapClient, parse_sources


def test_parse_default_sources():
    sources = parse_sources(None)
    assert sources[0].erddap_id == "ioos-sensors"
    assert sources[0].dataset_id == "org_cormp_sun2"
    assert "sea_water_temperature" in sources[0].variables


def test_mock_snapshot_emits_reference_and_telemetry():
    source = parse_sources(None)[0]
    fixture = Path(__file__).resolve().parents[1] / "fixtures" / "mock_erddap.json"
    snap = ErddapClient(str(fixture)).fetch_dataset(source, {}, mock=True)
    assert snap.dataset["dataset_id"] == "org_cormp_sun2"
    assert snap.station["station_id"] == "org_cormp_sun2"
    assert len(snap.observations) == 2
    assert "sea_water_temperature" in snap.observations[0]["measurements"]
    assert snap.state_updates
