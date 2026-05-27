"""
Test case for RegionalIntensity
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from carbon_intensity_mqtt_producer_data.regionalintensity import RegionalIntensity
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
            region_id=int(31),
            dnoregion='simzkooxcyjvutsoovpj',
            shortname='sdyiwwdkfhwbozmedelr',
            period_from=datetime.datetime.now(datetime.timezone.utc),
            period_to=datetime.datetime.now(datetime.timezone.utc),
            forecast=int(87),
            index='ypyevksujbtmcbucqtcs',
            biomass_pct=float(55.38724574723686),
            coal_pct=float(20.46978442376298),
            gas_pct=float(46.35638152902701),
            hydro_pct=float(88.68326772109164),
            imports_pct=float(28.584075638719586),
            nuclear_pct=float(28.800043262683705),
            oil_pct=float(61.85474829792359),
            other_pct=float(9.282861163137213),
            solar_pct=float(79.65578219851558),
            wind_pct=float(58.00038442101142),
            region='qpwufscfvhfcoqmkkrqi',
            ce_id='dybeaasjqmeryagibynp'
        )
        return instance

    
    def test_region_id_property(self):
        """
        Test region_id property
        """
        test_value = int(31)
        self.instance.region_id = test_value
        self.assertEqual(self.instance.region_id, test_value)
    
    def test_dnoregion_property(self):
        """
        Test dnoregion property
        """
        test_value = 'simzkooxcyjvutsoovpj'
        self.instance.dnoregion = test_value
        self.assertEqual(self.instance.dnoregion, test_value)
    
    def test_shortname_property(self):
        """
        Test shortname property
        """
        test_value = 'sdyiwwdkfhwbozmedelr'
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
        test_value = int(87)
        self.instance.forecast = test_value
        self.assertEqual(self.instance.forecast, test_value)
    
    def test_index_property(self):
        """
        Test index property
        """
        test_value = 'ypyevksujbtmcbucqtcs'
        self.instance.index = test_value
        self.assertEqual(self.instance.index, test_value)
    
    def test_biomass_pct_property(self):
        """
        Test biomass_pct property
        """
        test_value = float(55.38724574723686)
        self.instance.biomass_pct = test_value
        self.assertEqual(self.instance.biomass_pct, test_value)
    
    def test_coal_pct_property(self):
        """
        Test coal_pct property
        """
        test_value = float(20.46978442376298)
        self.instance.coal_pct = test_value
        self.assertEqual(self.instance.coal_pct, test_value)
    
    def test_gas_pct_property(self):
        """
        Test gas_pct property
        """
        test_value = float(46.35638152902701)
        self.instance.gas_pct = test_value
        self.assertEqual(self.instance.gas_pct, test_value)
    
    def test_hydro_pct_property(self):
        """
        Test hydro_pct property
        """
        test_value = float(88.68326772109164)
        self.instance.hydro_pct = test_value
        self.assertEqual(self.instance.hydro_pct, test_value)
    
    def test_imports_pct_property(self):
        """
        Test imports_pct property
        """
        test_value = float(28.584075638719586)
        self.instance.imports_pct = test_value
        self.assertEqual(self.instance.imports_pct, test_value)
    
    def test_nuclear_pct_property(self):
        """
        Test nuclear_pct property
        """
        test_value = float(28.800043262683705)
        self.instance.nuclear_pct = test_value
        self.assertEqual(self.instance.nuclear_pct, test_value)
    
    def test_oil_pct_property(self):
        """
        Test oil_pct property
        """
        test_value = float(61.85474829792359)
        self.instance.oil_pct = test_value
        self.assertEqual(self.instance.oil_pct, test_value)
    
    def test_other_pct_property(self):
        """
        Test other_pct property
        """
        test_value = float(9.282861163137213)
        self.instance.other_pct = test_value
        self.assertEqual(self.instance.other_pct, test_value)
    
    def test_solar_pct_property(self):
        """
        Test solar_pct property
        """
        test_value = float(79.65578219851558)
        self.instance.solar_pct = test_value
        self.assertEqual(self.instance.solar_pct, test_value)
    
    def test_wind_pct_property(self):
        """
        Test wind_pct property
        """
        test_value = float(58.00038442101142)
        self.instance.wind_pct = test_value
        self.assertEqual(self.instance.wind_pct, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'qpwufscfvhfcoqmkkrqi'
        self.instance.region = test_value
        self.assertEqual(self.instance.region, test_value)
    
    def test_ce_id_property(self):
        """
        Test ce_id property
        """
        test_value = 'dybeaasjqmeryagibynp'
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

