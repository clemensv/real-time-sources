"""
Test case for ConnectionType
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from open_charge_map_producer_data.io.openchargemap.connectiontype import ConnectionType


class Test_ConnectionType(unittest.TestCase):
    """
    Test case for ConnectionType
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_ConnectionType.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of ConnectionType for testing
        """
        instance = ConnectionType(
            reference_type='wngsmgcupktguofggqhc',
            reference_id=int(77),
            title='ssdwlzwebjfsdarerpoy',
            formal_name='pijkgsmlwbftqomxqftq',
            is_discontinued=True,
            is_obsolete=False
        )
        return instance

    
    def test_reference_type_property(self):
        """
        Test reference_type property
        """
        test_value = 'wngsmgcupktguofggqhc'
        self.instance.reference_type = test_value
        self.assertEqual(self.instance.reference_type, test_value)
    
    def test_reference_id_property(self):
        """
        Test reference_id property
        """
        test_value = int(77)
        self.instance.reference_id = test_value
        self.assertEqual(self.instance.reference_id, test_value)
    
    def test_title_property(self):
        """
        Test title property
        """
        test_value = 'ssdwlzwebjfsdarerpoy'
        self.instance.title = test_value
        self.assertEqual(self.instance.title, test_value)
    
    def test_formal_name_property(self):
        """
        Test formal_name property
        """
        test_value = 'pijkgsmlwbftqomxqftq'
        self.instance.formal_name = test_value
        self.assertEqual(self.instance.formal_name, test_value)
    
    def test_is_discontinued_property(self):
        """
        Test is_discontinued property
        """
        test_value = True
        self.instance.is_discontinued = test_value
        self.assertEqual(self.instance.is_discontinued, test_value)
    
    def test_is_obsolete_property(self):
        """
        Test is_obsolete property
        """
        test_value = False
        self.instance.is_obsolete = test_value
        self.assertEqual(self.instance.is_obsolete, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = ConnectionType.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = ConnectionType.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

