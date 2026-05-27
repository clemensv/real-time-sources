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
            locationGroupId='metaegstbupvswxfatck',
            locationGroupName='iuwpqaetlegzitgecsam',
            locationGroupDesc='rqozowsovkrarogxiovp',
            locationGroupUrl='ocjsrecwymeemhlqsvfg'
        )
        return instance

    
    def test_locationGroupId_property(self):
        """
        Test locationGroupId property
        """
        test_value = 'metaegstbupvswxfatck'
        self.instance.locationGroupId = test_value
        self.assertEqual(self.instance.locationGroupId, test_value)
    
    def test_locationGroupName_property(self):
        """
        Test locationGroupName property
        """
        test_value = 'iuwpqaetlegzitgecsam'
        self.instance.locationGroupName = test_value
        self.assertEqual(self.instance.locationGroupName, test_value)
    
    def test_locationGroupDesc_property(self):
        """
        Test locationGroupDesc property
        """
        test_value = 'rqozowsovkrarogxiovp'
        self.instance.locationGroupDesc = test_value
        self.assertEqual(self.instance.locationGroupDesc, test_value)
    
    def test_locationGroupUrl_property(self):
        """
        Test locationGroupUrl property
        """
        test_value = 'ocjsrecwymeemhlqsvfg'
        self.instance.locationGroupUrl = test_value
        self.assertEqual(self.instance.locationGroupUrl, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = LocationGroups.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
