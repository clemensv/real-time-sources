"""
Test case for FeedItem
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditem import FeedItem
from test_rssbridge_producer_data_microsoft_opendata_rssfeeds_feeditemsource import Test_FeedItemSource
from test_rssbridge_producer_data_microsoft_opendata_rssfeeds_feeditemsummary import Test_FeedItemSummary
from test_rssbridge_producer_data_microsoft_opendata_rssfeeds_feeditemauthor import Test_FeedItemAuthor
from test_rssbridge_producer_data_microsoft_opendata_rssfeeds_feeditemcontent import Test_FeedItemContent
from test_rssbridge_producer_data_microsoft_opendata_rssfeeds_feeditempublisher import Test_FeedItemPublisher
from test_rssbridge_producer_data_microsoft_opendata_rssfeeds_link import Test_Link
from test_rssbridge_producer_data_microsoft_opendata_rssfeeds_feeditemtitle import Test_FeedItemTitle
from test_rssbridge_producer_data_microsoft_opendata_rssfeeds_feeditemenclosure import Test_FeedItemEnclosure
import datetime


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
            author=Test_FeedItemAuthor.create_instance(),
            publisher=Test_FeedItemPublisher.create_instance(),
            summary=Test_FeedItemSummary.create_instance(),
            title=Test_FeedItemTitle.create_instance(),
            source=Test_FeedItemSource.create_instance(),
            content=[Test_FeedItemContent.create_instance(), Test_FeedItemContent.create_instance(), Test_FeedItemContent.create_instance()],
            enclosures=[Test_FeedItemEnclosure.create_instance(), Test_FeedItemEnclosure.create_instance(), Test_FeedItemEnclosure.create_instance(), Test_FeedItemEnclosure.create_instance(), Test_FeedItemEnclosure.create_instance()],
            published=datetime.datetime.now(datetime.timezone.utc),
            updated=datetime.datetime.now(datetime.timezone.utc),
            created=datetime.datetime.now(datetime.timezone.utc),
            expired=datetime.datetime.now(datetime.timezone.utc),
            id='dgcoivnoxrdqljakbmxf',
            license='sokifbvazmblvrhhtcnf',
            comments='fkafjdzqqmchuxihefbd',
            contributors=[Test_FeedItemAuthor.create_instance(), Test_FeedItemAuthor.create_instance()],
            links=[Test_Link.create_instance(), Test_Link.create_instance(), Test_Link.create_instance()]
        )
        return instance

    
    def test_author_property(self):
        """
        Test author property
        """
        test_value = Test_FeedItemAuthor.create_instance()
        self.instance.author = test_value
        self.assertEqual(self.instance.author, test_value)
    
    def test_publisher_property(self):
        """
        Test publisher property
        """
        test_value = Test_FeedItemPublisher.create_instance()
        self.instance.publisher = test_value
        self.assertEqual(self.instance.publisher, test_value)
    
    def test_summary_property(self):
        """
        Test summary property
        """
        test_value = Test_FeedItemSummary.create_instance()
        self.instance.summary = test_value
        self.assertEqual(self.instance.summary, test_value)
    
    def test_title_property(self):
        """
        Test title property
        """
        test_value = Test_FeedItemTitle.create_instance()
        self.instance.title = test_value
        self.assertEqual(self.instance.title, test_value)
    
    def test_source_property(self):
        """
        Test source property
        """
        test_value = Test_FeedItemSource.create_instance()
        self.instance.source = test_value
        self.assertEqual(self.instance.source, test_value)
    
    def test_content_property(self):
        """
        Test content property
        """
        test_value = [Test_FeedItemContent.create_instance(), Test_FeedItemContent.create_instance(), Test_FeedItemContent.create_instance()]
        self.instance.content = test_value
        self.assertEqual(self.instance.content, test_value)
    
    def test_enclosures_property(self):
        """
        Test enclosures property
        """
        test_value = [Test_FeedItemEnclosure.create_instance(), Test_FeedItemEnclosure.create_instance(), Test_FeedItemEnclosure.create_instance(), Test_FeedItemEnclosure.create_instance(), Test_FeedItemEnclosure.create_instance()]
        self.instance.enclosures = test_value
        self.assertEqual(self.instance.enclosures, test_value)
    
    def test_published_property(self):
        """
        Test published property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.published = test_value
        self.assertEqual(self.instance.published, test_value)
    
    def test_updated_property(self):
        """
        Test updated property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.updated = test_value
        self.assertEqual(self.instance.updated, test_value)
    
    def test_created_property(self):
        """
        Test created property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.created = test_value
        self.assertEqual(self.instance.created, test_value)
    
    def test_expired_property(self):
        """
        Test expired property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.expired = test_value
        self.assertEqual(self.instance.expired, test_value)
    
    def test_id_property(self):
        """
        Test id property
        """
        test_value = 'dgcoivnoxrdqljakbmxf'
        self.instance.id = test_value
        self.assertEqual(self.instance.id, test_value)
    
    def test_license_property(self):
        """
        Test license property
        """
        test_value = 'sokifbvazmblvrhhtcnf'
        self.instance.license = test_value
        self.assertEqual(self.instance.license, test_value)
    
    def test_comments_property(self):
        """
        Test comments property
        """
        test_value = 'fkafjdzqqmchuxihefbd'
        self.instance.comments = test_value
        self.assertEqual(self.instance.comments, test_value)
    
    def test_contributors_property(self):
        """
        Test contributors property
        """
        test_value = [Test_FeedItemAuthor.create_instance(), Test_FeedItemAuthor.create_instance()]
        self.instance.contributors = test_value
        self.assertEqual(self.instance.contributors, test_value)
    
    def test_links_property(self):
        """
        Test links property
        """
        test_value = [Test_Link.create_instance(), Test_Link.create_instance(), Test_Link.create_instance()]
        self.instance.links = test_value
        self.assertEqual(self.instance.links, test_value)
    
