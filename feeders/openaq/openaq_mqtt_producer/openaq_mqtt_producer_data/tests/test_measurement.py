"""
Test case for Measurement
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from openaq_mqtt_producer_data.org.openaq.measurement import Measurement
from openaq_mqtt_producer_data.org.openaq.parameternameenum import ParameterNameenum
import datetime


class Test_Measurement(unittest.TestCase):
    """
    Test case for Measurement
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Measurement.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Measurement for testing
        """
        instance = Measurement(
            location_id=int(59),
            sensor_id=int(55),
            country_iso='znhcinstqnieidhnbsru',
            parameter_id=int(82),
            parameter_name=ParameterNameenum.pm25,
            parameter_units='xuqvbwmwngayhqwqkxxi',
            datetime=datetime.datetime.now(datetime.timezone.utc),
            value=float(65.75311208782804),
            latitude=float(78.33660223972045),
            longitude=float(38.63528446704172),
            is_valid=True,
            has_flags=True,
            poll_time=datetime.datetime.now(datetime.timezone.utc)
        )
        return instance

    
    def test_location_id_property(self):
        """
        Test location_id property
        """
        test_value = int(59)
        self.instance.location_id = test_value
        self.assertEqual(self.instance.location_id, test_value)
    
    def test_sensor_id_property(self):
        """
        Test sensor_id property
        """
        test_value = int(55)
        self.instance.sensor_id = test_value
        self.assertEqual(self.instance.sensor_id, test_value)
    
    def test_country_iso_property(self):
        """
        Test country_iso property
        """
        test_value = 'znhcinstqnieidhnbsru'
        self.instance.country_iso = test_value
        self.assertEqual(self.instance.country_iso, test_value)
    
    def test_parameter_id_property(self):
        """
        Test parameter_id property
        """
        test_value = int(82)
        self.instance.parameter_id = test_value
        self.assertEqual(self.instance.parameter_id, test_value)
    
    def test_parameter_name_property(self):
        """
        Test parameter_name property
        """
        test_value = ParameterNameenum.pm25
        self.instance.parameter_name = test_value
        self.assertEqual(self.instance.parameter_name, test_value)
    
    def test_parameter_units_property(self):
        """
        Test parameter_units property
        """
        test_value = 'xuqvbwmwngayhqwqkxxi'
        self.instance.parameter_units = test_value
        self.assertEqual(self.instance.parameter_units, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(65.75311208782804)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(78.33660223972045)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(38.63528446704172)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_is_valid_property(self):
        """
        Test is_valid property
        """
        test_value = True
        self.instance.is_valid = test_value
        self.assertEqual(self.instance.is_valid, test_value)
    
    def test_has_flags_property(self):
        """
        Test has_flags property
        """
        test_value = True
        self.instance.has_flags = test_value
        self.assertEqual(self.instance.has_flags, test_value)
    
    def test_poll_time_property(self):
        """
        Test poll_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.poll_time = test_value
        self.assertEqual(self.instance.poll_time, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Measurement.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Measurement.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

