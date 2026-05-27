"""
Test case for WaterLevelObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from rws_waterwebservices_producer_data.nl.rws.waterwebservices.waterlevelobservation import WaterLevelObservation


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
            station_code='wbvopzwimufqegmcuxni',
            location_name='hbzdowkpuwdrdrzztfmw',
            timestamp='rtjfrohqjvcispvmlmnb',
            value=float(18.98980361178677),
            unit='wozadqnyizqcpqkolqls',
            quality_code='jkcxxvzujixraqdlkxhv',
            status='vhsrygeuvbtkmhmaxajm',
            compartment='glismjssbrqtodveaaeh',
            parameter='wzrvmnrzgehjcoqstoif'
        )
        return instance

    
    def test_station_code_property(self):
        """
        Test station_code property
        """
        test_value = 'wbvopzwimufqegmcuxni'
        self.instance.station_code = test_value
        self.assertEqual(self.instance.station_code, test_value)
    
    def test_location_name_property(self):
        """
        Test location_name property
        """
        test_value = 'hbzdowkpuwdrdrzztfmw'
        self.instance.location_name = test_value
        self.assertEqual(self.instance.location_name, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'rtjfrohqjvcispvmlmnb'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(18.98980361178677)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_unit_property(self):
        """
        Test unit property
        """
        test_value = 'wozadqnyizqcpqkolqls'
        self.instance.unit = test_value
        self.assertEqual(self.instance.unit, test_value)
    
    def test_quality_code_property(self):
        """
        Test quality_code property
        """
        test_value = 'jkcxxvzujixraqdlkxhv'
        self.instance.quality_code = test_value
        self.assertEqual(self.instance.quality_code, test_value)
    
    def test_status_property(self):
        """
        Test status property
        """
        test_value = 'vhsrygeuvbtkmhmaxajm'
        self.instance.status = test_value
        self.assertEqual(self.instance.status, test_value)
    
    def test_compartment_property(self):
        """
        Test compartment property
        """
        test_value = 'glismjssbrqtodveaaeh'
        self.instance.compartment = test_value
        self.assertEqual(self.instance.compartment, test_value)
    
    def test_parameter_property(self):
        """
        Test parameter property
        """
        test_value = 'wzrvmnrzgehjcoqstoif'
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
