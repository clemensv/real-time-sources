"""
Test case for Levels
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedstatic.levels import Levels

class Test_Levels(unittest.TestCase):
    """
    Test case for Levels
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Levels.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Levels for testing
        """
        instance = Levels(
            levelId='khuikpzjukkqkhugtemu',
            levelIndex=float(41.047808343759684),
            levelName='aqxmkrdwousvjlcwkqvd'
        )
        return instance

    
    def test_levelId_property(self):
        """
        Test levelId property
        """
        test_value = 'khuikpzjukkqkhugtemu'
        self.instance.levelId = test_value
        self.assertEqual(self.instance.levelId, test_value)
    
    def test_levelIndex_property(self):
        """
        Test levelIndex property
        """
        test_value = float(41.047808343759684)
        self.instance.levelIndex = test_value
        self.assertEqual(self.instance.levelIndex, test_value)
    
    def test_levelName_property(self):
        """
        Test levelName property
        """
        test_value = 'aqxmkrdwousvjlcwkqvd'
        self.instance.levelName = test_value
        self.assertEqual(self.instance.levelName, test_value)
    
