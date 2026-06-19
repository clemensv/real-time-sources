"""
Test case for RiverStation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from nepal_bipad_hydrology_amqp_producer_data.np.gov.bipad.hydrology.riverstation import RiverStation


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
            station_id='bdbhzzzfwevqkaiqmjii',
            title='ngskosmtcqfdrnkpkkkl',
            basin='nzgaoqpdfjnxpmniufoj',
            latitude=float(59.34571411838385),
            longitude=float(33.29246338935263),
            elevation=int(69),
            danger_level=float(29.598831830079387),
            warning_level=float(24.095852482167412),
            description='zvuebhbmgkwndpfauaao',
            data_source='qeoxtczrfxxndjwnakxn',
            province=int(20),
            district=int(33),
            municipality=int(80),
            ward=int(37)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'bdbhzzzfwevqkaiqmjii'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_title_property(self):
        """
        Test title property
        """
        test_value = 'ngskosmtcqfdrnkpkkkl'
        self.instance.title = test_value
        self.assertEqual(self.instance.title, test_value)
    
    def test_basin_property(self):
        """
        Test basin property
        """
        test_value = 'nzgaoqpdfjnxpmniufoj'
        self.instance.basin = test_value
        self.assertEqual(self.instance.basin, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(59.34571411838385)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(33.29246338935263)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_elevation_property(self):
        """
        Test elevation property
        """
        test_value = int(69)
        self.instance.elevation = test_value
        self.assertEqual(self.instance.elevation, test_value)
    
    def test_danger_level_property(self):
        """
        Test danger_level property
        """
        test_value = float(29.598831830079387)
        self.instance.danger_level = test_value
        self.assertEqual(self.instance.danger_level, test_value)
    
    def test_warning_level_property(self):
        """
        Test warning_level property
        """
        test_value = float(24.095852482167412)
        self.instance.warning_level = test_value
        self.assertEqual(self.instance.warning_level, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'zvuebhbmgkwndpfauaao'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_data_source_property(self):
        """
        Test data_source property
        """
        test_value = 'qeoxtczrfxxndjwnakxn'
        self.instance.data_source = test_value
        self.assertEqual(self.instance.data_source, test_value)
    
    def test_province_property(self):
        """
        Test province property
        """
        test_value = int(20)
        self.instance.province = test_value
        self.assertEqual(self.instance.province, test_value)
    
    def test_district_property(self):
        """
        Test district property
        """
        test_value = int(33)
        self.instance.district = test_value
        self.assertEqual(self.instance.district, test_value)
    
    def test_municipality_property(self):
        """
        Test municipality property
        """
        test_value = int(80)
        self.instance.municipality = test_value
        self.assertEqual(self.instance.municipality, test_value)
    
    def test_ward_property(self):
        """
        Test ward property
        """
        test_value = int(37)
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

