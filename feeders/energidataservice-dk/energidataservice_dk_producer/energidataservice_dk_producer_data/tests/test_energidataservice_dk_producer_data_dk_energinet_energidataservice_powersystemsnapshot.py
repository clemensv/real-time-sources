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
            minutes1_utc='riipjfmledwylphoaldg',
            minutes1_dk='yuwjxhxbrnxpuxvmrasu',
            price_area='qhwnabieswxyrpbbixrj',
            co2_emission=float(64.30065060379036),
            production_ge_100mw=float(92.0410853611208),
            production_lt_100mw=float(47.63347401939112),
            solar_power=float(22.156519246916083),
            offshore_wind_power=float(25.92833823158882),
            onshore_wind_power=float(69.7450795153061),
            exchange_sum=float(57.98446047272091),
            exchange_dk1_de=float(10.55513206187918),
            exchange_dk1_nl=float(0.9788084863047164),
            exchange_dk1_gb=float(6.53819072642462),
            exchange_dk1_no=float(84.83503826449002),
            exchange_dk1_se=float(57.616139303466795),
            exchange_dk1_dk2=float(92.4552440987605),
            exchange_dk2_de=float(26.39617456417801),
            exchange_dk2_se=float(40.121382344523695),
            exchange_bornholm_se=float(30.133469041335616),
            afrr_activated_dk1=float(73.92151357458937),
            afrr_activated_dk2=float(77.72579092763675),
            mfrr_activated_dk1=float(9.267098777616066),
            mfrr_activated_dk2=float(44.389176119685494),
            imbalance_dk1=float(80.09453498374818),
            imbalance_dk2=float(48.760181357536794)
        )
        return instance


    def test_minutes1_utc_property(self):
        """
        Test minutes1_utc property
        """
        test_value = 'riipjfmledwylphoaldg'
        self.instance.minutes1_utc = test_value
        self.assertEqual(self.instance.minutes1_utc, test_value)

    def test_minutes1_dk_property(self):
        """
        Test minutes1_dk property
        """
        test_value = 'yuwjxhxbrnxpuxvmrasu'
        self.instance.minutes1_dk = test_value
        self.assertEqual(self.instance.minutes1_dk, test_value)

    def test_price_area_property(self):
        """
        Test price_area property
        """
        test_value = 'qhwnabieswxyrpbbixrj'
        self.instance.price_area = test_value
        self.assertEqual(self.instance.price_area, test_value)

    def test_co2_emission_property(self):
        """
        Test co2_emission property
        """
        test_value = float(64.30065060379036)
        self.instance.co2_emission = test_value
        self.assertEqual(self.instance.co2_emission, test_value)

    def test_production_ge_100mw_property(self):
        """
        Test production_ge_100mw property
        """
        test_value = float(92.0410853611208)
        self.instance.production_ge_100mw = test_value
        self.assertEqual(self.instance.production_ge_100mw, test_value)

    def test_production_lt_100mw_property(self):
        """
        Test production_lt_100mw property
        """
        test_value = float(47.63347401939112)
        self.instance.production_lt_100mw = test_value
        self.assertEqual(self.instance.production_lt_100mw, test_value)

    def test_solar_power_property(self):
        """
        Test solar_power property
        """
        test_value = float(22.156519246916083)
        self.instance.solar_power = test_value
        self.assertEqual(self.instance.solar_power, test_value)

    def test_offshore_wind_power_property(self):
        """
        Test offshore_wind_power property
        """
        test_value = float(25.92833823158882)
        self.instance.offshore_wind_power = test_value
        self.assertEqual(self.instance.offshore_wind_power, test_value)

    def test_onshore_wind_power_property(self):
        """
        Test onshore_wind_power property
        """
        test_value = float(69.7450795153061)
        self.instance.onshore_wind_power = test_value
        self.assertEqual(self.instance.onshore_wind_power, test_value)

    def test_exchange_sum_property(self):
        """
        Test exchange_sum property
        """
        test_value = float(57.98446047272091)
        self.instance.exchange_sum = test_value
        self.assertEqual(self.instance.exchange_sum, test_value)

    def test_exchange_dk1_de_property(self):
        """
        Test exchange_dk1_de property
        """
        test_value = float(10.55513206187918)
        self.instance.exchange_dk1_de = test_value
        self.assertEqual(self.instance.exchange_dk1_de, test_value)

    def test_exchange_dk1_nl_property(self):
        """
        Test exchange_dk1_nl property
        """
        test_value = float(0.9788084863047164)
        self.instance.exchange_dk1_nl = test_value
        self.assertEqual(self.instance.exchange_dk1_nl, test_value)

    def test_exchange_dk1_gb_property(self):
        """
        Test exchange_dk1_gb property
        """
        test_value = float(6.53819072642462)
        self.instance.exchange_dk1_gb = test_value
        self.assertEqual(self.instance.exchange_dk1_gb, test_value)

    def test_exchange_dk1_no_property(self):
        """
        Test exchange_dk1_no property
        """
        test_value = float(84.83503826449002)
        self.instance.exchange_dk1_no = test_value
        self.assertEqual(self.instance.exchange_dk1_no, test_value)

    def test_exchange_dk1_se_property(self):
        """
        Test exchange_dk1_se property
        """
        test_value = float(57.616139303466795)
        self.instance.exchange_dk1_se = test_value
        self.assertEqual(self.instance.exchange_dk1_se, test_value)

    def test_exchange_dk1_dk2_property(self):
        """
        Test exchange_dk1_dk2 property
        """
        test_value = float(92.4552440987605)
        self.instance.exchange_dk1_dk2 = test_value
        self.assertEqual(self.instance.exchange_dk1_dk2, test_value)

    def test_exchange_dk2_de_property(self):
        """
        Test exchange_dk2_de property
        """
        test_value = float(26.39617456417801)
        self.instance.exchange_dk2_de = test_value
        self.assertEqual(self.instance.exchange_dk2_de, test_value)

    def test_exchange_dk2_se_property(self):
        """
        Test exchange_dk2_se property
        """
        test_value = float(40.121382344523695)
        self.instance.exchange_dk2_se = test_value
        self.assertEqual(self.instance.exchange_dk2_se, test_value)

    def test_exchange_bornholm_se_property(self):
        """
        Test exchange_bornholm_se property
        """
        test_value = float(30.133469041335616)
        self.instance.exchange_bornholm_se = test_value
        self.assertEqual(self.instance.exchange_bornholm_se, test_value)

    def test_afrr_activated_dk1_property(self):
        """
        Test afrr_activated_dk1 property
        """
        test_value = float(73.92151357458937)
        self.instance.afrr_activated_dk1 = test_value
        self.assertEqual(self.instance.afrr_activated_dk1, test_value)

    def test_afrr_activated_dk2_property(self):
        """
        Test afrr_activated_dk2 property
        """
        test_value = float(77.72579092763675)
        self.instance.afrr_activated_dk2 = test_value
        self.assertEqual(self.instance.afrr_activated_dk2, test_value)

    def test_mfrr_activated_dk1_property(self):
        """
        Test mfrr_activated_dk1 property
        """
        test_value = float(9.267098777616066)
        self.instance.mfrr_activated_dk1 = test_value
        self.assertEqual(self.instance.mfrr_activated_dk1, test_value)

    def test_mfrr_activated_dk2_property(self):
        """
        Test mfrr_activated_dk2 property
        """
        test_value = float(44.389176119685494)
        self.instance.mfrr_activated_dk2 = test_value
        self.assertEqual(self.instance.mfrr_activated_dk2, test_value)

    def test_imbalance_dk1_property(self):
        """
        Test imbalance_dk1 property
        """
        test_value = float(80.09453498374818)
        self.instance.imbalance_dk1 = test_value
        self.assertEqual(self.instance.imbalance_dk1, test_value)

    def test_imbalance_dk2_property(self):
        """
        Test imbalance_dk2 property
        """
        test_value = float(48.760181357536794)
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
