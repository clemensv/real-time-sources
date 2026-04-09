"""
Unit tests for EAWS ALBINA Avalanche Bulletin poller.
Tests core functionality without external dependencies.
"""

import pytest
import json
import os
import datetime
from unittest.mock import Mock, patch, MagicMock
from eaws_albina.eaws_albina import (
    AlbinaPoller,
    parse_connection_string,
    DANGER_RATING_MAP,
    DEFAULT_REGIONS,
    BASE_URL,
)


SAMPLE_BULLETIN = {
    "bulletins": [
        {
            "publicationTime": "2026-04-08T15:00:00Z",
            "validTime": {
                "startTime": "2026-04-08T15:00:00Z",
                "endTime": "2026-04-09T15:00:00Z",
            },
            "bulletinID": "6b548ab7-da3e-406a-bcab-087393335eca",
            "lang": "en",
            "dangerRatings": [
                {
                    "mainValue": "low",
                    "elevation": {"upperBound": "2400"},
                    "validTimePeriod": "earlier",
                },
                {
                    "mainValue": "moderate",
                    "elevation": {"lowerBound": "2400"},
                    "validTimePeriod": "earlier",
                },
                {
                    "mainValue": "considerable",
                    "elevation": {"upperBound": "2800"},
                    "validTimePeriod": "later",
                },
            ],
            "avalancheProblems": [
                {
                    "problemType": "persistent_weak_layers",
                    "elevation": {"lowerBound": "2400"},
                    "validTimePeriod": "earlier",
                    "snowpackStability": "poor",
                    "frequency": "few",
                    "avalancheSize": 3,
                    "aspects": ["N", "NW", "W", "NE", "E"],
                },
                {
                    "problemType": "wet_snow",
                    "elevation": {"upperBound": "2400"},
                    "validTimePeriod": "earlier",
                    "snowpackStability": "fair",
                    "frequency": "few",
                    "avalancheSize": 2,
                    "aspects": ["N", "NW", "W", "NE", "E", "SE", "S", "SW"],
                },
            ],
            "regions": [
                {"name": "Karwendel Mountains East", "regionID": "AT-07-04-02"},
            ],
            "tendency": [
                {
                    "highlights": "Danger will increase during the day.",
                    "tendencyType": "steady",
                    "validTime": {
                        "startTime": "2026-04-09T15:00:00Z",
                        "endTime": "2026-04-10T15:00:00Z",
                    },
                }
            ],
            "customData": {
                "ALBINA": {"mainDate": "2026-04-09"},
                "LWD_Tyrol": {"dangerPatterns": ["DP10", "DP1"]},
            },
            "avalancheActivity": {
                "highlights": "The danger of wet avalanches will already increase in the late morning.",
                "comment": "Detailed avalanche activity comment.",
            },
            "snowpackStructure": {
                "comment": "The surface of the snowpack has frozen to form a strong crust."
            },
        }
    ]
}

SAMPLE_MULTI_REGION = {
    "bulletins": [
        {
            "publicationTime": "2026-04-08T15:00:00Z",
            "validTime": {
                "startTime": "2026-04-08T15:00:00Z",
                "endTime": "2026-04-09T15:00:00Z",
            },
            "bulletinID": "multi-region-bulletin",
            "lang": "en",
            "dangerRatings": [
                {"mainValue": "high", "validTimePeriod": "all_day"},
            ],
            "avalancheProblems": [],
            "regions": [
                {"name": "Region A", "regionID": "AT-07-01"},
                {"name": "Region B", "regionID": "AT-07-02"},
                {"name": "Region C", "regionID": "AT-07-03"},
            ],
            "tendency": [{"tendencyType": "increasing"}],
            "customData": {},
            "avalancheActivity": {"highlights": "High danger everywhere."},
            "snowpackStructure": {"comment": "Unstable snowpack."},
        }
    ]
}


@pytest.fixture
def mock_kafka_config():
    return {"bootstrap.servers": "localhost:9092"}


@pytest.fixture
def temp_state_file(tmp_path):
    return str(tmp_path / "albina_state.json")


def _make_poller(mock_kafka_config, temp_state_file, regions=None, lang="en"):
    """Create an AlbinaPoller with a mocked Kafka producer."""
    with patch("confluent_kafka.Producer") as mock_producer_class:
        mock_producer_class.return_value = MagicMock()
        poller = AlbinaPoller(
            kafka_config=mock_kafka_config,
            kafka_topic="test-topic",
            last_polled_file=temp_state_file,
            regions=regions,
            lang=lang,
        )
    return poller


@pytest.mark.unit
class TestAlbinaPollerInit:
    def test_default_regions(self, mock_kafka_config, temp_state_file):
        poller = _make_poller(mock_kafka_config, temp_state_file)
        assert poller.regions == DEFAULT_REGIONS
        assert poller.lang == "en"
        assert poller.kafka_topic == "test-topic"

    def test_custom_regions(self, mock_kafka_config, temp_state_file):
        poller = _make_poller(mock_kafka_config, temp_state_file, regions=["AT-07"])
        assert poller.regions == ["AT-07"]

    def test_custom_lang(self, mock_kafka_config, temp_state_file):
        poller = _make_poller(mock_kafka_config, temp_state_file, lang="de")
        assert poller.lang == "de"


@pytest.mark.unit
class TestStateManagement:
    def test_load_state_empty(self, mock_kafka_config, temp_state_file):
        poller = _make_poller(mock_kafka_config, temp_state_file)
        state = poller.load_state()
        assert state == {"seen_keys": []}

    def test_load_state_existing(self, mock_kafka_config, temp_state_file):
        state_data = {"seen_keys": ["AT-07-01:2026-04-08T15:00:00+00:00"]}
        with open(temp_state_file, "w", encoding="utf-8") as f:
            json.dump(state_data, f)
        poller = _make_poller(mock_kafka_config, temp_state_file)
        state = poller.load_state()
        assert len(state["seen_keys"]) == 1

    def test_save_state(self, mock_kafka_config, temp_state_file):
        poller = _make_poller(mock_kafka_config, temp_state_file)
        poller.save_state({"seen_keys": ["key1", "key2"]})
        with open(temp_state_file, "r", encoding="utf-8") as f:
            saved = json.load(f)
        assert saved["seen_keys"] == ["key1", "key2"]

    def test_load_state_nonexistent_file(self, mock_kafka_config, tmp_path):
        path = str(tmp_path / "nonexistent" / "state.json")
        poller = _make_poller(mock_kafka_config, path)
        state = poller.load_state()
        assert state == {"seen_keys": []}


@pytest.mark.unit
class TestBuildUrl:
    def test_build_url_tirol(self):
        url = AlbinaPoller.build_url("2026-04-09", "AT-07", "en")
        assert url == f"{BASE_URL}/2026-04-09/2026-04-09_AT-07_en_CAAMLv6.json"

    def test_build_url_south_tyrol(self):
        url = AlbinaPoller.build_url("2026-04-09", "IT-32-BZ", "de")
        assert url == f"{BASE_URL}/2026-04-09/2026-04-09_IT-32-BZ_de_CAAMLv6.json"

    def test_build_url_italian(self):
        url = AlbinaPoller.build_url("2026-03-15", "IT-32-TN", "it")
        assert url == f"{BASE_URL}/2026-03-15/2026-03-15_IT-32-TN_it_CAAMLv6.json"


@pytest.mark.unit
class TestComputeMaxDanger:
    def test_single_rating(self):
        ratings = [{"mainValue": "moderate", "validTimePeriod": "all_day"}]
        name, val = AlbinaPoller.compute_max_danger(ratings)
        assert name == "moderate"
        assert val == 2

    def test_multiple_ratings(self):
        ratings = [
            {"mainValue": "low", "validTimePeriod": "earlier"},
            {"mainValue": "considerable", "validTimePeriod": "later"},
            {"mainValue": "moderate", "validTimePeriod": "earlier"},
        ]
        name, val = AlbinaPoller.compute_max_danger(ratings)
        assert name == "considerable"
        assert val == 3

    def test_empty_ratings(self):
        name, val = AlbinaPoller.compute_max_danger([])
        assert name is None
        assert val is None

    def test_very_high(self):
        ratings = [{"mainValue": "very_high"}]
        name, val = AlbinaPoller.compute_max_danger(ratings)
        assert name == "very_high"
        assert val == 5

    def test_high_rating(self):
        ratings = [{"mainValue": "high"}, {"mainValue": "low"}]
        name, val = AlbinaPoller.compute_max_danger(ratings)
        assert name == "high"
        assert val == 4

    def test_unknown_rating_ignored(self):
        ratings = [{"mainValue": "unknown_value"}, {"mainValue": "low"}]
        name, val = AlbinaPoller.compute_max_danger(ratings)
        assert name == "low"
        assert val == 1


@pytest.mark.unit
class TestParseBulletins:
    def test_parse_single_bulletin(self):
        events = AlbinaPoller.parse_bulletins(SAMPLE_BULLETIN, "en")
        assert len(events) == 1
        e = events[0]
        assert e.region_id == "AT-07-04-02"
        assert e.region_name == "Karwendel Mountains East"
        assert e.bulletin_id == "6b548ab7-da3e-406a-bcab-087393335eca"
        assert e.lang == "en"
        assert e.max_danger_rating is not None
        assert e.max_danger_rating.value == "considerable"
        assert e.max_danger_rating_value == 3
        assert e.tendency_type == "steady"
        assert e.avalanche_activity_highlights is not None
        assert "wet avalanches" in e.avalanche_activity_highlights
        assert e.snowpack_structure_comment is not None
        assert "crust" in e.snowpack_structure_comment

    def test_parse_danger_patterns(self):
        events = AlbinaPoller.parse_bulletins(SAMPLE_BULLETIN, "en")
        e = events[0]
        assert e.danger_patterns_json is not None
        patterns = json.loads(e.danger_patterns_json)
        assert "DP10" in patterns
        assert "DP1" in patterns

    def test_parse_danger_ratings_json(self):
        events = AlbinaPoller.parse_bulletins(SAMPLE_BULLETIN, "en")
        e = events[0]
        ratings = json.loads(e.danger_ratings_json)
        assert len(ratings) == 3
        assert ratings[0]["mainValue"] == "low"

    def test_parse_avalanche_problems_json(self):
        events = AlbinaPoller.parse_bulletins(SAMPLE_BULLETIN, "en")
        e = events[0]
        problems = json.loads(e.avalanche_problems_json)
        assert len(problems) == 2
        assert problems[0]["problemType"] == "persistent_weak_layers"
        assert problems[1]["problemType"] == "wet_snow"

    def test_parse_multi_region(self):
        events = AlbinaPoller.parse_bulletins(SAMPLE_MULTI_REGION, "en")
        assert len(events) == 3
        region_ids = [e.region_id for e in events]
        assert "AT-07-01" in region_ids
        assert "AT-07-02" in region_ids
        assert "AT-07-03" in region_ids
        for e in events:
            assert e.bulletin_id == "multi-region-bulletin"
            assert e.max_danger_rating.value == "high"
            assert e.max_danger_rating_value == 4

    def test_parse_empty_bulletins(self):
        events = AlbinaPoller.parse_bulletins({"bulletins": []}, "en")
        assert events == []

    def test_parse_no_bulletins_key(self):
        events = AlbinaPoller.parse_bulletins({}, "en")
        assert events == []

    def test_parse_missing_publication_time(self):
        data = {
            "bulletins": [
                {
                    "validTime": {"startTime": "2026-04-08T15:00:00Z", "endTime": "2026-04-09T15:00:00Z"},
                    "bulletinID": "test",
                    "dangerRatings": [],
                    "avalancheProblems": [],
                    "regions": [{"regionID": "AT-07-01", "name": "Test"}],
                }
            ]
        }
        events = AlbinaPoller.parse_bulletins(data, "en")
        assert events == []

    def test_parse_no_tendency(self):
        data = {
            "bulletins": [
                {
                    "publicationTime": "2026-04-08T15:00:00Z",
                    "validTime": {"startTime": "2026-04-08T15:00:00Z", "endTime": "2026-04-09T15:00:00Z"},
                    "bulletinID": "test",
                    "dangerRatings": [{"mainValue": "low"}],
                    "avalancheProblems": [],
                    "regions": [{"regionID": "AT-07-01", "name": "Test Region"}],
                    "customData": {},
                }
            ]
        }
        events = AlbinaPoller.parse_bulletins(data, "en")
        assert len(events) == 1
        assert events[0].tendency_type is None
        assert events[0].danger_patterns_json is None
        assert events[0].avalanche_activity_highlights is None
        assert events[0].snowpack_structure_comment is None

    def test_parse_no_danger_patterns(self):
        data = {
            "bulletins": [
                {
                    "publicationTime": "2026-04-08T15:00:00Z",
                    "validTime": {"startTime": "2026-04-08T15:00:00Z", "endTime": "2026-04-09T15:00:00Z"},
                    "bulletinID": "test-no-patterns",
                    "dangerRatings": [{"mainValue": "moderate"}],
                    "avalancheProblems": [],
                    "regions": [{"regionID": "IT-32-BZ-01", "name": "Rieserferner Group"}],
                    "customData": {"ALBINA": {"mainDate": "2026-04-09"}},
                }
            ]
        }
        events = AlbinaPoller.parse_bulletins(data, "en")
        assert len(events) == 1
        assert events[0].danger_patterns_json is None

    def test_parse_empty_regions_skipped(self):
        data = {
            "bulletins": [
                {
                    "publicationTime": "2026-04-08T15:00:00Z",
                    "validTime": {"startTime": "2026-04-08T15:00:00Z", "endTime": "2026-04-09T15:00:00Z"},
                    "bulletinID": "test-empty-region",
                    "dangerRatings": [],
                    "avalancheProblems": [],
                    "regions": [{"regionID": "", "name": ""}],
                }
            ]
        }
        events = AlbinaPoller.parse_bulletins(data, "en")
        assert events == []

    def test_publication_time_parsed_as_datetime(self):
        events = AlbinaPoller.parse_bulletins(SAMPLE_BULLETIN, "en")
        e = events[0]
        assert isinstance(e.publication_time, datetime.datetime)
        assert isinstance(e.valid_time_start, datetime.datetime)
        assert isinstance(e.valid_time_end, datetime.datetime)


@pytest.mark.unit
class TestFetchBulletin:
    @patch("eaws_albina.eaws_albina.requests.get")
    def test_fetch_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = SAMPLE_BULLETIN
        mock_get.return_value = mock_response
        result = AlbinaPoller.fetch_bulletin("https://example.com/test.json")
        assert result is not None
        assert "bulletins" in result

    @patch("eaws_albina.eaws_albina.requests.get")
    def test_fetch_404(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        result = AlbinaPoller.fetch_bulletin("https://example.com/test.json")
        assert result is None

    @patch("eaws_albina.eaws_albina.requests.get")
    def test_fetch_network_error(self, mock_get):
        mock_get.side_effect = Exception("Connection timeout")
        result = AlbinaPoller.fetch_bulletin("https://example.com/test.json")
        assert result is None

    @patch("eaws_albina.eaws_albina.requests.get")
    def test_fetch_server_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = Exception("500 Server Error")
        mock_get.return_value = mock_response
        result = AlbinaPoller.fetch_bulletin("https://example.com/test.json")
        assert result is None


@pytest.mark.unit
class TestFetchAndSend:
    @patch("eaws_albina.eaws_albina.requests.get")
    def test_fetch_and_send_new_events(self, mock_get, mock_kafka_config, temp_state_file):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = SAMPLE_BULLETIN
        mock_get.return_value = mock_response
        poller = _make_poller(mock_kafka_config, temp_state_file, regions=["AT-07"])
        count = poller.fetch_and_send("2026-04-09")
        assert count == 1

    @patch("eaws_albina.eaws_albina.requests.get")
    def test_fetch_and_send_dedup(self, mock_get, mock_kafka_config, temp_state_file):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = SAMPLE_BULLETIN
        mock_get.return_value = mock_response
        poller = _make_poller(mock_kafka_config, temp_state_file, regions=["AT-07"])
        count1 = poller.fetch_and_send("2026-04-09")
        count2 = poller.fetch_and_send("2026-04-09")
        assert count1 == 1
        assert count2 == 0

    @patch("eaws_albina.eaws_albina.requests.get")
    def test_fetch_and_send_404(self, mock_get, mock_kafka_config, temp_state_file):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        poller = _make_poller(mock_kafka_config, temp_state_file, regions=["AT-07"])
        count = poller.fetch_and_send("2026-08-15")
        assert count == 0

    @patch("eaws_albina.eaws_albina.requests.get")
    def test_fetch_and_send_multi_region(self, mock_get, mock_kafka_config, temp_state_file):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = SAMPLE_MULTI_REGION
        mock_get.return_value = mock_response
        poller = _make_poller(mock_kafka_config, temp_state_file, regions=["AT-07"])
        count = poller.fetch_and_send("2026-04-09")
        assert count == 3


@pytest.mark.unit
class TestParseConnectionString:
    def test_parse_valid_event_hubs(self):
        conn_str = "Endpoint=sb://mynamespace.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=abc123;EntityPath=myhub"
        result = parse_connection_string(conn_str)
        assert result["bootstrap.servers"] == "mynamespace.servicebus.windows.net:9093"
        assert result["kafka_topic"] == "myhub"
        assert result["sasl.username"] == "$ConnectionString"
        assert result["sasl.password"] == conn_str

    def test_parse_connection_string_without_entity_path(self):
        conn_str = "Endpoint=sb://mynamespace.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=abc123"
        result = parse_connection_string(conn_str)
        assert result["bootstrap.servers"] == "mynamespace.servicebus.windows.net:9093"
        assert "kafka_topic" not in result

    def test_parse_bootstrap_server(self):
        conn_str = "BootstrapServer=localhost:9092;EntityPath=my-topic"
        result = parse_connection_string(conn_str)
        assert result["bootstrap.servers"] == "localhost:9092"
        assert result["kafka_topic"] == "my-topic"

    def test_parse_password_is_full_string(self):
        conn_str = "Endpoint=sb://test.servicebus.windows.net/;SharedAccessKeyName=test;SharedAccessKey=key;EntityPath=hub"
        result = parse_connection_string(conn_str)
        assert result["sasl.password"] == conn_str


@pytest.mark.unit
class TestDangerRatingMap:
    def test_all_ratings_present(self):
        assert DANGER_RATING_MAP["low"] == 1
        assert DANGER_RATING_MAP["moderate"] == 2
        assert DANGER_RATING_MAP["considerable"] == 3
        assert DANGER_RATING_MAP["high"] == 4
        assert DANGER_RATING_MAP["very_high"] == 5

    def test_map_has_five_entries(self):
        assert len(DANGER_RATING_MAP) == 5


@pytest.mark.unit
class TestDataclasses:
    def test_create_avalanche_bulletin(self):
        from eaws_albina_producer_data import AvalancheBulletin, MaxDangerRatingenum

        event = AvalancheBulletin(
            region_id="AT-07-04-02",
            region_name="Karwendel Mountains East",
            bulletin_id="test-id",
            publication_time=datetime.datetime(2026, 4, 8, 15, 0, 0, tzinfo=datetime.timezone.utc),
            valid_time_start=datetime.datetime(2026, 4, 8, 15, 0, 0, tzinfo=datetime.timezone.utc),
            valid_time_end=datetime.datetime(2026, 4, 9, 15, 0, 0, tzinfo=datetime.timezone.utc),
            lang="en",
            max_danger_rating=MaxDangerRatingenum.considerable,
            max_danger_rating_value=3,
            danger_ratings_json="[]",
            avalanche_problems_json="[]",
            tendency_type="steady",
            danger_patterns_json='["DP10"]',
            avalanche_activity_highlights="Test highlights",
            snowpack_structure_comment="Test comment",
        )
        assert event.region_id == "AT-07-04-02"
        assert event.max_danger_rating == MaxDangerRatingenum.considerable
        assert event.max_danger_rating_value == 3

    def test_create_with_none_optional_fields(self):
        from eaws_albina_producer_data import AvalancheBulletin

        event = AvalancheBulletin(
            region_id="IT-32-BZ-01",
            region_name="Test Region",
            bulletin_id="test-id-2",
            publication_time=datetime.datetime(2026, 4, 8, 15, 0, 0, tzinfo=datetime.timezone.utc),
            valid_time_start=datetime.datetime(2026, 4, 8, 15, 0, 0, tzinfo=datetime.timezone.utc),
            valid_time_end=datetime.datetime(2026, 4, 9, 15, 0, 0, tzinfo=datetime.timezone.utc),
            lang="de",
            max_danger_rating=None,
            max_danger_rating_value=None,
            danger_ratings_json="[]",
            avalanche_problems_json="[]",
            tendency_type=None,
            danger_patterns_json=None,
            avalanche_activity_highlights=None,
            snowpack_structure_comment=None,
        )
        assert event.max_danger_rating is None
        assert event.max_danger_rating_value is None
        assert event.tendency_type is None
        assert event.danger_patterns_json is None

    def test_max_danger_rating_enum(self):
        from eaws_albina_producer_data import MaxDangerRatingenum

        assert MaxDangerRatingenum.low.value == "low"
        assert MaxDangerRatingenum.moderate.value == "moderate"
        assert MaxDangerRatingenum.considerable.value == "considerable"
        assert MaxDangerRatingenum.high.value == "high"
        assert MaxDangerRatingenum.very_high.value == "very_high"

    def test_bulletin_to_serializer_dict(self):
        from eaws_albina_producer_data import AvalancheBulletin, MaxDangerRatingenum

        event = AvalancheBulletin(
            region_id="AT-07-01",
            region_name="Test",
            bulletin_id="dict-test",
            publication_time=datetime.datetime(2026, 4, 8, 15, 0, 0, tzinfo=datetime.timezone.utc),
            valid_time_start=datetime.datetime(2026, 4, 8, 15, 0, 0, tzinfo=datetime.timezone.utc),
            valid_time_end=datetime.datetime(2026, 4, 9, 15, 0, 0, tzinfo=datetime.timezone.utc),
            lang="en",
            max_danger_rating=MaxDangerRatingenum.low,
            max_danger_rating_value=1,
            danger_ratings_json='[{"mainValue":"low"}]',
            avalanche_problems_json="[]",
            tendency_type=None,
            danger_patterns_json=None,
            avalanche_activity_highlights=None,
            snowpack_structure_comment=None,
        )
        d = event.to_serializer_dict()
        assert d["region_id"] == "AT-07-01"
        assert d["max_danger_rating"] == "low"
