"""
Test case for PeakDemandForecast
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from tepco_denkiyoho_producer_data.jp.tepco.denkiyoho.peakdemandforecast import PeakDemandForecast


class Test_PeakDemandForecast(unittest.TestCase):
    """
    Test case for PeakDemandForecast
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_PeakDemandForecast.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of PeakDemandForecast for testing
        """
        instance = PeakDemandForecast(
            date='hutjrydgjkfiiccljyng',
            time='odsfcsvoxisevhretycb',
            peak_demand_forecast_mw=float(37.69695482010344),
            peak_demand_forecast_jp_unit_value=int(43),
            peak_time_slot='qqyoragqqhmhufliqawj',
            update_datetime='zpbvawnmtkxlsyfnuyaz',
            update_datetime_local='wsinylsntsfgebkgxlly',
            area_code='mbkgrmsknuokdosldwae',
            area_name_jp='sgkwaysdmhclntlpqroj',
            area_name_en='rbaotsyxlohvclxvyvib'
        )
        return instance

    
    def test_date_property(self):
        """
        Test date property
        """
        test_value = 'hutjrydgjkfiiccljyng'
        self.instance.date = test_value
        self.assertEqual(self.instance.date, test_value)
    
    def test_time_property(self):
        """
        Test time property
        """
        test_value = 'odsfcsvoxisevhretycb'
        self.instance.time = test_value
        self.assertEqual(self.instance.time, test_value)
    
    def test_peak_demand_forecast_mw_property(self):
        """
        Test peak_demand_forecast_mw property
        """
        test_value = float(37.69695482010344)
        self.instance.peak_demand_forecast_mw = test_value
        self.assertEqual(self.instance.peak_demand_forecast_mw, test_value)
    
    def test_peak_demand_forecast_jp_unit_value_property(self):
        """
        Test peak_demand_forecast_jp_unit_value property
        """
        test_value = int(43)
        self.instance.peak_demand_forecast_jp_unit_value = test_value
        self.assertEqual(self.instance.peak_demand_forecast_jp_unit_value, test_value)
    
    def test_peak_time_slot_property(self):
        """
        Test peak_time_slot property
        """
        test_value = 'qqyoragqqhmhufliqawj'
        self.instance.peak_time_slot = test_value
        self.assertEqual(self.instance.peak_time_slot, test_value)
    
    def test_update_datetime_property(self):
        """
        Test update_datetime property
        """
        test_value = 'zpbvawnmtkxlsyfnuyaz'
        self.instance.update_datetime = test_value
        self.assertEqual(self.instance.update_datetime, test_value)
    
    def test_update_datetime_local_property(self):
        """
        Test update_datetime_local property
        """
        test_value = 'wsinylsntsfgebkgxlly'
        self.instance.update_datetime_local = test_value
        self.assertEqual(self.instance.update_datetime_local, test_value)
    
    def test_area_code_property(self):
        """
        Test area_code property
        """
        test_value = 'mbkgrmsknuokdosldwae'
        self.instance.area_code = test_value
        self.assertEqual(self.instance.area_code, test_value)
    
    def test_area_name_jp_property(self):
        """
        Test area_name_jp property
        """
        test_value = 'sgkwaysdmhclntlpqroj'
        self.instance.area_name_jp = test_value
        self.assertEqual(self.instance.area_name_jp, test_value)
    
    def test_area_name_en_property(self):
        """
        Test area_name_en property
        """
        test_value = 'rbaotsyxlohvclxvyvib'
        self.instance.area_name_en = test_value
        self.assertEqual(self.instance.area_name_en, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = PeakDemandForecast.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
