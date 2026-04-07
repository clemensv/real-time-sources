"""
Test case for WaterLevelObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from rws_waterwebservices_producer_data.waterlevelobservation import WaterLevelObservation
import datetime


class Test_WaterLevelObservation(unittest.TestCase):
    """
    Test case for WaterLevelObservation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_WaterLevelObservation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of WaterLevelObservation for testing
        """
        instance = WaterLevelObservation(
            location_code='uszksnchainndapnapty',
            location_name='cbdkekiamgqfrcxchywf',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            value=float(50.00323699227476),
            unit='lelcgwvezounanpvokob',
            quality_code='caykqxabyamstokjdhwj',
            status='xqxlxyittumuwwckvmgx',
            compartment='qaefgmtaimthzoewwyba',
            parameter='okwndknurifbvwayzgei'
        )
        return instance

    
    def test_location_code_property(self):
        """
        Test location_code property
        """
        test_value = 'uszksnchainndapnapty'
        self.instance.location_code = test_value
        self.assertEqual(self.instance.location_code, test_value)
    
    def test_location_name_property(self):
        """
        Test location_name property
        """
        test_value = 'cbdkekiamgqfrcxchywf'
        self.instance.location_name = test_value
        self.assertEqual(self.instance.location_name, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(50.00323699227476)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_unit_property(self):
        """
        Test unit property
        """
        test_value = 'lelcgwvezounanpvokob'
        self.instance.unit = test_value
        self.assertEqual(self.instance.unit, test_value)
    
    def test_quality_code_property(self):
        """
        Test quality_code property
        """
        test_value = 'caykqxabyamstokjdhwj'
        self.instance.quality_code = test_value
        self.assertEqual(self.instance.quality_code, test_value)
    
    def test_status_property(self):
        """
        Test status property
        """
        test_value = 'xqxlxyittumuwwckvmgx'
        self.instance.status = test_value
        self.assertEqual(self.instance.status, test_value)
    
    def test_compartment_property(self):
        """
        Test compartment property
        """
        test_value = 'qaefgmtaimthzoewwyba'
        self.instance.compartment = test_value
        self.assertEqual(self.instance.compartment, test_value)
    
    def test_parameter_property(self):
        """
        Test parameter property
        """
        test_value = 'okwndknurifbvwayzgei'
        self.instance.parameter = test_value
        self.assertEqual(self.instance.parameter, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = WaterLevelObservation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = WaterLevelObservation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

