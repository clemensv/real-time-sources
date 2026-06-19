"""
Test case for TravelTimeObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ndw_road_traffic_mqtt_producer_data.traveltimeobservation import TravelTimeObservation


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
            measurement_site_id='qrvkgvpoossvijwphpac',
            measurement_time='bcueuccrnlemajjoqqyx',
            duration=float(46.33363490209164),
            reference_duration=float(14.772258073834688),
            accuracy=float(60.488216728233),
            data_quality=float(85.51385511939421),
            number_of_input_values=int(80)
        )
        return instance

    
    def test_measurement_site_id_property(self):
        """
        Test measurement_site_id property
        """
        test_value = 'qrvkgvpoossvijwphpac'
        self.instance.measurement_site_id = test_value
        self.assertEqual(self.instance.measurement_site_id, test_value)
    
    def test_measurement_time_property(self):
        """
        Test measurement_time property
        """
        test_value = 'bcueuccrnlemajjoqqyx'
        self.instance.measurement_time = test_value
        self.assertEqual(self.instance.measurement_time, test_value)
    
    def test_duration_property(self):
        """
        Test duration property
        """
        test_value = float(46.33363490209164)
        self.instance.duration = test_value
        self.assertEqual(self.instance.duration, test_value)
    
    def test_reference_duration_property(self):
        """
        Test reference_duration property
        """
        test_value = float(14.772258073834688)
        self.instance.reference_duration = test_value
        self.assertEqual(self.instance.reference_duration, test_value)
    
    def test_accuracy_property(self):
        """
        Test accuracy property
        """
        test_value = float(60.488216728233)
        self.instance.accuracy = test_value
        self.assertEqual(self.instance.accuracy, test_value)
    
    def test_data_quality_property(self):
        """
        Test data_quality property
        """
        test_value = float(85.51385511939421)
        self.instance.data_quality = test_value
        self.assertEqual(self.instance.data_quality, test_value)
    
    def test_number_of_input_values_property(self):
        """
        Test number_of_input_values property
        """
        test_value = int(80)
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

