"""
Test case for Nearby
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa-producer_data.microsoft.opendata.us.noaa.stationtypes.nearby import Nearby


class Test_Nearby(unittest.TestCase):
    """
    Test case for Nearby
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Nearby.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Nearby for testing
        """
        instance = Nearby(
            self_='toscejumuepbjpuiptgu'
        )
        return instance

    
    def test_self__property(self):
        """
        Test self_ property
        """
        test_value = 'toscejumuepbjpuiptgu'
        self.instance.self_ = test_value
        self.assertEqual(self.instance.self_, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Nearby.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
