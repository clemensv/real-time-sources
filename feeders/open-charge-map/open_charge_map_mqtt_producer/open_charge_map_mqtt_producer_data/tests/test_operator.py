"""
Test case for Operator
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from open_charge_map_mqtt_producer_data.io.openchargemap.operator import Operator


class Test_Operator(unittest.TestCase):
    """
    Test case for Operator
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Operator.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Operator for testing
        """
        instance = Operator(
            reference_type='zwrofalxntpmghpobzad',
            reference_id=int(13),
            title='govubdmindcpmtyykcof',
            website_url='piscjfkzzrkihmhdqdar',
            comments='jgwmuingnqbrgwfdcmbq',
            phone_primary_contact='eolxsvthnisxejyvghjn',
            phone_secondary_contact='kidpbfbealcrguduwprq',
            contact_email='vfymkvzcjecgsztsprco',
            booking_url='jbnpuiwsaqhaaaauctfe',
            fault_report_email='zazbcxvawhlfejpzplug',
            is_private_individual=False,
            is_restricted_edit=False
        )
        return instance

    
    def test_reference_type_property(self):
        """
        Test reference_type property
        """
        test_value = 'zwrofalxntpmghpobzad'
        self.instance.reference_type = test_value
        self.assertEqual(self.instance.reference_type, test_value)
    
    def test_reference_id_property(self):
        """
        Test reference_id property
        """
        test_value = int(13)
        self.instance.reference_id = test_value
        self.assertEqual(self.instance.reference_id, test_value)
    
    def test_title_property(self):
        """
        Test title property
        """
        test_value = 'govubdmindcpmtyykcof'
        self.instance.title = test_value
        self.assertEqual(self.instance.title, test_value)
    
    def test_website_url_property(self):
        """
        Test website_url property
        """
        test_value = 'piscjfkzzrkihmhdqdar'
        self.instance.website_url = test_value
        self.assertEqual(self.instance.website_url, test_value)
    
    def test_comments_property(self):
        """
        Test comments property
        """
        test_value = 'jgwmuingnqbrgwfdcmbq'
        self.instance.comments = test_value
        self.assertEqual(self.instance.comments, test_value)
    
    def test_phone_primary_contact_property(self):
        """
        Test phone_primary_contact property
        """
        test_value = 'eolxsvthnisxejyvghjn'
        self.instance.phone_primary_contact = test_value
        self.assertEqual(self.instance.phone_primary_contact, test_value)
    
    def test_phone_secondary_contact_property(self):
        """
        Test phone_secondary_contact property
        """
        test_value = 'kidpbfbealcrguduwprq'
        self.instance.phone_secondary_contact = test_value
        self.assertEqual(self.instance.phone_secondary_contact, test_value)
    
    def test_contact_email_property(self):
        """
        Test contact_email property
        """
        test_value = 'vfymkvzcjecgsztsprco'
        self.instance.contact_email = test_value
        self.assertEqual(self.instance.contact_email, test_value)
    
    def test_booking_url_property(self):
        """
        Test booking_url property
        """
        test_value = 'jbnpuiwsaqhaaaauctfe'
        self.instance.booking_url = test_value
        self.assertEqual(self.instance.booking_url, test_value)
    
    def test_fault_report_email_property(self):
        """
        Test fault_report_email property
        """
        test_value = 'zazbcxvawhlfejpzplug'
        self.instance.fault_report_email = test_value
        self.assertEqual(self.instance.fault_report_email, test_value)
    
    def test_is_private_individual_property(self):
        """
        Test is_private_individual property
        """
        test_value = False
        self.instance.is_private_individual = test_value
        self.assertEqual(self.instance.is_private_individual, test_value)
    
    def test_is_restricted_edit_property(self):
        """
        Test is_restricted_edit property
        """
        test_value = False
        self.instance.is_restricted_edit = test_value
        self.assertEqual(self.instance.is_restricted_edit, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Operator.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Operator.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

