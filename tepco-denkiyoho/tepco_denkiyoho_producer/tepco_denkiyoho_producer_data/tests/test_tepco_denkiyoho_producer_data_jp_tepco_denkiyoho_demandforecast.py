"""
Test case for DemandForecast
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from tepco_denkiyoho_producer_data.jp.tepco.denkiyoho.demandforecast import DemandForecast


class Test_DemandForecast(unittest.TestCase):
    """
    Test case for DemandForecast
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_DemandForecast.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of DemandForecast for testing
        """
        instance = DemandForecast(
            date='xrbkcbouusuxldwmcdod',
            time='ptcogfbaawukyhakecrb',
            datetime='odjvwjsuuvevhurfwkns',
            datetime_local='mzwhlyqzpjtragaqrkrf',
            forecast_demand_mw=float(32.089295727134825),
            forecast_demand_jp_unit_value=int(56),
            usage_pct=float(11.674106888219393),
            supply_capacity_mw=float(57.00676291957924),
            supply_capacity_jp_unit_value=int(11),
            area_code='jbgyddgnymyavhsqtkej'
        )
        return instance

    
    def test_date_property(self):
        """
        Test date property
        """
        test_value = 'xrbkcbouusuxldwmcdod'
        self.instance.date = test_value
        self.assertEqual(self.instance.date, test_value)
    
    def test_time_property(self):
        """
        Test time property
        """
        test_value = 'ptcogfbaawukyhakecrb'
        self.instance.time = test_value
        self.assertEqual(self.instance.time, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'odjvwjsuuvevhurfwkns'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_datetime_local_property(self):
        """
        Test datetime_local property
        """
        test_value = 'mzwhlyqzpjtragaqrkrf'
        self.instance.datetime_local = test_value
        self.assertEqual(self.instance.datetime_local, test_value)
    
    def test_forecast_demand_mw_property(self):
        """
        Test forecast_demand_mw property
        """
        test_value = float(32.089295727134825)
        self.instance.forecast_demand_mw = test_value
        self.assertEqual(self.instance.forecast_demand_mw, test_value)
    
    def test_forecast_demand_jp_unit_value_property(self):
        """
        Test forecast_demand_jp_unit_value property
        """
        test_value = int(56)
        self.instance.forecast_demand_jp_unit_value = test_value
        self.assertEqual(self.instance.forecast_demand_jp_unit_value, test_value)
    
    def test_usage_pct_property(self):
        """
        Test usage_pct property
        """
        test_value = float(11.674106888219393)
        self.instance.usage_pct = test_value
        self.assertEqual(self.instance.usage_pct, test_value)
    
    def test_supply_capacity_mw_property(self):
        """
        Test supply_capacity_mw property
        """
        test_value = float(57.00676291957924)
        self.instance.supply_capacity_mw = test_value
        self.assertEqual(self.instance.supply_capacity_mw, test_value)
    
    def test_supply_capacity_jp_unit_value_property(self):
        """
        Test supply_capacity_jp_unit_value property
        """
        test_value = int(11)
        self.instance.supply_capacity_jp_unit_value = test_value
        self.assertEqual(self.instance.supply_capacity_jp_unit_value, test_value)
    
    def test_area_code_property(self):
        """
        Test area_code property
        """
        test_value = 'jbgyddgnymyavhsqtkej'
        self.instance.area_code = test_value
        self.assertEqual(self.instance.area_code, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = DemandForecast.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
