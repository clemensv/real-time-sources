"""
Test case for TravelTimeObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ndw_road_traffic_producer_data.traveltimeobservation import TravelTimeObservation


class Test_TravelTimeObservation(unittest.TestCase):
    """
    Test case for TravelTimeObservation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_TravelTimeObservation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of TravelTimeObservation for testing
        """
        instance = TravelTimeObservation(
            measurement_site_id='zexhzqdlhdknubvrlhmr',
            measurement_time='xlndksorlhqfubkhqflj',
            duration=float(76.27368014915646),
            reference_duration=float(18.997587750680843),
            accuracy=float(8.087380825204793),
            data_quality=float(3.3868221703492685),
            number_of_input_values=int(78)
        )
        return instance

    
    def test_measurement_site_id_property(self):
        """
        Test measurement_site_id property
        """
        test_value = 'zexhzqdlhdknubvrlhmr'
        self.instance.measurement_site_id = test_value
        self.assertEqual(self.instance.measurement_site_id, test_value)
    
    def test_measurement_time_property(self):
        """
        Test measurement_time property
        """
        test_value = 'xlndksorlhqfubkhqflj'
        self.instance.measurement_time = test_value
        self.assertEqual(self.instance.measurement_time, test_value)
    
    def test_duration_property(self):
        """
        Test duration property
        """
        test_value = float(76.27368014915646)
        self.instance.duration = test_value
        self.assertEqual(self.instance.duration, test_value)
    
    def test_reference_duration_property(self):
        """
        Test reference_duration property
        """
        test_value = float(18.997587750680843)
        self.instance.reference_duration = test_value
        self.assertEqual(self.instance.reference_duration, test_value)
    
    def test_accuracy_property(self):
        """
        Test accuracy property
        """
        test_value = float(8.087380825204793)
        self.instance.accuracy = test_value
        self.assertEqual(self.instance.accuracy, test_value)
    
    def test_data_quality_property(self):
        """
        Test data_quality property
        """
        test_value = float(3.3868221703492685)
        self.instance.data_quality = test_value
        self.assertEqual(self.instance.data_quality, test_value)
    
    def test_number_of_input_values_property(self):
        """
        Test number_of_input_values property
        """
        test_value = int(78)
        self.instance.number_of_input_values = test_value
        self.assertEqual(self.instance.number_of_input_values, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = TravelTimeObservation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = TravelTimeObservation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

