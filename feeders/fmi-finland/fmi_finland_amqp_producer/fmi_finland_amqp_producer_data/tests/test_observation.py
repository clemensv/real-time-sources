"""
Test case for Observation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from fmi_finland_amqp_producer_data.fi.fmi.opendata.airquality.observation import Observation


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
            fmisid='btzbsvlmdsslechoknto',
            station_name='tfyjzahujvtjergyvncq',
            observation_time='dqalwrgjeoowpydvwiih',
            aqindex=float(12.756703332859098),
            pm10_ug_m3=float(27.111537007381237),
            pm2_5_ug_m3=float(24.2455430368423),
            no2_ug_m3=float(24.109999249776635),
            o3_ug_m3=float(69.47465662961406),
            so2_ug_m3=float(22.045471382548033),
            co_mg_m3=float(38.6569612774626)
        )
        return instance

    
    def test_fmisid_property(self):
        """
        Test fmisid property
        """
        test_value = 'btzbsvlmdsslechoknto'
        self.instance.fmisid = test_value
        self.assertEqual(self.instance.fmisid, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'tfyjzahujvtjergyvncq'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_observation_time_property(self):
        """
        Test observation_time property
        """
        test_value = 'dqalwrgjeoowpydvwiih'
        self.instance.observation_time = test_value
        self.assertEqual(self.instance.observation_time, test_value)
    
    def test_aqindex_property(self):
        """
        Test aqindex property
        """
        test_value = float(12.756703332859098)
        self.instance.aqindex = test_value
        self.assertEqual(self.instance.aqindex, test_value)
    
    def test_pm10_ug_m3_property(self):
        """
        Test pm10_ug_m3 property
        """
        test_value = float(27.111537007381237)
        self.instance.pm10_ug_m3 = test_value
        self.assertEqual(self.instance.pm10_ug_m3, test_value)
    
    def test_pm2_5_ug_m3_property(self):
        """
        Test pm2_5_ug_m3 property
        """
        test_value = float(24.2455430368423)
        self.instance.pm2_5_ug_m3 = test_value
        self.assertEqual(self.instance.pm2_5_ug_m3, test_value)
    
    def test_no2_ug_m3_property(self):
        """
        Test no2_ug_m3 property
        """
        test_value = float(24.109999249776635)
        self.instance.no2_ug_m3 = test_value
        self.assertEqual(self.instance.no2_ug_m3, test_value)
    
    def test_o3_ug_m3_property(self):
        """
        Test o3_ug_m3 property
        """
        test_value = float(69.47465662961406)
        self.instance.o3_ug_m3 = test_value
        self.assertEqual(self.instance.o3_ug_m3, test_value)
    
    def test_so2_ug_m3_property(self):
        """
        Test so2_ug_m3 property
        """
        test_value = float(22.045471382548033)
        self.instance.so2_ug_m3 = test_value
        self.assertEqual(self.instance.so2_ug_m3, test_value)
    
    def test_co_mg_m3_property(self):
        """
        Test co_mg_m3 property
        """
        test_value = float(38.6569612774626)
        self.instance.co_mg_m3 = test_value
        self.assertEqual(self.instance.co_mg_m3, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Observation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Observation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

