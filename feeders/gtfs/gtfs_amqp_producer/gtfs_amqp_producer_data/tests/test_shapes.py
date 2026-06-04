"""
Test case for Shapes
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_amqp_producer_data.generaltransitfeedstatic.shapes import Shapes


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
            shapeId='fisnnjskfletqpakttud',
            shapePtLat=float(35.128134334690806),
            shapePtLon=float(12.246981966865722),
            shapePtSequence=int(16),
            shapeDistTraveled=float(92.7688929274379)
        )
        return instance

    
    def test_shapeId_property(self):
        """
        Test shapeId property
        """
        test_value = 'fisnnjskfletqpakttud'
        self.instance.shapeId = test_value
        self.assertEqual(self.instance.shapeId, test_value)
    
    def test_shapePtLat_property(self):
        """
        Test shapePtLat property
        """
        test_value = float(35.128134334690806)
        self.instance.shapePtLat = test_value
        self.assertEqual(self.instance.shapePtLat, test_value)
    
    def test_shapePtLon_property(self):
        """
        Test shapePtLon property
        """
        test_value = float(12.246981966865722)
        self.instance.shapePtLon = test_value
        self.assertEqual(self.instance.shapePtLon, test_value)
    
    def test_shapePtSequence_property(self):
        """
        Test shapePtSequence property
        """
        test_value = int(16)
        self.instance.shapePtSequence = test_value
        self.assertEqual(self.instance.shapePtSequence, test_value)
    
    def test_shapeDistTraveled_property(self):
        """
        Test shapeDistTraveled property
        """
        test_value = float(92.7688929274379)
        self.instance.shapeDistTraveled = test_value
        self.assertEqual(self.instance.shapeDistTraveled, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Shapes.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Shapes.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

