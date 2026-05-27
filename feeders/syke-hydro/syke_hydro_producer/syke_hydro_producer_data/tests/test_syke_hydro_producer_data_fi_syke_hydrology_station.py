"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from syke_hydro_producer_data.fi.syke.hydrology.station import Station


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
            station_id='vubovwqmjyltdbijfobd',
            name='udgykvkxrhojorgbhlqg',
            river_name='lehegzwwpotioywatwdj',
            water_area_name='craftntwxuvkbgodfuej',
            municipality='djfytmgfawifhpysuodt',
            latitude=float(59.244869400857716),
            longitude=float(21.25248093630807)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'vubovwqmjyltdbijfobd'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'udgykvkxrhojorgbhlqg'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_river_name_property(self):
        """
        Test river_name property
        """
        test_value = 'lehegzwwpotioywatwdj'
        self.instance.river_name = test_value
        self.assertEqual(self.instance.river_name, test_value)
    
    def test_water_area_name_property(self):
        """
        Test water_area_name property
        """
        test_value = 'craftntwxuvkbgodfuej'
        self.instance.water_area_name = test_value
        self.assertEqual(self.instance.water_area_name, test_value)
    
    def test_municipality_property(self):
        """
        Test municipality property
        """
        test_value = 'djfytmgfawifhpysuodt'
        self.instance.municipality = test_value
        self.assertEqual(self.instance.municipality, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(59.244869400857716)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(21.25248093630807)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Station.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
