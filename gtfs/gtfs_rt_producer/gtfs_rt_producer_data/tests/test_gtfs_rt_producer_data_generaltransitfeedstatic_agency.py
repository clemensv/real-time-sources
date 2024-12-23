"""
Test case for Agency
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedstatic.agency import Agency


class Test_Agency(unittest.TestCase):
    """
    Test case for Agency
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Agency.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Agency for testing
        """
        instance = Agency(
            agencyId='atazbhzxuucmkyuomisl',
            agencyName='uqnzimklsyuntlrwarto',
            agencyUrl='kqvqtykihnwlakvnrtpm',
            agencyTimezone='cswqvtrzlrcxaqbqcbic',
            agencyLang='jpnllyfybgiggqhjepin',
            agencyPhone='ndghupixjifosudknxbz',
            agencyFareUrl='lkqdddlccwompdqtjjbn',
            agencyEmail='gyevveccaxwualtqdooa'
        )
        return instance

    
    def test_agencyId_property(self):
        """
        Test agencyId property
        """
        test_value = 'atazbhzxuucmkyuomisl'
        self.instance.agencyId = test_value
        self.assertEqual(self.instance.agencyId, test_value)
    
    def test_agencyName_property(self):
        """
        Test agencyName property
        """
        test_value = 'uqnzimklsyuntlrwarto'
        self.instance.agencyName = test_value
        self.assertEqual(self.instance.agencyName, test_value)
    
    def test_agencyUrl_property(self):
        """
        Test agencyUrl property
        """
        test_value = 'kqvqtykihnwlakvnrtpm'
        self.instance.agencyUrl = test_value
        self.assertEqual(self.instance.agencyUrl, test_value)
    
    def test_agencyTimezone_property(self):
        """
        Test agencyTimezone property
        """
        test_value = 'cswqvtrzlrcxaqbqcbic'
        self.instance.agencyTimezone = test_value
        self.assertEqual(self.instance.agencyTimezone, test_value)
    
    def test_agencyLang_property(self):
        """
        Test agencyLang property
        """
        test_value = 'jpnllyfybgiggqhjepin'
        self.instance.agencyLang = test_value
        self.assertEqual(self.instance.agencyLang, test_value)
    
    def test_agencyPhone_property(self):
        """
        Test agencyPhone property
        """
        test_value = 'ndghupixjifosudknxbz'
        self.instance.agencyPhone = test_value
        self.assertEqual(self.instance.agencyPhone, test_value)
    
    def test_agencyFareUrl_property(self):
        """
        Test agencyFareUrl property
        """
        test_value = 'lkqdddlccwompdqtjjbn'
        self.instance.agencyFareUrl = test_value
        self.assertEqual(self.instance.agencyFareUrl, test_value)
    
    def test_agencyEmail_property(self):
        """
        Test agencyEmail property
        """
        test_value = 'gyevveccaxwualtqdooa'
        self.instance.agencyEmail = test_value
        self.assertEqual(self.instance.agencyEmail, test_value)
    
