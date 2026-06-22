import json

import pytest

from gtfs_core import DEFAULT_SOURCES_FILE, load_source_configs, select_entries


def test_default_catalog_loads_disabled_examples_only():
    configs = load_source_configs(selector="*")
    assert DEFAULT_SOURCES_FILE.endswith("gtfs-sources.json")
    assert [config["agency"] for config in configs] == ["mbta", "tfnsw", "replace-me"]
    assert configs[0]["gtfs_rt_urls"] == [
        "https://cdn.mbta.com/realtime/TripUpdates.pb",
        "https://cdn.mbta.com/realtime/VehiclePositions.pb",
        "https://cdn.mbta.com/realtime/Alerts.pb",
    ]


def test_default_selector_honors_enabled_flag():
    assert load_source_configs() == []


def test_selector_returns_named_entries_in_requested_order():
    configs = load_source_configs(selector="keyed-operator-template,mbta-boston")
    assert [config["agency"] for config in configs] == ["replace-me", "mbta"]


def test_selector_star_includes_disabled_templates():
    assert len(load_source_configs(selector="*")) == 3


def test_unknown_selector_raises():
    with pytest.raises(ValueError, match="Unknown GTFS_SOURCES entries"):
        load_source_configs(selector="does-not-exist")


def test_select_entries_default_skips_disabled():
    entries = [{"name": "enabled", "enabled": True}, {"name": "disabled", "enabled": False}]
    assert [entry["name"] for entry in select_entries(entries)] == ["enabled"]


def test_sources_file_override_via_tmp_path(tmp_path):
    catalog = tmp_path / "custom.sources.json"
    catalog.write_text(
        json.dumps(
            {
                "sources": [
                    {
                        "name": "custom",
                        "enabled": True,
                        "description": "Custom test feed",
                        "agency": "custom-agency",
                        "gtfs_rt_urls": ["https://example.invalid/custom.pb"],
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    configs = load_source_configs(sources_file=str(catalog))
    assert configs == [
        {
            "agency": "custom-agency",
            "gtfs_rt_urls": ["https://example.invalid/custom.pb"],
            "gtfs_rt_headers": None,
            "gtfs_headers": None,
            "route": "*",
        }
    ]


def test_env_interpolation_for_header_values(monkeypatch, tmp_path):
    monkeypatch.setenv("SOME_GTFS_KEY", "secret-123")
    catalog = tmp_path / "headers.sources.json"
    catalog.write_text(
        json.dumps(
            {
                "sources": [
                    {
                        "name": "keyed",
                        "enabled": True,
                        "agency": "keyed",
                        "gtfs_rt_urls": ["https://example.invalid/realtime.pb"],
                        "gtfs_rt_headers": {"Authorization": "Bearer ${SOME_GTFS_KEY}"},
                        "gtfs_headers": [["x-api-key", "${SOME_GTFS_KEY}"]],
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    configs = load_source_configs(sources_file=str(catalog))
    assert configs[0]["gtfs_rt_headers"] == [["Authorization", "Bearer secret-123"]]
    assert configs[0]["gtfs_headers"] == [["x-api-key", "secret-123"]]


def test_legacy_gtfs_rt_urls_single_feed_takes_precedence(tmp_path):
    catalog = tmp_path / "ignored.sources.json"
    catalog.write_text(
        json.dumps(
            {
                "sources": [
                    {
                        "name": "catalog",
                        "enabled": True,
                        "agency": "catalog-agency",
                        "gtfs_rt_urls": ["https://example.invalid/catalog.pb"],
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    configs = load_source_configs(
        gtfs_rt_urls=["https://example.invalid/legacy.pb"],
        agency="legacy-agency",
        gtfs_rt_headers=["Authorization=Bearer legacy"],
        sources_file=str(catalog),
    )
    assert configs == [
        {
            "gtfs_rt_urls": ["https://example.invalid/legacy.pb"],
            "gtfs_urls": None,
            "mdb_source_id": None,
            "agency": "legacy-agency",
            "route": "*",
            "gtfs_rt_headers": [["Authorization", "Bearer legacy"]],
            "gtfs_headers": None,
        }
    ]


def test_legacy_mdb_source_id_single_feed_takes_precedence():
    configs = load_source_configs(mdb_source_id="mdb-123", agency="mdb-agency", route="A")
    assert configs == [
        {
            "gtfs_rt_urls": None,
            "gtfs_urls": None,
            "mdb_source_id": "mdb-123",
            "agency": "mdb-agency",
            "route": "A",
            "gtfs_rt_headers": None,
            "gtfs_headers": None,
        }
    ]


def test_catalog_metadata_keys_are_stripped():
    configs = load_source_configs(selector="mbta-boston")
    assert "name" not in configs[0]
    assert "enabled" not in configs[0]
    assert "description" not in configs[0]
