"""
Test case for Observation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_amedas_mqtt_producer_data.jp.jma.amedas.observation import Observation
from jma_bosai_amedas_mqtt_producer_data.jp.jma.amedas.observationeventenum import ObservationEventEnum
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
            station_code='pnpilvwzscmcgucjnltb',
            observed_at=datetime.datetime.now(datetime.timezone.utc),
            observed_at_local=datetime.datetime.now(datetime.timezone.utc),
            temp=float(72.94007097121123),
            temp_qc_flag=int(79),
            humidity=float(42.429992224333624),
            humidity_qc_flag=int(93),
            pressure=float(86.5005665426254),
            pressure_qc_flag=int(78),
            normal_pressure=float(10.387333359576212),
            normal_pressure_qc_flag=int(16),
            wind_speed=float(20.325938782375786),
            wind_speed_qc_flag=int(59),
            wind_direction=float(23.157858750016167),
            wind_direction_qc_flag=int(72),
            wind_gust=float(44.2675290295839),
            wind_gust_qc_flag=int(39),
            wind_gust_direction=float(29.13984920377638),
            wind_gust_time=datetime.datetime.now(datetime.timezone.utc),
            max_temp=float(59.95056305027473),
            max_temp_time=datetime.datetime.now(datetime.timezone.utc),
            min_temp=float(40.7105204109899),
            min_temp_time=datetime.datetime.now(datetime.timezone.utc),
            precipitation10m=float(20.99366644872508),
            precipitation10m_qc_flag=int(9),
            precipitation1h=float(48.230212405449166),
            precipitation1h_qc_flag=int(71),
            precipitation3h=float(68.48379092250451),
            precipitation3h_qc_flag=int(89),
            precipitation24h=float(3.5769612474544576),
            precipitation24h_qc_flag=int(74),
            sun10m=float(54.78494803095624),
            sun10m_qc_flag=int(2),
            sun1h=float(47.23251303057127),
            sun1h_qc_flag=int(90),
            snow=float(31.166832585464753),
            snow_qc_flag=int(53),
            snow1h=float(88.7853700605655),
            snow1h_qc_flag=int(3),
            snow6h=float(25.78214991128047),
            snow6h_qc_flag=int(74),
            snow12h=float(39.261696099335666),
            snow12h_qc_flag=int(20),
            snow24h=float(89.66684539957838),
            snow24h_qc_flag=int(0),
            visibility=float(38.440824772294576),
            visibility_qc_flag=int(98),
            cloud=float(3.1951278363943514),
            cloud_qc_flag=int(17),
            weather=float(83.32854609529839),
            weather_qc_flag=int(20),
            prefecture='gmwiealcwurspwczbrno',
            event=ObservationEventEnum.observation
        )
        return instance

    
    def test_station_code_property(self):
        """
        Test station_code property
        """
        test_value = 'pnpilvwzscmcgucjnltb'
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
        test_value = float(72.94007097121123)
        self.instance.temp = test_value
        self.assertEqual(self.instance.temp, test_value)
    
    def test_temp_qc_flag_property(self):
        """
        Test temp_qc_flag property
        """
        test_value = int(79)
        self.instance.temp_qc_flag = test_value
        self.assertEqual(self.instance.temp_qc_flag, test_value)
    
    def test_humidity_property(self):
        """
        Test humidity property
        """
        test_value = float(42.429992224333624)
        self.instance.humidity = test_value
        self.assertEqual(self.instance.humidity, test_value)
    
    def test_humidity_qc_flag_property(self):
        """
        Test humidity_qc_flag property
        """
        test_value = int(93)
        self.instance.humidity_qc_flag = test_value
        self.assertEqual(self.instance.humidity_qc_flag, test_value)
    
    def test_pressure_property(self):
        """
        Test pressure property
        """
        test_value = float(86.5005665426254)
        self.instance.pressure = test_value
        self.assertEqual(self.instance.pressure, test_value)
    
    def test_pressure_qc_flag_property(self):
        """
        Test pressure_qc_flag property
        """
        test_value = int(78)
        self.instance.pressure_qc_flag = test_value
        self.assertEqual(self.instance.pressure_qc_flag, test_value)
    
    def test_normal_pressure_property(self):
        """
        Test normal_pressure property
        """
        test_value = float(10.387333359576212)
        self.instance.normal_pressure = test_value
        self.assertEqual(self.instance.normal_pressure, test_value)
    
    def test_normal_pressure_qc_flag_property(self):
        """
        Test normal_pressure_qc_flag property
        """
        test_value = int(16)
        self.instance.normal_pressure_qc_flag = test_value
        self.assertEqual(self.instance.normal_pressure_qc_flag, test_value)
    
    def test_wind_speed_property(self):
        """
        Test wind_speed property
        """
        test_value = float(20.325938782375786)
        self.instance.wind_speed = test_value
        self.assertEqual(self.instance.wind_speed, test_value)
    
    def test_wind_speed_qc_flag_property(self):
        """
        Test wind_speed_qc_flag property
        """
        test_value = int(59)
        self.instance.wind_speed_qc_flag = test_value
        self.assertEqual(self.instance.wind_speed_qc_flag, test_value)
    
    def test_wind_direction_property(self):
        """
        Test wind_direction property
        """
        test_value = float(23.157858750016167)
        self.instance.wind_direction = test_value
        self.assertEqual(self.instance.wind_direction, test_value)
    
    def test_wind_direction_qc_flag_property(self):
        """
        Test wind_direction_qc_flag property
        """
        test_value = int(72)
        self.instance.wind_direction_qc_flag = test_value
        self.assertEqual(self.instance.wind_direction_qc_flag, test_value)
    
    def test_wind_gust_property(self):
        """
        Test wind_gust property
        """
        test_value = float(44.2675290295839)
        self.instance.wind_gust = test_value
        self.assertEqual(self.instance.wind_gust, test_value)
    
    def test_wind_gust_qc_flag_property(self):
        """
        Test wind_gust_qc_flag property
        """
        test_value = int(39)
        self.instance.wind_gust_qc_flag = test_value
        self.assertEqual(self.instance.wind_gust_qc_flag, test_value)
    
    def test_wind_gust_direction_property(self):
        """
        Test wind_gust_direction property
        """
        test_value = float(29.13984920377638)
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
        test_value = float(59.95056305027473)
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
        test_value = float(40.7105204109899)
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
        test_value = float(20.99366644872508)
        self.instance.precipitation10m = test_value
        self.assertEqual(self.instance.precipitation10m, test_value)
    
    def test_precipitation10m_qc_flag_property(self):
        """
        Test precipitation10m_qc_flag property
        """
        test_value = int(9)
        self.instance.precipitation10m_qc_flag = test_value
        self.assertEqual(self.instance.precipitation10m_qc_flag, test_value)
    
    def test_precipitation1h_property(self):
        """
        Test precipitation1h property
        """
        test_value = float(48.230212405449166)
        self.instance.precipitation1h = test_value
        self.assertEqual(self.instance.precipitation1h, test_value)
    
    def test_precipitation1h_qc_flag_property(self):
        """
        Test precipitation1h_qc_flag property
        """
        test_value = int(71)
        self.instance.precipitation1h_qc_flag = test_value
        self.assertEqual(self.instance.precipitation1h_qc_flag, test_value)
    
    def test_precipitation3h_property(self):
        """
        Test precipitation3h property
        """
        test_value = float(68.48379092250451)
        self.instance.precipitation3h = test_value
        self.assertEqual(self.instance.precipitation3h, test_value)
    
    def test_precipitation3h_qc_flag_property(self):
        """
        Test precipitation3h_qc_flag property
        """
        test_value = int(89)
        self.instance.precipitation3h_qc_flag = test_value
        self.assertEqual(self.instance.precipitation3h_qc_flag, test_value)
    
    def test_precipitation24h_property(self):
        """
        Test precipitation24h property
        """
        test_value = float(3.5769612474544576)
        self.instance.precipitation24h = test_value
        self.assertEqual(self.instance.precipitation24h, test_value)
    
    def test_precipitation24h_qc_flag_property(self):
        """
        Test precipitation24h_qc_flag property
        """
        test_value = int(74)
        self.instance.precipitation24h_qc_flag = test_value
        self.assertEqual(self.instance.precipitation24h_qc_flag, test_value)
    
    def test_sun10m_property(self):
        """
        Test sun10m property
        """
        test_value = float(54.78494803095624)
        self.instance.sun10m = test_value
        self.assertEqual(self.instance.sun10m, test_value)
    
    def test_sun10m_qc_flag_property(self):
        """
        Test sun10m_qc_flag property
        """
        test_value = int(2)
        self.instance.sun10m_qc_flag = test_value
        self.assertEqual(self.instance.sun10m_qc_flag, test_value)
    
    def test_sun1h_property(self):
        """
        Test sun1h property
        """
        test_value = float(47.23251303057127)
        self.instance.sun1h = test_value
        self.assertEqual(self.instance.sun1h, test_value)
    
    def test_sun1h_qc_flag_property(self):
        """
        Test sun1h_qc_flag property
        """
        test_value = int(90)
        self.instance.sun1h_qc_flag = test_value
        self.assertEqual(self.instance.sun1h_qc_flag, test_value)
    
    def test_snow_property(self):
        """
        Test snow property
        """
        test_value = float(31.166832585464753)
        self.instance.snow = test_value
        self.assertEqual(self.instance.snow, test_value)
    
    def test_snow_qc_flag_property(self):
        """
        Test snow_qc_flag property
        """
        test_value = int(53)
        self.instance.snow_qc_flag = test_value
        self.assertEqual(self.instance.snow_qc_flag, test_value)
    
    def test_snow1h_property(self):
        """
        Test snow1h property
        """
        test_value = float(88.7853700605655)
        self.instance.snow1h = test_value
        self.assertEqual(self.instance.snow1h, test_value)
    
    def test_snow1h_qc_flag_property(self):
        """
        Test snow1h_qc_flag property
        """
        test_value = int(3)
        self.instance.snow1h_qc_flag = test_value
        self.assertEqual(self.instance.snow1h_qc_flag, test_value)
    
    def test_snow6h_property(self):
        """
        Test snow6h property
        """
        test_value = float(25.78214991128047)
        self.instance.snow6h = test_value
        self.assertEqual(self.instance.snow6h, test_value)
    
    def test_snow6h_qc_flag_property(self):
        """
        Test snow6h_qc_flag property
        """
        test_value = int(74)
        self.instance.snow6h_qc_flag = test_value
        self.assertEqual(self.instance.snow6h_qc_flag, test_value)
    
    def test_snow12h_property(self):
        """
        Test snow12h property
        """
        test_value = float(39.261696099335666)
        self.instance.snow12h = test_value
        self.assertEqual(self.instance.snow12h, test_value)
    
    def test_snow12h_qc_flag_property(self):
        """
        Test snow12h_qc_flag property
        """
        test_value = int(20)
        self.instance.snow12h_qc_flag = test_value
        self.assertEqual(self.instance.snow12h_qc_flag, test_value)
    
    def test_snow24h_property(self):
        """
        Test snow24h property
        """
        test_value = float(89.66684539957838)
        self.instance.snow24h = test_value
        self.assertEqual(self.instance.snow24h, test_value)
    
    def test_snow24h_qc_flag_property(self):
        """
        Test snow24h_qc_flag property
        """
        test_value = int(0)
        self.instance.snow24h_qc_flag = test_value
        self.assertEqual(self.instance.snow24h_qc_flag, test_value)
    
    def test_visibility_property(self):
        """
        Test visibility property
        """
        test_value = float(38.440824772294576)
        self.instance.visibility = test_value
        self.assertEqual(self.instance.visibility, test_value)
    
    def test_visibility_qc_flag_property(self):
        """
        Test visibility_qc_flag property
        """
        test_value = int(98)
        self.instance.visibility_qc_flag = test_value
        self.assertEqual(self.instance.visibility_qc_flag, test_value)
    
    def test_cloud_property(self):
        """
        Test cloud property
        """
        test_value = float(3.1951278363943514)
        self.instance.cloud = test_value
        self.assertEqual(self.instance.cloud, test_value)
    
    def test_cloud_qc_flag_property(self):
        """
        Test cloud_qc_flag property
        """
        test_value = int(17)
        self.instance.cloud_qc_flag = test_value
        self.assertEqual(self.instance.cloud_qc_flag, test_value)
    
    def test_weather_property(self):
        """
        Test weather property
        """
        test_value = float(83.32854609529839)
        self.instance.weather = test_value
        self.assertEqual(self.instance.weather, test_value)
    
    def test_weather_qc_flag_property(self):
        """
        Test weather_qc_flag property
        """
        test_value = int(20)
        self.instance.weather_qc_flag = test_value
        self.assertEqual(self.instance.weather_qc_flag, test_value)
    
    def test_prefecture_property(self):
        """
        Test prefecture property
        """
        test_value = 'gmwiealcwurspwczbrno'
        self.instance.prefecture = test_value
        self.assertEqual(self.instance.prefecture, test_value)
    
    def test_event_property(self):
        """
        Test event property
        """
        test_value = ObservationEventEnum.observation
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

