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
            shapeId='zylnznfaawgxulcfuijc',
            shapePtLat=float(0.8007517564493694),
            shapePtLon=float(32.43981679919942),
            shapePtSequence=int(44),
            shapeDistTraveled=float(99.46449341900879)
        )
        return instance

    
    def test_shapeId_property(self):
        """
        Test shapeId property
        """
        test_value = 'zylnznfaawgxulcfuijc'
        self.instance.shapeId = test_value
        self.assertEqual(self.instance.shapeId, test_value)
    
    def test_shapePtLat_property(self):
        """
        Test shapePtLat property
        """
        test_value = float(0.8007517564493694)
        self.instance.shapePtLat = test_value
        self.assertEqual(self.instance.shapePtLat, test_value)
    
    def test_shapePtLon_property(self):
        """
        Test shapePtLon property
        """
        test_value = float(32.43981679919942)
        self.instance.shapePtLon = test_value
        self.assertEqual(self.instance.shapePtLon, test_value)
    
    def test_shapePtSequence_property(self):
        """
        Test shapePtSequence property
        """
        test_value = int(44)
        self.instance.shapePtSequence = test_value
        self.assertEqual(self.instance.shapePtSequence, test_value)
    
    def test_shapeDistTraveled_property(self):
        """
        Test shapeDistTraveled property
        """
        test_value = float(99.46449341900879)
        self.instance.shapeDistTraveled = test_value
        self.assertEqual(self.instance.shapeDistTraveled, test_value)
    
