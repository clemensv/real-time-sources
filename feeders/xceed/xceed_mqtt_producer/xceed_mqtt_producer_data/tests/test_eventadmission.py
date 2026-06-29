"""
Test case for EventAdmission
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from xceed_mqtt_producer_data.eventadmission import EventAdmission


class Test_EventAdmission(unittest.TestCase):
    """
    Test case for EventAdmission
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_EventAdmission.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of EventAdmission for testing
        """
        instance = EventAdmission(
            event_id='bzpoluiiyylglsitzsob',
            admission_id='hhlzkvcyvqfevexxywkr',
            admission_type='jdjhcowwrujbqoduurbn',
            name='azugdfuvbzonplzpvcqp',
            is_sold_out=True,
            is_sales_closed=False,
            price=float(27.389603463895074),
            currency='odxvnmjbfqihhnglidna',
            remaining=int(6)
        )
        return instance

    
    def test_event_id_property(self):
        """
        Test event_id property
        """
        test_value = 'bzpoluiiyylglsitzsob'
        self.instance.event_id = test_value
        self.assertEqual(self.instance.event_id, test_value)
    
    def test_admission_id_property(self):
        """
        Test admission_id property
        """
        test_value = 'hhlzkvcyvqfevexxywkr'
        self.instance.admission_id = test_value
        self.assertEqual(self.instance.admission_id, test_value)
    
    def test_admission_type_property(self):
        """
        Test admission_type property
        """
        test_value = 'jdjhcowwrujbqoduurbn'
        self.instance.admission_type = test_value
        self.assertEqual(self.instance.admission_type, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'azugdfuvbzonplzpvcqp'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_is_sold_out_property(self):
        """
        Test is_sold_out property
        """
        test_value = True
        self.instance.is_sold_out = test_value
        self.assertEqual(self.instance.is_sold_out, test_value)
    
    def test_is_sales_closed_property(self):
        """
        Test is_sales_closed property
        """
        test_value = False
        self.instance.is_sales_closed = test_value
        self.assertEqual(self.instance.is_sales_closed, test_value)
    
    def test_price_property(self):
        """
        Test price property
        """
        test_value = float(27.389603463895074)
        self.instance.price = test_value
        self.assertEqual(self.instance.price, test_value)
    
    def test_currency_property(self):
        """
        Test currency property
        """
        test_value = 'odxvnmjbfqihhnglidna'
        self.instance.currency = test_value
        self.assertEqual(self.instance.currency, test_value)
    
    def test_remaining_property(self):
        """
        Test remaining property
        """
        test_value = int(6)
        self.instance.remaining = test_value
        self.assertEqual(self.instance.remaining, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = EventAdmission.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = EventAdmission.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

