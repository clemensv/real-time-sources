"""
Test case for FeedItem
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditem import FeedItem
from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditemcontent import FeedItemContent
from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditemauthor import FeedItemAuthor
from rssbridge_producer_data.microsoft.opendata.rssfeeds.link import Link
from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditempublisher import FeedItemPublisher
from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditemsource import FeedItemSource
from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditemtitle import FeedItemTitle
from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditemenclosure import FeedItemEnclosure
from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditemsummary import FeedItemSummary


class Test_FeedItem(unittest.TestCase):
    """
    Test case for FeedItem
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_FeedItem.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of FeedItem for testing
        """
        instance = FeedItem(
            feed_slug='wyaimgrxswnxwyuwwqgy',
            item='gbhfyjaetrrxsnfmwclc',
            author=None,
            publisher=None,
            summary=None,
            title=None,
            source=None,
            content=[None, None],
            enclosures=[None, None, None],
            published=int(74),
            updated=int(19),
            created=int(8),
            expired=int(93),
            id='eriesuosfshlszuqkpsd',
            license='epbbbwptcxuixdiglrxl',
            comments='mnzkqkccrmlpipyjdjpq',
            contributors=[None, None],
            links=[None, None]
        )
        return instance

    
    def test_feed_slug_property(self):
        """
        Test feed_slug property
        """
        test_value = 'wyaimgrxswnxwyuwwqgy'
        self.instance.feed_slug = test_value
        self.assertEqual(self.instance.feed_slug, test_value)
    
    def test_item_property(self):
        """
        Test item property
        """
        test_value = 'gbhfyjaetrrxsnfmwclc'
        self.instance.item = test_value
        self.assertEqual(self.instance.item, test_value)
    
    def test_author_property(self):
        """
        Test author property
        """
        test_value = None
        self.instance.author = test_value
        self.assertEqual(self.instance.author, test_value)
    
    def test_publisher_property(self):
        """
        Test publisher property
        """
        test_value = None
        self.instance.publisher = test_value
        self.assertEqual(self.instance.publisher, test_value)
    
    def test_summary_property(self):
        """
        Test summary property
        """
        test_value = None
        self.instance.summary = test_value
        self.assertEqual(self.instance.summary, test_value)
    
    def test_title_property(self):
        """
        Test title property
        """
        test_value = None
        self.instance.title = test_value
        self.assertEqual(self.instance.title, test_value)
    
    def test_source_property(self):
        """
        Test source property
        """
        test_value = None
        self.instance.source = test_value
        self.assertEqual(self.instance.source, test_value)
    
    def test_content_property(self):
        """
        Test content property
        """
        test_value = [None, None]
        self.instance.content = test_value
        self.assertEqual(self.instance.content, test_value)
    
    def test_enclosures_property(self):
        """
        Test enclosures property
        """
        test_value = [None, None, None]
        self.instance.enclosures = test_value
        self.assertEqual(self.instance.enclosures, test_value)
    
    def test_published_property(self):
        """
        Test published property
        """
        test_value = int(74)
        self.instance.published = test_value
        self.assertEqual(self.instance.published, test_value)
    
    def test_updated_property(self):
        """
        Test updated property
        """
        test_value = int(19)
        self.instance.updated = test_value
        self.assertEqual(self.instance.updated, test_value)
    
    def test_created_property(self):
        """
        Test created property
        """
        test_value = int(8)
        self.instance.created = test_value
        self.assertEqual(self.instance.created, test_value)
    
    def test_expired_property(self):
        """
        Test expired property
        """
        test_value = int(93)
        self.instance.expired = test_value
        self.assertEqual(self.instance.expired, test_value)
    
    def test_id_property(self):
        """
        Test id property
        """
        test_value = 'eriesuosfshlszuqkpsd'
        self.instance.id = test_value
        self.assertEqual(self.instance.id, test_value)
    
    def test_license_property(self):
        """
        Test license property
        """
        test_value = 'epbbbwptcxuixdiglrxl'
        self.instance.license = test_value
        self.assertEqual(self.instance.license, test_value)
    
    def test_comments_property(self):
        """
        Test comments property
        """
        test_value = 'mnzkqkccrmlpipyjdjpq'
        self.instance.comments = test_value
        self.assertEqual(self.instance.comments, test_value)
    
    def test_contributors_property(self):
        """
        Test contributors property
        """
        test_value = [None, None]
        self.instance.contributors = test_value
        self.assertEqual(self.instance.contributors, test_value)
    
    def test_links_property(self):
        """
        Test links property
        """
        test_value = [None, None]
        self.instance.links = test_value
        self.assertEqual(self.instance.links, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = FeedItem.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = FeedItem.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

