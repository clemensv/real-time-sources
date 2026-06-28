"""
Test case for StaticDataReport
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aisstream_amqp_producer_data.staticdatareport import StaticDataReport
from aisstream_amqp_producer_data.reporta import ReportA
from aisstream_amqp_producer_data.reportb import ReportB


class Test_StaticDataReport(unittest.TestCase):
    """
    Test case for StaticDataReport
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_StaticDataReport.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of StaticDataReport for testing
        """
        instance = StaticDataReport(
            MessageID=int(27),
            RepeatIndicator=int(91),
            UserID=int(36),
            Valid=False,
            Reserved=int(0),
            PartNumber=False,
            ReportA=None,
            ReportB=None
        )
        return instance

    
    def test_MessageID_property(self):
        """
        Test MessageID property
        """
        test_value = int(27)
        self.instance.MessageID = test_value
        self.assertEqual(self.instance.MessageID, test_value)
    
    def test_RepeatIndicator_property(self):
        """
        Test RepeatIndicator property
        """
        test_value = int(91)
        self.instance.RepeatIndicator = test_value
        self.assertEqual(self.instance.RepeatIndicator, test_value)
    
    def test_UserID_property(self):
        """
        Test UserID property
        """
        test_value = int(36)
        self.instance.UserID = test_value
        self.assertEqual(self.instance.UserID, test_value)
    
    def test_Valid_property(self):
        """
        Test Valid property
        """
        test_value = False
        self.instance.Valid = test_value
        self.assertEqual(self.instance.Valid, test_value)
    
    def test_Reserved_property(self):
        """
        Test Reserved property
        """
        test_value = int(0)
        self.instance.Reserved = test_value
        self.assertEqual(self.instance.Reserved, test_value)
    
    def test_PartNumber_property(self):
        """
        Test PartNumber property
        """
        test_value = False
        self.instance.PartNumber = test_value
        self.assertEqual(self.instance.PartNumber, test_value)
    
    def test_ReportA_property(self):
        """
        Test ReportA property
        """
        test_value = None
        self.instance.ReportA = test_value
        self.assertEqual(self.instance.ReportA, test_value)
    
    def test_ReportB_property(self):
        """
        Test ReportB property
        """
        test_value = None
        self.instance.ReportB = test_value
        self.assertEqual(self.instance.ReportB, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = StaticDataReport.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = StaticDataReport.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

