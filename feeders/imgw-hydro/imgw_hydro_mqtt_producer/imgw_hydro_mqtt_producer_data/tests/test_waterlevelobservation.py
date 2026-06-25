"""
Test case for WaterLevelObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from imgw_hydro_mqtt_producer_data.waterlevelobservation import WaterLevelObservation
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
            station_id='spygqxtraigpdccoyvyx',
            station_name='vzezyqlrewktobwmfjui',
            river='hsydtnrofhumelchjpah',
            voivodeship='jsenrhgsecrtbijpcuyn',
            water_level=float(92.03979288159542),
            water_level_timestamp=datetime.datetime.now(datetime.timezone.utc),
            water_temperature=float(0.9674221374644132),
            water_temperature_timestamp=datetime.datetime.now(datetime.timezone.utc),
            discharge=float(16.674484240497677),
            discharge_timestamp=datetime.datetime.now(datetime.timezone.utc),
            ice_phenomenon_code='kwuzctxnavdrcfowexsn',
            overgrowth_code='edjphznfakdpbhbhkbif',
            basin='iopktuzzhaycaycbgldm'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'spygqxtraigpdccoyvyx'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'vzezyqlrewktobwmfjui'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_river_property(self):
        """
        Test river property
        """
        test_value = 'hsydtnrofhumelchjpah'
        self.instance.river = test_value
        self.assertEqual(self.instance.river, test_value)
    
    def test_voivodeship_property(self):
        """
        Test voivodeship property
        """
        test_value = 'jsenrhgsecrtbijpcuyn'
        self.instance.voivodeship = test_value
        self.assertEqual(self.instance.voivodeship, test_value)
    
    def test_water_level_property(self):
        """
        Test water_level property
        """
        test_value = float(92.03979288159542)
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
        test_value = float(0.9674221374644132)
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
        test_value = float(16.674484240497677)
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
        test_value = 'kwuzctxnavdrcfowexsn'
        self.instance.ice_phenomenon_code = test_value
        self.assertEqual(self.instance.ice_phenomenon_code, test_value)
    
    def test_overgrowth_code_property(self):
        """
        Test overgrowth_code property
        """
        test_value = 'edjphznfakdpbhbhkbif'
        self.instance.overgrowth_code = test_value
        self.assertEqual(self.instance.overgrowth_code, test_value)
    
    def test_basin_property(self):
        """
        Test basin property
        """
        test_value = 'iopktuzzhaycaycbgldm'
        self.instance.basin = test_value
        self.assertEqual(self.instance.basin, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = WaterLevelObservation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = WaterLevelObservation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

