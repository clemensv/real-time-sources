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
            feedPublisherName='alnymvrclubcuoqwccvy',
            feedPublisherUrl='hulksvhfidcmjfbsximy',
            feedLang='zeuamikunmhdxfbcafhl',
            defaultLang='crefyzfkycekrasrmhac',
            feedStartDate='spzcjfypwhqmmwhhgsic',
            feedEndDate='htncyxsbxhunokvfeflq',
            feedVersion='fgxheuigrrcxiqqoecop',
            feedContactEmail='lyboftkrpwvtjbiuasxm',
            feedContactUrl='jtkjknjhiqmystdgruqm'
        )
        return instance

    
    def test_feedPublisherName_property(self):
        """
        Test feedPublisherName property
        """
        test_value = 'alnymvrclubcuoqwccvy'
        self.instance.feedPublisherName = test_value
        self.assertEqual(self.instance.feedPublisherName, test_value)
    
    def test_feedPublisherUrl_property(self):
        """
        Test feedPublisherUrl property
        """
        test_value = 'hulksvhfidcmjfbsximy'
        self.instance.feedPublisherUrl = test_value
        self.assertEqual(self.instance.feedPublisherUrl, test_value)
    
    def test_feedLang_property(self):
        """
        Test feedLang property
        """
        test_value = 'zeuamikunmhdxfbcafhl'
        self.instance.feedLang = test_value
        self.assertEqual(self.instance.feedLang, test_value)
    
    def test_defaultLang_property(self):
        """
        Test defaultLang property
        """
        test_value = 'crefyzfkycekrasrmhac'
        self.instance.defaultLang = test_value
        self.assertEqual(self.instance.defaultLang, test_value)
    
    def test_feedStartDate_property(self):
        """
        Test feedStartDate property
        """
        test_value = 'spzcjfypwhqmmwhhgsic'
        self.instance.feedStartDate = test_value
        self.assertEqual(self.instance.feedStartDate, test_value)
    
    def test_feedEndDate_property(self):
        """
        Test feedEndDate property
        """
        test_value = 'htncyxsbxhunokvfeflq'
        self.instance.feedEndDate = test_value
        self.assertEqual(self.instance.feedEndDate, test_value)
    
    def test_feedVersion_property(self):
        """
        Test feedVersion property
        """
        test_value = 'fgxheuigrrcxiqqoecop'
        self.instance.feedVersion = test_value
        self.assertEqual(self.instance.feedVersion, test_value)
    
    def test_feedContactEmail_property(self):
        """
        Test feedContactEmail property
        """
        test_value = 'lyboftkrpwvtjbiuasxm'
        self.instance.feedContactEmail = test_value
        self.assertEqual(self.instance.feedContactEmail, test_value)
    
    def test_feedContactUrl_property(self):
        """
        Test feedContactUrl property
        """
        test_value = 'jtkjknjhiqmystdgruqm'
        self.instance.feedContactUrl = test_value
        self.assertEqual(self.instance.feedContactUrl, test_value)
    
