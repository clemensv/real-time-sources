"""
Test case for EventSaleStatus
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from fienta_producer_data.eventsalestatus import EventSaleStatus


class Test_EventSaleStatus(unittest.TestCase):
    """
    Test case for EventSaleStatus
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_EventSaleStatus.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of EventSaleStatus for testing
        """
        instance = EventSaleStatus(
            event_id='vffhotwprfnryxngykcg',
            name='pmvpefkzyflmwqrvddam',
            sale_status='ecndvjhandrwkqdwaozp',
            status='cbmvfwsmrssjfskxvafv',
            start='mynsrqthjkncveermlch',
            url='yqpgvxclovclpiirvrni',
            updated_at='invakmfdlijvddxblmnh'
        )
        return instance

    
    def test_event_id_property(self):
        """
        Test event_id property
        """
        test_value = 'vffhotwprfnryxngykcg'
        self.instance.event_id = test_value
        self.assertEqual(self.instance.event_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'pmvpefkzyflmwqrvddam'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_sale_status_property(self):
        """
        Test sale_status property
        """
        test_value = 'ecndvjhandrwkqdwaozp'
        self.instance.sale_status = test_value
        self.assertEqual(self.instance.sale_status, test_value)
    
    def test_status_property(self):
        """
        Test status property
        """
        test_value = 'cbmvfwsmrssjfskxvafv'
        self.instance.status = test_value
        self.assertEqual(self.instance.status, test_value)
    
    def test_start_property(self):
        """
        Test start property
        """
        test_value = 'mynsrqthjkncveermlch'
        self.instance.start = test_value
        self.assertEqual(self.instance.start, test_value)
    
    def test_url_property(self):
        """
        Test url property
        """
        test_value = 'yqpgvxclovclpiirvrni'
        self.instance.url = test_value
        self.assertEqual(self.instance.url, test_value)
    
    def test_updated_at_property(self):
        """
        Test updated_at property
        """
        test_value = 'invakmfdlijvddxblmnh'
        self.instance.updated_at = test_value
        self.assertEqual(self.instance.updated_at, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = EventSaleStatus.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = EventSaleStatus.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

