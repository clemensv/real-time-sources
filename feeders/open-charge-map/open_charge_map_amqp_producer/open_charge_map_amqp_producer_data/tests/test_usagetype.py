"""
Test case for UsageType
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from open_charge_map_amqp_producer_data.io.openchargemap.usagetype import UsageType


class Test_UsageType(unittest.TestCase):
    """
    Test case for UsageType
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_UsageType.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of UsageType for testing
        """
        instance = UsageType(
            reference_type='sonwubccsploswbmpomq',
            reference_id=int(21),
            title='whfwhqrajmgzyscgspyd',
            is_pay_at_location=True,
            is_membership_required=False,
            is_access_key_required=True
        )
        return instance

    
    def test_reference_type_property(self):
        """
        Test reference_type property
        """
        test_value = 'sonwubccsploswbmpomq'
        self.instance.reference_type = test_value
        self.assertEqual(self.instance.reference_type, test_value)
    
    def test_reference_id_property(self):
        """
        Test reference_id property
        """
        test_value = int(21)
        self.instance.reference_id = test_value
        self.assertEqual(self.instance.reference_id, test_value)
    
    def test_title_property(self):
        """
        Test title property
        """
        test_value = 'whfwhqrajmgzyscgspyd'
        self.instance.title = test_value
        self.assertEqual(self.instance.title, test_value)
    
    def test_is_pay_at_location_property(self):
        """
        Test is_pay_at_location property
        """
        test_value = True
        self.instance.is_pay_at_location = test_value
        self.assertEqual(self.instance.is_pay_at_location, test_value)
    
    def test_is_membership_required_property(self):
        """
        Test is_membership_required property
        """
        test_value = False
        self.instance.is_membership_required = test_value
        self.assertEqual(self.instance.is_membership_required, test_value)
    
    def test_is_access_key_required_property(self):
        """
        Test is_access_key_required property
        """
        test_value = True
        self.instance.is_access_key_required = test_value
        self.assertEqual(self.instance.is_access_key_required, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = UsageType.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = UsageType.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

