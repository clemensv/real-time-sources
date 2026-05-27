"""
Test case for TravelTime
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ndl_netherlands_producer_data.nl.ndw.traffic.traveltime import TravelTime


class Test_TravelTime(unittest.TestCase):
    """
    Test case for TravelTime
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_TravelTime.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of TravelTime for testing
        """
        instance = TravelTime(
            site_id='xpnnznzmtswmwcrvgint',
            measurement_time='qkvdmmxsfhqgjmqblnai',
            duration=float(1.6885663100735804),
            reference_duration=float(9.47006145398902),
            accuracy=float(85.59335888586449),
            data_quality=float(6.847586163648911),
            number_of_input_values=int(68)
        )
        return instance

    
    def test_site_id_property(self):
        """
        Test site_id property
        """
        test_value = 'xpnnznzmtswmwcrvgint'
        self.instance.site_id = test_value
        self.assertEqual(self.instance.site_id, test_value)
    
    def test_measurement_time_property(self):
        """
        Test measurement_time property
        """
        test_value = 'qkvdmmxsfhqgjmqblnai'
        self.instance.measurement_time = test_value
        self.assertEqual(self.instance.measurement_time, test_value)
    
    def test_duration_property(self):
        """
        Test duration property
        """
        test_value = float(1.6885663100735804)
        self.instance.duration = test_value
        self.assertEqual(self.instance.duration, test_value)
    
    def test_reference_duration_property(self):
        """
        Test reference_duration property
        """
        test_value = float(9.47006145398902)
        self.instance.reference_duration = test_value
        self.assertEqual(self.instance.reference_duration, test_value)
    
    def test_accuracy_property(self):
        """
        Test accuracy property
        """
        test_value = float(85.59335888586449)
        self.instance.accuracy = test_value
        self.assertEqual(self.instance.accuracy, test_value)
    
    def test_data_quality_property(self):
        """
        Test data_quality property
        """
        test_value = float(6.847586163648911)
        self.instance.data_quality = test_value
        self.assertEqual(self.instance.data_quality, test_value)
    
    def test_number_of_input_values_property(self):
        """
        Test number_of_input_values property
        """
        test_value = int(68)
        self.instance.number_of_input_values = test_value
        self.assertEqual(self.instance.number_of_input_values, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = TravelTime.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = TravelTime.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

