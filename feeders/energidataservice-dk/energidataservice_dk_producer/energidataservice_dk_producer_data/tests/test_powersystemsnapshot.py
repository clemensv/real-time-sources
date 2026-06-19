"""
Test case for PowerSystemSnapshot
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from energidataservice_dk_producer_data.dk.energinet.energidataservice.powersystemsnapshot import PowerSystemSnapshot


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
            minutes1_utc='qoxffoskztpxfyaoyhlz',
            minutes1_dk='ofwytlgupivnbsmqbkrq',
            price_area='gsxusezxnatvfbuxjlek',
            co2_emission=float(43.619723199225724),
            production_ge_100mw=float(69.21466224793157),
            production_lt_100mw=float(21.48160426876412),
            solar_power=float(22.706285736945265),
            offshore_wind_power=float(68.24780719171287),
            onshore_wind_power=float(17.434160359154973),
            exchange_sum=float(75.31636471542451),
            exchange_dk1_de=float(18.224375823534842),
            exchange_dk1_nl=float(81.5711231625038),
            exchange_dk1_gb=float(7.010689783219259),
            exchange_dk1_no=float(92.07254021668317),
            exchange_dk1_se=float(69.28412038702903),
            exchange_dk1_dk2=float(71.08994591248336),
            exchange_dk2_de=float(68.13961166204375),
            exchange_dk2_se=float(70.29186276747545),
            exchange_bornholm_se=float(71.32335333103924),
            afrr_activated_dk1=float(35.78320938397969),
            afrr_activated_dk2=float(37.7581668454466),
            mfrr_activated_dk1=float(27.511687258035778),
            mfrr_activated_dk2=float(63.27638371752147),
            imbalance_dk1=float(5.86351559310212),
            imbalance_dk2=float(30.727511970977027)
        )
        return instance

    
    def test_minutes1_utc_property(self):
        """
        Test minutes1_utc property
        """
        test_value = 'qoxffoskztpxfyaoyhlz'
        self.instance.minutes1_utc = test_value
        self.assertEqual(self.instance.minutes1_utc, test_value)
    
    def test_minutes1_dk_property(self):
        """
        Test minutes1_dk property
        """
        test_value = 'ofwytlgupivnbsmqbkrq'
        self.instance.minutes1_dk = test_value
        self.assertEqual(self.instance.minutes1_dk, test_value)
    
    def test_price_area_property(self):
        """
        Test price_area property
        """
        test_value = 'gsxusezxnatvfbuxjlek'
        self.instance.price_area = test_value
        self.assertEqual(self.instance.price_area, test_value)
    
    def test_co2_emission_property(self):
        """
        Test co2_emission property
        """
        test_value = float(43.619723199225724)
        self.instance.co2_emission = test_value
        self.assertEqual(self.instance.co2_emission, test_value)
    
    def test_production_ge_100mw_property(self):
        """
        Test production_ge_100mw property
        """
        test_value = float(69.21466224793157)
        self.instance.production_ge_100mw = test_value
        self.assertEqual(self.instance.production_ge_100mw, test_value)
    
    def test_production_lt_100mw_property(self):
        """
        Test production_lt_100mw property
        """
        test_value = float(21.48160426876412)
        self.instance.production_lt_100mw = test_value
        self.assertEqual(self.instance.production_lt_100mw, test_value)
    
    def test_solar_power_property(self):
        """
        Test solar_power property
        """
        test_value = float(22.706285736945265)
        self.instance.solar_power = test_value
        self.assertEqual(self.instance.solar_power, test_value)
    
    def test_offshore_wind_power_property(self):
        """
        Test offshore_wind_power property
        """
        test_value = float(68.24780719171287)
        self.instance.offshore_wind_power = test_value
        self.assertEqual(self.instance.offshore_wind_power, test_value)
    
    def test_onshore_wind_power_property(self):
        """
        Test onshore_wind_power property
        """
        test_value = float(17.434160359154973)
        self.instance.onshore_wind_power = test_value
        self.assertEqual(self.instance.onshore_wind_power, test_value)
    
    def test_exchange_sum_property(self):
        """
        Test exchange_sum property
        """
        test_value = float(75.31636471542451)
        self.instance.exchange_sum = test_value
        self.assertEqual(self.instance.exchange_sum, test_value)
    
    def test_exchange_dk1_de_property(self):
        """
        Test exchange_dk1_de property
        """
        test_value = float(18.224375823534842)
        self.instance.exchange_dk1_de = test_value
        self.assertEqual(self.instance.exchange_dk1_de, test_value)
    
    def test_exchange_dk1_nl_property(self):
        """
        Test exchange_dk1_nl property
        """
        test_value = float(81.5711231625038)
        self.instance.exchange_dk1_nl = test_value
        self.assertEqual(self.instance.exchange_dk1_nl, test_value)
    
    def test_exchange_dk1_gb_property(self):
        """
        Test exchange_dk1_gb property
        """
        test_value = float(7.010689783219259)
        self.instance.exchange_dk1_gb = test_value
        self.assertEqual(self.instance.exchange_dk1_gb, test_value)
    
    def test_exchange_dk1_no_property(self):
        """
        Test exchange_dk1_no property
        """
        test_value = float(92.07254021668317)
        self.instance.exchange_dk1_no = test_value
        self.assertEqual(self.instance.exchange_dk1_no, test_value)
    
    def test_exchange_dk1_se_property(self):
        """
        Test exchange_dk1_se property
        """
        test_value = float(69.28412038702903)
        self.instance.exchange_dk1_se = test_value
        self.assertEqual(self.instance.exchange_dk1_se, test_value)
    
    def test_exchange_dk1_dk2_property(self):
        """
        Test exchange_dk1_dk2 property
        """
        test_value = float(71.08994591248336)
        self.instance.exchange_dk1_dk2 = test_value
        self.assertEqual(self.instance.exchange_dk1_dk2, test_value)
    
    def test_exchange_dk2_de_property(self):
        """
        Test exchange_dk2_de property
        """
        test_value = float(68.13961166204375)
        self.instance.exchange_dk2_de = test_value
        self.assertEqual(self.instance.exchange_dk2_de, test_value)
    
    def test_exchange_dk2_se_property(self):
        """
        Test exchange_dk2_se property
        """
        test_value = float(70.29186276747545)
        self.instance.exchange_dk2_se = test_value
        self.assertEqual(self.instance.exchange_dk2_se, test_value)
    
    def test_exchange_bornholm_se_property(self):
        """
        Test exchange_bornholm_se property
        """
        test_value = float(71.32335333103924)
        self.instance.exchange_bornholm_se = test_value
        self.assertEqual(self.instance.exchange_bornholm_se, test_value)
    
    def test_afrr_activated_dk1_property(self):
        """
        Test afrr_activated_dk1 property
        """
        test_value = float(35.78320938397969)
        self.instance.afrr_activated_dk1 = test_value
        self.assertEqual(self.instance.afrr_activated_dk1, test_value)
    
    def test_afrr_activated_dk2_property(self):
        """
        Test afrr_activated_dk2 property
        """
        test_value = float(37.7581668454466)
        self.instance.afrr_activated_dk2 = test_value
        self.assertEqual(self.instance.afrr_activated_dk2, test_value)
    
    def test_mfrr_activated_dk1_property(self):
        """
        Test mfrr_activated_dk1 property
        """
        test_value = float(27.511687258035778)
        self.instance.mfrr_activated_dk1 = test_value
        self.assertEqual(self.instance.mfrr_activated_dk1, test_value)
    
    def test_mfrr_activated_dk2_property(self):
        """
        Test mfrr_activated_dk2 property
        """
        test_value = float(63.27638371752147)
        self.instance.mfrr_activated_dk2 = test_value
        self.assertEqual(self.instance.mfrr_activated_dk2, test_value)
    
    def test_imbalance_dk1_property(self):
        """
        Test imbalance_dk1 property
        """
        test_value = float(5.86351559310212)
        self.instance.imbalance_dk1 = test_value
        self.assertEqual(self.instance.imbalance_dk1, test_value)
    
    def test_imbalance_dk2_property(self):
        """
        Test imbalance_dk2 property
        """
        test_value = float(30.727511970977027)
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

