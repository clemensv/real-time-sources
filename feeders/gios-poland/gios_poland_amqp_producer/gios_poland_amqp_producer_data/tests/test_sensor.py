"""
Test case for Sensor
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gios_poland_amqp_producer_data.sensor import Sensor


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
            sensor_id=int(31),
            station_id=int(41),
            parameter_name='frfsxqhussxhoumzqpts',
            parameter_formula='yfigndtxishyznocdmik',
            parameter_code='kiqywetkgbtzhplvlanb',
            parameter_id=int(51)
        )
        return instance

    
    def test_sensor_id_property(self):
        """
        Test sensor_id property
        """
        test_value = int(31)
        self.instance.sensor_id = test_value
        self.assertEqual(self.instance.sensor_id, test_value)
    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = int(41)
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_parameter_name_property(self):
        """
        Test parameter_name property
        """
        test_value = 'frfsxqhussxhoumzqpts'
        self.instance.parameter_name = test_value
        self.assertEqual(self.instance.parameter_name, test_value)
    
    def test_parameter_formula_property(self):
        """
        Test parameter_formula property
        """
        test_value = 'yfigndtxishyznocdmik'
        self.instance.parameter_formula = test_value
        self.assertEqual(self.instance.parameter_formula, test_value)
    
    def test_parameter_code_property(self):
        """
        Test parameter_code property
        """
        test_value = 'kiqywetkgbtzhplvlanb'
        self.instance.parameter_code = test_value
        self.assertEqual(self.instance.parameter_code, test_value)
    
    def test_parameter_id_property(self):
        """
        Test parameter_id property
        """
        test_value = int(51)
        self.instance.parameter_id = test_value
        self.assertEqual(self.instance.parameter_id, test_value)
    
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

