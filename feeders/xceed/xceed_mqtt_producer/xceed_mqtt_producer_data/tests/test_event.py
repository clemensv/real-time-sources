"""
Test case for Event
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from xceed_mqtt_producer_data.event import Event
import datetime


class Test_Event(unittest.TestCase):
    """
    Test case for Event
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Event.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Event for testing
        """
        instance = Event(
            event_id='bicyecaperjlzjhczzid',
            legacy_id=int(39),
            name='ebmxvbsnhqakbtkbbtrq',
            slug='wkcswzuayxdbhlhgifyb',
            starting_time=datetime.datetime.now(datetime.timezone.utc),
            ending_time=datetime.datetime.now(datetime.timezone.utc),
            cover_url='whwjbkvrkoaopfcgerbu',
            external_sales_url='hgmgzezhfbberbunzrrq',
            venue_id='aacncemfumnvivonxeiy',
            venue_name='egsjeajynezhqdvajgdc',
            venue_city='pmdlqkgrbsqoeqyukalv',
            venue_country_code='ykpgxgilenalpbztxakb'
        )
        return instance

    
    def test_event_id_property(self):
        """
        Test event_id property
        """
        test_value = 'bicyecaperjlzjhczzid'
        self.instance.event_id = test_value
        self.assertEqual(self.instance.event_id, test_value)
    
    def test_legacy_id_property(self):
        """
        Test legacy_id property
        """
        test_value = int(39)
        self.instance.legacy_id = test_value
        self.assertEqual(self.instance.legacy_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'ebmxvbsnhqakbtkbbtrq'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_slug_property(self):
        """
        Test slug property
        """
        test_value = 'wkcswzuayxdbhlhgifyb'
        self.instance.slug = test_value
        self.assertEqual(self.instance.slug, test_value)
    
    def test_starting_time_property(self):
        """
        Test starting_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.starting_time = test_value
        self.assertEqual(self.instance.starting_time, test_value)
    
    def test_ending_time_property(self):
        """
        Test ending_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.ending_time = test_value
        self.assertEqual(self.instance.ending_time, test_value)
    
    def test_cover_url_property(self):
        """
        Test cover_url property
        """
        test_value = 'whwjbkvrkoaopfcgerbu'
        self.instance.cover_url = test_value
        self.assertEqual(self.instance.cover_url, test_value)
    
    def test_external_sales_url_property(self):
        """
        Test external_sales_url property
        """
        test_value = 'hgmgzezhfbberbunzrrq'
        self.instance.external_sales_url = test_value
        self.assertEqual(self.instance.external_sales_url, test_value)
    
    def test_venue_id_property(self):
        """
        Test venue_id property
        """
        test_value = 'aacncemfumnvivonxeiy'
        self.instance.venue_id = test_value
        self.assertEqual(self.instance.venue_id, test_value)
    
    def test_venue_name_property(self):
        """
        Test venue_name property
        """
        test_value = 'egsjeajynezhqdvajgdc'
        self.instance.venue_name = test_value
        self.assertEqual(self.instance.venue_name, test_value)
    
    def test_venue_city_property(self):
        """
        Test venue_city property
        """
        test_value = 'pmdlqkgrbsqoeqyukalv'
        self.instance.venue_city = test_value
        self.assertEqual(self.instance.venue_city, test_value)
    
    def test_venue_country_code_property(self):
        """
        Test venue_country_code property
        """
        test_value = 'ykpgxgilenalpbztxakb'
        self.instance.venue_country_code = test_value
        self.assertEqual(self.instance.venue_country_code, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Event.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Event.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

