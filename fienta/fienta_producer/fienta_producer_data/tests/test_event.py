"""
Test case for Event
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from fienta_producer_data.event import Event
from typing import Any


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
            event_id='mlhdzvahadphdybrsoff',
            name='siixjbsnvqcfzuctpbgy',
            slug='stkofjmtzpewjdghpsvl',
            description='oxzxfnrvaasjjxuxgwlf',
            start='ydqcarenhxycfdeiijva',
            end='srtgycjnmzlianwvqqgt',
            timezone='udfwimufqyzrkqyrgnkt',
            url='xixsvwlycladavzvuhxz',
            language='mlsgzwglorpmnnucqhku',
            currency='vnuynweoloysvpqalvif',
            status='hnbnyamznrljrnvhdptk',
            sale_status='tflmczcjwejjdercjcmy',
            is_online=False,
            is_free=False,
            location='jfiaxkilwmtpbqrfxbvu',
            country='quxcgsktyrytrkctxakf',
            region='jpinmhfrcqdmbekadxjg',
            image_url='rxtzgemsaltmlelopweg',
            organizer_name='ftkgihbrqzfaqxvhwkpt',
            organizer_url='nkbpcuoktmvyqxenavaq',
            categories=None,
            created_at='slllnnlfghlrglnyrqag',
            updated_at='aeqcxvyzkvctgnhfxjkl'
        )
        return instance

    
    def test_event_id_property(self):
        """
        Test event_id property
        """
        test_value = 'mlhdzvahadphdybrsoff'
        self.instance.event_id = test_value
        self.assertEqual(self.instance.event_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'siixjbsnvqcfzuctpbgy'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_slug_property(self):
        """
        Test slug property
        """
        test_value = 'stkofjmtzpewjdghpsvl'
        self.instance.slug = test_value
        self.assertEqual(self.instance.slug, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'oxzxfnrvaasjjxuxgwlf'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_start_property(self):
        """
        Test start property
        """
        test_value = 'ydqcarenhxycfdeiijva'
        self.instance.start = test_value
        self.assertEqual(self.instance.start, test_value)
    
    def test_end_property(self):
        """
        Test end property
        """
        test_value = 'srtgycjnmzlianwvqqgt'
        self.instance.end = test_value
        self.assertEqual(self.instance.end, test_value)
    
    def test_timezone_property(self):
        """
        Test timezone property
        """
        test_value = 'udfwimufqyzrkqyrgnkt'
        self.instance.timezone = test_value
        self.assertEqual(self.instance.timezone, test_value)
    
    def test_url_property(self):
        """
        Test url property
        """
        test_value = 'xixsvwlycladavzvuhxz'
        self.instance.url = test_value
        self.assertEqual(self.instance.url, test_value)
    
    def test_language_property(self):
        """
        Test language property
        """
        test_value = 'mlsgzwglorpmnnucqhku'
        self.instance.language = test_value
        self.assertEqual(self.instance.language, test_value)
    
    def test_currency_property(self):
        """
        Test currency property
        """
        test_value = 'vnuynweoloysvpqalvif'
        self.instance.currency = test_value
        self.assertEqual(self.instance.currency, test_value)
    
    def test_status_property(self):
        """
        Test status property
        """
        test_value = 'hnbnyamznrljrnvhdptk'
        self.instance.status = test_value
        self.assertEqual(self.instance.status, test_value)
    
    def test_sale_status_property(self):
        """
        Test sale_status property
        """
        test_value = 'tflmczcjwejjdercjcmy'
        self.instance.sale_status = test_value
        self.assertEqual(self.instance.sale_status, test_value)
    
    def test_is_online_property(self):
        """
        Test is_online property
        """
        test_value = False
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
        test_value = 'jfiaxkilwmtpbqrfxbvu'
        self.instance.location = test_value
        self.assertEqual(self.instance.location, test_value)
    
    def test_country_property(self):
        """
        Test country property
        """
        test_value = 'quxcgsktyrytrkctxakf'
        self.instance.country = test_value
        self.assertEqual(self.instance.country, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'jpinmhfrcqdmbekadxjg'
        self.instance.region = test_value
        self.assertEqual(self.instance.region, test_value)
    
    def test_image_url_property(self):
        """
        Test image_url property
        """
        test_value = 'rxtzgemsaltmlelopweg'
        self.instance.image_url = test_value
        self.assertEqual(self.instance.image_url, test_value)
    
    def test_organizer_name_property(self):
        """
        Test organizer_name property
        """
        test_value = 'ftkgihbrqzfaqxvhwkpt'
        self.instance.organizer_name = test_value
        self.assertEqual(self.instance.organizer_name, test_value)
    
    def test_organizer_url_property(self):
        """
        Test organizer_url property
        """
        test_value = 'nkbpcuoktmvyqxenavaq'
        self.instance.organizer_url = test_value
        self.assertEqual(self.instance.organizer_url, test_value)
    
    def test_categories_property(self):
        """
        Test categories property
        """
        test_value = None
        self.instance.categories = test_value
        self.assertEqual(self.instance.categories, test_value)
    
    def test_created_at_property(self):
        """
        Test created_at property
        """
        test_value = 'slllnnlfghlrglnyrqag'
        self.instance.created_at = test_value
        self.assertEqual(self.instance.created_at, test_value)
    
    def test_updated_at_property(self):
        """
        Test updated_at property
        """
        test_value = 'aeqcxvyzkvctgnhfxjkl'
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

