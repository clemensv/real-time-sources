"""
Test case for LakeElevationNGVD29
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs-iv-producer_data.usgs.instantaneousvalues.lakeelevationngvd29 import LakeElevationNGVD29


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
            site_no='lvxrcsgfjsgansiyeoek',
            datetime='jovwierhnsdmupgkvmyh',
            value=float(92.90489074256534),
            exception='fxdoepnwyvlhflcpxezc',
            qualifiers=['lbsjpcspcdvpqahygvhy', 'zztdrvkzirgglozpksas', 'pwmbsmgoeihlpeeibrlw', 'dbvgmehbqqjewbtxlpfi', 'bbmwbwjdrgvfmjknkrcb'],
            parameter_cd='twnfrrjtzkaweweysqjw',
            timeseries_cd='oonxnojqtwsyprriqbsf'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'lvxrcsgfjsgansiyeoek'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'jovwierhnsdmupgkvmyh'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(92.90489074256534)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_exception_property(self):
        """
        Test exception property
        """
        test_value = 'fxdoepnwyvlhflcpxezc'
        self.instance.exception = test_value
        self.assertEqual(self.instance.exception, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['lbsjpcspcdvpqahygvhy', 'zztdrvkzirgglozpksas', 'pwmbsmgoeihlpeeibrlw', 'dbvgmehbqqjewbtxlpfi', 'bbmwbwjdrgvfmjknkrcb']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'twnfrrjtzkaweweysqjw'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'oonxnojqtwsyprriqbsf'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = LakeElevationNGVD29.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
