"""
Test case for PowerSystemSnapshot
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from energidataservice_dk_amqp_producer_data.dk.energinet.energidataservice.powersystemsnapshot import PowerSystemSnapshot


class Test_PowerSystemSnapshot(unittest.TestCase):
    """
    Test case for PowerSystemSnapshot
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_PowerSystemSnapshot.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of PowerSystemSnapshot for testing
        """
        instance = PowerSystemSnapshot(
            minutes1_utc='jmftxhxsrnybkdskkpnk',
            minutes1_dk='mggxgxucsfamdugmtwxp',
            price_area='pvykrejnakcfnaphjqoi',
            co2_emission=float(59.04485803743826),
            production_ge_100mw=float(79.34293178878825),
            production_lt_100mw=float(17.441591145210378),
            solar_power=float(15.726293254290535),
            offshore_wind_power=float(88.01350781343456),
            onshore_wind_power=float(73.55077945974055),
            exchange_sum=float(38.41460416452184),
            exchange_dk1_de=float(25.316822544376862),
            exchange_dk1_nl=float(10.723758191143562),
            exchange_dk1_gb=float(41.325965127209884),
            exchange_dk1_no=float(80.20231910802539),
            exchange_dk1_se=float(97.15259193810456),
            exchange_dk1_dk2=float(89.78508103132312),
            exchange_dk2_de=float(13.317965064457503),
            exchange_dk2_se=float(39.909633539019794),
            exchange_bornholm_se=float(27.527917276739032),
            afrr_activated_dk1=float(94.7169091879845),
            afrr_activated_dk2=float(28.388749388791567),
            mfrr_activated_dk1=float(87.32755807043857),
            mfrr_activated_dk2=float(10.204714628586487),
            imbalance_dk1=float(11.875638314235438),
            imbalance_dk2=float(57.239866665234985)
        )
        return instance

    
    def test_minutes1_utc_property(self):
        """
        Test minutes1_utc property
        """
        test_value = 'jmftxhxsrnybkdskkpnk'
        self.instance.minutes1_utc = test_value
        self.assertEqual(self.instance.minutes1_utc, test_value)
    
    def test_minutes1_dk_property(self):
        """
        Test minutes1_dk property
        """
        test_value = 'mggxgxucsfamdugmtwxp'
        self.instance.minutes1_dk = test_value
        self.assertEqual(self.instance.minutes1_dk, test_value)
    
    def test_price_area_property(self):
        """
        Test price_area property
        """
        test_value = 'pvykrejnakcfnaphjqoi'
        self.instance.price_area = test_value
        self.assertEqual(self.instance.price_area, test_value)
    
    def test_co2_emission_property(self):
        """
        Test co2_emission property
        """
        test_value = float(59.04485803743826)
        self.instance.co2_emission = test_value
        self.assertEqual(self.instance.co2_emission, test_value)
    
    def test_production_ge_100mw_property(self):
        """
        Test production_ge_100mw property
        """
        test_value = float(79.34293178878825)
        self.instance.production_ge_100mw = test_value
        self.assertEqual(self.instance.production_ge_100mw, test_value)
    
    def test_production_lt_100mw_property(self):
        """
        Test production_lt_100mw property
        """
        test_value = float(17.441591145210378)
        self.instance.production_lt_100mw = test_value
        self.assertEqual(self.instance.production_lt_100mw, test_value)
    
    def test_solar_power_property(self):
        """
        Test solar_power property
        """
        test_value = float(15.726293254290535)
        self.instance.solar_power = test_value
        self.assertEqual(self.instance.solar_power, test_value)
    
    def test_offshore_wind_power_property(self):
        """
        Test offshore_wind_power property
        """
        test_value = float(88.01350781343456)
        self.instance.offshore_wind_power = test_value
        self.assertEqual(self.instance.offshore_wind_power, test_value)
    
    def test_onshore_wind_power_property(self):
        """
        Test onshore_wind_power property
        """
        test_value = float(73.55077945974055)
        self.instance.onshore_wind_power = test_value
        self.assertEqual(self.instance.onshore_wind_power, test_value)
    
    def test_exchange_sum_property(self):
        """
        Test exchange_sum property
        """
        test_value = float(38.41460416452184)
        self.instance.exchange_sum = test_value
        self.assertEqual(self.instance.exchange_sum, test_value)
    
    def test_exchange_dk1_de_property(self):
        """
        Test exchange_dk1_de property
        """
        test_value = float(25.316822544376862)
        self.instance.exchange_dk1_de = test_value
        self.assertEqual(self.instance.exchange_dk1_de, test_value)
    
    def test_exchange_dk1_nl_property(self):
        """
        Test exchange_dk1_nl property
        """
        test_value = float(10.723758191143562)
        self.instance.exchange_dk1_nl = test_value
        self.assertEqual(self.instance.exchange_dk1_nl, test_value)
    
    def test_exchange_dk1_gb_property(self):
        """
        Test exchange_dk1_gb property
        """
        test_value = float(41.325965127209884)
        self.instance.exchange_dk1_gb = test_value
        self.assertEqual(self.instance.exchange_dk1_gb, test_value)
    
    def test_exchange_dk1_no_property(self):
        """
        Test exchange_dk1_no property
        """
        test_value = float(80.20231910802539)
        self.instance.exchange_dk1_no = test_value
        self.assertEqual(self.instance.exchange_dk1_no, test_value)
    
    def test_exchange_dk1_se_property(self):
        """
        Test exchange_dk1_se property
        """
        test_value = float(97.15259193810456)
        self.instance.exchange_dk1_se = test_value
        self.assertEqual(self.instance.exchange_dk1_se, test_value)
    
    def test_exchange_dk1_dk2_property(self):
        """
        Test exchange_dk1_dk2 property
        """
        test_value = float(89.78508103132312)
        self.instance.exchange_dk1_dk2 = test_value
        self.assertEqual(self.instance.exchange_dk1_dk2, test_value)
    
    def test_exchange_dk2_de_property(self):
        """
        Test exchange_dk2_de property
        """
        test_value = float(13.317965064457503)
        self.instance.exchange_dk2_de = test_value
        self.assertEqual(self.instance.exchange_dk2_de, test_value)
    
    def test_exchange_dk2_se_property(self):
        """
        Test exchange_dk2_se property
        """
        test_value = float(39.909633539019794)
        self.instance.exchange_dk2_se = test_value
        self.assertEqual(self.instance.exchange_dk2_se, test_value)
    
    def test_exchange_bornholm_se_property(self):
        """
        Test exchange_bornholm_se property
        """
        test_value = float(27.527917276739032)
        self.instance.exchange_bornholm_se = test_value
        self.assertEqual(self.instance.exchange_bornholm_se, test_value)
    
    def test_afrr_activated_dk1_property(self):
        """
        Test afrr_activated_dk1 property
        """
        test_value = float(94.7169091879845)
        self.instance.afrr_activated_dk1 = test_value
        self.assertEqual(self.instance.afrr_activated_dk1, test_value)
    
    def test_afrr_activated_dk2_property(self):
        """
        Test afrr_activated_dk2 property
        """
        test_value = float(28.388749388791567)
        self.instance.afrr_activated_dk2 = test_value
        self.assertEqual(self.instance.afrr_activated_dk2, test_value)
    
    def test_mfrr_activated_dk1_property(self):
        """
        Test mfrr_activated_dk1 property
        """
        test_value = float(87.32755807043857)
        self.instance.mfrr_activated_dk1 = test_value
        self.assertEqual(self.instance.mfrr_activated_dk1, test_value)
    
    def test_mfrr_activated_dk2_property(self):
        """
        Test mfrr_activated_dk2 property
        """
        test_value = float(10.204714628586487)
        self.instance.mfrr_activated_dk2 = test_value
        self.assertEqual(self.instance.mfrr_activated_dk2, test_value)
    
    def test_imbalance_dk1_property(self):
        """
        Test imbalance_dk1 property
        """
        test_value = float(11.875638314235438)
        self.instance.imbalance_dk1 = test_value
        self.assertEqual(self.instance.imbalance_dk1, test_value)
    
    def test_imbalance_dk2_property(self):
        """
        Test imbalance_dk2 property
        """
        test_value = float(57.239866665234985)
        self.instance.imbalance_dk2 = test_value
        self.assertEqual(self.instance.imbalance_dk2, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = PowerSystemSnapshot.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = PowerSystemSnapshot.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

