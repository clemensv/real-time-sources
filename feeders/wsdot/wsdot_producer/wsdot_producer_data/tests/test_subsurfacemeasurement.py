"""
Test case for SubSurfaceMeasurement
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from wsdot_producer_data.us.wa.wsdot.roadweather.subsurfacemeasurement import SubSurfaceMeasurement


class Test_SubSurfaceMeasurement(unittest.TestCase):
    """
    Test case for SubSurfaceMeasurement
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_SubSurfaceMeasurement.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of SubSurfaceMeasurement for testing
        """
        instance = SubSurfaceMeasurement(
            sensor_id=int(75),
            sub_surface_temperature=float(95.87770080038123)
        )
        return instance

    
    def test_sensor_id_property(self):
        """
        Test sensor_id property
        """
        test_value = int(75)
        self.instance.sensor_id = test_value
        self.assertEqual(self.instance.sensor_id, test_value)
    
    def test_sub_surface_temperature_property(self):
        """
        Test sub_surface_temperature property
        """
        test_value = float(95.87770080038123)
        self.instance.sub_surface_temperature = test_value
        self.assertEqual(self.instance.sub_surface_temperature, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = SubSurfaceMeasurement.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = SubSurfaceMeasurement.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

