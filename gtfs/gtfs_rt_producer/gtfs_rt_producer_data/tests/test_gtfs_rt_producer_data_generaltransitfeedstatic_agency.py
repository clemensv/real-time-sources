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
            agencyId='fzmsqekxvvgbvkutaelx',
            agencyName='mhldgpqtjwihqcxfevid',
            agencyUrl='wibufzzabfdpznevxtrh',
            agencyTimezone='eqmeypatwpqlpuiptefe',
            agencyLang='flzzmtxcgorlkqdwecwd',
            agencyPhone='qwsfpughkokmkrpejlmw',
            agencyFareUrl='jabjdewufgtbjveuzruj',
            agencyEmail='uzhbkptqktylknepaykj'
        )
        return instance

    
    def test_agencyId_property(self):
        """
        Test agencyId property
        """
        test_value = 'fzmsqekxvvgbvkutaelx'
        self.instance.agencyId = test_value
        self.assertEqual(self.instance.agencyId, test_value)
    
    def test_agencyName_property(self):
        """
        Test agencyName property
        """
        test_value = 'mhldgpqtjwihqcxfevid'
        self.instance.agencyName = test_value
        self.assertEqual(self.instance.agencyName, test_value)
    
    def test_agencyUrl_property(self):
        """
        Test agencyUrl property
        """
        test_value = 'wibufzzabfdpznevxtrh'
        self.instance.agencyUrl = test_value
        self.assertEqual(self.instance.agencyUrl, test_value)
    
    def test_agencyTimezone_property(self):
        """
        Test agencyTimezone property
        """
        test_value = 'eqmeypatwpqlpuiptefe'
        self.instance.agencyTimezone = test_value
        self.assertEqual(self.instance.agencyTimezone, test_value)
    
    def test_agencyLang_property(self):
        """
        Test agencyLang property
        """
        test_value = 'flzzmtxcgorlkqdwecwd'
        self.instance.agencyLang = test_value
        self.assertEqual(self.instance.agencyLang, test_value)
    
    def test_agencyPhone_property(self):
        """
        Test agencyPhone property
        """
        test_value = 'qwsfpughkokmkrpejlmw'
        self.instance.agencyPhone = test_value
        self.assertEqual(self.instance.agencyPhone, test_value)
    
    def test_agencyFareUrl_property(self):
        """
        Test agencyFareUrl property
        """
        test_value = 'jabjdewufgtbjveuzruj'
        self.instance.agencyFareUrl = test_value
        self.assertEqual(self.instance.agencyFareUrl, test_value)
    
    def test_agencyEmail_property(self):
        """
        Test agencyEmail property
        """
        test_value = 'uzhbkptqktylknepaykj'
        self.instance.agencyEmail = test_value
        self.assertEqual(self.instance.agencyEmail, test_value)
    
