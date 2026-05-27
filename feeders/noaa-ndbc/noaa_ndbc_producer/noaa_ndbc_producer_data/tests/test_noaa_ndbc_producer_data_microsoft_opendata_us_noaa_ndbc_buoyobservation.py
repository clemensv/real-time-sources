"""
Test case for BuoyObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_ndbc_producer_data.microsoft.opendata.us.noaa.ndbc.buoyobservation import BuoyObservation
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
            station_id='vmpbhnfcnqwtfgrohbyj',
            latitude=float(59.32281027064392),
            longitude=float(21.29368924358921),
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            wind_direction=float(43.84789656785095),
            wind_speed=float(87.99755111929521),
            gust=float(21.09826463884058),
            wave_height=float(90.84789846545274),
            dominant_wave_period=float(34.04891907029626),
            average_wave_period=float(93.2229627025557),
            mean_wave_direction=float(16.752315805452277),
            pressure=float(30.33244955511951),
            air_temperature=float(94.60953285576052),
            water_temperature=float(46.798769587013425),
            dewpoint=float(66.37908886174739),
            pressure_tendency=float(70.67600401456389),
            visibility=float(68.35477654244781),
            tide=float(20.741974109699136)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'vmpbhnfcnqwtfgrohbyj'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(59.32281027064392)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(21.29368924358921)
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
        test_value = float(43.84789656785095)
        self.instance.wind_direction = test_value
        self.assertEqual(self.instance.wind_direction, test_value)
    
    def test_wind_speed_property(self):
        """
        Test wind_speed property
        """
        test_value = float(87.99755111929521)
        self.instance.wind_speed = test_value
        self.assertEqual(self.instance.wind_speed, test_value)
    
    def test_gust_property(self):
        """
        Test gust property
        """
        test_value = float(21.09826463884058)
        self.instance.gust = test_value
        self.assertEqual(self.instance.gust, test_value)
    
    def test_wave_height_property(self):
        """
        Test wave_height property
        """
        test_value = float(90.84789846545274)
        self.instance.wave_height = test_value
        self.assertEqual(self.instance.wave_height, test_value)
    
    def test_dominant_wave_period_property(self):
        """
        Test dominant_wave_period property
        """
        test_value = float(34.04891907029626)
        self.instance.dominant_wave_period = test_value
        self.assertEqual(self.instance.dominant_wave_period, test_value)
    
    def test_average_wave_period_property(self):
        """
        Test average_wave_period property
        """
        test_value = float(93.2229627025557)
        self.instance.average_wave_period = test_value
        self.assertEqual(self.instance.average_wave_period, test_value)
    
    def test_mean_wave_direction_property(self):
        """
        Test mean_wave_direction property
        """
        test_value = float(16.752315805452277)
        self.instance.mean_wave_direction = test_value
        self.assertEqual(self.instance.mean_wave_direction, test_value)
    
    def test_pressure_property(self):
        """
        Test pressure property
        """
        test_value = float(30.33244955511951)
        self.instance.pressure = test_value
        self.assertEqual(self.instance.pressure, test_value)
    
    def test_air_temperature_property(self):
        """
        Test air_temperature property
        """
        test_value = float(94.60953285576052)
        self.instance.air_temperature = test_value
        self.assertEqual(self.instance.air_temperature, test_value)
    
    def test_water_temperature_property(self):
        """
        Test water_temperature property
        """
        test_value = float(46.798769587013425)
        self.instance.water_temperature = test_value
        self.assertEqual(self.instance.water_temperature, test_value)
    
    def test_dewpoint_property(self):
        """
        Test dewpoint property
        """
        test_value = float(66.37908886174739)
        self.instance.dewpoint = test_value
        self.assertEqual(self.instance.dewpoint, test_value)
    
    def test_pressure_tendency_property(self):
        """
        Test pressure_tendency property
        """
        test_value = float(70.67600401456389)
        self.instance.pressure_tendency = test_value
        self.assertEqual(self.instance.pressure_tendency, test_value)
    
    def test_visibility_property(self):
        """
        Test visibility property
        """
        test_value = float(68.35477654244781)
        self.instance.visibility = test_value
        self.assertEqual(self.instance.visibility, test_value)
    
    def test_tide_property(self):
        """
        Test tide property
        """
        test_value = float(20.741974109699136)
        self.instance.tide = test_value
        self.assertEqual(self.instance.tide, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = BuoyObservation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
