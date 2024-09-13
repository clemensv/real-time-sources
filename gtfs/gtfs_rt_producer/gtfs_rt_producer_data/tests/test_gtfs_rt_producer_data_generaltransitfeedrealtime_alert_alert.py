"""
Test case for Alert
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedrealtime.alert.alert import Alert
from test_gtfs_rt_producer_data_generaltransitfeedrealtime_alert_translatedstring import Test_TranslatedString
from test_gtfs_rt_producer_data_generaltransitfeedrealtime_alert_timerange import Test_TimeRange
from test_gtfs_rt_producer_data_generaltransitfeedrealtime_alert_alert_types_effect import Test_Effect
from test_gtfs_rt_producer_data_generaltransitfeedrealtime_alert_entityselector import Test_EntitySelector
from test_gtfs_rt_producer_data_generaltransitfeedrealtime_alert_alert_types_cause import Test_Cause

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
            active_period=[Test_TimeRange.create_instance(), Test_TimeRange.create_instance()],
            informed_entity=[Test_EntitySelector.create_instance(), Test_EntitySelector.create_instance(), Test_EntitySelector.create_instance(), Test_EntitySelector.create_instance()],
            cause=Test_Cause.create_instance(),
            effect=Test_Effect.create_instance(),
            url=Test_TranslatedString.create_instance(),
            header_text=Test_TranslatedString.create_instance(),
            description_text=Test_TranslatedString.create_instance()
        )
        return instance

    
    def test_active_period_property(self):
        """
        Test active_period property
        """
        test_value = [Test_TimeRange.create_instance(), Test_TimeRange.create_instance()]
        self.instance.active_period = test_value
        self.assertEqual(self.instance.active_period, test_value)
    
    def test_informed_entity_property(self):
        """
        Test informed_entity property
        """
        test_value = [Test_EntitySelector.create_instance(), Test_EntitySelector.create_instance(), Test_EntitySelector.create_instance(), Test_EntitySelector.create_instance()]
        self.instance.informed_entity = test_value
        self.assertEqual(self.instance.informed_entity, test_value)
    
    def test_cause_property(self):
        """
        Test cause property
        """
        test_value = Test_Cause.create_instance()
        self.instance.cause = test_value
        self.assertEqual(self.instance.cause, test_value)
    
    def test_effect_property(self):
        """
        Test effect property
        """
        test_value = Test_Effect.create_instance()
        self.instance.effect = test_value
        self.assertEqual(self.instance.effect, test_value)
    
    def test_url_property(self):
        """
        Test url property
        """
        test_value = Test_TranslatedString.create_instance()
        self.instance.url = test_value
        self.assertEqual(self.instance.url, test_value)
    
    def test_header_text_property(self):
        """
        Test header_text property
        """
        test_value = Test_TranslatedString.create_instance()
        self.instance.header_text = test_value
        self.assertEqual(self.instance.header_text, test_value)
    
    def test_description_text_property(self):
        """
        Test description_text property
        """
        test_value = Test_TranslatedString.create_instance()
        self.instance.description_text = test_value
        self.assertEqual(self.instance.description_text, test_value)
    
