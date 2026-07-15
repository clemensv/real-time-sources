"""
Test case for ChargerType
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from open_charge_map_producer_data.io.openchargemap.chargertype import ChargerType


class Test_ChargerType(unittest.TestCase):
    """
    Test case for ChargerType
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_ChargerType.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of ChargerType for testing
        """
        instance = ChargerType(
            reference_type='bqzcggwjdspjxhjeeala',
            reference_id=int(55),
            title='rhbfbvpbhtcmpgowzpzo',
            comments='jketukdytkvzhoftiluo',
            is_fast_charge_capable=False
        )
        return instance

    
    def test_reference_type_property(self):
        """
        Test reference_type property
        """
        test_value = 'bqzcggwjdspjxhjeeala'
        self.instance.reference_type = test_value
        self.assertEqual(self.instance.reference_type, test_value)
    
    def test_reference_id_property(self):
        """
        Test reference_id property
        """
        test_value = int(55)
        self.instance.reference_id = test_value
        self.assertEqual(self.instance.reference_id, test_value)
    
    def test_title_property(self):
        """
        Test title property
        """
        test_value = 'rhbfbvpbhtcmpgowzpzo'
        self.instance.title = test_value
        self.assertEqual(self.instance.title, test_value)
    
    def test_comments_property(self):
        """
        Test comments property
        """
        test_value = 'jketukdytkvzhoftiluo'
        self.instance.comments = test_value
        self.assertEqual(self.instance.comments, test_value)
    
    def test_is_fast_charge_capable_property(self):
        """
        Test is_fast_charge_capable property
        """
        test_value = False
        self.instance.is_fast_charge_capable = test_value
        self.assertEqual(self.instance.is_fast_charge_capable, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = ChargerType.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = ChargerType.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

