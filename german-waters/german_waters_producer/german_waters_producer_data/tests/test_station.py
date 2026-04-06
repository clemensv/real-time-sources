"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from german_waters_producer_data.station import Station


class Test_Station(unittest.TestCase):
    """
    Test case for Station
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Station.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Station for testing
        """
        instance = Station(
            station_id='rnzrhdwvwfpcygykryrw',
            station_name='hiuctlpwvmzcrlilqdfe',
            water_body='wtbafnfuarwtoadspjyb',
            state='uvmycwblykojbtfdsvjh',
            region='rvcetnyiejpxdsrrdcnl',
            provider='srlbbqsxtrvtsaearwrg',
            latitude=float(43.6581595257145),
            longitude=float(49.83795689777193),
            river_km=float(44.69247786336202),
            altitude=float(26.37989497033977),
            station_type='ftvhekvvfbrvjfmvikct',
            warn_level_cm=float(9.296879119389867),
            alarm_level_cm=float(43.30648059588951),
            warn_level_m3s=float(66.82145473295586),
            alarm_level_m3s=float(79.98576106579081)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'rnzrhdwvwfpcygykryrw'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'hiuctlpwvmzcrlilqdfe'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_water_body_property(self):
        """
        Test water_body property
        """
        test_value = 'wtbafnfuarwtoadspjyb'
        self.instance.water_body = test_value
        self.assertEqual(self.instance.water_body, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'uvmycwblykojbtfdsvjh'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'rvcetnyiejpxdsrrdcnl'
        self.instance.region = test_value
        self.assertEqual(self.instance.region, test_value)
    
    def test_provider_property(self):
        """
        Test provider property
        """
        test_value = 'srlbbqsxtrvtsaearwrg'
        self.instance.provider = test_value
        self.assertEqual(self.instance.provider, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(43.6581595257145)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(49.83795689777193)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_river_km_property(self):
        """
        Test river_km property
        """
        test_value = float(44.69247786336202)
        self.instance.river_km = test_value
        self.assertEqual(self.instance.river_km, test_value)
    
    def test_altitude_property(self):
        """
        Test altitude property
        """
        test_value = float(26.37989497033977)
        self.instance.altitude = test_value
        self.assertEqual(self.instance.altitude, test_value)
    
    def test_station_type_property(self):
        """
        Test station_type property
        """
        test_value = 'ftvhekvvfbrvjfmvikct'
        self.instance.station_type = test_value
        self.assertEqual(self.instance.station_type, test_value)
    
    def test_warn_level_cm_property(self):
        """
        Test warn_level_cm property
        """
        test_value = float(9.296879119389867)
        self.instance.warn_level_cm = test_value
        self.assertEqual(self.instance.warn_level_cm, test_value)
    
    def test_alarm_level_cm_property(self):
        """
        Test alarm_level_cm property
        """
        test_value = float(43.30648059588951)
        self.instance.alarm_level_cm = test_value
        self.assertEqual(self.instance.alarm_level_cm, test_value)
    
    def test_warn_level_m3s_property(self):
        """
        Test warn_level_m3s property
        """
        test_value = float(66.82145473295586)
        self.instance.warn_level_m3s = test_value
        self.assertEqual(self.instance.warn_level_m3s, test_value)
    
    def test_alarm_level_m3s_property(self):
        """
        Test alarm_level_m3s property
        """
        test_value = float(79.98576106579081)
        self.instance.alarm_level_m3s = test_value
        self.assertEqual(self.instance.alarm_level_m3s, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Station.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Station.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

