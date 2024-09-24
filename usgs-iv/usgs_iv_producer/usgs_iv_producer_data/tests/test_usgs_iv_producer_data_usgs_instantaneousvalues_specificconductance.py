"""
Test case for SpecificConductance
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_iv_producer_data.usgs.instantaneousvalues.specificconductance import SpecificConductance


class Test_SpecificConductance(unittest.TestCase):
    """
    Test case for SpecificConductance
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_SpecificConductance.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of SpecificConductance for testing
        """
        instance = SpecificConductance(
            site_no='grambmaloojgtppmkxfe',
            datetime='jwmgkmbccwdzrjpsfosi',
            value=float(61.818716255243466),
            exception='wsqoawarjqcqubqiogiw',
            qualifiers=['akqntsutvuzfeozqyvgs', 'tvphdkezeduxmddeeiux', 'ehlurljvyhllddmxbume', 'myepbbuqkhpvsaymlwgl'],
            parameter_cd='jeidxkiicewjjcanzslh',
            timeseries_cd='sqnmkggjsttahuhlnlfy'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'grambmaloojgtppmkxfe'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'jwmgkmbccwdzrjpsfosi'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(61.818716255243466)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'wsqoawarjqcqubqiogiw'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['akqntsutvuzfeozqyvgs', 'tvphdkezeduxmddeeiux', 'ehlurljvyhllddmxbume', 'myepbbuqkhpvsaymlwgl']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'jeidxkiicewjjcanzslh'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'sqnmkggjsttahuhlnlfy'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
