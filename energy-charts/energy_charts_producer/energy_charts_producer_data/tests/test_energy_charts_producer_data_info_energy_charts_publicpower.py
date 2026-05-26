"""
Test case for PublicPower
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from energy_charts_producer_data.info.energy_charts.publicpower import PublicPower
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
            country='zpdsqcyatkvyzooygrxp',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            unix_seconds=int(46),
            hydro_pumped_storage_consumption_mw=float(51.511444909163096),
            cross_border_electricity_trading_mw=float(61.95500676982437),
            hydro_run_of_river_mw=float(39.63713792550203),
            biomass_mw=float(29.68079576314664),
            fossil_brown_coal_lignite_mw=float(77.3882624457354),
            fossil_hard_coal_mw=float(85.41017283061592),
            fossil_oil_mw=float(2.8099579609623837),
            fossil_coal_derived_gas_mw=float(27.336490114273893),
            fossil_gas_mw=float(34.154191601687735),
            geothermal_mw=float(16.892305738985225),
            hydro_water_reservoir_mw=float(42.71873702351539),
            hydro_pumped_storage_mw=float(79.55109869300068),
            others_mw=float(64.69454573844105),
            waste_mw=float(39.462119598103975),
            wind_offshore_mw=float(86.25313132926149),
            wind_onshore_mw=float(97.41607614208648),
            solar_mw=float(96.19103554895526),
            nuclear_mw=float(35.30356515854979),
            load_mw=float(2.0415386083263987),
            residual_load_mw=float(99.81236078390035),
            renewable_share_of_generation_pct=float(12.817484361889896),
            renewable_share_of_load_pct=float(89.75433406927313)
        )
        return instance


    def test_country_property(self):
        """
        Test country property
        """
        test_value = 'zpdsqcyatkvyzooygrxp'
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
        test_value = int(46)
        self.instance.unix_seconds = test_value
        self.assertEqual(self.instance.unix_seconds, test_value)

    def test_hydro_pumped_storage_consumption_mw_property(self):
        """
        Test hydro_pumped_storage_consumption_mw property
        """
        test_value = float(51.511444909163096)
        self.instance.hydro_pumped_storage_consumption_mw = test_value
        self.assertEqual(self.instance.hydro_pumped_storage_consumption_mw, test_value)

    def test_cross_border_electricity_trading_mw_property(self):
        """
        Test cross_border_electricity_trading_mw property
        """
        test_value = float(61.95500676982437)
        self.instance.cross_border_electricity_trading_mw = test_value
        self.assertEqual(self.instance.cross_border_electricity_trading_mw, test_value)

    def test_hydro_run_of_river_mw_property(self):
        """
        Test hydro_run_of_river_mw property
        """
        test_value = float(39.63713792550203)
        self.instance.hydro_run_of_river_mw = test_value
        self.assertEqual(self.instance.hydro_run_of_river_mw, test_value)

    def test_biomass_mw_property(self):
        """
        Test biomass_mw property
        """
        test_value = float(29.68079576314664)
        self.instance.biomass_mw = test_value
        self.assertEqual(self.instance.biomass_mw, test_value)

    def test_fossil_brown_coal_lignite_mw_property(self):
        """
        Test fossil_brown_coal_lignite_mw property
        """
        test_value = float(77.3882624457354)
        self.instance.fossil_brown_coal_lignite_mw = test_value
        self.assertEqual(self.instance.fossil_brown_coal_lignite_mw, test_value)

    def test_fossil_hard_coal_mw_property(self):
        """
        Test fossil_hard_coal_mw property
        """
        test_value = float(85.41017283061592)
        self.instance.fossil_hard_coal_mw = test_value
        self.assertEqual(self.instance.fossil_hard_coal_mw, test_value)

    def test_fossil_oil_mw_property(self):
        """
        Test fossil_oil_mw property
        """
        test_value = float(2.8099579609623837)
        self.instance.fossil_oil_mw = test_value
        self.assertEqual(self.instance.fossil_oil_mw, test_value)

    def test_fossil_coal_derived_gas_mw_property(self):
        """
        Test fossil_coal_derived_gas_mw property
        """
        test_value = float(27.336490114273893)
        self.instance.fossil_coal_derived_gas_mw = test_value
        self.assertEqual(self.instance.fossil_coal_derived_gas_mw, test_value)

    def test_fossil_gas_mw_property(self):
        """
        Test fossil_gas_mw property
        """
        test_value = float(34.154191601687735)
        self.instance.fossil_gas_mw = test_value
        self.assertEqual(self.instance.fossil_gas_mw, test_value)

    def test_geothermal_mw_property(self):
        """
        Test geothermal_mw property
        """
        test_value = float(16.892305738985225)
        self.instance.geothermal_mw = test_value
        self.assertEqual(self.instance.geothermal_mw, test_value)

    def test_hydro_water_reservoir_mw_property(self):
        """
        Test hydro_water_reservoir_mw property
        """
        test_value = float(42.71873702351539)
        self.instance.hydro_water_reservoir_mw = test_value
        self.assertEqual(self.instance.hydro_water_reservoir_mw, test_value)

    def test_hydro_pumped_storage_mw_property(self):
        """
        Test hydro_pumped_storage_mw property
        """
        test_value = float(79.55109869300068)
        self.instance.hydro_pumped_storage_mw = test_value
        self.assertEqual(self.instance.hydro_pumped_storage_mw, test_value)

    def test_others_mw_property(self):
        """
        Test others_mw property
        """
        test_value = float(64.69454573844105)
        self.instance.others_mw = test_value
        self.assertEqual(self.instance.others_mw, test_value)

    def test_waste_mw_property(self):
        """
        Test waste_mw property
        """
        test_value = float(39.462119598103975)
        self.instance.waste_mw = test_value
        self.assertEqual(self.instance.waste_mw, test_value)

    def test_wind_offshore_mw_property(self):
        """
        Test wind_offshore_mw property
        """
        test_value = float(86.25313132926149)
        self.instance.wind_offshore_mw = test_value
        self.assertEqual(self.instance.wind_offshore_mw, test_value)

    def test_wind_onshore_mw_property(self):
        """
        Test wind_onshore_mw property
        """
        test_value = float(97.41607614208648)
        self.instance.wind_onshore_mw = test_value
        self.assertEqual(self.instance.wind_onshore_mw, test_value)

    def test_solar_mw_property(self):
        """
        Test solar_mw property
        """
        test_value = float(96.19103554895526)
        self.instance.solar_mw = test_value
        self.assertEqual(self.instance.solar_mw, test_value)

    def test_nuclear_mw_property(self):
        """
        Test nuclear_mw property
        """
        test_value = float(35.30356515854979)
        self.instance.nuclear_mw = test_value
        self.assertEqual(self.instance.nuclear_mw, test_value)

    def test_load_mw_property(self):
        """
        Test load_mw property
        """
        test_value = float(2.0415386083263987)
        self.instance.load_mw = test_value
        self.assertEqual(self.instance.load_mw, test_value)

    def test_residual_load_mw_property(self):
        """
        Test residual_load_mw property
        """
        test_value = float(99.81236078390035)
        self.instance.residual_load_mw = test_value
        self.assertEqual(self.instance.residual_load_mw, test_value)

    def test_renewable_share_of_generation_pct_property(self):
        """
        Test renewable_share_of_generation_pct property
        """
        test_value = float(12.817484361889896)
        self.instance.renewable_share_of_generation_pct = test_value
        self.assertEqual(self.instance.renewable_share_of_generation_pct, test_value)

    def test_renewable_share_of_load_pct_property(self):
        """
        Test renewable_share_of_load_pct property
        """
        test_value = float(89.75433406927313)
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
