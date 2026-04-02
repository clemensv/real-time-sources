"""Integration tests for the ENTSO-E bridge.

These tests verify the end-to-end flow from HTTP responses through
XML parsing, delta filtering, and event emission using mocked HTTP
and Kafka layers.
"""

import json
import os
import tempfile
from datetime import datetime, timedelta, timezone
from unittest.mock import Mock, patch, call

import pytest

from entsoe.entsoe import EntsoePoller, parse_connection_string, main
from entsoe.delta_state import load_state, save_state, set_last_polled


# Full multi-series XML with generation, load-like structure
MULTI_SERIES_XML = """<?xml version="1.0" encoding="UTF-8"?>
<GL_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0">
  <mRID>multi123</mRID>
  <type>A75</type>
  <TimeSeries>
    <mRID>ts_wind</mRID>
    <businessType>A01</businessType>
    <inBiddingZone_Domain.mRID>10YDE-AT-LU---Q</inBiddingZone_Domain.mRID>
    <quantity_Measure_Unit.name>MAW</quantity_Measure_Unit.name>
    <MktPSRType><psrType>B19</psrType></MktPSRType>
    <Period>
      <timeInterval>
        <start>2026-04-01T00:00Z</start>
        <end>2026-04-01T01:00Z</end>
      </timeInterval>
      <resolution>PT15M</resolution>
      <Point><position>1</position><quantity>800.0</quantity></Point>
      <Point><position>2</position><quantity>820.0</quantity></Point>
      <Point><position>3</position><quantity>810.0</quantity></Point>
      <Point><position>4</position><quantity>830.0</quantity></Point>
    </Period>
  </TimeSeries>
  <TimeSeries>
    <mRID>ts_solar</mRID>
    <businessType>A01</businessType>
    <inBiddingZone_Domain.mRID>10YDE-AT-LU---Q</inBiddingZone_Domain.mRID>
    <quantity_Measure_Unit.name>MAW</quantity_Measure_Unit.name>
    <MktPSRType><psrType>B16</psrType></MktPSRType>
    <Period>
      <timeInterval>
        <start>2026-04-01T00:00Z</start>
        <end>2026-04-01T01:00Z</end>
      </timeInterval>
      <resolution>PT15M</resolution>
      <Point><position>1</position><quantity>0.0</quantity></Point>
      <Point><position>2</position><quantity>50.0</quantity></Point>
      <Point><position>3</position><quantity>200.0</quantity></Point>
      <Point><position>4</position><quantity>350.0</quantity></Point>
    </Period>
  </TimeSeries>
  <TimeSeries>
    <mRID>ts_nuclear</mRID>
    <businessType>A01</businessType>
    <inBiddingZone_Domain.mRID>10YDE-AT-LU---Q</inBiddingZone_Domain.mRID>
    <quantity_Measure_Unit.name>MAW</quantity_Measure_Unit.name>
    <MktPSRType><psrType>B14</psrType></MktPSRType>
    <Period>
      <timeInterval>
        <start>2026-04-01T00:00Z</start>
        <end>2026-04-01T01:00Z</end>
      </timeInterval>
      <resolution>PT15M</resolution>
      <Point><position>1</position><quantity>4200.0</quantity></Point>
      <Point><position>2</position><quantity>4200.0</quantity></Point>
    </Period>
  </TimeSeries>
</GL_MarketDocument>"""

PRICE_24H_XML = """<?xml version="1.0" encoding="UTF-8"?>
<Publication_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-3:publicationdocument:7:3">
  <mRID>price_24h</mRID>
  <type>A44</type>
  <TimeSeries>
    <mRID>ts_price_fr</mRID>
    <businessType>A62</businessType>
    <in_Domain.mRID>10YFR-RTE------C</in_Domain.mRID>
    <currency_Unit.name>EUR</currency_Unit.name>
    <price_Measure_Unit.name>MWH</price_Measure_Unit.name>
    <Period>
      <timeInterval>
        <start>2026-04-01T00:00Z</start>
        <end>2026-04-01T06:00Z</end>
      </timeInterval>
      <resolution>PT60M</resolution>
      <Point><position>1</position><price.amount>42.00</price.amount></Point>
      <Point><position>2</position><price.amount>38.50</price.amount></Point>
      <Point><position>3</position><price.amount>35.20</price.amount></Point>
      <Point><position>4</position><price.amount>33.10</price.amount></Point>
      <Point><position>5</position><price.amount>31.00</price.amount></Point>
      <Point><position>6</position><price.amount>45.70</price.amount></Point>
    </Period>
  </TimeSeries>
</Publication_MarketDocument>"""


def _make_response(xml_text, status=200):
    """Create a mock HTTP response."""
    resp = Mock()
    resp.status_code = status
    resp.text = xml_text
    resp.raise_for_status = Mock()
    return resp


@pytest.mark.integration
class TestMultiDomainPolling:
    """Test polling across multiple domains and document types."""

    @patch("entsoe.entsoe.requests.get")
    def test_multi_domain_multi_doctype(self, mock_get, tmp_path):
        """Poll two domains × two document types in a single cycle."""
        gen_xml_de = MULTI_SERIES_XML
        gen_xml_fr = MULTI_SERIES_XML.replace("10YDE-AT-LU---Q", "10YFR-RTE------C")
        price_xml_de = PRICE_24H_XML.replace("10YFR-RTE------C", "10YDE-AT-LU---Q")
        price_xml_fr = PRICE_24H_XML

        call_count = {"n": 0}
        responses = [
            _make_response(gen_xml_de),
            _make_response(gen_xml_fr),
            _make_response(price_xml_de),
            _make_response(price_xml_fr),
        ]

        def side_effect(*args, **kwargs):
            idx = call_count["n"]
            call_count["n"] += 1
            return responses[idx]

        mock_get.side_effect = side_effect

        mock_producer = Mock()
        mock_producer.producer = Mock()
        mock_producer.producer.flush = Mock()

        poller = EntsoePoller(
            security_token="test-token",
            producer=mock_producer,
            state_file=str(tmp_path / "state.json"),
            domains=["10YDE-AT-LU---Q", "10YFR-RTE------C"],
            document_types=["A75", "A44"],
            lookback_hours=720,
            polling_interval=60,
        )

        total = poller.poll_once()

        # A75: 10 points per domain (4 wind + 4 solar + 2 nuclear) × 2 domains = 20
        # A44: 6 prices per domain × 2 domains = 12
        assert total == 32
        assert mock_producer.send_eu_entsoe_transparency_actual_generation_per_type.call_count == 20
        assert mock_producer.send_eu_entsoe_transparency_day_ahead_prices.call_count == 12
        assert mock_get.call_count == 4

    @patch("entsoe.entsoe.requests.get")
    def test_state_persists_across_cycles(self, mock_get, tmp_path):
        """After a poll cycle, a second cycle only emits new data."""
        mock_get.return_value = _make_response(MULTI_SERIES_XML)

        mock_producer = Mock()
        mock_producer.producer = Mock()
        mock_producer.producer.flush = Mock()

        state_file = str(tmp_path / "state.json")
        poller = EntsoePoller(
            security_token="test-token",
            producer=mock_producer,
            state_file=state_file,
            domains=["10YDE-AT-LU---Q"],
            document_types=["A75"],
            lookback_hours=720,
            polling_interval=60,
        )

        # First cycle: should emit all 10 points
        total1 = poller.poll_once()
        assert total1 == 10

        # Second cycle: same XML, all points <= checkpoint → 0 new
        mock_producer.reset_mock()
        total2 = poller.poll_once()
        assert total2 == 0

        # State file has checkpoint
        state = load_state(state_file)
        assert "A75" in state
        assert "10YDE-AT-LU---Q" in state["A75"]


@pytest.mark.integration
class TestPartialFailures:
    """Test behavior when some API calls fail."""

    @patch("entsoe.entsoe.requests.get")
    def test_one_domain_fails_others_succeed(self, mock_get, tmp_path):
        """If one domain returns 400, other domains still produce events."""
        call_count = {"n": 0}

        def side_effect(*args, **kwargs):
            idx = call_count["n"]
            call_count["n"] += 1
            if idx == 0:
                return _make_response(None, status=400)
            return _make_response(MULTI_SERIES_XML)

        mock_get.side_effect = side_effect

        mock_producer = Mock()
        mock_producer.producer = Mock()
        mock_producer.producer.flush = Mock()

        poller = EntsoePoller(
            security_token="test-token",
            producer=mock_producer,
            state_file=str(tmp_path / "state.json"),
            domains=["10YDE-AT-LU---Q", "10YFR-RTE------C"],
            document_types=["A75"],
            lookback_hours=720,
            polling_interval=60,
        )

        total = poller.poll_once()
        # First domain fails (0), second succeeds (10)
        assert total == 10

    @patch("entsoe.entsoe.requests.get")
    def test_http_exception_handled(self, mock_get, tmp_path):
        """Network errors are logged, not raised."""
        import requests as req
        mock_get.side_effect = req.ConnectionError("DNS resolution failed")

        mock_producer = Mock()
        mock_producer.producer = Mock()
        mock_producer.producer.flush = Mock()

        poller = EntsoePoller(
            security_token="test-token",
            producer=mock_producer,
            state_file=str(tmp_path / "state.json"),
            domains=["10YDE-AT-LU---Q"],
            document_types=["A75"],
            lookback_hours=24,
            polling_interval=60,
        )

        total = poller.poll_once()
        assert total == 0


@pytest.mark.integration
class TestEventDataContent:
    """Verify the actual data passed to producer send methods."""

    @patch("entsoe.entsoe.requests.get")
    def test_generation_event_fields(self, mock_get, tmp_path):
        """Verify ActualGenerationPerType data fields."""
        mock_get.return_value = _make_response(MULTI_SERIES_XML)

        mock_producer = Mock()
        mock_producer.producer = Mock()
        mock_producer.producer.flush = Mock()

        poller = EntsoePoller(
            security_token="test-token",
            producer=mock_producer,
            state_file=str(tmp_path / "state.json"),
            domains=["10YDE-AT-LU---Q"],
            document_types=["A75"],
            lookback_hours=720,
            polling_interval=60,
        )

        poller.poll_once()

        # Check the first call's data argument
        first_call = mock_producer.send_eu_entsoe_transparency_actual_generation_per_type.call_args_list[0]
        data = first_call[0][0]  # positional arg 0
        assert data.inDomain == "10YDE-AT-LU---Q"
        assert data.psrType == "B19"
        assert data.quantity == 800.0
        assert data.resolution == "PT15M"
        assert data.documentType == "A75"
        assert data.unitName == "MAW"

    @patch("entsoe.entsoe.requests.get")
    def test_price_event_fields(self, mock_get, tmp_path):
        """Verify DayAheadPrices data fields."""
        mock_get.return_value = _make_response(PRICE_24H_XML)

        mock_producer = Mock()
        mock_producer.producer = Mock()
        mock_producer.producer.flush = Mock()

        poller = EntsoePoller(
            security_token="test-token",
            producer=mock_producer,
            state_file=str(tmp_path / "state.json"),
            domains=["10YFR-RTE------C"],
            document_types=["A44"],
            lookback_hours=720,
            polling_interval=60,
        )

        poller.poll_once()

        first_call = mock_producer.send_eu_entsoe_transparency_day_ahead_prices.call_args_list[0]
        data = first_call[0][0]
        assert data.inDomain == "10YFR-RTE------C"
        assert data.price == 42.00
        assert data.currency == "EUR"
        assert data.unitName == "MWH"
        assert data.resolution == "PT60M"
        assert data.documentType == "A44"


@pytest.mark.integration
class TestConnectionStringIntegration:
    """Test the full connection string → config flow."""

    def test_fabric_event_stream_connection_string(self):
        """Verify Fabric Event Stream connection string is correctly parsed."""
        cs = (
            "Endpoint=sb://testnamespace.servicebus.windows.net/;"
            "SharedAccessKeyName=test_key_name;"
            "SharedAccessKey=dGVzdC1zaGFyZWQtYWNjZXNzLWtleS12YWx1ZTEyMzQ1Njc=;"
            "EntityPath=test_entity"
        )
        config = parse_connection_string(cs)
        assert config["bootstrap.servers"] == "testnamespace.servicebus.windows.net:9093"
        assert config["kafka_topic"] == "test_entity"
        assert config["sasl.username"] == "$ConnectionString"
        assert config["security.protocol"] == "SASL_SSL"
        assert config["sasl.mechanism"] == "PLAIN"
        # Password should be the entire connection string
        assert "SharedAccessKey=" in config["sasl.password"]


# XML for cross-border integration tests
CROSS_BORDER_FLOW_XML = """<?xml version="1.0" encoding="UTF-8"?>
<GL_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0">
  <mRID>cb_int</mRID>
  <type>A11</type>
  <TimeSeries>
    <mRID>ts_flow</mRID>
    <businessType>A01</businessType>
    <in_Domain.mRID>{in_domain}</in_Domain.mRID>
    <out_Domain.mRID>{out_domain}</out_Domain.mRID>
    <quantity_Measure_Unit.name>MAW</quantity_Measure_Unit.name>
    <Period>
      <timeInterval>
        <start>2026-04-01T00:00Z</start>
        <end>2026-04-01T02:00Z</end>
      </timeInterval>
      <resolution>PT60M</resolution>
      <Point><position>1</position><quantity>1200.0</quantity></Point>
      <Point><position>2</position><quantity>1350.0</quantity></Point>
    </Period>
  </TimeSeries>
</GL_MarketDocument>"""


@pytest.mark.integration
class TestCrossBorderPolling:
    """Integration tests for A11 cross-border physical flow polling."""

    @patch("entsoe.entsoe.requests.get")
    def test_cross_border_polls_each_pair(self, mock_get, tmp_path):
        """A11 queries are made for each cross-border pair."""
        pairs = [
            ("10Y1001A1001A83F", "10YFR-RTE------C"),  # DE→FR
            ("10YFR-RTE------C", "10Y1001A1001A83F"),  # FR→DE
        ]

        def side_effect(*args, **kwargs):
            url = args[0] if args else kwargs.get("url", "")
            params = kwargs.get("params", {})
            # Return valid XML for each pair
            in_d = "10Y1001A1001A83F" if "10Y1001A1001A83F" in str(url) + str(params) else "10YFR-RTE------C"
            out_d = "10YFR-RTE------C" if in_d == "10Y1001A1001A83F" else "10Y1001A1001A83F"
            xml = CROSS_BORDER_FLOW_XML.format(in_domain=in_d, out_domain=out_d)
            return _make_response(xml)

        mock_get.side_effect = side_effect

        mock_producer = Mock()
        mock_producer.producer = Mock()
        mock_producer.producer.flush = Mock()

        poller = EntsoePoller(
            security_token="test-token",
            producer=mock_producer,
            state_file=str(tmp_path / "state.json"),
            domains=[],
            document_types=["A11"],
            cross_border_pairs=pairs,
            lookback_hours=720,
            polling_interval=60,
        )

        total = poller.poll_once()
        # 2 points × 2 pairs = 4
        assert total == 4
        assert mock_producer.send_eu_entsoe_transparency_cross_border_physical_flows.call_count == 4

    @patch("entsoe.entsoe.requests.get")
    def test_cross_border_state_uses_pair_key(self, mock_get, tmp_path):
        """Cross-border state keys include both in and out domains."""
        pair = ("10Y1001A1001A83F", "10YFR-RTE------C")
        xml = CROSS_BORDER_FLOW_XML.format(in_domain=pair[0], out_domain=pair[1])
        mock_get.return_value = _make_response(xml)

        mock_producer = Mock()
        mock_producer.producer = Mock()
        mock_producer.producer.flush = Mock()

        state_file = str(tmp_path / "state.json")
        poller = EntsoePoller(
            security_token="test-token",
            producer=mock_producer,
            state_file=state_file,
            domains=[],
            document_types=["A11"],
            cross_border_pairs=[pair],
            lookback_hours=720,
            polling_interval=60,
        )

        total1 = poller.poll_once()
        assert total1 == 2

        state = load_state(state_file)
        assert "A11" in state
        # State key should include both domains
        state_key = f"{pair[0]}>{pair[1]}"
        assert state_key in state["A11"]

        # Second poll — same data → 0 new
        mock_producer.reset_mock()
        total2 = poller.poll_once()
        assert total2 == 0

    @patch("entsoe.entsoe.requests.get")
    def test_mixed_doctypes_with_cross_border(self, mock_get, tmp_path):
        """A75 + A11 in same poll cycle: domains for A75, pairs for A11."""
        call_count = {"n": 0}

        def side_effect(*args, **kwargs):
            idx = call_count["n"]
            call_count["n"] += 1
            if idx == 0:
                # A75 for DE domain
                return _make_response(MULTI_SERIES_XML)
            else:
                # A11 for cross-border pair
                xml = CROSS_BORDER_FLOW_XML.format(
                    in_domain="10Y1001A1001A83F",
                    out_domain="10YFR-RTE------C",
                )
                return _make_response(xml)

        mock_get.side_effect = side_effect

        mock_producer = Mock()
        mock_producer.producer = Mock()
        mock_producer.producer.flush = Mock()

        poller = EntsoePoller(
            security_token="test-token",
            producer=mock_producer,
            state_file=str(tmp_path / "state.json"),
            domains=["10YDE-AT-LU---Q"],
            document_types=["A75", "A11"],
            cross_border_pairs=[("10Y1001A1001A83F", "10YFR-RTE------C")],
            lookback_hours=720,
            polling_interval=60,
        )

        total = poller.poll_once()
        # A75: 10 generation points; A11: 2 cross-border points
        assert total == 12
        assert mock_producer.send_eu_entsoe_transparency_actual_generation_per_type.call_count == 10
        assert mock_producer.send_eu_entsoe_transparency_cross_border_physical_flows.call_count == 2
