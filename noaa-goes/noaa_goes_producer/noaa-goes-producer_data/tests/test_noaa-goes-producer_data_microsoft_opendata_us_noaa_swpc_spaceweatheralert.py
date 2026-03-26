"""
Test case for SpaceWeatherAlert
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa-goes-producer_data.microsoft.opendata.us.noaa.swpc.spaceweatheralert import SpaceWeatherAlert


class Test_SpaceWeatherAlert(unittest.TestCase):
    """
    Test case for SpaceWeatherAlert
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_SpaceWeatherAlert.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of SpaceWeatherAlert for testing
        """
        instance = SpaceWeatherAlert(
            product_id='kpbpawmcvsojtkulmapn',
            issue_datetime='bcxlwmhavwjbfcvjddgi',
            message='zdrffoibmnycdmptvsec'
        )
        return instance

    
    def test_product_id_property(self):
        """
        Test product_id property
        """
        test_value = 'kpbpawmcvsojtkulmapn'
        self.instance.product_id = test_value
        self.assertEqual(self.instance.product_id, test_value)
    
    def test_issue_datetime_property(self):
        """
        Test issue_datetime property
        """
        test_value = 'bcxlwmhavwjbfcvjddgi'
        self.instance.issue_datetime = test_value
        self.assertEqual(self.instance.issue_datetime, test_value)
    
    def test_message_property(self):
        """
        Test message property
        """
        test_value = 'zdrffoibmnycdmptvsec'
        self.instance.message = test_value
        self.assertEqual(self.instance.message, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = SpaceWeatherAlert.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
