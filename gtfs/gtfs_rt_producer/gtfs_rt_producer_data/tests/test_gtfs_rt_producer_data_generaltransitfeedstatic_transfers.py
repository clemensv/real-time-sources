"""
Test case for Transfers
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedstatic.transfers import Transfers


class Test_Transfers(unittest.TestCase):
    """
    Test case for Transfers
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Transfers.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Transfers for testing
        """
        instance = Transfers(
            fromStopId='bziyyysfglqmuskdolii',
            toStopId='eamkpfgqfshsiqlpcwmc',
            transferType=int(44),
            minTransferTime=int(73)
        )
        return instance

    
    def test_fromStopId_property(self):
        """
        Test fromStopId property
        """
        test_value = 'bziyyysfglqmuskdolii'
        self.instance.fromStopId = test_value
        self.assertEqual(self.instance.fromStopId, test_value)
    
    def test_toStopId_property(self):
        """
        Test toStopId property
        """
        test_value = 'eamkpfgqfshsiqlpcwmc'
        self.instance.toStopId = test_value
        self.assertEqual(self.instance.toStopId, test_value)
    
    def test_transferType_property(self):
        """
        Test transferType property
        """
        test_value = int(44)
        self.instance.transferType = test_value
        self.assertEqual(self.instance.transferType, test_value)
    
    def test_minTransferTime_property(self):
        """
        Test minTransferTime property
        """
        test_value = int(73)
        self.instance.minTransferTime = test_value
        self.assertEqual(self.instance.minTransferTime, test_value)
    
