"""
Test case for GoesProtonFlux
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_goes_producer_data.goesprotonflux import GoesProtonFlux


class Test_GoesProtonFlux(unittest.TestCase):
    """
    Test case for GoesProtonFlux
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_GoesProtonFlux.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of GoesProtonFlux for testing
        """
        instance = GoesProtonFlux(
            time_tag='lizreerjtmyvrlasdzbc',
            satellite=int(75),
            flux=float(35.63744142334965),
            energy='vodyncfpexndgdcoctpv'
        )
        return instance

    
    def test_time_tag_property(self):
        """
        Test time_tag property
        """
        test_value = 'lizreerjtmyvrlasdzbc'
        self.instance.time_tag = test_value
        self.assertEqual(self.instance.time_tag, test_value)
    
    def test_satellite_property(self):
        """
        Test satellite property
        """
        test_value = int(75)
        self.instance.satellite = test_value
        self.assertEqual(self.instance.satellite, test_value)
    
    def test_flux_property(self):
        """
        Test flux property
        """
        test_value = float(35.63744142334965)
        self.instance.flux = test_value
        self.assertEqual(self.instance.flux, test_value)
    
    def test_energy_property(self):
        """
        Test energy property
        """
        test_value = 'vodyncfpexndgdcoctpv'
        self.instance.energy = test_value
        self.assertEqual(self.instance.energy, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = GoesProtonFlux.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = GoesProtonFlux.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

