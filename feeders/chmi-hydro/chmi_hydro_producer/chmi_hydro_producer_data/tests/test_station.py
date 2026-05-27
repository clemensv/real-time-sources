"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from chmi_hydro_producer_data.station import Station


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
            station_id='mammobhgxkqcsloeeftd',
            dbc='fajcryetfrbouterkgdk',
            station_name='kqnnfsoswtrfwqkkvnnj',
            stream_name='hypawcfdkgidwrbggyds',
            latitude=float(37.19537309380387),
            longitude=float(41.97648021295816),
            flood_level_1=float(2.6167343847442237),
            flood_level_2=float(64.27077455530993),
            flood_level_3=float(76.08175539657718),
            flood_level_4=float(15.347173436917538),
            has_forecast=True
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'mammobhgxkqcsloeeftd'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_dbc_property(self):
        """
        Test dbc property
        """
        test_value = 'fajcryetfrbouterkgdk'
        self.instance.dbc = test_value
        self.assertEqual(self.instance.dbc, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'kqnnfsoswtrfwqkkvnnj'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_stream_name_property(self):
        """
        Test stream_name property
        """
        test_value = 'hypawcfdkgidwrbggyds'
        self.instance.stream_name = test_value
        self.assertEqual(self.instance.stream_name, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(37.19537309380387)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(41.97648021295816)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_flood_level_1_property(self):
        """
        Test flood_level_1 property
        """
        test_value = float(2.6167343847442237)
        self.instance.flood_level_1 = test_value
        self.assertEqual(self.instance.flood_level_1, test_value)
    
    def test_flood_level_2_property(self):
        """
        Test flood_level_2 property
        """
        test_value = float(64.27077455530993)
        self.instance.flood_level_2 = test_value
        self.assertEqual(self.instance.flood_level_2, test_value)
    
    def test_flood_level_3_property(self):
        """
        Test flood_level_3 property
        """
        test_value = float(76.08175539657718)
        self.instance.flood_level_3 = test_value
        self.assertEqual(self.instance.flood_level_3, test_value)
    
    def test_flood_level_4_property(self):
        """
        Test flood_level_4 property
        """
        test_value = float(15.347173436917538)
        self.instance.flood_level_4 = test_value
        self.assertEqual(self.instance.flood_level_4, test_value)
    
    def test_has_forecast_property(self):
        """
        Test has_forecast property
        """
        test_value = True
        self.instance.has_forecast = test_value
        self.assertEqual(self.instance.has_forecast, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Station.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
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

