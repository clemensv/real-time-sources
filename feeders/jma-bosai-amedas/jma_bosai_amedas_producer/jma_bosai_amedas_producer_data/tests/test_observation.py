"""
Test case for Observation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_amedas_producer_data.jp.jma.amedas.observation import Observation
from jma_bosai_amedas_producer_data.jp.jma.amedas.observationeventenum import ObservationEventEnum
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
            station_code='krozsehfyvcrpmsvocwl',
            observed_at=datetime.datetime.now(datetime.timezone.utc),
            observed_at_local=datetime.datetime.now(datetime.timezone.utc),
            temp=float(26.85499921476343),
            temp_qc_flag=int(38),
            humidity=float(73.62119047519151),
            humidity_qc_flag=int(8),
            pressure=float(94.6129054598148),
            pressure_qc_flag=int(96),
            normal_pressure=float(83.86494670484328),
            normal_pressure_qc_flag=int(47),
            wind_speed=float(67.1470566153106),
            wind_speed_qc_flag=int(40),
            wind_direction=float(42.495861734199714),
            wind_direction_qc_flag=int(54),
            wind_gust=float(66.6663611458625),
            wind_gust_qc_flag=int(56),
            wind_gust_direction=float(39.93986436875537),
            wind_gust_time=datetime.datetime.now(datetime.timezone.utc),
            max_temp=float(4.597604153411727),
            max_temp_time=datetime.datetime.now(datetime.timezone.utc),
            min_temp=float(84.47287052473624),
            min_temp_time=datetime.datetime.now(datetime.timezone.utc),
            precipitation10m=float(27.97937179260346),
            precipitation10m_qc_flag=int(71),
            precipitation1h=float(14.086164328660999),
            precipitation1h_qc_flag=int(59),
            precipitation3h=float(6.238482935078816),
            precipitation3h_qc_flag=int(77),
            precipitation24h=float(73.80837283347941),
            precipitation24h_qc_flag=int(59),
            sun10m=float(67.73277092874366),
            sun10m_qc_flag=int(58),
            sun1h=float(80.26102995327416),
            sun1h_qc_flag=int(5),
            snow=float(17.163040322929646),
            snow_qc_flag=int(2),
            snow1h=float(80.18284496472252),
            snow1h_qc_flag=int(79),
            snow6h=float(16.49387186870982),
            snow6h_qc_flag=int(97),
            snow12h=float(77.12537355105252),
            snow12h_qc_flag=int(53),
            snow24h=float(13.171597993286198),
            snow24h_qc_flag=int(43),
            visibility=float(92.21139753459897),
            visibility_qc_flag=int(52),
            cloud=float(16.4375189963879),
            cloud_qc_flag=int(69),
            weather=float(6.370101675984364),
            weather_qc_flag=int(61),
            prefecture='ilbgbordlyxeglhtldvr',
            event=ObservationEventEnum.observation
        )
        return instance

    
    def test_station_code_property(self):
        """
        Test station_code property
        """
        test_value = 'krozsehfyvcrpmsvocwl'
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
        test_value = float(26.85499921476343)
        self.instance.temp = test_value
        self.assertEqual(self.instance.temp, test_value)
    
    def test_temp_qc_flag_property(self):
        """
        Test temp_qc_flag property
        """
        test_value = int(38)
        self.instance.temp_qc_flag = test_value
        self.assertEqual(self.instance.temp_qc_flag, test_value)
    
    def test_humidity_property(self):
        """
        Test humidity property
        """
        test_value = float(73.62119047519151)
        self.instance.humidity = test_value
        self.assertEqual(self.instance.humidity, test_value)
    
    def test_humidity_qc_flag_property(self):
        """
        Test humidity_qc_flag property
        """
        test_value = int(8)
        self.instance.humidity_qc_flag = test_value
        self.assertEqual(self.instance.humidity_qc_flag, test_value)
    
    def test_pressure_property(self):
        """
        Test pressure property
        """
        test_value = float(94.6129054598148)
        self.instance.pressure = test_value
        self.assertEqual(self.instance.pressure, test_value)
    
    def test_pressure_qc_flag_property(self):
        """
        Test pressure_qc_flag property
        """
        test_value = int(96)
        self.instance.pressure_qc_flag = test_value
        self.assertEqual(self.instance.pressure_qc_flag, test_value)
    
    def test_normal_pressure_property(self):
        """
        Test normal_pressure property
        """
        test_value = float(83.86494670484328)
        self.instance.normal_pressure = test_value
        self.assertEqual(self.instance.normal_pressure, test_value)
    
    def test_normal_pressure_qc_flag_property(self):
        """
        Test normal_pressure_qc_flag property
        """
        test_value = int(47)
        self.instance.normal_pressure_qc_flag = test_value
        self.assertEqual(self.instance.normal_pressure_qc_flag, test_value)
    
    def test_wind_speed_property(self):
        """
        Test wind_speed property
        """
        test_value = float(67.1470566153106)
        self.instance.wind_speed = test_value
        self.assertEqual(self.instance.wind_speed, test_value)
    
    def test_wind_speed_qc_flag_property(self):
        """
        Test wind_speed_qc_flag property
        """
        test_value = int(40)
        self.instance.wind_speed_qc_flag = test_value
        self.assertEqual(self.instance.wind_speed_qc_flag, test_value)
    
    def test_wind_direction_property(self):
        """
        Test wind_direction property
        """
        test_value = float(42.495861734199714)
        self.instance.wind_direction = test_value
        self.assertEqual(self.instance.wind_direction, test_value)
    
    def test_wind_direction_qc_flag_property(self):
        """
        Test wind_direction_qc_flag property
        """
        test_value = int(54)
        self.instance.wind_direction_qc_flag = test_value
        self.assertEqual(self.instance.wind_direction_qc_flag, test_value)
    
    def test_wind_gust_property(self):
        """
        Test wind_gust property
        """
        test_value = float(66.6663611458625)
        self.instance.wind_gust = test_value
        self.assertEqual(self.instance.wind_gust, test_value)
    
    def test_wind_gust_qc_flag_property(self):
        """
        Test wind_gust_qc_flag property
        """
        test_value = int(56)
        self.instance.wind_gust_qc_flag = test_value
        self.assertEqual(self.instance.wind_gust_qc_flag, test_value)
    
    def test_wind_gust_direction_property(self):
        """
        Test wind_gust_direction property
        """
        test_value = float(39.93986436875537)
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
        test_value = float(4.597604153411727)
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
        test_value = float(84.47287052473624)
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
        test_value = float(27.97937179260346)
        self.instance.precipitation10m = test_value
        self.assertEqual(self.instance.precipitation10m, test_value)
    
    def test_precipitation10m_qc_flag_property(self):
        """
        Test precipitation10m_qc_flag property
        """
        test_value = int(71)
        self.instance.precipitation10m_qc_flag = test_value
        self.assertEqual(self.instance.precipitation10m_qc_flag, test_value)
    
    def test_precipitation1h_property(self):
        """
        Test precipitation1h property
        """
        test_value = float(14.086164328660999)
        self.instance.precipitation1h = test_value
        self.assertEqual(self.instance.precipitation1h, test_value)
    
    def test_precipitation1h_qc_flag_property(self):
        """
        Test precipitation1h_qc_flag property
        """
        test_value = int(59)
        self.instance.precipitation1h_qc_flag = test_value
        self.assertEqual(self.instance.precipitation1h_qc_flag, test_value)
    
    def test_precipitation3h_property(self):
        """
        Test precipitation3h property
        """
        test_value = float(6.238482935078816)
        self.instance.precipitation3h = test_value
        self.assertEqual(self.instance.precipitation3h, test_value)
    
    def test_precipitation3h_qc_flag_property(self):
        """
        Test precipitation3h_qc_flag property
        """
        test_value = int(77)
        self.instance.precipitation3h_qc_flag = test_value
        self.assertEqual(self.instance.precipitation3h_qc_flag, test_value)
    
    def test_precipitation24h_property(self):
        """
        Test precipitation24h property
        """
        test_value = float(73.80837283347941)
        self.instance.precipitation24h = test_value
        self.assertEqual(self.instance.precipitation24h, test_value)
    
    def test_precipitation24h_qc_flag_property(self):
        """
        Test precipitation24h_qc_flag property
        """
        test_value = int(59)
        self.instance.precipitation24h_qc_flag = test_value
        self.assertEqual(self.instance.precipitation24h_qc_flag, test_value)
    
    def test_sun10m_property(self):
        """
        Test sun10m property
        """
        test_value = float(67.73277092874366)
        self.instance.sun10m = test_value
        self.assertEqual(self.instance.sun10m, test_value)
    
    def test_sun10m_qc_flag_property(self):
        """
        Test sun10m_qc_flag property
        """
        test_value = int(58)
        self.instance.sun10m_qc_flag = test_value
        self.assertEqual(self.instance.sun10m_qc_flag, test_value)
    
    def test_sun1h_property(self):
        """
        Test sun1h property
        """
        test_value = float(80.26102995327416)
        self.instance.sun1h = test_value
        self.assertEqual(self.instance.sun1h, test_value)
    
    def test_sun1h_qc_flag_property(self):
        """
        Test sun1h_qc_flag property
        """
        test_value = int(5)
        self.instance.sun1h_qc_flag = test_value
        self.assertEqual(self.instance.sun1h_qc_flag, test_value)
    
    def test_snow_property(self):
        """
        Test snow property
        """
        test_value = float(17.163040322929646)
        self.instance.snow = test_value
        self.assertEqual(self.instance.snow, test_value)
    
    def test_snow_qc_flag_property(self):
        """
        Test snow_qc_flag property
        """
        test_value = int(2)
        self.instance.snow_qc_flag = test_value
        self.assertEqual(self.instance.snow_qc_flag, test_value)
    
    def test_snow1h_property(self):
        """
        Test snow1h property
        """
        test_value = float(80.18284496472252)
        self.instance.snow1h = test_value
        self.assertEqual(self.instance.snow1h, test_value)
    
    def test_snow1h_qc_flag_property(self):
        """
        Test snow1h_qc_flag property
        """
        test_value = int(79)
        self.instance.snow1h_qc_flag = test_value
        self.assertEqual(self.instance.snow1h_qc_flag, test_value)
    
    def test_snow6h_property(self):
        """
        Test snow6h property
        """
        test_value = float(16.49387186870982)
        self.instance.snow6h = test_value
        self.assertEqual(self.instance.snow6h, test_value)
    
    def test_snow6h_qc_flag_property(self):
        """
        Test snow6h_qc_flag property
        """
        test_value = int(97)
        self.instance.snow6h_qc_flag = test_value
        self.assertEqual(self.instance.snow6h_qc_flag, test_value)
    
    def test_snow12h_property(self):
        """
        Test snow12h property
        """
        test_value = float(77.12537355105252)
        self.instance.snow12h = test_value
        self.assertEqual(self.instance.snow12h, test_value)
    
    def test_snow12h_qc_flag_property(self):
        """
        Test snow12h_qc_flag property
        """
        test_value = int(53)
        self.instance.snow12h_qc_flag = test_value
        self.assertEqual(self.instance.snow12h_qc_flag, test_value)
    
    def test_snow24h_property(self):
        """
        Test snow24h property
        """
        test_value = float(13.171597993286198)
        self.instance.snow24h = test_value
        self.assertEqual(self.instance.snow24h, test_value)
    
    def test_snow24h_qc_flag_property(self):
        """
        Test snow24h_qc_flag property
        """
        test_value = int(43)
        self.instance.snow24h_qc_flag = test_value
        self.assertEqual(self.instance.snow24h_qc_flag, test_value)
    
    def test_visibility_property(self):
        """
        Test visibility property
        """
        test_value = float(92.21139753459897)
        self.instance.visibility = test_value
        self.assertEqual(self.instance.visibility, test_value)
    
    def test_visibility_qc_flag_property(self):
        """
        Test visibility_qc_flag property
        """
        test_value = int(52)
        self.instance.visibility_qc_flag = test_value
        self.assertEqual(self.instance.visibility_qc_flag, test_value)
    
    def test_cloud_property(self):
        """
        Test cloud property
        """
        test_value = float(16.4375189963879)
        self.instance.cloud = test_value
        self.assertEqual(self.instance.cloud, test_value)
    
    def test_cloud_qc_flag_property(self):
        """
        Test cloud_qc_flag property
        """
        test_value = int(69)
        self.instance.cloud_qc_flag = test_value
        self.assertEqual(self.instance.cloud_qc_flag, test_value)
    
    def test_weather_property(self):
        """
        Test weather property
        """
        test_value = float(6.370101675984364)
        self.instance.weather = test_value
        self.assertEqual(self.instance.weather, test_value)
    
    def test_weather_qc_flag_property(self):
        """
        Test weather_qc_flag property
        """
        test_value = int(61)
        self.instance.weather_qc_flag = test_value
        self.assertEqual(self.instance.weather_qc_flag, test_value)
    
    def test_prefecture_property(self):
        """
        Test prefecture property
        """
        test_value = 'ilbgbordlyxeglhtldvr'
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

