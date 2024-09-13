"""
Test case for Calendar
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedstatic.calendar import Calendar
from test_gtfs_rt_producer_data_generaltransitfeedstatic_serviceavailability import Test_ServiceAvailability

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
            serviceId='rqktpaciloqgftdetrjw',
            monday=Test_ServiceAvailability.create_instance(),
            tuesday=Test_ServiceAvailability.create_instance(),
            wednesday=Test_ServiceAvailability.create_instance(),
            thursday=Test_ServiceAvailability.create_instance(),
            friday=Test_ServiceAvailability.create_instance(),
            saturday=Test_ServiceAvailability.create_instance(),
            sunday=Test_ServiceAvailability.create_instance(),
            startDate='sburcgdjidphfenuhnfz',
            endDate='mffsmdbgrxnjsdfuxali'
        )
        return instance

    
    def test_serviceId_property(self):
        """
        Test serviceId property
        """
        test_value = 'rqktpaciloqgftdetrjw'
        self.instance.serviceId = test_value
        self.assertEqual(self.instance.serviceId, test_value)
    
    def test_monday_property(self):
        """
        Test monday property
        """
        test_value = Test_ServiceAvailability.create_instance()
        self.instance.monday = test_value
        self.assertEqual(self.instance.monday, test_value)
    
    def test_tuesday_property(self):
        """
        Test tuesday property
        """
        test_value = Test_ServiceAvailability.create_instance()
        self.instance.tuesday = test_value
        self.assertEqual(self.instance.tuesday, test_value)
    
    def test_wednesday_property(self):
        """
        Test wednesday property
        """
        test_value = Test_ServiceAvailability.create_instance()
        self.instance.wednesday = test_value
        self.assertEqual(self.instance.wednesday, test_value)
    
    def test_thursday_property(self):
        """
        Test thursday property
        """
        test_value = Test_ServiceAvailability.create_instance()
        self.instance.thursday = test_value
        self.assertEqual(self.instance.thursday, test_value)
    
    def test_friday_property(self):
        """
        Test friday property
        """
        test_value = Test_ServiceAvailability.create_instance()
        self.instance.friday = test_value
        self.assertEqual(self.instance.friday, test_value)
    
    def test_saturday_property(self):
        """
        Test saturday property
        """
        test_value = Test_ServiceAvailability.create_instance()
        self.instance.saturday = test_value
        self.assertEqual(self.instance.saturday, test_value)
    
    def test_sunday_property(self):
        """
        Test sunday property
        """
        test_value = Test_ServiceAvailability.create_instance()
        self.instance.sunday = test_value
        self.assertEqual(self.instance.sunday, test_value)
    
    def test_startDate_property(self):
        """
        Test startDate property
        """
        test_value = 'sburcgdjidphfenuhnfz'
        self.instance.startDate = test_value
        self.assertEqual(self.instance.startDate, test_value)
    
    def test_endDate_property(self):
        """
        Test endDate property
        """
        test_value = 'mffsmdbgrxnjsdfuxali'
        self.instance.endDate = test_value
        self.assertEqual(self.instance.endDate, test_value)
    
