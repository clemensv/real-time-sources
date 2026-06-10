"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from canada_eccc_wateroffice_producer_data.station import Station


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
            station_number='tlejjycislrmvyjjlmtx',
            station_name='smhprbpwczdltkxtsrhr',
            prov_terr_state_loc='rojiqfyepvizhxbiihrs',
            status_en='yqltqahsqioxjwrxmuah',
            contributor_en='gvmqhjtgadwvkmkklmxj',
            drainage_area_gross=float(45.73310295439388),
            drainage_area_effect=float(62.227151291035334),
            rhbn=False,
            real_time=True,
            latitude=float(41.06487598163435),
            longitude=float(28.61515576749908),
            basin='kqbzqmmczqmjnzdigxyd'
        )
        return instance

    
    def test_station_number_property(self):
        """
        Test station_number property
        """
        test_value = 'tlejjycislrmvyjjlmtx'
        self.instance.station_number = test_value
        self.assertEqual(self.instance.station_number, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'smhprbpwczdltkxtsrhr'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_prov_terr_state_loc_property(self):
        """
        Test prov_terr_state_loc property
        """
        test_value = 'rojiqfyepvizhxbiihrs'
        self.instance.prov_terr_state_loc = test_value
        self.assertEqual(self.instance.prov_terr_state_loc, test_value)
    
    def test_status_en_property(self):
        """
        Test status_en property
        """
        test_value = 'yqltqahsqioxjwrxmuah'
        self.instance.status_en = test_value
        self.assertEqual(self.instance.status_en, test_value)
    
    def test_contributor_en_property(self):
        """
        Test contributor_en property
        """
        test_value = 'gvmqhjtgadwvkmkklmxj'
        self.instance.contributor_en = test_value
        self.assertEqual(self.instance.contributor_en, test_value)
    
    def test_drainage_area_gross_property(self):
        """
        Test drainage_area_gross property
        """
        test_value = float(45.73310295439388)
        self.instance.drainage_area_gross = test_value
        self.assertEqual(self.instance.drainage_area_gross, test_value)
    
    def test_drainage_area_effect_property(self):
        """
        Test drainage_area_effect property
        """
        test_value = float(62.227151291035334)
        self.instance.drainage_area_effect = test_value
        self.assertEqual(self.instance.drainage_area_effect, test_value)
    
    def test_rhbn_property(self):
        """
        Test rhbn property
        """
        test_value = False
        self.instance.rhbn = test_value
        self.assertEqual(self.instance.rhbn, test_value)
    
    def test_real_time_property(self):
        """
        Test real_time property
        """
        test_value = True
        self.instance.real_time = test_value
        self.assertEqual(self.instance.real_time, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(41.06487598163435)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(28.61515576749908)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_basin_property(self):
        """
        Test basin property
        """
        test_value = 'kqbzqmmczqmjnzdigxyd'
        self.instance.basin = test_value
        self.assertEqual(self.instance.basin, test_value)
    
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

