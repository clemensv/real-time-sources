"""
Test case for Observation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from fmi_finland_producer_data.fi.fmi.opendata.airquality.observation import Observation


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
            fmisid='apjycxzyuobeuyfsdzxe',
            station_name='kwqrutwqrudfzviekcwh',
            observation_time='xvolrpqlvbnqakzypick',
            aqindex=float(67.11132549064253),
            pm10_ug_m3=float(15.133687369567506),
            pm2_5_ug_m3=float(70.72747234628142),
            no2_ug_m3=float(74.50750972775816),
            o3_ug_m3=float(96.91893314806096),
            so2_ug_m3=float(87.81549945583762),
            co_mg_m3=float(14.90214973087528)
        )
        return instance

    
    def test_fmisid_property(self):
        """
        Test fmisid property
        """
        test_value = 'apjycxzyuobeuyfsdzxe'
        self.instance.fmisid = test_value
        self.assertEqual(self.instance.fmisid, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'kwqrutwqrudfzviekcwh'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_observation_time_property(self):
        """
        Test observation_time property
        """
        test_value = 'xvolrpqlvbnqakzypick'
        self.instance.observation_time = test_value
        self.assertEqual(self.instance.observation_time, test_value)
    
    def test_aqindex_property(self):
        """
        Test aqindex property
        """
        test_value = float(67.11132549064253)
        self.instance.aqindex = test_value
        self.assertEqual(self.instance.aqindex, test_value)
    
    def test_pm10_ug_m3_property(self):
        """
        Test pm10_ug_m3 property
        """
        test_value = float(15.133687369567506)
        self.instance.pm10_ug_m3 = test_value
        self.assertEqual(self.instance.pm10_ug_m3, test_value)
    
    def test_pm2_5_ug_m3_property(self):
        """
        Test pm2_5_ug_m3 property
        """
        test_value = float(70.72747234628142)
        self.instance.pm2_5_ug_m3 = test_value
        self.assertEqual(self.instance.pm2_5_ug_m3, test_value)
    
    def test_no2_ug_m3_property(self):
        """
        Test no2_ug_m3 property
        """
        test_value = float(74.50750972775816)
        self.instance.no2_ug_m3 = test_value
        self.assertEqual(self.instance.no2_ug_m3, test_value)
    
    def test_o3_ug_m3_property(self):
        """
        Test o3_ug_m3 property
        """
        test_value = float(96.91893314806096)
        self.instance.o3_ug_m3 = test_value
        self.assertEqual(self.instance.o3_ug_m3, test_value)
    
    def test_so2_ug_m3_property(self):
        """
        Test so2_ug_m3 property
        """
        test_value = float(87.81549945583762)
        self.instance.so2_ug_m3 = test_value
        self.assertEqual(self.instance.so2_ug_m3, test_value)
    
    def test_co_mg_m3_property(self):
        """
        Test co_mg_m3 property
        """
        test_value = float(14.90214973087528)
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

