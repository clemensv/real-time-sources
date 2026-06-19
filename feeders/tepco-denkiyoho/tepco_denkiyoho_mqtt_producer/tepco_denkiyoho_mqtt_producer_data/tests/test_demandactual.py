"""
Test case for DemandActual
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from tepco_denkiyoho_mqtt_producer_data.jp.tepco.denkiyoho.demandactual import DemandActual
import datetime


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
            date=datetime.date.today(),
            time='mwonbennbltkrjgonboz',
            datetime=datetime.datetime.now(datetime.timezone.utc),
            datetime_local=datetime.datetime.now(datetime.timezone.utc),
            actual_demand_mw=float(97.1198052185979),
            actual_demand_jp_unit_value=int(73),
            solar_generation_mw=float(8.505989595504781),
            solar_generation_jp_unit_value=int(99),
            solar_share_pct=float(74.12619179733855),
            usage_pct=float(88.46064937047909),
            supply_capacity_mw=float(24.039223269771803),
            supply_capacity_jp_unit_value=int(2),
            area_code='sefpsaiiooqktcakpgud'
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
        test_value = 'mwonbennbltkrjgonboz'
        self.instance.time = test_value
        self.assertEqual(self.instance.time, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_datetime_local_property(self):
        """
        Test datetime_local property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.datetime_local = test_value
        self.assertEqual(self.instance.datetime_local, test_value)
    
    def test_actual_demand_mw_property(self):
        """
        Test actual_demand_mw property
        """
        test_value = float(97.1198052185979)
        self.instance.actual_demand_mw = test_value
        self.assertEqual(self.instance.actual_demand_mw, test_value)
    
    def test_actual_demand_jp_unit_value_property(self):
        """
        Test actual_demand_jp_unit_value property
        """
        test_value = int(73)
        self.instance.actual_demand_jp_unit_value = test_value
        self.assertEqual(self.instance.actual_demand_jp_unit_value, test_value)
    
    def test_solar_generation_mw_property(self):
        """
        Test solar_generation_mw property
        """
        test_value = float(8.505989595504781)
        self.instance.solar_generation_mw = test_value
        self.assertEqual(self.instance.solar_generation_mw, test_value)
    
    def test_solar_generation_jp_unit_value_property(self):
        """
        Test solar_generation_jp_unit_value property
        """
        test_value = int(99)
        self.instance.solar_generation_jp_unit_value = test_value
        self.assertEqual(self.instance.solar_generation_jp_unit_value, test_value)
    
    def test_solar_share_pct_property(self):
        """
        Test solar_share_pct property
        """
        test_value = float(74.12619179733855)
        self.instance.solar_share_pct = test_value
        self.assertEqual(self.instance.solar_share_pct, test_value)
    
    def test_usage_pct_property(self):
        """
        Test usage_pct property
        """
        test_value = float(88.46064937047909)
        self.instance.usage_pct = test_value
        self.assertEqual(self.instance.usage_pct, test_value)
    
    def test_supply_capacity_mw_property(self):
        """
        Test supply_capacity_mw property
        """
        test_value = float(24.039223269771803)
        self.instance.supply_capacity_mw = test_value
        self.assertEqual(self.instance.supply_capacity_mw, test_value)
    
    def test_supply_capacity_jp_unit_value_property(self):
        """
        Test supply_capacity_jp_unit_value property
        """
        test_value = int(2)
        self.instance.supply_capacity_jp_unit_value = test_value
        self.assertEqual(self.instance.supply_capacity_jp_unit_value, test_value)
    
    def test_area_code_property(self):
        """
        Test area_code property
        """
        test_value = 'sefpsaiiooqktcakpgud'
        self.instance.area_code = test_value
        self.assertEqual(self.instance.area_code, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = DemandActual.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = DemandActual.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

