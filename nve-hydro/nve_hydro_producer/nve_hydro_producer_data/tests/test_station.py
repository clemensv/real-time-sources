"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from nve_hydro_producer_data.station import Station


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
            station_id='imoikxxlvvqaxrphjzhs',
            station_name='tappiiwazuqctbjctsao',
            river_name='gwxqtwmflyptsibftvrn',
            latitude=float(52.28494696333586),
            longitude=float(40.85148615999793),
            masl=float(28.361835969062465),
            council_name='kffcndctmdjbmtsrtmrn',
            county_name='bgxbznilvmjurmhsczck',
            drainage_basin_area=float(69.26682800728226)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'imoikxxlvvqaxrphjzhs'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'tappiiwazuqctbjctsao'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_river_name_property(self):
        """
        Test river_name property
        """
        test_value = 'gwxqtwmflyptsibftvrn'
        self.instance.river_name = test_value
        self.assertEqual(self.instance.river_name, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(52.28494696333586)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(40.85148615999793)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_masl_property(self):
        """
        Test masl property
        """
        test_value = float(28.361835969062465)
        self.instance.masl = test_value
        self.assertEqual(self.instance.masl, test_value)
    
    def test_council_name_property(self):
        """
        Test council_name property
        """
        test_value = 'kffcndctmdjbmtsrtmrn'
        self.instance.council_name = test_value
        self.assertEqual(self.instance.council_name, test_value)
    
    def test_county_name_property(self):
        """
        Test county_name property
        """
        test_value = 'bgxbznilvmjurmhsczck'
        self.instance.county_name = test_value
        self.assertEqual(self.instance.county_name, test_value)
    
    def test_drainage_basin_area_property(self):
        """
        Test drainage_basin_area property
        """
        test_value = float(69.26682800728226)
        self.instance.drainage_basin_area = test_value
        self.assertEqual(self.instance.drainage_basin_area, test_value)
    
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

