"""
Test case for Attributions
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedstatic.attributions import Attributions

class Test_Attributions(unittest.TestCase):
    """
    Test case for Attributions
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Attributions.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Attributions for testing
        """
        instance = Attributions(
            attributionId='znhqbtqcufhiauxgbhnx',
            agencyId='mpkkzzkcxgenxfvxqcnf',
            routeId='xdkqyxmxhwzgoddibdgm',
            tripId='zmirwgjzgqoueyowykbt',
            organizationName='vlolwsbjcppsxtutluuz',
            isProducer=int(78),
            isOperator=int(62),
            isAuthority=int(88),
            attributionUrl='xhmaanmvtgmdcradwvjz',
            attributionEmail='hvnykkmixmehqlgbahki',
            attributionPhone='thxysegrzbxbuifjzgmy'
        )
        return instance

    
    def test_attributionId_property(self):
        """
        Test attributionId property
        """
        test_value = 'znhqbtqcufhiauxgbhnx'
        self.instance.attributionId = test_value
        self.assertEqual(self.instance.attributionId, test_value)
    
    def test_agencyId_property(self):
        """
        Test agencyId property
        """
        test_value = 'mpkkzzkcxgenxfvxqcnf'
        self.instance.agencyId = test_value
        self.assertEqual(self.instance.agencyId, test_value)
    
    def test_routeId_property(self):
        """
        Test routeId property
        """
        test_value = 'xdkqyxmxhwzgoddibdgm'
        self.instance.routeId = test_value
        self.assertEqual(self.instance.routeId, test_value)
    
    def test_tripId_property(self):
        """
        Test tripId property
        """
        test_value = 'zmirwgjzgqoueyowykbt'
        self.instance.tripId = test_value
        self.assertEqual(self.instance.tripId, test_value)
    
    def test_organizationName_property(self):
        """
        Test organizationName property
        """
        test_value = 'vlolwsbjcppsxtutluuz'
        self.instance.organizationName = test_value
        self.assertEqual(self.instance.organizationName, test_value)
    
    def test_isProducer_property(self):
        """
        Test isProducer property
        """
        test_value = int(78)
        self.instance.isProducer = test_value
        self.assertEqual(self.instance.isProducer, test_value)
    
    def test_isOperator_property(self):
        """
        Test isOperator property
        """
        test_value = int(62)
        self.instance.isOperator = test_value
        self.assertEqual(self.instance.isOperator, test_value)
    
    def test_isAuthority_property(self):
        """
        Test isAuthority property
        """
        test_value = int(88)
        self.instance.isAuthority = test_value
        self.assertEqual(self.instance.isAuthority, test_value)
    
    def test_attributionUrl_property(self):
        """
        Test attributionUrl property
        """
        test_value = 'xhmaanmvtgmdcradwvjz'
        self.instance.attributionUrl = test_value
        self.assertEqual(self.instance.attributionUrl, test_value)
    
    def test_attributionEmail_property(self):
        """
        Test attributionEmail property
        """
        test_value = 'hvnykkmixmehqlgbahki'
        self.instance.attributionEmail = test_value
        self.assertEqual(self.instance.attributionEmail, test_value)
    
    def test_attributionPhone_property(self):
        """
        Test attributionPhone property
        """
        test_value = 'thxysegrzbxbuifjzgmy'
        self.instance.attributionPhone = test_value
        self.assertEqual(self.instance.attributionPhone, test_value)
    
