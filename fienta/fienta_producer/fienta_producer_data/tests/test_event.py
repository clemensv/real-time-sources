"""
Test case for Event
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from fienta_producer_data.event import Event


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
            event_id='fqdcajvabhgbfbvdoced',
            name='daagywylgwgmlgogixod',
            slug='rnpdmzfmrqmtlugutrwn',
            description='btiaccubbjoaugrlajgw',
            start='slitotirndozzlaynjcr',
            end='chezpltnpuuyhzpogcbd',
            timezone='ewsmwejvzgrryieoqlnq',
            url='nypzglwovhefgqdbqeht',
            language='cnwkolkybhfxsipzynli',
            currency='aftyamrewhtvzhqtkiln',
            status='yyzohusiyntyrwmpztby',
            sale_status='vglfwyrokskwitxovlpw',
            is_online=True,
            is_free=False,
            location='jkgnfofjtngbeapvnphx',
            country='qgmvousqbmuvgyaofjih',
            region='reirmbppmmaetzseupek',
            image_url='vqdtwqsjsoqcdvfaxfwg',
            organizer_name='jyakpxkkfbsiltdbrogm',
            organizer_url='ttxfatunrgnbjutbgbms',
            categories={"test": "test"},
            created_at='khmojnhebopzcmqzwqhm',
            updated_at='yayembxhzirmvzwvrqno'
        )
        return instance

    
    def test_event_id_property(self):
        """
        Test event_id property
        """
        test_value = 'fqdcajvabhgbfbvdoced'
        self.instance.event_id = test_value
        self.assertEqual(self.instance.event_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'daagywylgwgmlgogixod'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_slug_property(self):
        """
        Test slug property
        """
        test_value = 'rnpdmzfmrqmtlugutrwn'
        self.instance.slug = test_value
        self.assertEqual(self.instance.slug, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'btiaccubbjoaugrlajgw'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_start_property(self):
        """
        Test start property
        """
        test_value = 'slitotirndozzlaynjcr'
        self.instance.start = test_value
        self.assertEqual(self.instance.start, test_value)
    
    def test_end_property(self):
        """
        Test end property
        """
        test_value = 'chezpltnpuuyhzpogcbd'
        self.instance.end = test_value
        self.assertEqual(self.instance.end, test_value)
    
    def test_timezone_property(self):
        """
        Test timezone property
        """
        test_value = 'ewsmwejvzgrryieoqlnq'
        self.instance.timezone = test_value
        self.assertEqual(self.instance.timezone, test_value)
    
    def test_url_property(self):
        """
        Test url property
        """
        test_value = 'nypzglwovhefgqdbqeht'
        self.instance.url = test_value
        self.assertEqual(self.instance.url, test_value)
    
    def test_language_property(self):
        """
        Test language property
        """
        test_value = 'cnwkolkybhfxsipzynli'
        self.instance.language = test_value
        self.assertEqual(self.instance.language, test_value)
    
    def test_currency_property(self):
        """
        Test currency property
        """
        test_value = 'aftyamrewhtvzhqtkiln'
        self.instance.currency = test_value
        self.assertEqual(self.instance.currency, test_value)
    
    def test_status_property(self):
        """
        Test status property
        """
        test_value = 'yyzohusiyntyrwmpztby'
        self.instance.status = test_value
        self.assertEqual(self.instance.status, test_value)
    
    def test_sale_status_property(self):
        """
        Test sale_status property
        """
        test_value = 'vglfwyrokskwitxovlpw'
        self.instance.sale_status = test_value
        self.assertEqual(self.instance.sale_status, test_value)
    
    def test_is_online_property(self):
        """
        Test is_online property
        """
        test_value = True
        self.instance.is_online = test_value
        self.assertEqual(self.instance.is_online, test_value)
    
    def test_is_free_property(self):
        """
        Test is_free property
        """
        test_value = False
        self.instance.is_free = test_value
        self.assertEqual(self.instance.is_free, test_value)
    
    def test_location_property(self):
        """
        Test location property
        """
        test_value = 'jkgnfofjtngbeapvnphx'
        self.instance.location = test_value
        self.assertEqual(self.instance.location, test_value)
    
    def test_country_property(self):
        """
        Test country property
        """
        test_value = 'qgmvousqbmuvgyaofjih'
        self.instance.country = test_value
        self.assertEqual(self.instance.country, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'reirmbppmmaetzseupek'
        self.instance.region = test_value
        self.assertEqual(self.instance.region, test_value)
    
    def test_image_url_property(self):
        """
        Test image_url property
        """
        test_value = 'vqdtwqsjsoqcdvfaxfwg'
        self.instance.image_url = test_value
        self.assertEqual(self.instance.image_url, test_value)
    
    def test_organizer_name_property(self):
        """
        Test organizer_name property
        """
        test_value = 'jyakpxkkfbsiltdbrogm'
        self.instance.organizer_name = test_value
        self.assertEqual(self.instance.organizer_name, test_value)
    
    def test_organizer_url_property(self):
        """
        Test organizer_url property
        """
        test_value = 'ttxfatunrgnbjutbgbms'
        self.instance.organizer_url = test_value
        self.assertEqual(self.instance.organizer_url, test_value)
    
    def test_categories_property(self):
        """
        Test categories property
        """
        test_value = {"test": "test"}
        self.instance.categories = test_value
        self.assertEqual(self.instance.categories, test_value)
    
    def test_created_at_property(self):
        """
        Test created_at property
        """
        test_value = 'khmojnhebopzcmqzwqhm'
        self.instance.created_at = test_value
        self.assertEqual(self.instance.created_at, test_value)
    
    def test_updated_at_property(self):
        """
        Test updated_at property
        """
        test_value = 'yayembxhzirmvzwvrqno'
        self.instance.updated_at = test_value
        self.assertEqual(self.instance.updated_at, test_value)
    
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

