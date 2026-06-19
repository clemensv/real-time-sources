"""
Test case for MsiSign
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ndw_road_traffic_producer_data.msisign import MsiSign


class Test_MsiSign(unittest.TestCase):
    """
    Test case for MsiSign
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_MsiSign.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of MsiSign for testing
        """
        instance = MsiSign(
            sign_id='ebvhvhgonhexyronjxff',
            sign_type='rwuwsjtrovtmzbuzgzcb',
            latitude=float(65.08074592231623),
            longitude=float(73.75503835421576),
            road_name='vwtlngnaacwegobbfzxa',
            lane='burqcmdzirccxydptstm',
            description='dxeztoqpamxyaisgvabu'
        )
        return instance

    
    def test_sign_id_property(self):
        """
        Test sign_id property
        """
        test_value = 'ebvhvhgonhexyronjxff'
        self.instance.sign_id = test_value
        self.assertEqual(self.instance.sign_id, test_value)
    
    def test_sign_type_property(self):
        """
        Test sign_type property
        """
        test_value = 'rwuwsjtrovtmzbuzgzcb'
        self.instance.sign_type = test_value
        self.assertEqual(self.instance.sign_type, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(65.08074592231623)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(73.75503835421576)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_road_name_property(self):
        """
        Test road_name property
        """
        test_value = 'vwtlngnaacwegobbfzxa'
        self.instance.road_name = test_value
        self.assertEqual(self.instance.road_name, test_value)
    
    def test_lane_property(self):
        """
        Test lane property
        """
        test_value = 'burqcmdzirccxydptstm'
        self.instance.lane = test_value
        self.assertEqual(self.instance.lane, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'dxeztoqpamxyaisgvabu'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = MsiSign.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = MsiSign.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

