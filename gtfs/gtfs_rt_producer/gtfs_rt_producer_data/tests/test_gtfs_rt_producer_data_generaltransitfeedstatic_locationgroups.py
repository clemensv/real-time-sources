"""
Test case for LocationGroups
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedstatic.locationgroups import LocationGroups

class Test_LocationGroups(unittest.TestCase):
    """
    Test case for LocationGroups
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_LocationGroups.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of LocationGroups for testing
        """
        instance = LocationGroups(
            locationGroupId='srwjohnhkzxqizvbgtng',
            locationGroupName='rbxshoxgkesqxhfaxswg',
            locationGroupDesc='kvafzpgwanbatmxoyjft',
            locationGroupUrl='ovrvhtldfimusextlrfz'
        )
        return instance

    
    def test_locationGroupId_property(self):
        """
        Test locationGroupId property
        """
        test_value = 'srwjohnhkzxqizvbgtng'
        self.instance.locationGroupId = test_value
        self.assertEqual(self.instance.locationGroupId, test_value)
    
    def test_locationGroupName_property(self):
        """
        Test locationGroupName property
        """
        test_value = 'rbxshoxgkesqxhfaxswg'
        self.instance.locationGroupName = test_value
        self.assertEqual(self.instance.locationGroupName, test_value)
    
    def test_locationGroupDesc_property(self):
        """
        Test locationGroupDesc property
        """
        test_value = 'kvafzpgwanbatmxoyjft'
        self.instance.locationGroupDesc = test_value
        self.assertEqual(self.instance.locationGroupDesc, test_value)
    
    def test_locationGroupUrl_property(self):
        """
        Test locationGroupUrl property
        """
        test_value = 'ovrvhtldfimusextlrfz'
        self.instance.locationGroupUrl = test_value
        self.assertEqual(self.instance.locationGroupUrl, test_value)
    
