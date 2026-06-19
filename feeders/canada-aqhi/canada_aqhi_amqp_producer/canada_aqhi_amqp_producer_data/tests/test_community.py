"""
Test case for Community
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from canada_aqhi_amqp_producer_data.ca.gc.weather.aqhi.community import Community


class Test_Community(unittest.TestCase):
    """
    Test case for Community
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Community.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Community for testing
        """
        instance = Community(
            province='wykkysroroglgbspxgch',
            community_name='ppvsrnjxxlshpnehspcv',
            cgndb_code='ggpfwgfgvimieiokswub',
            latitude=float(14.189259319358605),
            longitude=float(30.506623781642105),
            observation_url='hzwtmctzfhpvkipdwipb',
            forecast_url='vbwdmivjiwdicbfsvvsb'
        )
        return instance

    
    def test_province_property(self):
        """
        Test province property
        """
        test_value = 'wykkysroroglgbspxgch'
        self.instance.province = test_value
        self.assertEqual(self.instance.province, test_value)
    
    def test_community_name_property(self):
        """
        Test community_name property
        """
        test_value = 'ppvsrnjxxlshpnehspcv'
        self.instance.community_name = test_value
        self.assertEqual(self.instance.community_name, test_value)
    
    def test_cgndb_code_property(self):
        """
        Test cgndb_code property
        """
        test_value = 'ggpfwgfgvimieiokswub'
        self.instance.cgndb_code = test_value
        self.assertEqual(self.instance.cgndb_code, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(14.189259319358605)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(30.506623781642105)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_observation_url_property(self):
        """
        Test observation_url property
        """
        test_value = 'hzwtmctzfhpvkipdwipb'
        self.instance.observation_url = test_value
        self.assertEqual(self.instance.observation_url, test_value)
    
    def test_forecast_url_property(self):
        """
        Test forecast_url property
        """
        test_value = 'vbwdmivjiwdicbfsvvsb'
        self.instance.forecast_url = test_value
        self.assertEqual(self.instance.forecast_url, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Community.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Community.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

