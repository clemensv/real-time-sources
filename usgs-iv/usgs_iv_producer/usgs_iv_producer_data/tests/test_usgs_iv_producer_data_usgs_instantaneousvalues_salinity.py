"""
Test case for Salinity
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_iv_producer_data.usgs.instantaneousvalues.salinity import Salinity


class Test_Salinity(unittest.TestCase):
    """
    Test case for Salinity
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Salinity.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Salinity for testing
        """
        instance = Salinity(
            site_no='mrywicxelxbicqzauyma',
            datetime='rvnsgnenswnbkerqxytw',
            value=float(54.58085545990248),
            exception='vmmlmhfhwrpddqkjyprs',
            qualifiers=['dbelwvodevwdlnnpoiea', 'tnoqolhwvsxfupgchhom', 'rveejktifuolnjibulev'],
            parameter_cd='fahjorkxkuefzggsgdaw',
            timeseries_cd='msddwepmjpznwmhzzklb'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'mrywicxelxbicqzauyma'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'rvnsgnenswnbkerqxytw'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(54.58085545990248)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'vmmlmhfhwrpddqkjyprs'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['dbelwvodevwdlnnpoiea', 'tnoqolhwvsxfupgchhom', 'rveejktifuolnjibulev']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'fahjorkxkuefzggsgdaw'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'msddwepmjpznwmhzzklb'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
