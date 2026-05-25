"""
Test case for Observation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from fmi_finland_mqtt_producer_data.fi.fmi.opendata.airquality.observation import Observation


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
            fmisid='ffvbzhwlpoygmftxrpub',
            station_name='jwdtwpmqlimehlfmggcn',
            observation_time='hlbybreiszamwcbhlimu',
            aqindex=float(69.31137010242985),
            pm10_ug_m3=float(8.30858931655566),
            pm2_5_ug_m3=float(49.00686722601031),
            no2_ug_m3=float(71.08763131420874),
            o3_ug_m3=float(31.901843007842057),
            so2_ug_m3=float(1.53576172060923),
            co_mg_m3=float(55.33162250490823)
        )
        return instance

    
    def test_fmisid_property(self):
        """
        Test fmisid property
        """
        test_value = 'ffvbzhwlpoygmftxrpub'
        self.instance.fmisid = test_value
        self.assertEqual(self.instance.fmisid, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'jwdtwpmqlimehlfmggcn'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_observation_time_property(self):
        """
        Test observation_time property
        """
        test_value = 'hlbybreiszamwcbhlimu'
        self.instance.observation_time = test_value
        self.assertEqual(self.instance.observation_time, test_value)
    
    def test_aqindex_property(self):
        """
        Test aqindex property
        """
        test_value = float(69.31137010242985)
        self.instance.aqindex = test_value
        self.assertEqual(self.instance.aqindex, test_value)
    
    def test_pm10_ug_m3_property(self):
        """
        Test pm10_ug_m3 property
        """
        test_value = float(8.30858931655566)
        self.instance.pm10_ug_m3 = test_value
        self.assertEqual(self.instance.pm10_ug_m3, test_value)
    
    def test_pm2_5_ug_m3_property(self):
        """
        Test pm2_5_ug_m3 property
        """
        test_value = float(49.00686722601031)
        self.instance.pm2_5_ug_m3 = test_value
        self.assertEqual(self.instance.pm2_5_ug_m3, test_value)
    
    def test_no2_ug_m3_property(self):
        """
        Test no2_ug_m3 property
        """
        test_value = float(71.08763131420874)
        self.instance.no2_ug_m3 = test_value
        self.assertEqual(self.instance.no2_ug_m3, test_value)
    
    def test_o3_ug_m3_property(self):
        """
        Test o3_ug_m3 property
        """
        test_value = float(31.901843007842057)
        self.instance.o3_ug_m3 = test_value
        self.assertEqual(self.instance.o3_ug_m3, test_value)
    
    def test_so2_ug_m3_property(self):
        """
        Test so2_ug_m3 property
        """
        test_value = float(1.53576172060923)
        self.instance.so2_ug_m3 = test_value
        self.assertEqual(self.instance.so2_ug_m3, test_value)
    
    def test_co_mg_m3_property(self):
        """
        Test co_mg_m3 property
        """
        test_value = float(55.33162250490823)
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

