"""
Test case for ObservationStation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_nws_producer_data.observationstation import ObservationStation


class Test_ObservationStation(unittest.TestCase):
    """
    Test case for ObservationStation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_ObservationStation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of ObservationStation for testing
        """
        instance = ObservationStation(
            station_id='dftyenuryrcscdakrjpc',
            name='jgboxenqzltkcfjqgqfh',
            elevation_m=float(43.95384571074674),
            time_zone='uosrhanqkjeccnuedjmq',
            forecast_zone='uvympxcrzhtscukgssne',
            county='pcvcaxivusqppcoubpxb',
            fire_weather_zone='nqptsmxcljnvnonibzjo',
            state='qjjieqxoshfcmcncdrfj',
            zone_id='ujgjcbqptegmzexohmrz'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'dftyenuryrcscdakrjpc'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'jgboxenqzltkcfjqgqfh'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_elevation_m_property(self):
        """
        Test elevation_m property
        """
        test_value = float(43.95384571074674)
        self.instance.elevation_m = test_value
        self.assertEqual(self.instance.elevation_m, test_value)
    
    def test_time_zone_property(self):
        """
        Test time_zone property
        """
        test_value = 'uosrhanqkjeccnuedjmq'
        self.instance.time_zone = test_value
        self.assertEqual(self.instance.time_zone, test_value)
    
    def test_forecast_zone_property(self):
        """
        Test forecast_zone property
        """
        test_value = 'uvympxcrzhtscukgssne'
        self.instance.forecast_zone = test_value
        self.assertEqual(self.instance.forecast_zone, test_value)
    
    def test_county_property(self):
        """
        Test county property
        """
        test_value = 'pcvcaxivusqppcoubpxb'
        self.instance.county = test_value
        self.assertEqual(self.instance.county, test_value)
    
    def test_fire_weather_zone_property(self):
        """
        Test fire_weather_zone property
        """
        test_value = 'nqptsmxcljnvnonibzjo'
        self.instance.fire_weather_zone = test_value
        self.assertEqual(self.instance.fire_weather_zone, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'qjjieqxoshfcmcncdrfj'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_zone_id_property(self):
        """
        Test zone_id property
        """
        test_value = 'ujgjcbqptegmzexohmrz'
        self.instance.zone_id = test_value
        self.assertEqual(self.instance.zone_id, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = ObservationStation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = ObservationStation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = ObservationStation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

