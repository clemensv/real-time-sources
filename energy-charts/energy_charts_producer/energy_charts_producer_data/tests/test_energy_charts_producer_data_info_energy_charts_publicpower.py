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
            country='prvntdtngapjitqvmuvl',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            unix_seconds=int(61),
            hydro_pumped_storage_consumption_mw=float(37.36819172633483),
            cross_border_electricity_trading_mw=float(41.2969258029259),
            hydro_run_of_river_mw=float(19.626519939561437),
            biomass_mw=float(96.13535817620861),
            fossil_brown_coal_lignite_mw=float(92.41390904723875),
            fossil_hard_coal_mw=float(7.9382188636833995),
            fossil_oil_mw=float(62.54830072460085),
            fossil_coal_derived_gas_mw=float(81.30200108159137),
            fossil_gas_mw=float(10.590638359045412),
            geothermal_mw=float(70.83994366184862),
            hydro_water_reservoir_mw=float(74.31380250119123),
            hydro_pumped_storage_mw=float(2.986585496800076),
            others_mw=float(87.04268979011731),
            waste_mw=float(39.94083009660563),
            wind_offshore_mw=float(27.23897401036598),
            wind_onshore_mw=float(77.39182762319989),
            solar_mw=float(88.50008187982174),
            nuclear_mw=float(32.090875167245514),
            load_mw=float(82.964356629142),
            residual_load_mw=float(27.948137702583665),
            renewable_share_of_generation_pct=float(32.01745487079317),
            renewable_share_of_load_pct=float(67.8731756220697)
        )
        return instance

    
    def test_country_property(self):
        """
        Test country property
        """
        test_value = 'prvntdtngapjitqvmuvl'
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
        test_value = int(61)
        self.instance.unix_seconds = test_value
        self.assertEqual(self.instance.unix_seconds, test_value)
    
    def test_hydro_pumped_storage_consumption_mw_property(self):
        """
        Test hydro_pumped_storage_consumption_mw property
        """
        test_value = float(37.36819172633483)
        self.instance.hydro_pumped_storage_consumption_mw = test_value
        self.assertEqual(self.instance.hydro_pumped_storage_consumption_mw, test_value)
    
    def test_cross_border_electricity_trading_mw_property(self):
        """
        Test cross_border_electricity_trading_mw property
        """
        test_value = float(41.2969258029259)
        self.instance.cross_border_electricity_trading_mw = test_value
        self.assertEqual(self.instance.cross_border_electricity_trading_mw, test_value)
    
    def test_hydro_run_of_river_mw_property(self):
        """
        Test hydro_run_of_river_mw property
        """
        test_value = float(19.626519939561437)
        self.instance.hydro_run_of_river_mw = test_value
        self.assertEqual(self.instance.hydro_run_of_river_mw, test_value)
    
    def test_biomass_mw_property(self):
        """
        Test biomass_mw property
        """
        test_value = float(96.13535817620861)
        self.instance.biomass_mw = test_value
        self.assertEqual(self.instance.biomass_mw, test_value)
    
    def test_fossil_brown_coal_lignite_mw_property(self):
        """
        Test fossil_brown_coal_lignite_mw property
        """
        test_value = float(92.41390904723875)
        self.instance.fossil_brown_coal_lignite_mw = test_value
        self.assertEqual(self.instance.fossil_brown_coal_lignite_mw, test_value)
    
    def test_fossil_hard_coal_mw_property(self):
        """
        Test fossil_hard_coal_mw property
        """
        test_value = float(7.9382188636833995)
        self.instance.fossil_hard_coal_mw = test_value
        self.assertEqual(self.instance.fossil_hard_coal_mw, test_value)
    
    def test_fossil_oil_mw_property(self):
        """
        Test fossil_oil_mw property
        """
        test_value = float(62.54830072460085)
        self.instance.fossil_oil_mw = test_value
        self.assertEqual(self.instance.fossil_oil_mw, test_value)
    
    def test_fossil_coal_derived_gas_mw_property(self):
        """
        Test fossil_coal_derived_gas_mw property
        """
        test_value = float(81.30200108159137)
        self.instance.fossil_coal_derived_gas_mw = test_value
        self.assertEqual(self.instance.fossil_coal_derived_gas_mw, test_value)
    
    def test_fossil_gas_mw_property(self):
        """
        Test fossil_gas_mw property
        """
        test_value = float(10.590638359045412)
        self.instance.fossil_gas_mw = test_value
        self.assertEqual(self.instance.fossil_gas_mw, test_value)
    
    def test_geothermal_mw_property(self):
        """
        Test geothermal_mw property
        """
        test_value = float(70.83994366184862)
        self.instance.geothermal_mw = test_value
        self.assertEqual(self.instance.geothermal_mw, test_value)
    
    def test_hydro_water_reservoir_mw_property(self):
        """
        Test hydro_water_reservoir_mw property
        """
        test_value = float(74.31380250119123)
        self.instance.hydro_water_reservoir_mw = test_value
        self.assertEqual(self.instance.hydro_water_reservoir_mw, test_value)
    
    def test_hydro_pumped_storage_mw_property(self):
        """
        Test hydro_pumped_storage_mw property
        """
        test_value = float(2.986585496800076)
        self.instance.hydro_pumped_storage_mw = test_value
        self.assertEqual(self.instance.hydro_pumped_storage_mw, test_value)
    
    def test_others_mw_property(self):
        """
        Test others_mw property
        """
        test_value = float(87.04268979011731)
        self.instance.others_mw = test_value
        self.assertEqual(self.instance.others_mw, test_value)
    
    def test_waste_mw_property(self):
        """
        Test waste_mw property
        """
        test_value = float(39.94083009660563)
        self.instance.waste_mw = test_value
        self.assertEqual(self.instance.waste_mw, test_value)
    
    def test_wind_offshore_mw_property(self):
        """
        Test wind_offshore_mw property
        """
        test_value = float(27.23897401036598)
        self.instance.wind_offshore_mw = test_value
        self.assertEqual(self.instance.wind_offshore_mw, test_value)
    
    def test_wind_onshore_mw_property(self):
        """
        Test wind_onshore_mw property
        """
        test_value = float(77.39182762319989)
        self.instance.wind_onshore_mw = test_value
        self.assertEqual(self.instance.wind_onshore_mw, test_value)
    
    def test_solar_mw_property(self):
        """
        Test solar_mw property
        """
        test_value = float(88.50008187982174)
        self.instance.solar_mw = test_value
        self.assertEqual(self.instance.solar_mw, test_value)
    
    def test_nuclear_mw_property(self):
        """
        Test nuclear_mw property
        """
        test_value = float(32.090875167245514)
        self.instance.nuclear_mw = test_value
        self.assertEqual(self.instance.nuclear_mw, test_value)
    
    def test_load_mw_property(self):
        """
        Test load_mw property
        """
        test_value = float(82.964356629142)
        self.instance.load_mw = test_value
        self.assertEqual(self.instance.load_mw, test_value)
    
    def test_residual_load_mw_property(self):
        """
        Test residual_load_mw property
        """
        test_value = float(27.948137702583665)
        self.instance.residual_load_mw = test_value
        self.assertEqual(self.instance.residual_load_mw, test_value)
    
    def test_renewable_share_of_generation_pct_property(self):
        """
        Test renewable_share_of_generation_pct property
        """
        test_value = float(32.01745487079317)
        self.instance.renewable_share_of_generation_pct = test_value
        self.assertEqual(self.instance.renewable_share_of_generation_pct, test_value)
    
    def test_renewable_share_of_load_pct_property(self):
        """
        Test renewable_share_of_load_pct property
        """
        test_value = float(67.8731756220697)
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
