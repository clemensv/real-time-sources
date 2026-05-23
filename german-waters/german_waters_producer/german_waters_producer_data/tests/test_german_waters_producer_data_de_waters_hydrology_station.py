"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from german_waters_producer_data.de.waters.hydrology.station import Station


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
            station_id='momdbyignjfqyntzhvpg',
            station_name='gpbdryqlmcquiilkovrx',
            water_body='jwzoclkqneuubltdvspi',
            state='veoshaurtwhtbjcxrvge',
            region='lsjbfpppweflduvhjnqi',
            provider='sfscbkvfrzptlmjqpivg',
            latitude=float(88.163029486018),
            longitude=float(17.36368750604058),
            river_km=float(45.02936915705735),
            altitude=float(65.94691730184626),
            station_type='udnlrkmdzemujvopdrcw',
            warn_level_cm=float(81.08976877652698),
            alarm_level_cm=float(58.866582420723525),
            warn_level_m3s=float(17.03752997804344),
            alarm_level_m3s=float(10.44652831344095)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'momdbyignjfqyntzhvpg'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'gpbdryqlmcquiilkovrx'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_water_body_property(self):
        """
        Test water_body property
        """
        test_value = 'jwzoclkqneuubltdvspi'
        self.instance.water_body = test_value
        self.assertEqual(self.instance.water_body, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'veoshaurtwhtbjcxrvge'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'lsjbfpppweflduvhjnqi'
        self.instance.region = test_value
        self.assertEqual(self.instance.region, test_value)
    
    def test_provider_property(self):
        """
        Test provider property
        """
        test_value = 'sfscbkvfrzptlmjqpivg'
        self.instance.provider = test_value
        self.assertEqual(self.instance.provider, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(88.163029486018)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(17.36368750604058)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_river_km_property(self):
        """
        Test river_km property
        """
        test_value = float(45.02936915705735)
        self.instance.river_km = test_value
        self.assertEqual(self.instance.river_km, test_value)
    
    def test_altitude_property(self):
        """
        Test altitude property
        """
        test_value = float(65.94691730184626)
        self.instance.altitude = test_value
        self.assertEqual(self.instance.altitude, test_value)
    
    def test_station_type_property(self):
        """
        Test station_type property
        """
        test_value = 'udnlrkmdzemujvopdrcw'
        self.instance.station_type = test_value
        self.assertEqual(self.instance.station_type, test_value)
    
    def test_warn_level_cm_property(self):
        """
        Test warn_level_cm property
        """
        test_value = float(81.08976877652698)
        self.instance.warn_level_cm = test_value
        self.assertEqual(self.instance.warn_level_cm, test_value)
    
    def test_alarm_level_cm_property(self):
        """
        Test alarm_level_cm property
        """
        test_value = float(58.866582420723525)
        self.instance.alarm_level_cm = test_value
        self.assertEqual(self.instance.alarm_level_cm, test_value)
    
    def test_warn_level_m3s_property(self):
        """
        Test warn_level_m3s property
        """
        test_value = float(17.03752997804344)
        self.instance.warn_level_m3s = test_value
        self.assertEqual(self.instance.warn_level_m3s, test_value)
    
    def test_alarm_level_m3s_property(self):
        """
        Test alarm_level_m3s property
        """
        test_value = float(10.44652831344095)
        self.instance.alarm_level_m3s = test_value
        self.assertEqual(self.instance.alarm_level_m3s, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Station.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
