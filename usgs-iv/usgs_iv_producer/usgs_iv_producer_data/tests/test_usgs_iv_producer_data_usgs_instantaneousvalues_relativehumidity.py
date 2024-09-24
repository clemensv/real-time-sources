"""
Test case for RelativeHumidity
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_iv_producer_data.usgs.instantaneousvalues.relativehumidity import RelativeHumidity


class Test_RelativeHumidity(unittest.TestCase):
    """
    Test case for RelativeHumidity
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_RelativeHumidity.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of RelativeHumidity for testing
        """
        instance = RelativeHumidity(
            site_no='xljwfvoywvpildqsgwgo',
            datetime='hkmruulaxfusvjbbywro',
            value=float(8.983126298893174),
            exception='gclelycxxstdepczrvej',
            qualifiers=['ksfqwfklbzbygrkrfquh', 'ketbqldmnamnyqayctdy', 'ktszhbivfjeczqdfwbjt'],
            parameter_cd='dulikfjyjaluiqpallfj',
            timeseries_cd='ftvkzcnxiifwkertwkoa'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'xljwfvoywvpildqsgwgo'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'hkmruulaxfusvjbbywro'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(8.983126298893174)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'gclelycxxstdepczrvej'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['ksfqwfklbzbygrkrfquh', 'ketbqldmnamnyqayctdy', 'ktszhbivfjeczqdfwbjt']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'dulikfjyjaluiqpallfj'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'ftvkzcnxiifwkertwkoa'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
