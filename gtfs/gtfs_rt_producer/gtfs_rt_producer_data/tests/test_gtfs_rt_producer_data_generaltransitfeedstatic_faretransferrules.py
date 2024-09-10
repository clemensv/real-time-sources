"""
Test case for FareTransferRules
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedstatic.faretransferrules import FareTransferRules

class Test_FareTransferRules(unittest.TestCase):
    """
    Test case for FareTransferRules
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_FareTransferRules.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of FareTransferRules for testing
        """
        instance = FareTransferRules(
            fareTransferRuleId='deeifisuakhepuylepra',
            fareProductId='fpcthpfoziwjamocstbb',
            transferCount=int(77),
            fromLegGroupId='tcsniajftqaxtsflqthd',
            toLegGroupId='iebfocmundozjgwjqxws',
            duration=int(78),
            durationType='uktkcguysdejgupcxggz'
        )
        return instance

    
    def test_fareTransferRuleId_property(self):
        """
        Test fareTransferRuleId property
        """
        test_value = 'deeifisuakhepuylepra'
        self.instance.fareTransferRuleId = test_value
        self.assertEqual(self.instance.fareTransferRuleId, test_value)
    
    def test_fareProductId_property(self):
        """
        Test fareProductId property
        """
        test_value = 'fpcthpfoziwjamocstbb'
        self.instance.fareProductId = test_value
        self.assertEqual(self.instance.fareProductId, test_value)
    
    def test_transferCount_property(self):
        """
        Test transferCount property
        """
        test_value = int(77)
        self.instance.transferCount = test_value
        self.assertEqual(self.instance.transferCount, test_value)
    
    def test_fromLegGroupId_property(self):
        """
        Test fromLegGroupId property
        """
        test_value = 'tcsniajftqaxtsflqthd'
        self.instance.fromLegGroupId = test_value
        self.assertEqual(self.instance.fromLegGroupId, test_value)
    
    def test_toLegGroupId_property(self):
        """
        Test toLegGroupId property
        """
        test_value = 'iebfocmundozjgwjqxws'
        self.instance.toLegGroupId = test_value
        self.assertEqual(self.instance.toLegGroupId, test_value)
    
    def test_duration_property(self):
        """
        Test duration property
        """
        test_value = int(78)
        self.instance.duration = test_value
        self.assertEqual(self.instance.duration, test_value)
    
    def test_durationType_property(self):
        """
        Test durationType property
        """
        test_value = 'uktkcguysdejgupcxggz'
        self.instance.durationType = test_value
        self.assertEqual(self.instance.durationType, test_value)
    
