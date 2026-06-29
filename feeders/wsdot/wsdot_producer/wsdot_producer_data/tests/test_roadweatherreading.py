"""
Test case for RoadWeatherReading
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from wsdot_producer_data.us.wa.wsdot.roadweather.roadweatherreading import RoadWeatherReading
from wsdot_producer_data.us.wa.wsdot.roadweather.subsurfacemeasurement import SubSurfaceMeasurement
from wsdot_producer_data.us.wa.wsdot.roadweather.surfacemeasurement import SurfaceMeasurement


class Test_RoadWeatherReading(unittest.TestCase):
    """
    Test case for RoadWeatherReading
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_RoadWeatherReading.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of RoadWeatherReading for testing
        """
        instance = RoadWeatherReading(
            station_id='vhktqosymwbuctrztnei',
            station_name='gfdvwgoyambpqlfcmkrf',
            latitude=float(21.13354152093937),
            longitude=float(49.57220379572781),
            elevation=int(35),
            reading_time='pjbuxtxackfskukwyxaz',
            air_temperature=float(25.78169512245664),
            relative_humidity=int(67),
            average_wind_speed=float(12.131692685699102),
            average_wind_direction=int(36),
            wind_gust=float(50.82576446135476),
            visibility=int(4),
            precipitation_intensity=int(64),
            precipitation_type=int(21),
            precipitation_past_1_hour=float(95.13605521553194),
            precipitation_past_3_hours=float(1.2185033057316552),
            precipitation_past_6_hours=float(93.15599715065878),
            precipitation_past_12_hours=float(44.74664773468658),
            precipitation_past_24_hours=float(51.18496683632415),
            precipitation_accumulation=float(16.99653021428823),
            barometric_pressure=float(65.20922274436813),
            snow_depth=float(83.28772445842289),
            surface_measurements=[None],
            sub_surface_measurements=[None]
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'vhktqosymwbuctrztnei'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'gfdvwgoyambpqlfcmkrf'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(21.13354152093937)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(49.57220379572781)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_elevation_property(self):
        """
        Test elevation property
        """
        test_value = int(35)
        self.instance.elevation = test_value
        self.assertEqual(self.instance.elevation, test_value)
    
    def test_reading_time_property(self):
        """
        Test reading_time property
        """
        test_value = 'pjbuxtxackfskukwyxaz'
        self.instance.reading_time = test_value
        self.assertEqual(self.instance.reading_time, test_value)
    
    def test_air_temperature_property(self):
        """
        Test air_temperature property
        """
        test_value = float(25.78169512245664)
        self.instance.air_temperature = test_value
        self.assertEqual(self.instance.air_temperature, test_value)
    
    def test_relative_humidity_property(self):
        """
        Test relative_humidity property
        """
        test_value = int(67)
        self.instance.relative_humidity = test_value
        self.assertEqual(self.instance.relative_humidity, test_value)
    
    def test_average_wind_speed_property(self):
        """
        Test average_wind_speed property
        """
        test_value = float(12.131692685699102)
        self.instance.average_wind_speed = test_value
        self.assertEqual(self.instance.average_wind_speed, test_value)
    
    def test_average_wind_direction_property(self):
        """
        Test average_wind_direction property
        """
        test_value = int(36)
        self.instance.average_wind_direction = test_value
        self.assertEqual(self.instance.average_wind_direction, test_value)
    
    def test_wind_gust_property(self):
        """
        Test wind_gust property
        """
        test_value = float(50.82576446135476)
        self.instance.wind_gust = test_value
        self.assertEqual(self.instance.wind_gust, test_value)
    
    def test_visibility_property(self):
        """
        Test visibility property
        """
        test_value = int(4)
        self.instance.visibility = test_value
        self.assertEqual(self.instance.visibility, test_value)
    
    def test_precipitation_intensity_property(self):
        """
        Test precipitation_intensity property
        """
        test_value = int(64)
        self.instance.precipitation_intensity = test_value
        self.assertEqual(self.instance.precipitation_intensity, test_value)
    
    def test_precipitation_type_property(self):
        """
        Test precipitation_type property
        """
        test_value = int(21)
        self.instance.precipitation_type = test_value
        self.assertEqual(self.instance.precipitation_type, test_value)
    
    def test_precipitation_past_1_hour_property(self):
        """
        Test precipitation_past_1_hour property
        """
        test_value = float(95.13605521553194)
        self.instance.precipitation_past_1_hour = test_value
        self.assertEqual(self.instance.precipitation_past_1_hour, test_value)
    
    def test_precipitation_past_3_hours_property(self):
        """
        Test precipitation_past_3_hours property
        """
        test_value = float(1.2185033057316552)
        self.instance.precipitation_past_3_hours = test_value
        self.assertEqual(self.instance.precipitation_past_3_hours, test_value)
    
    def test_precipitation_past_6_hours_property(self):
        """
        Test precipitation_past_6_hours property
        """
        test_value = float(93.15599715065878)
        self.instance.precipitation_past_6_hours = test_value
        self.assertEqual(self.instance.precipitation_past_6_hours, test_value)
    
    def test_precipitation_past_12_hours_property(self):
        """
        Test precipitation_past_12_hours property
        """
        test_value = float(44.74664773468658)
        self.instance.precipitation_past_12_hours = test_value
        self.assertEqual(self.instance.precipitation_past_12_hours, test_value)
    
    def test_precipitation_past_24_hours_property(self):
        """
        Test precipitation_past_24_hours property
        """
        test_value = float(51.18496683632415)
        self.instance.precipitation_past_24_hours = test_value
        self.assertEqual(self.instance.precipitation_past_24_hours, test_value)
    
    def test_precipitation_accumulation_property(self):
        """
        Test precipitation_accumulation property
        """
        test_value = float(16.99653021428823)
        self.instance.precipitation_accumulation = test_value
        self.assertEqual(self.instance.precipitation_accumulation, test_value)
    
    def test_barometric_pressure_property(self):
        """
        Test barometric_pressure property
        """
        test_value = float(65.20922274436813)
        self.instance.barometric_pressure = test_value
        self.assertEqual(self.instance.barometric_pressure, test_value)
    
    def test_snow_depth_property(self):
        """
        Test snow_depth property
        """
        test_value = float(83.28772445842289)
        self.instance.snow_depth = test_value
        self.assertEqual(self.instance.snow_depth, test_value)
    
    def test_surface_measurements_property(self):
        """
        Test surface_measurements property
        """
        test_value = [None]
        self.instance.surface_measurements = test_value
        self.assertEqual(self.instance.surface_measurements, test_value)
    
    def test_sub_surface_measurements_property(self):
        """
        Test sub_surface_measurements property
        """
        test_value = [None]
        self.instance.sub_surface_measurements = test_value
        self.assertEqual(self.instance.sub_surface_measurements, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = RoadWeatherReading.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = RoadWeatherReading.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

