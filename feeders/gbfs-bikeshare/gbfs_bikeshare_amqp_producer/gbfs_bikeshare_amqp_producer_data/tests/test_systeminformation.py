"""
Test case for SystemInformation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gbfs_bikeshare_amqp_producer_data.systeminformation import SystemInformation


class Test_SystemInformation(unittest.TestCase):
    """
    Test case for SystemInformation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_SystemInformation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of SystemInformation for testing
        """
        instance = SystemInformation(
            system_id='kqdzzjtehmybbwxbhgck',
            name='jttrneezhriojjdirogb',
            operator='lsxcjnknlpcddbupsnlc',
            url='itzrppwewmivqccrthby',
            timezone='wkdfhphstejmmhtofcsx',
            language='alimlyqvycjwvhdvdoac',
            phone_number='ttpxrniicinvzglnuupt'
        )
        return instance

    
    def test_system_id_property(self):
        """
        Test system_id property
        """
        test_value = 'kqdzzjtehmybbwxbhgck'
        self.instance.system_id = test_value
        self.assertEqual(self.instance.system_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'jttrneezhriojjdirogb'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_operator_property(self):
        """
        Test operator property
        """
        test_value = 'lsxcjnknlpcddbupsnlc'
        self.instance.operator = test_value
        self.assertEqual(self.instance.operator, test_value)
    
    def test_url_property(self):
        """
        Test url property
        """
        test_value = 'itzrppwewmivqccrthby'
        self.instance.url = test_value
        self.assertEqual(self.instance.url, test_value)
    
    def test_timezone_property(self):
        """
        Test timezone property
        """
        test_value = 'wkdfhphstejmmhtofcsx'
        self.instance.timezone = test_value
        self.assertEqual(self.instance.timezone, test_value)
    
    def test_language_property(self):
        """
        Test language property
        """
        test_value = 'alimlyqvycjwvhdvdoac'
        self.instance.language = test_value
        self.assertEqual(self.instance.language, test_value)
    
    def test_phone_number_property(self):
        """
        Test phone_number property
        """
        test_value = 'ttpxrniicinvzglnuupt'
        self.instance.phone_number = test_value
        self.assertEqual(self.instance.phone_number, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = SystemInformation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = SystemInformation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

