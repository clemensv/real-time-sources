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
            supplier_id='kzwmdfzpnxlcgudnoztf',
            measurement_site_id='mdwsjaegksjjpyjthzbv',
            feed_url='dfaoilszdgudwmcpvszj',
            measurement_time=datetime.datetime.now(datetime.timezone.utc),
            measurement_time_key='odzgrmlubauctqgdiyaa',
            country_code='crpybedykfkbrhfhuhsm',
            operator_id='tuvvaowcczqzgbeygsoh',
            road_number='paacuqlylwdjfhkswrbm',
            average_speed_kmh=float(60.976125651549594),
            vehicle_flow_rate_veh_per_hour=int(74),
            occupancy_percent=float(62.43710267093948),
            travel_time_seconds=float(21.6081862953711),
            free_flow_travel_time_seconds=float(47.31038594093624),
            input_value_count=int(47),
            quality_status='yxjgsyhdfevxilfjlvxv',
            vehicle_type='evnfuwkfakyzwxxqtjyr',
            lane='lnxpbblkmafltfwwmlvz',
            raw_measurements='dndngzrgeblrwjumrrmm'
        )
        return instance

    
    def test_supplier_id_property(self):
        """
        Test supplier_id property
        """
        test_value = 'kzwmdfzpnxlcgudnoztf'
        self.instance.supplier_id = test_value
        self.assertEqual(self.instance.supplier_id, test_value)
    
    def test_measurement_site_id_property(self):
        """
        Test measurement_site_id property
        """
        test_value = 'mdwsjaegksjjpyjthzbv'
        self.instance.measurement_site_id = test_value
        self.assertEqual(self.instance.measurement_site_id, test_value)
    
    def test_feed_url_property(self):
        """
        Test feed_url property
        """
        test_value = 'dfaoilszdgudwmcpvszj'
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
        test_value = 'odzgrmlubauctqgdiyaa'
        self.instance.measurement_time_key = test_value
        self.assertEqual(self.instance.measurement_time_key, test_value)
    
    def test_country_code_property(self):
        """
        Test country_code property
        """
        test_value = 'crpybedykfkbrhfhuhsm'
        self.instance.country_code = test_value
        self.assertEqual(self.instance.country_code, test_value)
    
    def test_operator_id_property(self):
        """
        Test operator_id property
        """
        test_value = 'tuvvaowcczqzgbeygsoh'
        self.instance.operator_id = test_value
        self.assertEqual(self.instance.operator_id, test_value)
    
    def test_road_number_property(self):
        """
        Test road_number property
        """
        test_value = 'paacuqlylwdjfhkswrbm'
        self.instance.road_number = test_value
        self.assertEqual(self.instance.road_number, test_value)
    
    def test_average_speed_kmh_property(self):
        """
        Test average_speed_kmh property
        """
        test_value = float(60.976125651549594)
        self.instance.average_speed_kmh = test_value
        self.assertEqual(self.instance.average_speed_kmh, test_value)
    
    def test_vehicle_flow_rate_veh_per_hour_property(self):
        """
        Test vehicle_flow_rate_veh_per_hour property
        """
        test_value = int(74)
        self.instance.vehicle_flow_rate_veh_per_hour = test_value
        self.assertEqual(self.instance.vehicle_flow_rate_veh_per_hour, test_value)
    
    def test_occupancy_percent_property(self):
        """
        Test occupancy_percent property
        """
        test_value = float(62.43710267093948)
        self.instance.occupancy_percent = test_value
        self.assertEqual(self.instance.occupancy_percent, test_value)
    
    def test_travel_time_seconds_property(self):
        """
        Test travel_time_seconds property
        """
        test_value = float(21.6081862953711)
        self.instance.travel_time_seconds = test_value
        self.assertEqual(self.instance.travel_time_seconds, test_value)
    
    def test_free_flow_travel_time_seconds_property(self):
        """
        Test free_flow_travel_time_seconds property
        """
        test_value = float(47.31038594093624)
        self.instance.free_flow_travel_time_seconds = test_value
        self.assertEqual(self.instance.free_flow_travel_time_seconds, test_value)
    
    def test_input_value_count_property(self):
        """
        Test input_value_count property
        """
        test_value = int(47)
        self.instance.input_value_count = test_value
        self.assertEqual(self.instance.input_value_count, test_value)
    
    def test_quality_status_property(self):
        """
        Test quality_status property
        """
        test_value = 'yxjgsyhdfevxilfjlvxv'
        self.instance.quality_status = test_value
        self.assertEqual(self.instance.quality_status, test_value)
    
    def test_vehicle_type_property(self):
        """
        Test vehicle_type property
        """
        test_value = 'evnfuwkfakyzwxxqtjyr'
        self.instance.vehicle_type = test_value
        self.assertEqual(self.instance.vehicle_type, test_value)
    
    def test_lane_property(self):
        """
        Test lane property
        """
        test_value = 'lnxpbblkmafltfwwmlvz'
        self.instance.lane = test_value
        self.assertEqual(self.instance.lane, test_value)
    
    def test_raw_measurements_property(self):
        """
        Test raw_measurements property
        """
        test_value = 'dndngzrgeblrwjumrrmm'
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

