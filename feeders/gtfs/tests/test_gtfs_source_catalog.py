import json

import pytest

from gtfs_core import DEFAULT_SOURCES_FILE, load_source_configs, select_entries


def test_default_catalog_loads_disabled_examples_only():
    configs = load_source_configs(selector="*")
    assert DEFAULT_SOURCES_FILE.endswith("gtfs-sources.json")
    assert [config["agency"] for config in configs] == ["mbta", "mta-nyc", "hsl", "bkk", "tfnsw", "replace-me"]
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
    assert len(load_source_configs(selector="*")) == 6


def test_hsl_helsinki_entry_is_keyless():
    configs = load_source_configs(selector="hsl-helsinki")
    assert len(configs) == 1
    entry = configs[0]
    assert entry["agency"] == "hsl"
    # 3 keyless HSL GTFS-Realtime feeds (vehicle positions, trip updates, alerts)
    assert len(entry["gtfs_rt_urls"]) == 3
    assert all(url.startswith("https://realtime.hsl.fi/realtime/") for url in entry["gtfs_rt_urls"])
    # public keyless GTFS Schedule archive
    assert entry["gtfs_urls"] == ["https://infopalvelut.storage.hsldev.com/gtfs/hsl.zip"]
    # keyless: no auth headers and no ${...} placeholder anywhere
    assert entry["gtfs_rt_headers"] is None
    assert entry["gtfs_headers"] is None
    assert all("${" not in url for url in entry["gtfs_rt_urls"])


def test_bkk_budapest_entry_interpolates_key_into_urls(monkeypatch):
    monkeypatch.setenv("BKK_API_KEY", "test-bkk-key")
    configs = load_source_configs(selector="bkk-budapest")
    assert len(configs) == 1
    entry = configs[0]
    assert entry["agency"] == "bkk"
    # 3 GTFS-Realtime feeds; the key rides as a ?key= query parameter, expanded from the env
    assert len(entry["gtfs_rt_urls"]) == 3
    assert all(
        url.startswith("https://go.bkk.hu/api/query/v1/ws/gtfs-rt/full/") for url in entry["gtfs_rt_urls"]
    )
    assert all(url.endswith("?key=test-bkk-key") for url in entry["gtfs_rt_urls"])
    # the schedule archive is keyless (no placeholder)
    assert entry["gtfs_urls"] == ["https://bkk.hu/gtfs/budapest_gtfs.zip"]
    # BKK authenticates via URL query param, not headers
    assert entry["gtfs_rt_headers"] is None
    assert entry["gtfs_headers"] is None


def test_mta_nyc_entry_exposes_all_keyless_feeds():
    configs = load_source_configs(selector="mta-nyc")
    assert len(configs) == 1
    entry = configs[0]
    assert entry["agency"] == "mta-nyc"
    # 11 keyless GTFS-Realtime feeds (NYCT subway divisions + LIRR + MNR + alerts)
    assert len(entry["gtfs_rt_urls"]) == 11
    assert all(url.startswith("https://api-endpoint.mta.info/") for url in entry["gtfs_rt_urls"])
    # 7 public GTFS Schedule archives (subway supplemented + borough buses)
    assert len(entry["gtfs_urls"]) == 7
    # keyless: no auth headers required post-2023 MTA open-data migration
    assert entry["gtfs_rt_headers"] is None
    assert entry["gtfs_headers"] is None


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
