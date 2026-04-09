"""Unit tests for the ENTSO-E bridge."""

import json
import os
import tempfile
from datetime import datetime, timedelta, timezone
from unittest.mock import Mock, patch, MagicMock

import pytest

from entsoe.xml_parser import parse_entsoe_xml, build_api_url, TimeSeriesPoint, _parse_duration, _process_type_for_document
from entsoe.delta_state import load_state, save_state, get_last_polled, set_last_polled
from entsoe.entsoe import parse_connection_string, EntsoePoller


def _utc_hour(dt: datetime) -> datetime:
  return dt.astimezone(timezone.utc).replace(minute=0, second=0, microsecond=0)


def _iso8601_z(dt: datetime) -> str:
  return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")


def _period_param(dt: datetime) -> str:
  return dt.astimezone(timezone.utc).strftime("%Y%m%d%H%M")


FIXTURE_NOW = _utc_hour(datetime.now(timezone.utc))
GL_START = FIXTURE_NOW - timedelta(hours=12)
GL_END = GL_START + timedelta(hours=1)
PRICE_START = FIXTURE_NOW - timedelta(hours=36)
PRICE_END = PRICE_START + timedelta(days=1)
LOAD_START = FIXTURE_NOW - timedelta(hours=18)
LOAD_END = LOAD_START + timedelta(hours=1)
WIND_SOLAR_START = FIXTURE_NOW - timedelta(hours=10)
WIND_SOLAR_END = WIND_SOLAR_START + timedelta(hours=1)
CROSS_BORDER_START = FIXTURE_NOW - timedelta(hours=8)
CROSS_BORDER_END = CROSS_BORDER_START + timedelta(hours=1)
GENERATION_FORECAST_START = FIXTURE_NOW - timedelta(hours=6)
GENERATION_FORECAST_END = GENERATION_FORECAST_START + timedelta(hours=2)
STATE_TS = FIXTURE_NOW - timedelta(hours=1)


# ===== Sample XML fixtures =====

SAMPLE_GL_XML = f"""<?xml version="1.0" encoding="UTF-8"?>
<GL_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0">
  <mRID>abc123</mRID>
  <type>A75</type>
  <TimeSeries>
    <mRID>ts1</mRID>
    <businessType>A01</businessType>
    <inBiddingZone_Domain.mRID>10YDE-AT-LU---Q</inBiddingZone_Domain.mRID>
    <quantity_Measure_Unit.name>MAW</quantity_Measure_Unit.name>
    <MktPSRType>
      <psrType>B01</psrType>
    </MktPSRType>
    <Period>
      <timeInterval>
        <start>{_iso8601_z(GL_START)}</start>
        <end>{_iso8601_z(GL_END)}</end>
      </timeInterval>
      <resolution>PT15M</resolution>
      <Point>
        <position>1</position>
        <quantity>120.5</quantity>
      </Point>
      <Point>
        <position>2</position>
        <quantity>125.3</quantity>
      </Point>
      <Point>
        <position>3</position>
        <quantity>130.0</quantity>
      </Point>
      <Point>
        <position>4</position>
        <quantity>128.7</quantity>
      </Point>
    </Period>
  </TimeSeries>
  <TimeSeries>
    <mRID>ts2</mRID>
    <businessType>A01</businessType>
    <inBiddingZone_Domain.mRID>10YDE-AT-LU---Q</inBiddingZone_Domain.mRID>
    <quantity_Measure_Unit.name>MAW</quantity_Measure_Unit.name>
    <MktPSRType>
      <psrType>B02</psrType>
    </MktPSRType>
    <Period>
      <timeInterval>
        <start>{_iso8601_z(GL_START)}</start>
        <end>{_iso8601_z(GL_END)}</end>
      </timeInterval>
      <resolution>PT15M</resolution>
      <Point>
        <position>1</position>
        <quantity>500.0</quantity>
      </Point>
      <Point>
        <position>2</position>
        <quantity>510.0</quantity>
      </Point>
    </Period>
  </TimeSeries>
</GL_MarketDocument>"""

SAMPLE_PRICE_XML = f"""<?xml version="1.0" encoding="UTF-8"?>
<Publication_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-3:publicationdocument:7:3">
  <mRID>price123</mRID>
  <type>A44</type>
  <TimeSeries>
    <mRID>ts_price1</mRID>
    <businessType>A62</businessType>
    <in_Domain.mRID>10YFR-RTE------C</in_Domain.mRID>
    <currency_Unit.name>EUR</currency_Unit.name>
    <price_Measure_Unit.name>MWH</price_Measure_Unit.name>
    <Period>
      <timeInterval>
        <start>{_iso8601_z(PRICE_START)}</start>
        <end>{_iso8601_z(PRICE_END)}</end>
      </timeInterval>
      <resolution>PT60M</resolution>
      <Point>
        <position>1</position>
        <price.amount>45.67</price.amount>
      </Point>
      <Point>
        <position>2</position>
        <price.amount>42.10</price.amount>
      </Point>
      <Point>
        <position>3</position>
        <price.amount>38.50</price.amount>
      </Point>
    </Period>
  </TimeSeries>
</Publication_MarketDocument>"""

SAMPLE_LOAD_XML = f"""<?xml version="1.0" encoding="UTF-8"?>
<GL_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0">
  <mRID>load123</mRID>
  <type>A65</type>
  <TimeSeries>
    <mRID>ts_load1</mRID>
    <businessType>A04</businessType>
    <inBiddingZone_Domain.mRID>10YES-REE------0</inBiddingZone_Domain.mRID>
    <outBiddingZone_Domain.mRID>10YES-REE------0</outBiddingZone_Domain.mRID>
    <quantity_Measure_Unit.name>MAW</quantity_Measure_Unit.name>
    <Period>
      <timeInterval>
        <start>{_iso8601_z(LOAD_START)}</start>
        <end>{_iso8601_z(LOAD_END)}</end>
      </timeInterval>
      <resolution>PT15M</resolution>
      <Point>
        <position>1</position>
        <quantity>25000.0</quantity>
      </Point>
      <Point>
        <position>2</position>
        <quantity>25500.0</quantity>
      </Point>
    </Period>
  </TimeSeries>
</GL_MarketDocument>"""


# ===== XML Parser Tests =====

@pytest.mark.unit
class TestXmlParser:
    """Tests for the ENTSO-E XML parser."""

    def test_parse_generation_xml(self):
        """Parse A75 generation per type XML."""
        points = parse_entsoe_xml(SAMPLE_GL_XML, "A75")
        assert len(points) == 6  # 4 from B01 + 2 from B02

        # First point: B01, position 1
        p = points[0]
        assert p.in_domain == "10YDE-AT-LU---Q"
        assert p.psr_type == "B01"
        assert p.quantity == 120.5
        assert p.resolution == "PT15M"
        assert p.document_type == "A75"
        assert p.unit_name == "MAW"
        assert p.business_type == "A01"
        assert p.timestamp == GL_START

    def test_timestamp_computation(self):
        """Verify that timestamps are computed correctly from position and resolution."""
        points = parse_entsoe_xml(SAMPLE_GL_XML, "A75")
        assert points[0].timestamp == GL_START
        assert points[1].timestamp == GL_START + timedelta(minutes=15)
        assert points[2].timestamp == GL_START + timedelta(minutes=30)
        assert points[3].timestamp == GL_START + timedelta(minutes=45)

    def test_parse_price_xml(self):
        """Parse A44 day-ahead prices XML."""
        points = parse_entsoe_xml(SAMPLE_PRICE_XML, "A44")
        assert len(points) == 3

        p = points[0]
        assert p.in_domain == "10YFR-RTE------C"
        assert p.price == 45.67
        assert p.currency == "EUR"
        assert p.unit_name == "MWH"
        assert p.resolution == "PT60M"
        assert p.document_type == "A44"

    def test_price_timestamps_hourly(self):
        """Verify hourly timestamps for price data."""
        points = parse_entsoe_xml(SAMPLE_PRICE_XML, "A44")
        assert points[0].timestamp == PRICE_START
        assert points[1].timestamp == PRICE_START + timedelta(hours=1)
        assert points[2].timestamp == PRICE_START + timedelta(hours=2)

    def test_parse_load_xml(self):
        """Parse A65 actual total load XML."""
        points = parse_entsoe_xml(SAMPLE_LOAD_XML, "A65")
        assert len(points) == 2

        p = points[0]
        assert p.in_domain == "10YES-REE------0"
        assert p.out_domain == "10YES-REE------0"
        assert p.quantity == 25000.0
        assert p.document_type == "A65"

    def test_load_timestamps(self):
        """Verify timestamps for load data starting at offset."""
        points = parse_entsoe_xml(SAMPLE_LOAD_XML, "A65")
        assert points[0].timestamp == LOAD_START
        assert points[1].timestamp == LOAD_START + timedelta(minutes=15)

    def test_multiple_psr_types(self):
        """Verify that multiple time series with different PSR types are parsed."""
        points = parse_entsoe_xml(SAMPLE_GL_XML, "A75")
        psr_types = set(p.psr_type for p in points)
        assert psr_types == {"B01", "B02"}

    def test_parse_duration(self):
        """Test ISO 8601 duration parsing."""
        assert _parse_duration("PT15M") == timedelta(minutes=15)
        assert _parse_duration("PT30M") == timedelta(minutes=30)
        assert _parse_duration("PT60M") == timedelta(hours=1)
        assert _parse_duration("P1D") == timedelta(days=1)
        assert _parse_duration("PT2H30M") == timedelta(hours=2, minutes=30)

    def test_empty_xml(self):
        """Empty document returns no points."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <GL_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0">
          <mRID>empty</mRID>
        </GL_MarketDocument>"""
        points = parse_entsoe_xml(xml, "A75")
        assert points == []


# ===== API URL Builder Tests =====

@pytest.mark.unit
class TestBuildApiUrl:
    """Tests for API URL construction."""

    def test_basic_url(self):
        url = build_api_url(
            "https://web-api.tp.entsoe.eu/api",
            "test-token",
            "A75",
            "10YDE-AT-LU---Q",
        GL_START,
        GL_START + timedelta(hours=6),
        )
        assert "securityToken=test-token" in url
        assert "documentType=A75" in url
        assert "in_Domain=10YDE-AT-LU---Q" in url
        assert f"periodStart={_period_param(GL_START)}" in url
        assert f"periodEnd={_period_param(GL_START + timedelta(hours=6))}" in url

    def test_url_with_psr_type(self):
        url = build_api_url(
            "https://web-api.tp.entsoe.eu/api",
            "tok",
            "A75",
            "10YDE-AT-LU---Q",
        GL_START,
        GL_START + timedelta(days=1),
            psr_type="B01",
        )
        assert "psrType=B01" in url


# ===== Delta State Tests =====

@pytest.mark.unit
class TestDeltaState:
    """Tests for the delta state management."""

    def test_empty_state(self):
        """Loading a nonexistent file returns empty dict."""
        state = load_state("/tmp/nonexistent_entsoe_state_12345.json")
        assert state == {}

    def test_save_and_load(self):
        """Round-trip save and load."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            state_file = f.name
        try:
            state = {}
            ts = STATE_TS
            set_last_polled(state, "A75", "10YDE-AT-LU---Q", ts)
            save_state(state_file, state)

            loaded = load_state(state_file)
            result = get_last_polled(loaded, "A75", "10YDE-AT-LU---Q")
            assert result == ts
        finally:
            os.unlink(state_file)

    def test_get_last_polled_missing(self):
        """Missing key returns None."""
        state = {"A75": {"10YDE-AT-LU---Q": GL_START.isoformat()}}
        assert get_last_polled(state, "A44", "10YDE-AT-LU---Q") is None
        assert get_last_polled(state, "A75", "10YFR-RTE------C") is None

    def test_set_last_polled_creates_nesting(self):
        """Setting a new doc_type/domain creates the nested structure."""
        state = {}
        ts = PRICE_START
        set_last_polled(state, "A44", "10YFR-RTE------C", ts)
        assert state["A44"]["10YFR-RTE------C"] == PRICE_START.isoformat()

    def test_multiple_domains(self):
        """Multiple domains under one doc type."""
        state = {}
        ts1 = LOAD_START
        ts2 = LOAD_START + timedelta(hours=1)
        set_last_polled(state, "A75", "10YDE-AT-LU---Q", ts1)
        set_last_polled(state, "A75", "10YFR-RTE------C", ts2)
        assert get_last_polled(state, "A75", "10YDE-AT-LU---Q") == ts1
        assert get_last_polled(state, "A75", "10YFR-RTE------C") == ts2


# ===== Connection String Parsing Tests =====

@pytest.mark.unit
class TestConnectionStringParsing:
    """Tests for Event Hubs/Fabric connection string parsing."""

    def test_event_hubs_connection_string(self):
        cs = "Endpoint=sb://myns.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=abc123=;EntityPath=my-topic"
        result = parse_connection_string(cs)
        assert result["bootstrap.servers"] == "myns.servicebus.windows.net:9093"
        assert result["kafka_topic"] == "my-topic"
        assert result["sasl.username"] == "$ConnectionString"
        assert result["sasl.password"] == cs
        assert result["security.protocol"] == "SASL_SSL"

    def test_bootstrap_server_override(self):
        cs = "BootstrapServer=broker1:9092;EntityPath=topic1"
        result = parse_connection_string(cs)
        assert result["bootstrap.servers"] == "broker1:9092"
        assert result["kafka_topic"] == "topic1"


# ===== Poller Tests =====

@pytest.mark.unit
class TestEntsoePoller:
    """Tests for the polling and emission logic."""

    @pytest.fixture
    def mock_producer(self):
        producer = Mock()
        producer.producer = Mock()
        producer.producer.flush = Mock()
        return producer

    @pytest.fixture
    def poller(self, mock_producer, tmp_path):
        state_file = str(tmp_path / "state.json")
        return EntsoePoller(
            security_token="test-token",
            domain_producer=mock_producer,
            domain_psr_producer=mock_producer,
            cross_border_producer=mock_producer,
            kafka_producer=mock_producer.producer,
            state_file=state_file,
            domains=["10YDE-AT-LU---Q"],
            document_types=["A75"],
            lookback_hours=24,
            polling_interval=60,
        )

    @patch("entsoe.entsoe.requests.get")
    def test_poll_once_emits_events(self, mock_get, mock_producer, tmp_path):
        """A poll cycle with data emits events and advances checkpoint."""
        poller = EntsoePoller(
            security_token="test-token",
            domain_producer=mock_producer,
            domain_psr_producer=mock_producer,
            cross_border_producer=mock_producer,
            kafka_producer=mock_producer.producer,
            state_file=str(tmp_path / "state.json"),
            domains=["10YDE-AT-LU---Q"],
            document_types=["A75"],
            lookback_hours=24,
            polling_interval=60,
        )
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = SAMPLE_GL_XML
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        total = poller.poll_once()
        assert total == 6  # 4 B01 + 2 B02 points
        assert mock_producer.send_eu_entsoe_transparency_actual_generation_per_type.call_count == 6
        mock_producer.producer.flush.assert_called()

        # Checkpoint was saved
        state = load_state(poller.state_file)
        assert "A75" in state
        assert "10YDE-AT-LU---Q" in state["A75"]

    @patch("entsoe.entsoe.requests.get")
    def test_poll_no_data(self, mock_get, poller, mock_producer):
        """400 response (no data) results in zero events."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_get.return_value = mock_response

        total = poller.poll_once()
        assert total == 0
        assert mock_producer.send_eu_entsoe_transparency_actual_generation_per_type.call_count == 0

    @patch("entsoe.entsoe.requests.get")
    def test_delta_filtering(self, mock_get, poller, mock_producer):
        """Points before the checkpoint are filtered out."""
        checkpoint = GL_START + timedelta(minutes=30)
        set_last_polled(poller.state, "A75", "10YDE-AT-LU---Q", checkpoint)
        save_state(poller.state_file, poller.state)

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = SAMPLE_GL_XML
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        total = poller.poll_once()
        # B01: pos 1 (00:00), 2 (00:15), 3 (00:30), 4 (00:45) — only pos 4 after checkpoint
        # B02: pos 1 (00:00), 2 (00:15) — none after checkpoint
        assert total == 1
        assert mock_producer.send_eu_entsoe_transparency_actual_generation_per_type.call_count == 1

    @patch("entsoe.entsoe.requests.get")
    def test_price_emission(self, mock_get, tmp_path):
        """Day-ahead price events are emitted correctly."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = SAMPLE_PRICE_XML
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        mock_producer = Mock()
        mock_producer.producer = Mock()
        mock_producer.producer.flush = Mock()

        poller = EntsoePoller(
            security_token="test",
            domain_producer=mock_producer,
            domain_psr_producer=mock_producer,
            cross_border_producer=mock_producer,
            kafka_producer=mock_producer.producer,
            state_file=str(tmp_path / "state.json"),
            domains=["10YFR-RTE------C"],
            document_types=["A44"],
            lookback_hours=48,
            polling_interval=60,
        )

        total = poller.poll_once()
        assert total == 3
        assert mock_producer.send_eu_entsoe_transparency_day_ahead_prices.call_count == 3

    @patch("entsoe.entsoe.requests.get")
    def test_load_emission(self, mock_get, tmp_path):
        """Actual total load events are emitted correctly."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = SAMPLE_LOAD_XML
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        mock_producer = Mock()
        mock_producer.producer = Mock()
        mock_producer.producer.flush = Mock()

        poller = EntsoePoller(
            security_token="test",
            domain_producer=mock_producer,
            domain_psr_producer=mock_producer,
            cross_border_producer=mock_producer,
            kafka_producer=mock_producer.producer,
            state_file=str(tmp_path / "state.json"),
            domains=["10YES-REE------0"],
            document_types=["A65"],
            lookback_hours=48,
            polling_interval=60,
        )

        total = poller.poll_once()
        assert total == 2
        assert mock_producer.send_eu_entsoe_transparency_actual_total_load.call_count == 2


# ===== New document type fixtures =====

SAMPLE_WIND_SOLAR_FORECAST_XML = f"""<?xml version="1.0" encoding="UTF-8"?>
<GL_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0">
  <mRID>wsf123</mRID>
  <type>A69</type>
  <TimeSeries>
    <mRID>ts_wsf</mRID>
    <businessType>A01</businessType>
    <inBiddingZone_Domain.mRID>10Y1001A1001A83F</inBiddingZone_Domain.mRID>
    <quantity_Measure_Unit.name>MAW</quantity_Measure_Unit.name>
    <MktPSRType><psrType>B16</psrType></MktPSRType>
    <Period>
      <timeInterval>
        <start>{_iso8601_z(WIND_SOLAR_START)}</start>
        <end>{_iso8601_z(WIND_SOLAR_END)}</end>
      </timeInterval>
      <resolution>PT15M</resolution>
      <Point><position>1</position><quantity>0.0</quantity></Point>
      <Point><position>2</position><quantity>50.0</quantity></Point>
      <Point><position>3</position><quantity>200.0</quantity></Point>
    </Period>
  </TimeSeries>
</GL_MarketDocument>"""

SAMPLE_CROSS_BORDER_XML = f"""<?xml version="1.0" encoding="UTF-8"?>
<GL_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0">
  <mRID>cb123</mRID>
  <type>A11</type>
  <TimeSeries>
    <mRID>ts_cb</mRID>
    <businessType>A01</businessType>
    <in_Domain.mRID>10YFR-RTE------C</in_Domain.mRID>
    <out_Domain.mRID>10YES-REE------0</out_Domain.mRID>
    <quantity_Measure_Unit.name>MAW</quantity_Measure_Unit.name>
    <Period>
      <timeInterval>
        <start>{_iso8601_z(CROSS_BORDER_START)}</start>
        <end>{_iso8601_z(CROSS_BORDER_END)}</end>
      </timeInterval>
      <resolution>PT60M</resolution>
      <Point><position>1</position><quantity>1500.0</quantity></Point>
    </Period>
  </TimeSeries>
</GL_MarketDocument>"""

SAMPLE_GENERATION_FORECAST_XML = f"""<?xml version="1.0" encoding="UTF-8"?>
<GL_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0">
  <mRID>gf123</mRID>
  <type>A71</type>
  <TimeSeries>
    <mRID>ts_gf</mRID>
    <businessType>A01</businessType>
    <inBiddingZone_Domain.mRID>10Y1001A1001A83F</inBiddingZone_Domain.mRID>
    <quantity_Measure_Unit.name>MAW</quantity_Measure_Unit.name>
    <Period>
      <timeInterval>
        <start>{_iso8601_z(GENERATION_FORECAST_START)}</start>
        <end>{_iso8601_z(GENERATION_FORECAST_END)}</end>
      </timeInterval>
      <resolution>PT60M</resolution>
      <Point><position>1</position><quantity>45000.0</quantity></Point>
      <Point><position>2</position><quantity>44500.0</quantity></Point>
    </Period>
  </TimeSeries>
</GL_MarketDocument>"""


# ===== Tests for new document types =====

@pytest.mark.unit
class TestNewDocumentTypeParsing:
    """Tests for parsing new document types (A69, A11, A71, etc)."""

    def test_parse_wind_solar_forecast(self):
        """Parse A69 wind & solar forecast XML."""
        points = parse_entsoe_xml(SAMPLE_WIND_SOLAR_FORECAST_XML, "A69")
        assert len(points) == 3
        p = points[0]
        assert p.in_domain == "10Y1001A1001A83F"
        assert p.psr_type == "B16"
        assert p.quantity == 0.0
        assert p.document_type == "A69"
        assert p.resolution == "PT15M"

    def test_parse_cross_border_flows(self):
        """Parse A11 cross-border physical flows XML."""
        points = parse_entsoe_xml(SAMPLE_CROSS_BORDER_XML, "A11")
        assert len(points) == 1
        p = points[0]
        assert p.in_domain == "10YFR-RTE------C"
        assert p.out_domain == "10YES-REE------0"
        assert p.quantity == 1500.0
        assert p.document_type == "A11"

    def test_parse_generation_forecast(self):
        """Parse A71 generation forecast XML."""
        points = parse_entsoe_xml(SAMPLE_GENERATION_FORECAST_XML, "A71")
        assert len(points) == 2
        assert points[0].quantity == 45000.0
        assert points[1].quantity == 44500.0
        assert points[0].timestamp == GENERATION_FORECAST_START
        assert points[1].timestamp == GENERATION_FORECAST_START + timedelta(hours=1)


@pytest.mark.unit
class TestProcessTypeMapping:
    """Tests for document type → processType mapping."""

    def test_realised_types(self):
        for dt in ("A75", "A65", "A73", "A74", "A72", "A11", "A44"):
            assert _process_type_for_document(dt) == "A16"

    def test_forecast_types(self):
        for dt in ("A69", "A70", "A71"):
            assert _process_type_for_document(dt) == "A01"

    def test_capacity_type(self):
        assert _process_type_for_document("A68") == "A33"


@pytest.mark.unit
class TestBuildApiUrlExtended:
    """Tests for build_api_url with new parameters."""

    def test_cross_border_url(self):
        url = build_api_url(
            "https://web-api.tp.entsoe.eu/api", "tok", "A11",
            "10YFR-RTE------C",
        CROSS_BORDER_START,
        CROSS_BORDER_START + timedelta(days=1),
            out_domain="10YES-REE------0",
        )
        assert "documentType=A11" in url
        assert "in_Domain=10YFR-RTE------C" in url
        assert "out_Domain=10YES-REE------0" in url
        assert "processType=A16" in url

    def test_forecast_process_type(self):
        url = build_api_url(
            "https://web-api.tp.entsoe.eu/api", "tok", "A69",
            "10Y1001A1001A83F",
        WIND_SOLAR_START,
        WIND_SOLAR_START + timedelta(days=1),
        )
        assert "processType=A01" in url

    def test_capacity_process_type(self):
        url = build_api_url(
            "https://web-api.tp.entsoe.eu/api", "tok", "A68",
            "10Y1001A1001A83F",
        GENERATION_FORECAST_START,
        GENERATION_FORECAST_START + timedelta(days=1),
        )
        assert "processType=A33" in url


@pytest.mark.unit
class TestNewDocTypeEmission:
    """Tests for emitting events for new document types."""

    @patch("entsoe.entsoe.requests.get")
    def test_wind_solar_forecast_emission(self, mock_get, tmp_path):
        """A69 events are emitted via send_wind_solar_forecast."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = SAMPLE_WIND_SOLAR_FORECAST_XML
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        mock_producer = Mock()
        mock_producer.producer = Mock()
        mock_producer.producer.flush = Mock()

        poller = EntsoePoller(
            security_token="test",
            domain_producer=mock_producer,
            domain_psr_producer=mock_producer,
            cross_border_producer=mock_producer,
            kafka_producer=mock_producer.producer,
            state_file=str(tmp_path / "state.json"),
            domains=["10Y1001A1001A83F"], document_types=["A69"],
            lookback_hours=720, polling_interval=60,
        )
        total = poller.poll_once()
        assert total == 3
        assert mock_producer.send_eu_entsoe_transparency_wind_solar_forecast.call_count == 3

    @patch("entsoe.entsoe.requests.get")
    def test_cross_border_emission(self, mock_get, tmp_path):
        """A11 events are emitted via send_cross_border_physical_flows."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = SAMPLE_CROSS_BORDER_XML
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        mock_producer = Mock()
        mock_producer.producer = Mock()
        mock_producer.producer.flush = Mock()

        poller = EntsoePoller(
            security_token="test",
            domain_producer=mock_producer,
            domain_psr_producer=mock_producer,
            cross_border_producer=mock_producer,
            kafka_producer=mock_producer.producer,
            state_file=str(tmp_path / "state.json"),
            domains=[], document_types=["A11"],
            cross_border_pairs=[("10YFR-RTE------C", "10YES-REE------0")],
            lookback_hours=720, polling_interval=60,
        )
        total = poller.poll_once()
        assert total == 1
        assert mock_producer.send_eu_entsoe_transparency_cross_border_physical_flows.call_count == 1

    @patch("entsoe.entsoe.requests.get")
    def test_generation_forecast_emission(self, mock_get, tmp_path):
        """A71 events are emitted via send_generation_forecast."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = SAMPLE_GENERATION_FORECAST_XML
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        mock_producer = Mock()
        mock_producer.producer = Mock()
        mock_producer.producer.flush = Mock()

        poller = EntsoePoller(
            security_token="test",
            domain_producer=mock_producer,
            domain_psr_producer=mock_producer,
            cross_border_producer=mock_producer,
            kafka_producer=mock_producer.producer,
            state_file=str(tmp_path / "state.json"),
            domains=["10Y1001A1001A83F"], document_types=["A71"],
            lookback_hours=720, polling_interval=60,
        )
        total = poller.poll_once()
        assert total == 2
        assert mock_producer.send_eu_entsoe_transparency_generation_forecast.call_count == 2
