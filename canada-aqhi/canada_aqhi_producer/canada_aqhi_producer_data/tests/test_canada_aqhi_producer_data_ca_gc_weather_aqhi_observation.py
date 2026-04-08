"""
Test case for Observation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from canada_aqhi_producer_data.ca.gc.weather.aqhi.observation import Observation


class Test_Observation(unittest.TestCase):
    """
    Test case for Observation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Observation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Observation for testing
        """
        instance = Observation(
            province='mlxnzivetubbxresykph',
            community_name='lzllhxgdegxvrjimxbyi',
            cgndb_code='lvvaozzkuuvycyihudax',
            observation_datetime='klxyuqkxgtdauwnlvadx',
            aqhi=float(68.20060478337365),
            aqhi_category='ivembgabaamjfmbuxjey'
        )
        return instance

    
    def test_province_property(self):
        """
        Test province property
        """
        test_value = 'mlxnzivetubbxresykph'
        self.instance.province = test_value
        self.assertEqual(self.instance.province, test_value)
    
    def test_community_name_property(self):
        """
        Test community_name property
        """
        test_value = 'lzllhxgdegxvrjimxbyi'
        self.instance.community_name = test_value
        self.assertEqual(self.instance.community_name, test_value)
    
    def test_cgndb_code_property(self):
        """
        Test cgndb_code property
        """
        test_value = 'lvvaozzkuuvycyihudax'
        self.instance.cgndb_code = test_value
        self.assertEqual(self.instance.cgndb_code, test_value)
    
    def test_observation_datetime_property(self):
        """
        Test observation_datetime property
        """
        test_value = 'klxyuqkxgtdauwnlvadx'
        self.instance.observation_datetime = test_value
        self.assertEqual(self.instance.observation_datetime, test_value)
    
    def test_aqhi_property(self):
        """
        Test aqhi property
        """
        test_value = float(68.20060478337365)
        self.instance.aqhi = test_value
        self.assertEqual(self.instance.aqhi, test_value)
    
    def test_aqhi_category_property(self):
        """
        Test aqhi_category property
        """
        test_value = 'ivembgabaamjfmbuxjey'
        self.instance.aqhi_category = test_value
        self.assertEqual(self.instance.aqhi_category, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Observation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
