"""
Test case for DemandActual
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from tepco_denkiyoho_producer_data.jp.tepco.denkiyoho.demandactual import DemandActual


class Test_DemandActual(unittest.TestCase):
    """
    Test case for DemandActual
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_DemandActual.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of DemandActual for testing
        """
        instance = DemandActual(
            date='jfibxaqvartgeuebvlxb',
            time='anmueoflgfgjirctudph',
            datetime='tonsiodoyctlnpblvqcn',
            datetime_local='nuznrxokfhmfdonilezb',
            actual_demand_mw=float(74.13787447963816),
            actual_demand_jp_unit_value=int(58),
            solar_generation_mw=float(22.8980771662745),
            solar_generation_jp_unit_value=int(0),
            solar_share_pct=float(45.4920667825047),
            usage_pct=float(29.271525591985682),
            supply_capacity_mw=float(93.28785719127187),
            supply_capacity_jp_unit_value=int(19),
            area_code='emqmuxmehgwffsjgdqon'
        )
        return instance


    def test_date_property(self):
        """
        Test date property
        """
        test_value = 'jfibxaqvartgeuebvlxb'
        self.instance.date = test_value
        self.assertEqual(self.instance.date, test_value)

    def test_time_property(self):
        """
        Test time property
        """
        test_value = 'anmueoflgfgjirctudph'
        self.instance.time = test_value
        self.assertEqual(self.instance.time, test_value)

    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'tonsiodoyctlnpblvqcn'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)

    def test_datetime_local_property(self):
        """
        Test datetime_local property
        """
        test_value = 'nuznrxokfhmfdonilezb'
        self.instance.datetime_local = test_value
        self.assertEqual(self.instance.datetime_local, test_value)

    def test_actual_demand_mw_property(self):
        """
        Test actual_demand_mw property
        """
        test_value = float(74.13787447963816)
        self.instance.actual_demand_mw = test_value
        self.assertEqual(self.instance.actual_demand_mw, test_value)

    def test_actual_demand_jp_unit_value_property(self):
        """
        Test actual_demand_jp_unit_value property
        """
        test_value = int(58)
        self.instance.actual_demand_jp_unit_value = test_value
        self.assertEqual(self.instance.actual_demand_jp_unit_value, test_value)

    def test_solar_generation_mw_property(self):
        """
        Test solar_generation_mw property
        """
        test_value = float(22.8980771662745)
        self.instance.solar_generation_mw = test_value
        self.assertEqual(self.instance.solar_generation_mw, test_value)

    def test_solar_generation_jp_unit_value_property(self):
        """
        Test solar_generation_jp_unit_value property
        """
        test_value = int(0)
        self.instance.solar_generation_jp_unit_value = test_value
        self.assertEqual(self.instance.solar_generation_jp_unit_value, test_value)

    def test_solar_share_pct_property(self):
        """
        Test solar_share_pct property
        """
        test_value = float(45.4920667825047)
        self.instance.solar_share_pct = test_value
        self.assertEqual(self.instance.solar_share_pct, test_value)

    def test_usage_pct_property(self):
        """
        Test usage_pct property
        """
        test_value = float(29.271525591985682)
        self.instance.usage_pct = test_value
        self.assertEqual(self.instance.usage_pct, test_value)

    def test_supply_capacity_mw_property(self):
        """
        Test supply_capacity_mw property
        """
        test_value = float(93.28785719127187)
        self.instance.supply_capacity_mw = test_value
        self.assertEqual(self.instance.supply_capacity_mw, test_value)

    def test_supply_capacity_jp_unit_value_property(self):
        """
        Test supply_capacity_jp_unit_value property
        """
        test_value = int(19)
        self.instance.supply_capacity_jp_unit_value = test_value
        self.assertEqual(self.instance.supply_capacity_jp_unit_value, test_value)

    def test_area_code_property(self):
        """
        Test area_code property
        """
        test_value = 'emqmuxmehgwffsjgdqon'
        self.instance.area_code = test_value
        self.assertEqual(self.instance.area_code, test_value)

    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = DemandActual.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
