"""
Test case for Shapes
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedstatic.shapes import Shapes

class Test_Shapes(unittest.TestCase):
    """
    Test case for Shapes
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Shapes.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Shapes for testing
        """
        instance = Shapes(
            shapeId='dbsbzxssnwfudgczvywi',
            shapePtLat=float(60.276034048980485),
            shapePtLon=float(84.24714219567174),
            shapePtSequence=int(54),
            shapeDistTraveled=float(86.3784533860859)
        )
        return instance

    
    def test_shapeId_property(self):
        """
        Test shapeId property
        """
        test_value = 'dbsbzxssnwfudgczvywi'
        self.instance.shapeId = test_value
        self.assertEqual(self.instance.shapeId, test_value)
    
    def test_shapePtLat_property(self):
        """
        Test shapePtLat property
        """
        test_value = float(60.276034048980485)
        self.instance.shapePtLat = test_value
        self.assertEqual(self.instance.shapePtLat, test_value)
    
    def test_shapePtLon_property(self):
        """
        Test shapePtLon property
        """
        test_value = float(84.24714219567174)
        self.instance.shapePtLon = test_value
        self.assertEqual(self.instance.shapePtLon, test_value)
    
    def test_shapePtSequence_property(self):
        """
        Test shapePtSequence property
        """
        test_value = int(54)
        self.instance.shapePtSequence = test_value
        self.assertEqual(self.instance.shapePtSequence, test_value)
    
    def test_shapeDistTraveled_property(self):
        """
        Test shapeDistTraveled property
        """
        test_value = float(86.3784533860859)
        self.instance.shapeDistTraveled = test_value
        self.assertEqual(self.instance.shapeDistTraveled, test_value)
    
