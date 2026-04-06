"""
Test case for TidePredOffsets
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_producer_data.microsoft.opendata.us.noaa.stationtypes.tidepredoffsets import TidePredOffsets


class Test_TidePredOffsets(unittest.TestCase):
    """
    Test case for TidePredOffsets
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_TidePredOffsets.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of TidePredOffsets for testing
        """
        instance = TidePredOffsets(
            self_='ozvhujstlvflefytegps'
        )
        return instance

    
    def test_self__property(self):
        """
        Test self_ property
        """
        test_value = 'ozvhujstlvflefytegps'
        self.instance.self_ = test_value
        self.assertEqual(self.instance.self_, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = TidePredOffsets.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
