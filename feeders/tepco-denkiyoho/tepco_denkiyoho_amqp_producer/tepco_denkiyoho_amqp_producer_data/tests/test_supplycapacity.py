"""
Test case for SupplyCapacity
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from tepco_denkiyoho_amqp_producer_data.jp.tepco.denkiyoho.supplycapacity import SupplyCapacity
import datetime


class Test_SupplyCapacity(unittest.TestCase):
    """
    Test case for SupplyCapacity
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_SupplyCapacity.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of SupplyCapacity for testing
        """
        instance = SupplyCapacity(
            date=datetime.date.today(),
            time='urcpxazszpwzgbhzdikp',
            peak_supply_capacity_mw=float(30.974427990982857),
            peak_supply_capacity_jp_unit_value=int(95),
            peak_time_slot='lzktnqdglkheenewisvj',
            peak_reserve_margin_pct=float(70.26569102202266),
            peak_usage_pct=float(99.16924923296624),
            daily_max_usage_pct=float(29.28137839192836),
            daily_max_usage_time_slot='yyqypkyykmqdyuxpjqlq',
            update_datetime=datetime.datetime.now(datetime.timezone.utc),
            update_datetime_local=datetime.datetime.now(datetime.timezone.utc),
            area_code='yzuhxikwaomhexccaywv',
            area_name_jp='scfmexwwvzymgyfhnqvu',
            area_name_en='ylgzeymhvildpmqspiwh'
        )
        return instance

    
    def test_date_property(self):
        """
        Test date property
        """
        test_value = datetime.date.today()
        self.instance.date = test_value
        self.assertEqual(self.instance.date, test_value)
    
    def test_time_property(self):
        """
        Test time property
        """
        test_value = 'urcpxazszpwzgbhzdikp'
        self.instance.time = test_value
        self.assertEqual(self.instance.time, test_value)
    
    def test_peak_supply_capacity_mw_property(self):
        """
        Test peak_supply_capacity_mw property
        """
        test_value = float(30.974427990982857)
        self.instance.peak_supply_capacity_mw = test_value
        self.assertEqual(self.instance.peak_supply_capacity_mw, test_value)
    
    def test_peak_supply_capacity_jp_unit_value_property(self):
        """
        Test peak_supply_capacity_jp_unit_value property
        """
        test_value = int(95)
        self.instance.peak_supply_capacity_jp_unit_value = test_value
        self.assertEqual(self.instance.peak_supply_capacity_jp_unit_value, test_value)
    
    def test_peak_time_slot_property(self):
        """
        Test peak_time_slot property
        """
        test_value = 'lzktnqdglkheenewisvj'
        self.instance.peak_time_slot = test_value
        self.assertEqual(self.instance.peak_time_slot, test_value)
    
    def test_peak_reserve_margin_pct_property(self):
        """
        Test peak_reserve_margin_pct property
        """
        test_value = float(70.26569102202266)
        self.instance.peak_reserve_margin_pct = test_value
        self.assertEqual(self.instance.peak_reserve_margin_pct, test_value)
    
    def test_peak_usage_pct_property(self):
        """
        Test peak_usage_pct property
        """
        test_value = float(99.16924923296624)
        self.instance.peak_usage_pct = test_value
        self.assertEqual(self.instance.peak_usage_pct, test_value)
    
    def test_daily_max_usage_pct_property(self):
        """
        Test daily_max_usage_pct property
        """
        test_value = float(29.28137839192836)
        self.instance.daily_max_usage_pct = test_value
        self.assertEqual(self.instance.daily_max_usage_pct, test_value)
    
    def test_daily_max_usage_time_slot_property(self):
        """
        Test daily_max_usage_time_slot property
        """
        test_value = 'yyqypkyykmqdyuxpjqlq'
        self.instance.daily_max_usage_time_slot = test_value
        self.assertEqual(self.instance.daily_max_usage_time_slot, test_value)
    
    def test_update_datetime_property(self):
        """
        Test update_datetime property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.update_datetime = test_value
        self.assertEqual(self.instance.update_datetime, test_value)
    
    def test_update_datetime_local_property(self):
        """
        Test update_datetime_local property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.update_datetime_local = test_value
        self.assertEqual(self.instance.update_datetime_local, test_value)
    
    def test_area_code_property(self):
        """
        Test area_code property
        """
        test_value = 'yzuhxikwaomhexccaywv'
        self.instance.area_code = test_value
        self.assertEqual(self.instance.area_code, test_value)
    
    def test_area_name_jp_property(self):
        """
        Test area_name_jp property
        """
        test_value = 'scfmexwwvzymgyfhnqvu'
        self.instance.area_name_jp = test_value
        self.assertEqual(self.instance.area_name_jp, test_value)
    
    def test_area_name_en_property(self):
        """
        Test area_name_en property
        """
        test_value = 'ylgzeymhvildpmqspiwh'
        self.instance.area_name_en = test_value
        self.assertEqual(self.instance.area_name_en, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = SupplyCapacity.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = SupplyCapacity.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

