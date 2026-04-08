"""
Test case for PortCallAgent
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from digitraffic_maritime_producer_data.portcallagent import PortCallAgent


class Test_PortCallAgent(unittest.TestCase):
    """
    Test case for PortCallAgent
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_PortCallAgent.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of PortCallAgent for testing
        """
        instance = PortCallAgent(
            name='xcojepbgrwpnypnitnsb',
            port_call_direction='cvtgnexmtcymmmuuwvso',
            role=int(83)
        )
        return instance

    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'xcojepbgrwpnypnitnsb'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_port_call_direction_property(self):
        """
        Test port_call_direction property
        """
        test_value = 'cvtgnexmtcymmmuuwvso'
        self.instance.port_call_direction = test_value
        self.assertEqual(self.instance.port_call_direction, test_value)
    
    def test_role_property(self):
        """
        Test role property
        """
        test_value = int(83)
        self.instance.role = test_value
        self.assertEqual(self.instance.role, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = PortCallAgent.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = PortCallAgent.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

