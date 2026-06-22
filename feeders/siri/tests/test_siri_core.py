from __future__ import annotations

import json
from pathlib import Path

import pytest

from siri_core.acquisition import DEFAULT_BODS_URL, DEFAULT_ENTUR_URL, DEFAULT_TRAFIKLAB_URL, SiriClient, iter_vehicle_positions
from siri_core.config import DEFAULT_ENTUR_CLIENT_NAME, FeedConfig, load_feed_configs, parse_request_headers, select_entries


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


def test_entur_provider_defaults_to_siri_lite_paths_and_client_header():
    config = FeedConfig.from_env(provider="entur", data_types="et,vm,sx")
    client = SiriClient(
        provider=config.provider,
        siri_url=config.siri_url,
        data_types=config.data_types,
        request_headers=config.request_headers,
    )

    specs = client._build_request_specs()

    assert config.siri_url == DEFAULT_ENTUR_URL
    assert [spec.request_url for spec in specs] == [
        "https://api.entur.io/realtime/v1/rest/et",
        "https://api.entur.io/realtime/v1/rest/vm",
        "https://api.entur.io/realtime/v1/rest/sx",
    ]
    assert all(spec.headers == {"ET-Client-Name": DEFAULT_ENTUR_CLIENT_NAME} for spec in specs)
    assert all(spec.params == {} for spec in specs)


def test_parse_request_headers_accepts_semicolon_separated_values():
    assert parse_request_headers("ET-Client-Name=my-client;X-Trace = abc=123") == {
        "ET-Client-Name": "my-client",
        "X-Trace": "abc=123",
    }


def test_custom_headers_are_sent_with_request():
    class FakeResponse:
        content = b"<Siri xmlns=\"http://www.siri.org.uk/siri\"><ServiceDelivery /></Siri>"

        def raise_for_status(self):
            return None

    class FakeSession:
        def __init__(self):
            self.headers = {}
            self.calls = []

        def get(self, url, *, headers, params, timeout):
            self.calls.append({"url": url, "headers": headers, "params": params, "timeout": timeout})
            return FakeResponse()

    session = FakeSession()
    client = SiriClient(
        provider="custom",
        siri_url="https://example.test/siri",
        request_headers={"ET-Client-Name": "unit-test", "X-Extra": "yes"},
        session=session,
    )

    client.load_snapshot()

    assert session.calls == [
        {
            "url": "https://example.test/siri",
            "headers": {"ET-Client-Name": "unit-test", "X-Extra": "yes"},
            "params": {},
            "timeout": 30.0,
        }
    ]


def test_existing_provider_headers_are_unchanged_when_no_custom_headers():
    client = SiriClient(
        provider="trafiklab",
        siri_url=DEFAULT_TRAFIKLAB_URL,
        api_key="secret",
        operators=("skane/skanetrafiken",),
        data_types=("vm",),
    )

    specs = client._build_request_specs()

    assert specs[0].headers == {"X-Api-Key": "secret"}


def test_default_catalog_loads_enabled_bods(monkeypatch):
    monkeypatch.delenv("SIRI_PROVIDER", raising=False)
    monkeypatch.delenv("SIRI_URL", raising=False)
    configs = load_feed_configs()

    assert len(configs) == 1
    assert configs[0].provider == "bods"
    assert configs[0].siri_url == DEFAULT_BODS_URL
    assert configs[0].data_types == ("vm",)


def test_select_entries_default_skips_disabled():
    entries = [{"name": "a", "enabled": True}, {"name": "b", "enabled": False}]
    assert [entry["name"] for entry in select_entries(entries)] == ["a"]


def test_selector_returns_named_entries_in_order(monkeypatch):
    monkeypatch.delenv("SIRI_PROVIDER", raising=False)
    monkeypatch.delenv("SIRI_URL", raising=False)
    configs = load_feed_configs(selector="key-protected-siri-template,uk-bods-bulk-archive")

    assert [config.provider for config in configs] == ["custom", "bods"]
    assert configs[0].siri_url == "REPLACE_WITH_SIRI_URL"
    assert configs[1].siri_url == DEFAULT_BODS_URL


def test_selector_star_includes_disabled_templates(monkeypatch):
    monkeypatch.delenv("SIRI_PROVIDER", raising=False)
    monkeypatch.delenv("SIRI_URL", raising=False)
    configs = load_feed_configs(selector="*")

    assert len(configs) == 3
    assert any(config.provider == "custom" for config in configs)


def test_unknown_selector_raises(monkeypatch):
    monkeypatch.delenv("SIRI_PROVIDER", raising=False)
    monkeypatch.delenv("SIRI_URL", raising=False)
    with pytest.raises(ValueError):
        load_feed_configs(selector="does-not-exist")


def test_legacy_siri_url_single_source_takes_precedence(monkeypatch):
    monkeypatch.setenv("SIRI_URL", "https://example.test/legacy")
    monkeypatch.setenv("SIRI_PROVIDER", "custom")
    monkeypatch.setenv("SIRI_API_KEY", "legacy-key")
    monkeypatch.setenv("SIRI_OPERATORS", "op-a,op-b")
    monkeypatch.setenv("SIRI_DATA_TYPES", "vm,et")

    configs = load_feed_configs(selector="uk-bods-bulk-archive")

    assert len(configs) == 1
    assert configs[0].provider == "custom"
    assert configs[0].siri_url == "https://example.test/legacy"
    assert configs[0].api_key == "legacy-key"
    assert configs[0].operators == ("op-a", "op-b")
    assert configs[0].data_types == ("vm", "et")


def test_legacy_non_default_provider_single_source_takes_precedence(monkeypatch):
    monkeypatch.delenv("SIRI_URL", raising=False)
    monkeypatch.setenv("SIRI_PROVIDER", "entur")

    configs = load_feed_configs()

    assert len(configs) == 1
    assert configs[0].provider == "entur"
    assert configs[0].siri_url == DEFAULT_ENTUR_URL


def test_catalog_interpolates_api_key(monkeypatch):
    monkeypatch.delenv("SIRI_PROVIDER", raising=False)
    monkeypatch.delenv("SIRI_URL", raising=False)
    monkeypatch.setenv("PRIVATE_SIRI_KEY", "secret-123")
    raw = json.dumps({
        "sources": [
            {
                "name": "private",
                "provider": "custom",
                "siri_url": "https://example.test/siri",
                "api_key": "${PRIVATE_SIRI_KEY}",
            }
        ]
    })

    configs = load_feed_configs(raw)

    assert configs[0].api_key == "secret-123"


def test_catalog_accepts_string_operators(monkeypatch):
    monkeypatch.delenv("SIRI_PROVIDER", raising=False)
    monkeypatch.delenv("SIRI_URL", raising=False)
    raw = json.dumps({
        "sources": [
            {
                "name": "regional",
                "provider": "trafiklab",
                "operators": "skane/skanetrafiken,stockholm/sl",
            }
        ]
    })

    configs = load_feed_configs(raw)

    assert configs[0].operators == ("skane/skanetrafiken", "stockholm/sl")


def test_sources_file_override(tmp_path, monkeypatch):
    monkeypatch.delenv("SIRI_PROVIDER", raising=False)
    monkeypatch.delenv("SIRI_URL", raising=False)
    catalog = tmp_path / "custom.sources.json"
    catalog.write_text(
        json.dumps({
            "sources": [
                {
                    "name": "only",
                    "provider": "entur",
                    "siri_url": "https://api.entur.io/realtime/v1/rest/{data_type}",
                    "data_types": ["vm"],
                }
            ]
        }),
        encoding="utf-8",
    )

    configs = load_feed_configs(sources_file=str(catalog))

    assert len(configs) == 1
    assert configs[0].provider == "entur"
