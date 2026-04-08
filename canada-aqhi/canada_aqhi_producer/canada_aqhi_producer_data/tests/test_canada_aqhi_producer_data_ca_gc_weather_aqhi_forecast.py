"""
Test case for Forecast
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from canada_aqhi_producer_data.ca.gc.weather.aqhi.forecast import Forecast


class Test_Forecast(unittest.TestCase):
    """
    Test case for Forecast
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Forecast.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Forecast for testing
        """
        instance = Forecast(
            province='wqoihahdywskusbovass',
            community_name='ayqfxfxphdbilodmqwce',
            cgndb_code='gisoitkjrjijnkigocpk',
            publication_datetime='qlqlhcwxvawllxxjlmxq',
            forecast_date='ohyfhwmsxfidqczqkowi',
            forecast_period=int(38),
            forecast_period_label='rohtamzlyjmepgfiwmfq',
            aqhi=int(76),
            aqhi_category='swxdnckeaeabvhpeqymx'
        )
        return instance

    
    def test_province_property(self):
        """
        Test province property
        """
        test_value = 'wqoihahdywskusbovass'
        self.instance.province = test_value
        self.assertEqual(self.instance.province, test_value)
    
    def test_community_name_property(self):
        """
        Test community_name property
        """
        test_value = 'ayqfxfxphdbilodmqwce'
        self.instance.community_name = test_value
        self.assertEqual(self.instance.community_name, test_value)
    
    def test_cgndb_code_property(self):
        """
        Test cgndb_code property
        """
        test_value = 'gisoitkjrjijnkigocpk'
        self.instance.cgndb_code = test_value
        self.assertEqual(self.instance.cgndb_code, test_value)
    
    def test_publication_datetime_property(self):
        """
        Test publication_datetime property
        """
        test_value = 'qlqlhcwxvawllxxjlmxq'
        self.instance.publication_datetime = test_value
        self.assertEqual(self.instance.publication_datetime, test_value)
    
    def test_forecast_date_property(self):
        """
        Test forecast_date property
        """
        test_value = 'ohyfhwmsxfidqczqkowi'
        self.instance.forecast_date = test_value
        self.assertEqual(self.instance.forecast_date, test_value)
    
    def test_forecast_period_property(self):
        """
        Test forecast_period property
        """
        test_value = int(38)
        self.instance.forecast_period = test_value
        self.assertEqual(self.instance.forecast_period, test_value)
    
    def test_forecast_period_label_property(self):
        """
        Test forecast_period_label property
        """
        test_value = 'rohtamzlyjmepgfiwmfq'
        self.instance.forecast_period_label = test_value
        self.assertEqual(self.instance.forecast_period_label, test_value)
    
    def test_aqhi_property(self):
        """
        Test aqhi property
        """
        test_value = int(76)
        self.instance.aqhi = test_value
        self.assertEqual(self.instance.aqhi, test_value)
    
    def test_aqhi_category_property(self):
        """
        Test aqhi_category property
        """
        test_value = 'swxdnckeaeabvhpeqymx'
        self.instance.aqhi_category = test_value
        self.assertEqual(self.instance.aqhi_category, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Forecast.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
