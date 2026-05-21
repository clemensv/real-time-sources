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
            date='xnltnfqdlyomxzgdvwcy',
            time='ougxugyrbumuieutfejc',
            datetime='cqbfhohetsjehtnjuwdj',
            datetime_local='azbexftfyaveuxbzngyw',
            forecast_demand_mw=float(61.48926808721163),
            forecast_demand_jp_unit_value=int(12),
            usage_pct=float(93.39123310383005),
            supply_capacity_mw=float(14.638754017511314),
            supply_capacity_jp_unit_value=int(15),
            area_code='dnwwxuezqhtgatgtcfam'
        )
        return instance

    
    def test_date_property(self):
        """
        Test date property
        """
        test_value = 'xnltnfqdlyomxzgdvwcy'
        self.instance.date = test_value
        self.assertEqual(self.instance.date, test_value)
    
    def test_time_property(self):
        """
        Test time property
        """
        test_value = 'ougxugyrbumuieutfejc'
        self.instance.time = test_value
        self.assertEqual(self.instance.time, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'cqbfhohetsjehtnjuwdj'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_datetime_local_property(self):
        """
        Test datetime_local property
        """
        test_value = 'azbexftfyaveuxbzngyw'
        self.instance.datetime_local = test_value
        self.assertEqual(self.instance.datetime_local, test_value)
    
    def test_forecast_demand_mw_property(self):
        """
        Test forecast_demand_mw property
        """
        test_value = float(61.48926808721163)
        self.instance.forecast_demand_mw = test_value
        self.assertEqual(self.instance.forecast_demand_mw, test_value)
    
    def test_forecast_demand_jp_unit_value_property(self):
        """
        Test forecast_demand_jp_unit_value property
        """
        test_value = int(12)
        self.instance.forecast_demand_jp_unit_value = test_value
        self.assertEqual(self.instance.forecast_demand_jp_unit_value, test_value)
    
    def test_usage_pct_property(self):
        """
        Test usage_pct property
        """
        test_value = float(93.39123310383005)
        self.instance.usage_pct = test_value
        self.assertEqual(self.instance.usage_pct, test_value)
    
    def test_supply_capacity_mw_property(self):
        """
        Test supply_capacity_mw property
        """
        test_value = float(14.638754017511314)
        self.instance.supply_capacity_mw = test_value
        self.assertEqual(self.instance.supply_capacity_mw, test_value)
    
    def test_supply_capacity_jp_unit_value_property(self):
        """
        Test supply_capacity_jp_unit_value property
        """
        test_value = int(15)
        self.instance.supply_capacity_jp_unit_value = test_value
        self.assertEqual(self.instance.supply_capacity_jp_unit_value, test_value)
    
    def test_area_code_property(self):
        """
        Test area_code property
        """
        test_value = 'dnwwxuezqhtgatgtcfam'
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
