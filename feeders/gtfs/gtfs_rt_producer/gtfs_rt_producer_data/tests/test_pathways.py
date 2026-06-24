"""
Test case for Pathways
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedstatic.pathways import Pathways


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
            pathwayId='ssccqvsxrjgzmeggqdjj',
            fromStopId='hcwxdtgqukrgppepubwk',
            toStopId='epkmuukxhfbrmtzuepxf',
            pathwayMode=int(87),
            isBidirectional=int(4),
            length=float(49.16350209198232),
            traversalTime=int(6),
            stairCount=int(72),
            maxSlope=float(21.001901103968123),
            minWidth=float(51.669216892283366),
            signpostedAs='mqvlzagymjvmepoybphl',
            reversedSignpostedAs='injzrhpehtumldwrdsim'
        )
        return instance

    
    def test_pathwayId_property(self):
        """
        Test pathwayId property
        """
        test_value = 'ssccqvsxrjgzmeggqdjj'
        self.instance.pathwayId = test_value
        self.assertEqual(self.instance.pathwayId, test_value)
    
    def test_fromStopId_property(self):
        """
        Test fromStopId property
        """
        test_value = 'hcwxdtgqukrgppepubwk'
        self.instance.fromStopId = test_value
        self.assertEqual(self.instance.fromStopId, test_value)
    
    def test_toStopId_property(self):
        """
        Test toStopId property
        """
        test_value = 'epkmuukxhfbrmtzuepxf'
        self.instance.toStopId = test_value
        self.assertEqual(self.instance.toStopId, test_value)
    
    def test_pathwayMode_property(self):
        """
        Test pathwayMode property
        """
        test_value = int(87)
        self.instance.pathwayMode = test_value
        self.assertEqual(self.instance.pathwayMode, test_value)
    
    def test_isBidirectional_property(self):
        """
        Test isBidirectional property
        """
        test_value = int(4)
        self.instance.isBidirectional = test_value
        self.assertEqual(self.instance.isBidirectional, test_value)
    
    def test_length_property(self):
        """
        Test length property
        """
        test_value = float(49.16350209198232)
        self.instance.length = test_value
        self.assertEqual(self.instance.length, test_value)
    
    def test_traversalTime_property(self):
        """
        Test traversalTime property
        """
        test_value = int(6)
        self.instance.traversalTime = test_value
        self.assertEqual(self.instance.traversalTime, test_value)
    
    def test_stairCount_property(self):
        """
        Test stairCount property
        """
        test_value = int(72)
        self.instance.stairCount = test_value
        self.assertEqual(self.instance.stairCount, test_value)
    
    def test_maxSlope_property(self):
        """
        Test maxSlope property
        """
        test_value = float(21.001901103968123)
        self.instance.maxSlope = test_value
        self.assertEqual(self.instance.maxSlope, test_value)
    
    def test_minWidth_property(self):
        """
        Test minWidth property
        """
        test_value = float(51.669216892283366)
        self.instance.minWidth = test_value
        self.assertEqual(self.instance.minWidth, test_value)
    
    def test_signpostedAs_property(self):
        """
        Test signpostedAs property
        """
        test_value = 'mqvlzagymjvmepoybphl'
        self.instance.signpostedAs = test_value
        self.assertEqual(self.instance.signpostedAs, test_value)
    
    def test_reversedSignpostedAs_property(self):
        """
        Test reversedSignpostedAs property
        """
        test_value = 'injzrhpehtumldwrdsim'
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

