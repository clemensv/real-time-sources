"""
Test case for Operator
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from siri_producer_data.operator import Operator


class Test_Operator(unittest.TestCase):
    """
    Test case for Operator
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Operator.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Operator for testing
        """
        instance = Operator(
            operator_ref='apmhmwelomyardrznaag'
        )
        return instance

    
    def test_operator_ref_property(self):
        """
        Test operator_ref property
        """
        test_value = 'apmhmwelomyardrznaag'
        self.instance.operator_ref = test_value
        self.assertEqual(self.instance.operator_ref, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Operator.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Operator.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

