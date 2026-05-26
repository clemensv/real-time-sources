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
            minutes1_utc='ergiowpxpqjlxsbfrril',
            minutes1_dk='cklvhxlkbuffnlgitzuo',
            price_area='oielslmejtooftnpvgql',
            co2_emission=float(92.74683384671059),
            production_ge_100mw=float(3.9276839494905125),
            production_lt_100mw=float(61.74356311732541),
            solar_power=float(12.254584499585164),
            offshore_wind_power=float(11.161324120166839),
            onshore_wind_power=float(75.62076668743674),
            exchange_sum=float(32.550597937550464),
            exchange_dk1_de=float(50.36717679006644),
            exchange_dk1_nl=float(5.589920714631291),
            exchange_dk1_gb=float(81.22272955199008),
            exchange_dk1_no=float(59.68922792743613),
            exchange_dk1_se=float(15.726948513056648),
            exchange_dk1_dk2=float(95.48981776479883),
            exchange_dk2_de=float(88.90974759562334),
            exchange_dk2_se=float(71.18183226588916),
            exchange_bornholm_se=float(10.421661267979543),
            afrr_activated_dk1=float(91.1077286344693),
            afrr_activated_dk2=float(46.88652695691855),
            mfrr_activated_dk1=float(5.4804902100874635),
            mfrr_activated_dk2=float(15.76856113736027),
            imbalance_dk1=float(55.67114794466489),
            imbalance_dk2=float(83.02422994454872)
        )
        return instance


    def test_minutes1_utc_property(self):
        """
        Test minutes1_utc property
        """
        test_value = 'ergiowpxpqjlxsbfrril'
        self.instance.minutes1_utc = test_value
        self.assertEqual(self.instance.minutes1_utc, test_value)

    def test_minutes1_dk_property(self):
        """
        Test minutes1_dk property
        """
        test_value = 'cklvhxlkbuffnlgitzuo'
        self.instance.minutes1_dk = test_value
        self.assertEqual(self.instance.minutes1_dk, test_value)

    def test_price_area_property(self):
        """
        Test price_area property
        """
        test_value = 'oielslmejtooftnpvgql'
        self.instance.price_area = test_value
        self.assertEqual(self.instance.price_area, test_value)

    def test_co2_emission_property(self):
        """
        Test co2_emission property
        """
        test_value = float(92.74683384671059)
        self.instance.co2_emission = test_value
        self.assertEqual(self.instance.co2_emission, test_value)

    def test_production_ge_100mw_property(self):
        """
        Test production_ge_100mw property
        """
        test_value = float(3.9276839494905125)
        self.instance.production_ge_100mw = test_value
        self.assertEqual(self.instance.production_ge_100mw, test_value)

    def test_production_lt_100mw_property(self):
        """
        Test production_lt_100mw property
        """
        test_value = float(61.74356311732541)
        self.instance.production_lt_100mw = test_value
        self.assertEqual(self.instance.production_lt_100mw, test_value)

    def test_solar_power_property(self):
        """
        Test solar_power property
        """
        test_value = float(12.254584499585164)
        self.instance.solar_power = test_value
        self.assertEqual(self.instance.solar_power, test_value)

    def test_offshore_wind_power_property(self):
        """
        Test offshore_wind_power property
        """
        test_value = float(11.161324120166839)
        self.instance.offshore_wind_power = test_value
        self.assertEqual(self.instance.offshore_wind_power, test_value)

    def test_onshore_wind_power_property(self):
        """
        Test onshore_wind_power property
        """
        test_value = float(75.62076668743674)
        self.instance.onshore_wind_power = test_value
        self.assertEqual(self.instance.onshore_wind_power, test_value)

    def test_exchange_sum_property(self):
        """
        Test exchange_sum property
        """
        test_value = float(32.550597937550464)
        self.instance.exchange_sum = test_value
        self.assertEqual(self.instance.exchange_sum, test_value)

    def test_exchange_dk1_de_property(self):
        """
        Test exchange_dk1_de property
        """
        test_value = float(50.36717679006644)
        self.instance.exchange_dk1_de = test_value
        self.assertEqual(self.instance.exchange_dk1_de, test_value)

    def test_exchange_dk1_nl_property(self):
        """
        Test exchange_dk1_nl property
        """
        test_value = float(5.589920714631291)
        self.instance.exchange_dk1_nl = test_value
        self.assertEqual(self.instance.exchange_dk1_nl, test_value)

    def test_exchange_dk1_gb_property(self):
        """
        Test exchange_dk1_gb property
        """
        test_value = float(81.22272955199008)
        self.instance.exchange_dk1_gb = test_value
        self.assertEqual(self.instance.exchange_dk1_gb, test_value)

    def test_exchange_dk1_no_property(self):
        """
        Test exchange_dk1_no property
        """
        test_value = float(59.68922792743613)
        self.instance.exchange_dk1_no = test_value
        self.assertEqual(self.instance.exchange_dk1_no, test_value)

    def test_exchange_dk1_se_property(self):
        """
        Test exchange_dk1_se property
        """
        test_value = float(15.726948513056648)
        self.instance.exchange_dk1_se = test_value
        self.assertEqual(self.instance.exchange_dk1_se, test_value)

    def test_exchange_dk1_dk2_property(self):
        """
        Test exchange_dk1_dk2 property
        """
        test_value = float(95.48981776479883)
        self.instance.exchange_dk1_dk2 = test_value
        self.assertEqual(self.instance.exchange_dk1_dk2, test_value)

    def test_exchange_dk2_de_property(self):
        """
        Test exchange_dk2_de property
        """
        test_value = float(88.90974759562334)
        self.instance.exchange_dk2_de = test_value
        self.assertEqual(self.instance.exchange_dk2_de, test_value)

    def test_exchange_dk2_se_property(self):
        """
        Test exchange_dk2_se property
        """
        test_value = float(71.18183226588916)
        self.instance.exchange_dk2_se = test_value
        self.assertEqual(self.instance.exchange_dk2_se, test_value)

    def test_exchange_bornholm_se_property(self):
        """
        Test exchange_bornholm_se property
        """
        test_value = float(10.421661267979543)
        self.instance.exchange_bornholm_se = test_value
        self.assertEqual(self.instance.exchange_bornholm_se, test_value)

    def test_afrr_activated_dk1_property(self):
        """
        Test afrr_activated_dk1 property
        """
        test_value = float(91.1077286344693)
        self.instance.afrr_activated_dk1 = test_value
        self.assertEqual(self.instance.afrr_activated_dk1, test_value)

    def test_afrr_activated_dk2_property(self):
        """
        Test afrr_activated_dk2 property
        """
        test_value = float(46.88652695691855)
        self.instance.afrr_activated_dk2 = test_value
        self.assertEqual(self.instance.afrr_activated_dk2, test_value)

    def test_mfrr_activated_dk1_property(self):
        """
        Test mfrr_activated_dk1 property
        """
        test_value = float(5.4804902100874635)
        self.instance.mfrr_activated_dk1 = test_value
        self.assertEqual(self.instance.mfrr_activated_dk1, test_value)

    def test_mfrr_activated_dk2_property(self):
        """
        Test mfrr_activated_dk2 property
        """
        test_value = float(15.76856113736027)
        self.instance.mfrr_activated_dk2 = test_value
        self.assertEqual(self.instance.mfrr_activated_dk2, test_value)

    def test_imbalance_dk1_property(self):
        """
        Test imbalance_dk1 property
        """
        test_value = float(55.67114794466489)
        self.instance.imbalance_dk1 = test_value
        self.assertEqual(self.instance.imbalance_dk1, test_value)

    def test_imbalance_dk2_property(self):
        """
        Test imbalance_dk2 property
        """
        test_value = float(83.02422994454872)
        self.instance.imbalance_dk2 = test_value
        self.assertEqual(self.instance.imbalance_dk2, test_value)

    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = PowerSystemSnapshot.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
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

