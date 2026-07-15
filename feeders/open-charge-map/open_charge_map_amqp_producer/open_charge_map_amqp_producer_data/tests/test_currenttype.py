"""
Test case for CurrentType
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from open_charge_map_amqp_producer_data.io.openchargemap.currenttype import CurrentType


class Test_CurrentType(unittest.TestCase):
    """
    Test case for CurrentType
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_CurrentType.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of CurrentType for testing
        """
        instance = CurrentType(
            reference_type='kgwlbpucshldtpfamuls',
            reference_id=int(76),
            title='ihuoejwzdpltzeatpjeb',
            description='yhlcynppxejthdilkual'
        )
        return instance

    
    def test_reference_type_property(self):
        """
        Test reference_type property
        """
        test_value = 'kgwlbpucshldtpfamuls'
        self.instance.reference_type = test_value
        self.assertEqual(self.instance.reference_type, test_value)
    
    def test_reference_id_property(self):
        """
        Test reference_id property
        """
        test_value = int(76)
        self.instance.reference_id = test_value
        self.assertEqual(self.instance.reference_id, test_value)
    
    def test_title_property(self):
        """
        Test title property
        """
        test_value = 'ihuoejwzdpltzeatpjeb'
        self.instance.title = test_value
        self.assertEqual(self.instance.title, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'yhlcynppxejthdilkual'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = CurrentType.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = CurrentType.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

