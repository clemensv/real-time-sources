"""
Test case for ChargingTariff
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ndl_netherlands_producer_data.chargingtariff import ChargingTariff
from ndl_netherlands_producer_data.tarifftypeenum import TariffTypeenum
from ndl_netherlands_producer_data.tariffelement import TariffElement
import datetime


class Test_ChargingTariff(unittest.TestCase):
    """
    Test case for ChargingTariff
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_ChargingTariff.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of ChargingTariff for testing
        """
        instance = ChargingTariff(
            tariff_id='ivedrblsmiiizlnthxvu',
            country_code='ovxedpqigzfxgxfxyxto',
            party_id='coexloarsvghaiwnlxrd',
            currency='slhxidulxizpnophrdge',
            tariff_type=TariffTypeenum.AD_HOC_PAYMENT,
            tariff_alt_text='dzdwvnfgddrssokbalsj',
            tariff_alt_url='grurrqfnhugcziocqhqa',
            min_price_excl_vat=float(27.331686950390775),
            min_price_incl_vat=float(22.484057114682653),
            max_price_excl_vat=float(87.28888865996629),
            max_price_incl_vat=float(51.078490371364836),
            elements=[None, None, None, None],
            start_date_time=datetime.datetime.now(datetime.timezone.utc),
            end_date_time=datetime.datetime.now(datetime.timezone.utc),
            energy_mix_is_green_energy=False,
            last_updated=datetime.datetime.now(datetime.timezone.utc)
        )
        return instance

    
    def test_tariff_id_property(self):
        """
        Test tariff_id property
        """
        test_value = 'ivedrblsmiiizlnthxvu'
        self.instance.tariff_id = test_value
        self.assertEqual(self.instance.tariff_id, test_value)
    
    def test_country_code_property(self):
        """
        Test country_code property
        """
        test_value = 'ovxedpqigzfxgxfxyxto'
        self.instance.country_code = test_value
        self.assertEqual(self.instance.country_code, test_value)
    
    def test_party_id_property(self):
        """
        Test party_id property
        """
        test_value = 'coexloarsvghaiwnlxrd'
        self.instance.party_id = test_value
        self.assertEqual(self.instance.party_id, test_value)
    
    def test_currency_property(self):
        """
        Test currency property
        """
        test_value = 'slhxidulxizpnophrdge'
        self.instance.currency = test_value
        self.assertEqual(self.instance.currency, test_value)
    
    def test_tariff_type_property(self):
        """
        Test tariff_type property
        """
        test_value = TariffTypeenum.AD_HOC_PAYMENT
        self.instance.tariff_type = test_value
        self.assertEqual(self.instance.tariff_type, test_value)
    
    def test_tariff_alt_text_property(self):
        """
        Test tariff_alt_text property
        """
        test_value = 'dzdwvnfgddrssokbalsj'
        self.instance.tariff_alt_text = test_value
        self.assertEqual(self.instance.tariff_alt_text, test_value)
    
    def test_tariff_alt_url_property(self):
        """
        Test tariff_alt_url property
        """
        test_value = 'grurrqfnhugcziocqhqa'
        self.instance.tariff_alt_url = test_value
        self.assertEqual(self.instance.tariff_alt_url, test_value)
    
    def test_min_price_excl_vat_property(self):
        """
        Test min_price_excl_vat property
        """
        test_value = float(27.331686950390775)
        self.instance.min_price_excl_vat = test_value
        self.assertEqual(self.instance.min_price_excl_vat, test_value)
    
    def test_min_price_incl_vat_property(self):
        """
        Test min_price_incl_vat property
        """
        test_value = float(22.484057114682653)
        self.instance.min_price_incl_vat = test_value
        self.assertEqual(self.instance.min_price_incl_vat, test_value)
    
    def test_max_price_excl_vat_property(self):
        """
        Test max_price_excl_vat property
        """
        test_value = float(87.28888865996629)
        self.instance.max_price_excl_vat = test_value
        self.assertEqual(self.instance.max_price_excl_vat, test_value)
    
    def test_max_price_incl_vat_property(self):
        """
        Test max_price_incl_vat property
        """
        test_value = float(51.078490371364836)
        self.instance.max_price_incl_vat = test_value
        self.assertEqual(self.instance.max_price_incl_vat, test_value)
    
    def test_elements_property(self):
        """
        Test elements property
        """
        test_value = [None, None, None, None]
        self.instance.elements = test_value
        self.assertEqual(self.instance.elements, test_value)
    
    def test_start_date_time_property(self):
        """
        Test start_date_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.start_date_time = test_value
        self.assertEqual(self.instance.start_date_time, test_value)
    
    def test_end_date_time_property(self):
        """
        Test end_date_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.end_date_time = test_value
        self.assertEqual(self.instance.end_date_time, test_value)
    
    def test_energy_mix_is_green_energy_property(self):
        """
        Test energy_mix_is_green_energy property
        """
        test_value = False
        self.instance.energy_mix_is_green_energy = test_value
        self.assertEqual(self.instance.energy_mix_is_green_energy, test_value)
    
    def test_last_updated_property(self):
        """
        Test last_updated property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.last_updated = test_value
        self.assertEqual(self.instance.last_updated, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = ChargingTariff.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = ChargingTariff.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

