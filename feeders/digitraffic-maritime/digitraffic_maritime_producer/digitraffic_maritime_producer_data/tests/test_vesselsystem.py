"""
Test case for VesselSystem
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from digitraffic_maritime_producer_data.vesselsystem import VesselSystem


class Test_VesselSystem(unittest.TestCase):
    """
    Test case for VesselSystem
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_VesselSystem.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of VesselSystem for testing
        """
        instance = VesselSystem(
            ship_owner='usfcffipfrvogsdkiugp',
            ship_telephone_1='audxngqefcoccegjvcaf',
            ship_email='odqtlglvwlcjklioqhfc',
            ship_verifier='ftrvslhqsrhylmgzkgzi'
        )
        return instance

    
    def test_ship_owner_property(self):
        """
        Test ship_owner property
        """
        test_value = 'usfcffipfrvogsdkiugp'
        self.instance.ship_owner = test_value
        self.assertEqual(self.instance.ship_owner, test_value)
    
    def test_ship_telephone_1_property(self):
        """
        Test ship_telephone_1 property
        """
        test_value = 'audxngqefcoccegjvcaf'
        self.instance.ship_telephone_1 = test_value
        self.assertEqual(self.instance.ship_telephone_1, test_value)
    
    def test_ship_email_property(self):
        """
        Test ship_email property
        """
        test_value = 'odqtlglvwlcjklioqhfc'
        self.instance.ship_email = test_value
        self.assertEqual(self.instance.ship_email, test_value)
    
    def test_ship_verifier_property(self):
        """
        Test ship_verifier property
        """
        test_value = 'ftrvslhqsrhylmgzkgzi'
        self.instance.ship_verifier = test_value
        self.assertEqual(self.instance.ship_verifier, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = VesselSystem.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = VesselSystem.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

