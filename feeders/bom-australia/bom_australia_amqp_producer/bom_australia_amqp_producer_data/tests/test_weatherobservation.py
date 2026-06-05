"""
Test case for WeatherObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from bom_australia_amqp_producer_data.weatherobservation import WeatherObservation
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
            station_wmo='njzleoayynnkxvtlfeyt',
            station_name='cxrleiurcackfqwobdtx',
            observation_time_utc=datetime.datetime.now(datetime.timezone.utc),
            local_time='cserczqrxybkwmdoiiru',
            air_temp=float(58.84010423549365),
            apparent_temp=float(74.64671596399499),
            dewpt=float(33.883502387511356),
            rel_hum=int(77),
            delta_t=float(24.22186109501039),
            wind_dir='tvlgfyfwylwlohynsiyr',
            wind_spd_kmh=int(47),
            wind_spd_kt=int(64),
            gust_kmh=int(79),
            gust_kt=int(11),
            press=float(57.68537296196597),
            press_qnh=float(77.98430394971547),
            press_msl=float(73.92315699246753),
            press_tend='bevsphpmbkxfjusczerj',
            rain_trace='raigwkgzzserxoeookhc',
            cloud='uguibawcmoajwxvfsrrp',
            cloud_oktas=int(96),
            cloud_base_m=int(19),
            cloud_type='mzeucczsnzfypivpaezu',
            vis_km='nnaklffvsqujtleztwyc',
            weather='adnsppfhnsqydldjoyov',
            sea_state='zzrjgzlikgfhcoqqtyhu',
            swell_dir_worded='pyhiltkdoareifuiekzd',
            swell_height=float(63.390525884028634),
            swell_period=float(6.885650154512812),
            latitude=float(31.94135159383077),
            longitude=float(67.43045963121575),
            state='vuyviijrjznldldcenyu'
        )
        return instance

    
    def test_station_wmo_property(self):
        """
        Test station_wmo property
        """
        test_value = 'njzleoayynnkxvtlfeyt'
        self.instance.station_wmo = test_value
        self.assertEqual(self.instance.station_wmo, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'cxrleiurcackfqwobdtx'
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
        test_value = 'cserczqrxybkwmdoiiru'
        self.instance.local_time = test_value
        self.assertEqual(self.instance.local_time, test_value)
    
    def test_air_temp_property(self):
        """
        Test air_temp property
        """
        test_value = float(58.84010423549365)
        self.instance.air_temp = test_value
        self.assertEqual(self.instance.air_temp, test_value)
    
    def test_apparent_temp_property(self):
        """
        Test apparent_temp property
        """
        test_value = float(74.64671596399499)
        self.instance.apparent_temp = test_value
        self.assertEqual(self.instance.apparent_temp, test_value)
    
    def test_dewpt_property(self):
        """
        Test dewpt property
        """
        test_value = float(33.883502387511356)
        self.instance.dewpt = test_value
        self.assertEqual(self.instance.dewpt, test_value)
    
    def test_rel_hum_property(self):
        """
        Test rel_hum property
        """
        test_value = int(77)
        self.instance.rel_hum = test_value
        self.assertEqual(self.instance.rel_hum, test_value)
    
    def test_delta_t_property(self):
        """
        Test delta_t property
        """
        test_value = float(24.22186109501039)
        self.instance.delta_t = test_value
        self.assertEqual(self.instance.delta_t, test_value)
    
    def test_wind_dir_property(self):
        """
        Test wind_dir property
        """
        test_value = 'tvlgfyfwylwlohynsiyr'
        self.instance.wind_dir = test_value
        self.assertEqual(self.instance.wind_dir, test_value)
    
    def test_wind_spd_kmh_property(self):
        """
        Test wind_spd_kmh property
        """
        test_value = int(47)
        self.instance.wind_spd_kmh = test_value
        self.assertEqual(self.instance.wind_spd_kmh, test_value)
    
    def test_wind_spd_kt_property(self):
        """
        Test wind_spd_kt property
        """
        test_value = int(64)
        self.instance.wind_spd_kt = test_value
        self.assertEqual(self.instance.wind_spd_kt, test_value)
    
    def test_gust_kmh_property(self):
        """
        Test gust_kmh property
        """
        test_value = int(79)
        self.instance.gust_kmh = test_value
        self.assertEqual(self.instance.gust_kmh, test_value)
    
    def test_gust_kt_property(self):
        """
        Test gust_kt property
        """
        test_value = int(11)
        self.instance.gust_kt = test_value
        self.assertEqual(self.instance.gust_kt, test_value)
    
    def test_press_property(self):
        """
        Test press property
        """
        test_value = float(57.68537296196597)
        self.instance.press = test_value
        self.assertEqual(self.instance.press, test_value)
    
    def test_press_qnh_property(self):
        """
        Test press_qnh property
        """
        test_value = float(77.98430394971547)
        self.instance.press_qnh = test_value
        self.assertEqual(self.instance.press_qnh, test_value)
    
    def test_press_msl_property(self):
        """
        Test press_msl property
        """
        test_value = float(73.92315699246753)
        self.instance.press_msl = test_value
        self.assertEqual(self.instance.press_msl, test_value)
    
    def test_press_tend_property(self):
        """
        Test press_tend property
        """
        test_value = 'bevsphpmbkxfjusczerj'
        self.instance.press_tend = test_value
        self.assertEqual(self.instance.press_tend, test_value)
    
    def test_rain_trace_property(self):
        """
        Test rain_trace property
        """
        test_value = 'raigwkgzzserxoeookhc'
        self.instance.rain_trace = test_value
        self.assertEqual(self.instance.rain_trace, test_value)
    
    def test_cloud_property(self):
        """
        Test cloud property
        """
        test_value = 'uguibawcmoajwxvfsrrp'
        self.instance.cloud = test_value
        self.assertEqual(self.instance.cloud, test_value)
    
    def test_cloud_oktas_property(self):
        """
        Test cloud_oktas property
        """
        test_value = int(96)
        self.instance.cloud_oktas = test_value
        self.assertEqual(self.instance.cloud_oktas, test_value)
    
    def test_cloud_base_m_property(self):
        """
        Test cloud_base_m property
        """
        test_value = int(19)
        self.instance.cloud_base_m = test_value
        self.assertEqual(self.instance.cloud_base_m, test_value)
    
    def test_cloud_type_property(self):
        """
        Test cloud_type property
        """
        test_value = 'mzeucczsnzfypivpaezu'
        self.instance.cloud_type = test_value
        self.assertEqual(self.instance.cloud_type, test_value)
    
    def test_vis_km_property(self):
        """
        Test vis_km property
        """
        test_value = 'nnaklffvsqujtleztwyc'
        self.instance.vis_km = test_value
        self.assertEqual(self.instance.vis_km, test_value)
    
    def test_weather_property(self):
        """
        Test weather property
        """
        test_value = 'adnsppfhnsqydldjoyov'
        self.instance.weather = test_value
        self.assertEqual(self.instance.weather, test_value)
    
    def test_sea_state_property(self):
        """
        Test sea_state property
        """
        test_value = 'zzrjgzlikgfhcoqqtyhu'
        self.instance.sea_state = test_value
        self.assertEqual(self.instance.sea_state, test_value)
    
    def test_swell_dir_worded_property(self):
        """
        Test swell_dir_worded property
        """
        test_value = 'pyhiltkdoareifuiekzd'
        self.instance.swell_dir_worded = test_value
        self.assertEqual(self.instance.swell_dir_worded, test_value)
    
    def test_swell_height_property(self):
        """
        Test swell_height property
        """
        test_value = float(63.390525884028634)
        self.instance.swell_height = test_value
        self.assertEqual(self.instance.swell_height, test_value)
    
    def test_swell_period_property(self):
        """
        Test swell_period property
        """
        test_value = float(6.885650154512812)
        self.instance.swell_period = test_value
        self.assertEqual(self.instance.swell_period, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(31.94135159383077)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(67.43045963121575)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'vuyviijrjznldldcenyu'
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

