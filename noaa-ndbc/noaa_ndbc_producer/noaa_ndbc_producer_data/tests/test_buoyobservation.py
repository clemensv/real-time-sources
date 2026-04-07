"""
Test case for BuoyObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_ndbc_producer_data.buoyobservation import BuoyObservation
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
            station_id='naqublmrzzcwadqhixku',
            latitude=float(81.58063113937123),
            longitude=float(56.87558455273065),
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            wind_direction=float(72.3425509053619),
            wind_speed=float(31.519209359631382),
            gust=float(92.18458497994483),
            wave_height=float(53.86938872696979),
            dominant_wave_period=float(14.33025159549035),
            average_wave_period=float(36.0061749710534),
            mean_wave_direction=float(79.42157340968893),
            pressure=float(16.94806479926593),
            air_temperature=float(7.328927247653838),
            water_temperature=float(7.739535151612054),
            dewpoint=float(14.77855873113818)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'naqublmrzzcwadqhixku'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(81.58063113937123)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(56.87558455273065)
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
        test_value = float(72.3425509053619)
        self.instance.wind_direction = test_value
        self.assertEqual(self.instance.wind_direction, test_value)
    
    def test_wind_speed_property(self):
        """
        Test wind_speed property
        """
        test_value = float(31.519209359631382)
        self.instance.wind_speed = test_value
        self.assertEqual(self.instance.wind_speed, test_value)
    
    def test_gust_property(self):
        """
        Test gust property
        """
        test_value = float(92.18458497994483)
        self.instance.gust = test_value
        self.assertEqual(self.instance.gust, test_value)
    
    def test_wave_height_property(self):
        """
        Test wave_height property
        """
        test_value = float(53.86938872696979)
        self.instance.wave_height = test_value
        self.assertEqual(self.instance.wave_height, test_value)
    
    def test_dominant_wave_period_property(self):
        """
        Test dominant_wave_period property
        """
        test_value = float(14.33025159549035)
        self.instance.dominant_wave_period = test_value
        self.assertEqual(self.instance.dominant_wave_period, test_value)
    
    def test_average_wave_period_property(self):
        """
        Test average_wave_period property
        """
        test_value = float(36.0061749710534)
        self.instance.average_wave_period = test_value
        self.assertEqual(self.instance.average_wave_period, test_value)
    
    def test_mean_wave_direction_property(self):
        """
        Test mean_wave_direction property
        """
        test_value = float(79.42157340968893)
        self.instance.mean_wave_direction = test_value
        self.assertEqual(self.instance.mean_wave_direction, test_value)
    
    def test_pressure_property(self):
        """
        Test pressure property
        """
        test_value = float(16.94806479926593)
        self.instance.pressure = test_value
        self.assertEqual(self.instance.pressure, test_value)
    
    def test_air_temperature_property(self):
        """
        Test air_temperature property
        """
        test_value = float(7.328927247653838)
        self.instance.air_temperature = test_value
        self.assertEqual(self.instance.air_temperature, test_value)
    
    def test_water_temperature_property(self):
        """
        Test water_temperature property
        """
        test_value = float(7.739535151612054)
        self.instance.water_temperature = test_value
        self.assertEqual(self.instance.water_temperature, test_value)
    
    def test_dewpoint_property(self):
        """
        Test dewpoint property
        """
        test_value = float(14.77855873113818)
        self.instance.dewpoint = test_value
        self.assertEqual(self.instance.dewpoint, test_value)
    
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

