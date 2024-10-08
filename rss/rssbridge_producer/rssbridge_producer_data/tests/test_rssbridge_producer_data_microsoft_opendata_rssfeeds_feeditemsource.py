"""
Test case for FeedItemSource
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditemsource import FeedItemSource
from test_rssbridge_producer_data_microsoft_opendata_rssfeeds_feeditemauthor import Test_FeedItemAuthor
from test_rssbridge_producer_data_microsoft_opendata_rssfeeds_link import Test_Link
import datetime


class Test_FeedItemSource(unittest.TestCase):
    """
    Test case for FeedItemSource
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_FeedItemSource.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of FeedItemSource for testing
        """
        instance = FeedItemSource(
            author='dgckzcnbwobfrqtaqcbl',
            author_detail=Test_FeedItemAuthor.create_instance(),
            contributors=[Test_FeedItemAuthor.create_instance(), Test_FeedItemAuthor.create_instance(), Test_FeedItemAuthor.create_instance(), Test_FeedItemAuthor.create_instance(), Test_FeedItemAuthor.create_instance()],
            icon='ormobxnmhxfegfhkmdvh',
            id='gotmdeqahujupftnpsmo',
            link='hhlylsfgugkpsvzytivq',
            links=[Test_Link.create_instance(), Test_Link.create_instance()],
            logo='gjmubeizkquidwthwhom',
            rights='ncbednvhutbvzttcilto',
            subtitle='nqbeqnmtdvkmtlbhknuz',
            title='jtstbmkvinbdkjawetej',
            updated=datetime.datetime.now(datetime.timezone.utc)
        )
        return instance

    
    def test_author_property(self):
        """
        Test author property
        """
        test_value = 'dgckzcnbwobfrqtaqcbl'
        self.instance.author = test_value
        self.assertEqual(self.instance.author, test_value)
    
    def test_author_detail_property(self):
        """
        Test author_detail property
        """
        test_value = Test_FeedItemAuthor.create_instance()
        self.instance.author_detail = test_value
        self.assertEqual(self.instance.author_detail, test_value)
    
    def test_contributors_property(self):
        """
        Test contributors property
        """
        test_value = [Test_FeedItemAuthor.create_instance(), Test_FeedItemAuthor.create_instance(), Test_FeedItemAuthor.create_instance(), Test_FeedItemAuthor.create_instance(), Test_FeedItemAuthor.create_instance()]
        self.instance.contributors = test_value
        self.assertEqual(self.instance.contributors, test_value)
    
    def test_icon_property(self):
        """
        Test icon property
        """
        test_value = 'ormobxnmhxfegfhkmdvh'
        self.instance.icon = test_value
        self.assertEqual(self.instance.icon, test_value)
    
    def test_id_property(self):
        """
        Test id property
        """
        test_value = 'gotmdeqahujupftnpsmo'
        self.instance.id = test_value
        self.assertEqual(self.instance.id, test_value)
    
    def test_link_property(self):
        """
        Test link property
        """
        test_value = 'hhlylsfgugkpsvzytivq'
        self.instance.link = test_value
        self.assertEqual(self.instance.link, test_value)
    
    def test_links_property(self):
        """
        Test links property
        """
        test_value = [Test_Link.create_instance(), Test_Link.create_instance()]
        self.instance.links = test_value
        self.assertEqual(self.instance.links, test_value)
    
    def test_logo_property(self):
        """
        Test logo property
        """
        test_value = 'gjmubeizkquidwthwhom'
        self.instance.logo = test_value
        self.assertEqual(self.instance.logo, test_value)
    
    def test_rights_property(self):
        """
        Test rights property
        """
        test_value = 'ncbednvhutbvzttcilto'
        self.instance.rights = test_value
        self.assertEqual(self.instance.rights, test_value)
    
    def test_subtitle_property(self):
        """
        Test subtitle property
        """
        test_value = 'nqbeqnmtdvkmtlbhknuz'
        self.instance.subtitle = test_value
        self.assertEqual(self.instance.subtitle, test_value)
    
    def test_title_property(self):
        """
        Test title property
        """
        test_value = 'jtstbmkvinbdkjawetej'
        self.instance.title = test_value
        self.assertEqual(self.instance.title, test_value)
    
    def test_updated_property(self):
        """
        Test updated property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.updated = test_value
        self.assertEqual(self.instance.updated, test_value)
    
