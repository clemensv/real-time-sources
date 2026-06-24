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
            fareLegRuleId='fmkwdcvaxbazuynwlehe',
            fareProductId='mdrejambpkhdnydttcjm',
            legGroupId='ooiuxdnfqzvtxhepcbyh',
            networkId='fzazswszeupxxgamkjve',
            fromAreaId='ttflqhftriwqjctchevq',
            toAreaId='wwxraosfletmfnyolcvh'
        )
        return instance

    
    def test_fareLegRuleId_property(self):
        """
        Test fareLegRuleId property
        """
        test_value = 'fmkwdcvaxbazuynwlehe'
        self.instance.fareLegRuleId = test_value
        self.assertEqual(self.instance.fareLegRuleId, test_value)
    
    def test_fareProductId_property(self):
        """
        Test fareProductId property
        """
        test_value = 'mdrejambpkhdnydttcjm'
        self.instance.fareProductId = test_value
        self.assertEqual(self.instance.fareProductId, test_value)
    
    def test_legGroupId_property(self):
        """
        Test legGroupId property
        """
        test_value = 'ooiuxdnfqzvtxhepcbyh'
        self.instance.legGroupId = test_value
        self.assertEqual(self.instance.legGroupId, test_value)
    
    def test_networkId_property(self):
        """
        Test networkId property
        """
        test_value = 'fzazswszeupxxgamkjve'
        self.instance.networkId = test_value
        self.assertEqual(self.instance.networkId, test_value)
    
    def test_fromAreaId_property(self):
        """
        Test fromAreaId property
        """
        test_value = 'ttflqhftriwqjctchevq'
        self.instance.fromAreaId = test_value
        self.assertEqual(self.instance.fromAreaId, test_value)
    
    def test_toAreaId_property(self):
        """
        Test toAreaId property
        """
        test_value = 'wwxraosfletmfnyolcvh'
        self.instance.toAreaId = test_value
        self.assertEqual(self.instance.toAreaId, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = FareLegRules.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = FareLegRules.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

