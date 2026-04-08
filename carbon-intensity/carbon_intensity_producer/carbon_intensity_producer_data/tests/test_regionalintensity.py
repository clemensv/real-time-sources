"""
Test case for RegionalIntensity
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from carbon_intensity_producer_data.regionalintensity import RegionalIntensity
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
            region_id=int(59),
            dnoregion='jvjketbtxznkqmtsoiwz',
            shortname='oomtsrqfhzvoqpynixay',
            period_from=datetime.datetime.now(datetime.timezone.utc),
            period_to=datetime.datetime.now(datetime.timezone.utc),
            forecast=int(80),
            index='cjoinlsljldkwpctxtzd',
            biomass_pct=float(95.1495646246595),
            coal_pct=float(50.77925060176531),
            gas_pct=float(38.56349366426958),
            hydro_pct=float(7.715821078802554),
            imports_pct=float(66.0122212131472),
            nuclear_pct=float(60.09744330272721),
            oil_pct=float(41.72562816779719),
            other_pct=float(36.74825277458452),
            solar_pct=float(75.21148320644313),
            wind_pct=float(21.391270979586764)
        )
        return instance

    
    def test_region_id_property(self):
        """
        Test region_id property
        """
        test_value = int(59)
        self.instance.region_id = test_value
        self.assertEqual(self.instance.region_id, test_value)
    
    def test_dnoregion_property(self):
        """
        Test dnoregion property
        """
        test_value = 'jvjketbtxznkqmtsoiwz'
        self.instance.dnoregion = test_value
        self.assertEqual(self.instance.dnoregion, test_value)
    
    def test_shortname_property(self):
        """
        Test shortname property
        """
        test_value = 'oomtsrqfhzvoqpynixay'
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
        test_value = int(80)
        self.instance.forecast = test_value
        self.assertEqual(self.instance.forecast, test_value)
    
    def test_index_property(self):
        """
        Test index property
        """
        test_value = 'cjoinlsljldkwpctxtzd'
        self.instance.index = test_value
        self.assertEqual(self.instance.index, test_value)
    
    def test_biomass_pct_property(self):
        """
        Test biomass_pct property
        """
        test_value = float(95.1495646246595)
        self.instance.biomass_pct = test_value
        self.assertEqual(self.instance.biomass_pct, test_value)
    
    def test_coal_pct_property(self):
        """
        Test coal_pct property
        """
        test_value = float(50.77925060176531)
        self.instance.coal_pct = test_value
        self.assertEqual(self.instance.coal_pct, test_value)
    
    def test_gas_pct_property(self):
        """
        Test gas_pct property
        """
        test_value = float(38.56349366426958)
        self.instance.gas_pct = test_value
        self.assertEqual(self.instance.gas_pct, test_value)
    
    def test_hydro_pct_property(self):
        """
        Test hydro_pct property
        """
        test_value = float(7.715821078802554)
        self.instance.hydro_pct = test_value
        self.assertEqual(self.instance.hydro_pct, test_value)
    
    def test_imports_pct_property(self):
        """
        Test imports_pct property
        """
        test_value = float(66.0122212131472)
        self.instance.imports_pct = test_value
        self.assertEqual(self.instance.imports_pct, test_value)
    
    def test_nuclear_pct_property(self):
        """
        Test nuclear_pct property
        """
        test_value = float(60.09744330272721)
        self.instance.nuclear_pct = test_value
        self.assertEqual(self.instance.nuclear_pct, test_value)
    
    def test_oil_pct_property(self):
        """
        Test oil_pct property
        """
        test_value = float(41.72562816779719)
        self.instance.oil_pct = test_value
        self.assertEqual(self.instance.oil_pct, test_value)
    
    def test_other_pct_property(self):
        """
        Test other_pct property
        """
        test_value = float(36.74825277458452)
        self.instance.other_pct = test_value
        self.assertEqual(self.instance.other_pct, test_value)
    
    def test_solar_pct_property(self):
        """
        Test solar_pct property
        """
        test_value = float(75.21148320644313)
        self.instance.solar_pct = test_value
        self.assertEqual(self.instance.solar_pct, test_value)
    
    def test_wind_pct_property(self):
        """
        Test wind_pct property
        """
        test_value = float(21.391270979586764)
        self.instance.wind_pct = test_value
        self.assertEqual(self.instance.wind_pct, test_value)
    
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

