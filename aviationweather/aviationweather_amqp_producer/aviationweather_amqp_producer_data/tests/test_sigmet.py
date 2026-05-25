"""
Test case for Sigmet
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aviationweather_amqp_producer_data.sigmet import Sigmet
import datetime


class Test_Sigmet(unittest.TestCase):
    """
    Test case for Sigmet
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Sigmet.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Sigmet for testing
        """
        instance = Sigmet(
            icao_id='acjacvbmrxdgymqkmsjq',
            series_id='tjtlkjbdegovzzgagibs',
            valid_time_from=datetime.datetime.now(datetime.timezone.utc),
            valid_time_to=datetime.datetime.now(datetime.timezone.utc),
            hazard='yxdmglnipsybowrrtjlc',
            qualifier='cikskzmyyptkttafxibh',
            sigmet_type='jhaiayhvxowdsgvetlel',
            altitude_hi=int(18),
            altitude_low=int(80),
            movement_dir='bcsiyrrlajlnvrqtqfih',
            movement_spd='gpyaknqotkqarxogshcj',
            severity=int(20),
            raw_sigmet='udncwovvmytwbpdcagxj',
            coords='zgwqqhvvmtdxvijoncbb',
            sigmet_id='xyffbhgsolkhgctvdidk',
            region='xtsqnqbovibxkbyptqsi'
        )
        return instance

    
    def test_icao_id_property(self):
        """
        Test icao_id property
        """
        test_value = 'acjacvbmrxdgymqkmsjq'
        self.instance.icao_id = test_value
        self.assertEqual(self.instance.icao_id, test_value)
    
    def test_series_id_property(self):
        """
        Test series_id property
        """
        test_value = 'tjtlkjbdegovzzgagibs'
        self.instance.series_id = test_value
        self.assertEqual(self.instance.series_id, test_value)
    
    def test_valid_time_from_property(self):
        """
        Test valid_time_from property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.valid_time_from = test_value
        self.assertEqual(self.instance.valid_time_from, test_value)
    
    def test_valid_time_to_property(self):
        """
        Test valid_time_to property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.valid_time_to = test_value
        self.assertEqual(self.instance.valid_time_to, test_value)
    
    def test_hazard_property(self):
        """
        Test hazard property
        """
        test_value = 'yxdmglnipsybowrrtjlc'
        self.instance.hazard = test_value
        self.assertEqual(self.instance.hazard, test_value)
    
    def test_qualifier_property(self):
        """
        Test qualifier property
        """
        test_value = 'cikskzmyyptkttafxibh'
        self.instance.qualifier = test_value
        self.assertEqual(self.instance.qualifier, test_value)
    
    def test_sigmet_type_property(self):
        """
        Test sigmet_type property
        """
        test_value = 'jhaiayhvxowdsgvetlel'
        self.instance.sigmet_type = test_value
        self.assertEqual(self.instance.sigmet_type, test_value)
    
    def test_altitude_hi_property(self):
        """
        Test altitude_hi property
        """
        test_value = int(18)
        self.instance.altitude_hi = test_value
        self.assertEqual(self.instance.altitude_hi, test_value)
    
    def test_altitude_low_property(self):
        """
        Test altitude_low property
        """
        test_value = int(80)
        self.instance.altitude_low = test_value
        self.assertEqual(self.instance.altitude_low, test_value)
    
    def test_movement_dir_property(self):
        """
        Test movement_dir property
        """
        test_value = 'bcsiyrrlajlnvrqtqfih'
        self.instance.movement_dir = test_value
        self.assertEqual(self.instance.movement_dir, test_value)
    
    def test_movement_spd_property(self):
        """
        Test movement_spd property
        """
        test_value = 'gpyaknqotkqarxogshcj'
        self.instance.movement_spd = test_value
        self.assertEqual(self.instance.movement_spd, test_value)
    
    def test_severity_property(self):
        """
        Test severity property
        """
        test_value = int(20)
        self.instance.severity = test_value
        self.assertEqual(self.instance.severity, test_value)
    
    def test_raw_sigmet_property(self):
        """
        Test raw_sigmet property
        """
        test_value = 'udncwovvmytwbpdcagxj'
        self.instance.raw_sigmet = test_value
        self.assertEqual(self.instance.raw_sigmet, test_value)
    
    def test_coords_property(self):
        """
        Test coords property
        """
        test_value = 'zgwqqhvvmtdxvijoncbb'
        self.instance.coords = test_value
        self.assertEqual(self.instance.coords, test_value)
    
    def test_sigmet_id_property(self):
        """
        Test sigmet_id property
        """
        test_value = 'xyffbhgsolkhgctvdidk'
        self.instance.sigmet_id = test_value
        self.assertEqual(self.instance.sigmet_id, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'xtsqnqbovibxkbyptqsi'
        self.instance.region = test_value
        self.assertEqual(self.instance.region, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Sigmet.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Sigmet.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

