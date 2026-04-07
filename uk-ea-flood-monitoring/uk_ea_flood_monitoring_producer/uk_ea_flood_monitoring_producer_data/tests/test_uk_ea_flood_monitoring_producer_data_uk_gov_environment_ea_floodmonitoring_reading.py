"""
Test case for Reading
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from uk_ea_flood_monitoring_producer_data.uk.gov.environment.ea.floodmonitoring.reading import Reading
import datetime


class Test_Reading(unittest.TestCase):
    """
    Test case for Reading
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Reading.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Reading for testing
        """
        instance = Reading(
            station_reference='qwhpkvkvbatrktlqsjwr',
            date_time=datetime.datetime.now(datetime.timezone.utc),
            measure='pkttlogepdjcxzlrsmmq',
            value=float(97.27729835026001)
        )
        return instance

    
    def test_station_reference_property(self):
        """
        Test station_reference property
        """
        test_value = 'qwhpkvkvbatrktlqsjwr'
        self.instance.station_reference = test_value
        self.assertEqual(self.instance.station_reference, test_value)
    
    def test_date_time_property(self):
        """
        Test date_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.date_time = test_value
        self.assertEqual(self.instance.date_time, test_value)
    
    def test_measure_property(self):
        """
        Test measure property
        """
        test_value = 'pkttlogepdjcxzlrsmmq'
        self.instance.measure = test_value
        self.assertEqual(self.instance.measure, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(97.27729835026001)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Reading.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
