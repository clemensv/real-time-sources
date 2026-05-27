"""
Test case for RelativeHumidity
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_iv_mqtt_producer_data.usgs.instantaneousvalues.relativehumidity import RelativeHumidity


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
            site_no='gzacgxceimmzgdcwndnq',
            datetime='klroqcrsoabmildyvban',
            value=float(35.70344610598186),
            exception='onzdpybnudmjmmmffvip',
            qualifiers=['ouptthcgwjwpjlqdepgf', 'nfhxbxjfgkrkgbukurrj', 'yessczjcbxzfjftabjjp', 'iuhqfelnirhotoxcwqdu'],
            parameter_cd='gjidfjlgidibyhsacuij',
            timeseries_cd='smgykflckjzfufitrtxn'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'gzacgxceimmzgdcwndnq'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'klroqcrsoabmildyvban'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(35.70344610598186)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'onzdpybnudmjmmmffvip'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['ouptthcgwjwpjlqdepgf', 'nfhxbxjfgkrkgbukurrj', 'yessczjcbxzfjftabjjp', 'iuhqfelnirhotoxcwqdu']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'gjidfjlgidibyhsacuij'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'smgykflckjzfufitrtxn'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = RelativeHumidity.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = RelativeHumidity.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

