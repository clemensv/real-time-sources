"""
Unit tests for the Madrid Real-Time Traffic (Informo) bridge.
Tests core functionality without external dependencies.
"""

import pytest
import datetime
import xml.etree.ElementTree as ET
from unittest.mock import Mock, patch, MagicMock
from madrid_traffic_producer_data import MeasurementPoint, TrafficReading
from madrid_traffic.madrid_traffic import (
    parse_european_float,
    safe_int,
    round_to_5min,
    parse_pm_xml,
    build_measurement_point,
    build_traffic_reading,
    parse_connection_string,
    MadridTrafficPoller,
)


SAMPLE_PM_XML = """\
<?xml version="1.0" encoding="UTF-8"?>
<pms>
  <fecha_hora>15/06/2024 14:30:04</fecha_hora>
  <pm>
    <idelem>9841</idelem>
    <descripcion>Valle de Mena S-E - Acc.Ramon Castroviejo-Gta.Isaac Rabín</descripcion>
    <accesoAsociado>0301005</accesoAsociado>
    <intensidad>120</intensidad>
    <ocupacion>15</ocupacion>
    <carga>4</carga>
    <nivelServicio>0</nivelServicio>
    <intensidadSat>3100</intensidadSat>
    <error>N</error>
    <subarea>0328</subarea>
    <st_x>438339,375874991</st_x>
    <st_y>4480454,96970565</st_y>
  </pm>
  <pm>
    <idelem>9843</idelem>
    <descripcion>Dr.Ramon Castroviejo O-E</descripcion>
    <accesoAsociado>0301003</accesoAsociado>
    <intensidad>40</intensidad>
    <ocupacion>0</ocupacion>
    <carga>1</carga>
    <nivelServicio>0</nivelServicio>
    <intensidadSat>2000</intensidadSat>
    <error>N</error>
    <subarea>0328</subarea>
    <st_x>438098,880458143</st_x>
    <st_y>4480455,13738494</st_y>
  </pm>
  <pm>
    <idelem>5555</idelem>
    <descripcion>Error sensor test</descripcion>
    <accesoAsociado>0301099</accesoAsociado>
    <intensidad>0</intensidad>
    <ocupacion>0</ocupacion>
    <carga>0</carga>
    <nivelServicio>0</nivelServicio>
    <intensidadSat>1000</intensidadSat>
    <error>S</error>
    <subarea>0100</subarea>
    <st_x>440000,000000000</st_x>
    <st_y>4481000,00000000</st_y>
  </pm>
</pms>
"""

SAMPLE_PM_XML_MINIMAL = """\
<?xml version="1.0" encoding="UTF-8"?>
<pms>
  <pm>
    <idelem>1001</idelem>
    <descripcion>Test road</descripcion>
    <intensidad>50</intensidad>
    <ocupacion>10</ocupacion>
    <carga>2</carga>
    <nivelServicio>1</nivelServicio>
    <intensidadSat>500</intensidadSat>
    <error>N</error>
  </pm>
</pms>
"""

SAMPLE_PM_XML_EMPTY = """\
<?xml version="1.0" encoding="UTF-8"?>
<pms>
  <fecha_hora>15/06/2024 14:30:04</fecha_hora>
</pms>
"""


@pytest.mark.unit
class TestParseEuropeanFloat:
    """Tests for European comma-decimal float parsing."""

    def test_normal_value(self):
        assert parse_european_float('438339,375874991') == pytest.approx(438339.375874991)

    def test_integer_value(self):
        assert parse_european_float('12345') == 12345.0

    def test_dot_decimal(self):
        assert parse_european_float('12.34') == 12.34

    def test_empty_string(self):
        assert parse_european_float('') is None

    def test_none_value(self):
        assert parse_european_float(None) is None

    def test_whitespace(self):
        assert parse_european_float('  438339,375  ') == pytest.approx(438339.375)

    def test_invalid_string(self):
        assert parse_european_float('not-a-number') is None

    def test_negative_value(self):
        assert parse_european_float('-3,14') == pytest.approx(-3.14)


@pytest.mark.unit
class TestSafeInt:
    """Tests for safe integer parsing."""

    def test_normal_value(self):
        assert safe_int('120') == 120

    def test_zero(self):
        assert safe_int('0') == 0

    def test_empty_string(self):
        assert safe_int('') is None

    def test_none_value(self):
        assert safe_int(None) is None

    def test_whitespace(self):
        assert safe_int('  42  ') == 42

    def test_invalid_string(self):
        assert safe_int('abc') is None

    def test_float_string(self):
        assert safe_int('3.14') is None

    def test_negative(self):
        assert safe_int('-5') == -5


@pytest.mark.unit
class TestRoundTo5Min:
    """Tests for rounding datetime to 5-minute boundaries."""

    def test_exact_boundary(self):
        dt = datetime.datetime(2024, 6, 15, 14, 30, 0, tzinfo=datetime.timezone.utc)
        result = round_to_5min(dt)
        assert result.minute == 30
        assert result.second == 0

    def test_mid_interval(self):
        dt = datetime.datetime(2024, 6, 15, 14, 33, 45, tzinfo=datetime.timezone.utc)
        result = round_to_5min(dt)
        assert result.minute == 30
        assert result.second == 0
        assert result.microsecond == 0

    def test_just_before_boundary(self):
        dt = datetime.datetime(2024, 6, 15, 14, 34, 59, tzinfo=datetime.timezone.utc)
        result = round_to_5min(dt)
        assert result.minute == 30

    def test_at_zero(self):
        dt = datetime.datetime(2024, 6, 15, 14, 0, 0, tzinfo=datetime.timezone.utc)
        result = round_to_5min(dt)
        assert result.minute == 0

    def test_at_59(self):
        dt = datetime.datetime(2024, 6, 15, 14, 59, 59, tzinfo=datetime.timezone.utc)
        result = round_to_5min(dt)
        assert result.minute == 55


@pytest.mark.unit
class TestParsePmXml:
    """Tests for XML parsing of the pm.xml feed."""

    def test_parse_full_xml(self):
        sensors, fecha_hora = parse_pm_xml(SAMPLE_PM_XML)
        assert len(sensors) == 3
        assert fecha_hora == '15/06/2024 14:30:04'

    def test_parse_sensor_fields(self):
        sensors, _ = parse_pm_xml(SAMPLE_PM_XML)
        s = sensors[0]
        assert s['idelem'] == '9841'
        assert s['intensidad'] == '120'
        assert s['ocupacion'] == '15'
        assert s['carga'] == '4'
        assert s['nivelServicio'] == '0'
        assert s['intensidadSat'] == '3100'
        assert s['error'] == 'N'
        assert s['subarea'] == '0328'

    def test_parse_coordinates(self):
        sensors, _ = parse_pm_xml(SAMPLE_PM_XML)
        s = sensors[0]
        assert s['st_x'] == '438339,375874991'
        assert s['st_y'] == '4480454,96970565'

    def test_parse_empty_xml(self):
        sensors, fecha_hora = parse_pm_xml(SAMPLE_PM_XML_EMPTY)
        assert len(sensors) == 0
        assert fecha_hora == '15/06/2024 14:30:04'

    def test_parse_minimal_xml(self):
        sensors, fecha_hora = parse_pm_xml(SAMPLE_PM_XML_MINIMAL)
        assert len(sensors) == 1
        assert fecha_hora is None

    def test_sensor_description_with_special_chars(self):
        sensors, _ = parse_pm_xml(SAMPLE_PM_XML)
        assert 'Rabín' in sensors[0]['descripcion']


@pytest.mark.unit
class TestBuildMeasurementPoint:
    """Tests for building MeasurementPoint from raw sensor dict."""

    def test_full_sensor(self):
        sensors, _ = parse_pm_xml(SAMPLE_PM_XML)
        mp = build_measurement_point(sensors[0])
        assert mp.sensor_id == '9841'
        assert 'Valle de Mena' in mp.description
        assert mp.subarea == '0328'
        assert mp.saturation_intensity == 3100
        assert mp.longitude == pytest.approx(438339.375874991)
        assert mp.latitude == pytest.approx(4480454.96970565)

    def test_minimal_sensor(self):
        sensors, _ = parse_pm_xml(SAMPLE_PM_XML_MINIMAL)
        mp = build_measurement_point(sensors[0])
        assert mp.sensor_id == '1001'
        assert mp.description == 'Test road'
        assert mp.longitude is None
        assert mp.latitude is None
        assert mp.saturation_intensity == 500

    def test_element_type_absent(self):
        sensors, _ = parse_pm_xml(SAMPLE_PM_XML)
        mp = build_measurement_point(sensors[0])
        assert mp.element_type is None

    def test_empty_sensor_dict(self):
        mp = build_measurement_point({})
        assert mp.sensor_id == ''
        assert mp.description == ''


@pytest.mark.unit
class TestBuildTrafficReading:
    """Tests for building TrafficReading from raw sensor dict."""

    def test_full_reading(self):
        sensors, _ = parse_pm_xml(SAMPLE_PM_XML)
        ts = datetime.datetime(2024, 6, 15, 14, 30, 0, tzinfo=datetime.timezone.utc)
        reading = build_traffic_reading(sensors[0], ts)
        assert reading.sensor_id == '9841'
        assert reading.intensity == 120
        assert reading.occupancy == 15
        assert reading.load == 4
        assert reading.service_level == 0
        assert reading.error_flag == 'N'
        assert reading.timestamp == ts

    def test_error_sensor_reading(self):
        sensors, _ = parse_pm_xml(SAMPLE_PM_XML)
        ts = datetime.datetime(2024, 6, 15, 14, 30, 0, tzinfo=datetime.timezone.utc)
        reading = build_traffic_reading(sensors[2], ts)
        assert reading.sensor_id == '5555'
        assert reading.error_flag == 'S'

    def test_minimal_reading(self):
        sensors, _ = parse_pm_xml(SAMPLE_PM_XML_MINIMAL)
        ts = datetime.datetime(2024, 6, 15, 14, 30, 0, tzinfo=datetime.timezone.utc)
        reading = build_traffic_reading(sensors[0], ts)
        assert reading.sensor_id == '1001'
        assert reading.intensity == 50
        assert reading.occupancy == 10
        assert reading.load == 2
        assert reading.service_level == 1

    def test_empty_sensor_reading(self):
        ts = datetime.datetime(2024, 6, 15, 14, 30, 0, tzinfo=datetime.timezone.utc)
        reading = build_traffic_reading({}, ts)
        assert reading.sensor_id == ''
        assert reading.intensity is None
        assert reading.occupancy is None


@pytest.mark.unit
class TestParseConnectionString:
    """Tests for connection string parsing."""

    def test_plain_kafka(self):
        cs = "BootstrapServer=broker:9092;EntityPath=my-topic"
        result = parse_connection_string(cs)
        assert result['bootstrap.servers'] == 'broker:9092'
        assert result['kafka_topic'] == 'my-topic'
        assert 'sasl.username' not in result

    def test_event_hubs(self):
        cs = "Endpoint=sb://ns.servicebus.windows.net/;SharedAccessKeyName=send;SharedAccessKey=KEY123;EntityPath=madrid"
        result = parse_connection_string(cs)
        assert 'bootstrap.servers' in result
        assert result['kafka_topic'] == 'madrid'
        assert result['sasl.username'] == '$ConnectionString'
        assert result['security.protocol'] == 'SASL_SSL'

    def test_empty_string_raises(self):
        result = parse_connection_string("")
        assert 'bootstrap.servers' not in result


@pytest.mark.unit
class TestMadridTrafficPollerInit:
    """Tests for MadridTrafficPoller initialization."""

    @patch('madrid_traffic.madrid_traffic.EsMadridInformoEventProducer')
    @patch('confluent_kafka.Producer')
    def test_init(self, mock_producer_class, mock_event_producer):
        mock_kafka_producer = Mock()
        mock_producer_class.return_value = mock_kafka_producer

        poller = MadridTrafficPoller(
            kafka_config={'bootstrap.servers': 'localhost:9092'},
            kafka_topic='test-topic',
        )

        assert poller.kafka_topic == 'test-topic'
        mock_producer_class.assert_called_once_with({'bootstrap.servers': 'localhost:9092'})
        mock_event_producer.assert_called_once_with(mock_kafka_producer, 'test-topic')


@pytest.mark.unit
class TestMadridTrafficPollerParsing:
    """Tests for MadridTrafficPoller XML parsing and event emission."""

    @patch('madrid_traffic.madrid_traffic.EsMadridInformoEventProducer')
    @patch('confluent_kafka.Producer')
    def test_emit_reference_data(self, mock_producer_class, mock_event_producer_class):
        mock_kafka_producer = Mock()
        mock_producer_class.return_value = mock_kafka_producer
        mock_event_producer = Mock()
        mock_event_producer.producer = mock_kafka_producer
        mock_event_producer_class.return_value = mock_event_producer

        poller = MadridTrafficPoller(
            kafka_config={'bootstrap.servers': 'localhost:9092'},
            kafka_topic='test-topic',
        )

        sensors, _ = parse_pm_xml(SAMPLE_PM_XML)
        count = poller.emit_reference_data(sensors)
        assert count == 3
        assert mock_event_producer.send_es_madrid_informo_measurement_point.call_count == 3
        mock_kafka_producer.flush.assert_called_once()

    @patch('madrid_traffic.madrid_traffic.EsMadridInformoEventProducer')
    @patch('confluent_kafka.Producer')
    def test_emit_traffic_readings_skips_errors(self, mock_producer_class, mock_event_producer_class):
        mock_kafka_producer = Mock()
        mock_producer_class.return_value = mock_kafka_producer
        mock_event_producer = Mock()
        mock_event_producer.producer = mock_kafka_producer
        mock_event_producer_class.return_value = mock_event_producer

        poller = MadridTrafficPoller(
            kafka_config={'bootstrap.servers': 'localhost:9092'},
            kafka_topic='test-topic',
        )

        sensors, _ = parse_pm_xml(SAMPLE_PM_XML)
        poll_time = datetime.datetime(2024, 6, 15, 14, 32, 0, tzinfo=datetime.timezone.utc)
        count = poller.emit_traffic_readings(sensors, poll_time)
        # 3 sensors total, but sensor 5555 has error=S, so only 2
        assert count == 2
        assert mock_event_producer.send_es_madrid_informo_traffic_reading.call_count == 2

    @patch('madrid_traffic.madrid_traffic.EsMadridInformoEventProducer')
    @patch('confluent_kafka.Producer')
    def test_dedup_same_timestamp(self, mock_producer_class, mock_event_producer_class):
        mock_kafka_producer = Mock()
        mock_producer_class.return_value = mock_kafka_producer
        mock_event_producer = Mock()
        mock_event_producer.producer = mock_kafka_producer
        mock_event_producer_class.return_value = mock_event_producer

        poller = MadridTrafficPoller(
            kafka_config={'bootstrap.servers': 'localhost:9092'},
            kafka_topic='test-topic',
        )

        sensors, _ = parse_pm_xml(SAMPLE_PM_XML)
        poll_time = datetime.datetime(2024, 6, 15, 14, 32, 0, tzinfo=datetime.timezone.utc)

        count1 = poller.emit_traffic_readings(sensors, poll_time)
        assert count1 == 2

        # Same 5-min window, should be deduped
        poll_time2 = datetime.datetime(2024, 6, 15, 14, 33, 0, tzinfo=datetime.timezone.utc)
        count2 = poller.emit_traffic_readings(sensors, poll_time2)
        assert count2 == 0

    @patch('madrid_traffic.madrid_traffic.EsMadridInformoEventProducer')
    @patch('confluent_kafka.Producer')
    def test_new_timestamp_not_deduped(self, mock_producer_class, mock_event_producer_class):
        mock_kafka_producer = Mock()
        mock_producer_class.return_value = mock_kafka_producer
        mock_event_producer = Mock()
        mock_event_producer.producer = mock_kafka_producer
        mock_event_producer_class.return_value = mock_event_producer

        poller = MadridTrafficPoller(
            kafka_config={'bootstrap.servers': 'localhost:9092'},
            kafka_topic='test-topic',
        )

        sensors, _ = parse_pm_xml(SAMPLE_PM_XML)
        poll_time1 = datetime.datetime(2024, 6, 15, 14, 32, 0, tzinfo=datetime.timezone.utc)
        count1 = poller.emit_traffic_readings(sensors, poll_time1)
        assert count1 == 2

        # Different 5-min window
        poll_time2 = datetime.datetime(2024, 6, 15, 14, 37, 0, tzinfo=datetime.timezone.utc)
        count2 = poller.emit_traffic_readings(sensors, poll_time2)
        assert count2 == 2

    @patch('madrid_traffic.madrid_traffic.EsMadridInformoEventProducer')
    @patch('confluent_kafka.Producer')
    def test_emit_empty_sensors(self, mock_producer_class, mock_event_producer_class):
        mock_kafka_producer = Mock()
        mock_producer_class.return_value = mock_kafka_producer
        mock_event_producer = Mock()
        mock_event_producer.producer = mock_kafka_producer
        mock_event_producer_class.return_value = mock_event_producer

        poller = MadridTrafficPoller(
            kafka_config={'bootstrap.servers': 'localhost:9092'},
            kafka_topic='test-topic',
        )

        count = poller.emit_reference_data([])
        assert count == 0

    @patch('madrid_traffic.madrid_traffic.EsMadridInformoEventProducer')
    @patch('confluent_kafka.Producer')
    def test_emit_readings_empty_sensors(self, mock_producer_class, mock_event_producer_class):
        mock_kafka_producer = Mock()
        mock_producer_class.return_value = mock_kafka_producer
        mock_event_producer = Mock()
        mock_event_producer.producer = mock_kafka_producer
        mock_event_producer_class.return_value = mock_event_producer

        poller = MadridTrafficPoller(
            kafka_config={'bootstrap.servers': 'localhost:9092'},
            kafka_topic='test-topic',
        )

        poll_time = datetime.datetime(2024, 6, 15, 14, 30, 0, tzinfo=datetime.timezone.utc)
        count = poller.emit_traffic_readings([], poll_time)
        assert count == 0


@pytest.mark.unit
class TestMadridTrafficPollerPollAndSend:
    """Tests for the poll_and_send main loop."""

    @patch('madrid_traffic.madrid_traffic.EsMadridInformoEventProducer')
    @patch('confluent_kafka.Producer')
    @patch('madrid_traffic.madrid_traffic.requests.get')
    def test_poll_and_send_once(self, mock_get, mock_producer_class, mock_event_producer_class):
        mock_response = Mock()
        mock_response.text = SAMPLE_PM_XML
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        mock_kafka_producer = Mock()
        mock_producer_class.return_value = mock_kafka_producer
        mock_event_producer = Mock()
        mock_event_producer.producer = mock_kafka_producer
        mock_event_producer_class.return_value = mock_event_producer

        poller = MadridTrafficPoller(
            kafka_config={'bootstrap.servers': 'localhost:9092'},
            kafka_topic='test-topic',
        )
        poller.poll_and_send(once=True)

        # Should have emitted reference data + traffic readings
        assert mock_event_producer.send_es_madrid_informo_measurement_point.call_count == 3
        assert mock_event_producer.send_es_madrid_informo_traffic_reading.call_count == 2

    @patch('madrid_traffic.madrid_traffic.EsMadridInformoEventProducer')
    @patch('confluent_kafka.Producer')
    @patch('madrid_traffic.madrid_traffic.requests.get')
    def test_poll_and_send_handles_fetch_error(self, mock_get, mock_producer_class, mock_event_producer_class):
        mock_get.side_effect = Exception("Network error")

        mock_kafka_producer = Mock()
        mock_producer_class.return_value = mock_kafka_producer
        mock_event_producer = Mock()
        mock_event_producer.producer = mock_kafka_producer
        mock_event_producer_class.return_value = mock_event_producer

        poller = MadridTrafficPoller(
            kafka_config={'bootstrap.servers': 'localhost:9092'},
            kafka_topic='test-topic',
        )
        # Should not raise
        poller.poll_and_send(once=True)

        assert mock_event_producer.send_es_madrid_informo_measurement_point.call_count == 0
        assert mock_event_producer.send_es_madrid_informo_traffic_reading.call_count == 0


@pytest.mark.unit
class TestMadridTrafficPollerFetchXml:
    """Tests for fetch_xml method."""

    @patch('madrid_traffic.madrid_traffic.EsMadridInformoEventProducer')
    @patch('confluent_kafka.Producer')
    @patch('madrid_traffic.madrid_traffic.requests.get')
    def test_fetch_xml_success(self, mock_get, mock_producer_class, mock_event_producer_class):
        mock_response = Mock()
        mock_response.text = SAMPLE_PM_XML
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        mock_kafka_producer = Mock()
        mock_producer_class.return_value = mock_kafka_producer
        mock_event_producer_class.return_value = Mock(producer=mock_kafka_producer)

        poller = MadridTrafficPoller(
            kafka_config={'bootstrap.servers': 'localhost:9092'},
            kafka_topic='test-topic',
        )
        result = poller.fetch_xml()
        assert result == SAMPLE_PM_XML

    @patch('madrid_traffic.madrid_traffic.EsMadridInformoEventProducer')
    @patch('confluent_kafka.Producer')
    @patch('madrid_traffic.madrid_traffic.requests.get')
    def test_fetch_xml_failure(self, mock_get, mock_producer_class, mock_event_producer_class):
        mock_get.side_effect = Exception("Connection error")

        mock_kafka_producer = Mock()
        mock_producer_class.return_value = mock_kafka_producer
        mock_event_producer_class.return_value = Mock(producer=mock_kafka_producer)

        poller = MadridTrafficPoller(
            kafka_config={'bootstrap.servers': 'localhost:9092'},
            kafka_topic='test-topic',
        )
        result = poller.fetch_xml()
        assert result is None


@pytest.mark.unit
class TestDataclassSerialization:
    """Tests for data class serialization."""

    def test_measurement_point_to_json(self):
        mp = MeasurementPoint(
            sensor_id='9841',
            description='Test road segment',
            element_type='URB',
            subarea='0328',
            longitude=-3.703790,
            latitude=40.416775,
            saturation_intensity=3100,
        )
        json_str = mp.to_json()
        assert '9841' in json_str
        assert 'Test road segment' in json_str

    def test_traffic_reading_to_json(self):
        ts = datetime.datetime(2024, 6, 15, 14, 30, 0, tzinfo=datetime.timezone.utc)
        reading = TrafficReading(
            sensor_id='9841',
            intensity=120,
            occupancy=15,
            load=4,
            service_level=0,
            error_flag='N',
            timestamp=ts,
        )
        json_str = reading.to_json()
        assert '9841' in json_str
        assert '120' in json_str

    def test_measurement_point_nullable_fields(self):
        mp = MeasurementPoint(
            sensor_id='9841',
            description='Test',
            element_type=None,
            subarea=None,
            longitude=None,
            latitude=None,
            saturation_intensity=None,
        )
        json_str = mp.to_json()
        assert '9841' in json_str

    def test_traffic_reading_nullable_fields(self):
        ts = datetime.datetime(2024, 6, 15, 14, 30, 0, tzinfo=datetime.timezone.utc)
        reading = TrafficReading(
            sensor_id='9841',
            intensity=None,
            occupancy=None,
            load=None,
            service_level=None,
            error_flag=None,
            timestamp=ts,
        )
        json_str = reading.to_json()
        assert '9841' in json_str

    def test_measurement_point_from_dict(self):
        data = {
            'sensor_id': '9841',
            'description': 'Test',
            'element_type': 'URB',
            'subarea': '0328',
            'longitude': -3.703,
            'latitude': 40.416,
            'saturation_intensity': 3100,
        }
        mp = MeasurementPoint.from_serializer_dict(data)
        assert mp.sensor_id == '9841'
        assert mp.saturation_intensity == 3100

    def test_traffic_reading_create_instance(self):
        reading = TrafficReading.create_instance()
        assert reading.sensor_id is not None
        assert isinstance(reading.timestamp, datetime.datetime)


@pytest.mark.unit
class TestReferenceDataRefresh:
    """Tests for reference data refresh timing."""

    @patch('madrid_traffic.madrid_traffic.EsMadridInformoEventProducer')
    @patch('confluent_kafka.Producer')
    def test_reference_sent_on_first_call(self, mock_producer_class, mock_event_producer_class):
        mock_kafka_producer = Mock()
        mock_producer_class.return_value = mock_kafka_producer
        mock_event_producer = Mock()
        mock_event_producer.producer = mock_kafka_producer
        mock_event_producer_class.return_value = mock_event_producer

        poller = MadridTrafficPoller(
            kafka_config={'bootstrap.servers': 'localhost:9092'},
            kafka_topic='test-topic',
        )
        assert poller._last_reference_time == 0.0


@pytest.mark.unit
class TestXmlEdgeCases:
    """Tests for XML edge cases."""

    def test_sensor_with_empty_fields(self):
        xml = """\
<?xml version="1.0" encoding="UTF-8"?>
<pms>
  <pm>
    <idelem>1</idelem>
    <descripcion></descripcion>
    <intensidad></intensidad>
    <ocupacion></ocupacion>
    <carga></carga>
    <nivelServicio></nivelServicio>
    <intensidadSat></intensidadSat>
    <error></error>
    <subarea></subarea>
    <st_x></st_x>
    <st_y></st_y>
  </pm>
</pms>
"""
        sensors, _ = parse_pm_xml(xml)
        assert len(sensors) == 1
        mp = build_measurement_point(sensors[0])
        assert mp.sensor_id == '1'
        assert mp.longitude is None
        assert mp.latitude is None
        assert mp.saturation_intensity is None

    def test_malformed_xml_raises(self):
        with pytest.raises(ET.ParseError):
            parse_pm_xml("<not valid xml")

    def test_all_error_sensors_yield_zero_readings(self):
        xml = """\
<?xml version="1.0" encoding="UTF-8"?>
<pms>
  <pm>
    <idelem>1</idelem>
    <descripcion>A</descripcion>
    <intensidad>10</intensidad>
    <ocupacion>5</ocupacion>
    <carga>1</carga>
    <nivelServicio>0</nivelServicio>
    <intensidadSat>100</intensidadSat>
    <error>S</error>
  </pm>
  <pm>
    <idelem>2</idelem>
    <descripcion>B</descripcion>
    <intensidad>20</intensidad>
    <ocupacion>10</ocupacion>
    <carga>2</carga>
    <nivelServicio>1</nivelServicio>
    <intensidadSat>200</intensidadSat>
    <error>Y</error>
  </pm>
</pms>
"""
        sensors, _ = parse_pm_xml(xml)
        assert len(sensors) == 2
        # Both have errors
        ts = datetime.datetime(2024, 6, 15, 14, 30, 0, tzinfo=datetime.timezone.utc)
        for s in sensors:
            reading = build_traffic_reading(s, ts)
            assert reading.error_flag in ('S', 'Y')
