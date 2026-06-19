"""
Test case for PowerSystemSnapshot
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from energidataservice_dk_mqtt_producer_data.dk.energinet.energidataservice.powersystemsnapshot import PowerSystemSnapshot


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
            minutes1_utc='zwqsjxnpvpprpllcfcas',
            minutes1_dk='dyxgmkymhruueixatpav',
            price_area='iriwuozlxqrupvysacya',
            co2_emission=float(13.25560062497143),
            production_ge_100mw=float(30.0189815485563),
            production_lt_100mw=float(7.62871942335156),
            solar_power=float(97.05486751076351),
            offshore_wind_power=float(77.97636915623322),
            onshore_wind_power=float(7.255382320037363),
            exchange_sum=float(0.6975648221509534),
            exchange_dk1_de=float(34.05795137744712),
            exchange_dk1_nl=float(49.32342256984265),
            exchange_dk1_gb=float(5.776449589804599),
            exchange_dk1_no=float(48.59671803350585),
            exchange_dk1_se=float(83.97289932578333),
            exchange_dk1_dk2=float(39.60142641421709),
            exchange_dk2_de=float(71.60788930689814),
            exchange_dk2_se=float(69.29354221420645),
            exchange_bornholm_se=float(82.20131312779421),
            afrr_activated_dk1=float(93.2773039505012),
            afrr_activated_dk2=float(14.17585881180522),
            mfrr_activated_dk1=float(28.831133563494404),
            mfrr_activated_dk2=float(19.596170149556823),
            imbalance_dk1=float(59.50444295633815),
            imbalance_dk2=float(45.632467487704666)
        )
        return instance

    
    def test_minutes1_utc_property(self):
        """
        Test minutes1_utc property
        """
        test_value = 'zwqsjxnpvpprpllcfcas'
        self.instance.minutes1_utc = test_value
        self.assertEqual(self.instance.minutes1_utc, test_value)
    
    def test_minutes1_dk_property(self):
        """
        Test minutes1_dk property
        """
        test_value = 'dyxgmkymhruueixatpav'
        self.instance.minutes1_dk = test_value
        self.assertEqual(self.instance.minutes1_dk, test_value)
    
    def test_price_area_property(self):
        """
        Test price_area property
        """
        test_value = 'iriwuozlxqrupvysacya'
        self.instance.price_area = test_value
        self.assertEqual(self.instance.price_area, test_value)
    
    def test_co2_emission_property(self):
        """
        Test co2_emission property
        """
        test_value = float(13.25560062497143)
        self.instance.co2_emission = test_value
        self.assertEqual(self.instance.co2_emission, test_value)
    
    def test_production_ge_100mw_property(self):
        """
        Test production_ge_100mw property
        """
        test_value = float(30.0189815485563)
        self.instance.production_ge_100mw = test_value
        self.assertEqual(self.instance.production_ge_100mw, test_value)
    
    def test_production_lt_100mw_property(self):
        """
        Test production_lt_100mw property
        """
        test_value = float(7.62871942335156)
        self.instance.production_lt_100mw = test_value
        self.assertEqual(self.instance.production_lt_100mw, test_value)
    
    def test_solar_power_property(self):
        """
        Test solar_power property
        """
        test_value = float(97.05486751076351)
        self.instance.solar_power = test_value
        self.assertEqual(self.instance.solar_power, test_value)
    
    def test_offshore_wind_power_property(self):
        """
        Test offshore_wind_power property
        """
        test_value = float(77.97636915623322)
        self.instance.offshore_wind_power = test_value
        self.assertEqual(self.instance.offshore_wind_power, test_value)
    
    def test_onshore_wind_power_property(self):
        """
        Test onshore_wind_power property
        """
        test_value = float(7.255382320037363)
        self.instance.onshore_wind_power = test_value
        self.assertEqual(self.instance.onshore_wind_power, test_value)
    
    def test_exchange_sum_property(self):
        """
        Test exchange_sum property
        """
        test_value = float(0.6975648221509534)
        self.instance.exchange_sum = test_value
        self.assertEqual(self.instance.exchange_sum, test_value)
    
    def test_exchange_dk1_de_property(self):
        """
        Test exchange_dk1_de property
        """
        test_value = float(34.05795137744712)
        self.instance.exchange_dk1_de = test_value
        self.assertEqual(self.instance.exchange_dk1_de, test_value)
    
    def test_exchange_dk1_nl_property(self):
        """
        Test exchange_dk1_nl property
        """
        test_value = float(49.32342256984265)
        self.instance.exchange_dk1_nl = test_value
        self.assertEqual(self.instance.exchange_dk1_nl, test_value)
    
    def test_exchange_dk1_gb_property(self):
        """
        Test exchange_dk1_gb property
        """
        test_value = float(5.776449589804599)
        self.instance.exchange_dk1_gb = test_value
        self.assertEqual(self.instance.exchange_dk1_gb, test_value)
    
    def test_exchange_dk1_no_property(self):
        """
        Test exchange_dk1_no property
        """
        test_value = float(48.59671803350585)
        self.instance.exchange_dk1_no = test_value
        self.assertEqual(self.instance.exchange_dk1_no, test_value)
    
    def test_exchange_dk1_se_property(self):
        """
        Test exchange_dk1_se property
        """
        test_value = float(83.97289932578333)
        self.instance.exchange_dk1_se = test_value
        self.assertEqual(self.instance.exchange_dk1_se, test_value)
    
    def test_exchange_dk1_dk2_property(self):
        """
        Test exchange_dk1_dk2 property
        """
        test_value = float(39.60142641421709)
        self.instance.exchange_dk1_dk2 = test_value
        self.assertEqual(self.instance.exchange_dk1_dk2, test_value)
    
    def test_exchange_dk2_de_property(self):
        """
        Test exchange_dk2_de property
        """
        test_value = float(71.60788930689814)
        self.instance.exchange_dk2_de = test_value
        self.assertEqual(self.instance.exchange_dk2_de, test_value)
    
    def test_exchange_dk2_se_property(self):
        """
        Test exchange_dk2_se property
        """
        test_value = float(69.29354221420645)
        self.instance.exchange_dk2_se = test_value
        self.assertEqual(self.instance.exchange_dk2_se, test_value)
    
    def test_exchange_bornholm_se_property(self):
        """
        Test exchange_bornholm_se property
        """
        test_value = float(82.20131312779421)
        self.instance.exchange_bornholm_se = test_value
        self.assertEqual(self.instance.exchange_bornholm_se, test_value)
    
    def test_afrr_activated_dk1_property(self):
        """
        Test afrr_activated_dk1 property
        """
        test_value = float(93.2773039505012)
        self.instance.afrr_activated_dk1 = test_value
        self.assertEqual(self.instance.afrr_activated_dk1, test_value)
    
    def test_afrr_activated_dk2_property(self):
        """
        Test afrr_activated_dk2 property
        """
        test_value = float(14.17585881180522)
        self.instance.afrr_activated_dk2 = test_value
        self.assertEqual(self.instance.afrr_activated_dk2, test_value)
    
    def test_mfrr_activated_dk1_property(self):
        """
        Test mfrr_activated_dk1 property
        """
        test_value = float(28.831133563494404)
        self.instance.mfrr_activated_dk1 = test_value
        self.assertEqual(self.instance.mfrr_activated_dk1, test_value)
    
    def test_mfrr_activated_dk2_property(self):
        """
        Test mfrr_activated_dk2 property
        """
        test_value = float(19.596170149556823)
        self.instance.mfrr_activated_dk2 = test_value
        self.assertEqual(self.instance.mfrr_activated_dk2, test_value)
    
    def test_imbalance_dk1_property(self):
        """
        Test imbalance_dk1 property
        """
        test_value = float(59.50444295633815)
        self.instance.imbalance_dk1 = test_value
        self.assertEqual(self.instance.imbalance_dk1, test_value)
    
    def test_imbalance_dk2_property(self):
        """
        Test imbalance_dk2 property
        """
        test_value = float(45.632467487704666)
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

