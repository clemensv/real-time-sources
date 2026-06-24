"""
Test case for Calendar
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedstatic.calendar import Calendar
from typing import Any


class Test_Calendar(unittest.TestCase):
    """
    Test case for Calendar
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Calendar.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Calendar for testing
        """
        instance = Calendar(
            serviceId='lqaunwadtsqalltocbnf',
            monday=None,
            tuesday=None,
            wednesday=None,
            thursday=None,
            friday=None,
            saturday=None,
            sunday=None,
            startDate='tepunfxhsngnxgywsutv',
            endDate='uipwiwxionpxbeliuljp'
        )
        return instance

    
    def test_serviceId_property(self):
        """
        Test serviceId property
        """
        test_value = 'lqaunwadtsqalltocbnf'
        self.instance.serviceId = test_value
        self.assertEqual(self.instance.serviceId, test_value)
    
    def test_monday_property(self):
        """
        Test monday property
        """
        test_value = None
        self.instance.monday = test_value
        self.assertEqual(self.instance.monday, test_value)
    
    def test_tuesday_property(self):
        """
        Test tuesday property
        """
        test_value = None
        self.instance.tuesday = test_value
        self.assertEqual(self.instance.tuesday, test_value)
    
    def test_wednesday_property(self):
        """
        Test wednesday property
        """
        test_value = None
        self.instance.wednesday = test_value
        self.assertEqual(self.instance.wednesday, test_value)
    
    def test_thursday_property(self):
        """
        Test thursday property
        """
        test_value = None
        self.instance.thursday = test_value
        self.assertEqual(self.instance.thursday, test_value)
    
    def test_friday_property(self):
        """
        Test friday property
        """
        test_value = None
        self.instance.friday = test_value
        self.assertEqual(self.instance.friday, test_value)
    
    def test_saturday_property(self):
        """
        Test saturday property
        """
        test_value = None
        self.instance.saturday = test_value
        self.assertEqual(self.instance.saturday, test_value)
    
    def test_sunday_property(self):
        """
        Test sunday property
        """
        test_value = None
        self.instance.sunday = test_value
        self.assertEqual(self.instance.sunday, test_value)
    
    def test_startDate_property(self):
        """
        Test startDate property
        """
        test_value = 'tepunfxhsngnxgywsutv'
        self.instance.startDate = test_value
        self.assertEqual(self.instance.startDate, test_value)
    
    def test_endDate_property(self):
        """
        Test endDate property
        """
        test_value = 'uipwiwxionpxbeliuljp'
        self.instance.endDate = test_value
        self.assertEqual(self.instance.endDate, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Calendar.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Calendar.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

