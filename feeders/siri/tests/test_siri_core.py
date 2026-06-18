from __future__ import annotations

from pathlib import Path

import pytest

from siri_core.acquisition import DEFAULT_BODS_URL, DEFAULT_TRAFIKLAB_URL, SiriClient, iter_vehicle_positions


def test_iter_vehicle_positions_parses_sample_xml():
    client = SiriClient(provider="bods", api_key="", sample_mode=True)
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
    assert first.feedurl == DEFAULT_BODS_URL


def test_operator_filter_limits_snapshot():
    client = SiriClient(provider="bods", api_key="", operators=("ABCD",), sample_mode=True)
    snapshot = client.load_snapshot()

    assert snapshot.operators == ("ABCD",)
    assert [item.vehicle_ref for item in snapshot.vehicle_positions] == ["AB12"]


def test_iter_vehicle_positions_handles_raw_bytes():
    sample_path = Path(__file__).resolve().parents[1] / "sample_data" / "siri.xml"
    positions = list(iter_vehicle_positions(sample_path.read_bytes(), feedurl=DEFAULT_BODS_URL))

    assert {position.identity for position in positions} == {"A2BR/3312", "ABCD/AB12"}


def test_trafiklab_request_specs_expand_operator_and_data_type():
    client = SiriClient(
        provider="trafiklab",
        siri_url=DEFAULT_TRAFIKLAB_URL,
        api_key="secret",
        operators=("skane/skanetrafiken", "stockholm/sl"),
        data_types=("vm", "sx"),
    )

    specs = client._build_request_specs()

    assert [spec.request_url for spec in specs] == [
        "https://api.trafiklab.se/siri2.x/vm/skane/skanetrafiken",
        "https://api.trafiklab.se/siri2.x/sx/skane/skanetrafiken",
        "https://api.trafiklab.se/siri2.x/vm/stockholm/sl",
        "https://api.trafiklab.se/siri2.x/sx/stockholm/sl",
    ]
    assert all(spec.headers == {"X-Api-Key": "secret"} for spec in specs)
    assert all(spec.params == {} for spec in specs)


def test_custom_request_specs_attach_query_and_headers():
    client = SiriClient(provider="custom", siri_url="https://example.test/siri", api_key="secret", data_types=("vm",))

    specs = client._build_request_specs()

    assert len(specs) == 1
    assert specs[0].request_url == "https://example.test/siri"
    assert specs[0].params == {"api_key": "secret", "key": "secret"}
    assert specs[0].headers == {"X-Api-Key": "secret", "Authorization": "Bearer secret"}


def test_bods_bulk_archive_requires_no_api_key():
    # The default BODS endpoint is the public bulk archive, which is downloadable
    # without credentials. A missing key must NOT raise for this endpoint.
    client = SiriClient(provider="bods", api_key="")

    specs = client._build_request_specs()

    assert len(specs) == 1
    assert specs[0].request_url == DEFAULT_BODS_URL
    assert specs[0].is_zip is True
    assert specs[0].params == {}


def test_bods_bulk_archive_passes_api_key_when_present():
    client = SiriClient(provider="bods", api_key="secret")

    specs = client._build_request_specs()

    assert specs[0].params == {"api_key": "secret"}


def test_bods_datafeed_requires_api_key():
    # A non-bulk (filtered) datafeed URL still requires a key.
    client = SiriClient(
        provider="bods",
        siri_url="https://data.bus-data.dft.gov.uk/avl/datafeed",
        api_key="",
    )

    with pytest.raises(RuntimeError):
        client._build_request_specs()
