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
            station_wmo='mhrrgdiseqmzbxgavpzi',
            station_name='jdcusxlkecqglbdkbhqg',
            observation_time_utc=datetime.datetime.now(datetime.timezone.utc),
            local_time='wtjpaiptxigxdaztbacu',
            air_temp=float(3.302438610299152),
            apparent_temp=float(28.4281566018285),
            dewpt=float(59.48100824954638),
            rel_hum=int(67),
            delta_t=float(48.067339115556784),
            wind_dir='ljepsmfslflhjzdxvsww',
            wind_spd_kmh=int(95),
            wind_spd_kt=int(15),
            gust_kmh=int(1),
            gust_kt=int(20),
            press=float(80.93831537436863),
            press_qnh=float(30.747334980999387),
            press_msl=float(65.02687297452458),
            press_tend='vnhxmpeuruukuceszhov',
            rain_trace='pabdohljtnxfxvutovnz',
            cloud='exmodtyrstoefzpcbpnv',
            cloud_oktas=int(59),
            cloud_base_m=int(6),
            cloud_type='rogelldkvwdjrnmoagfb',
            vis_km='jtcdqxylqnrgzapaanmq',
            weather='jfzozgalmhvzeljmlrmg',
            sea_state='varvxqeqwvpqftuimurk',
            swell_dir_worded='jiewazydlulayvvxmlwr',
            swell_height=float(15.129297413095866),
            swell_period=float(10.63430890249526),
            latitude=float(41.459350697646855),
            longitude=float(18.263123638929724),
            state='doadezhkqzehxaggrdpu'
        )
        return instance

    
    def test_station_wmo_property(self):
        """
        Test station_wmo property
        """
        test_value = 'mhrrgdiseqmzbxgavpzi'
        self.instance.station_wmo = test_value
        self.assertEqual(self.instance.station_wmo, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'jdcusxlkecqglbdkbhqg'
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
        test_value = 'wtjpaiptxigxdaztbacu'
        self.instance.local_time = test_value
        self.assertEqual(self.instance.local_time, test_value)
    
    def test_air_temp_property(self):
        """
        Test air_temp property
        """
        test_value = float(3.302438610299152)
        self.instance.air_temp = test_value
        self.assertEqual(self.instance.air_temp, test_value)
    
    def test_apparent_temp_property(self):
        """
        Test apparent_temp property
        """
        test_value = float(28.4281566018285)
        self.instance.apparent_temp = test_value
        self.assertEqual(self.instance.apparent_temp, test_value)
    
    def test_dewpt_property(self):
        """
        Test dewpt property
        """
        test_value = float(59.48100824954638)
        self.instance.dewpt = test_value
        self.assertEqual(self.instance.dewpt, test_value)
    
    def test_rel_hum_property(self):
        """
        Test rel_hum property
        """
        test_value = int(67)
        self.instance.rel_hum = test_value
        self.assertEqual(self.instance.rel_hum, test_value)
    
    def test_delta_t_property(self):
        """
        Test delta_t property
        """
        test_value = float(48.067339115556784)
        self.instance.delta_t = test_value
        self.assertEqual(self.instance.delta_t, test_value)
    
    def test_wind_dir_property(self):
        """
        Test wind_dir property
        """
        test_value = 'ljepsmfslflhjzdxvsww'
        self.instance.wind_dir = test_value
        self.assertEqual(self.instance.wind_dir, test_value)
    
    def test_wind_spd_kmh_property(self):
        """
        Test wind_spd_kmh property
        """
        test_value = int(95)
        self.instance.wind_spd_kmh = test_value
        self.assertEqual(self.instance.wind_spd_kmh, test_value)
    
    def test_wind_spd_kt_property(self):
        """
        Test wind_spd_kt property
        """
        test_value = int(15)
        self.instance.wind_spd_kt = test_value
        self.assertEqual(self.instance.wind_spd_kt, test_value)
    
    def test_gust_kmh_property(self):
        """
        Test gust_kmh property
        """
        test_value = int(1)
        self.instance.gust_kmh = test_value
        self.assertEqual(self.instance.gust_kmh, test_value)
    
    def test_gust_kt_property(self):
        """
        Test gust_kt property
        """
        test_value = int(20)
        self.instance.gust_kt = test_value
        self.assertEqual(self.instance.gust_kt, test_value)
    
    def test_press_property(self):
        """
        Test press property
        """
        test_value = float(80.93831537436863)
        self.instance.press = test_value
        self.assertEqual(self.instance.press, test_value)
    
    def test_press_qnh_property(self):
        """
        Test press_qnh property
        """
        test_value = float(30.747334980999387)
        self.instance.press_qnh = test_value
        self.assertEqual(self.instance.press_qnh, test_value)
    
    def test_press_msl_property(self):
        """
        Test press_msl property
        """
        test_value = float(65.02687297452458)
        self.instance.press_msl = test_value
        self.assertEqual(self.instance.press_msl, test_value)
    
    def test_press_tend_property(self):
        """
        Test press_tend property
        """
        test_value = 'vnhxmpeuruukuceszhov'
        self.instance.press_tend = test_value
        self.assertEqual(self.instance.press_tend, test_value)
    
    def test_rain_trace_property(self):
        """
        Test rain_trace property
        """
        test_value = 'pabdohljtnxfxvutovnz'
        self.instance.rain_trace = test_value
        self.assertEqual(self.instance.rain_trace, test_value)
    
    def test_cloud_property(self):
        """
        Test cloud property
        """
        test_value = 'exmodtyrstoefzpcbpnv'
        self.instance.cloud = test_value
        self.assertEqual(self.instance.cloud, test_value)
    
    def test_cloud_oktas_property(self):
        """
        Test cloud_oktas property
        """
        test_value = int(59)
        self.instance.cloud_oktas = test_value
        self.assertEqual(self.instance.cloud_oktas, test_value)
    
    def test_cloud_base_m_property(self):
        """
        Test cloud_base_m property
        """
        test_value = int(6)
        self.instance.cloud_base_m = test_value
        self.assertEqual(self.instance.cloud_base_m, test_value)
    
    def test_cloud_type_property(self):
        """
        Test cloud_type property
        """
        test_value = 'rogelldkvwdjrnmoagfb'
        self.instance.cloud_type = test_value
        self.assertEqual(self.instance.cloud_type, test_value)
    
    def test_vis_km_property(self):
        """
        Test vis_km property
        """
        test_value = 'jtcdqxylqnrgzapaanmq'
        self.instance.vis_km = test_value
        self.assertEqual(self.instance.vis_km, test_value)
    
    def test_weather_property(self):
        """
        Test weather property
        """
        test_value = 'jfzozgalmhvzeljmlrmg'
        self.instance.weather = test_value
        self.assertEqual(self.instance.weather, test_value)
    
    def test_sea_state_property(self):
        """
        Test sea_state property
        """
        test_value = 'varvxqeqwvpqftuimurk'
        self.instance.sea_state = test_value
        self.assertEqual(self.instance.sea_state, test_value)
    
    def test_swell_dir_worded_property(self):
        """
        Test swell_dir_worded property
        """
        test_value = 'jiewazydlulayvvxmlwr'
        self.instance.swell_dir_worded = test_value
        self.assertEqual(self.instance.swell_dir_worded, test_value)
    
    def test_swell_height_property(self):
        """
        Test swell_height property
        """
        test_value = float(15.129297413095866)
        self.instance.swell_height = test_value
        self.assertEqual(self.instance.swell_height, test_value)
    
    def test_swell_period_property(self):
        """
        Test swell_period property
        """
        test_value = float(10.63430890249526)
        self.instance.swell_period = test_value
        self.assertEqual(self.instance.swell_period, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(41.459350697646855)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(18.263123638929724)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'doadezhkqzehxaggrdpu'
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

