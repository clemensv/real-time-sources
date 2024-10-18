"""
Test case for GateOpening
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_iv_producer_data.usgs.instantaneousvalues.gateopening import GateOpening


class Test_GateOpening(unittest.TestCase):
    """
    Test case for GateOpening
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_GateOpening.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of GateOpening for testing
        """
        instance = GateOpening(
            site_no='lljaerogvfwhpiioyrpg',
            datetime='pgjtyrdgeeotwpvnvjij',
            value=float(59.587877058611426),
            exception='lvhhcqbhztosmgvqtakn',
            qualifiers=['cvnnfdjflnqawytypvwq', 'jnognmfdbznwoonhsgoy', 'ffahpvcawgeesnxqzgok', 'drbaxcdhbjyuwwvqbael', 'ybsvvklgbekklhwhdwnj'],
            parameter_cd='namqrpmdphyeaeeeurae',
            timeseries_cd='vzeqdcvbphagdwpxxdxx'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'lljaerogvfwhpiioyrpg'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'pgjtyrdgeeotwpvnvjij'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(59.587877058611426)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'lvhhcqbhztosmgvqtakn'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['cvnnfdjflnqawytypvwq', 'jnognmfdbznwoonhsgoy', 'ffahpvcawgeesnxqzgok', 'drbaxcdhbjyuwwvqbael', 'ybsvvklgbekklhwhdwnj']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'namqrpmdphyeaeeeurae'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'vzeqdcvbphagdwpxxdxx'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
