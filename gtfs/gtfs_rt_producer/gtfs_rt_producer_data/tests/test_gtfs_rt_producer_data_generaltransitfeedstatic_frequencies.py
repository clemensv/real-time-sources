"""
Test case for Frequencies
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedstatic.frequencies import Frequencies


class Test_Frequencies(unittest.TestCase):
    """
    Test case for Frequencies
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Frequencies.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Frequencies for testing
        """
        instance = Frequencies(
            tripId='eypqnurmtmeaqjgxeakv',
            startTime='pudoyqtvpqgbfmpypvbk',
            endTime='frtcisfspmhkozflpmjj',
            headwaySecs=int(8),
            exactTimes=int(15)
        )
        return instance

    
    def test_tripId_property(self):
        """
        Test tripId property
        """
        test_value = 'eypqnurmtmeaqjgxeakv'
        self.instance.tripId = test_value
        self.assertEqual(self.instance.tripId, test_value)
    
    def test_startTime_property(self):
        """
        Test startTime property
        """
        test_value = 'pudoyqtvpqgbfmpypvbk'
        self.instance.startTime = test_value
        self.assertEqual(self.instance.startTime, test_value)
    
    def test_endTime_property(self):
        """
        Test endTime property
        """
        test_value = 'frtcisfspmhkozflpmjj'
        self.instance.endTime = test_value
        self.assertEqual(self.instance.endTime, test_value)
    
    def test_headwaySecs_property(self):
        """
        Test headwaySecs property
        """
        test_value = int(8)
        self.instance.headwaySecs = test_value
        self.assertEqual(self.instance.headwaySecs, test_value)
    
    def test_exactTimes_property(self):
        """
        Test exactTimes property
        """
        test_value = int(15)
        self.instance.exactTimes = test_value
        self.assertEqual(self.instance.exactTimes, test_value)
    
