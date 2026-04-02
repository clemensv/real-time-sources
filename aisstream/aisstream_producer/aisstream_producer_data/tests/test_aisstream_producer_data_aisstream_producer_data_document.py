"""
Test case for Document
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aisstream_producer_data.aisstream_producer_data.document import Document
from test_aisstream_producer_data_aisstream_producer_data_object import Test_Object


class Test_Document(unittest.TestCase):
    """
    Test case for Document
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Document.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Document for testing
        """
        instance = Document(
            MessageID=int(74),
            RepeatIndicator=int(42),
            UserID=int(41),
            Valid=True,
            Spare=int(88),
            Station1Msg1=Test_Object.create_instance(),
            Station1Msg2=Test_Object.create_instance(),
            Station2=Test_Object.create_instance()
        )
        return instance

    
    def test_MessageID_property(self):
        """
        Test MessageID property
        """
        test_value = int(74)
        self.instance.MessageID = test_value
        self.assertEqual(self.instance.MessageID, test_value)
    
    def test_RepeatIndicator_property(self):
        """
        Test RepeatIndicator property
        """
        test_value = int(42)
        self.instance.RepeatIndicator = test_value
        self.assertEqual(self.instance.RepeatIndicator, test_value)
    
    def test_UserID_property(self):
        """
        Test UserID property
        """
        test_value = int(41)
        self.instance.UserID = test_value
        self.assertEqual(self.instance.UserID, test_value)
    
    def test_Valid_property(self):
        """
        Test Valid property
        """
        test_value = True
        self.instance.Valid = test_value
        self.assertEqual(self.instance.Valid, test_value)
    
    def test_Spare_property(self):
        """
        Test Spare property
        """
        test_value = int(88)
        self.instance.Spare = test_value
        self.assertEqual(self.instance.Spare, test_value)
    
    def test_Station1Msg1_property(self):
        """
        Test Station1Msg1 property
        """
        test_value = Test_Object.create_instance()
        self.instance.Station1Msg1 = test_value
        self.assertEqual(self.instance.Station1Msg1, test_value)
    
    def test_Station1Msg2_property(self):
        """
        Test Station1Msg2 property
        """
        test_value = Test_Object.create_instance()
        self.instance.Station1Msg2 = test_value
        self.assertEqual(self.instance.Station1Msg2, test_value)
    
    def test_Station2_property(self):
        """
        Test Station2 property
        """
        test_value = Test_Object.create_instance()
        self.instance.Station2 = test_value
        self.assertEqual(self.instance.Station2, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Document.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
