"""
Test case for BikeshareSystem
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from tokyo_docomo_bikeshare_amqp_producer_data.bikesharesystem import BikeshareSystem


class Test_BikeshareSystem(unittest.TestCase):
    """
    Test case for BikeshareSystem
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_BikeshareSystem.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of BikeshareSystem for testing
        """
        instance = BikeshareSystem(
            system_id='frsiftdqweyufyppqtec',
            language='cimmuihrpzxrrjbzytme',
            name='okfbupjzxhcvfktbyahf',
            short_name='kforbicqgajatasxyjre',
            operator='sybxvxglmoydzsaodnio',
            url='zdhnpciprtkzifywsazt',
            purchase_url='eteaduwspxjkzsmxajko',
            start_date='lybthzmwncsfiotwcvfy',
            phone_number='umcqiykjwtkkbyyzkxqz',
            email='ouirqyhfvcrzziqiabqv',
            feed_contact_email='uhamcxwuaxqhxnuwfjvz',
            timezone='vlfiqdgwlwwbqidyozur',
            license_url='hdxmaxejtrpuozauneyl'
        )
        return instance

    
    def test_system_id_property(self):
        """
        Test system_id property
        """
        test_value = 'frsiftdqweyufyppqtec'
        self.instance.system_id = test_value
        self.assertEqual(self.instance.system_id, test_value)
    
    def test_language_property(self):
        """
        Test language property
        """
        test_value = 'cimmuihrpzxrrjbzytme'
        self.instance.language = test_value
        self.assertEqual(self.instance.language, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'okfbupjzxhcvfktbyahf'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_short_name_property(self):
        """
        Test short_name property
        """
        test_value = 'kforbicqgajatasxyjre'
        self.instance.short_name = test_value
        self.assertEqual(self.instance.short_name, test_value)
    
    def test_operator_property(self):
        """
        Test operator property
        """
        test_value = 'sybxvxglmoydzsaodnio'
        self.instance.operator = test_value
        self.assertEqual(self.instance.operator, test_value)
    
    def test_url_property(self):
        """
        Test url property
        """
        test_value = 'zdhnpciprtkzifywsazt'
        self.instance.url = test_value
        self.assertEqual(self.instance.url, test_value)
    
    def test_purchase_url_property(self):
        """
        Test purchase_url property
        """
        test_value = 'eteaduwspxjkzsmxajko'
        self.instance.purchase_url = test_value
        self.assertEqual(self.instance.purchase_url, test_value)
    
    def test_start_date_property(self):
        """
        Test start_date property
        """
        test_value = 'lybthzmwncsfiotwcvfy'
        self.instance.start_date = test_value
        self.assertEqual(self.instance.start_date, test_value)
    
    def test_phone_number_property(self):
        """
        Test phone_number property
        """
        test_value = 'umcqiykjwtkkbyyzkxqz'
        self.instance.phone_number = test_value
        self.assertEqual(self.instance.phone_number, test_value)
    
    def test_email_property(self):
        """
        Test email property
        """
        test_value = 'ouirqyhfvcrzziqiabqv'
        self.instance.email = test_value
        self.assertEqual(self.instance.email, test_value)
    
    def test_feed_contact_email_property(self):
        """
        Test feed_contact_email property
        """
        test_value = 'uhamcxwuaxqhxnuwfjvz'
        self.instance.feed_contact_email = test_value
        self.assertEqual(self.instance.feed_contact_email, test_value)
    
    def test_timezone_property(self):
        """
        Test timezone property
        """
        test_value = 'vlfiqdgwlwwbqidyozur'
        self.instance.timezone = test_value
        self.assertEqual(self.instance.timezone, test_value)
    
    def test_license_url_property(self):
        """
        Test license_url property
        """
        test_value = 'hdxmaxejtrpuozauneyl'
        self.instance.license_url = test_value
        self.assertEqual(self.instance.license_url, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = BikeshareSystem.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = BikeshareSystem.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

