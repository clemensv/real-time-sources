"""
Test case for WaterLevelObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from rws_waterwebservices_producer_data.nl.rws.waterwebservices.waterlevelobservation import WaterLevelObservation
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
            location_code='rhfqxkdlkkizdsoajtey',
            location_name='zksduvuyxjixvsmitssx',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            value=float(92.3519475502626),
            unit='cdkgirwewucblfhkgfbh',
            quality_code='xhwmlwrdycmbtcymgqky',
            status='ewbqdiqtnbxgrkqpqfmj',
            compartment='bxllafxqupeylxoxkfwv',
            parameter='rajeoxylgnsegozlfdry'
        )
        return instance

    
    def test_location_code_property(self):
        """
        Test location_code property
        """
        test_value = 'rhfqxkdlkkizdsoajtey'
        self.instance.location_code = test_value
        self.assertEqual(self.instance.location_code, test_value)
    
    def test_location_name_property(self):
        """
        Test location_name property
        """
        test_value = 'zksduvuyxjixvsmitssx'
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
        test_value = float(92.3519475502626)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_unit_property(self):
        """
        Test unit property
        """
        test_value = 'cdkgirwewucblfhkgfbh'
        self.instance.unit = test_value
        self.assertEqual(self.instance.unit, test_value)
    
    def test_quality_code_property(self):
        """
        Test quality_code property
        """
        test_value = 'xhwmlwrdycmbtcymgqky'
        self.instance.quality_code = test_value
        self.assertEqual(self.instance.quality_code, test_value)
    
    def test_status_property(self):
        """
        Test status property
        """
        test_value = 'ewbqdiqtnbxgrkqpqfmj'
        self.instance.status = test_value
        self.assertEqual(self.instance.status, test_value)
    
    def test_compartment_property(self):
        """
        Test compartment property
        """
        test_value = 'bxllafxqupeylxoxkfwv'
        self.instance.compartment = test_value
        self.assertEqual(self.instance.compartment, test_value)
    
    def test_parameter_property(self):
        """
        Test parameter property
        """
        test_value = 'rajeoxylgnsegozlfdry'
        self.instance.parameter = test_value
        self.assertEqual(self.instance.parameter, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = WaterLevelObservation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
