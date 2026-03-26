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
            fareLegRuleId='fzlzpfprznnskximhzsc',
            fareProductId='mduyxykmerlwicjhcljr',
            legGroupId='boifwlqujrshlnzxemcu',
            networkId='hylzwygnkxygatrlhovw',
            fromAreaId='mbaeakbtmcvxpnceofmv',
            toAreaId='sezaxymdskapjczuncuf'
        )
        return instance

    
    def test_fareLegRuleId_property(self):
        """
        Test fareLegRuleId property
        """
        test_value = 'fzlzpfprznnskximhzsc'
        self.instance.fareLegRuleId = test_value
        self.assertEqual(self.instance.fareLegRuleId, test_value)
    
    def test_fareProductId_property(self):
        """
        Test fareProductId property
        """
        test_value = 'mduyxykmerlwicjhcljr'
        self.instance.fareProductId = test_value
        self.assertEqual(self.instance.fareProductId, test_value)
    
    def test_legGroupId_property(self):
        """
        Test legGroupId property
        """
        test_value = 'boifwlqujrshlnzxemcu'
        self.instance.legGroupId = test_value
        self.assertEqual(self.instance.legGroupId, test_value)
    
    def test_networkId_property(self):
        """
        Test networkId property
        """
        test_value = 'hylzwygnkxygatrlhovw'
        self.instance.networkId = test_value
        self.assertEqual(self.instance.networkId, test_value)
    
    def test_fromAreaId_property(self):
        """
        Test fromAreaId property
        """
        test_value = 'mbaeakbtmcvxpnceofmv'
        self.instance.fromAreaId = test_value
        self.assertEqual(self.instance.fromAreaId, test_value)
    
    def test_toAreaId_property(self):
        """
        Test toAreaId property
        """
        test_value = 'sezaxymdskapjczuncuf'
        self.instance.toAreaId = test_value
        self.assertEqual(self.instance.toAreaId, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = FareLegRules.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
