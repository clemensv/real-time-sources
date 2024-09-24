"""
Test case for ReservoirStorage
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_iv_producer_data.usgs.instantaneousvalues.reservoirstorage import ReservoirStorage


class Test_ReservoirStorage(unittest.TestCase):
    """
    Test case for ReservoirStorage
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_ReservoirStorage.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of ReservoirStorage for testing
        """
        instance = ReservoirStorage(
            site_no='iwljpgzndootutmosnca',
            datetime='bmikfsyyebiyhxsnngxm',
            value=float(84.62145822159708),
            exception='gnrzyxqqspwujztvjzgw',
            qualifiers=['olxpllhnovrgmkxybyli', 'qgoxvnsaexuhugqwigka', 'syvbclhrfwpxmtfztvxn', 'ticcthbysudznypttfzx'],
            parameter_cd='qudmfxfzkgdmvwemmnza',
            timeseries_cd='szejpptyhuqyvllfpfub'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'iwljpgzndootutmosnca'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'bmikfsyyebiyhxsnngxm'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(84.62145822159708)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'gnrzyxqqspwujztvjzgw'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['olxpllhnovrgmkxybyli', 'qgoxvnsaexuhugqwigka', 'syvbclhrfwpxmtfztvxn', 'ticcthbysudznypttfzx']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'qudmfxfzkgdmvwemmnza'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'szejpptyhuqyvllfpfub'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
