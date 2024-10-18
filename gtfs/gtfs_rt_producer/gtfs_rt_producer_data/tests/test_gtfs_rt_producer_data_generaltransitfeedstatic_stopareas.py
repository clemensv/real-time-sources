"""
Test case for StopAreas
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedstatic.stopareas import StopAreas


class Test_StopAreas(unittest.TestCase):
    """
    Test case for StopAreas
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_StopAreas.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of StopAreas for testing
        """
        instance = StopAreas(
            stopAreaId='qwsagbljlrwyvmqtqpza',
            stopId='dejzsufbmuxfbaobdsnc',
            areaId='yzfpitytuqspnfrulawi'
        )
        return instance

    
    def test_stopAreaId_property(self):
        """
        Test stopAreaId property
        """
        test_value = 'qwsagbljlrwyvmqtqpza'
        self.instance.stopAreaId = test_value
        self.assertEqual(self.instance.stopAreaId, test_value)
    
    def test_stopId_property(self):
        """
        Test stopId property
        """
        test_value = 'dejzsufbmuxfbaobdsnc'
        self.instance.stopId = test_value
        self.assertEqual(self.instance.stopId, test_value)
    
    def test_areaId_property(self):
        """
        Test areaId property
        """
        test_value = 'yzfpitytuqspnfrulawi'
        self.instance.areaId = test_value
        self.assertEqual(self.instance.areaId, test_value)
    
