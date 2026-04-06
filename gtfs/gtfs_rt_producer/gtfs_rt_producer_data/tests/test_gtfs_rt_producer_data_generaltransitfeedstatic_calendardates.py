"""
Test case for CalendarDates
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedstatic.calendardates import CalendarDates
from test_gtfs_rt_producer_data_generaltransitfeedstatic_exceptiontype import Test_ExceptionType


class Test_CalendarDates(unittest.TestCase):
    """
    Test case for CalendarDates
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_CalendarDates.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of CalendarDates for testing
        """
        instance = CalendarDates(
            serviceId='sqqjmgyswwpvwjnwllfw',
            date='xuelmaypuioyerunmzlp',
            exceptionType=Test_ExceptionType.create_instance()
        )
        return instance

    
    def test_serviceId_property(self):
        """
        Test serviceId property
        """
        test_value = 'sqqjmgyswwpvwjnwllfw'
        self.instance.serviceId = test_value
        self.assertEqual(self.instance.serviceId, test_value)
    
    def test_date_property(self):
        """
        Test date property
        """
        test_value = 'xuelmaypuioyerunmzlp'
        self.instance.date = test_value
        self.assertEqual(self.instance.date, test_value)
    
    def test_exceptionType_property(self):
        """
        Test exceptionType property
        """
        test_value = Test_ExceptionType.create_instance()
        self.instance.exceptionType = test_value
        self.assertEqual(self.instance.exceptionType, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = CalendarDates.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
