"""
Unit tests for NOAA SWPC Space Weather poller.
Tests core functionality without external dependencies.
"""

import pytest
import json
import os
import tempfile
from unittest.mock import Mock, patch, MagicMock
from noaa_goes.noaa_goes import SWPCPoller, parse_connection_string


@pytest.fixture
def mock_kafka_config():
    return {
        'bootstrap.servers': 'localhost:9092',
        'sasl.mechanisms': 'PLAIN',
        'security.protocol': 'SASL_SSL',
        'sasl.username': 'test_user',
        'sasl.password': 'test_password'
    }


@pytest.fixture
def temp_state_file():
    fd, path = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.unlink(path)


@pytest.fixture
def poller(mock_kafka_config, temp_state_file):
    with patch('noaa_goes.noaa_goes.MicrosoftOpenDataUSNOAASWPCAlertsEventProducer'), \
         patch('noaa_goes.noaa_goes.MicrosoftOpenDataUSNOAASWPCObservationsEventProducer'), \
         patch('noaa_goes.noaa_goes.MicrosoftOpenDataUSNOAASWPCGOESParticleFluxEventProducer'), \
         patch('noaa_goes.noaa_goes.MicrosoftOpenDataUSNOAASWPCGOESMagnetometerEventProducer'), \
         patch('noaa_goes.noaa_goes.MicrosoftOpenDataUSNOAASWPCSolarFlaresEventProducer'), \
         patch('confluent_kafka.Producer'):
        p = SWPCPoller(
            kafka_config=mock_kafka_config,
            kafka_topic='test-topic',
            last_polled_file=temp_state_file
        )
        p.kafka_producer = MagicMock()
        return p


@pytest.mark.unit
class TestStateManagement:
    def test_load_state_empty(self, poller):
        poller.last_polled_file = '/tmp/nonexistent_swpc_state.json'
        state = poller.load_state()
        assert state == {}

    def test_load_state_existing(self, poller, temp_state_file):
        state_data = {"last_alert_id": "alert123", "last_kindex_time": "2024-01-01 00:00:00"}
        with open(temp_state_file, 'w', encoding='utf-8') as f:
            json.dump(state_data, f)
        state = poller.load_state()
        assert state["last_alert_id"] == "alert123"

    def test_save_state(self, poller, temp_state_file):
        state_data = {"last_alert_id": "alert456"}
        poller.save_state(state_data)
        with open(temp_state_file, 'r', encoding='utf-8') as f:
            saved = json.load(f)
        assert saved["last_alert_id"] == "alert456"


@pytest.mark.unit
class TestPollAlerts:
    @patch('noaa_goes.noaa_goes.requests.get')
    def test_poll_alerts_success(self, mock_get, poller):
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = [
            {"product_id": "ALTK04-20240101", "issue_datetime": "2024 Jan 01 0030 UTC",
             "message": "Geomagnetic K-index of 4"}
        ]
        mock_get.return_value = mock_response
        alerts = poller.poll_alerts()
        assert len(alerts) == 1
        assert alerts[0]["product_id"] == "ALTK04-20240101"

    @patch('noaa_goes.noaa_goes.requests.get')
    def test_poll_alerts_error(self, mock_get, poller):
        mock_get.side_effect = Exception("Connection error")
        alerts = poller.poll_alerts()
        assert alerts == []


@pytest.mark.unit
class TestPollKIndex:
    @patch('noaa_goes.noaa_goes.requests.get')
    def test_poll_k_index_success(self, mock_get, poller):
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = [
            {"time_tag": "2024-01-01 00:00:00.000", "Kp": 2, "a_running": 5, "station_count": 8},
            {"time_tag": "2024-01-01 03:00:00.000", "Kp": 3, "a_running": 7, "station_count": 8}
        ]
        mock_get.return_value = mock_response
        rows = poller.poll_k_index()
        assert len(rows) == 2
        assert rows[0]["Kp"] == 2

    @patch('noaa_goes.noaa_goes.requests.get')
    def test_poll_k_index_error(self, mock_get, poller):
        mock_get.side_effect = Exception("Timeout")
        rows = poller.poll_k_index()
        assert rows == []


@pytest.mark.unit
class TestPollSolarWind:
    @patch('noaa_goes.noaa_goes.requests.get')
    def test_poll_solar_wind_success(self, mock_get, poller):
        speed_response = Mock()
        speed_response.raise_for_status = Mock()
        speed_response.json.return_value = [{"proton_speed": 425.3, "time_tag": "2024-01-01T00:05:00Z"}]
        mag_response = Mock()
        mag_response.raise_for_status = Mock()
        mag_response.json.return_value = [{"bt": 5.2, "bz_gsm": -1.3, "time_tag": "2024-01-01T00:05:00Z"}]
        mock_get.side_effect = [speed_response, mag_response]
        records = poller.poll_solar_wind()
        assert len(records) == 1
        assert records[0]["wind_speed"] == 425.3
        assert records[0]["bt"] == 5.2
        assert records[0]["bz"] == -1.3

    @patch('noaa_goes.noaa_goes.requests.get')
    def test_poll_solar_wind_error(self, mock_get, poller):
        mock_get.side_effect = Exception("Network error")
        records = poller.poll_solar_wind()
        assert records == []


@pytest.mark.unit
class TestPollPlasma:
    @patch('noaa_goes.noaa_goes.requests.get')
    def test_poll_plasma_success(self, mock_get, poller):
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = [
            ["time_tag", "density", "speed", "temperature"],
            ["2024-01-01 00:01:00.000", "5.2", "380.1", "45000"],
            ["2024-01-01 00:02:00.000", None, "390.0", None],
        ]
        mock_get.return_value = mock_response
        rows = poller.poll_plasma()
        assert len(rows) == 2
        assert rows[0]["time_tag"] == "2024-01-01 00:01:00.000"
        assert rows[0]["density"] == "5.2"
        assert rows[1]["density"] is None

    @patch('noaa_goes.noaa_goes.requests.get')
    def test_poll_plasma_empty(self, mock_get, poller):
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = [["time_tag", "density", "speed", "temperature"]]
        mock_get.return_value = mock_response
        rows = poller.poll_plasma()
        assert rows == []


@pytest.mark.unit
class TestPollMag:
    @patch('noaa_goes.noaa_goes.requests.get')
    def test_poll_mag_success(self, mock_get, poller):
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = [
            ["time_tag", "bx_gsm", "by_gsm", "bz_gsm", "lon_gsm", "lat_gsm", "bt"],
            ["2024-01-01 00:01:00.000", "-3.5", "2.1", "-1.0", "142.5", "9.5", "4.5"],
        ]
        mock_get.return_value = mock_response
        rows = poller.poll_mag()
        assert len(rows) == 1
        assert rows[0]["bz_gsm"] == "-1.0"


@pytest.mark.unit
class TestPollGoesXrays:
    @patch('noaa_goes.noaa_goes.requests.get')
    def test_poll_goes_xrays_success(self, mock_get, poller):
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = [
            {"time_tag": "2024-01-01T00:00:00Z", "satellite": 19, "flux": 1.5e-6, "energy": "0.1-0.8nm"},
            {"time_tag": "2024-01-01T00:00:00Z", "satellite": 19, "flux": 3.2e-8, "energy": "0.05-0.4nm"},
        ]
        mock_get.return_value = mock_response
        rows = poller.poll_goes_xrays()
        assert len(rows) == 2
        assert rows[0]["flux"] == 1.5e-6


@pytest.mark.unit
class TestPollGoesProtons:
    @patch('noaa_goes.noaa_goes.requests.get')
    def test_poll_goes_protons_success(self, mock_get, poller):
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = [
            {"time_tag": "2024-01-01T00:00:00Z", "satellite": 19, "flux": 0.42, "energy": ">=10 MeV"},
        ]
        mock_get.return_value = mock_response
        rows = poller.poll_goes_protons()
        assert len(rows) == 1
        assert rows[0]["energy"] == ">=10 MeV"


@pytest.mark.unit
class TestPollGoesElectrons:
    @patch('noaa_goes.noaa_goes.requests.get')
    def test_poll_goes_electrons_success(self, mock_get, poller):
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = [
            {"time_tag": "2024-01-01T00:00:00Z", "satellite": 19, "flux": 1634.35, "energy": ">=2 MeV"},
        ]
        mock_get.return_value = mock_response
        rows = poller.poll_goes_electrons()
        assert len(rows) == 1
        assert rows[0]["flux"] == 1634.35


@pytest.mark.unit
class TestPollGoesMagnetometers:
    @patch('noaa_goes.noaa_goes.requests.get')
    def test_poll_goes_magnetometers_success(self, mock_get, poller):
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = [
            {"time_tag": "2024-01-01T00:00:00Z", "satellite": 19, "He": 45.01, "Hp": 73.11,
             "Hn": -0.82, "total": 85.86, "arcjet_flag": False},
        ]
        mock_get.return_value = mock_response
        rows = poller.poll_goes_magnetometers()
        assert len(rows) == 1
        assert rows[0]["Hp"] == 73.11


@pytest.mark.unit
class TestPollXrayFlares:
    @patch('noaa_goes.noaa_goes.requests.get')
    def test_poll_xray_flares_success(self, mock_get, poller):
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = [
            {"time_tag": "2024-01-01T06:38:00Z", "begin_time": "2024-01-01T06:25:00Z",
             "begin_class": "B6.9", "max_time": "2024-01-01T06:35:00Z", "max_class": "C1.2",
             "max_xrlong": 1.2e-6, "max_ratio": 0.03, "max_ratio_time": "2024-01-01T06:34:00Z",
             "current_int_xrlong": 5.5e-4, "end_time": "2024-01-01T06:50:00Z",
             "end_class": "B5.0", "satellite": 19},
        ]
        mock_get.return_value = mock_response
        rows = poller.poll_xray_flares()
        assert len(rows) == 1
        assert rows[0]["max_class"] == "C1.2"


@pytest.mark.unit
class TestSendAlerts:
    def test_send_alerts_new(self, poller):
        state = {}
        with patch.object(poller, 'poll_alerts', return_value=[
            {"product_id": "ALTK04", "issue_datetime": "2024 Jan 01", "message": "test"}
        ]):
            count = poller._send_alerts(state)
        assert count == 1
        assert state["last_alert_id"] == "ALTK04"
        poller.alerts_producer.send_microsoft_open_data_us_noaa_swpc_space_weather_alert.assert_called_once()

    def test_send_alerts_dedup(self, poller):
        state = {"last_alert_id": "ALTK04"}
        with patch.object(poller, 'poll_alerts', return_value=[
            {"product_id": "ALTK04", "issue_datetime": "2024 Jan 01", "message": "test"}
        ]):
            count = poller._send_alerts(state)
        assert count == 0


@pytest.mark.unit
class TestSendKIndex:
    def test_send_k_index_new(self, poller):
        state = {}
        with patch.object(poller, 'poll_k_index', return_value=[
            {"time_tag": "2024-01-01 00:00:00.000", "Kp": 3, "a_running": 7, "station_count": 8}
        ]):
            count = poller._send_k_index(state)
        assert count == 1
        assert state["last_kindex_time"] == "2024-01-01 00:00:00.000"

    def test_send_k_index_dedup(self, poller):
        state = {"last_kindex_time": "2024-01-01 00:00:00.000"}
        with patch.object(poller, 'poll_k_index', return_value=[
            {"time_tag": "2024-01-01 00:00:00.000", "Kp": 3, "a_running": 7, "station_count": 8}
        ]):
            count = poller._send_k_index(state)
        assert count == 0


@pytest.mark.unit
class TestSendPlasma:
    def test_send_plasma_new(self, poller):
        state = {}
        with patch.object(poller, 'poll_plasma', return_value=[
            {"time_tag": "2024-01-01 00:01:00.000", "density": "5.2", "speed": "380", "temperature": "45000"}
        ]):
            count = poller._send_plasma(state)
        assert count == 1
        assert state["last_plasma_time"] == "2024-01-01 00:01:00.000"

    def test_send_plasma_dedup(self, poller):
        state = {"last_plasma_time": "2024-01-01 00:05:00.000"}
        with patch.object(poller, 'poll_plasma', return_value=[
            {"time_tag": "2024-01-01 00:01:00.000", "density": "5.2", "speed": "380", "temperature": "45000"}
        ]):
            count = poller._send_plasma(state)
        assert count == 0

    def test_send_plasma_null_fields(self, poller):
        state = {}
        with patch.object(poller, 'poll_plasma', return_value=[
            {"time_tag": "2024-01-01 00:01:00.000", "density": None, "speed": "380", "temperature": None}
        ]):
            count = poller._send_plasma(state)
        assert count == 1
        call_args = poller.observations_producer.send_microsoft_open_data_us_noaa_swpc_solar_wind_plasma.call_args
        plasma_obj = call_args[0][1]
        assert plasma_obj.density is None
        assert plasma_obj.speed == 380.0
        assert plasma_obj.temperature is None


@pytest.mark.unit
class TestSendMag:
    def test_send_mag_new(self, poller):
        state = {}
        with patch.object(poller, 'poll_mag', return_value=[
            {"time_tag": "2024-01-01 00:01:00.000", "bx_gsm": "-3.5", "by_gsm": "2.1",
             "bz_gsm": "-1.0", "lon_gsm": "142.5", "lat_gsm": "9.5", "bt": "4.5"}
        ]):
            count = poller._send_mag(state)
        assert count == 1
        call_args = poller.observations_producer.send_microsoft_open_data_us_noaa_swpc_solar_wind_mag_field.call_args
        mag_obj = call_args[0][1]
        assert mag_obj.bx_gsm == -3.5
        assert mag_obj.bz_gsm == -1.0
        assert mag_obj.bt == 4.5


@pytest.mark.unit
class TestSendGoesXrays:
    def test_send_goes_xrays_new(self, poller):
        state = {}
        with patch.object(poller, 'poll_goes_xrays', return_value=[
            {"time_tag": "2024-01-01T00:00:00Z", "satellite": 19, "flux": 1.5e-6, "energy": "0.1-0.8nm"},
        ]):
            count = poller._send_goes_xrays(state)
        assert count == 1
        assert state["last_xray_time"] == "2024-01-01T00:00:00Z"
        poller.particle_flux_producer.send_microsoft_open_data_us_noaa_swpc_goes_xray_flux.assert_called_once()

    def test_send_goes_xrays_dedup(self, poller):
        state = {"last_xray_time": "2024-01-01T00:00:00Z"}
        with patch.object(poller, 'poll_goes_xrays', return_value=[
            {"time_tag": "2024-01-01T00:00:00Z", "satellite": 19, "flux": 1.5e-6, "energy": "0.1-0.8nm"},
        ]):
            count = poller._send_goes_xrays(state)
        assert count == 0


@pytest.mark.unit
class TestSendGoesMagnetometers:
    def test_send_goes_magnetometers_new(self, poller):
        state = {}
        with patch.object(poller, 'poll_goes_magnetometers', return_value=[
            {"time_tag": "2024-01-01T00:00:00Z", "satellite": 19, "He": 45.0, "Hp": 73.0,
             "Hn": -0.8, "total": 85.9, "arcjet_flag": False},
        ]):
            count = poller._send_goes_magnetometers(state)
        assert count == 1
        call_args = poller.magnetometer_producer.send_microsoft_open_data_us_noaa_swpc_goes_magnetometer.call_args
        mag_obj = call_args[0][2]
        assert mag_obj.he == 45.0
        assert mag_obj.hp == 73.0
        assert mag_obj.arcjet_flag is None  # xrcg __post_init__ treats False as falsy → None


@pytest.mark.unit
class TestSendXrayFlares:
    def test_send_xray_flares_new(self, poller):
        state = {}
        with patch.object(poller, 'poll_xray_flares', return_value=[
            {"time_tag": "2024-01-01T06:38:00Z", "begin_time": "2024-01-01T06:25:00Z",
             "begin_class": "B6.9", "max_time": "2024-01-01T06:35:00Z", "max_class": "C1.2",
             "max_xrlong": 1.2e-6, "max_ratio": 0.03, "max_ratio_time": "2024-01-01T06:34:00Z",
             "current_int_xrlong": 5.5e-4, "end_time": "2024-01-01T06:50:00Z",
             "end_class": "B5.0", "satellite": 19},
        ]):
            count = poller._send_xray_flares(state)
        assert count == 1
        call_args = poller.flares_producer.send_microsoft_open_data_us_noaa_swpc_xray_flare.call_args
        flare_obj = call_args[0][2]
        assert flare_obj.max_class == "C1.2"
        assert flare_obj.satellite == 19

    def test_send_xray_flares_null_fields(self, poller):
        state = {}
        with patch.object(poller, 'poll_xray_flares', return_value=[
            {"time_tag": "2024-01-01T06:38:00Z", "begin_time": "2024-01-01T06:25:00Z",
             "begin_class": None, "max_time": None, "max_class": None,
             "max_xrlong": None, "max_ratio": None, "max_ratio_time": None,
             "current_int_xrlong": None, "end_time": None, "end_class": None, "satellite": 19},
        ]):
            count = poller._send_xray_flares(state)
        assert count == 1
        call_args = poller.flares_producer.send_microsoft_open_data_us_noaa_swpc_xray_flare.call_args
        flare_obj = call_args[0][2]
        assert flare_obj.max_class is None
        assert flare_obj.end_time is None


@pytest.mark.unit
class TestSendGoesProtons:
    def test_send_goes_protons_new(self, poller):
        state = {}
        with patch.object(poller, 'poll_goes_protons', return_value=[
            {"time_tag": "2024-01-01T00:00:00Z", "satellite": 19, "flux": 0.42, "energy": ">=10 MeV"},
        ]):
            count = poller._send_goes_protons(state)
        assert count == 1
        assert state["last_proton_time"] == "2024-01-01T00:00:00Z"


@pytest.mark.unit
class TestSendGoesElectrons:
    def test_send_goes_electrons_new(self, poller):
        state = {}
        with patch.object(poller, 'poll_goes_electrons', return_value=[
            {"time_tag": "2024-01-01T00:00:00Z", "satellite": 19, "flux": 1634.35, "energy": ">=2 MeV"},
        ]):
            count = poller._send_goes_electrons(state)
        assert count == 1
        assert state["last_electron_time"] == "2024-01-01T00:00:00Z"


@pytest.mark.unit
class TestParseConnectionString:
    def test_parse_valid(self):
        conn_str = "Endpoint=sb://mynamespace.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=abc123;EntityPath=myhub"
        result = parse_connection_string(conn_str)
        assert result['bootstrap.servers'] == 'mynamespace.servicebus.windows.net:9093'
        assert result['kafka_topic'] == 'myhub'
        assert result['sasl.username'] == '$ConnectionString'

    def test_parse_bootstrap_server(self):
        conn_str = "BootstrapServer=localhost:9092;EntityPath=my-topic"
        result = parse_connection_string(conn_str)
        assert result['bootstrap.servers'] == 'localhost:9092'
        assert result['kafka_topic'] == 'my-topic'

    def test_parse_password_is_full_string(self):
        conn_str = "Endpoint=sb://test.servicebus.windows.net/;SharedAccessKeyName=test;SharedAccessKey=key;EntityPath=hub"
        result = parse_connection_string(conn_str)
        assert result['sasl.password'] == conn_str


@pytest.mark.unit
class TestSafeConversions:
    def test_safe_float(self, poller):
        assert poller._safe_float("3.14") == 3.14
        assert poller._safe_float(None) is None
        assert poller._safe_float("bad") is None
        assert poller._safe_float(42) == 42.0

    def test_safe_int(self, poller):
        assert poller._safe_int("19") == 19
        assert poller._safe_int(None) is None
        assert poller._safe_int("bad") is None
        assert poller._safe_int(19) == 19
