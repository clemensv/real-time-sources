"""
Test case for MeasurementPoint
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from madrid_traffic_producer_data.measurementpoint import MeasurementPoint


class Test_MeasurementPoint(unittest.TestCase):
    """
    Test case for MeasurementPoint
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_MeasurementPoint.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of MeasurementPoint for testing
        """
        instance = MeasurementPoint(
            sensor_id='vzqgbqzgyerfegsvosqt',
            description='jxixqubnkbpamzkerpjg',
            element_type='mnoyesdmuezicxchfjer',
            subarea='xkrhuqdhhkbagsbgmpco',
            longitude=float(63.68754033253363),
            latitude=float(85.24820982856797),
            saturation_intensity=int(75)
        )
        return instance

    
    def test_sensor_id_property(self):
        """
        Test sensor_id property
        """
        test_value = 'vzqgbqzgyerfegsvosqt'
        self.instance.sensor_id = test_value
        self.assertEqual(self.instance.sensor_id, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'jxixqubnkbpamzkerpjg'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_element_type_property(self):
        """
        Test element_type property
        """
        test_value = 'mnoyesdmuezicxchfjer'
        self.instance.element_type = test_value
        self.assertEqual(self.instance.element_type, test_value)
    
    def test_subarea_property(self):
        """
        Test subarea property
        """
        test_value = 'xkrhuqdhhkbagsbgmpco'
        self.instance.subarea = test_value
        self.assertEqual(self.instance.subarea, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(63.68754033253363)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(85.24820982856797)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_saturation_intensity_property(self):
        """
        Test saturation_intensity property
        """
        test_value = int(75)
        self.instance.saturation_intensity = test_value
        self.assertEqual(self.instance.saturation_intensity, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = MeasurementPoint.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = MeasurementPoint.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

