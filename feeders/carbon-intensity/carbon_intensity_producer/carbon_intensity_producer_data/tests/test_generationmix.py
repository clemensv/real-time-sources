"""
Test case for GenerationMix
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from carbon_intensity_producer_data.generationmix import GenerationMix
import datetime


class Test_GenerationMix(unittest.TestCase):
    """
    Test case for GenerationMix
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_GenerationMix.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of GenerationMix for testing
        """
        instance = GenerationMix(
            period_from=datetime.datetime.now(datetime.timezone.utc),
            period_to=datetime.datetime.now(datetime.timezone.utc),
            biomass_pct=float(53.27921957075665),
            coal_pct=float(91.17646445687274),
            gas_pct=float(17.782359973529115),
            hydro_pct=float(97.9633387546917),
            imports_pct=float(39.48848974791995),
            nuclear_pct=float(17.14762789059031),
            oil_pct=float(87.47183302941714),
            other_pct=float(98.91094833314264),
            solar_pct=float(57.05245486297672),
            wind_pct=float(44.574062634671975),
            region='slkzxbhbilmrqnzeproz',
            ce_id='kszqfwblumaqxttxnwwv'
        )
        return instance

    
    def test_period_from_property(self):
        """
        Test period_from property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.period_from = test_value
        self.assertEqual(self.instance.period_from, test_value)
    
    def test_period_to_property(self):
        """
        Test period_to property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.period_to = test_value
        self.assertEqual(self.instance.period_to, test_value)
    
    def test_biomass_pct_property(self):
        """
        Test biomass_pct property
        """
        test_value = float(53.27921957075665)
        self.instance.biomass_pct = test_value
        self.assertEqual(self.instance.biomass_pct, test_value)
    
    def test_coal_pct_property(self):
        """
        Test coal_pct property
        """
        test_value = float(91.17646445687274)
        self.instance.coal_pct = test_value
        self.assertEqual(self.instance.coal_pct, test_value)
    
    def test_gas_pct_property(self):
        """
        Test gas_pct property
        """
        test_value = float(17.782359973529115)
        self.instance.gas_pct = test_value
        self.assertEqual(self.instance.gas_pct, test_value)
    
    def test_hydro_pct_property(self):
        """
        Test hydro_pct property
        """
        test_value = float(97.9633387546917)
        self.instance.hydro_pct = test_value
        self.assertEqual(self.instance.hydro_pct, test_value)
    
    def test_imports_pct_property(self):
        """
        Test imports_pct property
        """
        test_value = float(39.48848974791995)
        self.instance.imports_pct = test_value
        self.assertEqual(self.instance.imports_pct, test_value)
    
    def test_nuclear_pct_property(self):
        """
        Test nuclear_pct property
        """
        test_value = float(17.14762789059031)
        self.instance.nuclear_pct = test_value
        self.assertEqual(self.instance.nuclear_pct, test_value)
    
    def test_oil_pct_property(self):
        """
        Test oil_pct property
        """
        test_value = float(87.47183302941714)
        self.instance.oil_pct = test_value
        self.assertEqual(self.instance.oil_pct, test_value)
    
    def test_other_pct_property(self):
        """
        Test other_pct property
        """
        test_value = float(98.91094833314264)
        self.instance.other_pct = test_value
        self.assertEqual(self.instance.other_pct, test_value)
    
    def test_solar_pct_property(self):
        """
        Test solar_pct property
        """
        test_value = float(57.05245486297672)
        self.instance.solar_pct = test_value
        self.assertEqual(self.instance.solar_pct, test_value)
    
    def test_wind_pct_property(self):
        """
        Test wind_pct property
        """
        test_value = float(44.574062634671975)
        self.instance.wind_pct = test_value
        self.assertEqual(self.instance.wind_pct, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'slkzxbhbilmrqnzeproz'
        self.instance.region = test_value
        self.assertEqual(self.instance.region, test_value)
    
    def test_ce_id_property(self):
        """
        Test ce_id property
        """
        test_value = 'kszqfwblumaqxttxnwwv'
        self.instance.ce_id = test_value
        self.assertEqual(self.instance.ce_id, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = GenerationMix.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = GenerationMix.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

