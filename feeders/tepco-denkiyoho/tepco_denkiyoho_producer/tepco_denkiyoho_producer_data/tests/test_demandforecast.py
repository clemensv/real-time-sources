"""
Test case for DemandForecast
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from tepco_denkiyoho_producer_data.jp.tepco.denkiyoho.demandforecast import DemandForecast
import datetime


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
            date=datetime.date.today(),
            time='anbavgnzyefefglcwnsv',
            datetime=datetime.datetime.now(datetime.timezone.utc),
            datetime_local=datetime.datetime.now(datetime.timezone.utc),
            forecast_demand_mw=float(33.92443475027629),
            forecast_demand_jp_unit_value=int(76),
            usage_pct=float(25.849534695113906),
            supply_capacity_mw=float(71.0934944623038),
            supply_capacity_jp_unit_value=int(91),
            area_code='cgmepopzezngzmrkzdjo'
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
        test_value = 'anbavgnzyefefglcwnsv'
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

    def test_forecast_demand_mw_property(self):
        """
        Test forecast_demand_mw property
        """
        test_value = float(33.92443475027629)
        self.instance.forecast_demand_mw = test_value
        self.assertEqual(self.instance.forecast_demand_mw, test_value)

    def test_forecast_demand_jp_unit_value_property(self):
        """
        Test forecast_demand_jp_unit_value property
        """
        test_value = int(76)
        self.instance.forecast_demand_jp_unit_value = test_value
        self.assertEqual(self.instance.forecast_demand_jp_unit_value, test_value)

    def test_usage_pct_property(self):
        """
        Test usage_pct property
        """
        test_value = float(25.849534695113906)
        self.instance.usage_pct = test_value
        self.assertEqual(self.instance.usage_pct, test_value)

    def test_supply_capacity_mw_property(self):
        """
        Test supply_capacity_mw property
        """
        test_value = float(71.0934944623038)
        self.instance.supply_capacity_mw = test_value
        self.assertEqual(self.instance.supply_capacity_mw, test_value)

    def test_supply_capacity_jp_unit_value_property(self):
        """
        Test supply_capacity_jp_unit_value property
        """
        test_value = int(91)
        self.instance.supply_capacity_jp_unit_value = test_value
        self.assertEqual(self.instance.supply_capacity_jp_unit_value, test_value)

    def test_area_code_property(self):
        """
        Test area_code property
        """
        test_value = 'cgmepopzezngzmrkzdjo'
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
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = DemandForecast.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = DemandForecast.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

