"""
Test case for Intensity
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from carbon_intensity_mqtt_producer_data.intensity import Intensity
import datetime


class Test_Intensity(unittest.TestCase):
    """
    Test case for Intensity
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Intensity.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Intensity for testing
        """
        instance = Intensity(
            period_from=datetime.datetime.now(datetime.timezone.utc),
            period_to=datetime.datetime.now(datetime.timezone.utc),
            forecast=int(13),
            actual=int(9),
            index='yfqejbbgmrehofntrqfv',
            region='rpqeyqfrmjznnrqntyxm',
            ce_id='fsfihkjxmakvgxwsbvli'
        )
        return instance

    
    def test_period_from_property(self):
        """
        Test period_from property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.period_from = test_value
        self.assertEqual(self.instance.period_from, test_value)
    
    def test_period_to_property(self):
        """
        Test period_to property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.period_to = test_value
        self.assertEqual(self.instance.period_to, test_value)
    
    def test_forecast_property(self):
        """
        Test forecast property
        """
        test_value = int(13)
        self.instance.forecast = test_value
        self.assertEqual(self.instance.forecast, test_value)
    
    def test_actual_property(self):
        """
        Test actual property
        """
        test_value = int(9)
        self.instance.actual = test_value
        self.assertEqual(self.instance.actual, test_value)
    
    def test_index_property(self):
        """
        Test index property
        """
        test_value = 'yfqejbbgmrehofntrqfv'
        self.instance.index = test_value
        self.assertEqual(self.instance.index, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'rpqeyqfrmjznnrqntyxm'
        self.instance.region = test_value
        self.assertEqual(self.instance.region, test_value)
    
    def test_ce_id_property(self):
        """
        Test ce_id property
        """
        test_value = 'fsfihkjxmakvgxwsbvli'
        self.instance.ce_id = test_value
        self.assertEqual(self.instance.ce_id, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Intensity.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Intensity.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

