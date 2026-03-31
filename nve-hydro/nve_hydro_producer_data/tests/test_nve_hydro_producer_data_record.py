"""
Test case for Record
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from nve_hydro_producer_data.record import Record


class Test_Record(unittest.TestCase):
    """
    Test case for Record
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Record.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Record for testing
        """
        instance = Record(
            station_id='nwwcufqbbqxuuctjllcf',
            station_name='cijezlgxjnenspieziii',
            river_name='dnvwfkqmlmwhsnmyaaay',
            latitude=float(29.625689162492364),
            longitude=float(81.06232574067567),
            masl=float(51.20208713444916),
            council_name='fltlmpcswcivfhohomha',
            county_name='liocwziznnjfhxcgylme',
            drainage_basin_area=float(54.22757889872399)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'nwwcufqbbqxuuctjllcf'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'cijezlgxjnenspieziii'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_river_name_property(self):
        """
        Test river_name property
        """
        test_value = 'dnvwfkqmlmwhsnmyaaay'
        self.instance.river_name = test_value
        self.assertEqual(self.instance.river_name, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(29.625689162492364)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(81.06232574067567)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_masl_property(self):
        """
        Test masl property
        """
        test_value = float(51.20208713444916)
        self.instance.masl = test_value
        self.assertEqual(self.instance.masl, test_value)
    
    def test_council_name_property(self):
        """
        Test council_name property
        """
        test_value = 'fltlmpcswcivfhohomha'
        self.instance.council_name = test_value
        self.assertEqual(self.instance.council_name, test_value)
    
    def test_county_name_property(self):
        """
        Test county_name property
        """
        test_value = 'liocwziznnjfhxcgylme'
        self.instance.county_name = test_value
        self.assertEqual(self.instance.county_name, test_value)
    
    def test_drainage_basin_area_property(self):
        """
        Test drainage_basin_area property
        """
        test_value = float(54.22757889872399)
        self.instance.drainage_basin_area = test_value
        self.assertEqual(self.instance.drainage_basin_area, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Record.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
