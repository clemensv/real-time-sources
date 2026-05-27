"""
Test case for Observation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from canada_eccc_wateroffice_amqp_producer_data.observation import Observation
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
            station_number='babkotcrnsrjpeodbtft',
            identifier='ltqfirzooyomigdzmiel',
            station_name='uueqjfedaikgtxrvnaks',
            prov_terr_state_loc='ksefqizlgsazfkshsqkv',
            observation_datetime=datetime.datetime.now(datetime.timezone.utc),
            level=float(15.287942141878851),
            discharge=float(72.40019887891391),
            latitude=float(96.07411560984556),
            longitude=float(54.71078523300462),
            basin='iaxsexwgbuvdjgardddv'
        )
        return instance

    
    def test_station_number_property(self):
        """
        Test station_number property
        """
        test_value = 'babkotcrnsrjpeodbtft'
        self.instance.station_number = test_value
        self.assertEqual(self.instance.station_number, test_value)
    
    def test_identifier_property(self):
        """
        Test identifier property
        """
        test_value = 'ltqfirzooyomigdzmiel'
        self.instance.identifier = test_value
        self.assertEqual(self.instance.identifier, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'uueqjfedaikgtxrvnaks'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_prov_terr_state_loc_property(self):
        """
        Test prov_terr_state_loc property
        """
        test_value = 'ksefqizlgsazfkshsqkv'
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
        test_value = float(15.287942141878851)
        self.instance.level = test_value
        self.assertEqual(self.instance.level, test_value)
    
    def test_discharge_property(self):
        """
        Test discharge property
        """
        test_value = float(72.40019887891391)
        self.instance.discharge = test_value
        self.assertEqual(self.instance.discharge, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(96.07411560984556)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(54.71078523300462)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_basin_property(self):
        """
        Test basin property
        """
        test_value = 'iaxsexwgbuvdjgardddv'
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

