"""
Test case for WeatherBulletin
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_japan_amqp_producer_data.weatherbulletin import WeatherBulletin
from jma_japan_amqp_producer_data.feedtypeenum import FeedTypeenum
import datetime


class Test_WeatherBulletin(unittest.TestCase):
    """
    Test case for WeatherBulletin
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_WeatherBulletin.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of WeatherBulletin for testing
        """
        instance = WeatherBulletin(
            bulletin_id='qvophyhxcrkhhpaavewg',
            title='tsjtlgrqcdaobmittrjf',
            author='yidruslfzwsduuwrtqpk',
            updated=datetime.datetime.now(datetime.timezone.utc),
            link='sxnjftptkvraxptnjfir',
            content='bhmzcixrqmlhivjmxokq',
            feed_type=FeedTypeenum.regular,
            office='oqfprwcoezpxpabpbmje'
        )
        return instance

    
    def test_bulletin_id_property(self):
        """
        Test bulletin_id property
        """
        test_value = 'qvophyhxcrkhhpaavewg'
        self.instance.bulletin_id = test_value
        self.assertEqual(self.instance.bulletin_id, test_value)
    
    def test_title_property(self):
        """
        Test title property
        """
        test_value = 'tsjtlgrqcdaobmittrjf'
        self.instance.title = test_value
        self.assertEqual(self.instance.title, test_value)
    
    def test_author_property(self):
        """
        Test author property
        """
        test_value = 'yidruslfzwsduuwrtqpk'
        self.instance.author = test_value
        self.assertEqual(self.instance.author, test_value)
    
    def test_updated_property(self):
        """
        Test updated property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.updated = test_value
        self.assertEqual(self.instance.updated, test_value)
    
    def test_link_property(self):
        """
        Test link property
        """
        test_value = 'sxnjftptkvraxptnjfir'
        self.instance.link = test_value
        self.assertEqual(self.instance.link, test_value)
    
    def test_content_property(self):
        """
        Test content property
        """
        test_value = 'bhmzcixrqmlhivjmxokq'
        self.instance.content = test_value
        self.assertEqual(self.instance.content, test_value)
    
    def test_feed_type_property(self):
        """
        Test feed_type property
        """
        test_value = FeedTypeenum.regular
        self.instance.feed_type = test_value
        self.assertEqual(self.instance.feed_type, test_value)
    
    def test_office_property(self):
        """
        Test office property
        """
        test_value = 'oqfprwcoezpxpabpbmje'
        self.instance.office = test_value
        self.assertEqual(self.instance.office, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = WeatherBulletin.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = WeatherBulletin.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

