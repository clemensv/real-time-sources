"""
Test case for BuoyObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_ndbc_amqp_producer_data.buoyobservation import BuoyObservation
import datetime


class Test_BuoyObservation(unittest.TestCase):
    """
    Test case for BuoyObservation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_BuoyObservation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of BuoyObservation for testing
        """
        instance = BuoyObservation(
            station_id='zuckqsobifriusolgith',
            latitude=float(87.38169456298381),
            longitude=float(68.40200649827041),
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            wind_direction=float(4.2625325394142655),
            wind_speed=float(96.3091045906952),
            gust=float(76.24922547210045),
            wave_height=float(60.312342240745274),
            dominant_wave_period=float(33.21118061835223),
            average_wave_period=float(67.97379243668216),
            mean_wave_direction=float(6.524896310909578),
            pressure=float(85.80604374209467),
            air_temperature=float(23.82974772579116),
            water_temperature=float(64.0196998592574),
            dewpoint=float(29.217473631696002),
            pressure_tendency=float(28.55296733840884),
            visibility=float(74.30976194837153),
            tide=float(27.69831068438513),
            region='yavahezpatmqkyqzutrj'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'zuckqsobifriusolgith'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(87.38169456298381)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(68.40200649827041)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_wind_direction_property(self):
        """
        Test wind_direction property
        """
        test_value = float(4.2625325394142655)
        self.instance.wind_direction = test_value
        self.assertEqual(self.instance.wind_direction, test_value)
    
    def test_wind_speed_property(self):
        """
        Test wind_speed property
        """
        test_value = float(96.3091045906952)
        self.instance.wind_speed = test_value
        self.assertEqual(self.instance.wind_speed, test_value)
    
    def test_gust_property(self):
        """
        Test gust property
        """
        test_value = float(76.24922547210045)
        self.instance.gust = test_value
        self.assertEqual(self.instance.gust, test_value)
    
    def test_wave_height_property(self):
        """
        Test wave_height property
        """
        test_value = float(60.312342240745274)
        self.instance.wave_height = test_value
        self.assertEqual(self.instance.wave_height, test_value)
    
    def test_dominant_wave_period_property(self):
        """
        Test dominant_wave_period property
        """
        test_value = float(33.21118061835223)
        self.instance.dominant_wave_period = test_value
        self.assertEqual(self.instance.dominant_wave_period, test_value)
    
    def test_average_wave_period_property(self):
        """
        Test average_wave_period property
        """
        test_value = float(67.97379243668216)
        self.instance.average_wave_period = test_value
        self.assertEqual(self.instance.average_wave_period, test_value)
    
    def test_mean_wave_direction_property(self):
        """
        Test mean_wave_direction property
        """
        test_value = float(6.524896310909578)
        self.instance.mean_wave_direction = test_value
        self.assertEqual(self.instance.mean_wave_direction, test_value)
    
    def test_pressure_property(self):
        """
        Test pressure property
        """
        test_value = float(85.80604374209467)
        self.instance.pressure = test_value
        self.assertEqual(self.instance.pressure, test_value)
    
    def test_air_temperature_property(self):
        """
        Test air_temperature property
        """
        test_value = float(23.82974772579116)
        self.instance.air_temperature = test_value
        self.assertEqual(self.instance.air_temperature, test_value)
    
    def test_water_temperature_property(self):
        """
        Test water_temperature property
        """
        test_value = float(64.0196998592574)
        self.instance.water_temperature = test_value
        self.assertEqual(self.instance.water_temperature, test_value)
    
    def test_dewpoint_property(self):
        """
        Test dewpoint property
        """
        test_value = float(29.217473631696002)
        self.instance.dewpoint = test_value
        self.assertEqual(self.instance.dewpoint, test_value)
    
    def test_pressure_tendency_property(self):
        """
        Test pressure_tendency property
        """
        test_value = float(28.55296733840884)
        self.instance.pressure_tendency = test_value
        self.assertEqual(self.instance.pressure_tendency, test_value)
    
    def test_visibility_property(self):
        """
        Test visibility property
        """
        test_value = float(74.30976194837153)
        self.instance.visibility = test_value
        self.assertEqual(self.instance.visibility, test_value)
    
    def test_tide_property(self):
        """
        Test tide property
        """
        test_value = float(27.69831068438513)
        self.instance.tide = test_value
        self.assertEqual(self.instance.tide, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'yavahezpatmqkyqzutrj'
        self.instance.region = test_value
        self.assertEqual(self.instance.region, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = BuoyObservation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = BuoyObservation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

