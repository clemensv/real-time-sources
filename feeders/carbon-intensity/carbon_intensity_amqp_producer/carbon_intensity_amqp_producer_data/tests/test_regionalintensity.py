"""
Test case for RegionalIntensity
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from carbon_intensity_amqp_producer_data.regionalintensity import RegionalIntensity
import datetime


class Test_RegionalIntensity(unittest.TestCase):
    """
    Test case for RegionalIntensity
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_RegionalIntensity.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of RegionalIntensity for testing
        """
        instance = RegionalIntensity(
            region_id=int(34),
            dnoregion='obmupycjezyqigmputdd',
            shortname='ytequkzaulnprxdgovgo',
            period_from=datetime.datetime.now(datetime.timezone.utc),
            period_to=datetime.datetime.now(datetime.timezone.utc),
            forecast=int(2),
            index='pvxxsrdssdmrlkgrlngy',
            biomass_pct=float(12.64137134417106),
            coal_pct=float(16.121282580056473),
            gas_pct=float(21.06708258031188),
            hydro_pct=float(6.7771881997414685),
            imports_pct=float(65.79080430743613),
            nuclear_pct=float(53.2211839401177),
            oil_pct=float(8.397964171047267),
            other_pct=float(15.597636694590221),
            solar_pct=float(35.04097884169831),
            wind_pct=float(43.78355864915772),
            region='xvolpbftytokyanvfsgh',
            ce_id='uoelixtrgzndielienrg'
        )
        return instance

    
    def test_region_id_property(self):
        """
        Test region_id property
        """
        test_value = int(34)
        self.instance.region_id = test_value
        self.assertEqual(self.instance.region_id, test_value)
    
    def test_dnoregion_property(self):
        """
        Test dnoregion property
        """
        test_value = 'obmupycjezyqigmputdd'
        self.instance.dnoregion = test_value
        self.assertEqual(self.instance.dnoregion, test_value)
    
    def test_shortname_property(self):
        """
        Test shortname property
        """
        test_value = 'ytequkzaulnprxdgovgo'
        self.instance.shortname = test_value
        self.assertEqual(self.instance.shortname, test_value)
    
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
    
    def test_forecast_property(self):
        """
        Test forecast property
        """
        test_value = int(2)
        self.instance.forecast = test_value
        self.assertEqual(self.instance.forecast, test_value)
    
    def test_index_property(self):
        """
        Test index property
        """
        test_value = 'pvxxsrdssdmrlkgrlngy'
        self.instance.index = test_value
        self.assertEqual(self.instance.index, test_value)
    
    def test_biomass_pct_property(self):
        """
        Test biomass_pct property
        """
        test_value = float(12.64137134417106)
        self.instance.biomass_pct = test_value
        self.assertEqual(self.instance.biomass_pct, test_value)
    
    def test_coal_pct_property(self):
        """
        Test coal_pct property
        """
        test_value = float(16.121282580056473)
        self.instance.coal_pct = test_value
        self.assertEqual(self.instance.coal_pct, test_value)
    
    def test_gas_pct_property(self):
        """
        Test gas_pct property
        """
        test_value = float(21.06708258031188)
        self.instance.gas_pct = test_value
        self.assertEqual(self.instance.gas_pct, test_value)
    
    def test_hydro_pct_property(self):
        """
        Test hydro_pct property
        """
        test_value = float(6.7771881997414685)
        self.instance.hydro_pct = test_value
        self.assertEqual(self.instance.hydro_pct, test_value)
    
    def test_imports_pct_property(self):
        """
        Test imports_pct property
        """
        test_value = float(65.79080430743613)
        self.instance.imports_pct = test_value
        self.assertEqual(self.instance.imports_pct, test_value)
    
    def test_nuclear_pct_property(self):
        """
        Test nuclear_pct property
        """
        test_value = float(53.2211839401177)
        self.instance.nuclear_pct = test_value
        self.assertEqual(self.instance.nuclear_pct, test_value)
    
    def test_oil_pct_property(self):
        """
        Test oil_pct property
        """
        test_value = float(8.397964171047267)
        self.instance.oil_pct = test_value
        self.assertEqual(self.instance.oil_pct, test_value)
    
    def test_other_pct_property(self):
        """
        Test other_pct property
        """
        test_value = float(15.597636694590221)
        self.instance.other_pct = test_value
        self.assertEqual(self.instance.other_pct, test_value)
    
    def test_solar_pct_property(self):
        """
        Test solar_pct property
        """
        test_value = float(35.04097884169831)
        self.instance.solar_pct = test_value
        self.assertEqual(self.instance.solar_pct, test_value)
    
    def test_wind_pct_property(self):
        """
        Test wind_pct property
        """
        test_value = float(43.78355864915772)
        self.instance.wind_pct = test_value
        self.assertEqual(self.instance.wind_pct, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'xvolpbftytokyanvfsgh'
        self.instance.region = test_value
        self.assertEqual(self.instance.region, test_value)
    
    def test_ce_id_property(self):
        """
        Test ce_id property
        """
        test_value = 'uoelixtrgzndielienrg'
        self.instance.ce_id = test_value
        self.assertEqual(self.instance.ce_id, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = RegionalIntensity.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = RegionalIntensity.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

