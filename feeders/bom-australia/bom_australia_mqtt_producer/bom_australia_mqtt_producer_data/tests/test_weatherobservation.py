"""
Test case for WeatherObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from bom_australia_mqtt_producer_data.weatherobservation import WeatherObservation
import datetime


class Test_WeatherObservation(unittest.TestCase):
    """
    Test case for WeatherObservation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_WeatherObservation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of WeatherObservation for testing
        """
        instance = WeatherObservation(
            station_wmo='qszjrsuhbjaxregxrykd',
            station_name='rskxwxfmarqfzmnfeopj',
            observation_time_utc=datetime.datetime.now(datetime.timezone.utc),
            local_time='bipvaowctouqjfhlelol',
            air_temp=float(50.5928473288046),
            apparent_temp=float(0.17574988246445988),
            dewpt=float(22.897777866865333),
            rel_hum=int(51),
            delta_t=float(3.5421577195516307),
            wind_dir='pkgxswzaffaevrggyfut',
            wind_spd_kmh=int(34),
            wind_spd_kt=int(38),
            gust_kmh=int(8),
            gust_kt=int(40),
            press=float(26.922259427733252),
            press_qnh=float(11.042695478689712),
            press_msl=float(24.732484525716913),
            press_tend='mpsmhpltfnztiifytfau',
            rain_trace='vpcyjeicoakhztdlvnuu',
            cloud='hezokzrsvjknxfmkmkei',
            cloud_oktas=int(15),
            cloud_base_m=int(50),
            cloud_type='anearsotwyujjpihetsj',
            vis_km='cyxaeihzblcewmjwzbvd',
            weather='ksjvmrfhnfgcfoguhell',
            sea_state='gfqhcmzbjiyqhejkymmq',
            swell_dir_worded='njaptytxmztlttngfohz',
            swell_height=float(93.33219979245716),
            swell_period=float(17.497465836248715),
            latitude=float(34.49555367936888),
            longitude=float(6.997588140317501),
            state='mjtzquauwjtjrlqgyxzz'
        )
        return instance

    
    def test_station_wmo_property(self):
        """
        Test station_wmo property
        """
        test_value = 'qszjrsuhbjaxregxrykd'
        self.instance.station_wmo = test_value
        self.assertEqual(self.instance.station_wmo, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'rskxwxfmarqfzmnfeopj'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_observation_time_utc_property(self):
        """
        Test observation_time_utc property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.observation_time_utc = test_value
        self.assertEqual(self.instance.observation_time_utc, test_value)
    
    def test_local_time_property(self):
        """
        Test local_time property
        """
        test_value = 'bipvaowctouqjfhlelol'
        self.instance.local_time = test_value
        self.assertEqual(self.instance.local_time, test_value)
    
    def test_air_temp_property(self):
        """
        Test air_temp property
        """
        test_value = float(50.5928473288046)
        self.instance.air_temp = test_value
        self.assertEqual(self.instance.air_temp, test_value)
    
    def test_apparent_temp_property(self):
        """
        Test apparent_temp property
        """
        test_value = float(0.17574988246445988)
        self.instance.apparent_temp = test_value
        self.assertEqual(self.instance.apparent_temp, test_value)
    
    def test_dewpt_property(self):
        """
        Test dewpt property
        """
        test_value = float(22.897777866865333)
        self.instance.dewpt = test_value
        self.assertEqual(self.instance.dewpt, test_value)
    
    def test_rel_hum_property(self):
        """
        Test rel_hum property
        """
        test_value = int(51)
        self.instance.rel_hum = test_value
        self.assertEqual(self.instance.rel_hum, test_value)
    
    def test_delta_t_property(self):
        """
        Test delta_t property
        """
        test_value = float(3.5421577195516307)
        self.instance.delta_t = test_value
        self.assertEqual(self.instance.delta_t, test_value)
    
    def test_wind_dir_property(self):
        """
        Test wind_dir property
        """
        test_value = 'pkgxswzaffaevrggyfut'
        self.instance.wind_dir = test_value
        self.assertEqual(self.instance.wind_dir, test_value)
    
    def test_wind_spd_kmh_property(self):
        """
        Test wind_spd_kmh property
        """
        test_value = int(34)
        self.instance.wind_spd_kmh = test_value
        self.assertEqual(self.instance.wind_spd_kmh, test_value)
    
    def test_wind_spd_kt_property(self):
        """
        Test wind_spd_kt property
        """
        test_value = int(38)
        self.instance.wind_spd_kt = test_value
        self.assertEqual(self.instance.wind_spd_kt, test_value)
    
    def test_gust_kmh_property(self):
        """
        Test gust_kmh property
        """
        test_value = int(8)
        self.instance.gust_kmh = test_value
        self.assertEqual(self.instance.gust_kmh, test_value)
    
    def test_gust_kt_property(self):
        """
        Test gust_kt property
        """
        test_value = int(40)
        self.instance.gust_kt = test_value
        self.assertEqual(self.instance.gust_kt, test_value)
    
    def test_press_property(self):
        """
        Test press property
        """
        test_value = float(26.922259427733252)
        self.instance.press = test_value
        self.assertEqual(self.instance.press, test_value)
    
    def test_press_qnh_property(self):
        """
        Test press_qnh property
        """
        test_value = float(11.042695478689712)
        self.instance.press_qnh = test_value
        self.assertEqual(self.instance.press_qnh, test_value)
    
    def test_press_msl_property(self):
        """
        Test press_msl property
        """
        test_value = float(24.732484525716913)
        self.instance.press_msl = test_value
        self.assertEqual(self.instance.press_msl, test_value)
    
    def test_press_tend_property(self):
        """
        Test press_tend property
        """
        test_value = 'mpsmhpltfnztiifytfau'
        self.instance.press_tend = test_value
        self.assertEqual(self.instance.press_tend, test_value)
    
    def test_rain_trace_property(self):
        """
        Test rain_trace property
        """
        test_value = 'vpcyjeicoakhztdlvnuu'
        self.instance.rain_trace = test_value
        self.assertEqual(self.instance.rain_trace, test_value)
    
    def test_cloud_property(self):
        """
        Test cloud property
        """
        test_value = 'hezokzrsvjknxfmkmkei'
        self.instance.cloud = test_value
        self.assertEqual(self.instance.cloud, test_value)
    
    def test_cloud_oktas_property(self):
        """
        Test cloud_oktas property
        """
        test_value = int(15)
        self.instance.cloud_oktas = test_value
        self.assertEqual(self.instance.cloud_oktas, test_value)
    
    def test_cloud_base_m_property(self):
        """
        Test cloud_base_m property
        """
        test_value = int(50)
        self.instance.cloud_base_m = test_value
        self.assertEqual(self.instance.cloud_base_m, test_value)
    
    def test_cloud_type_property(self):
        """
        Test cloud_type property
        """
        test_value = 'anearsotwyujjpihetsj'
        self.instance.cloud_type = test_value
        self.assertEqual(self.instance.cloud_type, test_value)
    
    def test_vis_km_property(self):
        """
        Test vis_km property
        """
        test_value = 'cyxaeihzblcewmjwzbvd'
        self.instance.vis_km = test_value
        self.assertEqual(self.instance.vis_km, test_value)
    
    def test_weather_property(self):
        """
        Test weather property
        """
        test_value = 'ksjvmrfhnfgcfoguhell'
        self.instance.weather = test_value
        self.assertEqual(self.instance.weather, test_value)
    
    def test_sea_state_property(self):
        """
        Test sea_state property
        """
        test_value = 'gfqhcmzbjiyqhejkymmq'
        self.instance.sea_state = test_value
        self.assertEqual(self.instance.sea_state, test_value)
    
    def test_swell_dir_worded_property(self):
        """
        Test swell_dir_worded property
        """
        test_value = 'njaptytxmztlttngfohz'
        self.instance.swell_dir_worded = test_value
        self.assertEqual(self.instance.swell_dir_worded, test_value)
    
    def test_swell_height_property(self):
        """
        Test swell_height property
        """
        test_value = float(93.33219979245716)
        self.instance.swell_height = test_value
        self.assertEqual(self.instance.swell_height, test_value)
    
    def test_swell_period_property(self):
        """
        Test swell_period property
        """
        test_value = float(17.497465836248715)
        self.instance.swell_period = test_value
        self.assertEqual(self.instance.swell_period, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(34.49555367936888)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(6.997588140317501)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'mjtzquauwjtjrlqgyxzz'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = WeatherObservation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = WeatherObservation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

