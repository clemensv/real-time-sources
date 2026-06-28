"""
Test case for Observation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_amedas_amqp_producer_data.jp.jma.amedas.observation import Observation
from jma_bosai_amedas_amqp_producer_data.jp.jma.amedas.observationeventenum import ObservationEventEnum
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
            station_code='dyzwxdqfyxchfuplxzqz',
            observed_at=datetime.datetime.now(datetime.timezone.utc),
            observed_at_local=datetime.datetime.now(datetime.timezone.utc),
            temp=float(26.120468748978876),
            temp_qc_flag=int(38),
            humidity=float(84.16824925759275),
            humidity_qc_flag=int(28),
            pressure=float(3.286051109640775),
            pressure_qc_flag=int(55),
            normal_pressure=float(7.872044872880579),
            normal_pressure_qc_flag=int(2),
            wind_speed=float(72.3617312864713),
            wind_speed_qc_flag=int(49),
            wind_direction=float(65.78773443732919),
            wind_direction_qc_flag=int(80),
            wind_gust=float(76.47197236636293),
            wind_gust_qc_flag=int(100),
            wind_gust_direction=float(60.86237199503736),
            wind_gust_time=datetime.datetime.now(datetime.timezone.utc),
            max_temp=float(73.44595475574788),
            max_temp_time=datetime.datetime.now(datetime.timezone.utc),
            min_temp=float(80.32624047620158),
            min_temp_time=datetime.datetime.now(datetime.timezone.utc),
            precipitation10m=float(90.90829072732306),
            precipitation10m_qc_flag=int(82),
            precipitation1h=float(57.524985152182495),
            precipitation1h_qc_flag=int(79),
            precipitation3h=float(88.88439441799942),
            precipitation3h_qc_flag=int(21),
            precipitation24h=float(27.70874100120013),
            precipitation24h_qc_flag=int(78),
            sun10m=float(12.224805196580634),
            sun10m_qc_flag=int(9),
            sun1h=float(57.74262415650844),
            sun1h_qc_flag=int(32),
            snow=float(84.8252167750316),
            snow_qc_flag=int(66),
            snow1h=float(73.34151298650671),
            snow1h_qc_flag=int(89),
            snow6h=float(48.02134457930271),
            snow6h_qc_flag=int(24),
            snow12h=float(56.49469592744355),
            snow12h_qc_flag=int(84),
            snow24h=float(12.805664620263336),
            snow24h_qc_flag=int(94),
            visibility=float(10.654270615760863),
            visibility_qc_flag=int(8),
            cloud=float(53.168051314754806),
            cloud_qc_flag=int(50),
            weather=float(53.70579634378151),
            weather_qc_flag=int(2),
            prefecture='fmkufclxmnqvwdfoivzq',
            event=ObservationEventEnum.observation
        )
        return instance

    
    def test_station_code_property(self):
        """
        Test station_code property
        """
        test_value = 'dyzwxdqfyxchfuplxzqz'
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
        test_value = float(26.120468748978876)
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
        test_value = float(84.16824925759275)
        self.instance.humidity = test_value
        self.assertEqual(self.instance.humidity, test_value)
    
    def test_humidity_qc_flag_property(self):
        """
        Test humidity_qc_flag property
        """
        test_value = int(28)
        self.instance.humidity_qc_flag = test_value
        self.assertEqual(self.instance.humidity_qc_flag, test_value)
    
    def test_pressure_property(self):
        """
        Test pressure property
        """
        test_value = float(3.286051109640775)
        self.instance.pressure = test_value
        self.assertEqual(self.instance.pressure, test_value)
    
    def test_pressure_qc_flag_property(self):
        """
        Test pressure_qc_flag property
        """
        test_value = int(55)
        self.instance.pressure_qc_flag = test_value
        self.assertEqual(self.instance.pressure_qc_flag, test_value)
    
    def test_normal_pressure_property(self):
        """
        Test normal_pressure property
        """
        test_value = float(7.872044872880579)
        self.instance.normal_pressure = test_value
        self.assertEqual(self.instance.normal_pressure, test_value)
    
    def test_normal_pressure_qc_flag_property(self):
        """
        Test normal_pressure_qc_flag property
        """
        test_value = int(2)
        self.instance.normal_pressure_qc_flag = test_value
        self.assertEqual(self.instance.normal_pressure_qc_flag, test_value)
    
    def test_wind_speed_property(self):
        """
        Test wind_speed property
        """
        test_value = float(72.3617312864713)
        self.instance.wind_speed = test_value
        self.assertEqual(self.instance.wind_speed, test_value)
    
    def test_wind_speed_qc_flag_property(self):
        """
        Test wind_speed_qc_flag property
        """
        test_value = int(49)
        self.instance.wind_speed_qc_flag = test_value
        self.assertEqual(self.instance.wind_speed_qc_flag, test_value)
    
    def test_wind_direction_property(self):
        """
        Test wind_direction property
        """
        test_value = float(65.78773443732919)
        self.instance.wind_direction = test_value
        self.assertEqual(self.instance.wind_direction, test_value)
    
    def test_wind_direction_qc_flag_property(self):
        """
        Test wind_direction_qc_flag property
        """
        test_value = int(80)
        self.instance.wind_direction_qc_flag = test_value
        self.assertEqual(self.instance.wind_direction_qc_flag, test_value)
    
    def test_wind_gust_property(self):
        """
        Test wind_gust property
        """
        test_value = float(76.47197236636293)
        self.instance.wind_gust = test_value
        self.assertEqual(self.instance.wind_gust, test_value)
    
    def test_wind_gust_qc_flag_property(self):
        """
        Test wind_gust_qc_flag property
        """
        test_value = int(100)
        self.instance.wind_gust_qc_flag = test_value
        self.assertEqual(self.instance.wind_gust_qc_flag, test_value)
    
    def test_wind_gust_direction_property(self):
        """
        Test wind_gust_direction property
        """
        test_value = float(60.86237199503736)
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
        test_value = float(73.44595475574788)
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
        test_value = float(80.32624047620158)
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
        test_value = float(90.90829072732306)
        self.instance.precipitation10m = test_value
        self.assertEqual(self.instance.precipitation10m, test_value)
    
    def test_precipitation10m_qc_flag_property(self):
        """
        Test precipitation10m_qc_flag property
        """
        test_value = int(82)
        self.instance.precipitation10m_qc_flag = test_value
        self.assertEqual(self.instance.precipitation10m_qc_flag, test_value)
    
    def test_precipitation1h_property(self):
        """
        Test precipitation1h property
        """
        test_value = float(57.524985152182495)
        self.instance.precipitation1h = test_value
        self.assertEqual(self.instance.precipitation1h, test_value)
    
    def test_precipitation1h_qc_flag_property(self):
        """
        Test precipitation1h_qc_flag property
        """
        test_value = int(79)
        self.instance.precipitation1h_qc_flag = test_value
        self.assertEqual(self.instance.precipitation1h_qc_flag, test_value)
    
    def test_precipitation3h_property(self):
        """
        Test precipitation3h property
        """
        test_value = float(88.88439441799942)
        self.instance.precipitation3h = test_value
        self.assertEqual(self.instance.precipitation3h, test_value)
    
    def test_precipitation3h_qc_flag_property(self):
        """
        Test precipitation3h_qc_flag property
        """
        test_value = int(21)
        self.instance.precipitation3h_qc_flag = test_value
        self.assertEqual(self.instance.precipitation3h_qc_flag, test_value)
    
    def test_precipitation24h_property(self):
        """
        Test precipitation24h property
        """
        test_value = float(27.70874100120013)
        self.instance.precipitation24h = test_value
        self.assertEqual(self.instance.precipitation24h, test_value)
    
    def test_precipitation24h_qc_flag_property(self):
        """
        Test precipitation24h_qc_flag property
        """
        test_value = int(78)
        self.instance.precipitation24h_qc_flag = test_value
        self.assertEqual(self.instance.precipitation24h_qc_flag, test_value)
    
    def test_sun10m_property(self):
        """
        Test sun10m property
        """
        test_value = float(12.224805196580634)
        self.instance.sun10m = test_value
        self.assertEqual(self.instance.sun10m, test_value)
    
    def test_sun10m_qc_flag_property(self):
        """
        Test sun10m_qc_flag property
        """
        test_value = int(9)
        self.instance.sun10m_qc_flag = test_value
        self.assertEqual(self.instance.sun10m_qc_flag, test_value)
    
    def test_sun1h_property(self):
        """
        Test sun1h property
        """
        test_value = float(57.74262415650844)
        self.instance.sun1h = test_value
        self.assertEqual(self.instance.sun1h, test_value)
    
    def test_sun1h_qc_flag_property(self):
        """
        Test sun1h_qc_flag property
        """
        test_value = int(32)
        self.instance.sun1h_qc_flag = test_value
        self.assertEqual(self.instance.sun1h_qc_flag, test_value)
    
    def test_snow_property(self):
        """
        Test snow property
        """
        test_value = float(84.8252167750316)
        self.instance.snow = test_value
        self.assertEqual(self.instance.snow, test_value)
    
    def test_snow_qc_flag_property(self):
        """
        Test snow_qc_flag property
        """
        test_value = int(66)
        self.instance.snow_qc_flag = test_value
        self.assertEqual(self.instance.snow_qc_flag, test_value)
    
    def test_snow1h_property(self):
        """
        Test snow1h property
        """
        test_value = float(73.34151298650671)
        self.instance.snow1h = test_value
        self.assertEqual(self.instance.snow1h, test_value)
    
    def test_snow1h_qc_flag_property(self):
        """
        Test snow1h_qc_flag property
        """
        test_value = int(89)
        self.instance.snow1h_qc_flag = test_value
        self.assertEqual(self.instance.snow1h_qc_flag, test_value)
    
    def test_snow6h_property(self):
        """
        Test snow6h property
        """
        test_value = float(48.02134457930271)
        self.instance.snow6h = test_value
        self.assertEqual(self.instance.snow6h, test_value)
    
    def test_snow6h_qc_flag_property(self):
        """
        Test snow6h_qc_flag property
        """
        test_value = int(24)
        self.instance.snow6h_qc_flag = test_value
        self.assertEqual(self.instance.snow6h_qc_flag, test_value)
    
    def test_snow12h_property(self):
        """
        Test snow12h property
        """
        test_value = float(56.49469592744355)
        self.instance.snow12h = test_value
        self.assertEqual(self.instance.snow12h, test_value)
    
    def test_snow12h_qc_flag_property(self):
        """
        Test snow12h_qc_flag property
        """
        test_value = int(84)
        self.instance.snow12h_qc_flag = test_value
        self.assertEqual(self.instance.snow12h_qc_flag, test_value)
    
    def test_snow24h_property(self):
        """
        Test snow24h property
        """
        test_value = float(12.805664620263336)
        self.instance.snow24h = test_value
        self.assertEqual(self.instance.snow24h, test_value)
    
    def test_snow24h_qc_flag_property(self):
        """
        Test snow24h_qc_flag property
        """
        test_value = int(94)
        self.instance.snow24h_qc_flag = test_value
        self.assertEqual(self.instance.snow24h_qc_flag, test_value)
    
    def test_visibility_property(self):
        """
        Test visibility property
        """
        test_value = float(10.654270615760863)
        self.instance.visibility = test_value
        self.assertEqual(self.instance.visibility, test_value)
    
    def test_visibility_qc_flag_property(self):
        """
        Test visibility_qc_flag property
        """
        test_value = int(8)
        self.instance.visibility_qc_flag = test_value
        self.assertEqual(self.instance.visibility_qc_flag, test_value)
    
    def test_cloud_property(self):
        """
        Test cloud property
        """
        test_value = float(53.168051314754806)
        self.instance.cloud = test_value
        self.assertEqual(self.instance.cloud, test_value)
    
    def test_cloud_qc_flag_property(self):
        """
        Test cloud_qc_flag property
        """
        test_value = int(50)
        self.instance.cloud_qc_flag = test_value
        self.assertEqual(self.instance.cloud_qc_flag, test_value)
    
    def test_weather_property(self):
        """
        Test weather property
        """
        test_value = float(53.70579634378151)
        self.instance.weather = test_value
        self.assertEqual(self.instance.weather, test_value)
    
    def test_weather_qc_flag_property(self):
        """
        Test weather_qc_flag property
        """
        test_value = int(2)
        self.instance.weather_qc_flag = test_value
        self.assertEqual(self.instance.weather_qc_flag, test_value)
    
    def test_prefecture_property(self):
        """
        Test prefecture property
        """
        test_value = 'fmkufclxmnqvwdfoivzq'
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

