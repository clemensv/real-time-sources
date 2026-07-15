"""
Test case for Country
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from open_charge_map_amqp_producer_data.io.openchargemap.country import Country


class Test_Country(unittest.TestCase):
    """
    Test case for Country
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Country.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Country for testing
        """
        instance = Country(
            reference_type='tbpjqdkqylrxpnctjnwe',
            reference_id=int(84),
            title='jbstkxeuooyylyiaeeum',
            iso_code='jitdaxbnmyrphfrwwynj',
            continent_code='zjoamwqannlrnnxjfjsr'
        )
        return instance

    
    def test_reference_type_property(self):
        """
        Test reference_type property
        """
        test_value = 'tbpjqdkqylrxpnctjnwe'
        self.instance.reference_type = test_value
        self.assertEqual(self.instance.reference_type, test_value)
    
    def test_reference_id_property(self):
        """
        Test reference_id property
        """
        test_value = int(84)
        self.instance.reference_id = test_value
        self.assertEqual(self.instance.reference_id, test_value)
    
    def test_title_property(self):
        """
        Test title property
        """
        test_value = 'jbstkxeuooyylyiaeeum'
        self.instance.title = test_value
        self.assertEqual(self.instance.title, test_value)
    
    def test_iso_code_property(self):
        """
        Test iso_code property
        """
        test_value = 'jitdaxbnmyrphfrwwynj'
        self.instance.iso_code = test_value
        self.assertEqual(self.instance.iso_code, test_value)
    
    def test_continent_code_property(self):
        """
        Test continent_code property
        """
        test_value = 'zjoamwqannlrnnxjfjsr'
        self.instance.continent_code = test_value
        self.assertEqual(self.instance.continent_code, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Country.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Country.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

