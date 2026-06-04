"""
Test case for PublicPower
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from energy_charts_amqp_producer_data.publicpower import PublicPower
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
            country='gqooyputllvyootiywrm',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            unix_seconds=int(99),
            hydro_pumped_storage_consumption_mw=float(19.600634951719385),
            cross_border_electricity_trading_mw=float(24.013215173412405),
            hydro_run_of_river_mw=float(43.474340144036695),
            biomass_mw=float(59.62981061459243),
            fossil_brown_coal_lignite_mw=float(5.525863481522963),
            fossil_hard_coal_mw=float(58.724914419863936),
            fossil_oil_mw=float(67.54489208154494),
            fossil_coal_derived_gas_mw=float(51.54335071763997),
            fossil_gas_mw=float(24.27176378137661),
            geothermal_mw=float(58.61363507454996),
            hydro_water_reservoir_mw=float(87.13527404394826),
            hydro_pumped_storage_mw=float(35.95729369045397),
            others_mw=float(22.415396973328015),
            waste_mw=float(9.09059881020342),
            wind_offshore_mw=float(94.23003491131414),
            wind_onshore_mw=float(62.961412907939796),
            solar_mw=float(36.34930492304475),
            nuclear_mw=float(84.51780819842669),
            load_mw=float(69.06779328169087),
            residual_load_mw=float(8.258001508235468),
            renewable_share_of_generation_pct=float(71.16350494904648),
            renewable_share_of_load_pct=float(71.60895351019177)
        )
        return instance

    
    def test_country_property(self):
        """
        Test country property
        """
        test_value = 'gqooyputllvyootiywrm'
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
        test_value = int(99)
        self.instance.unix_seconds = test_value
        self.assertEqual(self.instance.unix_seconds, test_value)
    
    def test_hydro_pumped_storage_consumption_mw_property(self):
        """
        Test hydro_pumped_storage_consumption_mw property
        """
        test_value = float(19.600634951719385)
        self.instance.hydro_pumped_storage_consumption_mw = test_value
        self.assertEqual(self.instance.hydro_pumped_storage_consumption_mw, test_value)
    
    def test_cross_border_electricity_trading_mw_property(self):
        """
        Test cross_border_electricity_trading_mw property
        """
        test_value = float(24.013215173412405)
        self.instance.cross_border_electricity_trading_mw = test_value
        self.assertEqual(self.instance.cross_border_electricity_trading_mw, test_value)
    
    def test_hydro_run_of_river_mw_property(self):
        """
        Test hydro_run_of_river_mw property
        """
        test_value = float(43.474340144036695)
        self.instance.hydro_run_of_river_mw = test_value
        self.assertEqual(self.instance.hydro_run_of_river_mw, test_value)
    
    def test_biomass_mw_property(self):
        """
        Test biomass_mw property
        """
        test_value = float(59.62981061459243)
        self.instance.biomass_mw = test_value
        self.assertEqual(self.instance.biomass_mw, test_value)
    
    def test_fossil_brown_coal_lignite_mw_property(self):
        """
        Test fossil_brown_coal_lignite_mw property
        """
        test_value = float(5.525863481522963)
        self.instance.fossil_brown_coal_lignite_mw = test_value
        self.assertEqual(self.instance.fossil_brown_coal_lignite_mw, test_value)
    
    def test_fossil_hard_coal_mw_property(self):
        """
        Test fossil_hard_coal_mw property
        """
        test_value = float(58.724914419863936)
        self.instance.fossil_hard_coal_mw = test_value
        self.assertEqual(self.instance.fossil_hard_coal_mw, test_value)
    
    def test_fossil_oil_mw_property(self):
        """
        Test fossil_oil_mw property
        """
        test_value = float(67.54489208154494)
        self.instance.fossil_oil_mw = test_value
        self.assertEqual(self.instance.fossil_oil_mw, test_value)
    
    def test_fossil_coal_derived_gas_mw_property(self):
        """
        Test fossil_coal_derived_gas_mw property
        """
        test_value = float(51.54335071763997)
        self.instance.fossil_coal_derived_gas_mw = test_value
        self.assertEqual(self.instance.fossil_coal_derived_gas_mw, test_value)
    
    def test_fossil_gas_mw_property(self):
        """
        Test fossil_gas_mw property
        """
        test_value = float(24.27176378137661)
        self.instance.fossil_gas_mw = test_value
        self.assertEqual(self.instance.fossil_gas_mw, test_value)
    
    def test_geothermal_mw_property(self):
        """
        Test geothermal_mw property
        """
        test_value = float(58.61363507454996)
        self.instance.geothermal_mw = test_value
        self.assertEqual(self.instance.geothermal_mw, test_value)
    
    def test_hydro_water_reservoir_mw_property(self):
        """
        Test hydro_water_reservoir_mw property
        """
        test_value = float(87.13527404394826)
        self.instance.hydro_water_reservoir_mw = test_value
        self.assertEqual(self.instance.hydro_water_reservoir_mw, test_value)
    
    def test_hydro_pumped_storage_mw_property(self):
        """
        Test hydro_pumped_storage_mw property
        """
        test_value = float(35.95729369045397)
        self.instance.hydro_pumped_storage_mw = test_value
        self.assertEqual(self.instance.hydro_pumped_storage_mw, test_value)
    
    def test_others_mw_property(self):
        """
        Test others_mw property
        """
        test_value = float(22.415396973328015)
        self.instance.others_mw = test_value
        self.assertEqual(self.instance.others_mw, test_value)
    
    def test_waste_mw_property(self):
        """
        Test waste_mw property
        """
        test_value = float(9.09059881020342)
        self.instance.waste_mw = test_value
        self.assertEqual(self.instance.waste_mw, test_value)
    
    def test_wind_offshore_mw_property(self):
        """
        Test wind_offshore_mw property
        """
        test_value = float(94.23003491131414)
        self.instance.wind_offshore_mw = test_value
        self.assertEqual(self.instance.wind_offshore_mw, test_value)
    
    def test_wind_onshore_mw_property(self):
        """
        Test wind_onshore_mw property
        """
        test_value = float(62.961412907939796)
        self.instance.wind_onshore_mw = test_value
        self.assertEqual(self.instance.wind_onshore_mw, test_value)
    
    def test_solar_mw_property(self):
        """
        Test solar_mw property
        """
        test_value = float(36.34930492304475)
        self.instance.solar_mw = test_value
        self.assertEqual(self.instance.solar_mw, test_value)
    
    def test_nuclear_mw_property(self):
        """
        Test nuclear_mw property
        """
        test_value = float(84.51780819842669)
        self.instance.nuclear_mw = test_value
        self.assertEqual(self.instance.nuclear_mw, test_value)
    
    def test_load_mw_property(self):
        """
        Test load_mw property
        """
        test_value = float(69.06779328169087)
        self.instance.load_mw = test_value
        self.assertEqual(self.instance.load_mw, test_value)
    
    def test_residual_load_mw_property(self):
        """
        Test residual_load_mw property
        """
        test_value = float(8.258001508235468)
        self.instance.residual_load_mw = test_value
        self.assertEqual(self.instance.residual_load_mw, test_value)
    
    def test_renewable_share_of_generation_pct_property(self):
        """
        Test renewable_share_of_generation_pct property
        """
        test_value = float(71.16350494904648)
        self.instance.renewable_share_of_generation_pct = test_value
        self.assertEqual(self.instance.renewable_share_of_generation_pct, test_value)
    
    def test_renewable_share_of_load_pct_property(self):
        """
        Test renewable_share_of_load_pct property
        """
        test_value = float(71.60895351019177)
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

