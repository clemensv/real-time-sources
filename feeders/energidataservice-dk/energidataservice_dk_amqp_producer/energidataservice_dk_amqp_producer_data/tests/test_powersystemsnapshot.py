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
            minutes1_utc='bpxiuowbrlrcuxjocfzm',
            minutes1_dk='xnpmttendvylxokvzzgy',
            price_area='rbwthmrsmjgdcqwjjisn',
            co2_emission=float(62.96444384519493),
            production_ge_100mw=float(27.482452791616907),
            production_lt_100mw=float(2.266522255847636),
            solar_power=float(8.40200205592735),
            offshore_wind_power=float(78.33569713820914),
            onshore_wind_power=float(19.72640995072904),
            exchange_sum=float(10.649610701120448),
            exchange_dk1_de=float(57.74585996879813),
            exchange_dk1_nl=float(64.86126603815438),
            exchange_dk1_gb=float(43.74928833043077),
            exchange_dk1_no=float(41.094335512383886),
            exchange_dk1_se=float(59.31998283039768),
            exchange_dk1_dk2=float(6.976521734783036),
            exchange_dk2_de=float(64.7357436212105),
            exchange_dk2_se=float(3.7757852788593893),
            exchange_bornholm_se=float(39.86076993290081),
            afrr_activated_dk1=float(34.847326861887865),
            afrr_activated_dk2=float(23.81896403943722),
            mfrr_activated_dk1=float(35.06633366373014),
            mfrr_activated_dk2=float(85.9858486451197),
            imbalance_dk1=float(58.570552214357186),
            imbalance_dk2=float(43.40503041488244)
        )
        return instance

    
    def test_minutes1_utc_property(self):
        """
        Test minutes1_utc property
        """
        test_value = 'bpxiuowbrlrcuxjocfzm'
        self.instance.minutes1_utc = test_value
        self.assertEqual(self.instance.minutes1_utc, test_value)
    
    def test_minutes1_dk_property(self):
        """
        Test minutes1_dk property
        """
        test_value = 'xnpmttendvylxokvzzgy'
        self.instance.minutes1_dk = test_value
        self.assertEqual(self.instance.minutes1_dk, test_value)
    
    def test_price_area_property(self):
        """
        Test price_area property
        """
        test_value = 'rbwthmrsmjgdcqwjjisn'
        self.instance.price_area = test_value
        self.assertEqual(self.instance.price_area, test_value)
    
    def test_co2_emission_property(self):
        """
        Test co2_emission property
        """
        test_value = float(62.96444384519493)
        self.instance.co2_emission = test_value
        self.assertEqual(self.instance.co2_emission, test_value)
    
    def test_production_ge_100mw_property(self):
        """
        Test production_ge_100mw property
        """
        test_value = float(27.482452791616907)
        self.instance.production_ge_100mw = test_value
        self.assertEqual(self.instance.production_ge_100mw, test_value)
    
    def test_production_lt_100mw_property(self):
        """
        Test production_lt_100mw property
        """
        test_value = float(2.266522255847636)
        self.instance.production_lt_100mw = test_value
        self.assertEqual(self.instance.production_lt_100mw, test_value)
    
    def test_solar_power_property(self):
        """
        Test solar_power property
        """
        test_value = float(8.40200205592735)
        self.instance.solar_power = test_value
        self.assertEqual(self.instance.solar_power, test_value)
    
    def test_offshore_wind_power_property(self):
        """
        Test offshore_wind_power property
        """
        test_value = float(78.33569713820914)
        self.instance.offshore_wind_power = test_value
        self.assertEqual(self.instance.offshore_wind_power, test_value)
    
    def test_onshore_wind_power_property(self):
        """
        Test onshore_wind_power property
        """
        test_value = float(19.72640995072904)
        self.instance.onshore_wind_power = test_value
        self.assertEqual(self.instance.onshore_wind_power, test_value)
    
    def test_exchange_sum_property(self):
        """
        Test exchange_sum property
        """
        test_value = float(10.649610701120448)
        self.instance.exchange_sum = test_value
        self.assertEqual(self.instance.exchange_sum, test_value)
    
    def test_exchange_dk1_de_property(self):
        """
        Test exchange_dk1_de property
        """
        test_value = float(57.74585996879813)
        self.instance.exchange_dk1_de = test_value
        self.assertEqual(self.instance.exchange_dk1_de, test_value)
    
    def test_exchange_dk1_nl_property(self):
        """
        Test exchange_dk1_nl property
        """
        test_value = float(64.86126603815438)
        self.instance.exchange_dk1_nl = test_value
        self.assertEqual(self.instance.exchange_dk1_nl, test_value)
    
    def test_exchange_dk1_gb_property(self):
        """
        Test exchange_dk1_gb property
        """
        test_value = float(43.74928833043077)
        self.instance.exchange_dk1_gb = test_value
        self.assertEqual(self.instance.exchange_dk1_gb, test_value)
    
    def test_exchange_dk1_no_property(self):
        """
        Test exchange_dk1_no property
        """
        test_value = float(41.094335512383886)
        self.instance.exchange_dk1_no = test_value
        self.assertEqual(self.instance.exchange_dk1_no, test_value)
    
    def test_exchange_dk1_se_property(self):
        """
        Test exchange_dk1_se property
        """
        test_value = float(59.31998283039768)
        self.instance.exchange_dk1_se = test_value
        self.assertEqual(self.instance.exchange_dk1_se, test_value)
    
    def test_exchange_dk1_dk2_property(self):
        """
        Test exchange_dk1_dk2 property
        """
        test_value = float(6.976521734783036)
        self.instance.exchange_dk1_dk2 = test_value
        self.assertEqual(self.instance.exchange_dk1_dk2, test_value)
    
    def test_exchange_dk2_de_property(self):
        """
        Test exchange_dk2_de property
        """
        test_value = float(64.7357436212105)
        self.instance.exchange_dk2_de = test_value
        self.assertEqual(self.instance.exchange_dk2_de, test_value)
    
    def test_exchange_dk2_se_property(self):
        """
        Test exchange_dk2_se property
        """
        test_value = float(3.7757852788593893)
        self.instance.exchange_dk2_se = test_value
        self.assertEqual(self.instance.exchange_dk2_se, test_value)
    
    def test_exchange_bornholm_se_property(self):
        """
        Test exchange_bornholm_se property
        """
        test_value = float(39.86076993290081)
        self.instance.exchange_bornholm_se = test_value
        self.assertEqual(self.instance.exchange_bornholm_se, test_value)
    
    def test_afrr_activated_dk1_property(self):
        """
        Test afrr_activated_dk1 property
        """
        test_value = float(34.847326861887865)
        self.instance.afrr_activated_dk1 = test_value
        self.assertEqual(self.instance.afrr_activated_dk1, test_value)
    
    def test_afrr_activated_dk2_property(self):
        """
        Test afrr_activated_dk2 property
        """
        test_value = float(23.81896403943722)
        self.instance.afrr_activated_dk2 = test_value
        self.assertEqual(self.instance.afrr_activated_dk2, test_value)
    
    def test_mfrr_activated_dk1_property(self):
        """
        Test mfrr_activated_dk1 property
        """
        test_value = float(35.06633366373014)
        self.instance.mfrr_activated_dk1 = test_value
        self.assertEqual(self.instance.mfrr_activated_dk1, test_value)
    
    def test_mfrr_activated_dk2_property(self):
        """
        Test mfrr_activated_dk2 property
        """
        test_value = float(85.9858486451197)
        self.instance.mfrr_activated_dk2 = test_value
        self.assertEqual(self.instance.mfrr_activated_dk2, test_value)
    
    def test_imbalance_dk1_property(self):
        """
        Test imbalance_dk1 property
        """
        test_value = float(58.570552214357186)
        self.instance.imbalance_dk1 = test_value
        self.assertEqual(self.instance.imbalance_dk1, test_value)
    
    def test_imbalance_dk2_property(self):
        """
        Test imbalance_dk2 property
        """
        test_value = float(43.40503041488244)
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

