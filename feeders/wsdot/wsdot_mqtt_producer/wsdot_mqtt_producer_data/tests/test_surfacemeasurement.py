"""
Test case for SurfaceMeasurement
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from wsdot_mqtt_producer_data.us.wa.wsdot.roadweather.surfacemeasurement import SurfaceMeasurement


class Test_SurfaceMeasurement(unittest.TestCase):
    """
    Test case for SurfaceMeasurement
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_SurfaceMeasurement.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of SurfaceMeasurement for testing
        """
        instance = SurfaceMeasurement(
            sensor_id=int(12),
            surface_temperature=float(86.41020488423197),
            road_freezing_temperature=float(78.96972993031122),
            road_surface_condition=int(11)
        )
        return instance

    
    def test_sensor_id_property(self):
        """
        Test sensor_id property
        """
        test_value = int(12)
        self.instance.sensor_id = test_value
        self.assertEqual(self.instance.sensor_id, test_value)
    
    def test_surface_temperature_property(self):
        """
        Test surface_temperature property
        """
        test_value = float(86.41020488423197)
        self.instance.surface_temperature = test_value
        self.assertEqual(self.instance.surface_temperature, test_value)
    
    def test_road_freezing_temperature_property(self):
        """
        Test road_freezing_temperature property
        """
        test_value = float(78.96972993031122)
        self.instance.road_freezing_temperature = test_value
        self.assertEqual(self.instance.road_freezing_temperature, test_value)
    
    def test_road_surface_condition_property(self):
        """
        Test road_surface_condition property
        """
        test_value = int(11)
        self.instance.road_surface_condition = test_value
        self.assertEqual(self.instance.road_surface_condition, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = SurfaceMeasurement.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = SurfaceMeasurement.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

