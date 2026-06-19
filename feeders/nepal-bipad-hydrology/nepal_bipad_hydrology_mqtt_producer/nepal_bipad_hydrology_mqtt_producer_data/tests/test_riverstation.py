"""
Test case for RiverStation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from nepal_bipad_hydrology_mqtt_producer_data.np.gov.bipad.hydrology.riverstation import RiverStation


class Test_RiverStation(unittest.TestCase):
    """
    Test case for RiverStation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_RiverStation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of RiverStation for testing
        """
        instance = RiverStation(
            station_id='zdaxsxtybdsacdtdlnhb',
            title='hsyxeqnwojucgnogbtdr',
            basin='vkvtvbgodtrnhesjietz',
            latitude=float(81.72268953985733),
            longitude=float(11.714478011700747),
            elevation=int(25),
            danger_level=float(69.52269911269528),
            warning_level=float(62.20659509396016),
            description='warcajfaabcsaegzwqez',
            data_source='sluiydfphnclvafzmvqg',
            province=int(55),
            district=int(26),
            municipality=int(92),
            ward=int(68)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'zdaxsxtybdsacdtdlnhb'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_title_property(self):
        """
        Test title property
        """
        test_value = 'hsyxeqnwojucgnogbtdr'
        self.instance.title = test_value
        self.assertEqual(self.instance.title, test_value)
    
    def test_basin_property(self):
        """
        Test basin property
        """
        test_value = 'vkvtvbgodtrnhesjietz'
        self.instance.basin = test_value
        self.assertEqual(self.instance.basin, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(81.72268953985733)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(11.714478011700747)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_elevation_property(self):
        """
        Test elevation property
        """
        test_value = int(25)
        self.instance.elevation = test_value
        self.assertEqual(self.instance.elevation, test_value)
    
    def test_danger_level_property(self):
        """
        Test danger_level property
        """
        test_value = float(69.52269911269528)
        self.instance.danger_level = test_value
        self.assertEqual(self.instance.danger_level, test_value)
    
    def test_warning_level_property(self):
        """
        Test warning_level property
        """
        test_value = float(62.20659509396016)
        self.instance.warning_level = test_value
        self.assertEqual(self.instance.warning_level, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'warcajfaabcsaegzwqez'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_data_source_property(self):
        """
        Test data_source property
        """
        test_value = 'sluiydfphnclvafzmvqg'
        self.instance.data_source = test_value
        self.assertEqual(self.instance.data_source, test_value)
    
    def test_province_property(self):
        """
        Test province property
        """
        test_value = int(55)
        self.instance.province = test_value
        self.assertEqual(self.instance.province, test_value)
    
    def test_district_property(self):
        """
        Test district property
        """
        test_value = int(26)
        self.instance.district = test_value
        self.assertEqual(self.instance.district, test_value)
    
    def test_municipality_property(self):
        """
        Test municipality property
        """
        test_value = int(92)
        self.instance.municipality = test_value
        self.assertEqual(self.instance.municipality, test_value)
    
    def test_ward_property(self):
        """
        Test ward property
        """
        test_value = int(68)
        self.instance.ward = test_value
        self.assertEqual(self.instance.ward, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = RiverStation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = RiverStation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

