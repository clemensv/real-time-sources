"""
Test case for LakeElevationNGVD29
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_iv_producer_data.usgs.instantaneousvalues.lakeelevationngvd29 import LakeElevationNGVD29


class Test_LakeElevationNGVD29(unittest.TestCase):
    """
    Test case for LakeElevationNGVD29
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_LakeElevationNGVD29.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of LakeElevationNGVD29 for testing
        """
        instance = LakeElevationNGVD29(
            site_no='pkezgykpsfeqkpxofnwq',
            datetime='kdmcxstnacrjacknrafr',
            value=float(43.71289632754287),
            exception='vxxkufeqfphkseqqlmtl',
            qualifiers=['ovnnchobvhumnnhxgmsr', 'bxwrskoyckdujmmhspkk', 'lmimeywjisytgcwmfonf'],
            parameter_cd='cgszreckvfyfidzruunu',
            timeseries_cd='ccvjlrtgewlspnuxrwme'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'pkezgykpsfeqkpxofnwq'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'kdmcxstnacrjacknrafr'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(43.71289632754287)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'vxxkufeqfphkseqqlmtl'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['ovnnchobvhumnnhxgmsr', 'bxwrskoyckdujmmhspkk', 'lmimeywjisytgcwmfonf']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'cgszreckvfyfidzruunu'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'ccvjlrtgewlspnuxrwme'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
