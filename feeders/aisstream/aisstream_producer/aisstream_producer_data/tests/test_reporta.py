"""
Test case for ReportA
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aisstream_producer_data.reporta import ReportA


class Test_ReportA(unittest.TestCase):
    """
    Test case for ReportA
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_ReportA.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of ReportA for testing
        """
        instance = ReportA(
            Valid=True,
            Name='ftdmpfbrhepxnelskwgk'
        )
        return instance

    
    def test_Valid_property(self):
        """
        Test Valid property
        """
        test_value = True
        self.instance.Valid = test_value
        self.assertEqual(self.instance.Valid, test_value)
    
    def test_Name_property(self):
        """
        Test Name property
        """
        test_value = 'ftdmpfbrhepxnelskwgk'
        self.instance.Name = test_value
        self.assertEqual(self.instance.Name, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = ReportA.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = ReportA.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

