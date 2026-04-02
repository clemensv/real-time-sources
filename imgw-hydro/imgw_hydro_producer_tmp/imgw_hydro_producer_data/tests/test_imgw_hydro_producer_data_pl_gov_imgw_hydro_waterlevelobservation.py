"""
Test case for WaterLevelObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from imgw_hydro_producer_data.pl.gov.imgw.hydro.waterlevelobservation import WaterLevelObservation
import datetime


class Test_WaterLevelObservation(unittest.TestCase):
    """
    Test case for WaterLevelObservation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_WaterLevelObservation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of WaterLevelObservation for testing
        """
        instance = WaterLevelObservation(
            station_id='ygyeeydyzrfslizoemej',
            station_name='ztulrbkzqzqfhvbbmsaj',
            river='dhonqioihntwlekhyepv',
            voivodeship='uipougjhaknupvgfiycn',
            water_level=float(74.54740000402174),
            water_level_timestamp=datetime.datetime.now(datetime.timezone.utc),
            water_temperature=float(84.86381640688678),
            water_temperature_timestamp=datetime.datetime.now(datetime.timezone.utc),
            discharge=float(47.24039482052091),
            discharge_timestamp=datetime.datetime.now(datetime.timezone.utc),
            ice_phenomenon_code='kztsjktjmdyynslphpiz',
            overgrowth_code='xfzotitjuhavcdlixvqv'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'ygyeeydyzrfslizoemej'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'ztulrbkzqzqfhvbbmsaj'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_river_property(self):
        """
        Test river property
        """
        test_value = 'dhonqioihntwlekhyepv'
        self.instance.river = test_value
        self.assertEqual(self.instance.river, test_value)
    
    def test_voivodeship_property(self):
        """
        Test voivodeship property
        """
        test_value = 'uipougjhaknupvgfiycn'
        self.instance.voivodeship = test_value
        self.assertEqual(self.instance.voivodeship, test_value)
    
    def test_water_level_property(self):
        """
        Test water_level property
        """
        test_value = float(74.54740000402174)
        self.instance.water_level = test_value
        self.assertEqual(self.instance.water_level, test_value)
    
    def test_water_level_timestamp_property(self):
        """
        Test water_level_timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.water_level_timestamp = test_value
        self.assertEqual(self.instance.water_level_timestamp, test_value)
    
    def test_water_temperature_property(self):
        """
        Test water_temperature property
        """
        test_value = float(84.86381640688678)
        self.instance.water_temperature = test_value
        self.assertEqual(self.instance.water_temperature, test_value)
    
    def test_water_temperature_timestamp_property(self):
        """
        Test water_temperature_timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.water_temperature_timestamp = test_value
        self.assertEqual(self.instance.water_temperature_timestamp, test_value)
    
    def test_discharge_property(self):
        """
        Test discharge property
        """
        test_value = float(47.24039482052091)
        self.instance.discharge = test_value
        self.assertEqual(self.instance.discharge, test_value)
    
    def test_discharge_timestamp_property(self):
        """
        Test discharge_timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.discharge_timestamp = test_value
        self.assertEqual(self.instance.discharge_timestamp, test_value)
    
    def test_ice_phenomenon_code_property(self):
        """
        Test ice_phenomenon_code property
        """
        test_value = 'kztsjktjmdyynslphpiz'
        self.instance.ice_phenomenon_code = test_value
        self.assertEqual(self.instance.ice_phenomenon_code, test_value)
    
    def test_overgrowth_code_property(self):
        """
        Test overgrowth_code property
        """
        test_value = 'xfzotitjuhavcdlixvqv'
        self.instance.overgrowth_code = test_value
        self.assertEqual(self.instance.overgrowth_code, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = WaterLevelObservation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
