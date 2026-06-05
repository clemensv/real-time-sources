"""
Test case for TsunamiBulletin
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ptwc_tsunami_producer_data.tsunamibulletin import TsunamiBulletin
from ptwc_tsunami_producer_data.categoryenum import CategoryEnum
from ptwc_tsunami_producer_data.basinenum import BasinEnum
from ptwc_tsunami_producer_data.feedenum import FeedEnum
from ptwc_tsunami_producer_data.ptwclevelenum import PtwcLevelenum
import datetime


class Test_TsunamiBulletin(unittest.TestCase):
    """
    Test case for TsunamiBulletin
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_TsunamiBulletin.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of TsunamiBulletin for testing
        """
        instance = TsunamiBulletin(
            bulletin_id='bigiwlzpelkxhyohxhog',
            feed=FeedEnum.PAAQ,
            center='gprpyxkldnsbxqfnwiqy',
            title='kxaaumzkblauwncfhcvj',
            updated=datetime.datetime.now(datetime.timezone.utc),
            latitude=float(79.54115307547934),
            longitude=float(8.376079045369734),
            category=CategoryEnum.Warning,
            magnitude='vqhhocbdkpslcumevpfz',
            affected_region='sjdsbhokdhjhestfcaky',
            note='cvnbirbtjbyisgmbkbtk',
            bulletin_url='wcezhstszhvdlgwriquf',
            cap_url='ufktmfztlsytgdifvwjd',
            basin=BasinEnum.pacific,
            ptwc_level=PtwcLevelenum.warning
        )
        return instance

    
    def test_bulletin_id_property(self):
        """
        Test bulletin_id property
        """
        test_value = 'bigiwlzpelkxhyohxhog'
        self.instance.bulletin_id = test_value
        self.assertEqual(self.instance.bulletin_id, test_value)
    
    def test_feed_property(self):
        """
        Test feed property
        """
        test_value = FeedEnum.PAAQ
        self.instance.feed = test_value
        self.assertEqual(self.instance.feed, test_value)
    
    def test_center_property(self):
        """
        Test center property
        """
        test_value = 'gprpyxkldnsbxqfnwiqy'
        self.instance.center = test_value
        self.assertEqual(self.instance.center, test_value)
    
    def test_title_property(self):
        """
        Test title property
        """
        test_value = 'kxaaumzkblauwncfhcvj'
        self.instance.title = test_value
        self.assertEqual(self.instance.title, test_value)
    
    def test_updated_property(self):
        """
        Test updated property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.updated = test_value
        self.assertEqual(self.instance.updated, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(79.54115307547934)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(8.376079045369734)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_category_property(self):
        """
        Test category property
        """
        test_value = CategoryEnum.Warning
        self.instance.category = test_value
        self.assertEqual(self.instance.category, test_value)
    
    def test_magnitude_property(self):
        """
        Test magnitude property
        """
        test_value = 'vqhhocbdkpslcumevpfz'
        self.instance.magnitude = test_value
        self.assertEqual(self.instance.magnitude, test_value)
    
    def test_affected_region_property(self):
        """
        Test affected_region property
        """
        test_value = 'sjdsbhokdhjhestfcaky'
        self.instance.affected_region = test_value
        self.assertEqual(self.instance.affected_region, test_value)
    
    def test_note_property(self):
        """
        Test note property
        """
        test_value = 'cvnbirbtjbyisgmbkbtk'
        self.instance.note = test_value
        self.assertEqual(self.instance.note, test_value)
    
    def test_bulletin_url_property(self):
        """
        Test bulletin_url property
        """
        test_value = 'wcezhstszhvdlgwriquf'
        self.instance.bulletin_url = test_value
        self.assertEqual(self.instance.bulletin_url, test_value)
    
    def test_cap_url_property(self):
        """
        Test cap_url property
        """
        test_value = 'ufktmfztlsytgdifvwjd'
        self.instance.cap_url = test_value
        self.assertEqual(self.instance.cap_url, test_value)
    
    def test_basin_property(self):
        """
        Test basin property
        """
        test_value = BasinEnum.pacific
        self.instance.basin = test_value
        self.assertEqual(self.instance.basin, test_value)
    
    def test_ptwc_level_property(self):
        """
        Test ptwc_level property
        """
        test_value = PtwcLevelenum.warning
        self.instance.ptwc_level = test_value
        self.assertEqual(self.instance.ptwc_level, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = TsunamiBulletin.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = TsunamiBulletin.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

