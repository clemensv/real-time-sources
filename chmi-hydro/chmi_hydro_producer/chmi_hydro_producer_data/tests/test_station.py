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
            station_id='ofuoeunjoltssbhdqdmi',
            dbc='iouljytbyustwebgfsdc',
            station_name='vxpernrmwphabihtuamj',
            stream_name='stuarxtsnqbvcwuyqiwa',
            latitude=float(49.37620261898071),
            longitude=float(88.30884948898151),
            flood_level_1=float(60.82358398551783),
            flood_level_2=float(49.42457654143918),
            flood_level_3=float(14.716280474620069),
            flood_level_4=float(55.21047637056081),
            has_forecast=True
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'ofuoeunjoltssbhdqdmi'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_dbc_property(self):
        """
        Test dbc property
        """
        test_value = 'iouljytbyustwebgfsdc'
        self.instance.dbc = test_value
        self.assertEqual(self.instance.dbc, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'vxpernrmwphabihtuamj'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_stream_name_property(self):
        """
        Test stream_name property
        """
        test_value = 'stuarxtsnqbvcwuyqiwa'
        self.instance.stream_name = test_value
        self.assertEqual(self.instance.stream_name, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(49.37620261898071)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(88.30884948898151)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_flood_level_1_property(self):
        """
        Test flood_level_1 property
        """
        test_value = float(60.82358398551783)
        self.instance.flood_level_1 = test_value
        self.assertEqual(self.instance.flood_level_1, test_value)
    
    def test_flood_level_2_property(self):
        """
        Test flood_level_2 property
        """
        test_value = float(49.42457654143918)
        self.instance.flood_level_2 = test_value
        self.assertEqual(self.instance.flood_level_2, test_value)
    
    def test_flood_level_3_property(self):
        """
        Test flood_level_3 property
        """
        test_value = float(14.716280474620069)
        self.instance.flood_level_3 = test_value
        self.assertEqual(self.instance.flood_level_3, test_value)
    
    def test_flood_level_4_property(self):
        """
        Test flood_level_4 property
        """
        test_value = float(55.21047637056081)
        self.instance.flood_level_4 = test_value
        self.assertEqual(self.instance.flood_level_4, test_value)
    
    def test_has_forecast_property(self):
        """
        Test has_forecast property
        """
        test_value = True
        self.instance.has_forecast = test_value
        self.assertEqual(self.instance.has_forecast, test_value)
    
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

