"""
Test case for LKI
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from luchtmeetnet_nl_mqtt_producer_data.nl.rivm.luchtmeetnet.lki import LKI


class Test_LKI(unittest.TestCase):
    """
    Test case for LKI
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_LKI.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of LKI for testing
        """
        instance = LKI(
            station_number='crcdkfmdrnmtdquekvvp',
            value=int(75),
            timestamp_measured='azbszwliocrzrskrphhm'
        )
        return instance

    
    def test_station_number_property(self):
        """
        Test station_number property
        """
        test_value = 'crcdkfmdrnmtdquekvvp'
        self.instance.station_number = test_value
        self.assertEqual(self.instance.station_number, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = int(75)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_timestamp_measured_property(self):
        """
        Test timestamp_measured property
        """
        test_value = 'azbszwliocrzrskrphhm'
        self.instance.timestamp_measured = test_value
        self.assertEqual(self.instance.timestamp_measured, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = LKI.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = LKI.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

