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
            site_no='zedvnregwsvajylfdsal',
            datetime='fcyduumwvpbkhkuplpmv',
            value=float(96.87091435622936),
            exception='tdmvdrlwkkswxdpqntrf',
            qualifiers=['crpdwilivtmevjcszegq', 'fdnelhmstfzxtwceclsv', 'tkqquddxvyzkbuuuqner', 'nhvqoytnaqvccvjyxgql'],
            parameter_cd='qifeqgctuckltentoueo',
            timeseries_cd='knewysuoegddsbxycptj'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'zedvnregwsvajylfdsal'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'fcyduumwvpbkhkuplpmv'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(96.87091435622936)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'tdmvdrlwkkswxdpqntrf'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['crpdwilivtmevjcszegq', 'fdnelhmstfzxtwceclsv', 'tkqquddxvyzkbuuuqner', 'nhvqoytnaqvccvjyxgql']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'qifeqgctuckltentoueo'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'knewysuoegddsbxycptj'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    