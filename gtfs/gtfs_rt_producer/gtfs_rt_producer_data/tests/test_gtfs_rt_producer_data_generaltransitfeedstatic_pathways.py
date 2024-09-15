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
            pathwayId='ncczfqfxmvpiyqbvduut',
            fromStopId='tlwjglaugocmayhomoak',
            toStopId='nrpcrfgqmrqexmhvjrkk',
            pathwayMode=int(58),
            isBidirectional=int(25),
            length=float(97.24756695801547),
            traversalTime=int(23),
            stairCount=int(84),
            maxSlope=float(97.3590036957665),
            minWidth=float(33.23002239778553),
            signpostedAs='rnnkanrcmllnqetkbfdm',
            reversedSignpostedAs='idglnepwjwwvezqpnpof'
        )
        return instance

    
    def test_pathwayId_property(self):
        """
        Test pathwayId property
        """
        test_value = 'ncczfqfxmvpiyqbvduut'
        self.instance.pathwayId = test_value
        self.assertEqual(self.instance.pathwayId, test_value)
    
    def test_fromStopId_property(self):
        """
        Test fromStopId property
        """
        test_value = 'tlwjglaugocmayhomoak'
        self.instance.fromStopId = test_value
        self.assertEqual(self.instance.fromStopId, test_value)
    
    def test_toStopId_property(self):
        """
        Test toStopId property
        """
        test_value = 'nrpcrfgqmrqexmhvjrkk'
        self.instance.toStopId = test_value
        self.assertEqual(self.instance.toStopId, test_value)
    
    def test_pathwayMode_property(self):
        """
        Test pathwayMode property
        """
        test_value = int(58)
        self.instance.pathwayMode = test_value
        self.assertEqual(self.instance.pathwayMode, test_value)
    
    def test_isBidirectional_property(self):
        """
        Test isBidirectional property
        """
        test_value = int(25)
        self.instance.isBidirectional = test_value
        self.assertEqual(self.instance.isBidirectional, test_value)
    
    def test_length_property(self):
        """
        Test length property
        """
        test_value = float(97.24756695801547)
        self.instance.length = test_value
        self.assertEqual(self.instance.length, test_value)
    
    def test_traversalTime_property(self):
        """
        Test traversalTime property
        """
        test_value = int(23)
        self.instance.traversalTime = test_value
        self.assertEqual(self.instance.traversalTime, test_value)
    
    def test_stairCount_property(self):
        """
        Test stairCount property
        """
        test_value = int(84)
        self.instance.stairCount = test_value
        self.assertEqual(self.instance.stairCount, test_value)
    
    def test_maxSlope_property(self):
        """
        Test maxSlope property
        """
        test_value = float(97.3590036957665)
        self.instance.maxSlope = test_value
        self.assertEqual(self.instance.maxSlope, test_value)
    
    def test_minWidth_property(self):
        """
        Test minWidth property
        """
        test_value = float(33.23002239778553)
        self.instance.minWidth = test_value
        self.assertEqual(self.instance.minWidth, test_value)
    
    def test_signpostedAs_property(self):
        """
        Test signpostedAs property
        """
        test_value = 'rnnkanrcmllnqetkbfdm'
        self.instance.signpostedAs = test_value
        self.assertEqual(self.instance.signpostedAs, test_value)
    
    def test_reversedSignpostedAs_property(self):
        """
        Test reversedSignpostedAs property
        """
        test_value = 'idglnepwjwwvezqpnpof'
        self.instance.reversedSignpostedAs = test_value
        self.assertEqual(self.instance.reversedSignpostedAs, test_value)
    
