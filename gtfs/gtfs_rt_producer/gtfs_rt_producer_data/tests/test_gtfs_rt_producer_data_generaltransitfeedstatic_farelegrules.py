"""
Test case for FareLegRules
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedstatic.farelegrules import FareLegRules


class Test_FareLegRules(unittest.TestCase):
    """
    Test case for FareLegRules
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_FareLegRules.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of FareLegRules for testing
        """
        instance = FareLegRules(
            fareLegRuleId='cylsmfyrjeqelhhfydtz',
            fareProductId='haybihejuqyjyqeektpv',
            legGroupId='vkmyxfrqqgmnuftphata',
            networkId='uabhzxnkaxxhusqovptb',
            fromAreaId='equtxhxrimehbbeqevpu',
            toAreaId='vybwwflquxfpmqnnjwix'
        )
        return instance

    
    def test_fareLegRuleId_property(self):
        """
        Test fareLegRuleId property
        """
        test_value = 'cylsmfyrjeqelhhfydtz'
        self.instance.fareLegRuleId = test_value
        self.assertEqual(self.instance.fareLegRuleId, test_value)
    
    def test_fareProductId_property(self):
        """
        Test fareProductId property
        """
        test_value = 'haybihejuqyjyqeektpv'
        self.instance.fareProductId = test_value
        self.assertEqual(self.instance.fareProductId, test_value)
    
    def test_legGroupId_property(self):
        """
        Test legGroupId property
        """
        test_value = 'vkmyxfrqqgmnuftphata'
        self.instance.legGroupId = test_value
        self.assertEqual(self.instance.legGroupId, test_value)
    
    def test_networkId_property(self):
        """
        Test networkId property
        """
        test_value = 'uabhzxnkaxxhusqovptb'
        self.instance.networkId = test_value
        self.assertEqual(self.instance.networkId, test_value)
    
    def test_fromAreaId_property(self):
        """
        Test fromAreaId property
        """
        test_value = 'equtxhxrimehbbeqevpu'
        self.instance.fromAreaId = test_value
        self.assertEqual(self.instance.fromAreaId, test_value)
    
    def test_toAreaId_property(self):
        """
        Test toAreaId property
        """
        test_value = 'vybwwflquxfpmqnnjwix'
        self.instance.toAreaId = test_value
        self.assertEqual(self.instance.toAreaId, test_value)
    
