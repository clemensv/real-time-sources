"""
Test case for LocationGeoJson
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedstatic.locationgeojson import LocationGeoJson


class Test_LocationGeoJson(unittest.TestCase):
    """
    Test case for LocationGeoJson
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_LocationGeoJson.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of LocationGeoJson for testing
        """
        instance = LocationGeoJson(
            locationGeoJsonId='icwpipfnjxctujnacjnl',
            locationGeoJsonType='aihywqwwmiujbepezyeo',
            locationGeoJsonData='hlkiwmzmeshjdcklbtua'
        )
        return instance

    
    def test_locationGeoJsonId_property(self):
        """
        Test locationGeoJsonId property
        """
        test_value = 'icwpipfnjxctujnacjnl'
        self.instance.locationGeoJsonId = test_value
        self.assertEqual(self.instance.locationGeoJsonId, test_value)
    
    def test_locationGeoJsonType_property(self):
        """
        Test locationGeoJsonType property
        """
        test_value = 'aihywqwwmiujbepezyeo'
        self.instance.locationGeoJsonType = test_value
        self.assertEqual(self.instance.locationGeoJsonType, test_value)
    
    def test_locationGeoJsonData_property(self):
        """
        Test locationGeoJsonData property
        """
        test_value = 'hlkiwmzmeshjdcklbtua'
        self.instance.locationGeoJsonData = test_value
        self.assertEqual(self.instance.locationGeoJsonData, test_value)
    
