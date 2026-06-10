"""
Test case for TollRate
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from wsdot_mqtt_producer_data.us.wa.wsdot.tolls.tollrate import TollRate


class Test_TollRate(unittest.TestCase):
    """
    Test case for TollRate
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_TollRate.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of TollRate for testing
        """
        instance = TollRate(
            trip_name='pqmkudassaoodrlplabp',
            state_route='lpmqcchjuiqbmoycycnu',
            travel_direction='qdancmctylvuqkqrtqjq',
            current_toll=int(53),
            current_message='vlucyzywvsdcbtdnbxwz',
            time_updated='qaozmhcdkeonetjrnkgf',
            start_location_name='jpjzagceizkafimhwskz',
            start_latitude=float(82.72430682223725),
            start_longitude=float(29.84008784454131),
            start_milepost=float(17.371005647374105),
            end_location_name='ghodujnltrsankchzcxw',
            end_latitude=float(83.96356891628135),
            end_longitude=float(44.77687236643047),
            end_milepost=float(27.4602198422089)
        )
        return instance

    
    def test_trip_name_property(self):
        """
        Test trip_name property
        """
        test_value = 'pqmkudassaoodrlplabp'
        self.instance.trip_name = test_value
        self.assertEqual(self.instance.trip_name, test_value)
    
    def test_state_route_property(self):
        """
        Test state_route property
        """
        test_value = 'lpmqcchjuiqbmoycycnu'
        self.instance.state_route = test_value
        self.assertEqual(self.instance.state_route, test_value)
    
    def test_travel_direction_property(self):
        """
        Test travel_direction property
        """
        test_value = 'qdancmctylvuqkqrtqjq'
        self.instance.travel_direction = test_value
        self.assertEqual(self.instance.travel_direction, test_value)
    
    def test_current_toll_property(self):
        """
        Test current_toll property
        """
        test_value = int(53)
        self.instance.current_toll = test_value
        self.assertEqual(self.instance.current_toll, test_value)
    
    def test_current_message_property(self):
        """
        Test current_message property
        """
        test_value = 'vlucyzywvsdcbtdnbxwz'
        self.instance.current_message = test_value
        self.assertEqual(self.instance.current_message, test_value)
    
    def test_time_updated_property(self):
        """
        Test time_updated property
        """
        test_value = 'qaozmhcdkeonetjrnkgf'
        self.instance.time_updated = test_value
        self.assertEqual(self.instance.time_updated, test_value)
    
    def test_start_location_name_property(self):
        """
        Test start_location_name property
        """
        test_value = 'jpjzagceizkafimhwskz'
        self.instance.start_location_name = test_value
        self.assertEqual(self.instance.start_location_name, test_value)
    
    def test_start_latitude_property(self):
        """
        Test start_latitude property
        """
        test_value = float(82.72430682223725)
        self.instance.start_latitude = test_value
        self.assertEqual(self.instance.start_latitude, test_value)
    
    def test_start_longitude_property(self):
        """
        Test start_longitude property
        """
        test_value = float(29.84008784454131)
        self.instance.start_longitude = test_value
        self.assertEqual(self.instance.start_longitude, test_value)
    
    def test_start_milepost_property(self):
        """
        Test start_milepost property
        """
        test_value = float(17.371005647374105)
        self.instance.start_milepost = test_value
        self.assertEqual(self.instance.start_milepost, test_value)
    
    def test_end_location_name_property(self):
        """
        Test end_location_name property
        """
        test_value = 'ghodujnltrsankchzcxw'
        self.instance.end_location_name = test_value
        self.assertEqual(self.instance.end_location_name, test_value)
    
    def test_end_latitude_property(self):
        """
        Test end_latitude property
        """
        test_value = float(83.96356891628135)
        self.instance.end_latitude = test_value
        self.assertEqual(self.instance.end_latitude, test_value)
    
    def test_end_longitude_property(self):
        """
        Test end_longitude property
        """
        test_value = float(44.77687236643047)
        self.instance.end_longitude = test_value
        self.assertEqual(self.instance.end_longitude, test_value)
    
    def test_end_milepost_property(self):
        """
        Test end_milepost property
        """
        test_value = float(27.4602198422089)
        self.instance.end_milepost = test_value
        self.assertEqual(self.instance.end_milepost, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = TollRate.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = TollRate.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

