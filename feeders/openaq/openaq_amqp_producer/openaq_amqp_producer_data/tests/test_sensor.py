"""
Test case for Sensor
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from openaq_amqp_producer_data.org.openaq.sensor import Sensor
from openaq_amqp_producer_data.org.openaq.parameternameenum import ParameterNameenum
import datetime


class Test_Sensor(unittest.TestCase):
    """
    Test case for Sensor
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Sensor.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Sensor for testing
        """
        instance = Sensor(
            location_id=int(4),
            sensor_id=int(99),
            country_iso='pogfyhrtkwbuapgxyiqd',
            sensor_name='xebhzrrdaghpwkqinhfo',
            parameter_id=int(42),
            parameter_name=ParameterNameenum.pm25,
            parameter_units='bmnieptphnpeantzvplw',
            parameter_display_name='pszqlaotjkadnvfpavdz',
            datetime_first=datetime.datetime.now(datetime.timezone.utc),
            datetime_last=datetime.datetime.now(datetime.timezone.utc),
            latest_value=float(87.68356563633344),
            latest_datetime=datetime.datetime.now(datetime.timezone.utc),
            latitude=float(55.295359905018614),
            longitude=float(96.50512173801779)
        )
        return instance

    
    def test_location_id_property(self):
        """
        Test location_id property
        """
        test_value = int(4)
        self.instance.location_id = test_value
        self.assertEqual(self.instance.location_id, test_value)
    
    def test_sensor_id_property(self):
        """
        Test sensor_id property
        """
        test_value = int(99)
        self.instance.sensor_id = test_value
        self.assertEqual(self.instance.sensor_id, test_value)
    
    def test_country_iso_property(self):
        """
        Test country_iso property
        """
        test_value = 'pogfyhrtkwbuapgxyiqd'
        self.instance.country_iso = test_value
        self.assertEqual(self.instance.country_iso, test_value)
    
    def test_sensor_name_property(self):
        """
        Test sensor_name property
        """
        test_value = 'xebhzrrdaghpwkqinhfo'
        self.instance.sensor_name = test_value
        self.assertEqual(self.instance.sensor_name, test_value)
    
    def test_parameter_id_property(self):
        """
        Test parameter_id property
        """
        test_value = int(42)
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
        test_value = 'bmnieptphnpeantzvplw'
        self.instance.parameter_units = test_value
        self.assertEqual(self.instance.parameter_units, test_value)
    
    def test_parameter_display_name_property(self):
        """
        Test parameter_display_name property
        """
        test_value = 'pszqlaotjkadnvfpavdz'
        self.instance.parameter_display_name = test_value
        self.assertEqual(self.instance.parameter_display_name, test_value)
    
    def test_datetime_first_property(self):
        """
        Test datetime_first property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.datetime_first = test_value
        self.assertEqual(self.instance.datetime_first, test_value)
    
    def test_datetime_last_property(self):
        """
        Test datetime_last property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.datetime_last = test_value
        self.assertEqual(self.instance.datetime_last, test_value)
    
    def test_latest_value_property(self):
        """
        Test latest_value property
        """
        test_value = float(87.68356563633344)
        self.instance.latest_value = test_value
        self.assertEqual(self.instance.latest_value, test_value)
    
    def test_latest_datetime_property(self):
        """
        Test latest_datetime property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.latest_datetime = test_value
        self.assertEqual(self.instance.latest_datetime, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(55.295359905018614)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(96.50512173801779)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Sensor.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Sensor.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

