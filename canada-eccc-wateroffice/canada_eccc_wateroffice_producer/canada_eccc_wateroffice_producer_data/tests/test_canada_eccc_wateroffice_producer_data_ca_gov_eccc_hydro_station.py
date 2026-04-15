"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from canada_eccc_wateroffice_producer_data.ca.gov.eccc.hydro.station import Station


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
            station_number='yzagyvihdxtpblsslrpv',
            station_name='bttgqgcgidvxclvuhjcx',
            prov_terr_state_loc='mfwwjqflqyymurzditlj',
            status_en='yyyhhfwcevcgjbyfiymz',
            contributor_en='flfclumspgjekfvzqbio',
            drainage_area_gross=float(98.58445148067554),
            drainage_area_effect=float(52.15738579956252),
            rhbn=False,
            real_time=False,
            latitude=float(1.5779007150856006),
            longitude=float(50.10290370098982)
        )
        return instance

    
    def test_station_number_property(self):
        """
        Test station_number property
        """
        test_value = 'yzagyvihdxtpblsslrpv'
        self.instance.station_number = test_value
        self.assertEqual(self.instance.station_number, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'bttgqgcgidvxclvuhjcx'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_prov_terr_state_loc_property(self):
        """
        Test prov_terr_state_loc property
        """
        test_value = 'mfwwjqflqyymurzditlj'
        self.instance.prov_terr_state_loc = test_value
        self.assertEqual(self.instance.prov_terr_state_loc, test_value)
    
    def test_status_en_property(self):
        """
        Test status_en property
        """
        test_value = 'yyyhhfwcevcgjbyfiymz'
        self.instance.status_en = test_value
        self.assertEqual(self.instance.status_en, test_value)
    
    def test_contributor_en_property(self):
        """
        Test contributor_en property
        """
        test_value = 'flfclumspgjekfvzqbio'
        self.instance.contributor_en = test_value
        self.assertEqual(self.instance.contributor_en, test_value)
    
    def test_drainage_area_gross_property(self):
        """
        Test drainage_area_gross property
        """
        test_value = float(98.58445148067554)
        self.instance.drainage_area_gross = test_value
        self.assertEqual(self.instance.drainage_area_gross, test_value)
    
    def test_drainage_area_effect_property(self):
        """
        Test drainage_area_effect property
        """
        test_value = float(52.15738579956252)
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
        test_value = False
        self.instance.real_time = test_value
        self.assertEqual(self.instance.real_time, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(1.5779007150856006)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(50.10290370098982)
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
