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
            station_id='bhiizrbuptgcsflnhqzd',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            depth=float(7.805589168615712),
            ocean_temperature=float(50.30981030452146),
            conductivity=float(91.44941457802659),
            salinity=float(55.8695719958839),
            oxygen_saturation=float(8.809905095287608),
            oxygen_concentration=float(43.86656408997946),
            chlorophyll_concentration=float(94.28566877847095),
            turbidity=float(4.251770786756448),
            ph=float(40.15590283558507),
            redox_potential=float(93.94246150150397)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'bhiizrbuptgcsflnhqzd'
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
        test_value = float(7.805589168615712)
        self.instance.depth = test_value
        self.assertEqual(self.instance.depth, test_value)
    
    def test_ocean_temperature_property(self):
        """
        Test ocean_temperature property
        """
        test_value = float(50.30981030452146)
        self.instance.ocean_temperature = test_value
        self.assertEqual(self.instance.ocean_temperature, test_value)
    
    def test_conductivity_property(self):
        """
        Test conductivity property
        """
        test_value = float(91.44941457802659)
        self.instance.conductivity = test_value
        self.assertEqual(self.instance.conductivity, test_value)
    
    def test_salinity_property(self):
        """
        Test salinity property
        """
        test_value = float(55.8695719958839)
        self.instance.salinity = test_value
        self.assertEqual(self.instance.salinity, test_value)
    
    def test_oxygen_saturation_property(self):
        """
        Test oxygen_saturation property
        """
        test_value = float(8.809905095287608)
        self.instance.oxygen_saturation = test_value
        self.assertEqual(self.instance.oxygen_saturation, test_value)
    
    def test_oxygen_concentration_property(self):
        """
        Test oxygen_concentration property
        """
        test_value = float(43.86656408997946)
        self.instance.oxygen_concentration = test_value
        self.assertEqual(self.instance.oxygen_concentration, test_value)
    
    def test_chlorophyll_concentration_property(self):
        """
        Test chlorophyll_concentration property
        """
        test_value = float(94.28566877847095)
        self.instance.chlorophyll_concentration = test_value
        self.assertEqual(self.instance.chlorophyll_concentration, test_value)
    
    def test_turbidity_property(self):
        """
        Test turbidity property
        """
        test_value = float(4.251770786756448)
        self.instance.turbidity = test_value
        self.assertEqual(self.instance.turbidity, test_value)
    
    def test_ph_property(self):
        """
        Test ph property
        """
        test_value = float(40.15590283558507)
        self.instance.ph = test_value
        self.assertEqual(self.instance.ph, test_value)
    
    def test_redox_potential_property(self):
        """
        Test redox_potential property
        """
        test_value = float(93.94246150150397)
        self.instance.redox_potential = test_value
        self.assertEqual(self.instance.redox_potential, test_value)
    
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

