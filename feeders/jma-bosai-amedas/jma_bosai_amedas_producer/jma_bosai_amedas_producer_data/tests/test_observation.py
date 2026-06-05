"""
Test case for Observation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_amedas_producer_data.jp.jma.amedas.observation import Observation
from jma_bosai_amedas_producer_data.jp.jma.amedas.eventenum import EventEnum
import datetime


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
            station_code='lecxvpuyijcsfctacuny',
            observed_at=datetime.datetime.now(datetime.timezone.utc),
            observed_at_local=datetime.datetime.now(datetime.timezone.utc),
            temp=float(82.25193807367188),
            temp_qc_flag=int(40),
            humidity=float(42.76522887763814),
            humidity_qc_flag=int(69),
            pressure=float(10.826512017666868),
            pressure_qc_flag=int(80),
            normal_pressure=float(45.25552899093764),
            normal_pressure_qc_flag=int(98),
            wind_speed=float(33.30469356193283),
            wind_speed_qc_flag=int(76),
            wind_direction=float(46.431501342095935),
            wind_direction_qc_flag=int(92),
            wind_gust=float(33.897136855973244),
            wind_gust_qc_flag=int(5),
            wind_gust_direction=float(96.8982522610014),
            wind_gust_time=datetime.datetime.now(datetime.timezone.utc),
            max_temp=float(61.09112203363889),
            max_temp_time=datetime.datetime.now(datetime.timezone.utc),
            min_temp=float(19.221558702260545),
            min_temp_time=datetime.datetime.now(datetime.timezone.utc),
            precipitation10m=float(23.853894971816036),
            precipitation10m_qc_flag=int(90),
            precipitation1h=float(89.8844809297176),
            precipitation1h_qc_flag=int(57),
            precipitation3h=float(93.55827320510761),
            precipitation3h_qc_flag=int(93),
            precipitation24h=float(55.35023160683639),
            precipitation24h_qc_flag=int(85),
            sun10m=float(41.3851501128827),
            sun10m_qc_flag=int(23),
            sun1h=float(41.10379610089604),
            sun1h_qc_flag=int(96),
            snow=float(9.023560979597633),
            snow_qc_flag=int(83),
            snow1h=float(75.08675838639306),
            snow1h_qc_flag=int(1),
            snow6h=float(66.83520034142349),
            snow6h_qc_flag=int(75),
            snow12h=float(62.84775588734585),
            snow12h_qc_flag=int(19),
            snow24h=float(81.15040621847662),
            snow24h_qc_flag=int(83),
            visibility=float(90.5746697156236),
            visibility_qc_flag=int(60),
            cloud=float(21.975560705736974),
            cloud_qc_flag=int(86),
            weather=float(55.43224019747974),
            weather_qc_flag=int(88),
            prefecture='zwtnkoqodbxkixkwdyip',
            event=EventEnum.observation
        )
        return instance

    
    def test_station_code_property(self):
        """
        Test station_code property
        """
        test_value = 'lecxvpuyijcsfctacuny'
        self.instance.station_code = test_value
        self.assertEqual(self.instance.station_code, test_value)
    
    def test_observed_at_property(self):
        """
        Test observed_at property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.observed_at = test_value
        self.assertEqual(self.instance.observed_at, test_value)
    
    def test_observed_at_local_property(self):
        """
        Test observed_at_local property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.observed_at_local = test_value
        self.assertEqual(self.instance.observed_at_local, test_value)
    
    def test_temp_property(self):
        """
        Test temp property
        """
        test_value = float(82.25193807367188)
        self.instance.temp = test_value
        self.assertEqual(self.instance.temp, test_value)
    
    def test_temp_qc_flag_property(self):
        """
        Test temp_qc_flag property
        """
        test_value = int(40)
        self.instance.temp_qc_flag = test_value
        self.assertEqual(self.instance.temp_qc_flag, test_value)
    
    def test_humidity_property(self):
        """
        Test humidity property
        """
        test_value = float(42.76522887763814)
        self.instance.humidity = test_value
        self.assertEqual(self.instance.humidity, test_value)
    
    def test_humidity_qc_flag_property(self):
        """
        Test humidity_qc_flag property
        """
        test_value = int(69)
        self.instance.humidity_qc_flag = test_value
        self.assertEqual(self.instance.humidity_qc_flag, test_value)
    
    def test_pressure_property(self):
        """
        Test pressure property
        """
        test_value = float(10.826512017666868)
        self.instance.pressure = test_value
        self.assertEqual(self.instance.pressure, test_value)
    
    def test_pressure_qc_flag_property(self):
        """
        Test pressure_qc_flag property
        """
        test_value = int(80)
        self.instance.pressure_qc_flag = test_value
        self.assertEqual(self.instance.pressure_qc_flag, test_value)
    
    def test_normal_pressure_property(self):
        """
        Test normal_pressure property
        """
        test_value = float(45.25552899093764)
        self.instance.normal_pressure = test_value
        self.assertEqual(self.instance.normal_pressure, test_value)
    
    def test_normal_pressure_qc_flag_property(self):
        """
        Test normal_pressure_qc_flag property
        """
        test_value = int(98)
        self.instance.normal_pressure_qc_flag = test_value
        self.assertEqual(self.instance.normal_pressure_qc_flag, test_value)
    
    def test_wind_speed_property(self):
        """
        Test wind_speed property
        """
        test_value = float(33.30469356193283)
        self.instance.wind_speed = test_value
        self.assertEqual(self.instance.wind_speed, test_value)
    
    def test_wind_speed_qc_flag_property(self):
        """
        Test wind_speed_qc_flag property
        """
        test_value = int(76)
        self.instance.wind_speed_qc_flag = test_value
        self.assertEqual(self.instance.wind_speed_qc_flag, test_value)
    
    def test_wind_direction_property(self):
        """
        Test wind_direction property
        """
        test_value = float(46.431501342095935)
        self.instance.wind_direction = test_value
        self.assertEqual(self.instance.wind_direction, test_value)
    
    def test_wind_direction_qc_flag_property(self):
        """
        Test wind_direction_qc_flag property
        """
        test_value = int(92)
        self.instance.wind_direction_qc_flag = test_value
        self.assertEqual(self.instance.wind_direction_qc_flag, test_value)
    
    def test_wind_gust_property(self):
        """
        Test wind_gust property
        """
        test_value = float(33.897136855973244)
        self.instance.wind_gust = test_value
        self.assertEqual(self.instance.wind_gust, test_value)
    
    def test_wind_gust_qc_flag_property(self):
        """
        Test wind_gust_qc_flag property
        """
        test_value = int(5)
        self.instance.wind_gust_qc_flag = test_value
        self.assertEqual(self.instance.wind_gust_qc_flag, test_value)
    
    def test_wind_gust_direction_property(self):
        """
        Test wind_gust_direction property
        """
        test_value = float(96.8982522610014)
        self.instance.wind_gust_direction = test_value
        self.assertEqual(self.instance.wind_gust_direction, test_value)
    
    def test_wind_gust_time_property(self):
        """
        Test wind_gust_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.wind_gust_time = test_value
        self.assertEqual(self.instance.wind_gust_time, test_value)
    
    def test_max_temp_property(self):
        """
        Test max_temp property
        """
        test_value = float(61.09112203363889)
        self.instance.max_temp = test_value
        self.assertEqual(self.instance.max_temp, test_value)
    
    def test_max_temp_time_property(self):
        """
        Test max_temp_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.max_temp_time = test_value
        self.assertEqual(self.instance.max_temp_time, test_value)
    
    def test_min_temp_property(self):
        """
        Test min_temp property
        """
        test_value = float(19.221558702260545)
        self.instance.min_temp = test_value
        self.assertEqual(self.instance.min_temp, test_value)
    
    def test_min_temp_time_property(self):
        """
        Test min_temp_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.min_temp_time = test_value
        self.assertEqual(self.instance.min_temp_time, test_value)
    
    def test_precipitation10m_property(self):
        """
        Test precipitation10m property
        """
        test_value = float(23.853894971816036)
        self.instance.precipitation10m = test_value
        self.assertEqual(self.instance.precipitation10m, test_value)
    
    def test_precipitation10m_qc_flag_property(self):
        """
        Test precipitation10m_qc_flag property
        """
        test_value = int(90)
        self.instance.precipitation10m_qc_flag = test_value
        self.assertEqual(self.instance.precipitation10m_qc_flag, test_value)
    
    def test_precipitation1h_property(self):
        """
        Test precipitation1h property
        """
        test_value = float(89.8844809297176)
        self.instance.precipitation1h = test_value
        self.assertEqual(self.instance.precipitation1h, test_value)
    
    def test_precipitation1h_qc_flag_property(self):
        """
        Test precipitation1h_qc_flag property
        """
        test_value = int(57)
        self.instance.precipitation1h_qc_flag = test_value
        self.assertEqual(self.instance.precipitation1h_qc_flag, test_value)
    
    def test_precipitation3h_property(self):
        """
        Test precipitation3h property
        """
        test_value = float(93.55827320510761)
        self.instance.precipitation3h = test_value
        self.assertEqual(self.instance.precipitation3h, test_value)
    
    def test_precipitation3h_qc_flag_property(self):
        """
        Test precipitation3h_qc_flag property
        """
        test_value = int(93)
        self.instance.precipitation3h_qc_flag = test_value
        self.assertEqual(self.instance.precipitation3h_qc_flag, test_value)
    
    def test_precipitation24h_property(self):
        """
        Test precipitation24h property
        """
        test_value = float(55.35023160683639)
        self.instance.precipitation24h = test_value
        self.assertEqual(self.instance.precipitation24h, test_value)
    
    def test_precipitation24h_qc_flag_property(self):
        """
        Test precipitation24h_qc_flag property
        """
        test_value = int(85)
        self.instance.precipitation24h_qc_flag = test_value
        self.assertEqual(self.instance.precipitation24h_qc_flag, test_value)
    
    def test_sun10m_property(self):
        """
        Test sun10m property
        """
        test_value = float(41.3851501128827)
        self.instance.sun10m = test_value
        self.assertEqual(self.instance.sun10m, test_value)
    
    def test_sun10m_qc_flag_property(self):
        """
        Test sun10m_qc_flag property
        """
        test_value = int(23)
        self.instance.sun10m_qc_flag = test_value
        self.assertEqual(self.instance.sun10m_qc_flag, test_value)
    
    def test_sun1h_property(self):
        """
        Test sun1h property
        """
        test_value = float(41.10379610089604)
        self.instance.sun1h = test_value
        self.assertEqual(self.instance.sun1h, test_value)
    
    def test_sun1h_qc_flag_property(self):
        """
        Test sun1h_qc_flag property
        """
        test_value = int(96)
        self.instance.sun1h_qc_flag = test_value
        self.assertEqual(self.instance.sun1h_qc_flag, test_value)
    
    def test_snow_property(self):
        """
        Test snow property
        """
        test_value = float(9.023560979597633)
        self.instance.snow = test_value
        self.assertEqual(self.instance.snow, test_value)
    
    def test_snow_qc_flag_property(self):
        """
        Test snow_qc_flag property
        """
        test_value = int(83)
        self.instance.snow_qc_flag = test_value
        self.assertEqual(self.instance.snow_qc_flag, test_value)
    
    def test_snow1h_property(self):
        """
        Test snow1h property
        """
        test_value = float(75.08675838639306)
        self.instance.snow1h = test_value
        self.assertEqual(self.instance.snow1h, test_value)
    
    def test_snow1h_qc_flag_property(self):
        """
        Test snow1h_qc_flag property
        """
        test_value = int(1)
        self.instance.snow1h_qc_flag = test_value
        self.assertEqual(self.instance.snow1h_qc_flag, test_value)
    
    def test_snow6h_property(self):
        """
        Test snow6h property
        """
        test_value = float(66.83520034142349)
        self.instance.snow6h = test_value
        self.assertEqual(self.instance.snow6h, test_value)
    
    def test_snow6h_qc_flag_property(self):
        """
        Test snow6h_qc_flag property
        """
        test_value = int(75)
        self.instance.snow6h_qc_flag = test_value
        self.assertEqual(self.instance.snow6h_qc_flag, test_value)
    
    def test_snow12h_property(self):
        """
        Test snow12h property
        """
        test_value = float(62.84775588734585)
        self.instance.snow12h = test_value
        self.assertEqual(self.instance.snow12h, test_value)
    
    def test_snow12h_qc_flag_property(self):
        """
        Test snow12h_qc_flag property
        """
        test_value = int(19)
        self.instance.snow12h_qc_flag = test_value
        self.assertEqual(self.instance.snow12h_qc_flag, test_value)
    
    def test_snow24h_property(self):
        """
        Test snow24h property
        """
        test_value = float(81.15040621847662)
        self.instance.snow24h = test_value
        self.assertEqual(self.instance.snow24h, test_value)
    
    def test_snow24h_qc_flag_property(self):
        """
        Test snow24h_qc_flag property
        """
        test_value = int(83)
        self.instance.snow24h_qc_flag = test_value
        self.assertEqual(self.instance.snow24h_qc_flag, test_value)
    
    def test_visibility_property(self):
        """
        Test visibility property
        """
        test_value = float(90.5746697156236)
        self.instance.visibility = test_value
        self.assertEqual(self.instance.visibility, test_value)
    
    def test_visibility_qc_flag_property(self):
        """
        Test visibility_qc_flag property
        """
        test_value = int(60)
        self.instance.visibility_qc_flag = test_value
        self.assertEqual(self.instance.visibility_qc_flag, test_value)
    
    def test_cloud_property(self):
        """
        Test cloud property
        """
        test_value = float(21.975560705736974)
        self.instance.cloud = test_value
        self.assertEqual(self.instance.cloud, test_value)
    
    def test_cloud_qc_flag_property(self):
        """
        Test cloud_qc_flag property
        """
        test_value = int(86)
        self.instance.cloud_qc_flag = test_value
        self.assertEqual(self.instance.cloud_qc_flag, test_value)
    
    def test_weather_property(self):
        """
        Test weather property
        """
        test_value = float(55.43224019747974)
        self.instance.weather = test_value
        self.assertEqual(self.instance.weather, test_value)
    
    def test_weather_qc_flag_property(self):
        """
        Test weather_qc_flag property
        """
        test_value = int(88)
        self.instance.weather_qc_flag = test_value
        self.assertEqual(self.instance.weather_qc_flag, test_value)
    
    def test_prefecture_property(self):
        """
        Test prefecture property
        """
        test_value = 'zwtnkoqodbxkixkwdyip'
        self.instance.prefecture = test_value
        self.assertEqual(self.instance.prefecture, test_value)
    
    def test_event_property(self):
        """
        Test event property
        """
        test_value = EventEnum.observation
        self.instance.event = test_value
        self.assertEqual(self.instance.event, test_value)
    
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

