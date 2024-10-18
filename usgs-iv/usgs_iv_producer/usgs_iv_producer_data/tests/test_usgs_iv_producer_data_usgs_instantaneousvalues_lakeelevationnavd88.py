"""
Test case for LakeElevationNAVD88
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_iv_producer_data.usgs.instantaneousvalues.lakeelevationnavd88 import LakeElevationNAVD88


class Test_LakeElevationNAVD88(unittest.TestCase):
    """
    Test case for LakeElevationNAVD88
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_LakeElevationNAVD88.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of LakeElevationNAVD88 for testing
        """
        instance = LakeElevationNAVD88(
            site_no='seplsabpiytqusleplvt',
            datetime='xmwthwfbvhtqmuxpecnq',
            value=float(44.87034349038941),
            exception='uxxggeivizuspjdgjcxg',
            qualifiers=['mledcdjgyhabqoldpbbw', 'shobqojaxcmxetwsioeo'],
            parameter_cd='oshyibqilypjgvmlddgo',
            timeseries_cd='ykfkslzefeeqthcjitwv'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'seplsabpiytqusleplvt'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'xmwthwfbvhtqmuxpecnq'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(44.87034349038941)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'uxxggeivizuspjdgjcxg'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['mledcdjgyhabqoldpbbw', 'shobqojaxcmxetwsioeo']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'oshyibqilypjgvmlddgo'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'ykfkslzefeeqthcjitwv'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
