"""
Test case for Observation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from dmi_producer_data.observation import Observation


class Test_Observation(unittest.TestCase):
    """
    Test case for Observation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Observation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Observation for testing
        """
        instance = Observation(
            observation_id='cuaeiasxdtprjnoeyyzb',
            station_id='sdojrtcjiqdyvsugscyj',
            parameter_id='yfziuizgrudqfznhjtcf',
            observed='xrsrmkdjbjivzxjivdpw',
            value=float(26.71185335950653),
            latitude=float(24.38531949845698),
            longitude=float(6.185448908443414)
        )
        return instance

    
    def test_observation_id_property(self):
        """
        Test observation_id property
        """
        test_value = 'cuaeiasxdtprjnoeyyzb'
        self.instance.observation_id = test_value
        self.assertEqual(self.instance.observation_id, test_value)
    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'sdojrtcjiqdyvsugscyj'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_parameter_id_property(self):
        """
        Test parameter_id property
        """
        test_value = 'yfziuizgrudqfznhjtcf'
        self.instance.parameter_id = test_value
        self.assertEqual(self.instance.parameter_id, test_value)
    
    def test_observed_property(self):
        """
        Test observed property
        """
        test_value = 'xrsrmkdjbjivzxjivdpw'
        self.instance.observed = test_value
        self.assertEqual(self.instance.observed, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(26.71185335950653)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(24.38531949845698)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(6.185448908443414)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Observation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Observation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

