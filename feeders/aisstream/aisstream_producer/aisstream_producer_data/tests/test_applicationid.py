"""
Test case for ApplicationID
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aisstream_producer_data.applicationid import ApplicationID


class Test_ApplicationID(unittest.TestCase):
    """
    Test case for ApplicationID
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_ApplicationID.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of ApplicationID for testing
        """
        instance = ApplicationID(
            Valid=True,
            DesignatedAreaCode=int(77),
            FunctionIdentifier=int(67)
        )
        return instance

    
    def test_Valid_property(self):
        """
        Test Valid property
        """
        test_value = True
        self.instance.Valid = test_value
        self.assertEqual(self.instance.Valid, test_value)
    
    def test_DesignatedAreaCode_property(self):
        """
        Test DesignatedAreaCode property
        """
        test_value = int(77)
        self.instance.DesignatedAreaCode = test_value
        self.assertEqual(self.instance.DesignatedAreaCode, test_value)
    
    def test_FunctionIdentifier_property(self):
        """
        Test FunctionIdentifier property
        """
        test_value = int(67)
        self.instance.FunctionIdentifier = test_value
        self.assertEqual(self.instance.FunctionIdentifier, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = ApplicationID.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = ApplicationID.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

