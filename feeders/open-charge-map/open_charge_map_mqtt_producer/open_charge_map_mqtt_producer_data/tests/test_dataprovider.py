"""
Test case for DataProvider
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from open_charge_map_mqtt_producer_data.io.openchargemap.dataprovider import DataProvider


class Test_DataProvider(unittest.TestCase):
    """
    Test case for DataProvider
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_DataProvider.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of DataProvider for testing
        """
        instance = DataProvider(
            reference_type='usivckurmahmlgloqxhc',
            reference_id=int(38),
            title='qqytralbigwvmulhqfza',
            website_url='vjrsatxxiohslpkyivdv',
            comments='yoxtiinoerczrsgpfvil',
            license='uwdqvdcgfpesnqrdwrdu',
            is_open_data_licensed=True,
            is_restricted_edit=True,
            is_approved_import=True,
            status_title='awzntbqbolrjzyjboahj',
            is_provider_enabled=False
        )
        return instance

    
    def test_reference_type_property(self):
        """
        Test reference_type property
        """
        test_value = 'usivckurmahmlgloqxhc'
        self.instance.reference_type = test_value
        self.assertEqual(self.instance.reference_type, test_value)
    
    def test_reference_id_property(self):
        """
        Test reference_id property
        """
        test_value = int(38)
        self.instance.reference_id = test_value
        self.assertEqual(self.instance.reference_id, test_value)
    
    def test_title_property(self):
        """
        Test title property
        """
        test_value = 'qqytralbigwvmulhqfza'
        self.instance.title = test_value
        self.assertEqual(self.instance.title, test_value)
    
    def test_website_url_property(self):
        """
        Test website_url property
        """
        test_value = 'vjrsatxxiohslpkyivdv'
        self.instance.website_url = test_value
        self.assertEqual(self.instance.website_url, test_value)
    
    def test_comments_property(self):
        """
        Test comments property
        """
        test_value = 'yoxtiinoerczrsgpfvil'
        self.instance.comments = test_value
        self.assertEqual(self.instance.comments, test_value)
    
    def test_license_property(self):
        """
        Test license property
        """
        test_value = 'uwdqvdcgfpesnqrdwrdu'
        self.instance.license = test_value
        self.assertEqual(self.instance.license, test_value)
    
    def test_is_open_data_licensed_property(self):
        """
        Test is_open_data_licensed property
        """
        test_value = True
        self.instance.is_open_data_licensed = test_value
        self.assertEqual(self.instance.is_open_data_licensed, test_value)
    
    def test_is_restricted_edit_property(self):
        """
        Test is_restricted_edit property
        """
        test_value = True
        self.instance.is_restricted_edit = test_value
        self.assertEqual(self.instance.is_restricted_edit, test_value)
    
    def test_is_approved_import_property(self):
        """
        Test is_approved_import property
        """
        test_value = True
        self.instance.is_approved_import = test_value
        self.assertEqual(self.instance.is_approved_import, test_value)
    
    def test_status_title_property(self):
        """
        Test status_title property
        """
        test_value = 'awzntbqbolrjzyjboahj'
        self.instance.status_title = test_value
        self.assertEqual(self.instance.status_title, test_value)
    
    def test_is_provider_enabled_property(self):
        """
        Test is_provider_enabled property
        """
        test_value = False
        self.instance.is_provider_enabled = test_value
        self.assertEqual(self.instance.is_provider_enabled, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = DataProvider.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = DataProvider.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

