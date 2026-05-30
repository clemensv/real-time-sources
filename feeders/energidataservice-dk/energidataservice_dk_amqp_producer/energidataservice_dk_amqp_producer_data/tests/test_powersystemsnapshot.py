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
            minutes1_utc='xnowrijzmkeprydynxfp',
            minutes1_dk='zvfvrypxrtwhvaahhufx',
            price_area='gurexpaekulfjjbhnsth',
            co2_emission=float(54.4221258711454),
            production_ge_100mw=float(11.058698169942016),
            production_lt_100mw=float(44.665445003173076),
            solar_power=float(15.619992328540588),
            offshore_wind_power=float(94.59295236363306),
            onshore_wind_power=float(45.89142866667007),
            exchange_sum=float(90.54510115539541),
            exchange_dk1_de=float(28.40738006172694),
            exchange_dk1_nl=float(82.09600085494918),
            exchange_dk1_gb=float(5.951780748127577),
            exchange_dk1_no=float(50.33773993746399),
            exchange_dk1_se=float(78.92350323718263),
            exchange_dk1_dk2=float(62.88955510978316),
            exchange_dk2_de=float(99.4419586663112),
            exchange_dk2_se=float(98.86022886307661),
            exchange_bornholm_se=float(23.052842691248145),
            afrr_activated_dk1=float(82.33722429853219),
            afrr_activated_dk2=float(3.0787929885833343),
            mfrr_activated_dk1=float(2.1253065503733626),
            mfrr_activated_dk2=float(37.313401479086835),
            imbalance_dk1=float(25.836296044703566),
            imbalance_dk2=float(4.407689944160021)
        )
        return instance

    
    def test_minutes1_utc_property(self):
        """
        Test minutes1_utc property
        """
        test_value = 'xnowrijzmkeprydynxfp'
        self.instance.minutes1_utc = test_value
        self.assertEqual(self.instance.minutes1_utc, test_value)
    
    def test_minutes1_dk_property(self):
        """
        Test minutes1_dk property
        """
        test_value = 'zvfvrypxrtwhvaahhufx'
        self.instance.minutes1_dk = test_value
        self.assertEqual(self.instance.minutes1_dk, test_value)
    
    def test_price_area_property(self):
        """
        Test price_area property
        """
        test_value = 'gurexpaekulfjjbhnsth'
        self.instance.price_area = test_value
        self.assertEqual(self.instance.price_area, test_value)
    
    def test_co2_emission_property(self):
        """
        Test co2_emission property
        """
        test_value = float(54.4221258711454)
        self.instance.co2_emission = test_value
        self.assertEqual(self.instance.co2_emission, test_value)
    
    def test_production_ge_100mw_property(self):
        """
        Test production_ge_100mw property
        """
        test_value = float(11.058698169942016)
        self.instance.production_ge_100mw = test_value
        self.assertEqual(self.instance.production_ge_100mw, test_value)
    
    def test_production_lt_100mw_property(self):
        """
        Test production_lt_100mw property
        """
        test_value = float(44.665445003173076)
        self.instance.production_lt_100mw = test_value
        self.assertEqual(self.instance.production_lt_100mw, test_value)
    
    def test_solar_power_property(self):
        """
        Test solar_power property
        """
        test_value = float(15.619992328540588)
        self.instance.solar_power = test_value
        self.assertEqual(self.instance.solar_power, test_value)
    
    def test_offshore_wind_power_property(self):
        """
        Test offshore_wind_power property
        """
        test_value = float(94.59295236363306)
        self.instance.offshore_wind_power = test_value
        self.assertEqual(self.instance.offshore_wind_power, test_value)
    
    def test_onshore_wind_power_property(self):
        """
        Test onshore_wind_power property
        """
        test_value = float(45.89142866667007)
        self.instance.onshore_wind_power = test_value
        self.assertEqual(self.instance.onshore_wind_power, test_value)
    
    def test_exchange_sum_property(self):
        """
        Test exchange_sum property
        """
        test_value = float(90.54510115539541)
        self.instance.exchange_sum = test_value
        self.assertEqual(self.instance.exchange_sum, test_value)
    
    def test_exchange_dk1_de_property(self):
        """
        Test exchange_dk1_de property
        """
        test_value = float(28.40738006172694)
        self.instance.exchange_dk1_de = test_value
        self.assertEqual(self.instance.exchange_dk1_de, test_value)
    
    def test_exchange_dk1_nl_property(self):
        """
        Test exchange_dk1_nl property
        """
        test_value = float(82.09600085494918)
        self.instance.exchange_dk1_nl = test_value
        self.assertEqual(self.instance.exchange_dk1_nl, test_value)
    
    def test_exchange_dk1_gb_property(self):
        """
        Test exchange_dk1_gb property
        """
        test_value = float(5.951780748127577)
        self.instance.exchange_dk1_gb = test_value
        self.assertEqual(self.instance.exchange_dk1_gb, test_value)
    
    def test_exchange_dk1_no_property(self):
        """
        Test exchange_dk1_no property
        """
        test_value = float(50.33773993746399)
        self.instance.exchange_dk1_no = test_value
        self.assertEqual(self.instance.exchange_dk1_no, test_value)
    
    def test_exchange_dk1_se_property(self):
        """
        Test exchange_dk1_se property
        """
        test_value = float(78.92350323718263)
        self.instance.exchange_dk1_se = test_value
        self.assertEqual(self.instance.exchange_dk1_se, test_value)
    
    def test_exchange_dk1_dk2_property(self):
        """
        Test exchange_dk1_dk2 property
        """
        test_value = float(62.88955510978316)
        self.instance.exchange_dk1_dk2 = test_value
        self.assertEqual(self.instance.exchange_dk1_dk2, test_value)
    
    def test_exchange_dk2_de_property(self):
        """
        Test exchange_dk2_de property
        """
        test_value = float(99.4419586663112)
        self.instance.exchange_dk2_de = test_value
        self.assertEqual(self.instance.exchange_dk2_de, test_value)
    
    def test_exchange_dk2_se_property(self):
        """
        Test exchange_dk2_se property
        """
        test_value = float(98.86022886307661)
        self.instance.exchange_dk2_se = test_value
        self.assertEqual(self.instance.exchange_dk2_se, test_value)
    
    def test_exchange_bornholm_se_property(self):
        """
        Test exchange_bornholm_se property
        """
        test_value = float(23.052842691248145)
        self.instance.exchange_bornholm_se = test_value
        self.assertEqual(self.instance.exchange_bornholm_se, test_value)
    
    def test_afrr_activated_dk1_property(self):
        """
        Test afrr_activated_dk1 property
        """
        test_value = float(82.33722429853219)
        self.instance.afrr_activated_dk1 = test_value
        self.assertEqual(self.instance.afrr_activated_dk1, test_value)
    
    def test_afrr_activated_dk2_property(self):
        """
        Test afrr_activated_dk2 property
        """
        test_value = float(3.0787929885833343)
        self.instance.afrr_activated_dk2 = test_value
        self.assertEqual(self.instance.afrr_activated_dk2, test_value)
    
    def test_mfrr_activated_dk1_property(self):
        """
        Test mfrr_activated_dk1 property
        """
        test_value = float(2.1253065503733626)
        self.instance.mfrr_activated_dk1 = test_value
        self.assertEqual(self.instance.mfrr_activated_dk1, test_value)
    
    def test_mfrr_activated_dk2_property(self):
        """
        Test mfrr_activated_dk2 property
        """
        test_value = float(37.313401479086835)
        self.instance.mfrr_activated_dk2 = test_value
        self.assertEqual(self.instance.mfrr_activated_dk2, test_value)
    
    def test_imbalance_dk1_property(self):
        """
        Test imbalance_dk1 property
        """
        test_value = float(25.836296044703566)
        self.instance.imbalance_dk1 = test_value
        self.assertEqual(self.instance.imbalance_dk1, test_value)
    
    def test_imbalance_dk2_property(self):
        """
        Test imbalance_dk2 property
        """
        test_value = float(4.407689944160021)
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

