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
            levelId='huvqqwskbbnjbyiwltkw',
            levelIndex=float(75.3704311572328),
            levelName='mcikfismyoqbaxdndujj'
        )
        return instance

    
    def test_levelId_property(self):
        """
        Test levelId property
        """
        test_value = 'huvqqwskbbnjbyiwltkw'
        self.instance.levelId = test_value
        self.assertEqual(self.instance.levelId, test_value)
    
    def test_levelIndex_property(self):
        """
        Test levelIndex property
        """
        test_value = float(75.3704311572328)
        self.instance.levelIndex = test_value
        self.assertEqual(self.instance.levelIndex, test_value)
    
    def test_levelName_property(self):
        """
        Test levelName property
        """
        test_value = 'mcikfismyoqbaxdndujj'
        self.instance.levelName = test_value
        self.assertEqual(self.instance.levelName, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Levels.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
