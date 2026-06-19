"""
Test case for GageHeight
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_iv_producer_data.usgs.instantaneousvalues.gageheight import GageHeight


class Test_GageHeight(unittest.TestCase):
    """
    Test case for GageHeight
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_GageHeight.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of GageHeight for testing
        """
        instance = GageHeight(
            site_no='hnzckpumgcvurxibpoxt',
            datetime='cmlcpbwqphursjbwpvxq',
            value=float(6.967991270688412),
            exception='ffugdislpausqjqqakff',
            qualifiers=['cfzzxxhwrirldwjetbyy', 'njjvkmidqtbvdpcghgzu', 'ozozkuagzdxohitcmebk', 'fdvcduxzttgysjbmoxep'],
            parameter_cd='skiazledbolzursqlflu',
            timeseries_cd='peljfjymzvoqkrfvpthf'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'hnzckpumgcvurxibpoxt'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'cmlcpbwqphursjbwpvxq'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(6.967991270688412)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'ffugdislpausqjqqakff'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['cfzzxxhwrirldwjetbyy', 'njjvkmidqtbvdpcghgzu', 'ozozkuagzdxohitcmebk', 'fdvcduxzttgysjbmoxep']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'skiazledbolzursqlflu'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'peljfjymzvoqkrfvpthf'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = GageHeight.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = GageHeight.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

