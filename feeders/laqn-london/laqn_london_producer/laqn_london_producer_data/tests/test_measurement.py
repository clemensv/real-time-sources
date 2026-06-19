"""
Test case for Measurement
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from laqn_london_producer_data.uk.kcl.laqn.measurement import Measurement


class Test_Measurement(unittest.TestCase):
    """
    Test case for Measurement
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Measurement.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Measurement for testing
        """
        instance = Measurement(
            site_code='dzvgnbsjifjgfevlpedl',
            species_code='uvbxjdunofrfabsrmfvc',
            measurement_date_gmt='hjtsohrewminibqapxam',
            value=float(98.57147101953458)
        )
        return instance

    
    def test_site_code_property(self):
        """
        Test site_code property
        """
        test_value = 'dzvgnbsjifjgfevlpedl'
        self.instance.site_code = test_value
        self.assertEqual(self.instance.site_code, test_value)
    
    def test_species_code_property(self):
        """
        Test species_code property
        """
        test_value = 'uvbxjdunofrfabsrmfvc'
        self.instance.species_code = test_value
        self.assertEqual(self.instance.species_code, test_value)
    
    def test_measurement_date_gmt_property(self):
        """
        Test measurement_date_gmt property
        """
        test_value = 'hjtsohrewminibqapxam'
        self.instance.measurement_date_gmt = test_value
        self.assertEqual(self.instance.measurement_date_gmt, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(98.57147101953458)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Measurement.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Measurement.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

