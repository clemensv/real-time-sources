"""
Test case for FeedInfo
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedstatic.feedinfo import FeedInfo


class Test_FeedInfo(unittest.TestCase):
    """
    Test case for FeedInfo
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_FeedInfo.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of FeedInfo for testing
        """
        instance = FeedInfo(
            feedPublisherName='hbuowzabernauorgugzs',
            feedPublisherUrl='yzbwljegnqlgvyzlspjp',
            feedLang='kfxugmbzjtfmfiprdxde',
            defaultLang='aokqgtenyaavktxqlofs',
            feedStartDate='mksqttvclwiisgbnjjrw',
            feedEndDate='kzqhfbxxnjbcaxxfnben',
            feedVersion='hhfedazingyrphbjerqq',
            feedContactEmail='ddnxiaxhbentglyonaww',
            feedContactUrl='oruugaedqaccnystdmrk'
        )
        return instance

    
    def test_feedPublisherName_property(self):
        """
        Test feedPublisherName property
        """
        test_value = 'hbuowzabernauorgugzs'
        self.instance.feedPublisherName = test_value
        self.assertEqual(self.instance.feedPublisherName, test_value)
    
    def test_feedPublisherUrl_property(self):
        """
        Test feedPublisherUrl property
        """
        test_value = 'yzbwljegnqlgvyzlspjp'
        self.instance.feedPublisherUrl = test_value
        self.assertEqual(self.instance.feedPublisherUrl, test_value)
    
    def test_feedLang_property(self):
        """
        Test feedLang property
        """
        test_value = 'kfxugmbzjtfmfiprdxde'
        self.instance.feedLang = test_value
        self.assertEqual(self.instance.feedLang, test_value)
    
    def test_defaultLang_property(self):
        """
        Test defaultLang property
        """
        test_value = 'aokqgtenyaavktxqlofs'
        self.instance.defaultLang = test_value
        self.assertEqual(self.instance.defaultLang, test_value)
    
    def test_feedStartDate_property(self):
        """
        Test feedStartDate property
        """
        test_value = 'mksqttvclwiisgbnjjrw'
        self.instance.feedStartDate = test_value
        self.assertEqual(self.instance.feedStartDate, test_value)
    
    def test_feedEndDate_property(self):
        """
        Test feedEndDate property
        """
        test_value = 'kzqhfbxxnjbcaxxfnben'
        self.instance.feedEndDate = test_value
        self.assertEqual(self.instance.feedEndDate, test_value)
    
    def test_feedVersion_property(self):
        """
        Test feedVersion property
        """
        test_value = 'hhfedazingyrphbjerqq'
        self.instance.feedVersion = test_value
        self.assertEqual(self.instance.feedVersion, test_value)
    
    def test_feedContactEmail_property(self):
        """
        Test feedContactEmail property
        """
        test_value = 'ddnxiaxhbentglyonaww'
        self.instance.feedContactEmail = test_value
        self.assertEqual(self.instance.feedContactEmail, test_value)
    
    def test_feedContactUrl_property(self):
        """
        Test feedContactUrl property
        """
        test_value = 'oruugaedqaccnystdmrk'
        self.instance.feedContactUrl = test_value
        self.assertEqual(self.instance.feedContactUrl, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = FeedInfo.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = FeedInfo.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

