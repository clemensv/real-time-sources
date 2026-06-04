"""
Test case for Pathways
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_producer_data.generaltransitfeedstatic.pathways import Pathways


class Test_Pathways(unittest.TestCase):
    """
    Test case for Pathways
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Pathways.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Pathways for testing
        """
        instance = Pathways(
            pathwayId='amkcxqweqeyqvvjcvlkz',
            fromStopId='vufrjfdzilvmhzobbqfj',
            toStopId='ozhucfqlhareseqxjlur',
            pathwayMode=int(48),
            isBidirectional=int(77),
            length=float(10.259465896958364),
            traversalTime=int(41),
            stairCount=int(12),
            maxSlope=float(82.56096198747206),
            minWidth=float(74.65265513822614),
            signpostedAs='edgrjokmacajeepsksja',
            reversedSignpostedAs='ywxecbgxgskqmgcuxlcd'
        )
        return instance

    
    def test_pathwayId_property(self):
        """
        Test pathwayId property
        """
        test_value = 'amkcxqweqeyqvvjcvlkz'
        self.instance.pathwayId = test_value
        self.assertEqual(self.instance.pathwayId, test_value)
    
    def test_fromStopId_property(self):
        """
        Test fromStopId property
        """
        test_value = 'vufrjfdzilvmhzobbqfj'
        self.instance.fromStopId = test_value
        self.assertEqual(self.instance.fromStopId, test_value)
    
    def test_toStopId_property(self):
        """
        Test toStopId property
        """
        test_value = 'ozhucfqlhareseqxjlur'
        self.instance.toStopId = test_value
        self.assertEqual(self.instance.toStopId, test_value)
    
    def test_pathwayMode_property(self):
        """
        Test pathwayMode property
        """
        test_value = int(48)
        self.instance.pathwayMode = test_value
        self.assertEqual(self.instance.pathwayMode, test_value)
    
    def test_isBidirectional_property(self):
        """
        Test isBidirectional property
        """
        test_value = int(77)
        self.instance.isBidirectional = test_value
        self.assertEqual(self.instance.isBidirectional, test_value)
    
    def test_length_property(self):
        """
        Test length property
        """
        test_value = float(10.259465896958364)
        self.instance.length = test_value
        self.assertEqual(self.instance.length, test_value)
    
    def test_traversalTime_property(self):
        """
        Test traversalTime property
        """
        test_value = int(41)
        self.instance.traversalTime = test_value
        self.assertEqual(self.instance.traversalTime, test_value)
    
    def test_stairCount_property(self):
        """
        Test stairCount property
        """
        test_value = int(12)
        self.instance.stairCount = test_value
        self.assertEqual(self.instance.stairCount, test_value)
    
    def test_maxSlope_property(self):
        """
        Test maxSlope property
        """
        test_value = float(82.56096198747206)
        self.instance.maxSlope = test_value
        self.assertEqual(self.instance.maxSlope, test_value)
    
    def test_minWidth_property(self):
        """
        Test minWidth property
        """
        test_value = float(74.65265513822614)
        self.instance.minWidth = test_value
        self.assertEqual(self.instance.minWidth, test_value)
    
    def test_signpostedAs_property(self):
        """
        Test signpostedAs property
        """
        test_value = 'edgrjokmacajeepsksja'
        self.instance.signpostedAs = test_value
        self.assertEqual(self.instance.signpostedAs, test_value)
    
    def test_reversedSignpostedAs_property(self):
        """
        Test reversedSignpostedAs property
        """
        test_value = 'ywxecbgxgskqmgcuxlcd'
        self.instance.reversedSignpostedAs = test_value
        self.assertEqual(self.instance.reversedSignpostedAs, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Pathways.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Pathways.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

