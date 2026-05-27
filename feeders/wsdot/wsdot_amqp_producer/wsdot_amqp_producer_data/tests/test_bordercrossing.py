"""
Test case for BorderCrossing
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from wsdot_amqp_producer_data.us.wa.wsdot.border.bordercrossing import BorderCrossing


class Test_BorderCrossing(unittest.TestCase):
    """
    Test case for BorderCrossing
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_BorderCrossing.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of BorderCrossing for testing
        """
        instance = BorderCrossing(
            crossing_name='xtjmaxxvcchshragzunz',
            wait_time=int(48),
            time='bnzfgmadddjdidsmmgyz',
            description='qqgtusqbfhpoiyqogxkq',
            road_name='gslvelvejpgxnchaqxyl',
            latitude=float(38.174256164998646),
            longitude=float(40.07124523288338)
        )
        return instance

    
    def test_crossing_name_property(self):
        """
        Test crossing_name property
        """
        test_value = 'xtjmaxxvcchshragzunz'
        self.instance.crossing_name = test_value
        self.assertEqual(self.instance.crossing_name, test_value)
    
    def test_wait_time_property(self):
        """
        Test wait_time property
        """
        test_value = int(48)
        self.instance.wait_time = test_value
        self.assertEqual(self.instance.wait_time, test_value)
    
    def test_time_property(self):
        """
        Test time property
        """
        test_value = 'bnzfgmadddjdidsmmgyz'
        self.instance.time = test_value
        self.assertEqual(self.instance.time, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'qqgtusqbfhpoiyqogxkq'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_road_name_property(self):
        """
        Test road_name property
        """
        test_value = 'gslvelvejpgxnchaqxyl'
        self.instance.road_name = test_value
        self.assertEqual(self.instance.road_name, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(38.174256164998646)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(40.07124523288338)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = BorderCrossing.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = BorderCrossing.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

