"""
Test case for LKI
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from luchtmeetnet_nl_producer_data.nl.rivm.luchtmeetnet.lki import LKI


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
            station_number='zxokpeezgkhsmmxllupj',
            value=int(25),
            timestamp_measured='obevfqnedgrjcqwqclgo'
        )
        return instance

    
    def test_station_number_property(self):
        """
        Test station_number property
        """
        test_value = 'zxokpeezgkhsmmxllupj'
        self.instance.station_number = test_value
        self.assertEqual(self.instance.station_number, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = int(25)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_timestamp_measured_property(self):
        """
        Test timestamp_measured property
        """
        test_value = 'obevfqnedgrjcqwqclgo'
        self.instance.timestamp_measured = test_value
        self.assertEqual(self.instance.timestamp_measured, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = LKI.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
