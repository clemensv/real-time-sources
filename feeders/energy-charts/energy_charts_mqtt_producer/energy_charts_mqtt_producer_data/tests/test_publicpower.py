"""
Test case for PublicPower
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from energy_charts_mqtt_producer_data.publicpower import PublicPower
import datetime


class Test_PublicPower(unittest.TestCase):
    """
    Test case for PublicPower
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_PublicPower.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of PublicPower for testing
        """
        instance = PublicPower(
            country='afmotuzwtugrdhdqxgfr',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            unix_seconds=int(27),
            hydro_pumped_storage_consumption_mw=float(11.824710936343374),
            cross_border_electricity_trading_mw=float(9.938566339124144),
            hydro_run_of_river_mw=float(21.0236415543376),
            biomass_mw=float(33.41478189543445),
            fossil_brown_coal_lignite_mw=float(60.327725326677395),
            fossil_hard_coal_mw=float(56.55941071928986),
            fossil_oil_mw=float(37.73766910556908),
            fossil_coal_derived_gas_mw=float(4.411781092056399),
            fossil_gas_mw=float(49.86042278548497),
            geothermal_mw=float(21.244483591529285),
            hydro_water_reservoir_mw=float(0.8798885803588008),
            hydro_pumped_storage_mw=float(67.360516230693),
            others_mw=float(70.76479857540677),
            waste_mw=float(60.87963726008538),
            wind_offshore_mw=float(27.572531340058504),
            wind_onshore_mw=float(76.7353533389567),
            solar_mw=float(62.019761917716686),
            nuclear_mw=float(29.412020003948424),
            load_mw=float(77.56130181192972),
            residual_load_mw=float(7.348640263171613),
            renewable_share_of_generation_pct=float(27.916764016166372),
            renewable_share_of_load_pct=float(67.65099140580718)
        )
        return instance

    
    def test_country_property(self):
        """
        Test country property
        """
        test_value = 'afmotuzwtugrdhdqxgfr'
        self.instance.country = test_value
        self.assertEqual(self.instance.country, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_unix_seconds_property(self):
        """
        Test unix_seconds property
        """
        test_value = int(27)
        self.instance.unix_seconds = test_value
        self.assertEqual(self.instance.unix_seconds, test_value)
    
    def test_hydro_pumped_storage_consumption_mw_property(self):
        """
        Test hydro_pumped_storage_consumption_mw property
        """
        test_value = float(11.824710936343374)
        self.instance.hydro_pumped_storage_consumption_mw = test_value
        self.assertEqual(self.instance.hydro_pumped_storage_consumption_mw, test_value)
    
    def test_cross_border_electricity_trading_mw_property(self):
        """
        Test cross_border_electricity_trading_mw property
        """
        test_value = float(9.938566339124144)
        self.instance.cross_border_electricity_trading_mw = test_value
        self.assertEqual(self.instance.cross_border_electricity_trading_mw, test_value)
    
    def test_hydro_run_of_river_mw_property(self):
        """
        Test hydro_run_of_river_mw property
        """
        test_value = float(21.0236415543376)
        self.instance.hydro_run_of_river_mw = test_value
        self.assertEqual(self.instance.hydro_run_of_river_mw, test_value)
    
    def test_biomass_mw_property(self):
        """
        Test biomass_mw property
        """
        test_value = float(33.41478189543445)
        self.instance.biomass_mw = test_value
        self.assertEqual(self.instance.biomass_mw, test_value)
    
    def test_fossil_brown_coal_lignite_mw_property(self):
        """
        Test fossil_brown_coal_lignite_mw property
        """
        test_value = float(60.327725326677395)
        self.instance.fossil_brown_coal_lignite_mw = test_value
        self.assertEqual(self.instance.fossil_brown_coal_lignite_mw, test_value)
    
    def test_fossil_hard_coal_mw_property(self):
        """
        Test fossil_hard_coal_mw property
        """
        test_value = float(56.55941071928986)
        self.instance.fossil_hard_coal_mw = test_value
        self.assertEqual(self.instance.fossil_hard_coal_mw, test_value)
    
    def test_fossil_oil_mw_property(self):
        """
        Test fossil_oil_mw property
        """
        test_value = float(37.73766910556908)
        self.instance.fossil_oil_mw = test_value
        self.assertEqual(self.instance.fossil_oil_mw, test_value)
    
    def test_fossil_coal_derived_gas_mw_property(self):
        """
        Test fossil_coal_derived_gas_mw property
        """
        test_value = float(4.411781092056399)
        self.instance.fossil_coal_derived_gas_mw = test_value
        self.assertEqual(self.instance.fossil_coal_derived_gas_mw, test_value)
    
    def test_fossil_gas_mw_property(self):
        """
        Test fossil_gas_mw property
        """
        test_value = float(49.86042278548497)
        self.instance.fossil_gas_mw = test_value
        self.assertEqual(self.instance.fossil_gas_mw, test_value)
    
    def test_geothermal_mw_property(self):
        """
        Test geothermal_mw property
        """
        test_value = float(21.244483591529285)
        self.instance.geothermal_mw = test_value
        self.assertEqual(self.instance.geothermal_mw, test_value)
    
    def test_hydro_water_reservoir_mw_property(self):
        """
        Test hydro_water_reservoir_mw property
        """
        test_value = float(0.8798885803588008)
        self.instance.hydro_water_reservoir_mw = test_value
        self.assertEqual(self.instance.hydro_water_reservoir_mw, test_value)
    
    def test_hydro_pumped_storage_mw_property(self):
        """
        Test hydro_pumped_storage_mw property
        """
        test_value = float(67.360516230693)
        self.instance.hydro_pumped_storage_mw = test_value
        self.assertEqual(self.instance.hydro_pumped_storage_mw, test_value)
    
    def test_others_mw_property(self):
        """
        Test others_mw property
        """
        test_value = float(70.76479857540677)
        self.instance.others_mw = test_value
        self.assertEqual(self.instance.others_mw, test_value)
    
    def test_waste_mw_property(self):
        """
        Test waste_mw property
        """
        test_value = float(60.87963726008538)
        self.instance.waste_mw = test_value
        self.assertEqual(self.instance.waste_mw, test_value)
    
    def test_wind_offshore_mw_property(self):
        """
        Test wind_offshore_mw property
        """
        test_value = float(27.572531340058504)
        self.instance.wind_offshore_mw = test_value
        self.assertEqual(self.instance.wind_offshore_mw, test_value)
    
    def test_wind_onshore_mw_property(self):
        """
        Test wind_onshore_mw property
        """
        test_value = float(76.7353533389567)
        self.instance.wind_onshore_mw = test_value
        self.assertEqual(self.instance.wind_onshore_mw, test_value)
    
    def test_solar_mw_property(self):
        """
        Test solar_mw property
        """
        test_value = float(62.019761917716686)
        self.instance.solar_mw = test_value
        self.assertEqual(self.instance.solar_mw, test_value)
    
    def test_nuclear_mw_property(self):
        """
        Test nuclear_mw property
        """
        test_value = float(29.412020003948424)
        self.instance.nuclear_mw = test_value
        self.assertEqual(self.instance.nuclear_mw, test_value)
    
    def test_load_mw_property(self):
        """
        Test load_mw property
        """
        test_value = float(77.56130181192972)
        self.instance.load_mw = test_value
        self.assertEqual(self.instance.load_mw, test_value)
    
    def test_residual_load_mw_property(self):
        """
        Test residual_load_mw property
        """
        test_value = float(7.348640263171613)
        self.instance.residual_load_mw = test_value
        self.assertEqual(self.instance.residual_load_mw, test_value)
    
    def test_renewable_share_of_generation_pct_property(self):
        """
        Test renewable_share_of_generation_pct property
        """
        test_value = float(27.916764016166372)
        self.instance.renewable_share_of_generation_pct = test_value
        self.assertEqual(self.instance.renewable_share_of_generation_pct, test_value)
    
    def test_renewable_share_of_load_pct_property(self):
        """
        Test renewable_share_of_load_pct property
        """
        test_value = float(67.65099140580718)
        self.instance.renewable_share_of_load_pct = test_value
        self.assertEqual(self.instance.renewable_share_of_load_pct, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = PublicPower.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = PublicPower.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

