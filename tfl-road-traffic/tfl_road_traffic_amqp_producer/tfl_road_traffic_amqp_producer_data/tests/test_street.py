"""
Test case for Street
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from tfl_road_traffic_amqp_producer_data.street import Street


class Test_Street(unittest.TestCase):
    """
    Test case for Street
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Street.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Street for testing
        """
        instance = Street(
            name='wslzcwywdbvtmvdvojgs',
            closure='jpnmdfovyxydwdpmumco',
            directions='byomqekizspwmqwvsxbt',
            source_system_id='kdvycvcdmlxyxywyjuuw',
            source_system_key='vhqqtfhndujfsmypqckk'
        )
        return instance

    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'wslzcwywdbvtmvdvojgs'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_closure_property(self):
        """
        Test closure property
        """
        test_value = 'jpnmdfovyxydwdpmumco'
        self.instance.closure = test_value
        self.assertEqual(self.instance.closure, test_value)
    
    def test_directions_property(self):
        """
        Test directions property
        """
        test_value = 'byomqekizspwmqwvsxbt'
        self.instance.directions = test_value
        self.assertEqual(self.instance.directions, test_value)
    
    def test_source_system_id_property(self):
        """
        Test source_system_id property
        """
        test_value = 'kdvycvcdmlxyxywyjuuw'
        self.instance.source_system_id = test_value
        self.assertEqual(self.instance.source_system_id, test_value)
    
    def test_source_system_key_property(self):
        """
        Test source_system_key property
        """
        test_value = 'vhqqtfhndujfsmypqckk'
        self.instance.source_system_key = test_value
        self.assertEqual(self.instance.source_system_key, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Street.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Street.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

