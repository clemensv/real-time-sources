"""
Test case for Dimension
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aisstream_amqp_producer_data.dimension import Dimension


class Test_Dimension(unittest.TestCase):
    """
    Test case for Dimension
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Dimension.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Dimension for testing
        """
        instance = Dimension(
            A=int(39),
            B=int(64),
            C=int(57),
            D=int(27)
        )
        return instance

    
    def test_A_property(self):
        """
        Test A property
        """
        test_value = int(39)
        self.instance.A = test_value
        self.assertEqual(self.instance.A, test_value)
    
    def test_B_property(self):
        """
        Test B property
        """
        test_value = int(64)
        self.instance.B = test_value
        self.assertEqual(self.instance.B, test_value)
    
    def test_C_property(self):
        """
        Test C property
        """
        test_value = int(57)
        self.instance.C = test_value
        self.assertEqual(self.instance.C, test_value)
    
    def test_D_property(self):
        """
        Test D property
        """
        test_value = int(27)
        self.instance.D = test_value
        self.assertEqual(self.instance.D, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Dimension.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Dimension.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

