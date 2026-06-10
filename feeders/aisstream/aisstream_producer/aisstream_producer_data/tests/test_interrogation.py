"""
Test case for Interrogation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aisstream_producer_data.interrogation import Interrogation
from aisstream_producer_data.station1msg1 import Station1Msg1
from aisstream_producer_data.station2 import Station2
from aisstream_producer_data.station1msg2 import Station1Msg2


class Test_Interrogation(unittest.TestCase):
    """
    Test case for Interrogation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Interrogation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Interrogation for testing
        """
        instance = Interrogation(
            MessageID=int(57),
            RepeatIndicator=int(7),
            UserID=int(18),
            Valid=False,
            Spare=int(72),
            Station1Msg1=None,
            Station1Msg2=None,
            Station2=None
        )
        return instance

    
    def test_MessageID_property(self):
        """
        Test MessageID property
        """
        test_value = int(57)
        self.instance.MessageID = test_value
        self.assertEqual(self.instance.MessageID, test_value)
    
    def test_RepeatIndicator_property(self):
        """
        Test RepeatIndicator property
        """
        test_value = int(7)
        self.instance.RepeatIndicator = test_value
        self.assertEqual(self.instance.RepeatIndicator, test_value)
    
    def test_UserID_property(self):
        """
        Test UserID property
        """
        test_value = int(18)
        self.instance.UserID = test_value
        self.assertEqual(self.instance.UserID, test_value)
    
    def test_Valid_property(self):
        """
        Test Valid property
        """
        test_value = False
        self.instance.Valid = test_value
        self.assertEqual(self.instance.Valid, test_value)
    
    def test_Spare_property(self):
        """
        Test Spare property
        """
        test_value = int(72)
        self.instance.Spare = test_value
        self.assertEqual(self.instance.Spare, test_value)
    
    def test_Station1Msg1_property(self):
        """
        Test Station1Msg1 property
        """
        test_value = None
        self.instance.Station1Msg1 = test_value
        self.assertEqual(self.instance.Station1Msg1, test_value)
    
    def test_Station1Msg2_property(self):
        """
        Test Station1Msg2 property
        """
        test_value = None
        self.instance.Station1Msg2 = test_value
        self.assertEqual(self.instance.Station1Msg2, test_value)
    
    def test_Station2_property(self):
        """
        Test Station2 property
        """
        test_value = None
        self.instance.Station2 = test_value
        self.assertEqual(self.instance.Station2, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Interrogation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Interrogation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

