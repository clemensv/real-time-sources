"""
Test case for ThresholdPeriod
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_waterdata_mqtt_producer_data.usgs.waterdata.thresholdperiod import ThresholdPeriod
import datetime


class Test_ThresholdPeriod(unittest.TestCase):
    """
    Test case for ThresholdPeriod
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_ThresholdPeriod.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of ThresholdPeriod for testing
        """
        instance = ThresholdPeriod(
            start_time=datetime.datetime.now(datetime.timezone.utc),
            end_time=datetime.datetime.now(datetime.timezone.utc),
            applied_time=datetime.datetime.now(datetime.timezone.utc),
            comments='ghvltowqaxasecujqqyo',
            suppress_data=True,
            reference_value=float(91.40126520188416),
            secondary_reference_value=float(95.56762060140524)
        )
        return instance

    
    def test_start_time_property(self):
        """
        Test start_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.start_time = test_value
        self.assertEqual(self.instance.start_time, test_value)
    
    def test_end_time_property(self):
        """
        Test end_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.end_time = test_value
        self.assertEqual(self.instance.end_time, test_value)
    
    def test_applied_time_property(self):
        """
        Test applied_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.applied_time = test_value
        self.assertEqual(self.instance.applied_time, test_value)
    
    def test_comments_property(self):
        """
        Test comments property
        """
        test_value = 'ghvltowqaxasecujqqyo'
        self.instance.comments = test_value
        self.assertEqual(self.instance.comments, test_value)
    
    def test_suppress_data_property(self):
        """
        Test suppress_data property
        """
        test_value = True
        self.instance.suppress_data = test_value
        self.assertEqual(self.instance.suppress_data, test_value)
    
    def test_reference_value_property(self):
        """
        Test reference_value property
        """
        test_value = float(91.40126520188416)
        self.instance.reference_value = test_value
        self.assertEqual(self.instance.reference_value, test_value)
    
    def test_secondary_reference_value_property(self):
        """
        Test secondary_reference_value property
        """
        test_value = float(95.56762060140524)
        self.instance.secondary_reference_value = test_value
        self.assertEqual(self.instance.secondary_reference_value, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = ThresholdPeriod.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = ThresholdPeriod.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

