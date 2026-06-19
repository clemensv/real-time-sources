"""
Test case for BuoyOceanographicObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_ndbc_producer_data.buoyoceanographicobservation import BuoyOceanographicObservation
import datetime


class Test_BuoyOceanographicObservation(unittest.TestCase):
    """
    Test case for BuoyOceanographicObservation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_BuoyOceanographicObservation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of BuoyOceanographicObservation for testing
        """
        instance = BuoyOceanographicObservation(
            station_id='nwtiivaoxbfnetykhriu',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            depth=float(17.131655911089638),
            ocean_temperature=float(42.11007531083351),
            conductivity=float(15.039942863881063),
            salinity=float(82.85306304815167),
            oxygen_saturation=float(24.532960556700722),
            oxygen_concentration=float(4.881752250504934),
            chlorophyll_concentration=float(76.12659854397552),
            turbidity=float(83.25517842626053),
            ph=float(54.11703436947217),
            redox_potential=float(41.262747118388766),
            region='iuvpqmykizoeftcjhfhb'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'nwtiivaoxbfnetykhriu'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_depth_property(self):
        """
        Test depth property
        """
        test_value = float(17.131655911089638)
        self.instance.depth = test_value
        self.assertEqual(self.instance.depth, test_value)
    
    def test_ocean_temperature_property(self):
        """
        Test ocean_temperature property
        """
        test_value = float(42.11007531083351)
        self.instance.ocean_temperature = test_value
        self.assertEqual(self.instance.ocean_temperature, test_value)
    
    def test_conductivity_property(self):
        """
        Test conductivity property
        """
        test_value = float(15.039942863881063)
        self.instance.conductivity = test_value
        self.assertEqual(self.instance.conductivity, test_value)
    
    def test_salinity_property(self):
        """
        Test salinity property
        """
        test_value = float(82.85306304815167)
        self.instance.salinity = test_value
        self.assertEqual(self.instance.salinity, test_value)
    
    def test_oxygen_saturation_property(self):
        """
        Test oxygen_saturation property
        """
        test_value = float(24.532960556700722)
        self.instance.oxygen_saturation = test_value
        self.assertEqual(self.instance.oxygen_saturation, test_value)
    
    def test_oxygen_concentration_property(self):
        """
        Test oxygen_concentration property
        """
        test_value = float(4.881752250504934)
        self.instance.oxygen_concentration = test_value
        self.assertEqual(self.instance.oxygen_concentration, test_value)
    
    def test_chlorophyll_concentration_property(self):
        """
        Test chlorophyll_concentration property
        """
        test_value = float(76.12659854397552)
        self.instance.chlorophyll_concentration = test_value
        self.assertEqual(self.instance.chlorophyll_concentration, test_value)
    
    def test_turbidity_property(self):
        """
        Test turbidity property
        """
        test_value = float(83.25517842626053)
        self.instance.turbidity = test_value
        self.assertEqual(self.instance.turbidity, test_value)
    
    def test_ph_property(self):
        """
        Test ph property
        """
        test_value = float(54.11703436947217)
        self.instance.ph = test_value
        self.assertEqual(self.instance.ph, test_value)
    
    def test_redox_potential_property(self):
        """
        Test redox_potential property
        """
        test_value = float(41.262747118388766)
        self.instance.redox_potential = test_value
        self.assertEqual(self.instance.redox_potential, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'iuvpqmykizoeftcjhfhb'
        self.instance.region = test_value
        self.assertEqual(self.instance.region, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = BuoyOceanographicObservation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = BuoyOceanographicObservation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

