"""
Test case for TrafficMeasurement
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from datex2_mqtt_producer_data.org.datex2.measured.trafficmeasurement import TrafficMeasurement
import datetime


class Test_TrafficMeasurement(unittest.TestCase):
    """
    Test case for TrafficMeasurement
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_TrafficMeasurement.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of TrafficMeasurement for testing
        """
        instance = TrafficMeasurement(
            supplier_id='trcsjivnpwkpqejbxayv',
            measurement_site_id='gmvaoxgclwjqdapfmkan',
            feed_url='cywoxfuqmiprzwajygvd',
            measurement_time=datetime.datetime.now(datetime.timezone.utc),
            measurement_time_key='vhspyncybkswygahfefx',
            country_code='ooguogtkqbhmneladtyn',
            operator_id='jxgntcvslqwihwqrstrr',
            road_number='lronbkyvpgkhcyhyefhz',
            average_speed_kmh=float(70.24368566463632),
            vehicle_flow_rate_veh_per_hour=int(37),
            occupancy_percent=float(50.04547336417756),
            travel_time_seconds=float(76.98477141481523),
            free_flow_travel_time_seconds=float(65.9849349808241),
            input_value_count=int(71),
            quality_status='imccpheifaszfwfjnixe',
            vehicle_type='tfqtjagkztbvkfslhbud',
            lane='gykgjbbzwlxkiodaggjf',
            raw_measurements='ebzmpkfjdopdprhikvpk'
        )
        return instance

    
    def test_supplier_id_property(self):
        """
        Test supplier_id property
        """
        test_value = 'trcsjivnpwkpqejbxayv'
        self.instance.supplier_id = test_value
        self.assertEqual(self.instance.supplier_id, test_value)
    
    def test_measurement_site_id_property(self):
        """
        Test measurement_site_id property
        """
        test_value = 'gmvaoxgclwjqdapfmkan'
        self.instance.measurement_site_id = test_value
        self.assertEqual(self.instance.measurement_site_id, test_value)
    
    def test_feed_url_property(self):
        """
        Test feed_url property
        """
        test_value = 'cywoxfuqmiprzwajygvd'
        self.instance.feed_url = test_value
        self.assertEqual(self.instance.feed_url, test_value)
    
    def test_measurement_time_property(self):
        """
        Test measurement_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.measurement_time = test_value
        self.assertEqual(self.instance.measurement_time, test_value)
    
    def test_measurement_time_key_property(self):
        """
        Test measurement_time_key property
        """
        test_value = 'vhspyncybkswygahfefx'
        self.instance.measurement_time_key = test_value
        self.assertEqual(self.instance.measurement_time_key, test_value)
    
    def test_country_code_property(self):
        """
        Test country_code property
        """
        test_value = 'ooguogtkqbhmneladtyn'
        self.instance.country_code = test_value
        self.assertEqual(self.instance.country_code, test_value)
    
    def test_operator_id_property(self):
        """
        Test operator_id property
        """
        test_value = 'jxgntcvslqwihwqrstrr'
        self.instance.operator_id = test_value
        self.assertEqual(self.instance.operator_id, test_value)
    
    def test_road_number_property(self):
        """
        Test road_number property
        """
        test_value = 'lronbkyvpgkhcyhyefhz'
        self.instance.road_number = test_value
        self.assertEqual(self.instance.road_number, test_value)
    
    def test_average_speed_kmh_property(self):
        """
        Test average_speed_kmh property
        """
        test_value = float(70.24368566463632)
        self.instance.average_speed_kmh = test_value
        self.assertEqual(self.instance.average_speed_kmh, test_value)
    
    def test_vehicle_flow_rate_veh_per_hour_property(self):
        """
        Test vehicle_flow_rate_veh_per_hour property
        """
        test_value = int(37)
        self.instance.vehicle_flow_rate_veh_per_hour = test_value
        self.assertEqual(self.instance.vehicle_flow_rate_veh_per_hour, test_value)
    
    def test_occupancy_percent_property(self):
        """
        Test occupancy_percent property
        """
        test_value = float(50.04547336417756)
        self.instance.occupancy_percent = test_value
        self.assertEqual(self.instance.occupancy_percent, test_value)
    
    def test_travel_time_seconds_property(self):
        """
        Test travel_time_seconds property
        """
        test_value = float(76.98477141481523)
        self.instance.travel_time_seconds = test_value
        self.assertEqual(self.instance.travel_time_seconds, test_value)
    
    def test_free_flow_travel_time_seconds_property(self):
        """
        Test free_flow_travel_time_seconds property
        """
        test_value = float(65.9849349808241)
        self.instance.free_flow_travel_time_seconds = test_value
        self.assertEqual(self.instance.free_flow_travel_time_seconds, test_value)
    
    def test_input_value_count_property(self):
        """
        Test input_value_count property
        """
        test_value = int(71)
        self.instance.input_value_count = test_value
        self.assertEqual(self.instance.input_value_count, test_value)
    
    def test_quality_status_property(self):
        """
        Test quality_status property
        """
        test_value = 'imccpheifaszfwfjnixe'
        self.instance.quality_status = test_value
        self.assertEqual(self.instance.quality_status, test_value)
    
    def test_vehicle_type_property(self):
        """
        Test vehicle_type property
        """
        test_value = 'tfqtjagkztbvkfslhbud'
        self.instance.vehicle_type = test_value
        self.assertEqual(self.instance.vehicle_type, test_value)
    
    def test_lane_property(self):
        """
        Test lane property
        """
        test_value = 'gykgjbbzwlxkiodaggjf'
        self.instance.lane = test_value
        self.assertEqual(self.instance.lane, test_value)
    
    def test_raw_measurements_property(self):
        """
        Test raw_measurements property
        """
        test_value = 'ebzmpkfjdopdprhikvpk'
        self.instance.raw_measurements = test_value
        self.assertEqual(self.instance.raw_measurements, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = TrafficMeasurement.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = TrafficMeasurement.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

