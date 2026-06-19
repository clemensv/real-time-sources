"""
Test case for PH
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_iv_producer_data.usgs.instantaneousvalues.ph import PH


class Test_PH(unittest.TestCase):
    """
    Test case for PH
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_PH.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of PH for testing
        """
        instance = PH(
            site_no='xiheazvtseegyozagnni',
            datetime='jsnxxcmfwyirxfoxocfk',
            value=float(87.38043480482276),
            exception='kvpsdbosggwrpavcxtnt',
            qualifiers=['kmqunkbhyijcehddstwp', 'bmcsvyvacujuywpjqfrh', 'vfjydgrznvsokcmisuyq'],
            parameter_cd='azrooqwtfftpxzvvlkbz',
            timeseries_cd='qlniybpcdiumbboiwjcv'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'xiheazvtseegyozagnni'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'jsnxxcmfwyirxfoxocfk'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(87.38043480482276)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'kvpsdbosggwrpavcxtnt'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['kmqunkbhyijcehddstwp', 'bmcsvyvacujuywpjqfrh', 'vfjydgrznvsokcmisuyq']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'azrooqwtfftpxzvvlkbz'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'qlniybpcdiumbboiwjcv'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = PH.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = PH.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

