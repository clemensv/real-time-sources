"""
Test case for SupplyCapacity
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from tepco_denkiyoho_producer_data.jp.tepco.denkiyoho.supplycapacity import SupplyCapacity


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
            date='jrzcxhwfphbnqjnpfcmr',
            time='cjumxjuenxbckaaoxnsr',
            peak_supply_capacity_mw=float(56.05572722838406),
            peak_supply_capacity_jp_unit_value=int(9),
            peak_time_slot='oroaasrqxkqqswjckton',
            peak_reserve_margin_pct=float(46.12601192381259),
            peak_usage_pct=float(32.090947390855554),
            daily_max_usage_pct=float(31.038382453917546),
            daily_max_usage_time_slot='wanpmfwmktqmvtphhhmx',
            update_datetime='xhuhsufppuqfizbyztwh',
            update_datetime_local='pnnlrnbtrcydeklwymti',
            area_code='mythlomezkodqhvfqcfj',
            area_name_jp='aczczjpvtdnvdjlcttok',
            area_name_en='szyzntlapyononkznbkw'
        )
        return instance


    def test_date_property(self):
        """
        Test date property
        """
        test_value = 'jrzcxhwfphbnqjnpfcmr'
        self.instance.date = test_value
        self.assertEqual(self.instance.date, test_value)

    def test_time_property(self):
        """
        Test time property
        """
        test_value = 'cjumxjuenxbckaaoxnsr'
        self.instance.time = test_value
        self.assertEqual(self.instance.time, test_value)

    def test_peak_supply_capacity_mw_property(self):
        """
        Test peak_supply_capacity_mw property
        """
        test_value = float(56.05572722838406)
        self.instance.peak_supply_capacity_mw = test_value
        self.assertEqual(self.instance.peak_supply_capacity_mw, test_value)

    def test_peak_supply_capacity_jp_unit_value_property(self):
        """
        Test peak_supply_capacity_jp_unit_value property
        """
        test_value = int(9)
        self.instance.peak_supply_capacity_jp_unit_value = test_value
        self.assertEqual(self.instance.peak_supply_capacity_jp_unit_value, test_value)

    def test_peak_time_slot_property(self):
        """
        Test peak_time_slot property
        """
        test_value = 'oroaasrqxkqqswjckton'
        self.instance.peak_time_slot = test_value
        self.assertEqual(self.instance.peak_time_slot, test_value)

    def test_peak_reserve_margin_pct_property(self):
        """
        Test peak_reserve_margin_pct property
        """
        test_value = float(46.12601192381259)
        self.instance.peak_reserve_margin_pct = test_value
        self.assertEqual(self.instance.peak_reserve_margin_pct, test_value)

    def test_peak_usage_pct_property(self):
        """
        Test peak_usage_pct property
        """
        test_value = float(32.090947390855554)
        self.instance.peak_usage_pct = test_value
        self.assertEqual(self.instance.peak_usage_pct, test_value)

    def test_daily_max_usage_pct_property(self):
        """
        Test daily_max_usage_pct property
        """
        test_value = float(31.038382453917546)
        self.instance.daily_max_usage_pct = test_value
        self.assertEqual(self.instance.daily_max_usage_pct, test_value)

    def test_daily_max_usage_time_slot_property(self):
        """
        Test daily_max_usage_time_slot property
        """
        test_value = 'wanpmfwmktqmvtphhhmx'
        self.instance.daily_max_usage_time_slot = test_value
        self.assertEqual(self.instance.daily_max_usage_time_slot, test_value)

    def test_update_datetime_property(self):
        """
        Test update_datetime property
        """
        test_value = 'xhuhsufppuqfizbyztwh'
        self.instance.update_datetime = test_value
        self.assertEqual(self.instance.update_datetime, test_value)

    def test_update_datetime_local_property(self):
        """
        Test update_datetime_local property
        """
        test_value = 'pnnlrnbtrcydeklwymti'
        self.instance.update_datetime_local = test_value
        self.assertEqual(self.instance.update_datetime_local, test_value)

    def test_area_code_property(self):
        """
        Test area_code property
        """
        test_value = 'mythlomezkodqhvfqcfj'
        self.instance.area_code = test_value
        self.assertEqual(self.instance.area_code, test_value)

    def test_area_name_jp_property(self):
        """
        Test area_name_jp property
        """
        test_value = 'aczczjpvtdnvdjlcttok'
        self.instance.area_name_jp = test_value
        self.assertEqual(self.instance.area_name_jp, test_value)

    def test_area_name_en_property(self):
        """
        Test area_name_en property
        """
        test_value = 'szyzntlapyononkznbkw'
        self.instance.area_name_en = test_value
        self.assertEqual(self.instance.area_name_en, test_value)

    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = SupplyCapacity.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
