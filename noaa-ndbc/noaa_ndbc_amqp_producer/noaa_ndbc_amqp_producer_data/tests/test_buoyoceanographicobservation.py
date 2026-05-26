"""
Test case for BuoyOceanographicObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_ndbc_amqp_producer_data.buoyoceanographicobservation import BuoyOceanographicObservation
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
            station_id='aeyvitwrhzvgyjzporqp',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            depth=float(13.032565367932857),
            ocean_temperature=float(59.76669548819454),
            conductivity=float(81.97292102571669),
            salinity=float(69.55220128578084),
            oxygen_saturation=float(4.787484286867516),
            oxygen_concentration=float(11.146918214061674),
            chlorophyll_concentration=float(95.12630897461518),
            turbidity=float(78.60366190779868),
            ph=float(98.50338441298538),
            redox_potential=float(19.386415431727897),
            region='txnwqeyzclkiwcuaduwu'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'aeyvitwrhzvgyjzporqp'
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
        test_value = float(13.032565367932857)
        self.instance.depth = test_value
        self.assertEqual(self.instance.depth, test_value)
    
    def test_ocean_temperature_property(self):
        """
        Test ocean_temperature property
        """
        test_value = float(59.76669548819454)
        self.instance.ocean_temperature = test_value
        self.assertEqual(self.instance.ocean_temperature, test_value)
    
    def test_conductivity_property(self):
        """
        Test conductivity property
        """
        test_value = float(81.97292102571669)
        self.instance.conductivity = test_value
        self.assertEqual(self.instance.conductivity, test_value)
    
    def test_salinity_property(self):
        """
        Test salinity property
        """
        test_value = float(69.55220128578084)
        self.instance.salinity = test_value
        self.assertEqual(self.instance.salinity, test_value)
    
    def test_oxygen_saturation_property(self):
        """
        Test oxygen_saturation property
        """
        test_value = float(4.787484286867516)
        self.instance.oxygen_saturation = test_value
        self.assertEqual(self.instance.oxygen_saturation, test_value)
    
    def test_oxygen_concentration_property(self):
        """
        Test oxygen_concentration property
        """
        test_value = float(11.146918214061674)
        self.instance.oxygen_concentration = test_value
        self.assertEqual(self.instance.oxygen_concentration, test_value)
    
    def test_chlorophyll_concentration_property(self):
        """
        Test chlorophyll_concentration property
        """
        test_value = float(95.12630897461518)
        self.instance.chlorophyll_concentration = test_value
        self.assertEqual(self.instance.chlorophyll_concentration, test_value)
    
    def test_turbidity_property(self):
        """
        Test turbidity property
        """
        test_value = float(78.60366190779868)
        self.instance.turbidity = test_value
        self.assertEqual(self.instance.turbidity, test_value)
    
    def test_ph_property(self):
        """
        Test ph property
        """
        test_value = float(98.50338441298538)
        self.instance.ph = test_value
        self.assertEqual(self.instance.ph, test_value)
    
    def test_redox_potential_property(self):
        """
        Test redox_potential property
        """
        test_value = float(19.386415431727897)
        self.instance.redox_potential = test_value
        self.assertEqual(self.instance.redox_potential, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'txnwqeyzclkiwcuaduwu'
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

