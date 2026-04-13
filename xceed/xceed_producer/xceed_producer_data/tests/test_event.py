"""
Test case for Event
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from xceed_producer_data.event import Event
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
            event_id='wgzgrybkygotzjsusede',
            legacy_id=int(86),
            name='mwchgztbjmuwkaitvwvh',
            slug='fojucagdwcvscfyibltd',
            starting_time=datetime.datetime.now(datetime.timezone.utc),
            ending_time=datetime.datetime.now(datetime.timezone.utc),
            cover_url='exmvqzutmrapvasguogc',
            external_sales_url='vqbngznaaobxdjpaewlf',
            venue_id='iwuebkgbmuendihjllog',
            venue_name='jjprmzhcnipxjooqkhpe',
            venue_city='zknvungijfdevvjczggi',
            venue_country_code='cazralggxfxxhempcueb'
        )
        return instance

    
    def test_event_id_property(self):
        """
        Test event_id property
        """
        test_value = 'wgzgrybkygotzjsusede'
        self.instance.event_id = test_value
        self.assertEqual(self.instance.event_id, test_value)
    
    def test_legacy_id_property(self):
        """
        Test legacy_id property
        """
        test_value = int(86)
        self.instance.legacy_id = test_value
        self.assertEqual(self.instance.legacy_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'mwchgztbjmuwkaitvwvh'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_slug_property(self):
        """
        Test slug property
        """
        test_value = 'fojucagdwcvscfyibltd'
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
        test_value = 'exmvqzutmrapvasguogc'
        self.instance.cover_url = test_value
        self.assertEqual(self.instance.cover_url, test_value)
    
    def test_external_sales_url_property(self):
        """
        Test external_sales_url property
        """
        test_value = 'vqbngznaaobxdjpaewlf'
        self.instance.external_sales_url = test_value
        self.assertEqual(self.instance.external_sales_url, test_value)
    
    def test_venue_id_property(self):
        """
        Test venue_id property
        """
        test_value = 'iwuebkgbmuendihjllog'
        self.instance.venue_id = test_value
        self.assertEqual(self.instance.venue_id, test_value)
    
    def test_venue_name_property(self):
        """
        Test venue_name property
        """
        test_value = 'jjprmzhcnipxjooqkhpe'
        self.instance.venue_name = test_value
        self.assertEqual(self.instance.venue_name, test_value)
    
    def test_venue_city_property(self):
        """
        Test venue_city property
        """
        test_value = 'zknvungijfdevvjczggi'
        self.instance.venue_city = test_value
        self.assertEqual(self.instance.venue_city, test_value)
    
    def test_venue_country_code_property(self):
        """
        Test venue_country_code property
        """
        test_value = 'cazralggxfxxhempcueb'
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

