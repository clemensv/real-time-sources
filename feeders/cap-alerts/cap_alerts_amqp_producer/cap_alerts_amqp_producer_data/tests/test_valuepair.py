"""
Test case for ValuePair
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from cap_alerts_amqp_producer_data.org.oasis.cap.alerts.valuepair import ValuePair


class Test_ValuePair(unittest.TestCase):
    """
    Test case for ValuePair
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_ValuePair.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of ValuePair for testing
        """
        instance = ValuePair(
            value_name='fvlzhngnxihkqxirpgxj',
            value='pcxyxhmcisshpawsxiai'
        )
        return instance

    
    def test_value_name_property(self):
        """
        Test value_name property
        """
        test_value = 'fvlzhngnxihkqxirpgxj'
        self.instance.value_name = test_value
        self.assertEqual(self.instance.value_name, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = 'pcxyxhmcisshpawsxiai'
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = ValuePair.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = ValuePair.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

