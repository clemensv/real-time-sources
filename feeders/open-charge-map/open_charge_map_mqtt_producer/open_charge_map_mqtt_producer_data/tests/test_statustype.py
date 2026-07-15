"""
Test case for StatusType
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from open_charge_map_mqtt_producer_data.io.openchargemap.statustype import StatusType


class Test_StatusType(unittest.TestCase):
    """
    Test case for StatusType
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_StatusType.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of StatusType for testing
        """
        instance = StatusType(
            reference_type='pjmsvmsdpijmpxuxieov',
            reference_id=int(4),
            title='zicqcitpnvxeeepcwevx',
            is_operational=True,
            is_user_selectable=True
        )
        return instance

    
    def test_reference_type_property(self):
        """
        Test reference_type property
        """
        test_value = 'pjmsvmsdpijmpxuxieov'
        self.instance.reference_type = test_value
        self.assertEqual(self.instance.reference_type, test_value)
    
    def test_reference_id_property(self):
        """
        Test reference_id property
        """
        test_value = int(4)
        self.instance.reference_id = test_value
        self.assertEqual(self.instance.reference_id, test_value)
    
    def test_title_property(self):
        """
        Test title property
        """
        test_value = 'zicqcitpnvxeeepcwevx'
        self.instance.title = test_value
        self.assertEqual(self.instance.title, test_value)
    
    def test_is_operational_property(self):
        """
        Test is_operational property
        """
        test_value = True
        self.instance.is_operational = test_value
        self.assertEqual(self.instance.is_operational, test_value)
    
    def test_is_user_selectable_property(self):
        """
        Test is_user_selectable property
        """
        test_value = True
        self.instance.is_user_selectable = test_value
        self.assertEqual(self.instance.is_user_selectable, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = StatusType.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = StatusType.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

