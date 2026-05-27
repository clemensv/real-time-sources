"""
Test case for VesselRegistration
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from digitraffic_maritime_producer_data.vesselregistration import VesselRegistration


class Test_VesselRegistration(unittest.TestCase):
    """
    Test case for VesselRegistration
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_VesselRegistration.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of VesselRegistration for testing
        """
        instance = VesselRegistration(
            nationality='ekuqpjcshjoreonanval',
            port_of_registry='eksungbzkimacnlmxokx'
        )
        return instance

    
    def test_nationality_property(self):
        """
        Test nationality property
        """
        test_value = 'ekuqpjcshjoreonanval'
        self.instance.nationality = test_value
        self.assertEqual(self.instance.nationality, test_value)
    
    def test_port_of_registry_property(self):
        """
        Test port_of_registry property
        """
        test_value = 'eksungbzkimacnlmxokx'
        self.instance.port_of_registry = test_value
        self.assertEqual(self.instance.port_of_registry, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = VesselRegistration.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = VesselRegistration.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

