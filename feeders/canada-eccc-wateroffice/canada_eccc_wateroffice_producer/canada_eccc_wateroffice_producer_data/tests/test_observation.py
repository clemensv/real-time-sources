"""
Test case for Observation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from canada_eccc_wateroffice_producer_data.observation import Observation
import datetime


class Test_Observation(unittest.TestCase):
    """
    Test case for Observation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Observation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Observation for testing
        """
        instance = Observation(
            station_number='bswpktfppcwvmutiagry',
            identifier='pbgdpuvyenofibafupvs',
            station_name='pdnsclftynpwevnjaupn',
            prov_terr_state_loc='etfeiksdgzrkjwshihnu',
            observation_datetime=datetime.datetime.now(datetime.timezone.utc),
            level=float(60.99570201812029),
            discharge=float(69.14431850337628),
            latitude=float(8.468047958539081),
            longitude=float(46.502875991865665),
            basin='qaepobteizjpqjgyyigj'
        )
        return instance

    
    def test_station_number_property(self):
        """
        Test station_number property
        """
        test_value = 'bswpktfppcwvmutiagry'
        self.instance.station_number = test_value
        self.assertEqual(self.instance.station_number, test_value)
    
    def test_identifier_property(self):
        """
        Test identifier property
        """
        test_value = 'pbgdpuvyenofibafupvs'
        self.instance.identifier = test_value
        self.assertEqual(self.instance.identifier, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'pdnsclftynpwevnjaupn'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_prov_terr_state_loc_property(self):
        """
        Test prov_terr_state_loc property
        """
        test_value = 'etfeiksdgzrkjwshihnu'
        self.instance.prov_terr_state_loc = test_value
        self.assertEqual(self.instance.prov_terr_state_loc, test_value)
    
    def test_observation_datetime_property(self):
        """
        Test observation_datetime property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.observation_datetime = test_value
        self.assertEqual(self.instance.observation_datetime, test_value)
    
    def test_level_property(self):
        """
        Test level property
        """
        test_value = float(60.99570201812029)
        self.instance.level = test_value
        self.assertEqual(self.instance.level, test_value)
    
    def test_discharge_property(self):
        """
        Test discharge property
        """
        test_value = float(69.14431850337628)
        self.instance.discharge = test_value
        self.assertEqual(self.instance.discharge, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(8.468047958539081)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(46.502875991865665)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_basin_property(self):
        """
        Test basin property
        """
        test_value = 'qaepobteizjpqjgyyigj'
        self.instance.basin = test_value
        self.assertEqual(self.instance.basin, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Observation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Observation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

