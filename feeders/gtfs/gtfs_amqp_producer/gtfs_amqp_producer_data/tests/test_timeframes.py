"""
Test case for Timeframes
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_amqp_producer_data.generaltransitfeedstatic.timeframes import Timeframes
from gtfs_amqp_producer_data.generaltransitfeedstatic.calendar import Calendar
from gtfs_amqp_producer_data.generaltransitfeedstatic.calendardates import CalendarDates


class Test_Timeframes(unittest.TestCase):
    """
    Test case for Timeframes
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Timeframes.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Timeframes for testing
        """
        instance = Timeframes(
            timeframeGroupId='bbtlasmujdfpgulswudz',
            startTime='onchpalkkkfscytaxdgz',
            endTime='fnwegrfujlfmhlvxnnfu',
            serviceDates=None
        )
        return instance

    
    def test_timeframeGroupId_property(self):
        """
        Test timeframeGroupId property
        """
        test_value = 'bbtlasmujdfpgulswudz'
        self.instance.timeframeGroupId = test_value
        self.assertEqual(self.instance.timeframeGroupId, test_value)
    
    def test_startTime_property(self):
        """
        Test startTime property
        """
        test_value = 'onchpalkkkfscytaxdgz'
        self.instance.startTime = test_value
        self.assertEqual(self.instance.startTime, test_value)
    
    def test_endTime_property(self):
        """
        Test endTime property
        """
        test_value = 'fnwegrfujlfmhlvxnnfu'
        self.instance.endTime = test_value
        self.assertEqual(self.instance.endTime, test_value)
    
    def test_serviceDates_property(self):
        """
        Test serviceDates property
        """
        test_value = None
        self.instance.serviceDates = test_value
        self.assertEqual(self.instance.serviceDates, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Timeframes.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Timeframes.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

