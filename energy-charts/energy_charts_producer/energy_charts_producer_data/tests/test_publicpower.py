"""
Test case for PublicPower
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from energy_charts_producer_data.publicpower import PublicPower
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
            country='gatqulbqbhqrapjglsqq',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            unix_seconds=int(71),
            hydro_pumped_storage_consumption_mw=float(82.24465615249034),
            cross_border_electricity_trading_mw=float(90.73703105380575),
            hydro_run_of_river_mw=float(26.6703439457882),
            biomass_mw=float(26.787055305704065),
            fossil_brown_coal_lignite_mw=float(50.975962741829626),
            fossil_hard_coal_mw=float(20.08875990559227),
            fossil_oil_mw=float(49.66381798374688),
            fossil_coal_derived_gas_mw=float(57.30944333900927),
            fossil_gas_mw=float(59.66505317607348),
            geothermal_mw=float(38.78572564890982),
            hydro_water_reservoir_mw=float(84.7007996799862),
            hydro_pumped_storage_mw=float(33.42260662143906),
            others_mw=float(7.2398684879426245),
            waste_mw=float(97.67175241159606),
            wind_offshore_mw=float(36.970546395527315),
            wind_onshore_mw=float(74.0649024503657),
            solar_mw=float(78.79443008224791),
            nuclear_mw=float(98.82024141456087),
            load_mw=float(48.2576843970127),
            residual_load_mw=float(26.106323922491292),
            renewable_share_of_generation_pct=float(17.503348106280725),
            renewable_share_of_load_pct=float(32.9074242112563)
        )
        return instance


    def test_country_property(self):
        """
        Test country property
        """
        test_value = 'gatqulbqbhqrapjglsqq'
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
        test_value = int(71)
        self.instance.unix_seconds = test_value
        self.assertEqual(self.instance.unix_seconds, test_value)

    def test_hydro_pumped_storage_consumption_mw_property(self):
        """
        Test hydro_pumped_storage_consumption_mw property
        """
        test_value = float(82.24465615249034)
        self.instance.hydro_pumped_storage_consumption_mw = test_value
        self.assertEqual(self.instance.hydro_pumped_storage_consumption_mw, test_value)

    def test_cross_border_electricity_trading_mw_property(self):
        """
        Test cross_border_electricity_trading_mw property
        """
        test_value = float(90.73703105380575)
        self.instance.cross_border_electricity_trading_mw = test_value
        self.assertEqual(self.instance.cross_border_electricity_trading_mw, test_value)

    def test_hydro_run_of_river_mw_property(self):
        """
        Test hydro_run_of_river_mw property
        """
        test_value = float(26.6703439457882)
        self.instance.hydro_run_of_river_mw = test_value
        self.assertEqual(self.instance.hydro_run_of_river_mw, test_value)

    def test_biomass_mw_property(self):
        """
        Test biomass_mw property
        """
        test_value = float(26.787055305704065)
        self.instance.biomass_mw = test_value
        self.assertEqual(self.instance.biomass_mw, test_value)

    def test_fossil_brown_coal_lignite_mw_property(self):
        """
        Test fossil_brown_coal_lignite_mw property
        """
        test_value = float(50.975962741829626)
        self.instance.fossil_brown_coal_lignite_mw = test_value
        self.assertEqual(self.instance.fossil_brown_coal_lignite_mw, test_value)

    def test_fossil_hard_coal_mw_property(self):
        """
        Test fossil_hard_coal_mw property
        """
        test_value = float(20.08875990559227)
        self.instance.fossil_hard_coal_mw = test_value
        self.assertEqual(self.instance.fossil_hard_coal_mw, test_value)

    def test_fossil_oil_mw_property(self):
        """
        Test fossil_oil_mw property
        """
        test_value = float(49.66381798374688)
        self.instance.fossil_oil_mw = test_value
        self.assertEqual(self.instance.fossil_oil_mw, test_value)

    def test_fossil_coal_derived_gas_mw_property(self):
        """
        Test fossil_coal_derived_gas_mw property
        """
        test_value = float(57.30944333900927)
        self.instance.fossil_coal_derived_gas_mw = test_value
        self.assertEqual(self.instance.fossil_coal_derived_gas_mw, test_value)

    def test_fossil_gas_mw_property(self):
        """
        Test fossil_gas_mw property
        """
        test_value = float(59.66505317607348)
        self.instance.fossil_gas_mw = test_value
        self.assertEqual(self.instance.fossil_gas_mw, test_value)

    def test_geothermal_mw_property(self):
        """
        Test geothermal_mw property
        """
        test_value = float(38.78572564890982)
        self.instance.geothermal_mw = test_value
        self.assertEqual(self.instance.geothermal_mw, test_value)

    def test_hydro_water_reservoir_mw_property(self):
        """
        Test hydro_water_reservoir_mw property
        """
        test_value = float(84.7007996799862)
        self.instance.hydro_water_reservoir_mw = test_value
        self.assertEqual(self.instance.hydro_water_reservoir_mw, test_value)

    def test_hydro_pumped_storage_mw_property(self):
        """
        Test hydro_pumped_storage_mw property
        """
        test_value = float(33.42260662143906)
        self.instance.hydro_pumped_storage_mw = test_value
        self.assertEqual(self.instance.hydro_pumped_storage_mw, test_value)

    def test_others_mw_property(self):
        """
        Test others_mw property
        """
        test_value = float(7.2398684879426245)
        self.instance.others_mw = test_value
        self.assertEqual(self.instance.others_mw, test_value)

    def test_waste_mw_property(self):
        """
        Test waste_mw property
        """
        test_value = float(97.67175241159606)
        self.instance.waste_mw = test_value
        self.assertEqual(self.instance.waste_mw, test_value)

    def test_wind_offshore_mw_property(self):
        """
        Test wind_offshore_mw property
        """
        test_value = float(36.970546395527315)
        self.instance.wind_offshore_mw = test_value
        self.assertEqual(self.instance.wind_offshore_mw, test_value)

    def test_wind_onshore_mw_property(self):
        """
        Test wind_onshore_mw property
        """
        test_value = float(74.0649024503657)
        self.instance.wind_onshore_mw = test_value
        self.assertEqual(self.instance.wind_onshore_mw, test_value)

    def test_solar_mw_property(self):
        """
        Test solar_mw property
        """
        test_value = float(78.79443008224791)
        self.instance.solar_mw = test_value
        self.assertEqual(self.instance.solar_mw, test_value)

    def test_nuclear_mw_property(self):
        """
        Test nuclear_mw property
        """
        test_value = float(98.82024141456087)
        self.instance.nuclear_mw = test_value
        self.assertEqual(self.instance.nuclear_mw, test_value)

    def test_load_mw_property(self):
        """
        Test load_mw property
        """
        test_value = float(48.2576843970127)
        self.instance.load_mw = test_value
        self.assertEqual(self.instance.load_mw, test_value)

    def test_residual_load_mw_property(self):
        """
        Test residual_load_mw property
        """
        test_value = float(26.106323922491292)
        self.instance.residual_load_mw = test_value
        self.assertEqual(self.instance.residual_load_mw, test_value)

    def test_renewable_share_of_generation_pct_property(self):
        """
        Test renewable_share_of_generation_pct property
        """
        test_value = float(17.503348106280725)
        self.instance.renewable_share_of_generation_pct = test_value
        self.assertEqual(self.instance.renewable_share_of_generation_pct, test_value)

    def test_renewable_share_of_load_pct_property(self):
        """
        Test renewable_share_of_load_pct property
        """
        test_value = float(32.9074242112563)
        self.instance.renewable_share_of_load_pct = test_value
        self.assertEqual(self.instance.renewable_share_of_load_pct, test_value)

    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = PublicPower.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
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

