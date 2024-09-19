"""
Test case for Streamflow
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_iv_producer_data.usgs.instantaneousvalues.streamflow import Streamflow


class Test_Streamflow(unittest.TestCase):
    """
    Test case for Streamflow
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Streamflow.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Streamflow for testing
        """
        instance = Streamflow(
            site_no='mmgueqyyhjggazsfafss',
            datetime='niytyfggaoacmucobpzc',
            value=float(99.26783845444123),
            qualifiers=['osnylfmjgbiviboiyywv', 'dbjqahbfvdhztmwalsgn', 'hhhympdjiywolpdtekns', 'hkqfmcngvdprtoyyhjgd']
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'mmgueqyyhjggazsfafss'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'niytyfggaoacmucobpzc'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(99.26783845444123)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['osnylfmjgbiviboiyywv', 'dbjqahbfvdhztmwalsgn', 'hhhympdjiywolpdtekns', 'hkqfmcngvdprtoyyhjgd']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
