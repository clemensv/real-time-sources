"""
Test case for GoesProtonFlux
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_goes_producer_data.microsoft.opendata.us.noaa.swpc.goesprotonflux import GoesProtonFlux


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
            time_tag='gfvkjufpztlbvtfrietn',
            satellite=int(23),
            flux=float(9.760774737463318),
            energy='rmrvnynhdpadazkmmivm'
        )
        return instance

    
    def test_time_tag_property(self):
        """
        Test time_tag property
        """
        test_value = 'gfvkjufpztlbvtfrietn'
        self.instance.time_tag = test_value
        self.assertEqual(self.instance.time_tag, test_value)
    
    def test_satellite_property(self):
        """
        Test satellite property
        """
        test_value = int(23)
        self.instance.satellite = test_value
        self.assertEqual(self.instance.satellite, test_value)
    
    def test_flux_property(self):
        """
        Test flux property
        """
        test_value = float(9.760774737463318)
        self.instance.flux = test_value
        self.assertEqual(self.instance.flux, test_value)
    
    def test_energy_property(self):
        """
        Test energy property
        """
        test_value = 'rmrvnynhdpadazkmmivm'
        self.instance.energy = test_value
        self.assertEqual(self.instance.energy, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = GoesProtonFlux.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
