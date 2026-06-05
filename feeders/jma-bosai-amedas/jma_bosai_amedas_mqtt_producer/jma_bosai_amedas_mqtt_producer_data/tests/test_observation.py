"""
Test case for Observation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_amedas_mqtt_producer_data.jp.jma.amedas.observation import Observation
from jma_bosai_amedas_mqtt_producer_data.jp.jma.amedas.eventenum import EventEnum
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
            station_code='dzooxtzgpupscnmatmtn',
            observed_at=datetime.datetime.now(datetime.timezone.utc),
            observed_at_local=datetime.datetime.now(datetime.timezone.utc),
            temp=float(44.69633690318299),
            temp_qc_flag=int(26),
            humidity=float(6.402065287051418),
            humidity_qc_flag=int(11),
            pressure=float(33.377391690744794),
            pressure_qc_flag=int(39),
            normal_pressure=float(27.86340815224625),
            normal_pressure_qc_flag=int(80),
            wind_speed=float(52.4318643421643),
            wind_speed_qc_flag=int(29),
            wind_direction=float(49.213098655765755),
            wind_direction_qc_flag=int(48),
            wind_gust=float(7.405317045262072),
            wind_gust_qc_flag=int(23),
            wind_gust_direction=float(73.80815079811667),
            wind_gust_time=datetime.datetime.now(datetime.timezone.utc),
            max_temp=float(42.636926315258314),
            max_temp_time=datetime.datetime.now(datetime.timezone.utc),
            min_temp=float(87.6787731968165),
            min_temp_time=datetime.datetime.now(datetime.timezone.utc),
            precipitation10m=float(10.931856691206509),
            precipitation10m_qc_flag=int(58),
            precipitation1h=float(32.932822893346895),
            precipitation1h_qc_flag=int(58),
            precipitation3h=float(35.55533680461803),
            precipitation3h_qc_flag=int(68),
            precipitation24h=float(23.499788393272127),
            precipitation24h_qc_flag=int(83),
            sun10m=float(28.993307944937598),
            sun10m_qc_flag=int(5),
            sun1h=float(28.814878771017316),
            sun1h_qc_flag=int(70),
            snow=float(94.62325963681496),
            snow_qc_flag=int(16),
            snow1h=float(16.734735763480213),
            snow1h_qc_flag=int(52),
            snow6h=float(5.394349342401405),
            snow6h_qc_flag=int(27),
            snow12h=float(64.65585561405966),
            snow12h_qc_flag=int(66),
            snow24h=float(39.288565459771704),
            snow24h_qc_flag=int(0),
            visibility=float(67.95599316060303),
            visibility_qc_flag=int(66),
            cloud=float(42.8215847052354),
            cloud_qc_flag=int(40),
            weather=float(74.23942445484742),
            weather_qc_flag=int(24),
            prefecture='brukfakejhmkjfrctkwt',
            event=EventEnum.observation
        )
        return instance

    
    def test_station_code_property(self):
        """
        Test station_code property
        """
        test_value = 'dzooxtzgpupscnmatmtn'
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
        test_value = float(44.69633690318299)
        self.instance.temp = test_value
        self.assertEqual(self.instance.temp, test_value)
    
    def test_temp_qc_flag_property(self):
        """
        Test temp_qc_flag property
        """
        test_value = int(26)
        self.instance.temp_qc_flag = test_value
        self.assertEqual(self.instance.temp_qc_flag, test_value)
    
    def test_humidity_property(self):
        """
        Test humidity property
        """
        test_value = float(6.402065287051418)
        self.instance.humidity = test_value
        self.assertEqual(self.instance.humidity, test_value)
    
    def test_humidity_qc_flag_property(self):
        """
        Test humidity_qc_flag property
        """
        test_value = int(11)
        self.instance.humidity_qc_flag = test_value
        self.assertEqual(self.instance.humidity_qc_flag, test_value)
    
    def test_pressure_property(self):
        """
        Test pressure property
        """
        test_value = float(33.377391690744794)
        self.instance.pressure = test_value
        self.assertEqual(self.instance.pressure, test_value)
    
    def test_pressure_qc_flag_property(self):
        """
        Test pressure_qc_flag property
        """
        test_value = int(39)
        self.instance.pressure_qc_flag = test_value
        self.assertEqual(self.instance.pressure_qc_flag, test_value)
    
    def test_normal_pressure_property(self):
        """
        Test normal_pressure property
        """
        test_value = float(27.86340815224625)
        self.instance.normal_pressure = test_value
        self.assertEqual(self.instance.normal_pressure, test_value)
    
    def test_normal_pressure_qc_flag_property(self):
        """
        Test normal_pressure_qc_flag property
        """
        test_value = int(80)
        self.instance.normal_pressure_qc_flag = test_value
        self.assertEqual(self.instance.normal_pressure_qc_flag, test_value)
    
    def test_wind_speed_property(self):
        """
        Test wind_speed property
        """
        test_value = float(52.4318643421643)
        self.instance.wind_speed = test_value
        self.assertEqual(self.instance.wind_speed, test_value)
    
    def test_wind_speed_qc_flag_property(self):
        """
        Test wind_speed_qc_flag property
        """
        test_value = int(29)
        self.instance.wind_speed_qc_flag = test_value
        self.assertEqual(self.instance.wind_speed_qc_flag, test_value)
    
    def test_wind_direction_property(self):
        """
        Test wind_direction property
        """
        test_value = float(49.213098655765755)
        self.instance.wind_direction = test_value
        self.assertEqual(self.instance.wind_direction, test_value)
    
    def test_wind_direction_qc_flag_property(self):
        """
        Test wind_direction_qc_flag property
        """
        test_value = int(48)
        self.instance.wind_direction_qc_flag = test_value
        self.assertEqual(self.instance.wind_direction_qc_flag, test_value)
    
    def test_wind_gust_property(self):
        """
        Test wind_gust property
        """
        test_value = float(7.405317045262072)
        self.instance.wind_gust = test_value
        self.assertEqual(self.instance.wind_gust, test_value)
    
    def test_wind_gust_qc_flag_property(self):
        """
        Test wind_gust_qc_flag property
        """
        test_value = int(23)
        self.instance.wind_gust_qc_flag = test_value
        self.assertEqual(self.instance.wind_gust_qc_flag, test_value)
    
    def test_wind_gust_direction_property(self):
        """
        Test wind_gust_direction property
        """
        test_value = float(73.80815079811667)
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
        test_value = float(42.636926315258314)
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
        test_value = float(87.6787731968165)
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
        test_value = float(10.931856691206509)
        self.instance.precipitation10m = test_value
        self.assertEqual(self.instance.precipitation10m, test_value)
    
    def test_precipitation10m_qc_flag_property(self):
        """
        Test precipitation10m_qc_flag property
        """
        test_value = int(58)
        self.instance.precipitation10m_qc_flag = test_value
        self.assertEqual(self.instance.precipitation10m_qc_flag, test_value)
    
    def test_precipitation1h_property(self):
        """
        Test precipitation1h property
        """
        test_value = float(32.932822893346895)
        self.instance.precipitation1h = test_value
        self.assertEqual(self.instance.precipitation1h, test_value)
    
    def test_precipitation1h_qc_flag_property(self):
        """
        Test precipitation1h_qc_flag property
        """
        test_value = int(58)
        self.instance.precipitation1h_qc_flag = test_value
        self.assertEqual(self.instance.precipitation1h_qc_flag, test_value)
    
    def test_precipitation3h_property(self):
        """
        Test precipitation3h property
        """
        test_value = float(35.55533680461803)
        self.instance.precipitation3h = test_value
        self.assertEqual(self.instance.precipitation3h, test_value)
    
    def test_precipitation3h_qc_flag_property(self):
        """
        Test precipitation3h_qc_flag property
        """
        test_value = int(68)
        self.instance.precipitation3h_qc_flag = test_value
        self.assertEqual(self.instance.precipitation3h_qc_flag, test_value)
    
    def test_precipitation24h_property(self):
        """
        Test precipitation24h property
        """
        test_value = float(23.499788393272127)
        self.instance.precipitation24h = test_value
        self.assertEqual(self.instance.precipitation24h, test_value)
    
    def test_precipitation24h_qc_flag_property(self):
        """
        Test precipitation24h_qc_flag property
        """
        test_value = int(83)
        self.instance.precipitation24h_qc_flag = test_value
        self.assertEqual(self.instance.precipitation24h_qc_flag, test_value)
    
    def test_sun10m_property(self):
        """
        Test sun10m property
        """
        test_value = float(28.993307944937598)
        self.instance.sun10m = test_value
        self.assertEqual(self.instance.sun10m, test_value)
    
    def test_sun10m_qc_flag_property(self):
        """
        Test sun10m_qc_flag property
        """
        test_value = int(5)
        self.instance.sun10m_qc_flag = test_value
        self.assertEqual(self.instance.sun10m_qc_flag, test_value)
    
    def test_sun1h_property(self):
        """
        Test sun1h property
        """
        test_value = float(28.814878771017316)
        self.instance.sun1h = test_value
        self.assertEqual(self.instance.sun1h, test_value)
    
    def test_sun1h_qc_flag_property(self):
        """
        Test sun1h_qc_flag property
        """
        test_value = int(70)
        self.instance.sun1h_qc_flag = test_value
        self.assertEqual(self.instance.sun1h_qc_flag, test_value)
    
    def test_snow_property(self):
        """
        Test snow property
        """
        test_value = float(94.62325963681496)
        self.instance.snow = test_value
        self.assertEqual(self.instance.snow, test_value)
    
    def test_snow_qc_flag_property(self):
        """
        Test snow_qc_flag property
        """
        test_value = int(16)
        self.instance.snow_qc_flag = test_value
        self.assertEqual(self.instance.snow_qc_flag, test_value)
    
    def test_snow1h_property(self):
        """
        Test snow1h property
        """
        test_value = float(16.734735763480213)
        self.instance.snow1h = test_value
        self.assertEqual(self.instance.snow1h, test_value)
    
    def test_snow1h_qc_flag_property(self):
        """
        Test snow1h_qc_flag property
        """
        test_value = int(52)
        self.instance.snow1h_qc_flag = test_value
        self.assertEqual(self.instance.snow1h_qc_flag, test_value)
    
    def test_snow6h_property(self):
        """
        Test snow6h property
        """
        test_value = float(5.394349342401405)
        self.instance.snow6h = test_value
        self.assertEqual(self.instance.snow6h, test_value)
    
    def test_snow6h_qc_flag_property(self):
        """
        Test snow6h_qc_flag property
        """
        test_value = int(27)
        self.instance.snow6h_qc_flag = test_value
        self.assertEqual(self.instance.snow6h_qc_flag, test_value)
    
    def test_snow12h_property(self):
        """
        Test snow12h property
        """
        test_value = float(64.65585561405966)
        self.instance.snow12h = test_value
        self.assertEqual(self.instance.snow12h, test_value)
    
    def test_snow12h_qc_flag_property(self):
        """
        Test snow12h_qc_flag property
        """
        test_value = int(66)
        self.instance.snow12h_qc_flag = test_value
        self.assertEqual(self.instance.snow12h_qc_flag, test_value)
    
    def test_snow24h_property(self):
        """
        Test snow24h property
        """
        test_value = float(39.288565459771704)
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
        test_value = float(67.95599316060303)
        self.instance.visibility = test_value
        self.assertEqual(self.instance.visibility, test_value)
    
    def test_visibility_qc_flag_property(self):
        """
        Test visibility_qc_flag property
        """
        test_value = int(66)
        self.instance.visibility_qc_flag = test_value
        self.assertEqual(self.instance.visibility_qc_flag, test_value)
    
    def test_cloud_property(self):
        """
        Test cloud property
        """
        test_value = float(42.8215847052354)
        self.instance.cloud = test_value
        self.assertEqual(self.instance.cloud, test_value)
    
    def test_cloud_qc_flag_property(self):
        """
        Test cloud_qc_flag property
        """
        test_value = int(40)
        self.instance.cloud_qc_flag = test_value
        self.assertEqual(self.instance.cloud_qc_flag, test_value)
    
    def test_weather_property(self):
        """
        Test weather property
        """
        test_value = float(74.23942445484742)
        self.instance.weather = test_value
        self.assertEqual(self.instance.weather, test_value)
    
    def test_weather_qc_flag_property(self):
        """
        Test weather_qc_flag property
        """
        test_value = int(24)
        self.instance.weather_qc_flag = test_value
        self.assertEqual(self.instance.weather_qc_flag, test_value)
    
    def test_prefecture_property(self):
        """
        Test prefecture property
        """
        test_value = 'brukfakejhmkjfrctkwt'
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

