"""
Test case for BikeshareSystem
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from tokyo_docomo_bikeshare_mqtt_producer_data.bikesharesystem import BikeshareSystem


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
            system_id='qrwkhryxedkkfevwwrdh',
            language='zzrooxfvbkpytnxfmquo',
            name='smdysackjymocmjonkag',
            short_name='bdvnedzdntawwvggorzi',
            operator='oqgmbnwbwzopevntvdfa',
            url='xpgzdbhpxexmiizjutku',
            purchase_url='agrsbjaxhmrpbsoaprpx',
            start_date='ajqcvmhlrxmjoapowkuc',
            phone_number='ceicfaqnsflalphshqgz',
            email='jwyajzeocgyqcihvwikh',
            feed_contact_email='uyrtluxvuyvmissjcscr',
            timezone='afrssjmtvikoanbgvznk',
            license_url='fhtlzurqfxqxcqagdaic'
        )
        return instance

    
    def test_system_id_property(self):
        """
        Test system_id property
        """
        test_value = 'qrwkhryxedkkfevwwrdh'
        self.instance.system_id = test_value
        self.assertEqual(self.instance.system_id, test_value)
    
    def test_language_property(self):
        """
        Test language property
        """
        test_value = 'zzrooxfvbkpytnxfmquo'
        self.instance.language = test_value
        self.assertEqual(self.instance.language, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'smdysackjymocmjonkag'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_short_name_property(self):
        """
        Test short_name property
        """
        test_value = 'bdvnedzdntawwvggorzi'
        self.instance.short_name = test_value
        self.assertEqual(self.instance.short_name, test_value)
    
    def test_operator_property(self):
        """
        Test operator property
        """
        test_value = 'oqgmbnwbwzopevntvdfa'
        self.instance.operator = test_value
        self.assertEqual(self.instance.operator, test_value)
    
    def test_url_property(self):
        """
        Test url property
        """
        test_value = 'xpgzdbhpxexmiizjutku'
        self.instance.url = test_value
        self.assertEqual(self.instance.url, test_value)
    
    def test_purchase_url_property(self):
        """
        Test purchase_url property
        """
        test_value = 'agrsbjaxhmrpbsoaprpx'
        self.instance.purchase_url = test_value
        self.assertEqual(self.instance.purchase_url, test_value)
    
    def test_start_date_property(self):
        """
        Test start_date property
        """
        test_value = 'ajqcvmhlrxmjoapowkuc'
        self.instance.start_date = test_value
        self.assertEqual(self.instance.start_date, test_value)
    
    def test_phone_number_property(self):
        """
        Test phone_number property
        """
        test_value = 'ceicfaqnsflalphshqgz'
        self.instance.phone_number = test_value
        self.assertEqual(self.instance.phone_number, test_value)
    
    def test_email_property(self):
        """
        Test email property
        """
        test_value = 'jwyajzeocgyqcihvwikh'
        self.instance.email = test_value
        self.assertEqual(self.instance.email, test_value)
    
    def test_feed_contact_email_property(self):
        """
        Test feed_contact_email property
        """
        test_value = 'uyrtluxvuyvmissjcscr'
        self.instance.feed_contact_email = test_value
        self.assertEqual(self.instance.feed_contact_email, test_value)
    
    def test_timezone_property(self):
        """
        Test timezone property
        """
        test_value = 'afrssjmtvikoanbgvznk'
        self.instance.timezone = test_value
        self.assertEqual(self.instance.timezone, test_value)
    
    def test_license_url_property(self):
        """
        Test license_url property
        """
        test_value = 'fhtlzurqfxqxcqagdaic'
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

