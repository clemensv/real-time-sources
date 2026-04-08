"""
Test case for BuoyOceanographicObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_ndbc_producer_data.microsoft.opendata.us.noaa.ndbc.buoyoceanographicobservation import BuoyOceanographicObservation
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
            station_id='pvwcnomyvhgczqbesvoo',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            depth=float(11.816667638927758),
            ocean_temperature=float(59.19990759614577),
            conductivity=float(73.73197671649518),
            salinity=float(63.380092690828796),
            oxygen_saturation=float(1.942601309133074),
            oxygen_concentration=float(91.06756945991845),
            chlorophyll_concentration=float(91.72297864158938),
            turbidity=float(7.515675205934902),
            ph=float(55.22682419535357),
            redox_potential=float(4.242893077268317)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'pvwcnomyvhgczqbesvoo'
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
        test_value = float(11.816667638927758)
        self.instance.depth = test_value
        self.assertEqual(self.instance.depth, test_value)
    
    def test_ocean_temperature_property(self):
        """
        Test ocean_temperature property
        """
        test_value = float(59.19990759614577)
        self.instance.ocean_temperature = test_value
        self.assertEqual(self.instance.ocean_temperature, test_value)
    
    def test_conductivity_property(self):
        """
        Test conductivity property
        """
        test_value = float(73.73197671649518)
        self.instance.conductivity = test_value
        self.assertEqual(self.instance.conductivity, test_value)
    
    def test_salinity_property(self):
        """
        Test salinity property
        """
        test_value = float(63.380092690828796)
        self.instance.salinity = test_value
        self.assertEqual(self.instance.salinity, test_value)
    
    def test_oxygen_saturation_property(self):
        """
        Test oxygen_saturation property
        """
        test_value = float(1.942601309133074)
        self.instance.oxygen_saturation = test_value
        self.assertEqual(self.instance.oxygen_saturation, test_value)
    
    def test_oxygen_concentration_property(self):
        """
        Test oxygen_concentration property
        """
        test_value = float(91.06756945991845)
        self.instance.oxygen_concentration = test_value
        self.assertEqual(self.instance.oxygen_concentration, test_value)
    
    def test_chlorophyll_concentration_property(self):
        """
        Test chlorophyll_concentration property
        """
        test_value = float(91.72297864158938)
        self.instance.chlorophyll_concentration = test_value
        self.assertEqual(self.instance.chlorophyll_concentration, test_value)
    
    def test_turbidity_property(self):
        """
        Test turbidity property
        """
        test_value = float(7.515675205934902)
        self.instance.turbidity = test_value
        self.assertEqual(self.instance.turbidity, test_value)
    
    def test_ph_property(self):
        """
        Test ph property
        """
        test_value = float(55.22682419535357)
        self.instance.ph = test_value
        self.assertEqual(self.instance.ph, test_value)
    
    def test_redox_potential_property(self):
        """
        Test redox_potential property
        """
        test_value = float(4.242893077268317)
        self.instance.redox_potential = test_value
        self.assertEqual(self.instance.redox_potential, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = BuoyOceanographicObservation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
