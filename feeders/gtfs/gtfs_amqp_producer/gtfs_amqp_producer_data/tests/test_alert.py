"""
Test case for Alert
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_amqp_producer_data.generaltransitfeedrealtime.alert.alert import Alert
from gtfs_amqp_producer_data.generaltransitfeedrealtime.alert.entityselector import EntitySelector
from gtfs_amqp_producer_data.generaltransitfeedrealtime.alert.timerange import TimeRange
from gtfs_amqp_producer_data.generaltransitfeedrealtime.alert.translatedstring import TranslatedString
from typing import Any


class Test_Alert(unittest.TestCase):
    """
    Test case for Alert
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Alert.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Alert for testing
        """
        instance = Alert(
            active_period=[None, None, None],
            informed_entity=[None, None, None, None],
            cause=None,
            effect=None,
            url=None,
            header_text=None,
            description_text=None
        )
        return instance

    
    def test_active_period_property(self):
        """
        Test active_period property
        """
        test_value = [None, None, None]
        self.instance.active_period = test_value
        self.assertEqual(self.instance.active_period, test_value)
    
    def test_informed_entity_property(self):
        """
        Test informed_entity property
        """
        test_value = [None, None, None, None]
        self.instance.informed_entity = test_value
        self.assertEqual(self.instance.informed_entity, test_value)
    
    def test_cause_property(self):
        """
        Test cause property
        """
        test_value = None
        self.instance.cause = test_value
        self.assertEqual(self.instance.cause, test_value)
    
    def test_effect_property(self):
        """
        Test effect property
        """
        test_value = None
        self.instance.effect = test_value
        self.assertEqual(self.instance.effect, test_value)
    
    def test_url_property(self):
        """
        Test url property
        """
        test_value = None
        self.instance.url = test_value
        self.assertEqual(self.instance.url, test_value)
    
    def test_header_text_property(self):
        """
        Test header_text property
        """
        test_value = None
        self.instance.header_text = test_value
        self.assertEqual(self.instance.header_text, test_value)
    
    def test_description_text_property(self):
        """
        Test description_text property
        """
        test_value = None
        self.instance.description_text = test_value
        self.assertEqual(self.instance.description_text, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Alert.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Alert.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

