"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from canada_eccc_wateroffice_mqtt_producer_data.station import Station


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
            station_number='hrqgjitaewallfocuyzk',
            station_name='kgibicjgbpldidqvrmqq',
            prov_terr_state_loc='psrcvqjkfzgscidwjtpf',
            status_en='cnjooghnwoslaiswdlxv',
            contributor_en='bxetgwvusttgexvyjftf',
            drainage_area_gross=float(66.0494533327738),
            drainage_area_effect=float(28.247418172926466),
            rhbn=True,
            real_time=True,
            latitude=float(23.192207564357915),
            longitude=float(56.09487184263391),
            basin='anbprjukemjdrigumlhq'
        )
        return instance

    
    def test_station_number_property(self):
        """
        Test station_number property
        """
        test_value = 'hrqgjitaewallfocuyzk'
        self.instance.station_number = test_value
        self.assertEqual(self.instance.station_number, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'kgibicjgbpldidqvrmqq'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_prov_terr_state_loc_property(self):
        """
        Test prov_terr_state_loc property
        """
        test_value = 'psrcvqjkfzgscidwjtpf'
        self.instance.prov_terr_state_loc = test_value
        self.assertEqual(self.instance.prov_terr_state_loc, test_value)
    
    def test_status_en_property(self):
        """
        Test status_en property
        """
        test_value = 'cnjooghnwoslaiswdlxv'
        self.instance.status_en = test_value
        self.assertEqual(self.instance.status_en, test_value)
    
    def test_contributor_en_property(self):
        """
        Test contributor_en property
        """
        test_value = 'bxetgwvusttgexvyjftf'
        self.instance.contributor_en = test_value
        self.assertEqual(self.instance.contributor_en, test_value)
    
    def test_drainage_area_gross_property(self):
        """
        Test drainage_area_gross property
        """
        test_value = float(66.0494533327738)
        self.instance.drainage_area_gross = test_value
        self.assertEqual(self.instance.drainage_area_gross, test_value)
    
    def test_drainage_area_effect_property(self):
        """
        Test drainage_area_effect property
        """
        test_value = float(28.247418172926466)
        self.instance.drainage_area_effect = test_value
        self.assertEqual(self.instance.drainage_area_effect, test_value)
    
    def test_rhbn_property(self):
        """
        Test rhbn property
        """
        test_value = True
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
        test_value = float(23.192207564357915)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(56.09487184263391)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_basin_property(self):
        """
        Test basin property
        """
        test_value = 'anbprjukemjdrigumlhq'
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

