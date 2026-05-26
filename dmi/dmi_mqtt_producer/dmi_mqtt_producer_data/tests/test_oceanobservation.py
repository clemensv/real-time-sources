"""
Test case for OceanObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from dmi_mqtt_producer_data.oceanobservation import OceanObservation
from dmi_mqtt_producer_data.parameteridenum import ParameterIdenum
import datetime


class Test_OceanObservation(unittest.TestCase):
    """
    Test case for OceanObservation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_OceanObservation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of OceanObservation for testing
        """
        instance = OceanObservation(
            observation_id='aubxwfahdltatiizfrhe',
            station_id='gfghoozajgfrcjbnzxyp',
            parameter_id=ParameterIdenum.temp_dry,
            observed=datetime.datetime.now(datetime.timezone.utc),
            value=float(92.14648234335634),
            latitude=float(46.224642991662776),
            longitude=float(83.14122939491428)
        )
        return instance

    
    def test_observation_id_property(self):
        """
        Test observation_id property
        """
        test_value = 'aubxwfahdltatiizfrhe'
        self.instance.observation_id = test_value
        self.assertEqual(self.instance.observation_id, test_value)
    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'gfghoozajgfrcjbnzxyp'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_parameter_id_property(self):
        """
        Test parameter_id property
        """
        test_value = ParameterIdenum.temp_dry
        self.instance.parameter_id = test_value
        self.assertEqual(self.instance.parameter_id, test_value)
    
    def test_observed_property(self):
        """
        Test observed property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.observed = test_value
        self.assertEqual(self.instance.observed, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(92.14648234335634)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(46.224642991662776)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(83.14122939491428)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = OceanObservation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = OceanObservation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

